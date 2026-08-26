/**
 * Claude Skills Registry - Search Application
 * Fast client-side search for Claude Code skills
 * v2.0 - Added Leaderboard, Stats, Favorites, Random Discovery
 */

const CONFIG = {
    INDEX_URL: 'search-index-lite.json',
    LEGACY_INDEX_URL: 'search-index.json',
    TAXONOMY_URL: 'category-taxonomy.json',
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

const CATEGORY_NAMES = {};
const CATEGORY_CODES_REVERSE = {};
const CATEGORY_META_BY_CODE = {};
const CATEGORY_META_BY_SLUG = {};
let DEFAULT_CATEGORY_CODE = 'oth';

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
    leaderboardRequestToken: 0,
    currentStarsFilter: '',
    currentSourceFilter: '',
    currentTagFilters: [],
    categoryCache: {},
    taxonomy: null,
    favorites: JSON.parse(localStorage.getItem('skillFavorites') || '[]'),
    theme: localStorage.getItem('theme') || 'dark',
    isLoading: true
};

const elements = {
    searchInput: document.getElementById('search-input'),
    metaDescription: document.querySelector('meta[name="description"]'),
    categoryFilter: document.getElementById('category-filter'),
    sortFilter: document.getElementById('sort-filter'),
    totalCount: document.getElementById('total-count'),
    resultCount: document.getElementById('result-count'),
    searchTime: document.getElementById('search-time'),
    searchScope: document.getElementById('search-scope'),
    searchAllBtn: document.getElementById('search-all-btn'),
    statsBar: document.getElementById('stats-bar'),
    loading: document.getElementById('loading'),
    featuredSection: document.getElementById('featured-section'),
    featuredList: document.getElementById('featured-list'),
    leaderboardSection: document.getElementById('leaderboard-section'),
    leaderboardList: document.getElementById('leaderboard-list'),
    leaderboardCategory: document.getElementById('leaderboard-category'),
    leaderboardStatus: document.getElementById('leaderboard-status'),
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
    filterToggle: document.getElementById('filter-toggle'),
    advancedFilters: document.getElementById('advanced-filters'),
    starsFilter: document.getElementById('stars-filter'),
    sourceFilter: document.getElementById('source-filter'),
    tagFilter: document.getElementById('tag-filter'),
    activeTags: document.getElementById('active-tags'),
    clearFilters: document.getElementById('clear-filters'),
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
        return DEFAULT_CATEGORY_CODE;
    }

    const normalized = String(category).trim().toLowerCase();
    if (!normalized) {
        return DEFAULT_CATEGORY_CODE;
    }
    if (CATEGORY_NAMES[normalized]) {
        return normalized;
    }
    return CATEGORY_CODES_REVERSE[normalized] || normalized;
}

function configureCategoryTaxonomy(payload) {
    Object.keys(CATEGORY_NAMES).forEach(key => delete CATEGORY_NAMES[key]);
    Object.keys(CATEGORY_CODES_REVERSE).forEach(key => delete CATEGORY_CODES_REVERSE[key]);
    Object.keys(CATEGORY_META_BY_CODE).forEach(key => delete CATEGORY_META_BY_CODE[key]);
    Object.keys(CATEGORY_META_BY_SLUG).forEach(key => delete CATEGORY_META_BY_SLUG[key]);

    payload.categories.forEach(category => {
        CATEGORY_NAMES[category.code] = category.display_name;
        CATEGORY_CODES_REVERSE[category.slug] = category.code;
        CATEGORY_META_BY_CODE[category.code] = category;
        CATEGORY_META_BY_SLUG[category.slug] = category;
    });
    DEFAULT_CATEGORY_CODE = payload.default_code;
}

function categoryDisplayName(category) {
    const code = normalizeCategoryCode(category);
    return CATEGORY_NAMES[code] || String(category || CATEGORY_NAMES[DEFAULT_CATEGORY_CODE] || 'Other');
}

function categoryReportingLabel(category) {
    const code = normalizeCategoryCode(category);
    const metadata = CATEGORY_META_BY_CODE[code];
    if (!metadata?.parent) {
        return categoryDisplayName(category);
    }
    const parent = CATEGORY_META_BY_SLUG[metadata.parent];
    return parent
        ? `${parent.display_name} › ${metadata.display_name}`
        : metadata.display_name;
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

async function loadSearchIndex() {
    return normalizeSearchIndex(await fetchJson(CONFIG.INDEX_URL));
}

function formatResultCount(count) {
    const base = `${count.toLocaleString()} results`;
    if (state.index?.isLite) {
        return `${base} in highlighted index`;
    }
    return base;
}

function readNumericStat(key, fallback = 0) {
    const rawValue = state.stats?.[key];
    if (rawValue === null || rawValue === undefined || rawValue === '') {
        return fallback;
    }

    const value = Number(rawValue);
    return Number.isFinite(value) ? value : fallback;
}

function getDisplaySkillCount() {
    return readNumericStat(
        'registry_skill_count_dedup',
        Number(state.index?.t || state.index?.s?.length || 0)
    );
}

function updateRegistryCountDisplay() {
    const dedupedCount = getDisplaySkillCount();
    if (!Number.isFinite(dedupedCount) || dedupedCount <= 0) {
        elements.totalCount.textContent = 'skills';
        elements.totalCount.removeAttribute('title');
        return;
    }

    const formattedDeduped = dedupedCount.toLocaleString();
    const rawArchiveCount = readNumericStat('archive_skill_md_count_raw', 0);
    const includedCount = Number(state.index?.includedCount || 0);

    elements.totalCount.textContent = formattedDeduped;

    const titleParts = [`${formattedDeduped} deduplicated skills`];
    if (rawArchiveCount > 0) {
        titleParts.push(`${rawArchiveCount.toLocaleString()} archived SKILL.md files`);
    }
    if (state.index?.isLite && includedCount > 0 && includedCount < dedupedCount) {
        titleParts.push(`${includedCount.toLocaleString()} highlighted skills loaded for first paint`);
    }
    elements.totalCount.title = titleParts.join(' · ');

    document.title = `Claude Skills Registry - Search ${formattedDeduped} Skills`;
    if (elements.metaDescription) {
        elements.metaDescription.setAttribute(
            'content',
            `Search and discover ${formattedDeduped} Claude Code skills for Claude Code, Codex CLI, and ChatGPT.`
        );
    }
    updateSearchScopeDisplay();
}

function updateSearchScopeDisplay() {
    const included = Number(state.index?.includedCount || state.index?.s?.length || 0);
    const total = getDisplaySkillCount() || included;
    const full = !state.index?.isLite;
    elements.searchScope.textContent = full
        ? `Searching all ${total.toLocaleString()} skills`
        : `Searching ${included.toLocaleString()} highlighted of ${total.toLocaleString()} skills`;
    elements.searchAllBtn.textContent = full ? 'All skills loaded' : `Search all ${total.toLocaleString()}`;
    elements.searchAllBtn.disabled = full;
}

async function init() {
    try {
        const [rawIndex, taxonomyData, featuredData, categoriesData, statsData, pluginsData] = await Promise.all([
            fetchJson(CONFIG.INDEX_URL),
            fetchJson(CONFIG.TAXONOMY_URL),
            fetch(CONFIG.FEATURED_URL).then(r => r.json()).catch(() => ({ skills: [] })),
            fetch(CONFIG.CATEGORIES_URL).then(r => r.json()).catch(() => ({ categories: [] })),
            fetch(CONFIG.STATS_URL).then(r => r.json()).catch(() => ({})),
            fetch(CONFIG.PLUGINS_URL).then(r => r.json()).catch(() => ({ plugins: [] }))
        ]);

        validateCategoryTaxonomy(taxonomyData);
        configureCategoryTaxonomy(taxonomyData);
        state.index = normalizeSearchIndex(rawIndex);
        state.taxonomy = taxonomyData;
        state.featured = featuredData.skills || [];
        state.plugins = pluginsData.plugins || [];
        state.categories = categoriesData.categories || [];
        state.stats = statsData || {};

        state.fuse = new Fuse(state.index.s, CONFIG.FUSE_OPTIONS);

        updateRegistryCountDisplay();
        elements.lastUpdated.textContent = `Updated: ${state.index.v}`;

        populateCategoryFilter();
        populateLeaderboardCategoryFilter();

        showFeatured();

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

function populateCategoryFilter() {
    state.categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.code;
        option.textContent = `${categoryReportingLabel(cat.code)} (${cat.count.toLocaleString()})`;
        elements.categoryFilter.appendChild(option);
    });
}

function populateLeaderboardCategoryFilter() {
    state.categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.code;
        option.textContent = categoryReportingLabel(cat.code);
        elements.leaderboardCategory.appendChild(option);
    });
}

function findCategoryByCode(code) {
    return state.categories.find(cat => cat.code === code);
}

async function loadCategoryLeaderboardSkills(categoryCode) {
    if (state.categoryCache[categoryCode]) {
        return state.categoryCache[categoryCode];
    }

    const category = findCategoryByCode(categoryCode);
    if (!category) throw new Error(`Unknown leaderboard category: ${categoryCode}`);
    validateCategoryIndexEntry(category, categoryCode);

    const manifest = await fetchJson(category.manifest);
    validateCategoryManifest(manifest, category, categoryCode);
    const parts = manifest.parts;
    const paths = new Set();
    let entryTotal = 0;
    parts.forEach(part => {
        validateCategoryPartEntry(part, paths);
        entryTotal += part.count;
    });
    if (entryTotal !== manifest.count) throw new Error('Category part counts do not match total');
    const firstPart = parts[0];
    if (!firstPart && manifest.count > 0) throw new Error('Category manifest has no first part');
    if (!firstPart) return [];
    const required = Math.min(CONFIG.LEADERBOARD_SIZE, manifest.count);
    if (!firstPart.path.endsWith('/part-000.json') || firstPart.count < required) throw new Error('First ranked part cannot satisfy leaderboard');
    const payload = await fetchJson(firstPart.path);
    validateCategoryPartPayload(payload, firstPart, manifest, categoryCode);
    const skills = payload.skills.map(normalizeSkillRecord);
    state.categoryCache[categoryCode] = skills;
    return skills;
}

async function loadFullSearchIndex() {
    if (!state.index?.isLite) {
        return state.index;
    }
    if (state.fullIndex) {
        return state.fullIndex;
    }
    const pointer = await fetchJson(CONFIG.LEGACY_INDEX_URL);
    validateSearchPointer(pointer);
    const manifest = await fetchJson(pointer.manifest);
    validateSearchManifest(manifest, pointer);
    const shards = manifest.shards;
    const paths = new Set();
    let entryTotal = 0;
    shards.forEach(shard => {
        validateSearchShardEntry(shard, paths);
        entryTotal += shard.count;
    });
    if (entryTotal !== manifest.total_count) throw new Error('Search shard counts do not match total');
    const payloads = await Promise.all(shards.map(shard => fetchJson(shard.path)));
    payloads.forEach((payload, index) => {
        validateSearchShardPayload(payload, shards[index], index, manifest);
    });
    const skills = payloads.flatMap(payload => payload.s);
    if (skills.some(skill => typeof skill.i !== 'string' || !skill.i ||
        typeof skill.b !== 'string' || !skill.b)) throw new Error('Search record stable key is missing');
    const stableKeys = skills.map(skill => `${skill.i}|${skill.b}`);
    if (new Set(stableKeys).size !== skills.length) {
        throw new Error('Search shards contain missing or duplicate stable records');
    }
    state.fullIndex = normalizeSearchIndex({ v: manifest.v, t: manifest.total_count, s: skills });
    return state.fullIndex;
}

async function getFilterBaseSkills() {
    return state.index.s;
}

async function activateFullSearch() {
    elements.searchAllBtn.disabled = true;
    elements.searchAllBtn.textContent = 'Loading all shards…';
    elements.searchScope.textContent = 'Loading the complete offline search index…';
    try {
        state.index = await loadFullSearchIndex();
        state.fuse = new Fuse(state.index.s, CONFIG.FUSE_OPTIONS);
        updateSearchScopeDisplay();
        if (state.currentQuery) search(state.currentQuery);
        else if (hasActiveFilters()) await searchWithFiltersOnly();
    } catch (error) {
        elements.searchScope.textContent = `Full search failed: ${error.message}`;
        elements.searchAllBtn.textContent = 'Retry Search all';
        elements.searchAllBtn.disabled = false;
    }
}

function switchView(view) {
    state.currentView = view;

    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.view === view);
    });

    elements.featuredSection.classList.add('hidden');
    elements.leaderboardSection.classList.add('hidden');
    elements.statsSection.classList.add('hidden');
    elements.pluginsSection.classList.add('hidden');
    elements.favoritesSection.classList.add('hidden');
    elements.searchResults.classList.add('hidden');
    elements.emptyState.classList.add('hidden');
    elements.loadMore.classList.add('hidden');
    elements.statsBar.classList.toggle('hidden', view !== 'featured');

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

    elements.featuredSection.classList.add('hidden');
    elements.leaderboardSection.classList.add('hidden');
    elements.statsSection.classList.add('hidden');
    elements.pluginsSection.classList.add('hidden');
    elements.favoritesSection.classList.add('hidden');
    elements.searchResults.classList.remove('hidden');
    elements.statsBar.classList.remove('hidden');

    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));

    let results = state.fuse.search(state.currentQuery);

    results = applyAllFilters(results);

    if (state.currentSort === 'stars') {
        results.sort((a, b) => (b.item.r || 0) - (a.item.r || 0));
    } else if (state.currentSort === 'name') {
        results.sort((a, b) => a.item.n.localeCompare(b.item.n));
    }

    state.results = results;

    const endTime = performance.now();
    const searchTimeMs = (endTime - startTime).toFixed(1);

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
elements.searchAllBtn.addEventListener('click', activateFullSearch);

elements.navTabs.addEventListener('click', (e) => {
    const tab = e.target.closest('.nav-tab');
    if (tab) {
        const view = tab.dataset.view;
        switchView(view);
        elements.searchInput.value = '';
        state.currentQuery = '';
    }
});

elements.leaderboardCategory.addEventListener('change', (e) => {
    showLeaderboard(e.target.value);
});

elements.randomBtn.addEventListener('click', showRandomSkill);

elements.quickTags.addEventListener('click', (e) => {
    if (e.target.classList.contains('tag')) {
        const query = e.target.dataset.query;
        elements.searchInput.value = query;
        search(query);
    }
});

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

document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== elements.searchInput) {
        e.preventDefault();
        elements.searchInput.focus();
    }
    if (e.key === 'r' && document.activeElement !== elements.searchInput && !elements.modal.classList.contains('hidden') === false) {
        showRandomSkill();
    }
});

elements.filterToggle.addEventListener('click', () => {
    elements.advancedFilters.classList.toggle('hidden');
    elements.filterToggle.classList.toggle('active');
});

elements.starsFilter.addEventListener('change', (e) => {
    state.currentStarsFilter = e.target.value;
    runFilterSearch();
});

elements.sourceFilter.addEventListener('change', (e) => {
    state.currentSourceFilter = e.target.value;
    runFilterSearch();
});

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

function renderActiveTags() {
    elements.activeTags.innerHTML = state.currentTagFilters.map(tag => {
        const safe = escapeHtml(tag);
        return `<span class="active-tag">#${safe}<button class="remove-tag-btn" data-tag="${safe}">&times;</button></span>`;
    }).join('');
}

elements.activeTags.addEventListener('click', (e) => {
    const btn = e.target.closest('.remove-tag-btn');
    if (btn) {
        const tag = btn.dataset.tag;
        state.currentTagFilters = state.currentTagFilters.filter(t => t !== tag);
        renderActiveTags();
        runFilterSearch();
    }
});

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

async function applyFiltersAndSearch() {
    if (state.currentQuery) {
        search(state.currentQuery);
    } else if (hasActiveFilters()) {
        await searchWithFiltersOnly();
    }
}

function hasActiveFilters() {
    return state.currentStarsFilter || state.currentSourceFilter ||
           state.currentTagFilters.length > 0 || state.currentCategory;
}

async function searchWithFiltersOnly() {
    const startTime = performance.now();
    state.displayedCount = 0;

    const baseSkills = await getFilterBaseSkills();
    let results = baseSkills.map(item => ({ item, score: 0 }));

    results = applyAllFilters(results);

    if (state.currentSort === 'stars') {
        results.sort((a, b) => (b.item.r || 0) - (a.item.r || 0));
    } else if (state.currentSort === 'name') {
        results.sort((a, b) => a.item.n.localeCompare(b.item.n));
    }

    state.results = results;

    const endTime = performance.now();
    const searchTimeMs = (endTime - startTime).toFixed(1);

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

function applyAllFilters(results) {
    if (state.currentCategory) {
        results = results.filter(r => r.item.c === state.currentCategory);
    }

    if (state.currentStarsFilter) {
        const minStars = parseStarsFilter(state.currentStarsFilter);
        if (minStars === 0) {
            results = results.filter(r => !r.item.r || r.item.r === 0);
        } else if (minStars > 0) {
            results = results.filter(r => (r.item.r || 0) >= minStars);
        }
    }

    if (state.currentSourceFilter) {
        if (state.currentSourceFilter === 'community') {
            results = results.filter(r => r.item.c !== 'off');
        }
    }

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

function parseStarsFilter(value) {
    if (value === '0') return 0;
    if (value === '10+') return 10;
    if (value === '100+') return 100;
    if (value === '500+') return 500;
    if (value === '1000+') return 1000;
    return -1;
}

function initTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    elements.themeIcon.textContent = state.theme === 'dark' ? '🌙' : '☀️';
}

elements.themeToggle.addEventListener('click', () => {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem('theme', state.theme);
    elements.themeIcon.textContent = state.theme === 'dark' ? '🌙' : '☀️';
});

initTheme();

init();
