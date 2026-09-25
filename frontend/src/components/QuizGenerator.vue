<script setup>

import { ref } from "vue";
import { generateQuiz, getActiveDocument, getApiError } from "../services/api";


const number = ref(10);

const questions = ref([]);

const loading = ref(false);

const error = ref("");

const activeDocument = ref(getActiveDocument());


async function createQuiz() {

    activeDocument.value = getActiveDocument();
    if (!activeDocument.value?.id) {
        error.value = "Upload a PDF or TXT document on the Home page first.";
        return;
    }

    loading.value = true;

    questions.value = [];

    error.value = "";

    try {

        const result = await generateQuiz(
            activeDocument.value.id,
            number.value
        );

        questions.value = result.questions;

    } catch (err) {

        console.error(err);

        error.value = getApiError(err, "Failed to generate quiz.");

    } finally {

        loading.value = false;
    }
}

</script>


<template>

    <div class="quiz">

        <h2>Generate Quiz</h2>

        <p class="document-name">
            {{ activeDocument?.filename || "No document selected" }}
        </p>

        <div class="controls">

            <label>
                Number of questions:
            </label>

            <input
                v-model.number="number"
                type="number"
                min="1"
                max="50"
            />

            <button
                @click="createQuiz"
                :disabled="loading"
            >
                {{ loading ? "Generating..." : "Generate Quiz" }}
            </button>

        </div>


        <p v-if="error" class="error">
            {{ error }}
        </p>


        <div
            v-for="(question, index) in questions"
            :key="index"
            class="question"
        >

            <strong>
                {{ index + 1 }}.
            </strong>

            {{ question }}

        </div>

    </div>

</template>


<style scoped>

.quiz {
    padding: 25px;
    background: white;
    border-radius: 12px;
}

.controls {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
}

.document-name {
    margin-bottom: 16px;
    color: #666;
}

input {
    width: 70px;
    padding: 8px;
}

button {
    padding: 10px 15px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.question {
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    background: #f5f5f5;
}

</style>
