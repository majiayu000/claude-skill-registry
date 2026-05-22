/**
 * Rendering, detail modal, and utility helpers for the registry app.
 * Loaded before app.js; functions resolve app globals at call time.
 */

// Show featured skills
function showFeatured() {
    elements.featuredSection.classList.remove('hidden');
    elements.featuredList.innerHTML = state.featured.slice(0, 12).map(skill =>
        createSkillCard(skill, true)
    ).join('');
}

// Show leaderboard
async function showLeaderboard(categoryFilter = '') {
    elements.leaderboardSection.classList.remove('hidden');
    elements.leaderboardList.innerHTML = '';

    let skills;
    try {
        skills = categoryFilter
            ? await loadCategorySkills(categoryFilter)
            : await loadFullSearchSkills();
    } catch (error) {
        console.warn('Failed to load full leaderboard data; using startup index:', error);
        skills = categoryFilter
            ? state.index.s.filter(s => s.c === categoryFilter)
            : state.index.s;
    }

    // Sort by stars descending
    skills = [...skills]
        .filter(s => s.r > 0)
        .sort((a, b) => (b.r || 0) - (a.r || 0));

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

    const totalSkills = getTotalSkillCount();
    const uniqueRepos = getNumericStat('unique_repo_count', countUniqueRepos(state.index.s));
    const officialCount = getNumericStat('official_skill_count', getCategoryCount('off'));
    const categoryCount = state.categories.length || getNumericStat('categories', 0);
    const pluginCount = state.plugins.length || getNumericStat('total_plugins', 0);

    document.getElementById('stat-total').textContent = totalSkills.toLocaleString();
    document.getElementById('stat-repos').textContent = uniqueRepos.toLocaleString();
    document.getElementById('stat-official').textContent = officialCount.toLocaleString();
    document.getElementById('stat-plugins').textContent = pluginCount.toLocaleString();
    document.getElementById('stat-categories').textContent = categoryCount;

    renderCategoryChart();
    renderReposChart();
}

function getNumericStat(key, fallback) {
    const rawValue = state.stats?.[key];
    if (rawValue === null || rawValue === undefined || rawValue === '') {
        return fallback;
    }

    const value = Number(rawValue);
    return Number.isFinite(value) ? value : fallback;
}

function getTotalSkillCount() {
    return getNumericStat(
        'registry_skill_count_dedup',
        Number(state.index?.t || state.index?.s?.length || 0)
    );
}

function getCategoryCount(code) {
    const category = state.categories.find(cat => cat.code === code);
    return Number(category?.count || 0);
}

function getRepoFromInstall(install) {
    const parts = String(install || '').split('/');
    return parts.length >= 2 ? `${parts[0]}/${parts[1]}` : String(install || '');
}

function countUniqueRepos(skills) {
    return new Set(skills.map(skill => getRepoFromInstall(skill.i)).filter(Boolean)).size;
}

// Render category distribution chart
function renderCategoryChart() {
    const chartContainer = document.getElementById('category-chart');

    const sorted = state.categories
        .map(category => [
            category.code,
            Number(category.count || 0),
            category.name || CATEGORY_NAMES[category.code] || category.code
        ])
        .filter(([, count]) => count > 0)
        .sort((a, b) => b[1] - a[1]);

    if (sorted.length === 0) {
        chartContainer.innerHTML = '';
        return;
    }

    const maxCount = sorted[0][1];
    const totalSkills = getTotalSkillCount();

    chartContainer.innerHTML = sorted.map(([code, count, name]) => {
        const color = CATEGORY_COLORS[code] || '#576574';
        const percentage = totalSkills > 0 ? ((count / totalSkills) * 100).toFixed(1) : '0.0';
        const barWidth = (count / maxCount) * 100;

        return `
            <div class="chart-row">
                <div class="chart-label">${escapeHtml(name)}</div>
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

    const sorted = getTopRepositories();

    if (sorted.length === 0) {
        chartContainer.innerHTML = '';
        return;
    }

    const maxCount = sorted[0][1];

    chartContainer.innerHTML = sorted.map(([repo, count], index) => {
        const barWidth = (count / maxCount) * 100;
        const colors = ['#00fff2', '#ff6b6b', '#ffd93d', '#6bcb77', '#c56cf0',
                        '#ff9ff3', '#54a0ff', '#ff9f43', '#5f27cd', '#00d2d3'];

        return `
            <div class="chart-row">
                <div class="chart-label" title="${escapeHtml(repo)}">${escapeHtml(repo.length > 25 ? repo.slice(0, 25) + '...' : repo)}</div>
                <div class="chart-bar-container">
                    <div class="chart-bar" style="width: ${barWidth}%; background: ${colors[index % colors.length]}"></div>
                </div>
                <div class="chart-value">${count.toLocaleString()}</div>
            </div>
        `;
    }).join('');
}

function getTopRepositories() {
    if (Array.isArray(state.stats?.top_repositories) && state.stats.top_repositories.length > 0) {
        return state.stats.top_repositories
            .map(entry => [entry.repo, Number(entry.count || 0)])
            .filter(([repo, count]) => repo && count > 0)
            .slice(0, 10);
    }

    const repoCounts = {};
    state.index.s.forEach(skill => {
        const repo = getRepoFromInstall(skill.i);
        if (repo) {
            repoCounts[repo] = (repoCounts[repo] || 0) + 1;
        }
    });
    return Object.entries(repoCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
}

// Show plugins
function showPlugins() {
    elements.pluginsSection.classList.remove('hidden');

    if (state.plugins.length === 0) {
        elements.pluginsList.classList.add('hidden');
        elements.pluginsEmpty.classList.remove('hidden');
        return;
    }

    elements.pluginsEmpty.classList.add('hidden');
    elements.pluginsList.classList.remove('hidden');
    elements.pluginsList.innerHTML = state.plugins.map(createPluginCard).join('');
}

// Create plugin card HTML
function createPluginCard(plugin) {
    const skills = plugin.skills || [];
    const commands = plugin.commands || [];
    const hooks = plugin.hooks || [];
    const tags = plugin.tags || [];
    const category = CATEGORY_NAMES[CATEGORY_CODES_REVERSE[plugin.category]] || plugin.category || 'Other';

    const skillsHtml = skills.slice(0, 6).map(s =>
        `<span class="plugin-skill-tag">${escapeHtml(s)}</span>`
    ).join('');
    const moreSkills = skills.length > 6 ? `<span class="plugin-skill-tag more">+${skills.length - 6} more</span>` : '';

    const commandsHtml = commands.slice(0, 3).map(c =>
        `<code class="plugin-cmd">${escapeHtml(c)}</code>`
    ).join('');
    const moreCommands = commands.length > 3 ? `<span class="plugin-skill-tag more">+${commands.length - 3}</span>` : '';

    const tagsHtml = tags.slice(0, 4).map(tag =>
        `<span class="skill-tag">#${escapeHtml(tag)}</span>`
    ).join('');

    return `
        <div class="plugin-card">
            <div class="plugin-header">
                <span class="plugin-icon">📦</span>
                <span class="plugin-name">${escapeHtml(plugin.name)}</span>
                <span class="skill-category">${escapeHtml(category)}</span>
            </div>
            <p class="skill-description">${escapeHtml(plugin.description)}</p>
            <div class="plugin-contents">
                <div class="plugin-row">
                    <span class="plugin-label">Skills (${skills.length}):</span>
                    <div class="plugin-items">${skillsHtml}${moreSkills}</div>
                </div>
                ${commands.length > 0 ? `
                <div class="plugin-row">
                    <span class="plugin-label">Commands (${commands.length}):</span>
                    <div class="plugin-items">${commandsHtml}${moreCommands}</div>
                </div>
                ` : ''}
                ${hooks.length > 0 ? `
                <div class="plugin-row">
                    <span class="plugin-label">Hooks:</span>
                    <div class="plugin-items">${hooks.map(h => `<code class="plugin-cmd">${escapeHtml(h)}</code>`).join('')}</div>
                </div>
                ` : ''}
            </div>
            <div class="skill-meta">${tagsHtml}</div>
            <div class="skill-install">
                <div class="install-cmd">
                    <span class="prefix">$</span>
                    <span>${escapeHtml(plugin.install || 'See repository')}</span>
                    ${plugin.install ? `<button class="copy-btn" onclick="copyToClipboard(event, '${escapeHtml(plugin.install)}')" title="Copy">📋</button>` : ''}
                </div>
            </div>
            <div class="plugin-footer">
                <a href="https://github.com/${escapeHtml(plugin.repo)}" target="_blank" style="color: var(--accent-primary); font-size: 0.85rem;">
                    View on GitHub →
                </a>
                ${plugin.homepage ? `<a href="${escapeHtml(plugin.homepage)}" target="_blank" style="color: var(--text-secondary); font-size: 0.85rem;">npm →</a>` : ''}
            </div>
        </div>
    `;
}

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

    // Find skill in the loaded startup index or the current lazy-loaded result page.
    const skill = state.index.s.find(s => s.i === install)
        || state.results.map(result => result.item).find(s => s.i === install);
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
