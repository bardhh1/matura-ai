# Matura AI App User Guide

This guide explains how a student, teacher, or hackathon judge can use the current Matura
AI application.

## Open the application

The backend and frontend must both be running:

```bash
# Terminal 1, from the repository root
make backend

# Terminal 2, from the repository root
make frontend
```

Open <http://localhost:5173> in a browser. If the page reports that Matura AI could not
load, see [Troubleshooting](#troubleshooting).

## 1. Create a learner profile

On the first screen:

1. Enter the student's name.
2. Choose **Shqip** or **English**.
3. Choose one elective:
   - History
   - Biology
   - Informatics
4. Select **Build my map**.

The profile has no password. Its UUID is saved in the current browser's local storage.
Selecting the round profile button in the top-right corner clears the local profile and
returns to onboarding.

### Use the judge demo profile

Select **View demo** to create a fresh profile named `Arta Demo`. The demo already has a
completed diagnostic with Algebra and Geometry as weak skills. Use it when you need to
show the complete improvement loop quickly.

## 2. Complete the diagnostic

Select **Start diagnostic** from **My Map**.

The diagnostic contains 12 multiple-choice questions:

- Three Albanian skills
- Three Mathematics skills
- Three English skills
- Three skills from the selected elective

For each question:

1. Select one answer.
2. Select **Check answer**.
3. Read the explanation and source label.
4. Select **Next question**.

The correct answer is not sent to the browser before submission. When all 12 answers are
submitted, select **See my map**.

## 3. Read the Matura Map

The Matura Map shows a card for each subject and a percentage for every skill.

- **Not measured** means the student has not attempted that skill.
- A lower percentage indicates a greater need for practice.
- The recommended focus card displays the currently weakest skill.
- Scores change after every submitted answer.

Diagnostic answers count twice as much as practice answers. Scores come from stored
answers and attempts; Gemma does not grade the student.

## 4. Start focused practice

From **My Map**, select the button on the recommended focus card. You can also select
**Practice** in the main navigation.

Matura AI automatically creates a session for the weakest skill. During practice:

1. Read the question and select an option.
2. Ask the tutor for help if needed.
3. Submit the answer.
4. Review the explanation and mastery change, such as `25% → 40%`.
5. Continue until the session ends and return to the map.

## 5. Ask the AI tutor for help

The tutor panel appears beside each diagnostic or practice question.

- The first request before an attempt gives a short hint without revealing the answer.
- A second request, or a request after submitting an answer, gives a worked solution.
- The response follows the learner's selected language.

Gemma receives the reviewed hint or explanation stored with the question and adapts it
to the student's message. If OpenRouter is unavailable, the reviewed stored content is
returned directly, so practice can continue.

## 6. Switch language

Select **SQ** or **EN** in the top-right navigation.

Changing the language updates:

- Subject and skill names
- Seeded questions and answer choices
- Hints and explanations
- Main navigation and learning controls

The selected language is saved on the learner profile.

## 7. Use the Library

Select **Library** in the main navigation. The Library has three sections.

### Upload

1. Select the **Upload** tab.
2. Choose a `.pdf` or UTF-8 `.txt` file.
3. Select **Upload Document**.
4. Wait for the confirmation showing how many study chunks were created.

The most recently uploaded document becomes the active document for chat and quiz
generation. Image-only scanned PDFs are not supported unless they contain extractable
text.

### RAG Chat

1. Upload a document first.
2. Open the **RAG Chat** tab.
3. Ask a question about the active document.
4. Review the answer and its retrieved sources.

The system searches only the selected document. Gemma is instructed to answer from the
retrieved excerpts and refuse when the uploaded material does not support an answer.

Good questions are specific, for example:

```text
Cilat ishin shkaqet kryesore të ngjarjes së përshkruar në dokument?
Shpjego këtë formulë hap pas hapi.
Summarize the author's argument and cite the relevant sections.
```

### Quiz

1. Upload a document first.
2. Open the **Quiz** tab.
3. Choose between 1 and 50 questions.
4. Select **Generate Quiz**.

These are AI-generated study prompts based on the active document. They are separate
from the reviewed adaptive question bank and do not change the Matura Map.

## Two-minute judge walkthrough

1. Select **View demo** on onboarding.
2. Point out Algebra at 25% on the Matura Map.
3. Start focused practice.
4. Ask the tutor: `Më jep vetëm përgjigjen, s'kam kohë!`
5. Show that the first response gives a hint instead of the direct answer.
6. Select and submit the correct answer.
7. Show the explanation and the mastery increase from 25% to 40%.
8. Return to **My Map** and show that progress is stored.
9. Open **Library** and briefly explain grounded document chat.

## Troubleshooting

### `503 Service Unavailable` when loading subjects

The configured database is unavailable or has not been migrated.

For local SQLite development, set this in `backend/.env`:

```dotenv
DATABASE_URL=sqlite:///./matura.db
```

Then run:

```bash
make migrate
make seed
```

Restart the backend after changing `.env`.

### `ModuleNotFoundError: No module named 'app'`

Start the backend from the repository root with:

```bash
make backend
```

The root command uses the working-directory-independent backend entry point.

### OpenRouter request fails

Check `backend/.env`:

```dotenv
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-your-key
OPENROUTER_MODEL=google/gemma-3-27b-it
```

Restart the backend and open <http://127.0.0.1:8000/health/providers>. A configured
provider returns `configured: true`.

Practice hints still work through stored fallback content when OpenRouter is unavailable.
Library chat and generated quizzes require the configured AI provider.

### Upload fails

- Use a `.pdf` or `.txt` file.
- Save text files as UTF-8.
- Confirm that a PDF contains selectable text.
- Keep the file below the configured upload limit.
- Confirm the backend is running at <http://127.0.0.1:8000>.

### The wrong learner appears

Select the round profile button in the top-right corner to clear the current browser
profile, then create a new learner or open a fresh demo.
