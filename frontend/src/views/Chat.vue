<script setup>

import ChatBox from "../components/ChatBox.vue";

</script>


<template>

    <main class="page">

        <h1>Document Chat</h1>

        <p>
            Ask questions about your uploaded document.
        </p>

        <ChatBox />

    </main>

</template>


<style scoped>

.page {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
}

</style>