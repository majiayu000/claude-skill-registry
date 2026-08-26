-- Tighten community RLS: public clients may read public fields, while all
-- identity-sensitive writes use authenticated RPCs or ownership policies.

DROP POLICY IF EXISTS "Anyone can insert stats" ON public.skill_stats;
DROP POLICY IF EXISTS "Anyone can update stats" ON public.skill_stats;
DROP POLICY IF EXISTS "Anyone can read stats" ON public.skill_stats;
DROP POLICY IF EXISTS "Anyone can read likes" ON public.skill_likes;
DROP POLICY IF EXISTS "Anyone can insert likes" ON public.skill_likes;
DROP POLICY IF EXISTS "Users can delete own likes" ON public.skill_likes;
DROP POLICY IF EXISTS "Anyone can insert comments" ON public.skill_comments;
DROP POLICY IF EXISTS "Users can update own comments" ON public.skill_comments;
DROP POLICY IF EXISTS "Users can read own favorites" ON public.user_favorites;
DROP POLICY IF EXISTS "Users can insert favorites" ON public.user_favorites;
DROP POLICY IF EXISTS "Users can delete own favorites" ON public.user_favorites;
DROP POLICY IF EXISTS "Authenticated users can update own comments" ON public.skill_comments;
DROP POLICY IF EXISTS "Authenticated users can read own favorites" ON public.user_favorites;
DROP POLICY IF EXISTS "Authenticated users can insert own favorites" ON public.user_favorites;
DROP POLICY IF EXISTS "Authenticated users can delete own favorites" ON public.user_favorites;

CREATE POLICY "Anyone can read stats" ON public.skill_stats
  FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Anyone can read comments" ON public.skill_comments;
CREATE POLICY "Anyone can read comments" ON public.skill_comments
  FOR SELECT TO anon, authenticated USING (is_deleted = false);

CREATE INDEX IF NOT EXISTS idx_skill_comments_device_created
  ON public.skill_comments(device_id, created_at DESC);

ALTER TABLE public.user_favorites
  DROP CONSTRAINT IF EXISTS user_favorites_skill_install_bounds;
ALTER TABLE public.user_favorites
  ADD CONSTRAINT user_favorites_skill_install_bounds CHECK (
    char_length(btrim(skill_install)) BETWEEN 3 AND 512
    AND strpos(skill_install, '/') > 0
    AND skill_install !~ '[[:cntrl:]]'
  ) NOT VALID;
ALTER TABLE public.user_favorites
  DROP CONSTRAINT IF EXISTS user_favorites_folder_bounds;
ALTER TABLE public.user_favorites
  ADD CONSTRAINT user_favorites_folder_bounds CHECK (
    folder IS NULL OR char_length(folder) <= 50
  ) NOT VALID;
ALTER TABLE public.user_favorites
  DROP CONSTRAINT IF EXISTS user_favorites_note_bounds;
ALTER TABLE public.user_favorites
  ADD CONSTRAINT user_favorites_note_bounds CHECK (
    note IS NULL OR char_length(note) <= 2000
  ) NOT VALID;

REVOKE ALL ON TABLE public.skill_stats FROM anon, authenticated;
REVOKE ALL ON TABLE public.skill_likes FROM anon, authenticated;
REVOKE ALL ON TABLE public.skill_comments FROM anon, authenticated;
REVOKE ALL ON TABLE public.user_favorites FROM anon, authenticated;

GRANT SELECT ON TABLE public.skill_stats TO anon, authenticated;
GRANT SELECT (
  id, skill_install, nickname, content, rating, is_deleted, created_at, updated_at
) ON TABLE public.skill_comments TO anon, authenticated;
GRANT UPDATE (is_deleted) ON TABLE public.skill_comments TO authenticated;

CREATE POLICY "Authenticated users can update own comments" ON public.skill_comments
  FOR UPDATE TO authenticated
  USING (device_id = (SELECT auth.uid())::TEXT)
  WITH CHECK (device_id = (SELECT auth.uid())::TEXT);

CREATE POLICY "Authenticated users can read own favorites" ON public.user_favorites
  FOR SELECT TO authenticated
  USING (device_id = (SELECT auth.uid())::TEXT);

CREATE POLICY "Authenticated users can insert own favorites" ON public.user_favorites
  FOR INSERT TO authenticated
  WITH CHECK (
    device_id = (SELECT auth.uid())::TEXT
    AND (user_id IS NULL OR user_id = (SELECT auth.uid()))
  );

CREATE POLICY "Authenticated users can delete own favorites" ON public.user_favorites
  FOR DELETE TO authenticated
  USING (device_id = (SELECT auth.uid())::TEXT);

-- Replacing a function with a different signature creates an overload, so
-- explicitly remove the old caller-supplied identity variants first.
DROP FUNCTION IF EXISTS public.toggle_like(TEXT, TEXT);
DROP FUNCTION IF EXISTS public.add_comment(TEXT, TEXT, TEXT, TEXT, INT);
DROP FUNCTION IF EXISTS public.get_skill_stats(TEXT, TEXT);

CREATE OR REPLACE FUNCTION public.toggle_like(p_skill_install TEXT)
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

CREATE OR REPLACE FUNCTION public.add_comment(
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

CREATE OR REPLACE FUNCTION public.get_skill_stats(p_skill_install TEXT)
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

CREATE OR REPLACE FUNCTION public.toggle_favorite(p_skill_install TEXT)
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

CREATE OR REPLACE FUNCTION public.get_favorites()
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

CREATE OR REPLACE FUNCTION public.sync_favorites(p_skill_installs TEXT[])
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

CREATE OR REPLACE FUNCTION public.get_trending_skills(p_limit INT DEFAULT 50)
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

REVOKE EXECUTE ON FUNCTION public.toggle_like(TEXT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.add_comment(TEXT, TEXT, TEXT, INT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.get_skill_stats(TEXT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.get_trending_skills(INT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.toggle_favorite(TEXT) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.get_favorites() FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.sync_favorites(TEXT[]) FROM PUBLIC, anon, authenticated;

GRANT EXECUTE ON FUNCTION public.toggle_like(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.add_comment(TEXT, TEXT, TEXT, INT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_skill_stats(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_trending_skills(INT) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION public.toggle_favorite(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_favorites() TO authenticated;
GRANT EXECUTE ON FUNCTION public.sync_favorites(TEXT[]) TO authenticated;
