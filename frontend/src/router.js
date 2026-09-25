import { createRouter, createWebHistory } from "vue-router";

import Home from "./views/Home.vue";
import Chat from "./views/Chat.vue";
import Quiz from "./views/Quiz.vue";


const routes = [

    {
        path: "/",
        component: Home
    },

    {
        path: "/chat",
        component: Chat
    },

    {
        path: "/quiz",
        component: Quiz
    }

];


const router = createRouter({

    history: createWebHistory(),

    routes

});


export default router;
