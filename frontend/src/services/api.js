import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1",
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


export async function askQuestion(documentId, question) {

    const response = await api.post(
        "/chat/",
        {
            document_id: documentId,
            question: question,
        }
    );

    return response.data;
}


export async function generateQuiz(documentId, number = 10) {

    const response = await api.post(
        "/quiz/generate",
        {
            document_id: documentId,
            number: number,
        }
    );

    return response.data;
}

export async function getCatalog(locale = "sq") { return (await api.get("/catalog/subjects", { params: { locale } })).data; }
export async function createLearner(payload) { return (await api.post("/learners", payload)).data; }
export async function createDemoLearner() { return (await api.post("/demo/learners")).data; }
export async function updateLearner(learnerId, payload) { return (await api.patch(`/learners/${learnerId}`, payload)).data; }
export async function getDashboard(learnerId) { return (await api.get(`/learners/${learnerId}/dashboard`)).data; }
export async function startDiagnostic(learnerId) { return (await api.post(`/learners/${learnerId}/diagnostics`)).data; }
export async function startPractice(learnerId) { return (await api.post(`/learners/${learnerId}/practice`)).data; }
export async function getNextQuestion(sessionId) { return (await api.get(`/sessions/${sessionId}/next`)).data; }
export async function submitAnswer(sessionId, questionId, selectedIndex) {
    return (await api.post(`/sessions/${sessionId}/answers`, { question_id: questionId, selected_index: selectedIndex })).data;
}
export async function requestTutorHelp(learnerId, questionId, message) {
    return (await api.post("/tutor/help", { learner_id: learnerId, question_id: questionId, message })).data;
}


const ACTIVE_DOCUMENT_KEY = "matura-ai.active-document";

export function setActiveDocument(document) {
    localStorage.setItem(
        ACTIVE_DOCUMENT_KEY,
        JSON.stringify({ id: document.id, filename: document.filename })
    );
}


export function getActiveDocument() {
    try {
        return JSON.parse(localStorage.getItem(ACTIVE_DOCUMENT_KEY));
    } catch {
        return null;
    }
}


export function getApiError(error, fallback) {
    return error?.response?.data?.detail || fallback;
}


export default api;
