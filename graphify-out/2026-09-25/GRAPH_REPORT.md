# Graph Report - matura-ai  (2026-09-25)

## Corpus Check
- 76 files · ~35,793 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 450 nodes · 764 edges · 39 communities (33 shown, 6 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 132 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `02dac353`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 27
- Community 28
- graphify reference: extra exports and benchmark
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- AGENTS.md
- extraction-spec.md
- README.md

## God Nodes (most connected - your core abstractions)
1. `LearningRepository` - 33 edges
2. `Settings` - 18 edges
3. `DocumentRepository` - 18 edges
4. `getApiError()` - 18 edges
5. `ApplicationError` - 15 edges
6. `Base` - 14 edges
7. `LearningService` - 14 edges
8. `GenerationClient` - 13 edges
9. `Matura AI` - 13 edges
10. `AppContainer` - 12 edges

## Surprising Connections (you probably didn't know these)
- `GeminiGenerationClient` --uses--> `Settings`  [INFERRED]
  backend/app/services/generation_client.py → backend/app/config.py
- `GenerationClient` --uses--> `Settings`  [INFERRED]
  backend/app/services/generation_client.py → backend/app/config.py
- `OpenRouterGenerationClient` --uses--> `Settings`  [INFERRED]
  backend/app/services/generation_client.py → backend/app/config.py
- `test_generation_provider_requires_its_api_key_only_when_requested()` --calls--> `Settings`  [INFERRED]
  backend/tests/test_llm_service.py → backend/app/config.py
- `AppContainer` --uses--> `EmbeddingService`  [INFERRED]
  backend/app/container.py → backend/app/services/embedding_service.py

## Import Cycles
- None detected.

## Communities (39 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (19): get_settings(), Runtime configuration loaded from environment variables or backend/.env., Settings, AppContainer, create_container(), create_database(), Database, create_app() (+11 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (13): Base, Attempt, Learner, LearningSession, Question, Skill, Subject, TutorInteraction (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (20): ApplicationError, EmptyDocumentError, InvalidLearningStateError, LearnerNotFoundError, LearningSessionNotFoundError, QuestionNotFoundError, UnsupportedDocumentError, UploadTooLargeError (+12 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (16): DocumentNotFoundError, ChatHandler, UUID, DocumentHandler, UUID, QuizHandler, Document, DocumentChunk (+8 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (26): AnswerRequest, AnswerResponse, CatalogResponse, ChatRequest, ChatResponse, DashboardResponse, DocumentResponse, DocumentSummary (+18 more)

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (11): AIProviderError, ConfigurationError, create_generation_client(), GeminiGenerationClient, GenerationClient, OpenRouterGenerationClient, QuizService, Generate quiz questions using only the document. (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.17
Nodes (21): api, createDemoLearner(), createLearner(), getApiError(), getCatalog(), getDashboard(), startDiagnostic(), startPractice() (+13 more)

### Community 7 - "Community 7"
Cohesion: 0.13
Nodes (18): resetProfile(), route, router, toggleLocale(), router, routes, updateLearner(), clearLearner() (+10 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (20): axios, dependencies, axios, vue, vue-router, devDependencies, vite, @vitejs/plugin-vue (+12 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (18): getNextQuestion(), requestTutorHelp(), submitAnswer(), answer(), askTutor(), error, loading, loadNext() (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.24
Nodes (4): EmbeddingService, Convert one piece of text into an embedding vector., Convert multiple document chunks into embedding vectors., SentenceTransformer

### Community 11 - "Community 11"
Cohesion: 0.27
Nodes (7): error, handleUpload(), message, selectedFile, uploading, setActiveDocument(), uploadDocument()

### Community 12 - "Community 12"
Cohesion: 0.27
Nodes (8): activeDocument, createQuiz(), error, loading, number, questions, generateQuiz(), getActiveDocument()

### Community 13 - "Community 13"
Cohesion: 0.25
Nodes (6): activeDocument, loading, messages, question, sendMessage(), askQuestion()

### Community 14 - "Community 14"
Cohesion: 0.53
Nodes (4): create_learner(), test_diagnostic_mastery_practice_and_no_answer_leakage(), test_each_elective_builds_twelve_question_diagnostic(), test_locale_can_change()

### Community 27 - "Community 27"
Cohesion: 0.06
Nodes (33): 1. Create a learner profile, 2. Complete the diagnostic, 3. Read the Matura Map, 4. Start focused practice, `503 Service Unavailable` when loading subjects, 5. Ask the AI tutor for help, 6. Switch language, 7. Use the Library (+25 more)

### Community 28 - "Community 28"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 29 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 30 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 31 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 32 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 33 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

## Knowledge Gaps
- **121 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+116 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `Community 0` to `Community 2`, `Community 4`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `LearningRepository` connect `Community 1` to `Community 2`, `Community 5`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `ApplicationError` connect `Community 2` to `Community 0`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `LearningRepository` (e.g. with `LearningService` and `Mastery`) actually correct?**
  _`LearningRepository` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Settings` (e.g. with `AppContainer` and `GeminiGenerationClient`) actually correct?**
  _`Settings` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `DocumentRepository` (e.g. with `ChatHandler` and `DocumentHandler`) actually correct?**
  _`DocumentRepository` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _121 weakly-connected nodes found - possible documentation gaps or missing edges._