---
name: product-shots-image-gen
description: 'Unified image-generation engine for the product-shots ecosystem. Dispatches to the right model family (OpenAI gpt-image-2 / Gemini gemini-3-pro-image-preview Nano Banana Pro) with one parameterised script for text-to-image and image-to-image. Primary backend: OmniMaaS / Cloubic gateway (https://api.omnimaas.com/v1); also supports any OpenAI-SDK-compatible gateway via fallback env vars. Auto-resizes oversized reference images to prevent edge-proxy timeouts. Use when the user says "generate an image", "make a picture", "create a visual", "render this", "edit this image", "做一张图", "生成图片", "改这张图" — or when invoked as the image-generation backend by another product-shots skill (main-image / detail-page / ad-creative / social-post / multi-angle). NOT a creative-direction skill: takes a prompt + optional reference images, returns a file path.'
license: MIT
metadata:
  author: motiful
  source: product-shots ecosystem
  skill_id: product_shots_image_gen
  version: "1.0"
---

# Image Gen

The **image-generation engine** of the product-shots ecosystem. A single, parameterised entry point: routes the request to the correct API endpoint based on model family (OpenAI's `/v1/images/generations` + `/v1/images/edits` vs Gemini's `/v1/chat/completions` multimodal), preprocesses reference images, and returns a saved file path.

**Primary backend: OmniMaaS / Cloubic image gateway** — `https://api.omnimaas.com/v1`. The gateway is OpenAI-SDK-compatible and unifies access to GPT image 2 and the Gemini Nano Banana family behind one auth token. See:

- GPT image 2 via OmniMaaS: https://docs.cloubic.com/docs/zh-CN/image-generation/image-openai
- Gemini via OmniMaaS: https://docs.cloubic.com/docs/zh-CN/image-generation/image-gemini

**Fallback backends:** any other OpenAI-SDK-compatible image gateway works — set `PRODUCT_SHOTS_IMAGEGEN_BASE_URL` + `PRODUCT_SHOTS_IMAGEGEN_API_KEY`, or keep the legacy `CANVASFLOW_IMAGEGEN_*` env vars for migrated installs.

## Onboarding (First-Use Setup)

**Before generating any image, this skill MUST verify an API gateway is configured.** If env vars are missing, surface the instructions below to the user verbatim — never silently fall back to a hard-coded key, never ask the user to fork the repo, never ask them to paste a key into chat.

### Detection logic

Run on every invocation. The resolution order:

1. `OMNIMAAS_API_KEY` (env var, preferred — unified Cloubic / OmniMaaS gateway)
2. `PRODUCT_SHOTS_IMAGEGEN_API_KEY` (env var, generic fallback)
3. `CANVASFLOW_IMAGEGEN_API_KEY` (env var, legacy compatibility)
4. `~/.product_shots_imagegen_api_key` (file, chmod 600, one-line key)
5. `~/.canvasflow_imagegen_api_key` (file, legacy)

If none resolve, **stop and emit the onboarding message** in the next section. Do **NOT** attempt the API call.

### Onboarding message (show to user verbatim when env missing)

> **This skill needs an image-gateway API key before it can generate.** You haven't configured one yet — here's the 30-second setup:
>
> **Option A — temporary (this terminal only):**
> ```bash
> export OMNIMAAS_API_KEY="sk-..."             # your OmniMaaS / Cloubic token
> # optional: only set this if you have a private gateway endpoint
> # export OMNIMAAS_BASE_URL="https://api.omnimaas.com/v1"
> ```
>
> **Option B — persistent across sessions:**
> Add the same `export` line to your `~/.zshrc` (or `~/.bashrc`), then `source ~/.zshrc`.
>
> **Option C — file-based (no env vars):**
> ```bash
> echo "sk-..." > ~/.product_shots_imagegen_api_key
> chmod 600 ~/.product_shots_imagegen_api_key
> ```
>
> **Where the key comes from:** [docs.cloubic.com](https://docs.cloubic.com) — get a token from the OmniMaaS / Cloubic dashboard. The same token covers both OpenAI `gpt-image-2` and Gemini `gemini-3-pro-image-preview` (Nano Banana Pro).
>
> Any OpenAI-SDK-compatible image gateway also works — replace `OMNIMAAS_*` with `PRODUCT_SHOTS_IMAGEGEN_BASE_URL` + `PRODUCT_SHOTS_IMAGEGEN_API_KEY` pointing at your gateway.
>
> Once configured, re-run the original request.

### Security invariants

- **Never** echo the full key. When confirming detection, show only the first 8 characters (`sk-wPfH6K…`).
- **Never** write the key to logs, stdout, or any file inside the repo.
- **Never** instruct the user to fork the repo, edit skill source, or paste their key into chat. The key lives in env / `~/.*_api_key` files only.
- API key is transmitted **only** via the `Authorization: Bearer <key>` header.

### Local-proxy bypass (CN users)

ClashX / Shadowsocks / similar local proxies inject `ALL_PROXY=socks5://...` into the environment, which breaks `requests` (`Missing dependencies for SOCKS support`). The bundled `scripts/generate.py` already handles this via `Session.trust_env = False`. If you implement a custom caller, replicate this pattern.

## Engagement Principles

These rules always apply. Read them before acting.

1. **Auto-detect model family — never ask the user.** The model name (e.g., `gpt-image-2` vs `gemini-3-pro-image-preview`) determines the endpoint and request shape. Caller specifies model; skill resolves family.
2. **Default to `gemini-3-pro-image-preview`** when the caller does not specify a model. It is the strongest single-model performer (Nano Banana Pro) and supports both text-to-image and image-to-image through one endpoint. See `references/model-selection.md`.
3. **Reference images MUST be ≤1024px max dimension AND ≤1MB before being sent.** Auto-resize otherwise. Reason: most edge proxies time out at ~100s; a 2.5MB PNG + base64 expansion + Gemini processing reliably triggers HTTP 524 at that ceiling. See `references/reference-image-handling.md`.
4. **Negative constraints are appended to the prompt as "Avoid: …", never sent as a separate parameter.** No supported model exposes a true `negative_prompt` field; this is by API design, not a workaround.
5. **Aspect ratio handling diverges by family.** OpenAI: translated to a pixel `size` param. Gemini: appended to the prompt text ("aspect ratio: X:Y") since chat-completions has no size field. Caller passes `--aspect-ratio`; skill handles both.
6. **Output is always saved to disk and the path returned.** Never return base64 or URL to the caller — the file on disk is the canonical artifact. Default location uses a timestamp; caller can override with `--output`.
7. **Cost and token usage are logged on every call.** Caller can budget. Estimated rates: gpt-image-2 ≈ ¥0.35/image, gemini-3-pro-image-preview ≈ ¥1/image, gemini-3.1-flash-image-preview ≈ ¥0.20/image.
8. **Bounded retries for image-to-image; fail-fast everywhere else.** Image-to-image calls retry up to **3 attempts** on retryable errors (HTTP 429, 5xx, 524, connection errors, read timeouts) with exponential backoff (1s, 4s, 16s between attempts). Text-to-image calls do **not** retry. Auth errors (401 / 403) fail fast — never retried. See `references/error-handling.md`.
9. **API keys never reach logs or stdout.** Loaded in this order: `OMNIMAAS_API_KEY` (preferred — Cloubic / OmniMaaS gateway) → `PRODUCT_SHOTS_IMAGEGEN_API_KEY` (canonical generic) → `RENDER_API_KEY` (short alias) → `CANVASFLOW_IMAGEGEN_API_KEY` (legacy) → `~/.product_shots_imagegen_api_key` → `~/.product_shots_render_api_key` (compat) → `~/.canvasflow_imagegen_api_key` (legacy). Passed only via the `Authorization` header. Never echoed. The base URL is auto-resolved (defaults to `https://api.omnimaas.com/v1` when `OMNIMAAS_API_KEY` is set without an explicit `OMNIMAAS_BASE_URL`).

## Execution Procedure

Follow this procedure exactly. Each step maps to a section of `scripts/generate.py`.

```
generate_image(prompt, model, [aspect_ratio], [negative_prompt],
               [reference_images], [output_path]) → file_path

# Step 0 — Resolve API key + base URL (MUST come first)
api_key,  key_source = load_api_key()
    # 1. OMNIMAAS_API_KEY env var (preferred — OmniMaaS gateway)
    # 2. PRODUCT_SHOTS_IMAGEGEN_API_KEY env var (canonical generic)
    # 3. RENDER_API_KEY env var (short alias)
    # 4. CANVASFLOW_IMAGEGEN_API_KEY env var (legacy)
    # 5. ~/.product_shots_imagegen_api_key file
    # 6. ~/.product_shots_render_api_key file (compat)
    # 7. ~/.canvasflow_imagegen_api_key file (legacy)
    # fail with clear message if none present
base_url, url_source = load_base_url()
    # 1. OMNIMAAS_BASE_URL env var
    # 2. PRODUCT_SHOTS_IMAGEGEN_BASE_URL env var (canonical generic)
    # 3. RENDER_BASE_URL env var (short alias)
    # 4. CANVASFLOW_IMAGEGEN_BASE_URL env var (legacy)
    # 5. https://api.omnimaas.com/v1 (default when OMNIMAAS_API_KEY is set)

# Step 0a — Validate caller arguments + fill caller-context defaults
args = validate_args(args)                       # see references/parameter-spec.md
    # rejects empty prompt, unknown model, invalid aspect_ratio
    # auto-fills size for OpenAI from aspect_ratio
    # warns when Gemini ignores --n / --size
args = lookup_caller_defaults(caller_skill, surface) | args
    # caller-skill-specific defaults from parameter-spec.md §Family-Specific Defaults
    # explicit args win over defaults (dict merge with args on the right)

# Step 1 — Resolve model + identify family
if not model:
    model = select_default_model(use_case)       # see references/model-selection.md
        # use_case from caller brief: "text-overlay" / "photorealistic" /
        # "creative" / "image-to-image" / "cost-sensitive" / "general" (default)
        # ⚠ "text-overlay" WINS over all others — any caller whose prompt
        # asks for on-image letters or digits (headlines, labels, CTAs,
        # price chips, callouts) MUST pass "text-overlay" so the dispatcher
        # routes to gpt-image-2. Gemini family garbles small text.
family = model_family(model)                     # see references/model-selection.md
    # openai  → {gpt-image-1, gpt-image-2, dall-e-3}
    # gemini  → {gemini-3-pro-image-preview, gemini-3.1-flash-image-preview, ...}
    # unknown → exit with the supported model list

# Step 2 — Preprocess reference images (if any)
for img_path in reference_images:
    img_path = maybe_resize(img_path, max_dim=1024, max_bytes=1MB)
    # Pillow thumbnail → temp file
    # passthrough if already within limits
    # see references/reference-image-handling.md

# Step 3 — Compose effective prompt and size
final_prompt = compose_prompt(prompt, negative_prompt, aspect_ratio, family)
    # Gemini: prompt + "(aspect ratio: X:Y)" + "Avoid: ..."
    # OpenAI: prompt + "Avoid: ..."  (aspect handled via size param instead)
if family == "openai":
    size = OPENAI_SIZE_BY_RATIO[aspect_ratio] OR explicit --size OR "1024x1024"

# Step 4 — Dispatch
if family == "openai":
    if reference_images:
        response = POST <base_url>/images/edits  (multipart, image[]=@file...)
    else:
        response = POST <base_url>/images/generations  (JSON, {model, prompt, n, size})
elif family == "gemini":
    response = POST <base_url>/chat/completions
        body: {model, messages:[{role:"user", content:[
            {type:"text", text: final_prompt},
            {type:"image_url", image_url:{url: data_url_per_ref_image}}, ...
        ]}]}

if response.status != 200:
    handle_http_error(family, response.status, response.body)
                                                 # see references/error-handling.md

# Step 5 — Parse response (family-specific)
if family == "openai":
    first = response.body["data"][0]
    if "b64_json" not in first and "url" not in first:
        classify_response_error(family, response.body)  # references/error-handling.md
    image_bytes = base64_decode(first["b64_json"]) if "b64_json" in first else fetch(first["url"])
    ext = "png"
elif family == "gemini":
    content = response.body["choices"][0]["message"]["content"]
    # content is a markdown string: ![image](data:image/jpeg;base64,...)
    if no "data:image/...;base64" pattern in content:
        classify_response_error(family, response.body)  # references/error-handling.md
    image_bytes = base64_decode(extract_data_url(content))
    ext = "jpeg"

# Step 6 — Save + log
out_path = output_path OR ./output-<unix_ts>.<ext>
write_bytes(out_path, image_bytes)
log(gateway_source, elapsed, file_size, total_tokens, out_path)

# Self-check
assert out_path.exists()
assert out_path.stat().st_size > 10_000        # tiny files = broken response
return out_path
```

## TOC of Module Files

- `references/model-selection.md` — Model catalogue (image models supported by this skill), family routing rules, decision tree for choosing the right model per use case (photorealism / text rendering / cheap-and-fast / CJK text rendering).
- `references/parameter-spec.md` — Every CLI flag of `scripts/generate.py`: name, type, default, applicability per family, valid range. Single source of truth for what callers can pass — including the full API key / base URL resolution order.
- `references/reference-image-handling.md` — The 524 finding, the 1024px / 1MB ceiling, multi-reference behaviour (Gemini ≤9 images per call), passthrough rule, why we use Pillow `thumbnail` (preserves aspect ratio).
- `references/error-handling.md` — Common API failure modes (401 / 429 / 524 / malformed response / connection timeout) with diagnostic messages and recommended caller behaviour. The 524 → resize-and-retry pattern.

## Section Index

```
Goal                                              → SKILL.md intro paragraph
Engagement Principles                             → SKILL.md §Engagement Principles
Execution Procedure                               → SKILL.md §Execution Procedure
Model Selection                                   → references/model-selection.md
   Family Routing
   Model Catalogue
   Decision Tree
Parameter Spec                                    → references/parameter-spec.md
   CLI Flags
   Aspect Ratio → OpenAI Size Mapping
   API Key + Base URL Resolution
Reference Image Handling                          → references/reference-image-handling.md
   The 524 Finding
   Auto-Resize Rule
   Multi-Reference Constraints
Error Handling                                    → references/error-handling.md
   Common Failure Modes
   Retry Patterns
```

## Tooling

- `scripts/generate.py` — the parameterised entry point. Stdlib + `requests` + `Pillow` only. No host capability requirements.
- `scripts/setup.sh` — idempotent dependency installer (Python 3 + pip + requests + Pillow). Run once before first use.
- **No** sub-skill calls. This skill is a leaf: it does not invoke other skills.
- Callers (other product-shots specialists) invoke via shell. Resolve the script path from the host's skill directory rather than hardcoding any platform path:
  ```
  # Path examples — pick whichever your harness uses; do NOT bake one in:
  #   Claude Code:  ~/.claude/skills/product-shots-image-gen/scripts/generate.py
  #   Codex:        ~/.agents/skills/product-shots-image-gen/scripts/generate.py
  #   Cursor:       ~/.cursor/skills/product-shots-image-gen/scripts/generate.py
  #   Windsurf:     ~/.codeium/windsurf/skills/product-shots-image-gen/scripts/generate.py
  #   Copilot:      ~/.copilot/skills/product-shots-image-gen/scripts/generate.py
  python <skill-dir>/scripts/generate.py \
      --prompt "..." --model gemini-3-pro-image-preview --output ./out.jpeg
  ```
  or via direct Python import of the `generate_openai` / `generate_gemini` functions.

## Caller Contract

When invoked from another skill in the product-shots ecosystem (e.g., `product-shots-main-image` reaching its `image = generate_image(prompt)` step), the caller passes:

| Field | Required | Format | Skill behaviour |
|---|---|---|---|
| `prompt` | yes | string, ≤4000 chars | passed through (+ negative + aspect ratio appended) |
| `model` | yes | from supported set | family-routed to correct endpoint |
| `aspect_ratio` | no | "1:1" / "16:9" / "9:16" / "4:3" / "3:4" / "3:2" / "2:3" | OpenAI: → `size`; Gemini: appended to prompt |
| `reference_images` | no | list of file paths | auto-resized to ≤1024px / ≤1MB before send |
| `negative_prompt` | no | string | appended as "Avoid: …" |
| `output` | no | file path | defaults to `./output-<ts>.<png\|jpeg>` |

Returns: file path on disk (PNG for OpenAI, JPEG for Gemini). Caller MUST treat the file as the canonical artifact.

## OmniMaaS gateway setup quickstart

```
# 1. Get an OmniMaaS / Cloubic API token from https://docs.cloubic.com
export OMNIMAAS_API_KEY="your-omnimaas-token"

# 2. (optional) Override the base URL if you have a private endpoint
# export OMNIMAAS_BASE_URL="https://api.omnimaas.com/v1"

# 3. Install dependencies
bash scripts/setup.sh

# 4. Test
python scripts/generate.py --prompt "a red apple on wood" \
                           --model gemini-3-pro-image-preview \
                           --output /tmp/test.jpeg
```

When `OMNIMAAS_API_KEY` is set, the script auto-defaults the base URL to `https://api.omnimaas.com/v1` — no additional configuration required.
