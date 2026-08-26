-- ═══════════════════════════════════════════════════════════
-- Claude Skills Registry - Supabase Schema
-- 社区版：点赞、评论、收藏（不需要强制登录）
-- ═══════════════════════════════════════════════════════════

-- 1. 技能统计表（点赞数、评论数）
CREATE TABLE IF NOT EXISTS skill_stats (
  skill_install TEXT PRIMARY KEY,           -- 技能安装路径，如 "openai/codex/skill-installer"
  likes_count INT DEFAULT 0,                -- 点赞总数
  comments_count INT DEFAULT 0,             -- 评论总数
  views_count INT DEFAULT 0,                -- 浏览次数
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 点赞记录表（防止重复点赞）
CREATE TABLE IF NOT EXISTS skill_likes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  skill_install TEXT NOT NULL,              -- 技能安装路径
  device_id TEXT NOT NULL,                  -- 设备ID（匿名用户）
  user_id UUID REFERENCES auth.users,       -- 可选：登录用户ID
  created_at TIMESTAMPTZ DEFAULT NOW(),

  -- 每个设备/用户只能点赞一次
  UNIQUE(skill_install, device_id)
);

-- 3. 评论表
CREATE TABLE IF NOT EXISTS skill_comments (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  skill_install TEXT NOT NULL,              -- 技能安装路径
  device_id TEXT NOT NULL,                  -- 设备ID
  user_id UUID REFERENCES auth.users,       -- 可选：登录用户ID
  nickname TEXT DEFAULT 'Anonymous',        -- 昵称
  content TEXT NOT NULL,                    -- 评论内容
  rating INT CHECK (rating >= 1 AND rating <= 5), -- 1-5星评分
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. 收藏表（需要设备ID或用户ID）
CREATE TABLE IF NOT EXISTS user_favorites (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  skill_install TEXT NOT NULL,
  device_id TEXT,                           -- 设备ID（匿名用户）
  user_id UUID REFERENCES auth.users,       -- 登录用户ID
  folder TEXT DEFAULT 'default',            -- 收藏夹名称
  note TEXT,                                -- 用户笔记
  created_at TIMESTAMPTZ DEFAULT NOW(),

  -- 每个设备/用户每个技能只收藏一次
  UNIQUE(skill_install, device_id),
  UNIQUE(skill_install, user_id)
);

-- ═══════════════════════════════════════════════════════════
-- 索引优化
-- ═══════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_skill_stats_likes ON skill_stats(likes_count DESC);
CREATE INDEX IF NOT EXISTS idx_skill_comments_skill ON skill_comments(skill_install);
CREATE INDEX IF NOT EXISTS idx_skill_comments_created ON skill_comments(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_skill_comments_device_created ON skill_comments(device_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_favorites_device ON user_favorites(device_id);
CREATE INDEX IF NOT EXISTS idx_user_favorites_user ON user_favorites(user_id);

ALTER TABLE user_favorites
  ADD CONSTRAINT user_favorites_skill_install_bounds CHECK (
    char_length(btrim(skill_install)) BETWEEN 3 AND 512
    AND strpos(skill_install, '/') > 0
    AND skill_install !~ '[[:cntrl:]]'
  );
ALTER TABLE user_favorites
  ADD CONSTRAINT user_favorites_folder_bounds CHECK (
    folder IS NULL OR char_length(folder) <= 50
  );
ALTER TABLE user_favorites
  ADD CONSTRAINT user_favorites_note_bounds CHECK (
    note IS NULL OR char_length(note) <= 2000
  );

-- ═══════════════════════════════════════════════════════════
-- RLS (Row Level Security) 策略
-- ═══════════════════════════════════════════════════════════

-- 启用 RLS
ALTER TABLE skill_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE skill_likes ENABLE ROW LEVEL SECURITY;
ALTER TABLE skill_comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;

-- Public clients can read aggregate stats and non-deleted public comment fields.
CREATE POLICY "Anyone can read stats" ON skill_stats
  FOR SELECT TO anon, authenticated USING (true);

CREATE POLICY "Anyone can read comments" ON skill_comments
  FOR SELECT TO anon, authenticated USING (is_deleted = false);

-- Authenticated and anonymous-auth users may only mutate rows tied to auth.uid().
CREATE POLICY "Authenticated users can update own comments" ON skill_comments
  FOR UPDATE TO authenticated
  USING (device_id = (SELECT auth.uid())::TEXT)
  WITH CHECK (device_id = (SELECT auth.uid())::TEXT);

CREATE POLICY "Authenticated users can read own favorites" ON user_favorites
  FOR SELECT TO authenticated
  USING (device_id = (SELECT auth.uid())::TEXT);

CREATE POLICY "Authenticated users can insert own favorites" ON user_favorites
  FOR INSERT TO authenticated
  WITH CHECK (
    device_id = (SELECT auth.uid())::TEXT
    AND (user_id IS NULL OR user_id = (SELECT auth.uid()))
  );

CREATE POLICY "Authenticated users can delete own favorites" ON user_favorites
  FOR DELETE TO authenticated
  USING (device_id = (SELECT auth.uid())::TEXT);

REVOKE ALL ON TABLE skill_stats FROM anon, authenticated;
REVOKE ALL ON TABLE skill_likes FROM anon, authenticated;
REVOKE ALL ON TABLE skill_comments FROM anon, authenticated;
REVOKE ALL ON TABLE user_favorites FROM anon, authenticated;

GRANT SELECT ON TABLE skill_stats TO anon, authenticated;
GRANT SELECT (
  id, skill_install, nickname, content, rating, is_deleted, created_at, updated_at
) ON TABLE skill_comments TO anon, authenticated;
GRANT UPDATE (is_deleted) ON TABLE skill_comments TO authenticated;

-- ═══════════════════════════════════════════════════════════
-- 辅助函数
-- ═══════════════════════════════════════════════════════════

-- 点赞函数（自动更新统计）
CREATE OR REPLACE FUNCTION toggle_like(p_skill_install TEXT)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_user_id UUID := auth.uid();
  v_device_id TEXT;
  v_skill_install TEXT := btrim(p_skill_install);
  v_exists BOOLEAN;
  v_new_count INT;
BEGIN
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'authentication required' USING ERRCODE = '42501';
  END IF;
  IF v_skill_install IS NULL
     OR char_length(v_skill_install) NOT BETWEEN 3 AND 512
     OR strpos(v_skill_install, '/') = 0
     OR v_skill_install ~ '[[:cntrl:]]' THEN
    RAISE EXCEPTION 'invalid skill install' USING ERRCODE = '22023';
  END IF;

  v_device_id := v_user_id::TEXT;
  PERFORM pg_catalog.pg_advisory_xact_lock(
    pg_catalog.hashtextextended(v_skill_install || ':' || v_device_id, 0)
  );

  SELECT EXISTS(
    SELECT 1 FROM public.skill_likes
    WHERE skill_install = v_skill_install AND device_id = v_device_id
  ) INTO v_exists;

  IF v_exists THEN
    DELETE FROM public.skill_likes
    WHERE skill_install = v_skill_install AND device_id = v_device_id;

    UPDATE public.skill_stats
    SET likes_count = GREATEST(0, likes_count - 1), updated_at = NOW()
    WHERE skill_install = v_skill_install;
  ELSE
    INSERT INTO public.skill_likes (skill_install, device_id, user_id)
    VALUES (v_skill_install, v_device_id, v_user_id);

    INSERT INTO public.skill_stats (skill_install, likes_count)
    VALUES (v_skill_install, 1)
    ON CONFLICT (skill_install)
    DO UPDATE SET
      likes_count = public.skill_stats.likes_count + 1,
      updated_at = NOW();
  END IF;

  SELECT likes_count INTO v_new_count
  FROM public.skill_stats WHERE skill_install = v_skill_install;

  RETURN pg_catalog.json_build_object(
    'liked', NOT v_exists,
    'count', COALESCE(v_new_count, 0)
  );
END;
$$;

-- 添加评论函数
CREATE OR REPLACE FUNCTION add_comment(
  p_skill_install TEXT,
  p_content TEXT,
  p_nickname TEXT DEFAULT 'Anonymous',
  p_rating INT DEFAULT NULL
)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_user_id UUID := auth.uid();
  v_device_id TEXT;
  v_skill_install TEXT := btrim(p_skill_install);
  v_content TEXT := btrim(p_content);
  v_nickname TEXT := COALESCE(NULLIF(btrim(p_nickname), ''), 'Anonymous');
  v_comment_id UUID;
BEGIN
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'authentication required' USING ERRCODE = '42501';
  END IF;
  IF v_skill_install IS NULL
     OR char_length(v_skill_install) NOT BETWEEN 3 AND 512
     OR strpos(v_skill_install, '/') = 0
     OR v_skill_install ~ '[[:cntrl:]]' THEN
    RAISE EXCEPTION 'invalid skill install' USING ERRCODE = '22023';
  END IF;
  IF v_content IS NULL OR char_length(v_content) NOT BETWEEN 1 AND 500 THEN
    RAISE EXCEPTION 'comment must contain 1 to 500 characters' USING ERRCODE = '22023';
  END IF;
  IF char_length(v_nickname) > 30 THEN
    RAISE EXCEPTION 'nickname must contain at most 30 characters' USING ERRCODE = '22023';
  END IF;
  IF p_rating IS NOT NULL AND p_rating NOT BETWEEN 1 AND 5 THEN
    RAISE EXCEPTION 'rating must be between 1 and 5' USING ERRCODE = '22023';
  END IF;

  v_device_id := v_user_id::TEXT;
  IF EXISTS (
    SELECT 1 FROM public.skill_comments
    WHERE device_id = v_device_id
      AND created_at > NOW() - INTERVAL '10 seconds'
  ) THEN
    RAISE EXCEPTION 'comments are limited to one every 10 seconds' USING ERRCODE = 'P0001';
  END IF;

  INSERT INTO public.skill_comments (
    skill_install, device_id, user_id, content, nickname, rating
  ) VALUES (
    v_skill_install, v_device_id, v_user_id, v_content, v_nickname, p_rating
  )
  RETURNING id INTO v_comment_id;

  INSERT INTO public.skill_stats (skill_install, comments_count)
  VALUES (v_skill_install, 1)
  ON CONFLICT (skill_install)
  DO UPDATE SET
    comments_count = public.skill_stats.comments_count + 1,
    updated_at = NOW();

  RETURN pg_catalog.json_build_object('id', v_comment_id, 'success', true);
END;
$$;

-- 获取技能统计和用户状态
CREATE OR REPLACE FUNCTION get_skill_stats(p_skill_install TEXT)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_user_id UUID := auth.uid();
  v_device_id TEXT;
  v_stats public.skill_stats%ROWTYPE;
  v_liked BOOLEAN;
  v_favorited BOOLEAN;
BEGIN
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'authentication required' USING ERRCODE = '42501';
  END IF;
  v_device_id := v_user_id::TEXT;

  SELECT * INTO v_stats
  FROM public.skill_stats WHERE skill_install = p_skill_install;

  SELECT EXISTS(
    SELECT 1 FROM public.skill_likes
    WHERE skill_install = p_skill_install AND device_id = v_device_id
  ) INTO v_liked;

  SELECT EXISTS(
    SELECT 1 FROM public.user_favorites
    WHERE skill_install = p_skill_install AND device_id = v_device_id
  ) INTO v_favorited;

  RETURN pg_catalog.json_build_object(
    'likes_count', COALESCE(v_stats.likes_count, 0),
    'comments_count', COALESCE(v_stats.comments_count, 0),
    'views_count', COALESCE(v_stats.views_count, 0),
    'liked', COALESCE(v_liked, false),
    'favorited', COALESCE(v_favorited, false)
  );
END;
$$;

CREATE OR REPLACE FUNCTION toggle_favorite(p_skill_install TEXT)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_user_id UUID := auth.uid();
  v_device_id TEXT;
  v_skill_install TEXT := btrim(p_skill_install);
  v_changed INT;
BEGIN
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'authentication required' USING ERRCODE = '42501';
  END IF;
  IF v_skill_install IS NULL
     OR char_length(v_skill_install) NOT BETWEEN 3 AND 512
     OR strpos(v_skill_install, '/') = 0
     OR v_skill_install ~ '[[:cntrl:]]' THEN
    RAISE EXCEPTION 'invalid skill install' USING ERRCODE = '22023';
  END IF;

  v_device_id := v_user_id::TEXT;
  PERFORM pg_catalog.pg_advisory_xact_lock(
    pg_catalog.hashtextextended('favorite:' || v_device_id || ':' || v_skill_install, 0)
  );

  DELETE FROM public.user_favorites
  WHERE skill_install = v_skill_install AND device_id = v_device_id;
  GET DIAGNOSTICS v_changed = ROW_COUNT;
  IF v_changed > 0 THEN
    RETURN false;
  END IF;

  IF (SELECT count(*) FROM public.user_favorites WHERE device_id = v_device_id) >= 1000 THEN
    RAISE EXCEPTION 'favorite quota exceeded' USING ERRCODE = 'P0001';
  END IF;

  INSERT INTO public.user_favorites (skill_install, device_id, user_id)
  VALUES (v_skill_install, v_device_id, v_user_id);
  RETURN true;
END;
$$;

CREATE OR REPLACE FUNCTION get_favorites()
RETURNS TABLE (skill_install TEXT)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_user_id UUID := auth.uid();
BEGIN
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'authentication required' USING ERRCODE = '42501';
  END IF;

  RETURN QUERY
  SELECT favorite.skill_install
  FROM public.user_favorites favorite
  WHERE favorite.device_id = v_user_id::TEXT
  ORDER BY favorite.created_at;
END;
$$;

CREATE OR REPLACE FUNCTION sync_favorites(p_skill_installs TEXT[])
RETURNS INT
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_user_id UUID := auth.uid();
  v_device_id TEXT;
  v_existing_count INT;
  v_new_count INT;
  v_inserted INT;
BEGIN
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'authentication required' USING ERRCODE = '42501';
  END IF;
  IF p_skill_installs IS NULL OR cardinality(p_skill_installs) = 0 THEN
    RETURN 0;
  END IF;
  IF cardinality(p_skill_installs) > 500 THEN
    RAISE EXCEPTION 'at most 500 favorites may be synced at once' USING ERRCODE = '22023';
  END IF;
  IF EXISTS (
    SELECT 1 FROM unnest(p_skill_installs) AS candidate(skill_install)
    WHERE candidate.skill_install IS NULL
       OR char_length(btrim(candidate.skill_install)) NOT BETWEEN 3 AND 512
       OR strpos(candidate.skill_install, '/') = 0
       OR candidate.skill_install ~ '[[:cntrl:]]'
  ) THEN
    RAISE EXCEPTION 'invalid skill install' USING ERRCODE = '22023';
  END IF;

  v_device_id := v_user_id::TEXT;
  PERFORM pg_catalog.pg_advisory_xact_lock(
    pg_catalog.hashtextextended('favorite-sync:' || v_device_id, 0)
  );
  SELECT count(*) INTO v_existing_count
  FROM public.user_favorites WHERE device_id = v_device_id;
  SELECT count(*) INTO v_new_count
  FROM (
    SELECT DISTINCT btrim(candidate.skill_install) AS skill_install
    FROM unnest(p_skill_installs) AS candidate(skill_install)
  ) requested
  WHERE NOT EXISTS (
    SELECT 1 FROM public.user_favorites favorite
    WHERE favorite.device_id = v_device_id
      AND favorite.skill_install = requested.skill_install
  );
  IF v_existing_count + v_new_count > 1000 THEN
    RAISE EXCEPTION 'favorite quota exceeded' USING ERRCODE = 'P0001';
  END IF;

  INSERT INTO public.user_favorites (skill_install, device_id, user_id)
  SELECT DISTINCT btrim(candidate.skill_install), v_device_id, v_user_id
  FROM unnest(p_skill_installs) AS candidate(skill_install)
  ON CONFLICT (skill_install, device_id) DO NOTHING;
  GET DIAGNOSTICS v_inserted = ROW_COUNT;
  RETURN v_inserted;
END;
$$;

-- 获取热门技能排行
CREATE OR REPLACE FUNCTION get_trending_skills(p_limit INT DEFAULT 50)
RETURNS TABLE (
  skill_install TEXT,
  likes_count INT,
  comments_count INT,
  score NUMERIC
)
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = ''
AS $$
BEGIN
  IF p_limit IS NULL OR p_limit NOT BETWEEN 1 AND 100 THEN
    RAISE EXCEPTION 'limit must be between 1 and 100' USING ERRCODE = '22023';
  END IF;

  RETURN QUERY
  SELECT
    s.skill_install,
    s.likes_count,
    s.comments_count,
    (s.likes_count * 2 + s.comments_count)::NUMERIC AS score
  FROM public.skill_stats s
  ORDER BY score DESC, s.updated_at DESC
  LIMIT p_limit;
END;
$$;

REVOKE EXECUTE ON FUNCTION toggle_like(TEXT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION add_comment(TEXT, TEXT, TEXT, INT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION get_skill_stats(TEXT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION get_trending_skills(INT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION toggle_favorite(TEXT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION get_favorites() FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION sync_favorites(TEXT[]) FROM PUBLIC, anon, authenticated;

GRANT EXECUTE ON FUNCTION toggle_like(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION add_comment(TEXT, TEXT, TEXT, INT) TO authenticated;
GRANT EXECUTE ON FUNCTION get_skill_stats(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION get_trending_skills(INT) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION toggle_favorite(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION get_favorites() TO authenticated;
GRANT EXECUTE ON FUNCTION sync_favorites(TEXT[]) TO authenticated;
