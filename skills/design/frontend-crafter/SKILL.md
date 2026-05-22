---
name: frontend-crafter
description: Especialista em Frontend Mobile-First, UX Black & Orange, Sistema de Cache Offline (IndexedDB), Navegação SPA v3.0 e Performance. Use para criar/ajustar telas, componentes, otimizar CSS/JS, implementar patterns de cache ou debugging de frontend issues.
allowed-tools: Read, Grep, LS, Bash, Edit
---

# Frontend Crafter Skill (Mobile-First Master)

## 🎯 Missão
Criar experiências frontend excepcionais para o Super Cartola Manager com foco em mobile-first, performance e UX consistente.

---

## 1. 🎨 Design System - Black & Orange

### 1.1 Paleta de Cores

```css
:root {
  /* === PRIMÁRIAS === */
  --laranja: #FF4500;           /* Cor principal */
  --laranja-hover: #FF5500;     /* Hover states */
  --laranja-dark: #CC3700;      /* Variação escura */
  
  /* === BACKGROUNDS === */
  --bg-card: #1a1a1a;           /* Cards dark */
  --bg-secondary: #2a2a2a;      /* Seções alternadas */
  --bg-overlay: rgba(0,0,0,0.8);/* Modals/overlays */
  
  /* === STATUS === */
  --verde-lucro: #10b981;       /* Lucro/Vitória */
  --vermelho-prejuizo: #ef4444; /* Prejuízo/Derrota */
  --amarelo-neutro: #f59e0b;    /* Neutro/Atenção */
  
  /* === TEXTOS === */
  --text-primary: #ffffff;
  --text-secondary: #a0a0a0;
  --text-muted: #666666;
  
  /* === BORDAS === */
  --border-color: #333333;
  --border-radius: 12px;
}
```

### 1.2 Typography (TRES FONTES OBRIGATORIAS)

```css
/* OBRIGATORIO: Sistema de 3 fontes */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Russo+One&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* === FAMILIAS DE FONTE === */
  --font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-family-brand: 'Russo One', sans-serif;  /* Titulos, stats, CTAs */
  --font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;  /* Codigo, numeros */
}

body {
  font-family: var(--font-family-base);
  -webkit-font-smoothing: antialiased;
}

/* INTER - Corpo de texto (padrao) */
.body { font-family: var(--font-family-base); font-size: 16px; font-weight: 400; }
.small { font-family: var(--font-family-base); font-size: 14px; font-weight: 400; }
.caption { font-family: var(--font-family-base); font-size: 12px; font-weight: 500; }

/* RUSSO ONE - Titulos e destaques (brand) */
.font-brand { font-family: var(--font-family-brand); font-weight: 400; }
.h1 { font-family: var(--font-family-brand); font-size: 28px; letter-spacing: 0.5px; }
.h2 { font-family: var(--font-family-brand); font-size: 24px; letter-spacing: 0.5px; }
.h3 { font-family: var(--font-family-brand); font-size: 20px; letter-spacing: 0.3px; }

/* JETBRAINS MONO - Codigo e numeros tabulares */
.font-mono { font-family: var(--font-family-mono); }
.tabular-nums { font-variant-numeric: tabular-nums; }
```

**REGRA:** Russo One so tem peso 400, usar `letter-spacing` para ajustar espacamento.

### 1.3 Componentes Base

```html
<!-- Card Padrão -->
<div class="card">
  <div class="card-header">
    <h3>Título</h3>
  </div>
  <div class="card-body">
    <!-- Conteúdo -->
  </div>
</div>

<style>
.card {
  background: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
</style>

<!-- Botão Primário -->
<button class="btn-primary">
  <i class="material-icons">check</i>
  Confirmar
</button>

<style>
.btn-primary {
  background: linear-gradient(135deg, var(--laranja), var(--laranja-dark));
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 69, 0, 0.4);
}
</style>
```

### 1.4 Icons - Material Icons OBRIGATÓRIO

```html
<!-- NUNCA usar emojis, SEMPRE Material Icons -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<!-- Exemplos -->
<i class="material-icons">home</i>
<i class="material-icons">trophy</i>
<i class="material-icons">account_balance_wallet</i>
<i class="material-icons">bar_chart</i>
```

---

## 2. 📱 Arquitetura Mobile SPA v3.0

### 2.1 Estrutura de Fragmentos

```
public/participante/
├── fronts/                    # Templates (fragmentos HTML)
│   ├── home.html
│   ├── ranking.html
│   ├── extrato.html
│   └── perfil.html
├── core/
│   ├── navigation.js          # Sistema de navegação v3.0
│   ├── cache-manager.js       # IndexedDB manager
│   └── api-client.js          # HTTP client
└── modules/
    ├── ranking/
    │   ├── ranking.js         # Lógica do módulo
    │   └── ranking.css        # Estilos específicos
    └── extrato/
        └── ...
```

**IMPORTANTE:** Fragmentos são HTML puro sem `<html>`, `<head>` ou `<body>`.

```html
<!-- ✅ CORRETO: fronts/ranking.html -->
<div id="ranking-container">
  <h2>Ranking</h2>
  <div class="ranking-list"></div>
</div>

<!-- ❌ ERRADO -->
<!DOCTYPE html>
<html>
  <head>...</head>
  <body>...</body>
</html>
```

### 2.2 Navegação SPA v3.0

```javascript
// participante-navigation.js
class NavigationManager {
  constructor() {
    this.currentPage = null;
    this.debounceTimer = null;
    this.DEBOUNCE_DELAY = 100; // ms
  }
  
  async navigate(page, skipHistory = false) {
    // Debounce - NUNCA usar flag de travamento
    clearTimeout(this.debounceTimer);
    
    this.debounceTimer = setTimeout(async () => {
      await this._doNavigate(page, skipHistory);
    }, this.DEBOUNCE_DELAY);
  }
  
  async _doNavigate(page, skipHistory) {
    // Validar página
    const validPages = ['home', 'ranking', 'extrato', 'perfil'];
    if (!validPages.includes(page)) {
      console.error('Página inválida:', page);
      return;
    }
    
    // Evitar navegação duplicada
    if (this.currentPage === page) return;
    
    try {
      // 1. Loading state
      this.showLoading();
      
      // 2. Carregar fragmento
      const html = await fetch(`/participante/fronts/${page}.html`).then(r => r.text());
      
      // 3. Renderizar
      document.getElementById('main-content').innerHTML = html;
      
      // 4. Executar módulo específico
      await this.loadModule(page);
      
      // 5. Atualizar history
      if (!skipHistory) {
        window.history.pushState({ page }, '', `#${page}`);
      }
      
      // 6. Atualizar nav
      this.updateActiveNav(page);
      this.currentPage = page;
      
    } catch (error) {
      console.error('Erro ao navegar:', error);
      this.showError();
    } finally {
      this.hideLoading();
    }
  }
  
  async loadModule(page) {
    // Carregar script do módulo dinamicamente
    if (typeof window[`${page}Module`] === 'object') {
      await window[`${page}Module`].init();
    }
  }
  
  showLoading() {
    // Glass overlay - OBRIGATÓRIO em reloads
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'glass-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
  }
  
  hideLoading() {
    document.getElementById('loading-overlay')?.remove();
  }
}

// Interceptar botão voltar
window.addEventListener('popstate', (e) => {
  if (e.state && e.state.page) {
    navManager.navigate(e.state.page, true);
  }
});
```

### 2.3 Loading States

```html
<!-- Splash Screen (apenas 1ª visita) -->
<div id="splash-screen" class="splash">
  <img src="/img/logo.png" alt="Super Cartola">
  <div class="spinner"></div>
</div>

<!-- Glass Overlay (reloads/PTR) -->
<div class="glass-overlay">
  <div class="spinner"></div>
</div>

<style>
.splash {
  position: fixed;
  inset: 0;
  background: #000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.glass-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 69, 0, 0.3);
  border-top-color: var(--laranja);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
```

---

## 3. 💾 Performance & Cache (IndexedDB)

### 3.1 Cache Strategy - Cache-First

```javascript
// cache-manager.js
class CacheManager {
  constructor() {
    this.dbName = 'super_cartola_cache';
    this.version = 1;
    this.db = null;
  }
  
  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };
      
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        
        // Criar stores
        if (!db.objectStoreNames.contains('participante')) {
          db.createObjectStore('participante', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('ranking')) {
          db.createObjectStore('ranking', { keyPath: 'key' });
        }
        if (!db.objectStoreNames.contains('extrato')) {
          db.createObjectStore('extrato', { keyPath: 'key' });
        }
      };
    });
  }
  
  async get(store, key) {
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([store], 'readonly');
      const objectStore = transaction.objectStore(store);
      const request = objectStore.get(key);
      
      request.onsuccess = () => {
        const data = request.result;
        
        // Verificar TTL
        if (data && this.isExpired(data)) {
          this.delete(store, key);
          resolve(null);
        } else {
          resolve(data);
        }
      };
      request.onerror = () => reject(request.error);
    });
  }
  
  async set(store, data, ttl = null) {
    const record = {
      ...data,
      _timestamp: Date.now(),
      _ttl: ttl || this.getTTL(store)
    };
    
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([store], 'readwrite');
      const objectStore = transaction.objectStore(store);
      const request = objectStore.put(record);
      
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }
  
  isExpired(data) {
    if (!data._timestamp || !data._ttl) return false;
    return Date.now() - data._timestamp > data._ttl;
  }
  
  getTTL(store) {
    const TTL_MAP = {
      participante: 24 * 60 * 60 * 1000,  // 24h
      liga: 24 * 60 * 60 * 1000,          // 24h
      ranking: 60 * 60 * 1000,            // 1h
      extrato: 30 * 60 * 1000             // 30min
    };
    return TTL_MAP[store] || 60 * 60 * 1000; // default 1h
  }
}

// Cache-First Pattern
async function loadRanking() {
  // 1. Tentar cache (render instantâneo)
  const cached = await cacheManager.get('ranking', 'current');
  if (cached) {
    renderRanking(cached.data);
  }
  
  // 2. Fetch fresh (background)
  try {
    const fresh = await fetch('/api/ranking').then(r => r.json());
    await cacheManager.set('ranking', { key: 'current', data: fresh });
    
    // 3. Re-render se mudou
    if (!cached || JSON.stringify(cached.data) !== JSON.stringify(fresh)) {
      renderRanking(fresh);
    }
  } catch (error) {
    // Se fetch falhar e temos cache, continuar com cache
    if (!cached) {
      showError('Não foi possível carregar dados');
    }
  }
}
```

### 3.2 TTL por Módulo

```javascript
const CACHE_TTL = {
  // Dados estáticos/semi-estáticos
  participante: 24 * 60 * 60 * 1000,    // 24h
  liga: 24 * 60 * 60 * 1000,            // 24h
  config: 7 * 24 * 60 * 60 * 1000,      // 7 dias
  
  // Dados dinâmicos
  ranking: 60 * 60 * 1000,              // 1h
  extrato: 30 * 60 * 1000,              // 30min
  rodadaAtual: 10 * 60 * 1000,          // 10min
  
  // Dados em tempo real
  liveFeed: 60 * 1000                   // 1min
};
```

---

## 4. 📱 Componentes Mobile Premium (v3.2)

### 4.1 Header com Avatar e Badge

```html
<!-- Header Premium com identidade do usuario -->
<header class="header-premium">
  <div class="header-content">
    <!-- Avatar com Iniciais -->
    <div class="user-section">
      <div class="avatar-circle">
        <span class="avatar-initials font-brand">PM</span>
      </div>
      <div class="user-info">
        <h1 class="user-name font-brand">Paulinett Miranda</h1>
        <div class="badge-premium">
          <i class="material-icons badge-icon">star</i>
          <span>Premium</span>
        </div>
      </div>
    </div>
    <!-- Notificacoes -->
    <button class="btn-icon" aria-label="Notificacoes">
      <i class="material-icons">notifications</i>
    </button>
  </div>
</header>

<style>
.header-premium {
  padding: 48px 16px 24px;
  background: #000;
  position: sticky;
  top: 0;
  z-index: 20;
  border-bottom: 1px solid var(--border-color);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #bdc3c7;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--bg-card);
}

.avatar-initials {
  color: #1a1a1a;
  font-size: 14px;
}

.user-name {
  font-size: 18px;
  color: var(--text-primary);
  line-height: 1.2;
}

.badge-premium {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: 2px;
}

.badge-premium .badge-icon {
  font-size: 12px;
  color: #f59e0b;
}

.badge-premium span {
  font-size: 10px;
  color: #f59e0b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-icon {
  padding: 8px;
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
}

.btn-icon .material-icons {
  font-size: 24px;
}
</style>
```

### 4.2 Grid de Atalhos (4 colunas)

```html
<!-- Grid de acoes rapidas -->
<section class="action-grid">
  <button class="action-item">
    <div class="action-icon">
      <i class="material-icons">emoji_events</i>
    </div>
    <span class="action-label">Premiacoes</span>
  </button>
  <button class="action-item">
    <div class="action-icon">
      <i class="material-icons">groups</i>
    </div>
    <span class="action-label">Participantes</span>
  </button>
  <button class="action-item">
    <div class="action-icon">
      <i class="material-icons">description</i>
    </div>
    <span class="action-label">Regras</span>
  </button>
  <button class="action-item">
    <div class="action-icon">
      <i class="material-icons">workspace_premium</i>
    </div>
    <span class="action-label">Cartola PRO</span>
  </button>
</section>

<style>
.action-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  padding: 0 16px;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  cursor: pointer;
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  border: 1px solid var(--laranja);
  background: var(--bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.action-icon:hover {
  background: var(--bg-secondary);
}

.action-icon .material-icons {
  font-size: 24px;
  color: var(--laranja);
}

.action-label {
  font-size: 10px;
  color: var(--text-secondary);
  font-weight: 500;
  text-align: center;
}
</style>
```

### 4.3 Card de Status do Time (Split Layout)

```html
<!-- Card com Pontos e Posicao lado a lado -->
<section class="team-status-card">
  <div class="team-header">
    <h2 class="team-name font-brand">Urubu Play F.C.</h2>
    <div class="team-shield">
      <i class="material-icons">shield</i>
    </div>
  </div>
  <div class="stats-split">
    <div class="stat-block">
      <span class="stat-label">Pontos</span>
      <span class="stat-value font-mono text-accent">0</span>
      <span class="stat-hint">Aguardando 1a rodada</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-block">
      <span class="stat-label">Posicao</span>
      <span class="stat-value font-mono">--</span>
      <span class="stat-hint">Aguardando 1a rodada</span>
    </div>
  </div>
</section>

<style>
.team-status-card {
  background: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 20px;
  margin: 16px;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}

.team-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.team-name {
  font-size: 20px;
  color: var(--text-primary);
}

.team-shield {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.team-shield .material-icons {
  font-size: 16px;
  color: var(--text-muted);
}

.stats-split {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 16px;
}

.stat-block {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 48px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.stat-value.text-accent {
  color: var(--laranja);
}

.stat-hint {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 4px;
}

.stat-divider {
  width: 1px;
  background: var(--border-color);
}
</style>
```

### 4.4 FAB do Mercado (Floating Action Button)

```html
<!-- FAB com Timer do Mercado -->
<div class="fab-mercado">
  <button class="fab-btn">
    <div class="fab-icon">
      <i class="material-icons">storefront</i>
    </div>
    <div class="fab-content">
      <span class="fab-timer">Fecha em 7d 5h</span>
      <span class="fab-status font-brand">Aberto R1</span>
    </div>
  </button>
</div>

<style>
.fab-mercado {
  position: fixed;
  bottom: 96px; /* Acima do bottom nav */
  right: 16px;
  z-index: 40;
}

.fab-btn {
  background: linear-gradient(135deg, var(--verde-lucro), #27ae60);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 24px;
  padding: 10px 24px 10px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 180px;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
  transition: transform 0.2s;
}

.fab-btn:hover {
  transform: scale(1.05);
}

.fab-icon {
  width: 32px;
  height: 32px;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fab-icon .material-icons {
  font-size: 16px;
  color: #fff;
}

.fab-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.fab-timer {
  font-size: 10px;
  color: rgba(255,255,255,0.8);
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.fab-status {
  font-size: 14px;
  color: #fff;
  text-transform: uppercase;
}
</style>
```

### 4.5 Card de Jogo (Match Card)

```html
<!-- Card de partida com escudos -->
<div class="match-card">
  <div class="match-league">Brasileirao Serie A</div>
  <div class="match-content">
    <!-- Time 1 -->
    <div class="match-team">
      <div class="team-badge" style="background-color: #c8102e;">
        <span>FLA</span>
      </div>
      <span class="team-name-short">Flamengo</span>
    </div>
    <!-- VS e Horario -->
    <div class="match-center">
      <span class="match-vs">VS</span>
      <span class="match-time font-mono">16:00</span>
    </div>
    <!-- Time 2 -->
    <div class="match-team">
      <div class="team-badge" style="background-color: #006437;">
        <span>PAL</span>
      </div>
      <span class="team-name-short">Palmeiras</span>
    </div>
  </div>
</div>

<style>
.match-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 12px;
  border: 1px solid var(--border-color);
}

.match-league {
  font-size: 11px;
  color: var(--text-muted);
  padding-bottom: 8px;
  margin-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.match-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.match-team {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 33%;
}

.team-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.team-badge span {
  font-size: 10px;
  font-weight: 700;
  color: #fff;
}

.team-name-short {
  font-size: 10px;
  color: var(--text-primary);
  text-align: center;
}

.match-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 33%;
}

.match-vs {
  font-size: 12px;
  color: var(--laranja);
  font-weight: 700;
  margin-bottom: 2px;
}

.match-time {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}
</style>
```

### 4.6 Bottom Navigation (4 itens)

```html
<!-- Bottom Nav fixo -->
<nav class="bottom-nav">
  <a href="#home" class="nav-item active">
    <i class="material-icons">home</i>
    <span>Inicio</span>
  </a>
  <a href="#ranking" class="nav-item">
    <i class="material-icons">leaderboard</i>
    <span>Ranking</span>
  </a>
  <a href="#menu" class="nav-item">
    <i class="material-icons">apps</i>
    <span>Menu</span>
  </a>
  <a href="#financeiro" class="nav-item">
    <i class="material-icons">account_balance_wallet</i>
    <span>Financeiro</span>
  </a>
</nav>

<style>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: #000;
  border-top: 1px solid var(--border-color);
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  z-index: 50;
  padding-bottom: env(safe-area-inset-bottom);
}

.bottom-nav .nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s;
}

.bottom-nav .nav-item.active,
.bottom-nav .nav-item:hover {
  color: var(--laranja);
}

.bottom-nav .nav-item .material-icons {
  font-size: 22px;
}

.bottom-nav .nav-item span {
  font-size: 10px;
  font-weight: 500;
}
</style>
```

### 4.7 Mapeamento Font Awesome → Material Icons

| Font Awesome | Material Icons | Uso |
|--------------|----------------|-----|
| `fa-trophy` | `emoji_events` | Premiacoes |
| `fa-users` | `groups` | Participantes |
| `fa-clipboard-list` | `description` | Regras |
| `fa-crown` | `workspace_premium` | Premium |
| `fa-home` | `home` | Inicio |
| `fa-chart-line` | `leaderboard` | Ranking |
| `fa-th` | `apps` | Menu |
| `fa-wallet` | `account_balance_wallet` | Financeiro |
| `fa-shop` | `storefront` | Mercado |
| `fa-coins` | `payments` | Saldo |
| `fa-bell` | `notifications` | Alertas |
| `fa-shield-alt` | `shield` | Escudo |

---

## 5. 🎭 Admin UI (Desktop)

### 4.1 Layout Padrão

```html
<div class="admin-layout">
  <aside class="sidebar">
    <div class="logo">
      <img src="/img/logo.png" alt="SC">
      <h3>Super Cartola</h3>
    </div>
    <nav>
      <a href="#dashboard" class="nav-item active">
        <i class="material-icons">dashboard</i>
        Dashboard
      </a>
      <a href="#ligas" class="nav-item">
        <i class="material-icons">emoji_events</i>
        Ligas
      </a>
      <!-- ... -->
    </nav>
  </aside>
  
  <main class="main-content">
    <header class="topbar">
      <h1>Dashboard</h1>
      <div class="user-menu">...</div>
    </header>
    
    <div class="content">
      <!-- Módulo renderizado aqui -->
    </div>
  </main>
</div>

<style>
.admin-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  height: 100vh;
}

.sidebar {
  background: var(--bg-card);
  border-right: 1px solid var(--border-color);
  padding: 24px;
  overflow-y: auto;
}

.main-content {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.topbar {
  height: 64px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}
</style>
```

### 4.2 Módulos Admin

```javascript
// Padrão de módulo admin
const adminTesouraria = {
  currentLigaId: null,
  currentTemporada: null,
  
  async render(container, ligaId, temporada) {
    this.currentLigaId = ligaId;
    this.currentTemporada = temporada;
    
    // Carregar template
    const template = await fetch('/admin/modules/tesouraria.html').then(r => r.text());
    document.querySelector(container).innerHTML = template;
    
    // Carregar dados
    await this.loadData();
    
    // Bind events
    this.bindEvents();
  },
  
  async loadData() {
    const data = await fetch(`/api/tesouraria/${this.currentLigaId}/${this.currentTemporada}`)
      .then(r => r.json());
    
    this.renderTable(data);
    this.renderStats(data);
  },
  
  renderTable(data) {
    const tbody = document.querySelector('#tesouraria-table tbody');
    tbody.innerHTML = data.participantes.map(p => `
      <tr>
        <td>${p.nome}</td>
        <td class="${p.saldo >= 0 ? 'positivo' : 'negativo'}">
          R$ ${p.saldo.toFixed(2).replace('.', ',')}
        </td>
        <td>
          <button onclick="adminTesouraria.verExtrato('${p.id}')">
            Ver Extrato
          </button>
        </td>
      </tr>
    `).join('');
  },
  
  bindEvents() {
    // ...
  },
  
  // API pública
  async recarregar() {
    await this.loadData();
  },
  
  mudarTemporada(temporada) {
    this.currentTemporada = temporada;
    this.recarregar();
  }
};
```

---

## 6. 📤 Export System (Mobile Dark HD)

### 5.1 Configuração Padrão

```javascript
const EXPORT_CONFIG = {
  backgroundColor: '#000000',
  scale: 2,                    // Retina
  useCORS: true,
  logging: false,
  width: 1080,
  height: 1920,
  pixelRatio: 2
};

async function exportarModulo(elementId, filename) {
  const element = document.getElementById(elementId);
  
  // Aplicar classe de export (mobile otimizado)
  element.classList.add('export-mode');
  
  try {
    const canvas = await html2canvas(element, EXPORT_CONFIG);
    
    // Download
    const link = document.createElement('a');
    link.download = `${filename}_${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    
    // Feedback
    showToast('✅ Imagem exportada com sucesso!');
  } catch (error) {
    console.error('Erro ao exportar:', error);
    showToast('🔴 Erro ao exportar imagem');
  } finally {
    element.classList.remove('export-mode');
  }
}
```

### 5.2 CSS para Export

```css
/* Otimizações para export */
.export-mode {
  width: 1080px !important;
  min-height: 1920px !important;
  padding: 40px !important;
  background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%) !important;
}

.export-mode .card {
  box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}

.export-mode .text {
  -webkit-font-smoothing: antialiased !important;
  text-rendering: optimizeLegibility !important;
}
```

---

## 7. 🛠️ Debugging & Tools

### 6.1 Performance Monitoring

```javascript
// Adicionar no index.html
if ('performance' in window) {
  window.addEventListener('load', () => {
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    const connectTime = perfData.responseEnd - perfData.requestStart;
    const renderTime = perfData.domComplete - perfData.domLoading;
    
    console.log('📊 Performance Metrics:');
    console.log(`  Page Load: ${pageLoadTime}ms`);
    console.log(`  Connect: ${connectTime}ms`);
    console.log(`  Render: ${renderTime}ms`);
    
    // Enviar para analytics (se configurado)
    if (window.analytics) {
      window.analytics.track('page_performance', {
        pageLoadTime,
        connectTime,
        renderTime
      });
    }
  });
}
```

### 6.2 Responsive Debug

```html
<!-- Adicionar no footer -->
<div id="debug-viewport" style="position: fixed; bottom: 0; right: 0; padding: 8px; background: rgba(0,0,0,0.8); color: lime; font-size: 12px; z-index: 10000;">
  <script>
    function updateViewport() {
      const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
      const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
      document.getElementById('debug-viewport').textContent = `${vw}x${vh}`;
    }
    window.addEventListener('resize', updateViewport);
    updateViewport();
  </script>
</div>
```

---

## 8. 📋 Checklists

### 7.1 Novo Módulo Mobile

```markdown
□ Criar fragmento em /fronts/
□ Criar arquivo JS do módulo
□ Implementar Cache-First pattern
□ Adicionar rota no navigation.js
□ Criar ícone Material Icons
□ Testar em viewport mobile (360x640)
□ Validar TTL do cache
□ Implementar loading states
□ Testar offline
□ Validar export (se aplicável)
```

### 7.2 CSS Performance

```markdown
□ Evitar seletores complexos (> 3 níveis)
□ Usar transform para animações (não top/left)
□ Adicionar will-change em elementos animados
□ Minificar antes de deploy
□ Verificar bundle size (<100KB)
□ Usar CSS Grid/Flexbox (não floats)
□ Lazy load imagens (loading="lazy")
```

---

**STATUS:** Frontend Crafter - READY TO CRAFT

**Versao:** 3.2 (Mobile Premium Components)

**Ultima atualizacao:** 2026-01-23

**Changelog v3.2:**
- Nova secao 4: Componentes Mobile Premium
- Header com Avatar e Badge Premium
- Grid de Atalhos 4 colunas (outlined icons)
- Card de Status do Time com split Pontos/Posicao
- FAB do Mercado com timer integrado e gradiente verde
- Match Card com escudos circulares
- Bottom Navigation padronizado (4 itens)
- Tabela de conversao Font Awesome → Material Icons
- Todos componentes usando variaveis CSS do Design System

**Changelog v3.1:**
- Documentado sistema de 3 fontes: Inter (base), Russo One (brand), JetBrains Mono (mono)
- Classe `.font-brand` para titulos com Russo One
- Variaveis CSS padronizadas: `--font-family-base`, `--font-family-brand`, `--font-family-mono`
