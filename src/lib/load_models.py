import spacy
from transformers import pipeline
import logging

# Remove NLTK imports to avoid punkt_tab issues
import nltk
# from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_nltk(self):
    """Setup text processing tools"""
    # Use spaCy for tokenization instead of NLTK to avoid punkt_tab issues
    try:
        # Try to download NLTK stopwords, but don't fail if it doesn't work
        nltk.download("stopwords", quiet=True)
        self.stop_words = set(stopwords.words("english"))
    except:
        # Fallback to basic English stopwords
        self.stop_words = {
            "i",
            "me",
            "my",
            "myself",
            "we",
            "our",
            "ours",
            "ourselves",
            "you",
            "your",
            "yours",
            "yourself",
            "yourselves",
            "he",
            "him",
            "his",
            "himself",
            "she",
            "her",
            "hers",
            "herself",
            "it",
            "its",
            "itself",
            "they",
            "them",
            "their",
            "theirs",
            "themselves",
            "what",
            "which",
            "who",
            "whom",
            "this",
            "that",
            "these",
            "those",
            "am",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "having",
            "do",
            "does",
            "did",
            "doing",
            "a",
            "an",
            "the",
            "and",
            "but",
            "if",
            "or",
            "because",
            "as",
            "until",
            "while",
            "of",
            "at",
            "by",
            "for",
            "with",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "up",
            "down",
            "in",
            "out",
            "on",
            "off",
            "over",
            "under",
            "again",
            "further",
            "then",
            "once",
        }


def setup_models(self):
    logger.info("Loading models...")

    # spaCy for NLP tasks
    try:
        self.nlp = spacy.load("en_core_web_sm")
    except OSError:
        logger.error(
            "Please install spaCy model: python -m spacy download en_core_web_sm"
        )
        raise

    # Zero-shot classification for role prediction
    self.role_classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=0 if self.check_gpu() else -1,
    )

    # Zero-shot classification for skill detection
    # self.skill_classifier = pipeline(
    #     "zero-shot-classification",
    #     model="microsoft/DialoGPT-medium",  # Alternative: "facebook/bart-large-mnli"
    #     device=0 if self.check_gpu() else -1,
    # )

    # For better skill extraction, you might want to use a more specialized model
    self.skill_classifier = pipeline(
        "zero-shot-classification",
        model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
        device=0 if self.check_gpu() else -1,
    )

    logger.info("Models loaded successfully!")
