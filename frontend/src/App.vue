<script setup>
import { useRoute, useRouter } from "vue-router";
import { updateLearner } from "./services/api";
import { clearLearner, learner, locale, saveLearner, t } from "./services/profile";
const route = useRoute(); const router = useRouter();
async function toggleLocale() { if (!learner.value) return; const next = locale.value === "sq" ? "en" : "sq"; saveLearner(await updateLearner(learner.value.id, { preferred_locale: next })); window.dispatchEvent(new Event("matura-locale-change")); }
function resetProfile() { clearLearner(); router.push("/"); }
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <router-link class="brand" to="/" aria-label="Matura AI home"><span class="brand-mark">M</span><span>Matura AI</span></router-link>
      <nav v-if="learner" class="primary-nav" aria-label="Primary navigation">
        <router-link to="/">{{ t("map") }}</router-link><router-link to="/practice">{{ t("practice") }}</router-link><router-link to="/library">{{ t("library") }}</router-link>
      </nav>
      <div v-if="learner" class="profile-actions"><button class="language-button" type="button" @click="toggleLocale">{{ locale === "sq" ? "SQ" : "EN" }}</button><button class="avatar-button" type="button" :title="learner.display_name" @click="resetProfile">{{ learner.display_name.slice(0, 1).toUpperCase() }}</button></div>
    </header>
    <main id="main-content" :class="{ 'session-main': route.name === 'session' || route.name === 'practice-session' }"><router-view /></main>
  </div>
</template>
