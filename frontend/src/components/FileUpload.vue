<script setup>
import { ref } from "vue";
import { uploadDocument } from "../services/api";

const selectedFile = ref(null);
const uploading = ref(false);
const message = ref("");
const error = ref("");

function handleFileChange(event) {
    selectedFile.value = event.target.files[0];

    message.value = "";
    error.value = "";
}


async function handleUpload() {

    if (!selectedFile.value) {
        error.value = "Please select a PDF or TXT file.";
        return;
    }

    uploading.value = true;
    message.value = "";
    error.value = "";

    try {

        const result = await uploadDocument(
            selectedFile.value
        );

        message.value =
            `${result.message} ${result.chunks} chunks created.`;

    } catch (err) {

        console.error(err);

        error.value =
            "Failed to upload the document.";

    } finally {

        uploading.value = false;
    }
}
</script>


<template>

    <div class="upload-box">

        <h2>Upload Document</h2>

        <p>
            Upload a PDF or TXT document to start asking questions.
        </p>

        <input
            type="file"
            accept=".pdf,.txt"
            @change="handleFileChange"
        />

        <button
            @click="handleUpload"
            :disabled="uploading"
        >
            {{ uploading ? "Processing..." : "Upload Document" }}
        </button>

        <p v-if="message" class="success">
            {{ message }}
        </p>

        <p v-if="error" class="error">
            {{ error }}
        </p>

    </div>

</template>


<style scoped>

.upload-box {
    padding: 25px;
    border: 1px solid #ddd;
    border-radius: 12px;
    background: white;
}

input {
    display: block;
    margin: 15px 0;
}

button {
    padding: 10px 18px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

button:disabled {
    cursor: not-allowed;
}

.success {
    margin-top: 15px;
}

.error {
    margin-top: 15px;
}

</style>