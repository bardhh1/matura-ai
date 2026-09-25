import uuid


def upload_notes(client):
    response = client.post(
        "/api/v1/documents/upload",
        files={
            "file": (
                "algebra.txt",
                b"An equation states that two expressions are equal.",
                "text/plain",
            )
        },
    )
    assert response.status_code == 200
    return response.json()


def test_upload_chat_quiz_flow(client):
    document = upload_notes(client)

    listed = client.get("/api/v1/documents/")
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == document["id"]

    chat = client.post(
        "/api/v1/chat/",
        json={"document_id": document["id"], "question": "What is an equation?"},
    )
    assert chat.status_code == 200
    assert chat.json()["answer"] == "Grounded answer from chunk 1."
    assert chat.json()["sources"][0]["chunk"] == 1

    quiz = client.post(
        "/api/v1/quiz/generate",
        json={"document_id": document["id"], "number": 3},
    )
    assert quiz.status_code == 200
    assert quiz.json()["questions"] == ["Question 1?", "Question 2?", "Question 3?"]


def test_missing_document_returns_structured_404(client):
    response = client.post(
        "/api/v1/chat/",
        json={"document_id": str(uuid.uuid4()), "question": "What is this?"},
    )

    assert response.status_code == 404
    assert response.json()["code"] == "document_not_found"


def test_invalid_upload_returns_structured_415(client):
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("notes.docx", b"not really a docx", "application/octet-stream")},
    )

    assert response.status_code == 415
    assert response.json()["code"] == "unsupported_document"
