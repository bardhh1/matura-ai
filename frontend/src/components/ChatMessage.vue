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
}

</style>