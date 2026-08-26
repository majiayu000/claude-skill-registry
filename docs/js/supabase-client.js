/**
 * Supabase Client for Claude Skills Registry
 * 社区功能：点赞、评论、收藏同步
 * 使用 Supabase Anonymous Auth 实现无感匿名用户
 */

const SUPABASE_URL = 'https://gyrtkwwnghfwesvdiwap.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_gAuZcQ3joPqZAnmjdMBckg_WC4DL4Sl';

// 初始化 Supabase 客户端
const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// 用户状态
let currentUser = null;
let isInitialized = false;

// 获取当前用户ID（兼容匿名和登录用户）
function getUserId() {
    return currentUser?.id || localStorage.getItem('deviceId') || 'anonymous';
}

// 初始化匿名认证
async function initAuth() {
    if (isInitialized) return currentUser;

    try {
        // 检查是否已有会话
        const { data: { session } } = await supabaseClient.auth.getSession();

        if (session?.user) {
            currentUser = session.user;
            console.log('Existing session found:', currentUser.id);
        } else {
            // 自动创建匿名用户
            const { data, error } = await supabaseClient.auth.signInAnonymously();

            if (error) {
                console.warn('Anonymous auth failed, falling back to device ID:', error.message);
                // 降级到 device ID
                currentUser = { id: getDeviceIdFallback() };
            } else {
                currentUser = data.user;
                console.log('Anonymous user created:', currentUser.id);
            }
        }

        isInitialized = true;
        return currentUser;
    } catch (error) {
        console.error('Auth init error:', error);
        currentUser = { id: getDeviceIdFallback() };
        isInitialized = true;
        return currentUser;
    }
}

// 降级方案：设备ID
function getDeviceIdFallback() {
    let deviceId = localStorage.getItem('deviceId');
    if (!deviceId) {
        deviceId = 'device_' + crypto.randomUUID();
        localStorage.setItem('deviceId', deviceId);
    }
    return deviceId;
}

// 监听认证状态变化
supabaseClient.auth.onAuthStateChange((event, session) => {
    if (session?.user) {
        currentUser = session.user;
        console.log('Auth state changed:', event, currentUser.id);
    }
});

// 绑定 GitHub 账户（升级匿名用户）
async function linkGitHub() {
    const { data, error } = await supabaseClient.auth.linkIdentity({
        provider: 'github',
        options: {
            redirectTo: window.location.origin
        }
    });

    if (error) {
        console.error('Link GitHub error:', error);
        return { success: false, error: error.message };
    }

    return { success: true, data };
}

// 登出
async function signOut() {
    const { error } = await supabaseClient.auth.signOut();
    if (!error) {
        currentUser = null;
        // 重新创建匿名用户
        await initAuth();
    }
    return { success: !error };
}

// 检查是否是匿名用户
function isAnonymous() {
    return currentUser?.is_anonymous === true;
}

// 获取用户信息
function getUser() {
    return currentUser;
}

// 兼容旧代码的 DEVICE_ID
const DEVICE_ID = getDeviceIdFallback();

// ═══════════════════════════════════════════════════════════
// 点赞功能
// ═══════════════════════════════════════════════════════════

/**
 * 切换点赞状态
 * @param {string} skillInstall - 技能安装路径
 * @returns {Promise<{liked: boolean, count: number}>}
 */
async function toggleLike(skillInstall) {
    try {
        await initAuth(); // 确保已初始化

        const { data, error } = await supabaseClient
            .rpc('toggle_like', {
                p_skill_install: skillInstall
            });

        if (error) throw error;
        return data;
    } catch (error) {
        console.error('Error toggling like:', error);
        // 降级到本地存储
        return toggleLikeLocal(skillInstall);
    }
}

// 本地点赞降级方案
function toggleLikeLocal(skillInstall) {
    const likes = JSON.parse(localStorage.getItem('localLikes') || '{}');
    const isLiked = !likes[skillInstall];

    if (isLiked) {
        likes[skillInstall] = true;
    } else {
        delete likes[skillInstall];
    }

    localStorage.setItem('localLikes', JSON.stringify(likes));
    return { liked: isLiked, count: 0 };
}

/**
 * 检查是否已点赞
 * @param {string} skillInstall
 * @returns {Promise<boolean>}
 */
async function isLiked(skillInstall) {
    try {
        const stats = await getSkillStats(skillInstall);
        return !!stats.liked;
    } catch (error) {
        // 降级检查本地
        const likes = JSON.parse(localStorage.getItem('localLikes') || '{}');
        return !!likes[skillInstall];
    }
}

/**
 * 获取点赞数
 * @param {string} skillInstall
 * @returns {Promise<number>}
 */
async function getLikesCount(skillInstall) {
    try {
        const { data, error } = await supabaseClient
            .from('skill_stats')
            .select('likes_count')
            .eq('skill_install', skillInstall)
            .single();

        if (error && error.code !== 'PGRST116') throw error;
        return data?.likes_count || 0;
    } catch (error) {
        return 0;
    }
}

// ═══════════════════════════════════════════════════════════
// 评论功能
// ═══════════════════════════════════════════════════════════

/**
 * 添加评论
 * @param {string} skillInstall
 * @param {string} content
 * @param {string} nickname
 * @param {number} rating - 1-5
 * @returns {Promise<{id: string, success: boolean}>}
 */
async function addComment(skillInstall, content, nickname = 'Anonymous', rating = null) {
    try {
        await initAuth();

        const { data, error } = await supabaseClient
            .rpc('add_comment', {
                p_skill_install: skillInstall,
                p_content: content,
                p_nickname: nickname,
                p_rating: rating
            });

        if (error) throw error;
        return data;
    } catch (error) {
        console.error('Error adding comment:', error);
        return { success: false, error: error.message };
    }
}

/**
 * 获取技能评论
 * @param {string} skillInstall
 * @param {number} limit
 * @param {number} offset
 * @returns {Promise<Array>}
 */
async function getComments(skillInstall, limit = 20, offset = 0) {
    try {
        const { data, error } = await supabaseClient
            .from('skill_comments')
            .select('id,skill_install,nickname,content,rating,is_deleted,created_at,updated_at')
            .eq('skill_install', skillInstall)
            .eq('is_deleted', false)
            .order('created_at', { ascending: false })
            .range(offset, offset + limit - 1);

        if (error) throw error;
        return data || [];
    } catch (error) {
        console.error('Error fetching comments:', error);
        return [];
    }
}

/**
 * 删除自己的评论
 * @param {string} commentId
 * @returns {Promise<boolean>}
 */
async function deleteComment(commentId) {
    try {
        await initAuth();

        const { error } = await supabaseClient
            .from('skill_comments')
            .update({ is_deleted: true })
            .eq('id', commentId);

        if (error) throw error;
        return true;
    } catch (error) {
        console.error('Error deleting comment:', error);
        return false;
    }
}

// ═══════════════════════════════════════════════════════════
// 收藏功能（云同步）
// ═══════════════════════════════════════════════════════════

/**
 * 切换收藏状态
 * @param {string} skillInstall
 * @returns {Promise<boolean>} - 新的收藏状态
 */
async function toggleFavoriteCloud(skillInstall) {
    try {
        await initAuth();
        const { data, error } = await supabaseClient
            .rpc('toggle_favorite', { p_skill_install: skillInstall });

        if (error) throw error;
        return !!data;
    } catch (error) {
        console.error('Error toggling favorite:', error);
        // 降级到本地存储
        return toggleFavoriteLocal(skillInstall);
    }
}

// 本地收藏降级
function toggleFavoriteLocal(skillInstall) {
    const favorites = JSON.parse(localStorage.getItem('skillFavorites') || '[]');
    const index = favorites.indexOf(skillInstall);

    if (index > -1) {
        favorites.splice(index, 1);
        localStorage.setItem('skillFavorites', JSON.stringify(favorites));
        return false;
    } else {
        favorites.push(skillInstall);
        localStorage.setItem('skillFavorites', JSON.stringify(favorites));
        return true;
    }
}

/**
 * 获取所有收藏
 * @returns {Promise<Array<string>>}
 */
async function getFavorites() {
    try {
        await initAuth();

        const { data, error } = await supabaseClient
            .rpc('get_favorites');

        if (error) throw error;
        return (data || []).map(f => f.skill_install);
    } catch (error) {
        // 降级到本地
        return JSON.parse(localStorage.getItem('skillFavorites') || '[]');
    }
}

/**
 * 同步本地收藏到云端
 */
async function syncFavoritesToCloud() {
    const localFavorites = JSON.parse(localStorage.getItem('skillFavorites') || '[]');
    if (localFavorites.length === 0) return;

    try {
        await initAuth();

        // 获取云端收藏
        const cloudFavorites = await getFavorites();

        // 找出需要同步的
        const toSync = localFavorites.filter(f => !cloudFavorites.includes(f));

        if (toSync.length > 0) {
            const { error } = await supabaseClient
                .rpc('sync_favorites', { p_skill_installs: toSync });

            if (error) throw error;
            console.log(`Synced ${toSync.length} favorites to cloud`);
        }
    } catch (error) {
        console.error('Error syncing favorites:', error);
    }
}

// ═══════════════════════════════════════════════════════════
// 统计和排行
// ═══════════════════════════════════════════════════════════

/**
 * 获取技能统计
 * @param {string} skillInstall
 * @returns {Promise<{likes_count, comments_count, liked, favorited}>}
 */
async function getSkillStats(skillInstall) {
    try {
        await initAuth();

        const { data, error } = await supabaseClient
            .rpc('get_skill_stats', {
                p_skill_install: skillInstall
            });

        if (error) throw error;
        return data;
    } catch (error) {
        return {
            likes_count: 0,
            comments_count: 0,
            liked: false,
            favorited: false
        };
    }
}

/**
 * 获取热门技能排行
 * @param {number} limit
 * @returns {Promise<Array>}
 */
async function getTrendingSkills(limit = 50) {
    try {
        const { data, error } = await supabaseClient
            .rpc('get_trending_skills', { p_limit: limit });

        if (error) throw error;
        return data || [];
    } catch (error) {
        console.error('Error fetching trending:', error);
        return [];
    }
}

/**
 * 批量获取多个技能的统计
 * @param {Array<string>} skillInstalls
 * @returns {Promise<Object>} - { skillInstall: { likes_count, ... } }
 */
async function getBatchStats(skillInstalls) {
    try {
        const { data, error } = await supabaseClient
            .from('skill_stats')
            .select('*')
            .in('skill_install', skillInstalls);

        if (error) throw error;

        const stats = {};
        (data || []).forEach(s => {
            stats[s.skill_install] = s;
        });
        return stats;
    } catch (error) {
        return {};
    }
}

// ═══════════════════════════════════════════════════════════
// 初始化
// ═══════════════════════════════════════════════════════════

// 页面加载时初始化认证并同步收藏
document.addEventListener('DOMContentLoaded', async () => {
    // 初始化匿名认证
    await initAuth();
    console.log('Auth initialized, user:', getUserId());

    // 延迟同步收藏
    setTimeout(syncFavoritesToCloud, 2000);
});

// 导出给全局使用
window.SkillsDB = {
    // 认证相关
    initAuth,
    getUser,
    getUserId,
    isAnonymous,
    linkGitHub,
    signOut,

    // 点赞
    toggleLike,
    isLiked,
    getLikesCount,

    // 评论
    addComment,
    getComments,
    deleteComment,

    // 收藏
    toggleFavorite: toggleFavoriteCloud,
    getFavorites,

    // 统计
    getSkillStats,
    getTrendingSkills,
    getBatchStats,

    // Supabase 客户端（高级用法）
    client: supabaseClient
};
