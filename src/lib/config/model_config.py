from dataclasses import dataclass
from typing import Dict, Any, List
from pathlib import Path

model_path = Path(__file__).parent.resolve() / \
    "../../training/skill_extractor_zsl_model"
model_path = model_path.resolve()
print("Model path:", model_path)


@dataclass
class ModelConfig:
    # nlp model Model
    spacy_model: str = "en_core_web_sm"

    # zero-shot classification models
    # role_classifier_model: str = "facebook/bart-large-mnli"
    role_classifier_model: str = str(model_path)
    # skill_classifier_model: str = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
    skill_classifier_model: str = str(model_path)

    # processing params
    confidence_threshold: float = 0.85
    zsl_batch_size: int = 16
    text_chunk_size: int = 400

    # device settings
    use_gpu: bool = True
    device: int = 0  # GPU device number

    # candidate roles for classification
    candidate_roles: List[str] = None

    def __post_init__(self):
        if self.candidate_roles is None:
            self.candidate_roles = [
                "Frontend Developer",
                "Backend Developer",
                "Full Stack Developer",
                "Data Scientist",
                "Machine Learning Engineer",
                "DevOps Engineer",
                "Mobile Developer",
                "UI/UX Designer",
                "Software Engineer",
                "Data Engineer",
                "Cloud Engineer",
                "Software Architect",
                "Product Manager",
                "Technical Lead",
                "Cybersecurity Specialist"
            ]

    @classmethod
    def get_default_config(cls) -> 'ModelConfig':
        return cls()

    @classmethod
    def get_fast_config(cls) -> 'ModelConfig':
        return cls(
            confidence_threshold=0.6,
            zsl_batch_size=64,
            text_chunk_size=300,
            use_gpu=True
        )

    @classmethod
    def get_accurate_config(cls) -> 'ModelConfig':
        return cls(
            confidence_threshold=0.8,
            zsl_batch_size=16,
            text_chunk_size=800,
            use_gpu=True
        )

    @classmethod
    def get_cpu_config(cls) -> 'ModelConfig':
        return cls(
            use_gpu=False,
            device=-1,
            zsl_batch_size=10,
            text_chunk_size=400
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'spacy_model': self.spacy_model,
            'role_classifier_model': self.role_classifier_model,
            'skill_classifier_model': self.skill_classifier_model,
            'confidence_threshold': self.confidence_threshold,
            'zsl_batch_size': self.zsl_batch_size,
            'text_chunk_size': self.text_chunk_size,
            'use_gpu': self.use_gpu,
            'device': self.device,
            'candidate_roles': self.candidate_roles
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ModelConfig':
        return cls(**config_dict)
