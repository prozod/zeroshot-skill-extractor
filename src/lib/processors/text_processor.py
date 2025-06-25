import re
import unicodedata
import string
import logging
from typing import List
from ..utils.model_utils import get_model_manager

logger = logging.getLogger(__name__)


class TextProcessor:
    """Handles text preprocessing and chunking"""

    def __init__(self, spacy_model: str = "en_core_web_sm"):
        self.model_manager = get_model_manager()
        self.nlp = self.model_manager.load_spacy_model(spacy_model)

    def clean_text(self, text: str) -> str:
        # replace all control characters (\u0003) with space
        text = ''.join(
            c if unicodedata.category(c)[0] != 'C' else ' '
            for c in text
        )

        # normalize newlines
        text = re.sub(r'\n+', '\n', text)

        # replace excessive whitespace with single space
        text = re.sub(r'[ \t\r\f\v]+', ' ', text)

        return text.strip()

    def extract_sentences(self, text: str) -> List[str]:
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    def create_chunks(self, text: str, chunk_size: int = 500) -> List[str]:
        """split text into chunks for better processing"""
        sentences = self.extract_sentences(text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # check if adding this sentence exceeds chunk size
            if len(current_chunk + " " + sentence) <= chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                # start new chunk with current sentence
                current_chunk = sentence

        # if last chunk is not empty, add it
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def get_text_statistics(self, text: str) -> dict:
        """Get basic text statistics"""
        doc = self.nlp(text)

        return {
            'character_count': len(text),
            'word_count': len(text.split()),
            'sentence_count': len(list(doc.sents)),
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()]),
            'avg_sentence_length': len(text.split()) / max(len(list(doc.sents)), 1)
        }

    def extract_context_around_match(self, text: str, match_start: int, match_end: int,
                                     context_size: int = 50) -> str:
        """Extract context around a text match"""
        start = max(0, match_start - context_size)
        end = min(len(text), match_end + context_size)
        return text[start:end].strip()

    def tokenize_and_filter(self, text: str, min_length: int = 2) -> List[str]:
        """Tokenize text and filter tokens"""
        doc = self.nlp(text.lower())

        tokens = []
        for token in doc:
            # skip punctuation, spaces and stop words
            if (not token.is_punct and
                not token.is_space and
                not token.is_stop and
                    len(token.text) >= min_length):
                tokens.append(token.text)

        return tokens

    def remove_diacritics(self, text: str) -> str:
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )

    def normalize_skill_text(self, skill: str) -> str:
        skill = self.remove_diacritics(skill.lower())
        skill = re.escape(skill)
        skill = skill.replace('.', r'\.')  # escape dots
        skill = skill.replace(' ', r'[-\s]')  # match spaces or hyphens
        return skill

    def create_skill_patterns(self, skill: str) -> List[str]:
        """Create regex patterns for matching skill in text"""
        skill_lower = skill.lower()

        if skill_lower == 'c':
            return [r'(?<!\w)[cC](?!\w)']
        elif skill_lower == 'r':
            return [r'(?<!\w)[rR](?!\w)']
        elif skill_lower == 'c#':
            return [r'(?<!\w)[cC]\#(?!\w)']
        elif skill_lower == 'c++':
            return [r'(?<!\w)[cC]\+\+(?!\w)']

        normalized = self.normalize_skill_text(skill)
        return [rf'(?<![\w+#]){normalized}(?![\w+#])']
