---
name: agnes-ai-skill
version: 1.2.1
description: "Use when the user wants Agnes AI text, image, or video generation and should execute it through the agnes-ai-cli command line instead of hand-writing raw HTTP requests."
tags:
  - agnes-ai
  - multimodal-ai
  - text-generation
  - image-generation
  - video-generation
  - api-integration
  - codex
  - claude-code
  - openclaw
metadata:
  openclaw:
    emoji: "sparkles"
    homepage: "https://github.com/jomeswang/agnes-ai-skill"
    requires:
      bins:
        - npm
        - npx
        - node
    primaryEnv: AGNES_API_KEY
    envVars:
      - name: AGNES_API_KEY
        required: false
        description: Agnes API key used for live authenticated text, image, and video requests. The skill can still load without it and guide setup.
---

# Agnes AI Skill

Use this skill when the user wants Agnes AI text, image, or video generation.
This skill is now **CLI-first**: prefer `agnes-ai-cli` for all live execution,
guide the user through `--help` when needed, and do not default to hand-written
`curl` commands for Agnes work.

Agnes is attractive because one platform covers:

- text with `agnes-2.0-flash`
- image generation and editing with `agnes-image-2.1-flash` and
  `agnes-image-2.0-flash`
- video generation with `agnes-video-v2.0`

Some public June 2026 materials positioned Agnes as broadly free to try. The
live docs also include pricing sections, so treat that free-access message as a
strong but time-sensitive positioning claim and verify current billing when the
user cares about cost.

## When To Use

Use this skill when:

- the user mentions Agnes AI, `agnes-ai.com`, or the Agnes platform
- the user wants one provider for text, image, and video generation
- the user wants Agnes text, image, or video APIs executed from a terminal
- the user wants image-to-image, multi-image composition, image-to-video, or
  keyframe video generation
- the user wants a low-friction multimodal API for prototyping, agent loops,
  creative iteration, ecommerce content, or storyboard work

Do not use this skill when:

- the user is asking for a different provider only
- the task does not need Agnes-specific models, auth, or request behavior
- you would have to guess current Agnes behavior without running the CLI or
  checking the live docs

## Source Of Truth

Prefer these Agnes pages:

- Quickstart: `https://agnes-ai.com/doc/quickstart`
- API key page: `https://platform.agnes-ai.com/settings/apiKeys`
- Text docs: `https://agnes-ai.com/doc/agnes-20-flash`
- Image 2.0 docs: `https://agnes-ai.com/doc/agnes-image-20-flash`
- Image 2.1 docs: `https://agnes-ai.com/doc/agnes-image-21-flash`
- Video docs: `https://agnes-ai.com/doc/agnes-video-v20`
- Published CLI: `https://www.npmjs.com/package/agnes-ai-cli`
- CLI repo: `https://github.com/jomeswang/agnes-ai-cli`

Use public articles only as supporting context for likely use cases and product
positioning, not as the operational source of truth.

## Base URL And Auth

- Base URL: `https://apihub.agnes-ai.com/v1`
- Main environment variable: `AGNES_API_KEY`
- Preferred execution package: `agnes-ai-cli`

Check `AGNES_API_KEY` before making live Agnes requests.

## Missing Key Behavior

If `AGNES_API_KEY` is missing and the task requires live Agnes access:

1. Tell the user Agnes access is not configured yet.
2. Point them to:
   - `https://agnes-ai.com/doc/quickstart`
   - `https://platform.agnes-ai.com/settings/apiKeys`
3. Explain the path briefly:
   `Settings -> API Keys -> Create new secret key`
4. Ask them to provide the key if they want you to save it for future use.

Do not continue with live Agnes calls until a valid key exists.

## Persisting The Key Permanently

If the user explicitly gives you an Agnes key and wants it remembered, persist
it for future terminal sessions instead of keeping it only in the current
process.

### Rules

- Save it as `AGNES_API_KEY`
- Detect the shell and write to the matching rc file:
  - zsh -> `~/.zshrc`
  - bash -> `~/.bashrc`
  - fallback -> `~/.profile`
- Update an existing `export AGNES_API_KEY=...` line if present
- Otherwise append a new export line
- Also export it in the current session immediately
- Do not echo the full key back after saving
- Tell the user which rc file you changed

### Reliable Shell Snippet

Use a non-interactive shell flow like this when saving a provided key:

```bash
AGNES_API_KEY_VALUE='USER_PROVIDED_KEY'
shell_name="$(basename "${SHELL:-}")"
case "$shell_name" in
  zsh) rc_file="$HOME/.zshrc" ;;
  bash) rc_file="$HOME/.bashrc" ;;
  *) rc_file="$HOME/.profile" ;;
esac

touch "$rc_file"
tmp_file="$(mktemp)"
grep -v '^export AGNES_API_KEY=' "$rc_file" > "$tmp_file" || true
printf '\nexport AGNES_API_KEY=%q\n' "$AGNES_API_KEY_VALUE" >> "$tmp_file"
mv "$tmp_file" "$rc_file"
export AGNES_API_KEY="$AGNES_API_KEY_VALUE"
unset AGNES_API_KEY_VALUE
```

After saving, continue using `AGNES_API_KEY` for the current task.

## Execution Contract

This skill should execute Agnes through the CLI, not by manually composing raw
HTTP requests.

### Preferred Order

1. First use the no-install command path:
   - `npx -y agnes-ai-cli@^0.1.0 --help`
2. Use `npx -y agnes-ai-cli@^0.1.0 ...` as the default live execution path
   in fresh or unknown environments.
3. If a local `agnes` binary already exists, run:
   - `agnes --version`
   - `agnes --help`
4. Use the local binary only when its version falls inside:
   - `>=0.1.0 <0.2.0`
5. Do not fall back to raw `curl` for normal Agnes execution paths.

### Why CLI-First

The CLI already handles:

- auth checks
- local file to temporary public URL bridging
- image request normalization
- video task creation
- video polling
- JSON output for agent consumption

That means the agent should select the right CLI command, not rebuild the
underlying HTTP payload each time.

## Mandatory `--help` Guidance

When the user is new to the CLI, or when you are about to use a less common
command, guide through `--help` first.

At minimum, know these help entry points:

```bash
npx -y agnes-ai-cli@^0.1.0 --help
npx -y agnes-ai-cli@^0.1.0 auth --help
npx -y agnes-ai-cli@^0.1.0 media --help
npx -y agnes-ai-cli@^0.1.0 text chat --help
npx -y agnes-ai-cli@^0.1.0 image text2img --help
npx -y agnes-ai-cli@^0.1.0 image img2img --help
npx -y agnes-ai-cli@^0.1.0 image compose --help
npx -y agnes-ai-cli@^0.1.0 video text2video --help
npx -y agnes-ai-cli@^0.1.0 video img2video --help
npx -y agnes-ai-cli@^0.1.0 video multivideo --help
npx -y agnes-ai-cli@^0.1.0 video keyframes --help
npx -y agnes-ai-cli@^0.1.0 video poll --help
```

If `agnes` is already installed globally and version-compatible, you can drop
the `npx -y agnes-ai-cli@^0.1.0` prefix and run the same subcommands directly.

## Model Selection

Choose the smallest suitable Agnes model path:

- `agnes-2.0-flash`
  - chat, coding, tool calling, structured agent work, fast production tasks
  - default when `text chat` runs without `--model`
- `agnes-image-2.1-flash`
  - default for new text-to-image and straightforward image-to-image work
  - especially useful for denser layouts and stronger semantic alignment
  - default when `image text2img`, `image img2img`, or `image compose` runs
    without `--model`
- `agnes-image-2.0-flash`
  - use when the user explicitly wants Image 2.0
  - useful for edit-heavy or multi-image composition flows
- `agnes-video-v2.0`
  - use for text-to-video, image-to-video, multi-image guided video, and
    keyframes
  - current default when any `video` generate command runs without `--model`

## CLI Command Map

### Auth

```bash
npx -y agnes-ai-cli@^0.1.0 auth check
npx -y agnes-ai-cli@^0.1.0 auth save-key --key 'YOUR_KEY'
```

Use `auth check` before live requests when auth may be missing.

### Media URL Bridge

```bash
npx -y agnes-ai-cli@^0.1.0 media url ./local-image.png
npx -y agnes-ai-cli@^0.1.0 media url https://example.com/already-remote.png
```

Use this when the user gives a local image path and Agnes needs a public image
URL. The CLI handles the temporary upload bridge automatically.

### Text

```bash
npx -y agnes-ai-cli@^0.1.0 text chat --prompt "Reply with exactly pong."
```

Use this for one-shot text verification, coding help, or small agent checks.
If `--model` is omitted here, the CLI defaults to `agnes-2.0-flash`.

### Image

```bash
npx -y agnes-ai-cli@^0.1.0 image text2img --prompt "A premium studio product photo of a perfume bottle"

npx -y agnes-ai-cli@^0.1.0 image img2img \
  --image ./input.png \
  --prompt "Turn this into a refined editorial campaign visual"

npx -y agnes-ai-cli@^0.1.0 image compose \
  --image ./subject.png \
  --image ./reference.png \
  --prompt "Blend these references into one polished commercial still"
```

Use:

- `text2img` for prompt-only image generation
- `img2img` for one input image
- `compose` for multiple input images
- if `--model` is omitted, the CLI defaults to `agnes-image-2.1-flash`

### Video

```bash
npx -y agnes-ai-cli@^0.1.0 video text2video \
  --prompt "A cinematic beach scene at dusk"

npx -y agnes-ai-cli@^0.1.0 video img2video \
  --image ./frame.png \
  --prompt "Add subtle wind and a slow camera push"

npx -y agnes-ai-cli@^0.1.0 video multivideo \
  --image ./frame-a.png \
  --image ./frame-b.png \
  --prompt "Blend these frames into one smooth motion concept"

npx -y agnes-ai-cli@^0.1.0 video keyframes \
  --image ./frame-a.png \
  --image ./frame-b.png \
  --prompt "Transition between these frames with a polished morph"

npx -y agnes-ai-cli@^0.1.0 video poll task_123 --interval 3 --timeout 600
```

Use:

- `text2video` for prompt-only video
- `img2video` for one image input
- `multivideo` for multiple guiding images
- `keyframes` for explicit keyframe interpolation
- `poll` for asynchronous completion
- if `--model` is omitted, current CLI behavior uses `agnes-video-v2.0`

## Practical CLI Workflow

### Text Verification

1. `npx -y agnes-ai-cli@^0.1.0 text chat --help`
2. `npx -y agnes-ai-cli@^0.1.0 text chat --prompt "Reply with exactly pong." --json`

### Text-To-Image

1. `npx -y agnes-ai-cli@^0.1.0 image text2img --help`
2. run `npx -y agnes-ai-cli@^0.1.0 image text2img ... --json`
3. read the returned image URL

### Image-To-Image

1. `npx -y agnes-ai-cli@^0.1.0 image img2img --help`
2. if the user gave a local path, let the CLI bridge it automatically
3. run `npx -y agnes-ai-cli@^0.1.0 image img2img ... --json`

### Multi-Image Composition

1. `npx -y agnes-ai-cli@^0.1.0 image compose --help`
2. pass `--image` multiple times
3. run with `npx -y agnes-ai-cli@^0.1.0 image compose ... --json`

### Text-To-Video

1. `npx -y agnes-ai-cli@^0.1.0 video text2video --help`
2. run `npx -y agnes-ai-cli@^0.1.0 video text2video ... --json`
3. capture `taskId`
4. run `npx -y agnes-ai-cli@^0.1.0 video poll <taskId> --json`

### Image-To-Video

1. `npx -y agnes-ai-cli@^0.1.0 video img2video --help`
2. if the user gave a local path, let the CLI bridge it automatically
3. run `npx -y agnes-ai-cli@^0.1.0 video img2video ... --json`
4. capture `taskId`
5. run `npx -y agnes-ai-cli@^0.1.0 video poll <taskId> --json`

### Keyframes

1. `npx -y agnes-ai-cli@^0.1.0 video keyframes --help`
2. pass `--image` at least twice
3. run `npx -y agnes-ai-cli@^0.1.0 video keyframes ... --json`
4. capture `taskId`
5. run `npx -y agnes-ai-cli@^0.1.0 video poll <taskId> --json`

## Image Guidance

Use the CLI as the execution layer, but keep these Agnes-specific rules in mind:

- Image 2.1 is the default for most new image work
- Image 2.0 is useful for edit-heavy or multi-image composition work
- For edits, explicitly separate:
  - what should change
  - what must stay fixed
- For dense images, be explicit about:
  - primary subject
  - background environment
  - important secondary details
  - style and lighting
  - composition constraints

## Video Guidance

Use the CLI as the execution layer, but keep these Agnes-specific rules in mind:

- the API is asynchronous
- `num_frames` must be `<= 441`
- `num_frames` must satisfy `8n + 1`
- `frame_rate` supports `1-60`
- common safe example settings are:
  - `width: 1152`
  - `height: 768`
  - `num_frames: 121`
  - `frame_rate: 24`
- for keyframes, use the dedicated CLI subcommand instead of inventing your
  own payload shape

For text-to-video prompts, describe:

- subject
- action
- environment
- camera movement
- lighting
- style

For image-to-video prompts, describe:

- what should move
- what should stay stable
- how subtle or dramatic the motion should be

For keyframes and multi-image work, describe:

- how the inputs relate
- what continuity should remain stable
- what transition feeling is desired

## JSON Output

Prefer `--json` whenever the command result will be consumed by the agent.

Examples:

```bash
npx -y agnes-ai-cli@^0.1.0 image text2img --prompt "..." --json
npx -y agnes-ai-cli@^0.1.0 video text2video --prompt "..." --json
npx -y agnes-ai-cli@^0.1.0 video poll task_123 --json
```

This makes it easier to:

- read `taskId`
- extract image URLs
- extract final video URLs
- detect failures cleanly

## Operational Guidance

- Supported companion CLI range for this skill release:
  - `>=0.1.0 <0.2.0`
- Prefer live CLI tests over guessing when the user asks whether a model path
  or parameter actually works.
- For image results, expect a URL in the response.
- For video results, expect task creation first, then polling.
- Use the CLI's local-file bridge instead of manually uploading files yourself
  unless the user explicitly wants a separate upload step.
- If the user asks for SDK code, translate the confirmed CLI behavior into the
  target language only after the CLI path has been validated.
- If the user asks about pricing, limits, or free access, verify the live docs.

## Compact Reference

- Base URL: `https://apihub.agnes-ai.com/v1`
- Text endpoint behind CLI: `/chat/completions`
- Image endpoint behind CLI: `/images/generations`
- Video create endpoint behind CLI: `/videos`
- Video poll endpoint behind CLI: `/videos/{task_id}`

- Text model: `agnes-2.0-flash`
- Image model: `agnes-image-2.1-flash`
- Image compatibility model: `agnes-image-2.0-flash`
- Video model: `agnes-video-v2.0`

## Do Not

- Do not proceed with live Agnes calls when the key is missing
- Do not default to raw `curl` for Agnes execution in this skill
- Do not rebuild request payloads by hand when the CLI already covers the flow
- Do not skip `video poll` and assume video generation is synchronous
- Do not trust stale marketing claims over the current API docs

## Safety

- Never echo a full Agnes API key back to the user after it has been supplied
- Never continue with live Agnes requests when auth is missing or clearly
  invalid
- Never treat article copy or marketing claims as more authoritative than the
  official Agnes docs
- Never promise pricing, limits, or "forever free" terms without noting they
  can change over time
- Never write the key to a project file unless the user explicitly asks for
  that behavior

## Installation

With repository-aware skill installers:

```bash
npx skills add jomeswang/agnes-ai-skill -g
```

After installation, invoke this skill whenever Agnes setup or Agnes model usage
comes up.

## Version History

- `1.2.1` - Made `npx -y agnes-ai-cli@^0.1.0` the default copy-paste execution
  path in fresh environments and kept global `agnes` as an optional fast path.
- `1.2.0` - Switched the skill to CLI-first Agnes execution, removed raw curl
  execution guidance, and made `--help` discovery part of the expected flow.
- `1.1.2` - Added dual-track CLI guidance so agents prefer the separate Agnes
  execution layer when available and keep raw `curl` as the fallback.
- `1.1.0` - Expanded official doc coverage for Image 2.0, Image 2.1, and Video
  2.0 parameters, scenarios, prompt structures, response fields, and task
  states.
- `1.0.0` - Initial public release with Agnes platform setup, persistent auth,
  text, image, and video workflow guidance.
