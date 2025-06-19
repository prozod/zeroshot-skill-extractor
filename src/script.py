import re
import sys
import json
import logging
from typing import List, Dict
from pathlib import Path
from lib.utils.model_utils import ModelManager
from lib.config.skill_categories import SkillCategories
from lib.config.model_config import ModelConfig
from lib.processors.text_processor import TextProcessor
from lib.extractors.text_extractor import TextExtractor
from lib.extractors.skill_extractor import RuleBasedSkillExtractor, ZeroShotSkillExtractor, HybridSkillExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeSkillExtractor:
    def setup_models(self):
        logger.info("Loading models...")
        self.model_manager = ModelManager()
        self.nlp = self.model_manager.load_spacy_model(self.config.spacy_model)
        self.role_classifier = self.model_manager.load_zero_shot_classifier(
            self.config.role_classifier_model, self.config.use_gpu)
        self.skill_classifier = self.model_manager.load_zero_shot_classifier(
            self.config.skill_classifier_model, self.config.use_gpu)
        logger.info("Models loaded successfully!")

    def __init__(self, config: ModelConfig = None):
        self.config = config

        # skills
        self.skill_categories = SkillCategories.get_default_skills()
        self.all_candidate_skills = SkillCategories.get_all_skills_flat(
            self.skill_categories)
        self.skill_to_category = SkillCategories.get_skill_to_category_mapping(
            self.skill_categories)

        # extractors
        self.rule_extractor = RuleBasedSkillExtractor(
            config, self.skill_categories)
        self.zsl_extractor = ZeroShotSkillExtractor(
            config, self.skill_categories)
        self.hybrid_extractor = HybridSkillExtractor(
            config, self.skill_categories)
        self.text_extractor = TextExtractor(config)

        # processors
        self.text_processor = TextProcessor(
            spacy_model=self.config.spacy_model)

        self.setup_models()

    def extract_skills_with_zsl(self, text: str) -> List[Dict]:
        return self.zsl_extractor.extract(text)

    def extract_skills_rule_based(self, text: str) -> List[Dict]:
        return self.rule_extractor.extract(text)

    def hybrid_skill_extraction(self, text: str) -> Dict:
        return self.hybrid_extractor.extract(text)

    def classify_role(self, text: str) -> Dict:
        """Classify the target role using zero-shot classification"""
        candidate_roles = [
            "Web Developer",
            "Frontend Developer",
            "Backend Developer",
            "Frontend Engineer",
            "Backend Engineer",
            "SysAdmin",
            "Cloud R&D Engineer",
            "Full Stack Developer",
            "Data Scientist",
            "Machine Learning Engineer",
            "AI Engineer",
            "Artificial Intelligence Engineer",
            "DevOps Engineer",
            "Mobile Developer",
            "UI/UX Designer",
            "Software Engineer",
            "Data Engineer",
            "Cloud Engineer",
            "Software Architect",
            "Product Manager",
            "Technical Lead",
            "Cybersecurity Specialist",
            "iOS Developer",
            "Tehnical Lead",
            "Platform Engineer",
            "Data Engineer",
            "Site Reliability Engineer"
            "Cloud Architect",
            "MLOps",
            "Prompt Engineer",
            "GenAI Engineer",
            "Web3 Developer"
        ]

        # Take a representative sample of the text
        text_sample = text[:3000]

        try:
            result = self.role_classifier(text_sample, candidate_roles)
            return {
                "predicted_role": result["labels"][0],
                "confidence": result["scores"][0],
                "top_3_roles": {
                    role: score
                    for role, score in zip(result["labels"][:3], result["scores"][:3])
                },
            }
        except Exception as e:
            logger.error(f"Error in role classification: {e}")
            return {
                "predicted_role": "Sorry, couldn't predict role.",
                "confidence": 0.0,
                "error": str(e),
            }

    def extract_experience_years(self, text: str) -> List[Dict]:
        """Extract years of experience using regex patterns"""
        patterns = [
            r"(\d+)\+?\s*years?\s*(?:of\s*)?experience",
            r"(\d+)\+?\s*years?\s*in",
            r"experience\s*:?\s*(\d+)\+?\s*years?",
            r"(\d+)\+?\s*years?\s*(?:working|developing|programming)",
        ]

        experiences = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                years = int(match.group(1))
                experiences.append(
                    {
                        "years": years,
                        "context": match.group(0),
                        "position": match.span(),
                    }
                )

        return experiences

    def process_resume(self, pdf_path: str) -> Dict:
        """Main processing function"""
        logger.info(f"Processing resume: {pdf_path}")

        text = self.text_extractor.extract_from_pdf(pdf_path)
        text = self.text_processor.clean_text(text)

        skill_extraction = self.hybrid_skill_extraction(text)

        role_prediction = self.classify_role(text)

        experience_info = self.extract_experience_years(text)

        results = {
            "file_path": pdf_path,
            "predicted_role": role_prediction,
            "skills": skill_extraction,
            "experience": experience_info,
            "text_stats": {
                "length": len(text),
                "words": len(text.split()),
                "sentences": len([sent for sent in self.nlp(text).sents]),
            }
        }

        return results

    def save_results(self, results: Dict, output_path: str):
        """Save results to JSON file"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, default=str, ensure_ascii=False)
        logger.info(f"Results saved to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_pdf>")
        sys.exit(1)

    pdf = sys.argv[1]

    config = ModelConfig.get_accurate_config()
    extractor = ResumeSkillExtractor(config=config)
    results = extractor.process_resume(pdf)

    print("\n======= DETAILED SKILLS =======")
    for skill_info in results["skills"]["detailed_skills"]:
        skill = skill_info.get("skill", "UNKNOWN")
        confidence = skill_info.get("confidence", 0.0)
        source = skill_info.get("method", "N/A")
        matches = skill_info.get("matches", 0)
        print(
            f"- {skill} (confidence: {confidence:.2f}, source: {source}, matches: {matches})")

    print("\n======= EXTRACTION STATISTICS =======")
    stats = results["skills"]["extraction_stats"]
    print(f"Total skills found: {stats['total_found']}")
    print(f"Zero-shot detected: {stats['zsl_count']}")
    print(f"Rule-based detected: {stats['rule_based_count']}\n")

    extractor.save_results(results, "resume_analysis_zsl_results.json")


if __name__ == "__main__":
    main()
