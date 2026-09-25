<script setup>

import FileUpload from "../components/FileUpload.vue";

</script>


<template>

    <main class="home">

        <div class="hero">

            <h1>
                AI Document Assistant
            </h1>

            <p>
                Upload a document and use AI to ask questions
                and generate study questions.
            </p>

        </div>


        <FileUpload />

    </main>

</template>


<style scoped>

.home {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
}

.hero {
    margin-bottom: 30px;
}

h1 {
    font-size: 40px;
    margin-bottom: 10px;
}

p {
    line-height: 1.6;
}

</style>