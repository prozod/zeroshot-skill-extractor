import re
import logging
from typing import Dict, List, Any
from collections import defaultdict

from lib.extractors.base_extractor import SkillExtractorBase
from lib.config.model_config import ModelConfig
from lib.processors.text_processor import TextProcessor
from lib.utils.model_utils import get_model_manager
from lib.config.skill_categories import SkillCategories

logger = logging.getLogger(__name__)


class RuleBasedSkillExtractor(SkillExtractorBase):
    def __init__(self, config: ModelConfig, skill_categories: Dict[str, List[str]]):
        super().__init__(config, skill_categories)
        self.text_processor = TextProcessor(config.spacy_model)

    def extract(self, text: str, **kwargs) -> List[Dict[str, Any]]:
        self.validate_input(text)

        text_lower = text.lower()
        found_skills = []
        seen_skills = set()

        for skill in self.all_skills:
            skill_patterns = self.text_processor.create_skill_patterns(skill)
            total_matches = []
            all_positions = []

            for pattern in skill_patterns:
                matches = list(re.finditer(pattern, text_lower))
                if matches:
                    total_matches.extend(matches)
                    all_positions.extend([match.span() for match in matches])

            if total_matches and skill not in seen_skills:
                context = self.text_processor.extract_context_around_match(
                    text, total_matches[0].start(), total_matches[0].end(), context_size=50
                )

                found_skills.append({
                    'skill': skill,
                    'confidence': 0.80,
                    'category': self.categorize_skill(skill),
                    'method': 'rule_based',
                    'context': context,
                    'matches': len(total_matches),
                    'positions': all_positions
                })
                seen_skills.add(skill)

        logger.info(f"Rule-based extraction found {len(found_skills)} skills")
        # print("\n----------- skills found rule-based: \n")
        # for skill in found_skills:
        #     print(f"{skill['skill']} (x{skill['matches']})")

        return found_skills


class ZeroShotSkillExtractor(SkillExtractorBase):

    def __init__(self, config: ModelConfig, skill_categories: Dict[str, List[str]]):
        super().__init__(config, skill_categories)
        self.text_processor = TextProcessor(config.spacy_model)
        self.model_manager = get_model_manager()
        self.classifier = None

    def setup(self):
        self.classifier = self.model_manager.load_zero_shot_classifier(
            self.config.skill_classifier_model,
            use_gpu=self.config.use_gpu,
            cache_key="skill_classifier"
        )

    def extract(self, text: str, candidate_skills: List[str] = None, **kwargs) -> List[Dict[str, Any]]:
        self.validate_input(text)

        if self.classifier is None:
            self.setup()

        # use given candidates or filter from all skills
        if candidate_skills is None:
            candidate_skills = self._get_candidate_skills_from_text(text)

        if not candidate_skills:
            logger.info("No candidate skills found for ZSL verification")
            return []

        logger.info(f"ZSL processing {len(candidate_skills)} candidate skills")

        # split text into chunks for better processing
        chunks = self.text_processor.create_chunks(
            text, self.config.text_chunk_size)
        detected_skills = []

        # process in batches to avoid overwhelming the model
        batch_size = self.config.zsl_batch_size

        for i in range(0, len(candidate_skills), batch_size):
            batch_skills = candidate_skills[i:i + batch_size]

            for chunk_idx, chunk in enumerate(chunks):
                # skip very short chunks
                if len(chunk.split()) < 10:
                    continue
                # all_skills = SkillCategories.get_all_skills_flat(
                #     SkillCategories.get_default_skills())

                try:
                    result = self.classifier(
                        chunk, batch_skills, multi_label=True)

                    if isinstance(result['scores'], list):
                        for skill, score in zip(result['labels'], result['scores']):
                            if score > self.config.confidence_threshold:
                                detected_skills.append({
                                    'skill': skill,
                                    'confidence': score,
                                    'category': self.categorize_skill(skill),
                                    'chunk_index': chunk_idx,
                                    'context': chunk[:100] + "..." if len(chunk) > 100 else chunk,
                                    'method': 'zero_shot'
                                })

                except Exception as e:
                    logger.warning(f"error processing chunk {
                                   chunk_idx} with batch {i}: {e}")
                    continue

        # remove duplicates and keep highest confidence
        unique_skills = {}
        for skill_info in detected_skills:
            skill_name = skill_info['skill']
            if (skill_name not in unique_skills or
                    skill_info['confidence'] > unique_skills[skill_name]['confidence']):
                unique_skills[skill_name] = skill_info

        final_skills = list(unique_skills.values())
        logger.info(f"ZSL extraction found {len(final_skills)} skills")

        # print("\n---------- ZSL SKILL -------------")
        # for skill_info in detected_skills:
        #     skill = skill_info['skill']
        #     confidence = skill_info['confidence']
        #     print(skill, confidence)
        #     print("\n")

        return sorted(final_skills, key=lambda x: x['confidence'], reverse=True)

    def _get_candidate_skills_from_text(self, text: str) -> List[str]:
        text_lower = text.lower()
        candidates = []

        for skill in self.all_skills:
            skill_patterns = self.text_processor.create_skill_patterns(skill)

            for pattern in skill_patterns:
                if re.search(pattern, text_lower):
                    candidates.append(skill)
                    break

        return candidates


class HybridSkillExtractor(SkillExtractorBase):
    def __init__(self, config: ModelConfig, skill_categories: Dict[str, List[str]]):
        super().__init__(config, skill_categories)

        self.rule_based_extractor = RuleBasedSkillExtractor(
            config, skill_categories)
        self.zsl_extractor = ZeroShotSkillExtractor(config, skill_categories)

    def extract(self, text: str, **kwargs) -> Dict[str, Any]:
        self.validate_input(text)

        logger.info("Starting hybrid skill extraction")

        # rule-based extraction
        rule_based_skills = self.rule_based_extractor.extract(text)

        # get candidate skills for ZSL verification
        candidate_skills = [skill['skill'] for skill in rule_based_skills]

        # ZSL verification and additional detection
        zsl_skills = self.zsl_extractor.extract(text, candidate_skills)

        # combine results
        combined_results = self._combine_results(rule_based_skills, zsl_skills)

        return combined_results

    def _combine_results(self, rule_based_skills: List[Dict], zsl_skills: List[Dict]) -> Dict[str, Any]:
        all_skills = {}
        detailed_skills = []

        for skill_info in rule_based_skills:
            skill_name = skill_info['skill']
            all_skills[skill_name] = skill_info

        # add ZSL skills that weren't caught by rules
        for skill_info in zsl_skills:
            skill_name = skill_info['skill']

            if skill_name not in all_skills:
                if skill_info['confidence'] > 0.85:
                    all_skills[skill_name] = skill_info
            else:
                # update existing skill with ZSL confidence if higher
                if skill_info['confidence'] > all_skills[skill_name]['confidence']:
                    all_skills[skill_name]['confidence'] = skill_info['confidence']
                    all_skills[skill_name]['method'] = 'hybrid [ZSL verified] '

        detailed_skills = list(all_skills.values())
        categorized_skills = self._categorize_skills(detailed_skills)
        skill_summary = self._generate_skill_summary(categorized_skills)
        logger.info(f"Hybrid extraction completed: {
                    len(detailed_skills)} skills found")

        return {
            'detailed_skills': detailed_skills,
            'categorized_skills': categorized_skills,
            'skill_summary': skill_summary,
            'extraction_stats': {
                'total_found': len(detailed_skills),
                'rule_based_count': len(rule_based_skills),
                'zsl_count': len(zsl_skills),
                'hybrid_method': True
            },
            'skill_names': list(all_skills.keys())
        }

    def _categorize_skills(self, skill_details: List[Dict]) -> Dict[str, List[Dict]]:
        categorized = defaultdict(list)

        for skill_info in skill_details:
            category = skill_info.get('category', 'other')
            categorized[category].append(skill_info)

        return dict(categorized)

    def _generate_skill_summary(self, categorized_skills: Dict) -> Dict[str, Any]:
        summary = {}
        total_skills = 0

        for category, skills in categorized_skills.items():
            if skills:
                avg_confidence = sum(s.get('confidence', 0)
                                     for s in skills) / len(skills)
                summary[category] = {
                    'count': len(skills),
                    'skills': [s['skill'] for s in skills],
                    'avg_confidence': round(avg_confidence, 3),
                    'top_skill': max(skills, key=lambda x: x.get('confidence', 0))['skill']
                }
                total_skills += len(skills)

        summary['total_skills'] = total_skills
        return summary

    def debug_extract(self, text: str) -> Dict[str, Any]:
        logger.info("=== DEBUG: Starting hybrid skill extraction ===")

        debug_info = {
            'text_preview': text[:500] + "..." if len(text) > 500 else text,
            'text_length': len(text)
        }

        # 1: rule based extraction
        rule_based_skills = self.rule_based_extractor.extract(text)
        debug_info['rule_based'] = {
            'count': len(rule_based_skills),
            'skills': [s['skill'] for s in rule_based_skills],
            'details': rule_based_skills[:5]  # First 5 for preview
        }

        # 2: ZSL extraction
        candidate_skills = [skill['skill'] for skill in rule_based_skills]
        zsl_skills = self.zsl_extractor.extract(text, candidate_skills)
        debug_info['zero_shot'] = {
            'candidates_processed': len(candidate_skills),
            'count': len(zsl_skills),
            'skills': [s['skill'] for s in zsl_skills],
            'details': zsl_skills[:5]  # First 5 for preview
        }

        # 3: combined results
        combined = self._combine_results(rule_based_skills, zsl_skills)
        debug_info['combined'] = {
            'total_unique_skills': len(combined['skill_names']),
            'final_skills': combined['skill_names'],
            'by_category': {cat: len(skills) for cat, skills in combined['categorized_skills'].items()}
        }

        return debug_info
