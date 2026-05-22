/**
 * Claude Skills Registry - Search Application
 * Fast client-side search for 67,000+ skills
 * v2.0 - Added Leaderboard, Stats, Favorites, Random Discovery
 */

const CONFIG = {
    INDEX_URL: 'search-index-lite.json',
    LEGACY_INDEX_URL: 'search-index.json',
    FEATURED_URL: 'featured.json',
    CATEGORIES_URL: 'categories/index.json',
    STATS_URL: 'stats.json',
    PLUGINS_URL: 'plugins.json',
    PAGE_SIZE: 20,
    LEADERBOARD_SIZE: 50,
    DEBOUNCE_MS: 300,
    FUSE_OPTIONS: {
        keys: [
            { name: 'n', weight: 0.4 },  // name
            { name: 'd', weight: 0.3 },  // description
            { name: 'g', weight: 0.2 },  // tags
            { name: 'c', weight: 0.1 }   // category
        ],
        threshold: 0.4,
        includeScore: true,
        ignoreLocation: true,
        minMatchCharLength: 2
    }
};

// Category code to full name mapping
const CATEGORY_NAMES = {
    'dev': 'Development',
    'ops': 'DevOps',
    'sec': 'Security',
    'doc': 'Documents',
    'des': 'Design',
    'tst': 'Testing',
    'prd': 'Product',
    'mkt': 'Marketing',
    'pro': 'Productivity',
    'dat': 'Data',
    'off': 'Official',
    'oth': 'Other'
};

// Full category name to short code mapping
const CATEGORY_CODES_REVERSE = Object.fromEntries(
    Object.entries(CATEGORY_NAMES).map(([code, name]) => [name.toLowerCase(), code])
);

// Category colors for charts
const CATEGORY_COLORS = {
    'dev': '#00fff2',
    'ops': '#ff6b6b',
    'sec': '#ffd93d',
    'doc': '#6bcb77',
    'des': '#c56cf0',
    'tst': '#ff9ff3',
    'prd': '#54a0ff',
    'mkt': '#ff9f43',
    'pro': '#5f27cd',
    'dat': '#00d2d3',
    'off': '#f368e0',
    'oth': '#576574'
};

// State
let state = {
    index: null,
    fullIndex: null,
    fuse: null,
    featured: [],
    plugins: [],
    categories: [],
    stats: {},
    results: [],
    displayedCount: 0,
    currentQuery: '',
    currentCategory: '',
    currentSort: 'relevance',
    currentView: 'featured',
    currentStarsFilter: '',
    currentSourceFilter: '',
    currentTagFilters: [],
    categoryCache: {},
    favorites: JSON.parse(localStorage.getItem('skillFavorites') || '[]'),
    theme: localStorage.getItem('theme') || 'dark',
    isLoading: true
};

// DOM Elements
const elements = {
    searchInput: document.getElementById('search-input'),
    categoryFilter: document.getElementById('category-filter'),
    sortFilter: document.getElementById('sort-filter'),
    totalCount: document.getElementById('total-count'),
    resultCount: document.getElementById('result-count'),
    searchTime: document.getElementById('search-time'),
    statsBar: document.getElementById('stats-bar'),
    loading: document.getElementById('loading'),
    featuredSection: document.getElementById('featured-section'),
    featuredList: document.getElementById('featured-list'),
    leaderboardSection: document.getElementById('leaderboard-section'),
    leaderboardList: document.getElementById('leaderboard-list'),
    leaderboardCategory: document.getElementById('leaderboard-category'),
    statsSection: document.getElementById('stats-section'),
    pluginsSection: document.getElementById('plugins-section'),
    pluginsList: document.getElementById('plugins-list'),
    pluginsEmpty: document.getElementById('plugins-empty'),
    favoritesSection: document.getElementById('favorites-section'),
    favoritesList: document.getElementById('favorites-list'),
    favoritesEmpty: document.getElementById('favorites-empty'),
    searchResults: document.getElementById('search-results'),
    emptyState: document.getElementById('empty-state'),
    loadMore: document.getElementById('load-more'),
    loadMoreBtn: document.getElementById('load-more-btn'),
    lastUpdated: document.getElementById('last-updated'),
    quickTags: document.getElementById('quick-tags'),
    navTabs: document.getElementById('nav-tabs'),
    randomBtn: document.getElementById('random-btn'),
    modal: document.getElementById('skill-modal'),
    modalClose: document.getElementById('modal-close'),
    modalBody: document.getElementById('modal-body'),
    // Advanced filters
    filterToggle: document.getElementById('filter-toggle'),
    advancedFilters: document.getElementById('advanced-filters'),
    starsFilter: document.getElementById('stars-filter'),
    sourceFilter: document.getElementById('source-filter'),
    tagFilter: document.getElementById('tag-filter'),
    activeTags: document.getElementById('active-tags'),
    clearFilters: document.getElementById('clear-filters'),
    // Theme
    themeToggle: document.getElementById('theme-toggle'),
    themeIcon: document.getElementById('theme-icon')
};

async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`${url} returned ${response.status}`);
    }
    return response.json();
}

function normalizeCategoryCode(category) {
    if (!category) {
        return 'oth';
    }

    const normalized = String(category).trim().toLowerCase();
    if (CATEGORY_NAMES[normalized]) {
        return normalized;
    }
    return CATEGORY_CODES_REVERSE[normalized] || 'oth';
}

function normalizeSkillRecord(skill) {
    if (skill.n) {
        return skill;
    }

    return {
        n: skill.name || 'Unknown skill',
        d: skill.description || '',
        c: normalizeCategoryCode(skill.category),
        g: Array.isArray(skill.tags) ? skill.tags.slice(0, 5) : [],
        r: Number(skill.stars || 0),
        i: skill.install || skill.id || skill.name || '',
        b: skill.branch || 'main'
    };
}

function normalizeSearchIndex(indexData) {
    if (Array.isArray(indexData.s)) {
        return {
            ...indexData,
            s: indexData.s.map(normalizeSkillRecord),
            includedCount: indexData.s.length,
            isLite: false
        };
    }

    if (Array.isArray(indexData.skills)) {
        return {
            v: indexData.version || indexData.updated_at || '',
            t: Number(indexData.total_count || indexData.skills.length),
            s: indexData.skills.map(normalizeSkillRecord),
            includedCount: Number(indexData.included_count || indexData.skills.length),
            isLite: true
        };
    }

    throw new Error('Unsupported search index schema');
}

async function loadShardedSearchIndex(pointerData) {
    const manifestPath = pointerData.manifest;
    if (!manifestPath) {
        throw new Error('Search index pointer is missing manifest');
    }

    const manifest = await fetchJson(manifestPath);
    const shardPayloads = await Promise.all(
        (manifest.shards || []).map(shard => fetchJson(shard.path))
    );
    const skills = shardPayloads.flatMap(payload => payload.s || []);
    return normalizeSearchIndex({
        v: manifest.v || pointerData.v || '',
        t: manifest.total_count || pointerData.t || skills.length,
        s: skills
    });
}

async function loadSearchIndexUrl(url) {
    const indexData = await fetchJson(url);
    if (indexData.deprecated_full_payload && indexData.manifest) {
        return loadShardedSearchIndex(indexData);
    }
    return normalizeSearchIndex(indexData);
}

async function loadSearchIndex() {
    try {
        return await loadSearchIndexUrl(CONFIG.INDEX_URL);
    } catch (error) {
        console.warn(`Failed to load ${CONFIG.INDEX_URL}; falling back to ${CONFIG.LEGACY_INDEX_URL}:`, error);
        return await loadSearchIndexUrl(CONFIG.LEGACY_INDEX_URL);
    }
}

function formatResultCount(count) {
    const base = `${count.toLocaleString()} results`;
    if (state.index?.isLite) {
        return `${base} in highlighted index`;
    }
    return base;
}

// Initialize
async function init() {
    try {
        // Load index and featured in parallel
        const [indexData, featuredData, categoriesData, statsData, pluginsData] = await Promise.all([
            loadSearchIndex(),
            fetch(CONFIG.FEATURED_URL).then(r => r.json()).catch(() => ({ skills: [] })),
            fetch(CONFIG.CATEGORIES_URL).then(r => r.json()).catch(() => ({ categories: [] })),
            fetch(CONFIG.STATS_URL).then(r => r.json()).catch(() => ({})),
            fetch(CONFIG.PLUGINS_URL).then(r => r.json()).catch(() => ({ plugins: [] }))
        ]);

        state.index = indexData;
        state.featured = featuredData.skills || [];
        state.plugins = pluginsData.plugins || [];
        state.categories = categoriesData.categories || [];
        state.stats = statsData || {};

        // Initialize Fuse.js
        state.fuse = new Fuse(state.index.s, CONFIG.FUSE_OPTIONS);

        // Update UI
        elements.totalCount.textContent = state.index.t.toLocaleString();
        if (state.index.isLite && state.index.includedCount < state.index.t) {
            elements.totalCount.title = `Searching ${state.index.includedCount.toLocaleString()} highlighted skills out of ${state.index.t.toLocaleString()} total`;
        }
        elements.lastUpdated.textContent = `Updated: ${state.index.v}`;

        // Populate category filters
        populateCategoryFilter();
        populateLeaderboardCategoryFilter();

        // Show featured
        showFeatured();

        // Hide loading
        elements.loading.classList.add('hidden');
        state.isLoading = false;

    } catch (error) {
        console.error('Failed to load index:', error);
        elements.loading.innerHTML = `
            <span style="font-size: 2rem;">❌</span>
            <p>Failed to load skills index</p>
            <p style="font-size: 0.9rem; color: var(--text-muted);">${error.message}</p>
        `;
    }
}

// Populate category filter
function populateCategoryFilter() {
    state.categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.code;
        option.textContent = `${cat.name} (${cat.count.toLocaleString()})`;
        elements.categoryFilter.appendChild(option);
    });
}

// Populate leaderboard category filter
function populateLeaderboardCategoryFilter() {
    state.categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.code;
        option.textContent = `${cat.name}`;
        elements.leaderboardCategory.appendChild(option);
    });
}

function findCategoryByCode(code) {
    return state.categories.find(cat => cat.code === code);
}

async function loadCategorySkills(categoryCode) {
    if (!categoryCode) {
        return state.index.s;
    }
    if (state.categoryCache[categoryCode]) {
        return state.categoryCache[categoryCode];
    }

    const category = findCategoryByCode(categoryCode);
    if (!category || !category.manifest) {
        return state.index.s.filter(skill => skill.c === categoryCode);
    }

    const manifest = await fetchJson(category.manifest);
    const partPayloads = await Promise.all(
        (manifest.parts || []).map(part => fetchJson(part.path))
    );
    const skills = partPayloads
        .flatMap(part => part.skills || [])
        .map(normalizeSkillRecord);
    state.categoryCache[categoryCode] = skills;
    return skills;
}

async function loadFullSearchSkills() {
    if (!state.index?.isLite) {
        return state.index?.s || [];
    }
    if (state.fullIndex) {
        return state.fullIndex.s;
    }

    state.fullIndex = await loadSearchIndexUrl(CONFIG.LEGACY_INDEX_URL);
    return state.fullIndex.s;
}

async function getFilterBaseSkills() {
    if (state.currentCategory && !state.currentQuery) {
        return loadCategorySkills(state.currentCategory);
    }
    return state.index.s;
}

// Switch view
function switchView(view) {
    state.currentView = view;

    // Update nav tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.view === view);
    });

    // Hide all sections
    elements.featuredSection.classList.add('hidden');
    elements.leaderboardSection.classList.add('hidden');
    elements.statsSection.classList.add('hidden');
    elements.pluginsSection.classList.add('hidden');
    elements.favoritesSection.classList.add('hidden');
    elements.searchResults.classList.add('hidden');
    elements.emptyState.classList.add('hidden');
    elements.loadMore.classList.add('hidden');
    elements.statsBar.classList.toggle('hidden', view !== 'featured');

    // Show selected section
    switch (view) {
        case 'featured':
            showFeatured();
            break;
        case 'leaderboard':
            showLeaderboard();
            break;
        case 'stats':
            showStats();
            break;
        case 'plugins':
            showPlugins();
            break;
        case 'favorites':
            showFavorites();
            break;
    }
}

// Search
function search(query) {
    const startTime = performance.now();

    state.currentQuery = query.trim().toLowerCase();
    state.displayedCount = 0;

    if (!state.currentQuery) {
        switchView('featured');
        elements.resultCount.textContent = '';
        elements.searchTime.textContent = '';
        return;
    }

    // Hide all sections, show search results
    elements.featuredSection.classList.add('hidden');
    elements.leaderboardSection.classList.add('hidden');
    elements.statsSection.classList.add('hidden');
    elements.pluginsSection.classList.add('hidden');
    elements.favoritesSection.classList.add('hidden');
    elements.searchResults.classList.remove('hidden');
    elements.statsBar.classList.remove('hidden');

    // Reset nav tabs
    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));

    // Perform search
    let results = state.fuse.search(state.currentQuery);

    // Apply all filters (category, stars, source, tags)
    results = applyAllFilters(results);

    // Apply sort
    if (state.currentSort === 'stars') {
        results.sort((a, b) => (b.item.r || 0) - (a.item.r || 0));
    } else if (state.currentSort === 'name') {
        results.sort((a, b) => a.item.n.localeCompare(b.item.n));
    }

    state.results = results;

    const endTime = performance.now();
    const searchTimeMs = (endTime - startTime).toFixed(1);

    // Update UI
    elements.resultCount.textContent = formatResultCount(results.length);
    elements.searchTime.textContent = `${searchTimeMs}ms`;

    if (results.length === 0) {
        elements.searchResults.classList.add('hidden');
        elements.emptyState.classList.remove('hidden');
        elements.loadMore.classList.add('hidden');
    } else {
        elements.emptyState.classList.add('hidden');
        displayResults();
    }
}

// Event Listeners
elements.searchInput.addEventListener('input', debounce((e) => {
    search(e.target.value);
}, CONFIG.DEBOUNCE_MS));

elements.searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        search(e.target.value);
    }
});

elements.categoryFilter.addEventListener('change', (e) => {
    state.currentCategory = e.target.value;
    runFilterSearch();
});

elements.sortFilter.addEventListener('change', (e) => {
    state.currentSort = e.target.value;
    runFilterSearch();
});

elements.loadMoreBtn.addEventListener('click', displayResults);

// Nav tabs
elements.navTabs.addEventListener('click', (e) => {
    const tab = e.target.closest('.nav-tab');
    if (tab) {
        const view = tab.dataset.view;
        switchView(view);
        // Clear search when switching views
        elements.searchInput.value = '';
        state.currentQuery = '';
    }
});

// Leaderboard category filter
elements.leaderboardCategory.addEventListener('change', (e) => {
    showLeaderboard(e.target.value);
});

// Random button
elements.randomBtn.addEventListener('click', showRandomSkill);

// Quick tags
elements.quickTags.addEventListener('click', (e) => {
    if (e.target.classList.contains('tag')) {
        const query = e.target.dataset.query;
        elements.searchInput.value = query;
        search(query);
    }
});

// Modal
elements.modalClose.addEventListener('click', () => {
    elements.modal.classList.add('hidden');
});

elements.modal.querySelector('.modal-backdrop').addEventListener('click', () => {
    elements.modal.classList.add('hidden');
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        elements.modal.classList.add('hidden');
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Focus search on '/'
    if (e.key === '/' && document.activeElement !== elements.searchInput) {
        e.preventDefault();
        elements.searchInput.focus();
    }
    // Random skill on 'r'
    if (e.key === 'r' && document.activeElement !== elements.searchInput && !elements.modal.classList.contains('hidden') === false) {
        showRandomSkill();
    }
});

// ═══════════════════════════════════════════════════════════
// ADVANCED FILTERS
// ═══════════════════════════════════════════════════════════

// Toggle advanced filters panel
elements.filterToggle.addEventListener('click', () => {
    elements.advancedFilters.classList.toggle('hidden');
    elements.filterToggle.classList.toggle('active');
});

// Stars filter
elements.starsFilter.addEventListener('change', (e) => {
    state.currentStarsFilter = e.target.value;
    runFilterSearch();
});

// Source filter
elements.sourceFilter.addEventListener('change', (e) => {
    state.currentSourceFilter = e.target.value;
    runFilterSearch();
});

// Tag filter input
elements.tagFilter.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.value.trim()) {
        e.preventDefault();
        const tag = e.target.value.trim().toLowerCase();
        if (!state.currentTagFilters.includes(tag)) {
            state.currentTagFilters.push(tag);
            renderActiveTags();
            runFilterSearch();
        }
        e.target.value = '';
    }
});

// Render active tag filters
function renderActiveTags() {
    elements.activeTags.innerHTML = state.currentTagFilters.map(tag => {
        const safe = escapeHtml(tag);
        return `<span class="active-tag">#${safe}<button class="remove-tag-btn" data-tag="${safe}">&times;</button></span>`;
    }).join('');
}

// Delegate click for tag removal (avoids inline onclick XSS risk)
elements.activeTags.addEventListener('click', (e) => {
    const btn = e.target.closest('.remove-tag-btn');
    if (btn) {
        const tag = btn.dataset.tag;
        state.currentTagFilters = state.currentTagFilters.filter(t => t !== tag);
        renderActiveTags();
        runFilterSearch();
    }
});

// Clear all filters
elements.clearFilters.addEventListener('click', () => {
    state.currentStarsFilter = '';
    state.currentSourceFilter = '';
    state.currentTagFilters = [];
    state.currentCategory = '';
    elements.starsFilter.value = '';
    elements.sourceFilter.value = '';
    elements.categoryFilter.value = '';
    elements.tagFilter.value = '';
    renderActiveTags();
    runFilterSearch();
});

function runFilterSearch() {
    applyFiltersAndSearch().catch(() => {
        elements.resultCount.textContent = 'Failed to load filtered results';
    });
}

// Apply all filters and search
async function applyFiltersAndSearch() {
    if (state.currentQuery) {
        search(state.currentQuery);
    } else if (hasActiveFilters()) {
        // If no search query but filters active, search all
        await searchWithFiltersOnly();
    }
}

// Check if any filters are active
function hasActiveFilters() {
    return state.currentStarsFilter || state.currentSourceFilter ||
           state.currentTagFilters.length > 0 || state.currentCategory;
}

// Search with only filters (no query)
async function searchWithFiltersOnly() {
    const startTime = performance.now();
    state.displayedCount = 0;

    const baseSkills = await getFilterBaseSkills();
    let results = baseSkills.map(item => ({ item, score: 0 }));

    // Apply filters
    results = applyAllFilters(results);

    // Apply sort
    if (state.currentSort === 'stars') {
        results.sort((a, b) => (b.item.r || 0) - (a.item.r || 0));
    } else if (state.currentSort === 'name') {
        results.sort((a, b) => a.item.n.localeCompare(b.item.n));
    }

    state.results = results;

    const endTime = performance.now();
    const searchTimeMs = (endTime - startTime).toFixed(1);

    // Update UI
    elements.featuredSection.classList.add('hidden');
    elements.leaderboardSection.classList.add('hidden');
    elements.statsSection.classList.add('hidden');
    elements.pluginsSection.classList.add('hidden');
    elements.favoritesSection.classList.add('hidden');
    elements.searchResults.classList.remove('hidden');
    elements.statsBar.classList.remove('hidden');

    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));

    elements.resultCount.textContent = formatResultCount(results.length);
    elements.searchTime.textContent = `${searchTimeMs}ms`;

    if (results.length === 0) {
        elements.searchResults.classList.add('hidden');
        elements.emptyState.classList.remove('hidden');
        elements.loadMore.classList.add('hidden');
    } else {
        elements.emptyState.classList.add('hidden');
        displayResults();
    }
}

// Apply all filters to results
function applyAllFilters(results) {
    // Category filter
    if (state.currentCategory) {
        results = results.filter(r => r.item.c === state.currentCategory);
    }

    // Stars filter
    if (state.currentStarsFilter) {
        const minStars = parseStarsFilter(state.currentStarsFilter);
        if (minStars === 0) {
            results = results.filter(r => !r.item.r || r.item.r === 0);
        } else if (minStars > 0) {
            results = results.filter(r => (r.item.r || 0) >= minStars);
        }
    }

    // Source filter
    if (state.currentSourceFilter) {
        if (state.currentSourceFilter === 'official') {
            results = results.filter(r => r.item.c === 'off');
        } else if (state.currentSourceFilter === 'community') {
            results = results.filter(r => r.item.c !== 'off');
        }
    }

    // Tag filters
    if (state.currentTagFilters.length > 0) {
        results = results.filter(r => {
            const tags = (r.item.g || []).map(t => t.toLowerCase());
            return state.currentTagFilters.some(tf =>
                tags.some(t => t.includes(tf))
            );
        });
    }

    return results;
}

// Parse stars filter value
function parseStarsFilter(value) {
    if (value === '0') return 0;
    if (value === '10+') return 10;
    if (value === '100+') return 100;
    if (value === '500+') return 500;
    if (value === '1000+') return 1000;
    return -1;
}

// ═══════════════════════════════════════════════════════════
// THEME TOGGLE
// ═══════════════════════════════════════════════════════════

// Initialize theme
function initTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    elements.themeIcon.textContent = state.theme === 'dark' ? '🌙' : '☀️';
}

// Toggle theme
elements.themeToggle.addEventListener('click', () => {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem('theme', state.theme);
    elements.themeIcon.textContent = state.theme === 'dark' ? '🌙' : '☀️';
});

// Initialize theme on load
initTheme();

// Initialize
init();
