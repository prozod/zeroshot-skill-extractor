import logging
import PyPDF2
from lib.config.model_config import ModelConfig
from .base_extractor import BaseExtractor

logger = logging.getLogger(__name__)


class TextExtractor(BaseExtractor):
    def __init__(self, config: ModelConfig = None):
        super().__init__(config or ModelConfig.get_default_config())

    def extract(self, file_path: str) -> str:
        self.validate_input(file_path)
        if not file_path.lower().endswith(".pdf"):
            raise ValueError("sorry, we only accept PDF for now.")

        return self.extract_from_pdf(file_path)

    def extract_from_pdf(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        text += page_text+"\n"
                    except Exception as e:
                        logger.warning(f"error extracting text from page  {
                                       page_num}: {e}")
                        continue

                if not text.strip():
                    raise ValueError("no text could be extracted from PDF")

                logger.info(f"successfully extracted {
                            len(text)} characters from PDF")
                return text

        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        except Exception as e:
            logger.error(f"krror extracting text from PDF {pdf_path}: {e}")
            raise
