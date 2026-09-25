# Matura AI

Matura AI is a bilingual adaptive study coach for Kosovo's Matura exam. A student takes
a 12-question diagnostic, receives a skill-level Matura Map, and trains the weakest
measured skill. Gemma provides progressive tutoring while grading and mastery remain
deterministic.

![Matura AI dashboard](artifacts/screenshots/dashboard.png)

## Product flow

```mermaid
flowchart LR
    A[Create learner] --> B[12-question diagnostic]
    B --> C[Personal Matura Map]
    C --> D[Weakest skill selected]
    D --> E[Focused practice]
    E --> F[Hint, answer, explanation]
    F --> C
```

The current demonstration includes:

- Albanian and English interface and question content.
- Core subjects: Albanian, Mathematics, and English.
- Electives: History, Biology, or Informatics.
- 54 seeded questions across 18 skills.
- Deterministic grading, mastery, and weakest-skill selection.
- Progressive tutor help: a hint first, then a worked solution.
- A Library for PDF/TXT upload, grounded RAG chat, citations, and quiz generation.
- A pre-diagnosed demo profile for a short judge walkthrough.

For step-by-step product instructions, see the [App User Guide](docs/USER_GUIDE.md).
For the current keep/remove and readiness assessment, see the
[Product Audit](docs/PRODUCT_AUDIT.md).

## Technology

| Layer | Technology |
| --- | --- |
| Frontend | Vue 3, Vue Router, Vite |
| API | FastAPI, Pydantic |
| Persistence | SQLAlchemy 2, Alembic |
| Production database | PostgreSQL with pgvector |
| Local development | SQLite with cosine-similarity fallback |
| Embeddings | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Tutor and generation | Gemma 3 27B through OpenRouter |
| Code intelligence | Graphify |

## Architecture

```mermaid
flowchart LR
    UI[Vue application] --> API[FastAPI routes]
    API --> LS[Learning service]
    API --> RH[RAG handlers]
    LS --> LR[Learning repository]
    RH --> DR[Document repository]
    RH --> EMB[Sentence Transformer]
    RH --> AI[Gemma through OpenRouter]
    LS --> AI
    LR --> DB[(PostgreSQL + pgvector)]
    DR --> DB
```

- `routes` validate HTTP requests and serialize responses.
- `handlers` coordinate document upload, RAG chat, and generated quizzes.
- `services` contain learning, tutoring, retrieval, embedding, and generation logic.
- `store` contains SQLAlchemy repository queries.
- `models` contains API schemas and database entities.
- `migrations` contains the Alembic schema history.
- `frontend/src/views` contains the main user journeys.

Gemma writes explanations, adapts tutor language, answers from retrieved excerpts, and
generates Library study questions. It does not grade answers or calculate mastery.

## Requirements

- Python 3.12
- Node.js and npm
- An [OpenRouter API key](https://openrouter.ai/settings/keys)
- Docker Desktop for the PostgreSQL path, or SQLite for local development

## Quick start with SQLite

SQLite is the fastest way to run the application locally and does not require Docker.

1. Install backend and frontend dependencies:

   ```bash
   make setup
   ```

2. Create the backend environment file:

   ```bash
   cp backend/.env.example backend/.env
   ```

3. Set these values in `backend/.env`:

   ```dotenv
   DATABASE_URL=sqlite:///./matura.db
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=sk-or-v1-your-key
   OPENROUTER_MODEL=google/gemma-3-27b-it
   ```

4. Create the schema and seed the curriculum:

   ```bash
   make migrate
   make seed
   ```

5. Start the backend:

   ```bash
   make backend
   ```

6. In a second terminal, start the frontend:

   ```bash
   make frontend
   ```

Open <http://localhost:5173>. API documentation is available at
<http://127.0.0.1:8000/docs>.

## Run with PostgreSQL and pgvector

Use this path to match the intended production database.

1. Install and start Docker Desktop.
2. Keep the default database URL in `backend/.env`:

   ```dotenv
   DATABASE_URL=postgresql+psycopg://matura:matura@localhost:5432/matura
   ```

3. Start the database, migrate, and seed:

   ```bash
   make db-up
   make migrate
   make seed
   ```

4. Run `make backend` and `make frontend` in separate terminals.

Stop the database with `make db-down`.

## Deterministic mastery

Diagnostic attempts have weight 2 and practice attempts have weight 1:

```text
score = 100 × (1 + weighted correct) / (2 + weighted attempts)
```

An unattempted skill appears as **Not measured**. The recommended skill is selected by
the lowest score, then the fewest attempts, then stable skill order. AI output never
enters this calculation.

## RAG document flow

1. The Library accepts UTF-8 `.txt` and text-readable `.pdf` files.
2. Text is split into overlapping chunks and embedded locally.
3. A student question is embedded with the same model.
4. Retrieval returns relevant chunks from the selected document only.
5. Gemma receives those excerpts and must answer from them with source citations.
6. If the retrieved material is insufficient, the API returns an explicit refusal.

The model does not train on uploaded documents. Retrieved text is supplied temporarily
for each request.

## API surface

Adaptive learning endpoints:

```text
GET   /api/v1/catalog/subjects
POST  /api/v1/learners
PATCH /api/v1/learners/{id}
GET   /api/v1/learners/{id}/dashboard
POST  /api/v1/learners/{id}/diagnostics
POST  /api/v1/learners/{id}/practice
GET   /api/v1/sessions/{id}/next
POST  /api/v1/sessions/{id}/answers
POST  /api/v1/tutor/help
```

Library endpoints:

```text
POST /api/v1/documents/upload
POST /api/v1/chat/
POST /api/v1/quiz/generate
```

## Verification

Run the full backend and frontend gate:

```bash
make verify
```

This runs Ruff, backend tests, and the frontend production build. The backend tests cover
answer leakage, diagnostic selection, mastery calculations, weakest-skill selection,
language switching, tutor progression, AI fallback, and the demo profile.

Health endpoints:

```text
GET /health
GET /health/providers
```

## Graphify

The repository includes a project-scoped Graphify skill and a generated local knowledge
graph. Open [the interactive graph](graphify-out/graph.html) or run:

```bash
graphify query "How does the adaptive learning flow work?"
graphify explain "LearningService"
graphify affected "Question"
graphify update .
```

Graphify's post-commit and post-checkout hooks keep the structural graph current. The
existing graph was built in local `--code-only` mode, so repository content was not sent
to an external model.

## Project status and limitations

- The 54-question bank demonstrates the product and is not an official MAShTI bank.
- Learner profiles have no passwords and persist through a UUID in browser local storage.
- SQLite is intended for local development; use PostgreSQL for deployment.
- Library-generated quizzes are study prompts and do not affect mastery.
- Authentication, ownership controls, rate limiting, moderation, monitoring, and a
  teacher-reviewed production curriculum are required before public launch.
