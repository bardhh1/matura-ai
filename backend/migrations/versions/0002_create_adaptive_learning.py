"""Create adaptive learning domain.

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-25
"""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "subjects",
        sa.Column("code", sa.String(32), primary_key=True),
        sa.Column("name_sq", sa.String(100), nullable=False),
        sa.Column("name_en", sa.String(100), nullable=False),
        sa.Column("is_core", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
    )
    op.create_table(
        "learners",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("display_name", sa.String(80), nullable=False),
        sa.Column("preferred_locale", sa.String(2), nullable=False),
        sa.Column("elective_subject_code", sa.String(32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["elective_subject_code"], ["subjects.code"]),
    )
    op.create_table(
        "skills",
        sa.Column("code", sa.String(64), primary_key=True),
        sa.Column("subject_code", sa.String(32), nullable=False),
        sa.Column("name_sq", sa.String(120), nullable=False),
        sa.Column("name_en", sa.String(120), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["subject_code"], ["subjects.code"], ondelete="CASCADE"),
    )
    op.create_index("ix_skills_subject_code", "skills", ["subject_code"])
    op.create_table(
        "questions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("skill_code", sa.String(64), nullable=False),
        sa.Column("prompt_sq", sa.Text(), nullable=False),
        sa.Column("prompt_en", sa.Text(), nullable=False),
        sa.Column("options_sq", sa.JSON(), nullable=False),
        sa.Column("options_en", sa.JSON(), nullable=False),
        sa.Column("correct_index", sa.Integer(), nullable=False),
        sa.Column("hint_sq", sa.Text(), nullable=False),
        sa.Column("hint_en", sa.Text(), nullable=False),
        sa.Column("explanation_sq", sa.Text(), nullable=False),
        sa.Column("explanation_en", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.Integer(), nullable=False),
        sa.Column("source_label", sa.String(255), nullable=False),
        sa.Column("source_chunk_id", sa.Uuid(), nullable=True),
        sa.Column("diagnostic_order", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["skill_code"], ["skills.code"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_chunk_id"], ["document_chunks.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_questions_skill_code", "questions", ["skill_code"])
    op.create_table(
        "learning_sessions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("learner_id", sa.Uuid(), nullable=False),
        sa.Column("kind", sa.String(20), nullable=False),
        sa.Column("target_skill_code", sa.String(64), nullable=True),
        sa.Column("question_ids", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["learner_id"], ["learners.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_skill_code"], ["skills.code"]),
    )
    op.create_index("ix_learning_sessions_learner_id", "learning_sessions", ["learner_id"])
    op.create_table(
        "attempts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("learner_id", sa.Uuid(), nullable=False),
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("question_id", sa.Uuid(), nullable=False),
        sa.Column("selected_index", sa.Integer(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["learner_id"], ["learners.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["session_id"], ["learning_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_attempts_learner_id", "attempts", ["learner_id"])
    op.create_index("ix_attempts_session_id", "attempts", ["session_id"])
    op.create_index("ix_attempts_question_id", "attempts", ["question_id"])
    op.create_index(
        "ix_attempts_session_question", "attempts", ["session_id", "question_id"], unique=True
    )
    op.create_table(
        "tutor_interactions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("learner_id", sa.Uuid(), nullable=False),
        sa.Column("question_id", sa.Uuid(), nullable=False),
        sa.Column("user_message", sa.Text(), nullable=False),
        sa.Column("response", sa.Text(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("used_ai", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["learner_id"], ["learners.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_tutor_interactions_learner_id", "tutor_interactions", ["learner_id"])
    op.create_index("ix_tutor_interactions_question_id", "tutor_interactions", ["question_id"])


def downgrade() -> None:
    op.drop_table("tutor_interactions")
    op.drop_table("attempts")
    op.drop_table("learning_sessions")
    op.drop_table("questions")
    op.drop_table("skills")
    op.drop_table("learners")
    op.drop_table("subjects")
