<script setup>
import { ref } from "vue";
import ChatBox from "../components/ChatBox.vue"; import FileUpload from "../components/FileUpload.vue"; import QuizGenerator from "../components/QuizGenerator.vue";
import { locale } from "../services/profile";
const tab = ref("sources");
</script>
<template><section class="library-page page-wrap"><span class="eyebrow">SOURCE LIBRARY</span><h1>{{ locale === "sq" ? "Mëso nga materialet e tua" : "Learn from your own sources" }}</h1><p>{{ locale === "sq" ? "Ngarko materiale të verifikuara, pyet me citime ose krijo pyetje studimi." : "Upload trusted material, ask cited questions, or generate study prompts." }}</p><div class="library-tabs"><button :class="{ active: tab === 'sources' }" @click="tab = 'sources'">{{ locale === "sq" ? "Ngarko" : "Upload" }}</button><button :class="{ active: tab === 'chat' }" @click="tab = 'chat'">Chat</button><button :class="{ active: tab === 'quiz' }" @click="tab = 'quiz'">Quiz</button></div><div class="library-content"><FileUpload v-if="tab === 'sources'" /><ChatBox v-else-if="tab === 'chat'" /><QuizGenerator v-else /></div></section></template>
