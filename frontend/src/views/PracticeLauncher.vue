<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { getApiError, startPractice } from "../services/api";
import { learner, locale } from "../services/profile";

const router = useRouter();
const error = ref("");
onMounted(async () => {
    if (!learner.value) return router.replace("/");
    try {
        const session = await startPractice(learner.value.id);
        router.replace(`/practice/${session.id}`);
    } catch (err) {
        error.value = locale.value === "sq"
            ? "Përfundo diagnostikimin para se të fillosh praktikën."
            : getApiError(err, "Complete the diagnostic before starting practice.");
    }
});
</script>

<template>
  <section class="page-wrap launcher"><span class="eyebrow">{{ locale === "sq" ? "PRAKTIKË" : "PRACTICE" }}</span><h1>{{ error || (locale === "sq" ? "Po zgjedhim aftësinë e radhës…" : "Choosing your next skill…") }}</h1><button v-if="error" class="primary-button" @click="router.push('/')">{{ locale === "sq" ? "Kthehu te harta" : "Return to map" }}</button></section>
</template>
