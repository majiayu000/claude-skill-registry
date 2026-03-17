---
name: helper-reference
description: Tum helper fonksiyonlari referansi. Use for quick lookup of available functions.
---

# Helper Reference

Tum helper dosyalari ve public fonksiyonlari.

## flux_helper.py
FLUX.2 Pro gorsel uretimi.

```python
generate_image_flux(prompt, width=1024, height=1024, output_format="png") -> Dict
# Returns: {success, image_path, duration, cost}

get_credits() -> Dict
# Returns: {success, credits}
```

## cloudinary_helper.py
Video CDN yonetimi.

```python
configure_cloudinary() -> bool
# Cloudinary SDK'yi baslat

upload_video_to_cloudinary(video_path, folder="olivenet-reels") -> Dict
# Returns: {success, url, public_id, duration}

delete_from_cloudinary(public_id) -> Dict
# Returns: {success}
```

## instagram_helper.py
Instagram Graph API v21.0.

```python
# Hesap
get_account_info() -> Dict
# Returns: {username, followers_count, media_count}

# Yayinlama
post_photo_to_instagram(image_url, caption) -> str  # post_id
post_video_to_instagram(video_url, caption) -> str  # post_id
post_carousel_to_instagram(image_urls, caption) -> str  # post_id
post_reels_to_instagram(video_path, caption) -> Dict
# Returns: {success, id}

# Video donusum
convert_video_for_instagram(video_path) -> Dict
# Returns: {success, output_path, converted}

# Insights
get_media_insights(media_id) -> Dict
get_recent_media(limit=10) -> List

# CDN upload
upload_image_to_cdn(image_path) -> str  # public URL
```

## insights_helper.py
Instagram Analytics.

```python
get_instagram_account_info() -> Dict
get_instagram_media_type(media_id) -> Dict
# Returns: {media_type, media_product_type, is_reels}

get_instagram_reels_insights(media_id) -> Dict
# Returns: plays, reach, saves, shares, engagement_rate

get_instagram_image_insights(media_id) -> Dict
# Returns: impressions, reach, saves, likes, engagement_rate

get_instagram_insights() -> List  # Son 10 post
get_best_performing_content() -> List  # Top 20

sync_insights_to_database() -> int  # Guncellenen post sayisi
```

## sora_helper.py
OpenAI Sora video uretimi.

```python
generate_video_sora(prompt, duration=8, size="720x1280", model="sora-2") -> Dict
# Returns: {success, video_path, video_id, model, file_size_mb}

analyze_prompt_complexity(prompt, topic="") -> Dict
# Returns: {complexity, model, duration}
# complexity: high -> sora-2-pro, medium -> sora-2, low -> veo3

generate_video_smart(prompt, topic="", force_model=None, duration=8) -> Dict
# Otomatik model secimi + Veo fallback
# Returns: {success, video_path, model_used}
```

## veo_helper.py
Google Veo video uretimi.

```python
generate_video_veo3(prompt, aspect_ratio="9:16", duration_seconds=8) -> Dict
# Returns: {success, video_path, file_size_mb, model, duration}

generate_video_with_retry(prompt, max_retries=2) -> Dict
# Retry mekanizmali versiyon
```

## gemini_helper.py (devre disi)
Google Gemini gorsel uretimi. Aktif degil, FLUX tercih ediliyor.

```python
generate_realistic_image(topic, post_text, output_dir) -> str  # filepath
create_image_prompt(topic, post_text) -> str  # Ingilizce prompt
test_gemini_connection() -> Dict
```

## claude_helper.py
Claude CLI wrapper ve template generation.

```python
# CLI
run_claude_code(prompt, timeout=60) -> str
# Claude CLI calistir, response dondur

# Icerik
generate_post_text(topic) -> str
# Sosyal medya post metni olustur

# Template generation (HTML)
generate_dashboard_html(data) -> str
generate_feature_grid_html(data) -> str
generate_timeline_html(data) -> str
generate_before_after_html(data) -> str
generate_comparison_html(data) -> str
generate_quote_html(data) -> str
generate_billboard_html(data) -> str
generate_big_number_html(data) -> str
generate_process_html(data) -> str
generate_checklist_html(data) -> str
```

## renderer.py
HTML -> PNG rendering.

```python
render_html_to_png(html_content, output_path=None, width=1080, height=1080) -> str
# Returns: PNG dosya yolu

render_html_file_to_png(html_path, output_path=None) -> str
# HTML dosyasindan render

save_html_and_render(html_content, base_name=None) -> Tuple[str, str]
# Returns: (html_path, png_path)

get_browser() -> Browser  # Playwright browser
close_browser() -> None
cleanup() -> None
```

## config.py
Konfigürasyon ve ayarlar.

```python
settings.telegram_bot_token
settings.telegram_admin_chat_id
settings.instagram_access_token
settings.instagram_user_id
settings.gemini_api_key
settings.flux_api_key
settings.openai_api_key
settings.cloudinary_cloud_name

# Paths
settings.base_dir
settings.context_dir
settings.templates_dir
settings.outputs_dir
settings.database_path

# Timeouts
settings.claude_timeout_post  # 60s
settings.claude_timeout_visual  # 90s
settings.api_timeout_video  # 300s

# Thresholds
settings.min_review_score  # 7.0
settings.max_instagram_words  # 120
```

## Dosya Konumlari

| Helper | Konum |
|--------|-------|
| flux_helper.py | app/flux_helper.py |
| cloudinary_helper.py | app/cloudinary_helper.py |
| instagram_helper.py | app/instagram_helper.py |
| insights_helper.py | app/insights_helper.py |
| sora_helper.py | app/sora_helper.py |
| veo_helper.py | app/veo_helper.py |
| gemini_helper.py | app/gemini_helper.py |
| claude_helper.py | app/claude_helper.py |
| renderer.py | app/renderer.py |
| config.py | app/config.py |
