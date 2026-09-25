from pathlib import Path
import pdfplumber


def load_document(file_path: str) -> str:
    """
    Load text from a PDF or TXT file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # TXT file
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    # PDF file
    if path.suffix.lower() == ".pdf":
        text = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text.append(page_text)

        return "\n".join(text)

    raise ValueError("Only PDF and TXT files are supported.")


def chunk_text(text: str, target_words: int = 300) -> list[str]:
    """
    Split document text into chunks.

    Each chunk tries to contain approximately target_words words.
    """

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = []
    current_word_count = 0

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        words = paragraph.split()

        # If adding this paragraph would make the chunk too large,
        # save the current chunk first.
        if current_word_count + len(words) > target_words:
            if current_chunk:
                chunks.append(" ".join(current_chunk))

            current_chunk = []
            current_word_count = 0

        current_chunk.append(paragraph)
        current_word_count += len(words)

    # Add the final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks