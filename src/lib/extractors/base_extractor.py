"""
Base extractor class for all extractors
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from ..config.model_config import ModelConfig


class BaseExtractor(ABC):
    def __init__(self, config: ModelConfig):
        self.config = config
        # self.setup()

    # def setup(self):  # called during initialization - override if needed
    #     pass

    @abstractmethod
    def extract(self, text: str, **kwargs) -> Any:
        """Extract information from text. Must be implemented by subclasses."""
        pass

    def validate_input(self, path: str) -> bool:
        if not isinstance(path, str):
            raise TypeError("Path must be a string")

        if not path.strip():
            raise ValueError("Path cannot be empty")

        return True

    def get_extraction_metadata(self) -> Dict[str, Any]:
        return {
            'extractor_type': self.__class__.__name__,
            'config': self.config.to_dict() if hasattr(self.config, 'to_dict') else str(self.config)
        }


class SkillExtractorBase(BaseExtractor):
    def __init__(self, config: ModelConfig, skill_categories: Dict[str, List[str]]):
        self.skill_categories = skill_categories
        self.all_skills = self._flatten_skills(skill_categories)
        self.skill_to_category = self._create_skill_mapping(skill_categories)
        super().__init__(config)

    def _flatten_skills(self, skill_categories: Dict[str, List[str]]) -> List[str]:
        all_skills = []
        for skills in skill_categories.values():
            all_skills.extend(skills)
        return all_skills

    def _create_skill_mapping(self, skill_categories: Dict[str, List[str]]) -> Dict[str, str]:
        mapping = {}
        for category, skills in skill_categories.items():
            for skill in skills:
                mapping[skill] = category
        return mapping

    def categorize_skill(self, skill: str) -> str:
        return self.skill_to_category.get(skill, 'other')
