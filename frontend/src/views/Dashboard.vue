<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { createDemoLearner, createLearner, getCatalog, getDashboard, getApiError, startDiagnostic, startPractice } from "../services/api";
import { learner, locale, saveLearner, t } from "../services/profile";

const router = useRouter();
const route = useRoute();
const dashboard = ref(null); const catalog = ref({ core: [], electives: [] });
const loading = ref(false); const error = ref("");
const form = ref({ display_name: "", preferred_locale: "sq", elective_subject_code: "history" });

async function load() {
    error.value = "";
    try { catalog.value = await getCatalog(locale.value); dashboard.value = learner.value ? await getDashboard(learner.value.id) : null; }
    catch (err) { error.value = getApiError(err, "Matura AI could not load. Check that the API and database are running."); }
}
async function createProfile() {
    loading.value = true; error.value = "";
    try { saveLearner(await createLearner(form.value)); await load(); }
    catch (err) { error.value = getApiError(err, "Could not create the learner profile."); }
    finally { loading.value = false; }
}
async function openDemo() {
    loading.value = true; error.value = "";
    try { saveLearner(await createDemoLearner()); await load(); }
    catch (err) { error.value = getApiError(err, "Could not create the demo profile."); }
    finally { loading.value = false; }
}
async function beginDiagnostic() {
    loading.value = true;
    try { const session = await startDiagnostic(learner.value.id); router.push(`/diagnostic/${session.id}`); }
    catch (err) { error.value = getApiError(err, "Could not start the diagnostic."); }
    finally { loading.value = false; }
}
async function beginPractice() {
    loading.value = true;
    try { const session = await startPractice(learner.value.id); router.push(`/practice/${session.id}`); }
    catch (err) { error.value = getApiError(err, "Could not start practice."); }
    finally { loading.value = false; }
}
function scoreLabel(score) { return score === null ? t("unmeasured") : `${score}%`; }
function onLocaleChange() { load(); }
onMounted(async () => {
    if (route.query.demo === "1" && !learner.value) await openDemo();
    else await load();
    window.addEventListener("matura-locale-change", onLocaleChange);
});
onUnmounted(() => window.removeEventListener("matura-locale-change", onLocaleChange));
</script>

<template>
  <section v-if="!learner" class="onboarding page-wrap">
    <div class="onboarding-copy">
      <span class="eyebrow">MATURA 2027</span>
      <h1>Gjej çfarë nuk di.<br><span>Pastaj përmirësoje.</span></h1>
      <p>Një tutor që mat aftësitë e tua dhe zgjedh ushtrimin e duhur për hapin e radhës.</p>
      <div class="loop-line" aria-label="Learning loop"><span>Diagnostiko</span><i></i><span>Ushtro</span><i></i><span>Përmirëso</span></div>
    </div>
    <form class="onboarding-card" @submit.prevent="createProfile">
      <div><span class="step-label">PROFILI YT / YOUR PROFILE</span><h2>Le ta ndërtojmë hartën tënde</h2></div>
      <label>Emri / Name<input v-model.trim="form.display_name" required minlength="2" autocomplete="name" placeholder="p.sh. Arta" /></label>
      <fieldset><legend>Gjuha / Language</legend><div class="segmented"><label><input v-model="form.preferred_locale" type="radio" value="sq" /><span>Shqip</span></label><label><input v-model="form.preferred_locale" type="radio" value="en" /><span>English</span></label></div></fieldset>
      <label>Lënda zgjedhore / Elective<select v-model="form.elective_subject_code"><option value="history">Histori / History</option><option value="biology">Biologji / Biology</option><option value="informatics">Informatikë / Informatics</option></select></label>
      <p v-if="error" class="error-message" role="alert">{{ error }}</p>
      <button class="primary-button" :disabled="loading">{{ loading ? "..." : "Krijo hartën / Build my map" }}</button>
      <button class="secondary-button" type="button" :disabled="loading" @click="openDemo">Shiko demon 2-minutëshe / View demo</button>
      <small>Pa fjalëkalim. Ky profil ruhet vetëm për demonstrim.</small>
    </form>
  </section>

  <section v-else class="dashboard page-wrap">
    <p v-if="error" class="error-message" role="alert">{{ error }}</p>
    <div v-if="dashboard" class="dashboard-head"><div><span class="eyebrow">{{ t("hello") }}, {{ dashboard.learner.display_name }}</span><h1>{{ t("tagline") }}</h1></div><div class="answer-count"><strong>{{ dashboard.total_attempts }}</strong><span>{{ t("attempts") }}</span></div></div>
    <div v-if="dashboard && !dashboard.diagnostic_complete" class="diagnostic-callout">
      <div class="callout-number">12</div><div><span class="eyebrow">HAPI I PARË / FIRST STEP</span><h2>Ndërto hartën e aftësive</h2><p>Katër lëndë, dymbëdhjetë pyetje, rreth gjashtë minuta.</p></div><button class="primary-button" :disabled="loading" @click="beginDiagnostic">{{ t("start") }}</button>
    </div>
    <template v-if="dashboard && dashboard.diagnostic_complete">
      <div class="focus-card"><div><span class="eyebrow">{{ t("weakest") }}</span><h2>{{ dashboard.weakest_skill.name }}</h2><p>{{ scoreLabel(dashboard.weakest_skill.score) }} · {{ dashboard.weakest_skill.attempts }} {{ t("attempts") }}</p></div><button class="primary-button" :disabled="loading" @click="beginPractice">{{ t("train") }}</button></div>
      <div class="section-heading"><div><span class="eyebrow">MATURA MAP</span><h2>{{ t("map") }}</h2></div><p>Rezultati ndryshon pas çdo përgjigjeje.</p></div>
      <div class="subject-grid"><article v-for="subject in dashboard.subjects" :key="subject.code" class="subject-card"><header><h3>{{ subject.name }}</h3><strong>{{ scoreLabel(subject.score) }}</strong></header><div v-for="skill in subject.skills" :key="skill.code" class="skill-row"><div><span>{{ skill.name }}</span><b>{{ scoreLabel(skill.score) }}</b></div><div class="meter"><span :style="{ width: `${skill.score ?? 0}%` }"></span></div></div></article></div>
    </template>
  </section>
</template>
