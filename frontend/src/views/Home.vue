<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const navigateTo = (path) => {
  router.push(path);
};
</script>

<template>
  <div class="home-container">
    <!-- Navigacioni -->
    <header class="navbar">
      <div class="logo">
        <span class="brand-title">Matura<span class="brand-ai">AI</span></span>
      </div>
      <nav class="nav-links">
        <router-link to="/chat">Ngarko & Kuiz</router-link>
        <router-link to="/test-solver">Zgjidhësi i Testit</router-link>
        <router-link to="/just-ask">Vetëm Pyet</router-link>
      </nav>
    </header>

    <!-- Seksioni Kryesor (Hero) -->
    <main class="hero-section">
      <h1 class="hero-title">
       Asistenti yt për, <span class="italic-highlight">testin e Maturës</span><br />
      
      </h1>
      <p class="hero-subtitle">
        Tutor me AI që lexon materialin tënd, kontrollon testet tuaja<br />
        dhe i përgjigjet çdo gjëje — në pak sekonda.
      </p>

      <!-- Karta e Veçorive -->
      <div class="cards-grid">
        <!-- 01: Ngarko & Kuiz -->
        <div class="feature-card" @click="navigateTo('/chat')">
          <div class="card-header">
            <div class="icon-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <span class="card-number">01</span>
          </div>
          <div class="card-body">
            <h3>Ngarko & Kuiz</h3>
            <p>
              Ngarko një dokument PDF, pyet çfarëdo rreth tij dhe gjenero pyetje ushtruese.
            </p>
          </div>
          <div class="card-footer">
            <span>Hape</span>
            <span class="arrow">&rarr;</span>
          </div>
        </div>

        <!-- 02: Zgjidhësi i Testit -->
        <div class="feature-card" @click="navigateTo('/test-solver')">
          <div class="card-header">
            <div class="icon-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 11l3 3L22 4"/>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
              </svg>
            </div>
            <span class="card-number">02</span>
          </div>
          <div class="card-body">
            <h3>Zgjidhësi i Testit</h3>
            <p>
              Ngarko një test dhe merr përgjigjet — shpejt, ose të shpjeguara plotësisht për të mësuar.
            </p>
          </div>
          <div class="card-footer">
            <span>Hape</span>
            <span class="arrow">&rarr;</span>
          </div>
        </div>

        <!-- 03: Vetëm Pyet -->
        <div class="feature-card" @click="navigateTo('/just-ask')">
          <div class="card-header">
            <div class="icon-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2l2.4 6.6 6.6 2.4-6.6 2.4L12 20l-2.4-6.6L3 11l6.6-2.4L12 2z"/>
              </svg>
            </div>
            <span class="card-number">03</span>
          </div>
          <div class="card-body">
            <h3>Vetëm Pyet</h3>
            <p>
              Bëj çfarëdo pyetjeje dhe merr përgjigje të qarta të bazuara nga burime të hapura.
            </p>
          </div>
          <div class="card-footer">
            <span>Hape</span>
            <span class="arrow">&rarr;</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
  background-color: #f7f6f2;
  display: flex;
  flex-direction: column;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.8rem 4rem;
}

.brand-title {
  font-family: 'Instrument Serif', serif;
  font-size: 1.85rem;
  font-weight: 500;
}

.brand-ai {
  font-style: italic;
  color: #3b52d4;
}

.nav-links {
  display: flex;
  gap: 2.5rem;
}

.nav-links a {
  text-decoration: none;
  color: #555;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.nav-links a:hover {
  color: #111;
}

.hero-section {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 2rem 5rem 2rem;
  text-align: center;
  flex-grow: 1;
}

.hero-title {
  font-family: 'Sora', serif;
  font-size: 4.8rem;
  line-height: 1.05;
  font-weight: 400;
  letter-spacing: -0.03em;
  margin-bottom: 1.5rem;
  color: #111;
}

.italic-highlight {
  font-style: italic;
  color: #3b52d4;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: 4rem;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.feature-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 2.25rem;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 290px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.icon-box {
  width: 42px;
  height: 42px;
  background-color: #0f172a;
  color: #ffffff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-number {
  font-family: 'sora', serif;
  font-size: 1.3rem;
  color: #999;
  font-style: italic;
}

.card-body h3 {
  font-family: 'sora', serif;
  font-size: 1.85rem;
  font-weight: 400;
  margin-bottom: 0.5rem;
  color: #111;
}

.card-body p {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.45;
}

.card-footer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: #111;
}

.arrow {
  transition: transform 0.2s ease;
}

.feature-card:hover .arrow {
  transform: translateX(4px);
}

@media (max-width: 900px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
  .hero-title {
    font-size: 3.2rem;
  }
}
</style>