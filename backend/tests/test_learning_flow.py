def create_learner(client, locale="sq", elective="history"):
    response = client.post(
        "/api/v1/learners",
        json={
            "display_name": "Arta",
            "preferred_locale": locale,
            "elective_subject_code": elective,
        },
    )
    assert response.status_code == 200
    return response.json()


def test_diagnostic_mastery_practice_and_no_answer_leakage(client):
    learner = create_learner(client)
    initial = client.get(f"/api/v1/learners/{learner['id']}/dashboard").json()
    assert initial["diagnostic_complete"] is False
    assert all(
        skill["score"] is None for subject in initial["subjects"] for skill in subject["skills"]
    )

    session_response = client.post(f"/api/v1/learners/{learner['id']}/diagnostics")
    assert session_response.status_code == 200
    learning_session = session_response.json()
    assert learning_session["total_questions"] == 12

    first = client.get(f"/api/v1/sessions/{learning_session['id']}/next").json()["question"]
    assert "correct_index" not in first
    assert "explanation" not in first
    hint = client.post(
        "/api/v1/tutor/help",
        json={
            "learner_id": learner["id"],
            "question_id": first["id"],
            "message": "Më jep përgjigjen",
        },
    ).json()
    assert hint["level"] == 1
    solution = client.post(
        "/api/v1/tutor/help",
        json={"learner_id": learner["id"], "question_id": first["id"], "message": "Ma shpjego"},
    ).json()
    assert solution["level"] == 2

    last_answer = None
    for _ in range(12):
        next_payload = client.get(f"/api/v1/sessions/{learning_session['id']}/next").json()
        question = next_payload["question"]
        assert question is not None
        last_answer = client.post(
            f"/api/v1/sessions/{learning_session['id']}/answers",
            json={"question_id": question["id"], "selected_index": 0},
        )
        assert last_answer.status_code == 200
    assert last_answer.json()["session_complete"] is True

    dashboard = client.get(f"/api/v1/learners/{learner['id']}/dashboard").json()
    assert dashboard["diagnostic_complete"] is True
    assert dashboard["total_attempts"] == 12
    assert dashboard["weakest_skill"] is not None

    practice = client.post(f"/api/v1/learners/{learner['id']}/practice")
    assert practice.status_code == 200
    assert practice.json()["target_skill_code"] == dashboard["weakest_skill"]["code"]
    practice_question = client.get(f"/api/v1/sessions/{practice.json()['id']}/next").json()[
        "question"
    ]
    result = client.post(
        f"/api/v1/sessions/{practice.json()['id']}/answers",
        json={"question_id": practice_question["id"], "selected_index": 0},
    ).json()
    assert result["mastery_after"] is not None
    assert result["next_action"] == "next_question"


def test_each_elective_builds_twelve_question_diagnostic(client):
    for elective in ("history", "biology", "informatics"):
        learner = create_learner(client, locale="en", elective=elective)
        session = client.post(f"/api/v1/learners/{learner['id']}/diagnostics").json()
        assert session["total_questions"] == 12
        question = client.get(f"/api/v1/sessions/{session['id']}/next").json()["question"]
        assert question["subject"] == "Albanian"


def test_locale_can_change(client):
    learner = create_learner(client, locale="sq")
    updated = client.patch(f"/api/v1/learners/{learner['id']}", json={"preferred_locale": "en"})
    assert updated.status_code == 200
    dashboard = client.get(f"/api/v1/learners/{learner['id']}/dashboard").json()
    assert dashboard["subjects"][0]["name"] == "Albanian"


def test_demo_profile_is_ready_for_focused_practice(client):
    learner = client.post("/api/v1/demo/learners").json()
    dashboard = client.get(f"/api/v1/learners/{learner['id']}/dashboard").json()
    assert dashboard["diagnostic_complete"] is True
    assert dashboard["weakest_skill"]["code"] == "math_algebra"
    practice = client.post(f"/api/v1/learners/{learner['id']}/practice")
    assert practice.status_code == 200
