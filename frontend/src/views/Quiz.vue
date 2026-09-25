<script setup>

import QuizGenerator from "../components/QuizGenerator.vue";

</script>


<template>

    <main class="page">

        <h1>Quiz Generator</h1>

        <p>
            Generate study questions from your document.
        </p>

        <QuizGenerator />

    </main>

</template>


<style scoped>

.page {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
}

</style>