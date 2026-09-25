import { computed, ref } from "vue";

const PROFILE_KEY = "matura-ai.learner";
const stored = localStorage.getItem(PROFILE_KEY);
export const learner = ref(stored ? JSON.parse(stored) : null);
export const locale = computed(() => learner.value?.preferred_locale || "sq");

export function saveLearner(value) {
    learner.value = value;
    localStorage.setItem(PROFILE_KEY, JSON.stringify(value));
}
export function clearLearner() { learner.value = null; localStorage.removeItem(PROFILE_KEY); }

const copy = {
    sq: { map: "Harta ime", practice: "Praktikë", library: "Biblioteka", tagline: "Mëso atë që të duhet më shumë.", start: "Fillo diagnostikimin", unmeasured: "Pa matur", weakest: "Fokusi i radhës", train: "Ushtro këtë aftësi", attempts: "përgjigje", hello: "Përshëndetje" },
    en: { map: "My Map", practice: "Practice", library: "Library", tagline: "Study what you need most.", start: "Start diagnostic", unmeasured: "Not measured", weakest: "Your next focus", train: "Train this skill", attempts: "answers", hello: "Hello" },
};
export function t(key) { return copy[locale.value]?.[key] || copy.en[key] || key; }
