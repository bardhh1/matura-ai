import pytest

from app.errors import EmptyDocumentError, UnsupportedDocumentError
from app.services.document_service import chunk_text, extract_text


def test_chunk_text_splits_long_paragraph_with_overlap():
    text = " ".join(f"word-{index}" for index in range(12))

    chunks = chunk_text(text, target_words=5, overlap_words=2)

    assert chunks == [
        "word-0 word-1 word-2 word-3 word-4",
        "word-3 word-4 word-5 word-6 word-7",
        "word-6 word-7 word-8 word-9 word-10",
        "word-9 word-10 word-11",
    ]


def test_chunk_text_does_not_create_an_overlap_only_tail():
    text = "one two three four five"

    assert chunk_text(text, target_words=5, overlap_words=2) == [text]


def test_extract_text_rejects_unsupported_and_empty_documents():
    with pytest.raises(UnsupportedDocumentError):
        extract_text("notes.docx", b"hello")

    with pytest.raises(EmptyDocumentError):
        extract_text("notes.txt", b"  \n")
