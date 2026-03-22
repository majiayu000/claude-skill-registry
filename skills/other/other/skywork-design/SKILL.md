---
name: Skywork Design
description: Generate or edit images via backend Skywork Image API. Use for any image creation, poster design, logo design, visual asset generation, or image modification request. Supports text-to-image and image-to-image editing with aspect ratio and resolution control.
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Visual Design — Image Generation & Editing

Generate new images or edit existing ones via the backend image API.
Be patient, it takes about 2 minutes to generate an image each time.

---

## Authentication (Required First)

Before using this skill, authentication must be completed. Run the auth script first:

```bash
# Authenticate: checks env token / cached token / browser login
python3 <skill-dir>/scripts/skywork_auth.py || exit 1
```

**Token priority**:
1. Environment variable `SKYBOT_TOKEN` → if set, use directly
2. Cached token file `~/.skywork_token` → validate via API, if valid, use it
3. No valid token → opens browser for login, polls until complete, saves token

**IMPORTANT - Login URL handling**: If script output contains a line starting with `[LOGIN_URL]`, you **MUST** immediately send that URL to the user in a clickable message (e.g. "Please open this link to log in: <url>"). The user may be in an environment where the browser cannot open automatically, so always surface the login URL.

---

## Usage

Run the script using absolute path (do NOT cd to skill directory):

**Generate new image:**
```bash
python3 <SKILL_DIR>/scripts/generate_image.py --prompt "description" --filename "output.png" [--aspect-ratio 3:4] [--resolution 1K|2K|4K]
```

**Edit existing image:**
```bash
python3 <SKILL_DIR>/scripts/generate_image.py --prompt "edit instructions" --filename "output.png" --input-image "source.png" [--aspect-ratio 3:4] [--resolution 2K]
```

**Edit with multiple reference images:**
```bash
python3 <SKILL_DIR>/scripts/generate_image.py --prompt "combine these styles" --filename "output.png" -i "ref1.png" -i "ref2.png"
```

Always run from the user's working directory so images save there.

## When to Generate vs Edit

- **Generation** (`--prompt` only): Creating new images from scratch — posters, logos, illustrations, photos, infographics.
- **Editing** (`--prompt` + `--input-image`): User provides existing image(s) and wants modifications — style changes, element addition/removal, color adjustments, format conversion.
  - Notice: Edit api supports character resemblance of up to 4 characters and the fidelity of up to 10 objects in a single workflow

If the user uploads/references images and wants changes, always use `--input-image`.

## Resolution

- **1K** — ~1024px, fast drafts
- **2K** (default) — ~2048px, good for most deliverables
- **4K** — ~4096px, final high-res output

Map user requests: "low/draft" → 1K, "normal/medium/2K" → 2K, "high-res/hi-res/4K/ultra" → 4K.

## Aspect Ratio

Supported ratios: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`.

Selection guidance:
- **1:1** — Social media avatars, icons, album covers
- **3:4 / 4:3** — General posters, presentations
- **4:5 / 5:4** — Instagram posts, portraits
- **9:16 / 16:9** — Mobile stories / desktop wallpapers, video covers
- **2:3 / 3:2** — Print posters, book covers
- **21:9** — Ultra-wide banners, cinema format

If the user doesn't specify, omit `--aspect-ratio` and let the API decide.

## Filename Convention

Pattern: `yyyy-mm-dd-hh-mm-ss-descriptive-name.png`

Examples:
- "A serene Japanese garden" → `2026-03-10-14-23-05-japanese-garden.png`
- "sunset over mountains" → `2026-03-10-15-30-12-sunset-mountains.png`
- Unclear context → `2026-03-10-17-12-48-x9k2.png`

## Preflight

- `command -v python3` (must exist)
- If editing: verify each `--input-image` file exists

## Common Failures

- `Error: Input image not found:` → wrong path; verify `--input-image` file exists
- `HTTP error 500` → backend service error; retry or check server status
- `Request failed: Connection refused` → backend service unavailable; ensure the service is running
- **Insufficient benefit**: The script or log may show a message like `Insufficient benefit. Please upgrade your account at {url}`, meaning the user's benefit level does not meet the requirement for this skill.

### How to reply when benefit is insufficient

When you detect the above, **reply in the user's current language** — do not echo the English message. Use this pattern:

- Convey: "Sorry, image generation failed. This skill requires upgrading your Skywork membership to use." then a single call-to-action link.
- **Format**: One short sentence in the user's language + a link like `[Upgrade now →](url)` or the equivalent in their language.
- **URL**: Extract the upgrade URL from the log/script output (e.g. the `at https://...` part).

## Output

- Script prints the local file path and the OSS URL.
- Depending on the platform, use the most appropriate way to deliver the image (e.g. send as image message, display inline, or print the URLs). By default, return both the local path and OSS URL to the user. The OSS URL ensures cross-platform accessibility.

## Design Scenarios

Match the user's request to a scenario and read the corresponding file for specialized workflow:

- **E-commerce product image**: See [scenarios/e-commerce.md](scenarios/e-commerce.md)
- **Storyboard**: See [scenarios/storyboard.md](scenarios/storyboard.md)
- **Infographic**: See [scenarios/infographic.md](scenarios/infographic.md)
- **Logo**: See [scenarios/logo.md](scenarios/logo.md)
- **Branding / VI**: See [scenarios/branding.md](scenarios/branding.md)
- **Brochure**: See [scenarios/brochure.md](scenarios/brochure.md)
- **Social media**: See [scenarios/social-media.md](scenarios/social-media.md)
- **Poster**: See [scenarios/poster.md](scenarios/poster.md)

## Prompt Engineering

### Prompts Best Practices

Follow these principles for quality prompts using the image API for generation or editing:

- **Describe the scene, don't just list keywords.** A narrative, descriptive paragraph produces much better results than disconnected words. The model's core strength is deep language understanding.
  - Weak: "cat, sunset, beach"
  - Strong: "A ginger tabby cat sitting on a sandy beach at golden hour, facing the camera with soft warm backlighting, shallow depth of field, ocean waves blurred in the background"
- **Be hyper-specific.** The more detail you provide, the more control you have. Include all visual details: style, colors, composition, lighting, background, textures.
- **Provide context and intent.** Explain the purpose of the image — the model's understanding of context influences the output.
- **Use step-by-step instructions** for complex scenes with many elements. Break the prompt into layers: foreground, middle ground, background.
- **Use "semantic negative prompts."** Instead of "no cars," describe positively: "an empty, deserted street with no signs of traffic."
- **Control the camera.** Use photographic and cinematic terms: "wide-angle shot", "macro shot", "low-angle perspective", "bird's eye view", "rule of thirds", "shallow depth of field".
- **Time perception.** If the result needs real-time timeliness, mention the current time context in the prompt.
- **Text in images.** Place text content within double quotation marks:
  > A movie poster with the title "INCEPTION" in large silver metallic letters at the top
- Clearly specify and emphasize the elements that require modification. Describe reference images by their order (first image, second image), not by filename.