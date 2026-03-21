---
name: md2wechat
description: Convert Markdown to WeChat Official Account HTML, process images, generate cover and infographic images, and create drafts for OpenClaw.
metadata: {"openclaw":{"emoji":"📝","homepage":"https://github.com/geekjourneyx/md2wechat-skill","primaryEnv":"WECHAT_APPID","requires":{"env":["WECHAT_APPID","WECHAT_SECRET"]},"install":[{"id":"openclaw-installer-shell","kind":"download","label":"Download fixed-version OpenClaw installer (shell)","url":"https://github.com/geekjourneyx/md2wechat-skill/releases/download/v2.0.1/install-openclaw.sh","os":["darwin","linux"]},{"id":"openclaw-installer-powershell","kind":"download","label":"Download fixed-version installer (PowerShell)","url":"https://github.com/geekjourneyx/md2wechat-skill/releases/download/v2.0.1/install.ps1","os":["win32"]},{"id":"openclaw-skill-bundle","kind":"download","label":"Download OpenClaw skill bundle","url":"https://github.com/geekjourneyx/md2wechat-skill/releases/download/v2.0.1/md2wechat-openclaw-skill.tar.gz","archive":"tar.gz","targetDir":"~/.openclaw/skills","os":["darwin","linux","win32"]},{"id":"openclaw-runtime-linux","kind":"download","label":"Download md2wechat runtime (Linux amd64)","url":"https://github.com/geekjourneyx/md2wechat-skill/releases/download/v2.0.1/md2wechat-linux-amd64","targetDir":"~/.openclaw/tools/md2wechat","os":["linux"]},{"id":"openclaw-runtime-darwin","kind":"download","label":"Download md2wechat runtime (macOS amd64)","url":"https://github.com/geekjourneyx/md2wechat-skill/releases/download/v2.0.1/md2wechat-darwin-amd64","targetDir":"~/.openclaw/tools/md2wechat","os":["darwin"]}]}}
---

# md2wechat for OpenClaw

Transparency:

- Reads local Markdown files and local images.
- May upload generated images and HTML to WeChat draft and media endpoints.
- May call external image-generation services to create or enrich images.
- Draft upload requires `WECHAT_APPID` and `WECHAT_SECRET`.
- Image generation usually also requires `IMAGE_API_KEY`, plus optional `IMAGE_PROVIDER` / `IMAGE_API_BASE`.

Configuration entry point:

- Check `~/.config/md2wechat/config.yaml` first.
- To change the API domain, image provider, or confirm default mode behavior, see `docs/CONFIG.md` in the repository.
- When `--mode` is not provided explicitly, `convert` still defaults to `api`.

## Runtime Boundary

- This skill only executes an already-installed `md2wechat` runtime.
- It looks for the runtime under `~/.openclaw/tools/md2wechat` first, then falls back to `PATH`.
- The runtime must also match the current skill version. A mismatched runtime is rejected instead of being executed silently.
- It does not download binaries at execution time, does not use a cache bootstrapper, and does not silently fall back to remote downloads.
- `clawhub install md2wechat` currently installs only the skill shell and does **not** guarantee automatic `md2wechat` runtime provisioning.
- `metadata.openclaw.install` exposes fixed-version install resources and installer entry points; the complete and verifiable installation path is still the fixed-version `install-openclaw.sh` installer.

## Recommended Flow

1. Use the fixed-version OpenClaw installer to install both the skill and the runtime. Do not treat `clawhub install md2wechat` as a complete installation path.
2. Use discovery commands first to confirm what the current instance supports:
   - `md2wechat capabilities --json`
   - `md2wechat providers list --json`
   - `md2wechat themes list --json`
   - `md2wechat prompts list --json`
   - `md2wechat prompts list --kind image --archetype cover --json`
3. Then run the task you actually need:
   - `convert <file.md> --preview`
   - `convert <file.md> --draft --cover <cover.jpg>`
   - `generate_cover --article <file.md>`
   - `generate_infographic --article <file.md> --preset infographic-comparison`
   - `generate_image --preset cover-hero --article <file.md> --model <image-model>`
   - `create_image_post -m <file.md> -t "<title>"`
4. If you need AI conversion or AI image generation, add the image-service configuration before running those commands.

When a task depends on a specific resource, inspect it first:

- `md2wechat providers show <name> --json`
- `md2wechat themes show <name> --json`
- `md2wechat prompts show <name> --kind <kind> --json`
- `md2wechat prompts render <name> --kind <kind> --var KEY=VALUE --json`

Recommended image workflow:

- Prefer `generate_cover` for article covers.
- Prefer `generate_infographic` for infographic-style visual summaries.
- Only fall back to `generate_image "raw prompt"` when no suitable preset exists.

See [references/runtime.md](references/runtime.md) for the runtime lookup contract.
