/**
 * Claude Skills Registry - Search Application
 * Fast client-side search for 67,000+ skills
 * v2.0 - Added Leaderboard, Stats, Favorites, Random Discovery
 */

const CONFIG = {
    INDEX_URL: 'search-index.json',
    FEATURED_URL: 'featured.json',
    CATEGORIES_URL: 'categories/index.json',
    COLLECTIONS_URL: 'collections.json',
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
    fuse: null,
    featured: [],
    collections: [],
    categories: [],
    results: [],
    displayedCount: 0,
    currentQuery: '',
    currentCategory: '',
    currentSort: 'relevance',
    currentView: 'featured',
    currentStarsFilter: '',
    currentSourceFilter: '',
    currentTagFilters: [],
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
    collectionsSection: document.getElementById('collections-section'),
    collectionsList: document.getElementById('collections-list'),
    collectionsEmpty: document.getElementById('collections-empty'),
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

// Initialize
async function init() {
    try {
        // Load index and featured in parallel
        const [indexData, featuredData, categoriesData, collectionsData] = await Promise.all([
            fetch(CONFIG.INDEX_URL).then(r => r.json()),
            fetch(CONFIG.FEATURED_URL).then(r => r.json()).catch(() => ({ skills: [] })),
            fetch(CONFIG.CATEGORIES_URL).then(r => r.json()).catch(() => ({ categories: [] })),
            fetch(CONFIG.COLLECTIONS_URL).then(r => r.json()).catch(() => ({ collections: [] }))
        ]);

        state.index = indexData;
        state.featured = featuredData.skills || [];
        state.collections = collectionsData.collections || [];
        state.categories = categoriesData.categories || [];

        // Initialize Fuse.js
        state.fuse = new Fuse(state.index.s, CONFIG.FUSE_OPTIONS);

        // Update UI
        elements.totalCount.textContent = state.index.t.toLocaleString();
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
    elements.collectionsSection.classList.add('hidden');
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
        case 'collections':
            showCollections();
            break;
        case 'favorites':
            showFavorites();
            break;
    }
}

// Show featured skills
function showFeatured() {
    elements.featuredSection.classList.remove('hidden');
    elements.featuredList.innerHTML = state.featured.slice(0, 12).map(skill =>
        createSkillCard(skill, true)
    ).join('');
}

// Show leaderboard
function showLeaderboard(categoryFilter = '') {
    elements.leaderboardSection.classList.remove('hidden');

    // Get all skills sorted by stars
    let skills = [...state.index.s].filter(s => s.r > 0);

    // Apply category filter
    if (categoryFilter) {
        skills = skills.filter(s => s.c === categoryFilter);
    }

    // Sort by stars descending
    skills.sort((a, b) => (b.r || 0) - (a.r || 0));

    // Take top N
    const topSkills = skills.slice(0, CONFIG.LEADERBOARD_SIZE);

    elements.leaderboardList.innerHTML = topSkills.map((skill, index) =>
        createLeaderboardCard(skill, index + 1)
    ).join('');
}

// Create leaderboard card
function createLeaderboardCard(skill, rank) {
    const name = skill.n;
    const description = skill.d;
    const category = CATEGORY_NAMES[skill.c] || skill.c;
    const stars = skill.r;
    const install = skill.i;
    const isFavorite = state.favorites.includes(install);

    let rankClass = '';
    let rankIcon = '';
    if (rank === 1) { rankClass = 'gold'; rankIcon = '🥇'; }
    else if (rank === 2) { rankClass = 'silver'; rankIcon = '🥈'; }
    else if (rank === 3) { rankClass = 'bronze'; rankIcon = '🥉'; }

    const isOfficial = skill.c === 'off';

    return `
        <div class="leaderboard-card ${rankClass}" data-install="${escapeHtml(install)}" onclick="showSkillDetail(this)">
            <div class="rank ${rankClass}">${rankIcon || '#' + rank}</div>
            <div class="leaderboard-info">
                <div class="leaderboard-header">
                    <span class="skill-name">
                        ${escapeHtml(name)}
                        ${isOfficial ? '<span class="official-badge" title="Official Anthropic Skill">✓</span>' : ''}
                    </span>
                    <span class="skill-stars">⭐ ${stars.toLocaleString()}</span>
                </div>
                <p class="skill-description">${escapeHtml(description)}</p>
                <div class="leaderboard-meta">
                    <span class="skill-category">${escapeHtml(category)}</span>
                    <button class="favorite-btn ${isFavorite ? 'active' : ''}" onclick="toggleFavorite(event, '${escapeHtml(install)}')" title="${isFavorite ? 'Remove from favorites' : 'Add to favorites'}">
                        ${isFavorite ? '❤️' : '🤍'}
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Show stats
function showStats() {
    elements.statsSection.classList.remove('hidden');

    // Calculate stats
    const totalSkills = state.index.t;
    const uniqueRepos = new Set(state.index.s.map(s => {
        const parts = s.i.split('/');
        return parts.length >= 2 ? `${parts[0]}/${parts[1]}` : s.i;
    })).size;
    const officialCount = state.index.s.filter(s => s.c === 'off').length;
    const categoryCount = state.categories.length;

    // Update stat cards
    document.getElementById('stat-total').textContent = totalSkills.toLocaleString();
    document.getElementById('stat-repos').textContent = uniqueRepos.toLocaleString();
    document.getElementById('stat-official').textContent = officialCount.toLocaleString();
    document.getElementById('stat-collections').textContent = state.collections.length;
    document.getElementById('stat-categories').textContent = categoryCount;

    // Render category chart
    renderCategoryChart();

    // Render top repos chart
    renderReposChart();
}

// Render category distribution chart
function renderCategoryChart() {
    const chartContainer = document.getElementById('category-chart');

    // Count by category
    const categoryCounts = {};
    state.index.s.forEach(skill => {
        const cat = skill.c || 'oth';
        categoryCounts[cat] = (categoryCounts[cat] || 0) + 1;
    });

    // Sort by count
    const sorted = Object.entries(categoryCounts)
        .sort((a, b) => b[1] - a[1]);

    const maxCount = sorted[0][1];

    chartContainer.innerHTML = sorted.map(([code, count]) => {
        const name = CATEGORY_NAMES[code] || code;
        const color = CATEGORY_COLORS[code] || '#576574';
        const percentage = ((count / state.index.t) * 100).toFixed(1);
        const barWidth = (count / maxCount) * 100;

        return `
            <div class="chart-row">
                <div class="chart-label">${name}</div>
                <div class="chart-bar-container">
                    <div class="chart-bar" style="width: ${barWidth}%; background: ${color}"></div>
                </div>
                <div class="chart-value">${count.toLocaleString()} (${percentage}%)</div>
            </div>
        `;
    }).join('');
}

// Render top repositories chart
function renderReposChart() {
    const chartContainer = document.getElementById('repos-chart');

    // Count by repo
    const repoCounts = {};
    state.index.s.forEach(skill => {
        const parts = skill.i.split('/');
        if (parts.length >= 2) {
            const repo = `${parts[0]}/${parts[1]}`;
            repoCounts[repo] = (repoCounts[repo] || 0) + 1;
        }
    });

    // Sort by count and take top 10
    const sorted = Object.entries(repoCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);

    const maxCount = sorted[0][1];

    chartContainer.innerHTML = sorted.map(([repo, count], index) => {
        const barWidth = (count / maxCount) * 100;
        const colors = ['#00fff2', '#ff6b6b', '#ffd93d', '#6bcb77', '#c56cf0',
                        '#ff9ff3', '#54a0ff', '#ff9f43', '#5f27cd', '#00d2d3'];

        return `
            <div class="chart-row">
                <div class="chart-label" title="${repo}">${repo.length > 25 ? repo.slice(0, 25) + '...' : repo}</div>
                <div class="chart-bar-container">
                    <div class="chart-bar" style="width: ${barWidth}%; background: ${colors[index % colors.length]}"></div>
                </div>
                <div class="chart-value">${count.toLocaleString()}</div>
            </div>
        `;
    }).join('');
}

// Show collections
function showCollections() {
    elements.collectionsSection.classList.remove('hidden');

    if (state.collections.length === 0) {
        elements.collectionsList.classList.add('hidden');
        elements.collectionsEmpty.classList.remove('hidden');
        return;
    }

    elements.collectionsEmpty.classList.add('hidden');
    elements.collectionsList.classList.remove('hidden');
    elements.collectionsList.innerHTML = state.collections.map(createCollectionCard).join('');
}

// Create collection card HTML
function createCollectionCard(collection) {
    const skills = collection.skills || [];
    const commands = collection.commands || [];
    const hooks = collection.hooks || [];
    const tags = collection.tags || [];
    const category = CATEGORY_NAMES[CATEGORY_CODES_REVERSE[collection.category]] || collection.category || 'Other';

    const skillsHtml = skills.slice(0, 6).map(s =>
        `<span class="collection-skill-tag">${escapeHtml(s)}</span>`
    ).join('');
    const moreSkills = skills.length > 6 ? `<span class="collection-skill-tag more">+${skills.length - 6} more</span>` : '';

    const commandsHtml = commands.slice(0, 3).map(c =>
        `<code class="collection-cmd">${escapeHtml(c)}</code>`
    ).join('');
    const moreCommands = commands.length > 3 ? `<span class="collection-skill-tag more">+${commands.length - 3}</span>` : '';

    const tagsHtml = tags.slice(0, 4).map(tag =>
        `<span class="skill-tag">#${escapeHtml(tag)}</span>`
    ).join('');

    return `
        <div class="collection-card">
            <div class="collection-header">
                <span class="collection-icon">📦</span>
                <span class="collection-name">${escapeHtml(collection.name)}</span>
                <span class="skill-category">${escapeHtml(category)}</span>
            </div>
            <p class="skill-description">${escapeHtml(collection.description)}</p>
            <div class="collection-contents">
                <div class="collection-row">
                    <span class="collection-label">Skills (${skills.length}):</span>
                    <div class="collection-items">${skillsHtml}${moreSkills}</div>
                </div>
                ${commands.length > 0 ? `
                <div class="collection-row">
                    <span class="collection-label">Commands (${commands.length}):</span>
                    <div class="collection-items">${commandsHtml}${moreCommands}</div>
                </div>
                ` : ''}
                ${hooks.length > 0 ? `
                <div class="collection-row">
                    <span class="collection-label">Hooks:</span>
                    <div class="collection-items">${hooks.map(h => `<code class="collection-cmd">${escapeHtml(h)}</code>`).join('')}</div>
                </div>
                ` : ''}
            </div>
            <div class="skill-meta">${tagsHtml}</div>
            <div class="skill-install">
                <div class="install-cmd">
                    <span class="prefix">$</span>
                    <span>${escapeHtml(collection.install || 'See repository')}</span>
                    ${collection.install ? `<button class="copy-btn" onclick="copyToClipboard(event, '${escapeHtml(collection.install)}')" title="Copy">📋</button>` : ''}
                </div>
            </div>
            <div class="collection-footer">
                <a href="https://github.com/${escapeHtml(collection.repo)}" target="_blank" style="color: var(--accent-primary); font-size: 0.85rem;">
                    View on GitHub →
                </a>
                ${collection.homepage ? `<a href="${escapeHtml(collection.homepage)}" target="_blank" style="color: var(--text-secondary); font-size: 0.85rem;">npm →</a>` : ''}
            </div>
        </div>
    `;
}

// Reverse category code lookup
const CATEGORY_CODES_REVERSE = Object.fromEntries(
    Object.entries(CATEGORY_NAMES).map(([code, name]) => [name.toLowerCase(), code])
);

// Copy text to clipboard
function copyToClipboard(event, text) {
    event.stopPropagation();
    navigator.clipboard.writeText(text).then(() => {
        const btn = event.target;
        btn.textContent = '✓';
        setTimeout(() => btn.textContent = '📋', 1500);
    });
}

// Show favorites
function showFavorites() {
    elements.favoritesSection.classList.remove('hidden');

    if (state.favorites.length === 0) {
        elements.favoritesList.classList.add('hidden');
        elements.favoritesEmpty.classList.remove('hidden');
        return;
    }

    elements.favoritesEmpty.classList.add('hidden');
    elements.favoritesList.classList.remove('hidden');

    // Find favorite skills
    const favoriteSkills = state.favorites
        .map(install => state.index.s.find(s => s.i === install))
        .filter(Boolean);

    elements.favoritesList.innerHTML = favoriteSkills.map(skill =>
        createSkillCard(skill, false, true)
    ).join('');
}

// Toggle favorite
function toggleFavorite(event, install) {
    event.stopPropagation();

    const index = state.favorites.indexOf(install);
    if (index > -1) {
        state.favorites.splice(index, 1);
    } else {
        state.favorites.push(install);
    }

    // Save to localStorage
    localStorage.setItem('skillFavorites', JSON.stringify(state.favorites));

    // Update button
    const btn = event.target;
    const isFavorite = state.favorites.includes(install);
    btn.textContent = isFavorite ? '❤️' : '🤍';
    btn.classList.toggle('active', isFavorite);

    // Update favorites view if currently showing
    if (state.currentView === 'favorites') {
        showFavorites();
    }
}

// Show random skill
function showRandomSkill() {
    const randomIndex = Math.floor(Math.random() * state.index.s.length);
    const skill = state.index.s[randomIndex];

    // Create a temporary card element to pass to showSkillDetail
    const tempCard = document.createElement('div');
    tempCard.dataset.install = skill.i;
    showSkillDetail(tempCard);
}

// Create skill card HTML
function createSkillCard(skill, isFeatured = false, showFavoriteBtn = true) {
    const name = isFeatured ? skill.name : skill.n;
    const description = isFeatured ? skill.description : skill.d;
    const category = isFeatured ? skill.category : CATEGORY_NAMES[skill.c] || skill.c;
    const categoryCode = isFeatured ? skill.category : skill.c;
    const tags = isFeatured ? (skill.tags || []) : (skill.g || []);
    const stars = isFeatured ? skill.stars : skill.r;
    const install = isFeatured ? skill.install : skill.i;

    const isFavorite = state.favorites.includes(install);
    const isOfficial = categoryCode === 'off' || categoryCode === 'official';

    const tagsHtml = tags.slice(0, 3).map(tag =>
        `<span class="skill-tag">#${tag}</span>`
    ).join('');

    return `
        <div class="skill-card" data-install="${escapeHtml(install)}" onclick="showSkillDetail(this)">
            <div class="skill-header">
                <span class="skill-name">
                    ${escapeHtml(name)}
                    ${isOfficial ? '<span class="official-badge" title="Official Anthropic Skill">✓</span>' : ''}
                </span>
                <div class="skill-header-right">
                    ${stars > 0 ? `<span class="skill-stars">⭐ ${stars.toLocaleString()}</span>` : ''}
                    ${showFavoriteBtn ? `
                        <button class="favorite-btn ${isFavorite ? 'active' : ''}" onclick="toggleFavorite(event, '${escapeHtml(install)}')" title="${isFavorite ? 'Remove from favorites' : 'Add to favorites'}">
                            ${isFavorite ? '❤️' : '🤍'}
                        </button>
                    ` : ''}
                </div>
            </div>
            <p class="skill-description">${escapeHtml(description)}</p>
            <div class="skill-meta">
                <span class="skill-category">${escapeHtml(category)}</span>
                <div class="skill-tags">${tagsHtml}</div>
            </div>
            <div class="skill-install">
                <div class="install-cmd">
                    <span class="prefix">$</span>
                    <span>sk install ${escapeHtml(install)}</span>
                    <button class="copy-btn" onclick="copyInstall(event, '${escapeHtml(install)}')" title="Copy">📋</button>
                </div>
            </div>
        </div>
    `;
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
    elements.collectionsSection.classList.add('hidden');
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
    elements.resultCount.textContent = `${results.length.toLocaleString()} results`;
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

// Display results with pagination
function displayResults() {
    const start = state.displayedCount;
    const end = start + CONFIG.PAGE_SIZE;
    const pageResults = state.results.slice(start, end);

    const html = pageResults.map(result => createSkillCard(result.item)).join('');

    if (start === 0) {
        elements.searchResults.innerHTML = html;
    } else {
        elements.searchResults.insertAdjacentHTML('beforeend', html);
    }

    state.displayedCount = end;

    // Show/hide load more
    if (state.displayedCount < state.results.length) {
        elements.loadMore.classList.remove('hidden');
    } else {
        elements.loadMore.classList.add('hidden');
    }
}

// Show skill detail modal with similar skills
async function showSkillDetail(card) {
    const install = card.dataset.install;

    // Find skill in index
    const skill = state.index.s.find(s => s.i === install);
    if (!skill) return;

    const tagsHtml = (skill.g || []).map(tag =>
        `<span class="tag">#${tag}</span>`
    ).join(' ');

    const isFavorite = state.favorites.includes(install);
    const isOfficial = skill.c === 'off';

    // Find similar skills based on tags
    const similarSkills = findSimilarSkills(skill, 4);
    const similarHtml = similarSkills.length > 0 ? `
        <div class="similar-skills">
            <h4>Similar Skills</h4>
            <div class="similar-grid">
                ${similarSkills.map(s => `
                    <div class="similar-card" data-install="${escapeHtml(s.i)}" onclick="showSkillDetail(this)">
                        <span class="similar-name">${escapeHtml(s.n)}</span>
                        <span class="similar-stars">${s.r > 0 ? '⭐' + s.r.toLocaleString() : ''}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    ` : '';

    elements.modalBody.innerHTML = `
        <div class="modal-header-row">
            <h2 style="color: var(--accent-primary);">
                ${escapeHtml(skill.n)}
                ${isOfficial ? '<span class="official-badge" title="Official Anthropic Skill">✓</span>' : ''}
            </h2>
            <button class="favorite-btn large ${isFavorite ? 'active' : ''}" onclick="toggleFavorite(event, '${escapeHtml(install)}')">
                ${isFavorite ? '❤️' : '🤍'}
            </button>
        </div>
        <p style="margin-bottom: 1rem; color: var(--text-secondary);">${escapeHtml(skill.d)}</p>

        <div style="margin-bottom: 1rem;">
            <strong>Category:</strong> ${CATEGORY_NAMES[skill.c] || skill.c}<br>
            <strong>Stars:</strong> ${skill.r > 0 ? '⭐ ' + skill.r.toLocaleString() : 'N/A'}
        </div>

        ${tagsHtml ? `<div style="margin-bottom: 1rem;">${tagsHtml}</div>` : ''}

        <!-- Community Stats -->
        <div class="community-stats" id="community-stats-${escapeHtml(install).replace(/[^a-zA-Z0-9]/g, '-')}">
            <button class="like-btn" id="like-btn" onclick="handleLike('${escapeHtml(install)}')">
                <span class="like-icon">👍</span>
                <span class="like-count" id="like-count">0</span>
            </button>
            <span class="comment-count" id="comment-count-display">💬 0 comments</span>
        </div>

        <div style="margin-top: 1.5rem;">
            <strong>Install:</strong>
            <div class="install-cmd" style="margin-top: 0.5rem;">
                <span class="prefix">$</span>
                <span>sk install ${escapeHtml(install)}</span>
                <button class="copy-btn" onclick="copyInstall(event, '${escapeHtml(install)}')" title="Copy">📋</button>
            </div>
        </div>

        <div style="margin-top: 1rem;">
            <a href="${getGitHubUrl(install, skill.b || 'main')}" target="_blank" style="color: var(--accent-primary);">
                View on GitHub →
            </a>
        </div>

        ${similarHtml}

        <!-- Comments Section -->
        <div class="comments-section">
            <h4>💬 Comments</h4>
            <div class="comment-form">
                <input type="text" id="comment-nickname" placeholder="Nickname (optional)" maxlength="30">
                <div class="rating-input" id="rating-input">
                    <span class="rating-star" data-rating="1">☆</span>
                    <span class="rating-star" data-rating="2">☆</span>
                    <span class="rating-star" data-rating="3">☆</span>
                    <span class="rating-star" data-rating="4">☆</span>
                    <span class="rating-star" data-rating="5">☆</span>
                </div>
                <textarea id="comment-content" placeholder="Share your thoughts about this skill..." maxlength="500"></textarea>
                <button class="submit-comment-btn" onclick="handleSubmitComment('${escapeHtml(install)}')">Post Comment</button>
            </div>
            <div class="comments-list" id="comments-list">
                <div class="loading-comments">Loading comments...</div>
            </div>
        </div>
    `;

    elements.modal.classList.remove('hidden');

    // Load community stats and comments
    loadCommunityData(install);
}

// Load community data (stats + comments)
async function loadCommunityData(install) {
    if (!window.SkillsDB) return;

    try {
        // Load stats
        const stats = await window.SkillsDB.getSkillStats(install);
        const likeBtn = document.getElementById('like-btn');
        const likeCount = document.getElementById('like-count');
        const commentCountDisplay = document.getElementById('comment-count-display');

        if (likeBtn && likeCount) {
            likeCount.textContent = stats.likes_count || 0;
            if (stats.liked) {
                likeBtn.classList.add('liked');
                likeBtn.querySelector('.like-icon').textContent = '👍';
            }
        }
        if (commentCountDisplay) {
            commentCountDisplay.textContent = `💬 ${stats.comments_count || 0} comments`;
        }

        // Load comments
        const comments = await window.SkillsDB.getComments(install);
        renderComments(comments);

    } catch (error) {
        console.error('Error loading community data:', error);
    }
}

// Handle like button click
async function handleLike(install) {
    if (!window.SkillsDB) return;

    const likeBtn = document.getElementById('like-btn');
    const likeCount = document.getElementById('like-count');

    // Optimistic UI update
    const wasLiked = likeBtn.classList.contains('liked');
    likeBtn.classList.toggle('liked');
    const currentCount = parseInt(likeCount.textContent) || 0;
    likeCount.textContent = wasLiked ? Math.max(0, currentCount - 1) : currentCount + 1;

    // API call
    const result = await window.SkillsDB.toggleLike(install);
    if (result) {
        likeCount.textContent = result.count;
        likeBtn.classList.toggle('liked', result.liked);
    }
}

// Rating state
let currentRating = 0;

// Handle rating click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('rating-star')) {
        const rating = parseInt(e.target.dataset.rating);
        currentRating = rating;
        updateRatingDisplay(rating);
    }
});

function updateRatingDisplay(rating) {
    document.querySelectorAll('.rating-star').forEach((star, index) => {
        star.textContent = index < rating ? '★' : '☆';
        star.classList.toggle('active', index < rating);
    });
}

// Handle comment submission
async function handleSubmitComment(install) {
    if (!window.SkillsDB) return;

    const nicknameInput = document.getElementById('comment-nickname');
    const contentInput = document.getElementById('comment-content');
    const submitBtn = document.querySelector('.submit-comment-btn');

    const content = contentInput.value.trim();
    if (!content) {
        alert('Please enter a comment');
        return;
    }

    const nickname = nicknameInput.value.trim() || 'Anonymous';

    // Disable button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Posting...';

    try {
        const result = await window.SkillsDB.addComment(install, content, nickname, currentRating || null);

        if (result.success) {
            // Clear form
            contentInput.value = '';
            nicknameInput.value = '';
            currentRating = 0;
            updateRatingDisplay(0);

            // Reload comments
            const comments = await window.SkillsDB.getComments(install);
            renderComments(comments);

            // Update comment count
            const commentCountDisplay = document.getElementById('comment-count-display');
            if (commentCountDisplay) {
                const count = parseInt(commentCountDisplay.textContent.match(/\d+/)?.[0] || 0) + 1;
                commentCountDisplay.textContent = `💬 ${count} comments`;
            }
        } else {
            alert('Failed to post comment. Please try again.');
        }
    } catch (error) {
        console.error('Error posting comment:', error);
        alert('Failed to post comment. Please try again.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Post Comment';
    }
}

// Render comments
function renderComments(comments) {
    const commentsList = document.getElementById('comments-list');
    if (!commentsList) return;

    if (!comments || comments.length === 0) {
        commentsList.innerHTML = '<div class="no-comments">No comments yet. Be the first to share your thoughts!</div>';
        return;
    }

    commentsList.innerHTML = comments.map(comment => {
        const date = new Date(comment.created_at).toLocaleDateString();
        const ratingHtml = comment.rating ?
            `<span class="comment-rating">${'★'.repeat(comment.rating)}${'☆'.repeat(5 - comment.rating)}</span>` : '';

        return `
            <div class="comment-item">
                <div class="comment-header">
                    <span class="comment-author">${escapeHtml(comment.nickname)}</span>
                    ${ratingHtml}
                    <span class="comment-date">${date}</span>
                </div>
                <p class="comment-text">${escapeHtml(comment.content)}</p>
            </div>
        `;
    }).join('');
}

// Find similar skills based on tags and category
function findSimilarSkills(skill, limit = 4) {
    const tags = skill.g || [];
    const category = skill.c;

    if (tags.length === 0 && !category) return [];

    // Score each skill by similarity
    const scored = state.index.s
        .filter(s => s.i !== skill.i) // Exclude current skill
        .map(s => {
            let score = 0;
            const sTags = s.g || [];

            // Tag overlap
            const tagOverlap = tags.filter(t => sTags.includes(t)).length;
            score += tagOverlap * 2;

            // Same category
            if (s.c === category) score += 1;

            // Bonus for stars
            if (s.r > 0) score += 0.1;

            return { skill: s, score };
        })
        .filter(item => item.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, limit)
        .map(item => item.skill);

    return scored;
}

// Copy install command
function copyInstall(event, install) {
    event.stopPropagation();
    const cmd = `sk install ${install}`;
    navigator.clipboard.writeText(cmd).then(() => {
        const btn = event.target;
        btn.textContent = '✓';
        setTimeout(() => btn.textContent = '📋', 1500);
    });
}

// Generate proper GitHub URL from install path and branch
function getGitHubUrl(install, branch = 'main') {
    if (!install) return '#';
    const parts = install.split('/');
    if (parts.length < 2) return '#';

    const owner = parts[0];
    const repo = parts[1];
    const path = parts.slice(2).join('/');

    if (path) {
        return `https://github.com/${owner}/${repo}/blob/${branch}/${path}/SKILL.md`;
    } else {
        return `https://github.com/${owner}/${repo}/blob/${branch}/SKILL.md`;
    }
}

// Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Debounce
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
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
    if (state.currentQuery) {
        search(state.currentQuery);
    }
});

elements.sortFilter.addEventListener('change', (e) => {
    state.currentSort = e.target.value;
    if (state.currentQuery) {
        search(state.currentQuery);
    }
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
    applyFiltersAndSearch();
});

// Source filter
elements.sourceFilter.addEventListener('change', (e) => {
    state.currentSourceFilter = e.target.value;
    applyFiltersAndSearch();
});

// Tag filter input
elements.tagFilter.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.value.trim()) {
        e.preventDefault();
        const tag = e.target.value.trim().toLowerCase();
        if (!state.currentTagFilters.includes(tag)) {
            state.currentTagFilters.push(tag);
            renderActiveTags();
            applyFiltersAndSearch();
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
        applyFiltersAndSearch();
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
    applyFiltersAndSearch();
});

// Apply all filters and search
function applyFiltersAndSearch() {
    if (state.currentQuery) {
        search(state.currentQuery);
    } else if (hasActiveFilters()) {
        // If no search query but filters active, search all
        searchWithFiltersOnly();
    }
}

// Check if any filters are active
function hasActiveFilters() {
    return state.currentStarsFilter || state.currentSourceFilter ||
           state.currentTagFilters.length > 0 || state.currentCategory;
}

// Search with only filters (no query)
function searchWithFiltersOnly() {
    const startTime = performance.now();
    state.displayedCount = 0;

    // Get all skills
    let results = state.index.s.map(item => ({ item, score: 0 }));

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
    elements.collectionsSection.classList.add('hidden');
    elements.favoritesSection.classList.add('hidden');
    elements.searchResults.classList.remove('hidden');
    elements.statsBar.classList.remove('hidden');

    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));

    elements.resultCount.textContent = `${results.length.toLocaleString()} results`;
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
