<script setup>
import { ref } from "vue";
import { uploadDocument, askQuestion, generateQuiz } from "../services/api";

const fileName = ref("");
const isUploaded = ref(false);
const isUploading = ref(false);

const inputQuestion = ref("");
const messages = ref([]);
const isAsking = ref(false);

// Generator Panel state
const showGenerator = ref(true);
const quizCount = ref(5);
const customPrompt = ref("");
const generatedQuiz = ref([]);
const isGenerating = ref(false);

const handleFileUpload = async (event) => {
  const selectedFile = event.target.files[0];
  if (!selectedFile) return;

  fileName.value = selectedFile.name;
  isUploading.value = true;

  try {
    await uploadDocument(selectedFile);
    isUploaded.value = true;
  } catch (err) {
    alert("Ngarkimi dështoi. Ju lutem kontrolloni lidhjen me serverin.");
  } finally {
    isUploading.value = false;
  }
};

const triggerReplaceFile = () => {
  const fileInput = document.getElementById("pdf-input-hidden");
  if (fileInput) fileInput.click();
};

const sendQuestion = async () => {
  if (!inputQuestion.value.trim() || isAsking.value) return;

  const query = inputQuestion.value;
  messages.value.push({ sender: "user", text: query });
  inputQuestion.value = "";
  isAsking.value = true;

  try {
    const data = await askQuestion(query);
    messages.value.push({ sender: "ai", text: data.answer || data.response || "Nuk u pranua asnjë përgjigje." });
  } catch (err) {
    messages.value.push({ sender: "ai", text: "Gabim gjatë marrjes së përgjigjes." });
  } finally {
    isAsking.value = false;
  }
};

const triggerGenerate = async () => {
  isGenerating.value = true;

  try {
    const data = await generateQuiz(quizCount.value);
    generatedQuiz.value = data.questions || data.quiz || data;
  } catch (err) {
    alert("Dështoi gjenerimi i pyetjeve të kuizit.");
  } finally {
    isGenerating.value = false;
  }
};
</script>

<template>
  <div class="page-container">
    <!-- Navigacioni i sipërm -->
    <header class="navbar">
      <router-link to="/" class="logo">
        Matura<span class="logo-ai">AI</span>
      </router-link>
      <nav class="nav-links">
        <router-link to="/chat" class="nav-btn active">Ngarko & Kuiz</router-link>
        <router-link to="/test-solver" class="nav-link">Zgjidhësi i Testit</router-link>
        <router-link to="/just-ask" class="nav-link">Vetëm Pyet</router-link>
      </nav>
    </header>

    <!-- Përmbajtja Kryesore -->
    <main class="main-content">
      <!-- Hidden file input for Replace action -->
      <input 
        type="file" 
        accept=".pdf" 
        id="pdf-input-hidden" 
        class="hidden-input" 
        @change="handleFileUpload" 
      />

      <!-- Header Section -->
      <section class="page-header flex-between">
        <div>
          <span v-if="!isUploaded" class="section-tag">01 — NGARKO & KUIZ</span>
          <h1 class="page-title">Pyet dokumentin tënd</h1>
          <p class="page-subtitle">
            Ngarko një PDF, pyet çfarëdo rreth tij, pastaj gjenero pyetje ushtruese nga ai.
          </p>
        </div>

        <!-- Butoni Close generator (shfaqet vetëm kur është ngarkuar PDF) -->
        <button 
          v-if="isUploaded && showGenerator" 
          class="close-gen-btn" 
          @click="showGenerator = false"
        >
          <span>&times;</span> Mbyll gjeneruesin
        </button>
        <button 
          v-if="isUploaded && !showGenerator" 
          class="open-gen-btn" 
          @click="showGenerator = true"
        >
           Hap gjeneruesin
        </button>
      </section>

      <!-- PAMJA 1: Para ngarkimit të PDF -->
      <section v-if="!isUploaded" class="upload-container">
        <input 
          type="file" 
          accept=".pdf" 
          id="pdf-upload-main" 
          class="hidden-input" 
          @change="handleFileUpload" 
        />
        <label for="pdf-upload-main" class="dropzone-label">
          <div class="cloud-icon-box">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b52d4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>
              <polyline points="11 13 13 11 15 13"/>
              <line x1="13" y1="11" x2="13" y2="17"/>
            </svg>
          </div>
          <h2 class="drop-title">
            {{ isUploading ? 'Po ngarkohet dokumenti...' : 'Ngarko PDF-në tënde këtu' }}
          </h2>
          <p class="drop-sub">ose kliko për të shfletuar · PDF</p>
        </label>
      </section>

      <!-- PAMJA 2: Pas ngarkimit të PDF -->
      <section v-else class="workspace-container">
        <!-- Shiriti i dokumentit të ngarkuar -->
        <div class="file-status-card">
          <div class="file-info">
            <div class="pdf-badge">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3b52d4" stroke-width="2">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
            </div>
            <span class="file-name">{{ fileName }}</span>
          </div>
          <button class="replace-btn" @click="triggerReplaceFile">Ndrro</button>
        </div>

        <!-- Rrjeta e punës: Chat (Majtas) + Testo Veten (Djathtas) -->
        <div class="workspace-grid" :class="{ 'full-chat': !showGenerator }">
          <!-- Paneli i bisedës -->
          <div class="chat-panel">
            <div class="chat-history">
              <div v-if="messages.length === 0" class="empty-chat-placeholder">
                Bëj pyetjen tënde të parë rreth <strong>{{ fileName }}</strong>.
              </div>

              <div 
                v-for="(msg, idx) in messages" 
                :key="idx" 
                :class="['msg-bubble', msg.sender]"
              >
                {{ msg.text }}
              </div>
            </div>

            <!-- Inputi i bisedës -->
            <div class="chat-input-wrapper">
              <input 
                type="text" 
                v-model="inputQuestion" 
                placeholder="Pyet rreth dokumentit tënd..." 
                @keyup.enter="sendQuestion" 
              />
              <button class="send-btn" @click="sendQuestion" :disabled="isAsking">
                &uarr;
              </button>
            </div>
          </div>

          <!-- Paneli djathtas: Testo Veten -->
          <div v-if="showGenerator" class="generator-panel">
            <div class="gen-header">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b52d4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20h9"/>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
              </svg>
              <h3>Testo Veten</h3>
            </div>

            <div class="gen-body">
              <textarea 
                v-model="customPrompt" 
                placeholder="Opsionale: p.sh. fokusohu në kapitullin 3, bëji më të vështira..."
                class="prompt-textarea"
              ></textarea>

              <div class="gen-controls">
                <div class="number-selector">
                  <button 
                    :class="{ active: quizCount === 3 }" 
                    @click="quizCount = 3"
                  >3</button>
                  <button 
                    :class="{ active: quizCount === 5 }" 
                    @click="quizCount = 5"
                  >5</button>
                  <button 
                    :class="{ active: quizCount === 10 }" 
                    @click="quizCount = 10"
                  >10</button>
                </div>

                <button class="generate-action-btn" @click="triggerGenerate" :disabled="isGenerating">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2l2.4 6.6 6.6 2.4-6.6 2.4L12 20l-2.4-6.6L3 11l6.6-2.4L12 2z"/>
                  </svg>
                  {{ isGenerating ? 'Po gjenerohet...' : 'Gjenero' }}
                </button>
              </div>

              <!-- Zona e shfaqjes së pyetjeve -->
              <div class="quiz-results-area">
                <div v-if="generatedQuiz.length === 0 && !isGenerating" class="empty-quiz-placeholder">
                  Pyetjet tuaja ushtruese do të shfaqen këtu.
                </div>

                <div v-else-if="isGenerating" class="loading-quiz">
                  Po krijohen pyetjet nga dokumenti...
                </div>

                <div v-else class="quiz-questions-list">
                  <div v-for="(q, idx) in generatedQuiz" :key="idx" class="quiz-item">
                    <p class="q-text"><strong>{{ idx + 1 }}.</strong> {{ q.question || q.text || q }}</p>
                    <div v-if="q.options" class="q-options">
                      <button v-for="(opt, oIdx) in q.options" :key="oIdx" class="opt-btn">
                        {{ opt }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&display=swap');

.page-container {
  min-height: 100vh;
  background-color: #f7f6f2;
  font-family: 'Inter', sans-serif;
  color: #1a1a1a;
  display: flex;
  flex-direction: column;
}

/* Navigacioni */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 4rem;
}

.logo {
  text-decoration: none;
  font-family: 'Instrument Serif', serif;
  font-size: 1.85rem;
  color: #111;
    font-weight: 500;
}

.logo-ai {
  font-style: italic;
  color: #3b52d4;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-btn.active {
  background-color: #111827;
  color: #ffffff;
  padding: 0.5rem 1.2rem;
  border-radius: 20px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
}

.nav-link {
  text-decoration: none;
  color: #666;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #111;
}

/* Përmbajtja */
.main-content {
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
  padding: 1rem 4rem 3rem 4rem;
  flex-grow: 1;
}

.hidden-input {
  display: none;
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.section-tag {
  font-size: 0.75rem;
  font-weight: 600;
  color: #3b52d4;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
  display: block;
}

.page-title {
  font-family: 'sora', serif;
  font-size: 3.5rem;
  font-weight: 400;
  color: #111;
  margin-bottom: 0.4rem;
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: #666;
  font-size: 1rem;
  margin-bottom: 2rem;
}

.close-gen-btn, .open-gen-btn {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  font-size: 0.88rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #333;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}

/* PAMJA 1: Dropzone */
.upload-container {
  background: transparent;
  border: 1.5px dashed #d0d5dd;
  border-radius: 24px;
  padding: 5rem 2rem;
  text-align: center;
  margin-top: 1rem;
  transition: border-color 0.2s;
}

.upload-container:hover {
  border-color: #3b52d4;
}

.dropzone-label {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cloud-icon-box {
  width: 48px;
  height: 48px;
  background-color: #eef2ff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.2rem;
}

.drop-title {
  font-family: 'sora', serif;
  font-size: 2.2rem;
  font-weight: 400;
  color: #111;
  margin-bottom: 0.4rem;
}

.drop-sub {
  font-size: 0.9rem;
  color: #888;
}

/* PAMJA 2: Workspace */
.file-status-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 0.9rem 1.2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #eaeaea;
  margin-bottom: 1.5rem;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.pdf-badge {
  background: #eef2ff;
  padding: 0.4rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
}

.file-name {
  font-size: 0.95rem;
  font-weight: 500;
  color: #222;
}

.replace-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 0.9rem;
  cursor: pointer;
}

.replace-btn:hover {
  color: #111;
}

.workspace-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  min-height: 520px;
}

.workspace-grid.full-chat {
  grid-template-columns: 1fr;
}

/* Chat Panel */
.chat-panel {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #eaeaea;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.empty-chat-placeholder {
  color: #888;
  font-size: 0.95rem;
  text-align: center;
  margin-top: 35%;
}

.msg-bubble {
  max-width: 80%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  font-size: 0.9rem;
  line-height: 1.4;
}

.msg-bubble.user {
  align-self: flex-end;
  background: #3b52d4;
  color: white;
}

.msg-bubble.ai {
  align-self: flex-start;
  background: #f3f4f6;
  color: #111;
}

.chat-input-wrapper {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 0.4rem 0.6rem 0.4rem 1rem;
  display: flex;
  align-items: center;
  margin-top: 1rem;
}

.chat-input-wrapper input {
  border: none;
  background: transparent;
  width: 100%;
  outline: none;
  font-size: 0.9rem;
}

.send-btn {
  background: #c7d2fe;
  color: #312e81;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
}

/* Generator Panel (Testo Veten) */
.generator-panel {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #eaeaea;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.gen-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.gen-header h3 {
  font-family: 'sora', serif;
  font-size: 1.8rem;
  font-weight: 400;
  color: #111;
}

.prompt-textarea {
  width: 100%;
  height: 70px;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  font-family: inherit;
  font-size: 0.88rem;
  resize: none;
  outline: none;
  margin-bottom: 1rem;
}

.gen-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.number-selector {
  background: #f1f5f9;
  padding: 3px;
  border-radius: 12px;
  display: flex;
  gap: 2px;
}

.number-selector button {
  border: none;
  background: transparent;
  padding: 0.35rem 0.8rem;
  border-radius: 9px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  color: #666;
}

.number-selector button.active {
  background: #ffffff;
  color: #111;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.generate-action-btn {
  background: #3b52d4;
  color: white;
  border: none;
  padding: 0.55rem 1.2rem;
  border-radius: 20px;
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.quiz-results-area {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-quiz-placeholder {
  color: #888;
  font-size: 0.9rem;
  text-align: center;
}

.loading-quiz {
  color: #3b52d4;
  font-size: 0.9rem;
}

.quiz-questions-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow-y: auto;
  max-height: 280px;
}

.quiz-item {
  background: #f8fafc;
  padding: 0.8rem 1rem;
  border-radius: 10px;
  font-size: 0.88rem;
}

.q-options {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-top: 0.5rem;
}

.opt-btn {
  text-align: left;
  background: white;
  border: 1px solid #cbd5e1;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  font-size: 0.82rem;
  cursor: pointer;
}
</style>