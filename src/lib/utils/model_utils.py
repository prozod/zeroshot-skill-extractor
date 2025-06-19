"""
Model utilities for loading and managing ML models
"""
import logging
from typing import Any, Optional
import spacy
from transformers import pipeline

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages loading and caching of ML models"""

    def __init__(self):
        self._models = {}
        self._nlp_model = None

    def check_gpu_availability(self) -> bool:
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            logger.warning("PyTorch not installed, using CPU")
            return False

    def load_spacy_model(self, model_name: str = "en_core_web_sm") -> spacy.Language:
        """Load and cache spaCy model"""
        if self._nlp_model is None:
            try:
                self._nlp_model = spacy.load(model_name)
                logger.info(f"Loaded spaCy model: {model_name}")
            except OSError:
                logger.error(
                    f"Please install spaCy model: python -m spacy download {model_name}")
                raise
        return self._nlp_model

    def load_zero_shot_classifier(
        self,
        model_name: str,
        use_gpu: bool = True,
        cache_key: Optional[str] = None
    ) -> Any:
        """Load and cache zero-shot classification model"""
        if cache_key is None:
            cache_key = f"zsl_{model_name}"

        if cache_key not in self._models:
            device = 0 if (use_gpu and self.check_gpu_availability()) else -1

            try:
                model = pipeline(
                    "zero-shot-classification",
                    model=model_name,
                    device=device,
                    multi_label=True
                )
                self._models[cache_key] = model
                logger.info(
                    f"Loaded zero-shot classifier: {model_name} on device {device}")
            except Exception as e:
                logger.error(f"Error loading model {model_name}: {e}")
                raise

        return self._models[cache_key]

    def get_model(self, cache_key: str) -> Optional[Any]:
        return self._models.get(cache_key)

    def clear_cache(self):
        """Clear model cache"""
        self._models.clear()
        self._nlp_model = None
        logger.info("Model cache cleared")

    def get_cache_info(self) -> dict:
        """Get information about cached models"""
        return {
            "cached_models": list(self._models.keys()),
            "spacy_loaded": self._nlp_model is not None,
            "gpu_available": self.check_gpu_availability()
        }


# Global model manager instance
model_manager = ModelManager()


def get_model_manager() -> ModelManager:
    return model_manager


class StopWordsManager:
    """Manages stop words for text processing"""

    def __init__(self):
        self._stop_words = None

    def get_stop_words(self) -> set:
        """Get English stop words"""
        if self._stop_words is None:
            try:
                import nltk
                nltk.download("stopwords", quiet=True)
                from nltk.corpus import stopwords
                self._stop_words = set(stopwords.words("english"))
                logger.info("Loaded NLTK stopwords")
            except Exception:
                # Fallback to basic English stopwords
                self._stop_words = {
                    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
                    "you", "your", "yours", "yourself", "yourselves", "he", "him",
                    "his", "himself", "she", "her", "hers", "herself", "it", "its",
                    "itself", "they", "them", "their", "theirs", "themselves",
                    "what", "which", "who", "whom", "this", "that", "these", "those",
                    "am", "is", "are", "was", "were", "be", "been", "being",
                    "have", "has", "had", "having", "do", "does", "did", "doing",
                    "a", "an", "the", "and", "but", "if", "or", "because", "as",
                    "until", "while", "of", "at", "by", "for", "with", "through",
                    "during", "before", "after", "above", "below", "up", "down",
                    "in", "out", "on", "off", "over", "under", "again", "further",
                    "then", "once"
                }
                logger.info("Using fallback stopwords")

        return self._stop_words


# Global stop words manager
stop_words_manager = StopWordsManager()


def get_stop_words() -> set:
    """Get English stop words"""
    return stop_words_manager.get_stop_words()
