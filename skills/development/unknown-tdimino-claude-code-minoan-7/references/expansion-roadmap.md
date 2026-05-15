# Expansion Roadmap

Planned engines beyond the free-tier Phase 1 (Vision, GeoSpy, Gemini).

## Phase 2 — Paid APIs

### SerpAPI Google Lens (`rt_lens.py`)
- **Pricing**: $50/mo for 5K searches
- **Signal**: Knowledge graph entities, visual matches, source pages. Superior to Vision API for pop culture identification — recognizes specific TV episodes, movie scenes, characters by name.
- **API**: REST. `engine=google_lens`, image upload or URL. Python SDK: `pip install google-search-results`.
- **Env**: `SERPAPI_KEY`

### TinEye (`rt_tineye.py`)
- **Pricing**: $200/mo for 5K searches
- **Signal**: Exact/near-duplicate provenance tracking. Finds where an image was first published, all domains hosting it, crawl dates. Best for copyright and attribution tracking.
- **API**: REST. Python SDK: `pip install pytineye`. Supports image file or URL input.
- **Env**: `TINEYE_API_KEY`

### Lenso.ai (`rt_lenso.py`)
- **Pricing**: Contact for API pricing
- **Signal**: Category-based reverse search (People/face recognition, Places, Duplicates/copyrights, Similar). Face search returns matching faces across the web.
- **API**: REST, base64 image input. GitHub reference: `lenso-ai/reverse-image-search-api`.
- **Env**: `LENSO_API_KEY`

### Yandex Images (`rt_yandex.py`)
- **Pricing**: $50/mo via SerpAPI (same key as Google Lens)
- **Signal**: Superior face/scene matching, especially for non-US content. Better than Google for Eastern European, Russian, and Asian media.
- **API**: SerpAPI Yandex endpoint. `engine=yandex_images`.
- **Env**: `SERPAPI_KEY` (shared with rt_lens.py)

## Phase 3 — Custom Corpus

### Twelve Labs (`rt_twelvelabs.py`)
- **Pricing**: Free tier: 15 min video indexing. Paid plans for more.
- **Signal**: Video understanding — index your own video library, then search by text, visual similarity, or audio. Best for "find this scene in my collection" rather than identifying unknown sources.
- **API**: REST + Python SDK: `pip install twelvelabs`. Requires pre-indexing videos into an index.
- **Env**: `TWELVELABS_API_KEY`

### Apify Google Lens Scraper (`rt_apify.py`)
- **Pricing**: $7.99/1K searches (pay-per-use, no subscription)
- **Signal**: Cloud-based Google Lens scraper actor. Returns visual matches, AI descriptions, OCR text. Alternative to SerpAPI for pay-as-you-go pricing.
- **API**: Apify platform. Actor: `zen-studio/google-lens-visual-search`. Python client: `pip install apify-client`.
- **Env**: `APIFY_TOKEN`
