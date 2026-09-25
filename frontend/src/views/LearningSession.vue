<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getApiError, getNextQuestion, requestTutorHelp, submitAnswer } from "../services/api";
import { learner, locale } from "../services/profile";

const route = useRoute(); const router = useRouter();
const payload = ref(null); const selected = ref(null); const result = ref(null);
const loading = ref(false); const error = ref(""); const tutorMessage = ref(""); const tutorReplies = ref([]);
const sq = computed(() => locale.value === "sq"); const question = computed(() => payload.value?.question);

async function loadNext() {
  loading.value = true; error.value = ""; selected.value = null; result.value = null; tutorReplies.value = [];
  try { payload.value = await getNextQuestion(route.params.sessionId); if (!payload.value.question) router.push("/"); }
  catch (err) { error.value = getApiError(err, "Could not load the next question."); }
  finally { loading.value = false; }
}
async function answer() {
  if (selected.value === null) return; loading.value = true;
  try { result.value = await submitAnswer(route.params.sessionId, question.value.id, selected.value); }
  catch (err) { error.value = getApiError(err, "Could not save the answer."); }
  finally { loading.value = false; }
}
async function askTutor() {
  if (!tutorMessage.value.trim()) return; const message = tutorMessage.value; tutorMessage.value = ""; loading.value = true;
  try { const reply = await requestTutorHelp(learner.value.id, question.value.id, message); tutorReplies.value.push({ message, ...reply }); }
  catch (err) { error.value = getApiError(err, "Tutor help is temporarily unavailable."); }
  finally { loading.value = false; }
}
function proceed() { result.value.session_complete ? router.push("/") : loadNext(); }
onMounted(loadNext);
</script>

<template>
  <section class="session-page page-wrap">
    <p v-if="error" class="error-message" role="alert">{{ error }}</p>
    <template v-if="question">
      <div class="session-progress"><button class="text-button" type="button" @click="router.push('/')">← {{ sq ? "Harta" : "Map" }}</button><span>{{ question.subject }} · {{ question.skill }}</span><strong>{{ question.position }} / {{ question.total }}</strong></div>
      <div class="progress-track"><span :style="{ width: `${(question.position / question.total) * 100}%` }"></span></div>
      <div class="learning-layout">
        <article class="question-panel"><span class="eyebrow">{{ payload.session.kind === "diagnostic" ? (sq ? "DIAGNOSTIKIM" : "DIAGNOSTIC") : (sq ? "PRAKTIKË E FOKUSUAR" : "FOCUSED PRACTICE") }}</span><h1>{{ question.prompt }}</h1>
          <div class="options" role="radiogroup"><button v-for="(option, index) in question.options" :key="option" type="button" :disabled="!!result" :class="{ selected: selected === index, correct: result && index === result.correct_index, wrong: result && selected === index && !result.correct }" @click="selected = index"><span>{{ String.fromCharCode(65 + index) }}</span>{{ option }}</button></div>
          <button v-if="!result" class="primary-button answer-button" :disabled="selected === null || loading" @click="answer">{{ sq ? "Kontrollo përgjigjen" : "Check answer" }}</button>
          <div v-else class="result-box" :class="{ success: result.correct }"><div><strong>{{ result.feedback }}</strong><span>{{ result.mastery_before ?? 50 }}% → {{ result.mastery_after }}%</span></div><p>{{ result.explanation }}</p><small>{{ result.source_label }}</small><button class="primary-button" @click="proceed">{{ result.session_complete ? (sq ? "Shiko hartën" : "See my map") : (sq ? "Pyetja tjetër" : "Next question") }}</button></div>
        </article>
        <aside class="tutor-panel"><div><span class="tutor-icon">AI</span><div><strong>Matura Tutor</strong><small>{{ sq ? "Ndihmë pa ta marrë mendimin" : "Help without taking over" }}</small></div></div><p>{{ sq ? "Kërko një udhëzim. Në kërkesën e parë jap vetëm një hint; zgjidhjen e plotë pas tentimit." : "Ask for guidance. The first request gives a hint; the full solution comes after an attempt." }}</p><div v-for="reply in tutorReplies" :key="reply.message" class="tutor-reply"><small>{{ reply.level === 1 ? "HINT" : "SOLUTION" }}</small>{{ reply.response }}</div><form @submit.prevent="askTutor"><label for="tutor-message">{{ sq ? "Pyet tutorin" : "Ask the tutor" }}</label><textarea id="tutor-message" v-model="tutorMessage" :placeholder="sq ? 'Më jep vetëm përgjigjen...' : 'Just give me the answer...'" rows="3"></textarea><button class="secondary-button" :disabled="loading">{{ sq ? "Kërko ndihmë" : "Ask for help" }}</button></form></aside>
      </div>
    </template>
  </section>
</template>
