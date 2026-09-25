import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    },
});


export async function uploadDocument(file) {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/documents/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
}


export async function askQuestion(question) {

    const response = await api.post(
        "/chat/",
        {
            question: question,
        }
    );

    return response.data;
}


export async function generateQuiz(number = 10) {

    const response = await api.post(
        "/quiz/generate",
        {
            number: number,
        }
    );

    return response.data;
}


export default api;