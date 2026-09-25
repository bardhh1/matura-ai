<script setup>

import { ref } from "vue";
import { askQuestion, getActiveDocument, getApiError } from "../services/api";
import ChatMessage from "./ChatMessage.vue";


const question = ref("");

const loading = ref(false);

const messages = ref([]);

const activeDocument = ref(getActiveDocument());


async function sendMessage() {

    if (!question.value.trim()) {
        return;
    }

    activeDocument.value = getActiveDocument();
    if (!activeDocument.value?.id) {
        messages.value.push({
            role: "assistant",
            content: "Upload a PDF or TXT document on the Home page first."
        });
        return;
    }

    const userQuestion = question.value;

    messages.value.push({
        role: "user",
        content: userQuestion
    });

    question.value = "";

    loading.value = true;

    try {

        const result = await askQuestion(
            activeDocument.value.id,
            userQuestion
        );

        messages.value.push({
            role: "assistant",
            content: result.answer,
            sources: result.sources
        });

    } catch (error) {

        console.error(error);

        messages.value.push({
            role: "assistant",
            content: getApiError(error, "Something went wrong while contacting the server.")
        });

    } finally {

        loading.value = false;
    }
}

</script>


<template>

    <div class="chat-container">

        <div class="document-bar">
            {{ activeDocument?.filename || "No document selected" }}
        </div>

        <div class="messages">

            <ChatMessage
                v-for="(message, index) in messages"
                :key="index"
                :message="message"
            />

            <div v-if="loading" class="loading">
                AI is thinking...
            </div>

        </div>


        <form
            class="chat-input"
            @submit.prevent="sendMessage"
        >

            <input
                v-model="question"
                type="text"
                placeholder="Ask something about your document..."
            />

            <button
                type="submit"
                :disabled="loading"
            >
                Send
            </button>

        </form>

    </div>

</template>


<style scoped>

.chat-container {
    display: flex;
    flex-direction: column;
    height: 600px;
    border: 1px solid #ddd;
    border-radius: 12px;
    background: white;
}

.document-bar {
    padding: 10px 15px;
    border-bottom: 1px solid #ddd;
    color: #666;
    font-size: 14px;
}

.messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}

.loading {
    padding: 10px;
}

.chat-input {
    display: flex;
    gap: 10px;
    padding: 15px;
    border-top: 1px solid #ddd;
}

.chat-input input {
    flex: 1;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
}

.chat-input button {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

</style>
