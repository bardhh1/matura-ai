<template>

    <div class="app">

        <nav class="navbar">

            <div class="logo">
                Matura AI
            </div>

            <div class="nav-links">

                <router-link to="/">
                    Home
                </router-link>

                <router-link to="/chat">
                    Chat
                </router-link>

                <router-link to="/quiz">
                    Quiz
                </router-link>

            </div>

        </nav>


        <router-view />

    </div>

</template>


<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f5f7fb;
    color: #222;
}

.navbar {
    height: 65px;
    padding: 0 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: white;
    border-bottom: 1px solid #ddd;
}

.logo {
    font-size: 20px;
    font-weight: bold;
}

.nav-links {
    display: flex;
    gap: 25px;
}

.nav-links a {
    text-decoration: none;
    color: #444;
}

.nav-links a.router-link-active {
    font-weight: bold;
}

</style>