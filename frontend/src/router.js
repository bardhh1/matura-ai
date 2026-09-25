import { createRouter, createWebHistory } from "vue-router";

import Dashboard from "./views/Dashboard.vue";
import LearningSession from "./views/LearningSession.vue";
import Library from "./views/Library.vue";
import PracticeLauncher from "./views/PracticeLauncher.vue";


const routes = [

    {
        path: "/",
        component: Dashboard
    },

    {
        path: "/diagnostic/:sessionId",
        name: "session",
        component: LearningSession
    },

    {
        path: "/practice/:sessionId",
        name: "practice-session",
        component: LearningSession
    },
    {
        path: "/practice",
        component: PracticeLauncher
    },
    {
        path: "/library",
        component: Library
    }

];


const router = createRouter({

    history: createWebHistory(),

    routes

});


export default router;
