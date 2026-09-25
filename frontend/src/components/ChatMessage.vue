<script setup>

defineProps({
    message: {
        type: Object,
        required: true
    }
});

</script>


<template>

    <div
        class="message"
        :class="message.role"
    >

        <div class="message-label">
            {{ message.role === "user" ? "You" : "AI Assistant" }}
        </div>

        <div class="message-text">
            {{ message.content }}
        </div>

        <details v-if="message.sources?.length" class="sources">
            <summary>{{ message.sources.length }} sources</summary>
            <div v-for="source in message.sources" :key="source.chunk" class="source">
                <strong>Chunk {{ source.chunk }}</strong>
                <span>{{ Math.round(source.score * 100) }}% match</span>
                <p>{{ source.excerpt }}</p>
            </div>
        </details>

    </div>

</template>


<style scoped>

.message {
    margin-bottom: 15px;
    padding: 12px 16px;
    border-radius: 12px;
    max-width: 75%;
}

.user {
    margin-left: auto;
    background: #e8f0ff;
}

.assistant {
    margin-right: auto;
    background: #f1f1f1;
}

.message-label {
    font-weight: bold;
    margin-bottom: 5px;
}

.message-text {
    line-height: 1.5;
    white-space: pre-wrap;
}

.sources {
    margin-top: 12px;
    font-size: 13px;
}

.source {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #ddd;
}

.source span {
    margin-left: 8px;
    color: #666;
}

</style>
