from io import BytesIO
from pathlib import Path

import pdfplumber

from app.errors import EmptyDocumentError, UnsupportedDocumentError


def extract_text(filename: str, content: bytes) -> str:
    """Extract UTF-8 text or text from a PDF without writing user files to disk."""

    suffix = Path(filename).suffix.lower()
    if suffix == ".txt":
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise UnsupportedDocumentError("TXT files must use UTF-8 encoding") from exc
    elif suffix == ".pdf":
        try:
            with pdfplumber.open(BytesIO(content)) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
        except Exception as exc:
            raise UnsupportedDocumentError("The PDF could not be read") from exc
        text = "\n\n".join(page for page in pages if page.strip())
    else:
        raise UnsupportedDocumentError("Only PDF and TXT files are supported")

    normalized = "\n".join(line.rstrip() for line in text.replace("\x00", "").splitlines()).strip()
    if not normalized:
        raise EmptyDocumentError("The document does not contain extractable text")
    return normalized


def chunk_text(text: str, target_words: int = 300, overlap_words: int = 50) -> list[str]:
    """Create fixed-size overlapping chunks so long paragraphs are never left unsplit."""

    if target_words <= 0:
        raise ValueError("target_words must be positive")
    if overlap_words < 0 or overlap_words >= target_words:
        raise ValueError("overlap_words must be between 0 and target_words")

    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + target_words, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap_words
    return chunks
