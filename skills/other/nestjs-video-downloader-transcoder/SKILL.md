---
name: video-downloader-transcoder
description: Add, repair, and verify the existing NestJS `VideoDownloaderTranscoderModule` that downloads media with `yt-dlp` via `youtube-dl-exec`, transcodes with `ffmpeg-static`, and maintains `POST /video-downloader-transcoder/transcode` with validated DTOs, quality presets, optional preview embedding, safe subprocess execution, and structured stage logging. Use when users ask to implement/fix video download+transcode APIs, debug yt-dlp/ffmpeg wiring, enforce env-driven limits, or stabilize this synchronous pipeline.
---

# NestJS Video Downloader + Transcoder

## Purpose

Use this skill for changes to the existing synchronous download+transcode feature in a NestJS backend. This skill does not design async queue/job systems unless explicitly requested.

## Target Surface

Primary implementation paths:

1. `src/libs/video-downloader-transcoder/video-downloader-transcoder.module.ts`
2. `src/libs/video-downloader-transcoder/controllers/video-downloader-transcoder.controller.ts`
3. `src/libs/video-downloader-transcoder/services/video-downloader-transcoder.service.ts`
4. `src/libs/video-downloader-transcoder/dtos/transcode-video.dto.ts`
5. `src/libs/video-downloader-transcoder/dtos/transcode-video-response.dto.ts`

## Hard Constraints

1. Require an existing NestJS application. Do not scaffold a new app in this skill.
2. Do not rely on global `ffmpeg`; use `ffmpeg-static` path by default.
3. Use `youtube-dl-exec` for `yt-dlp` execution; support optional custom binary via env.
4. Spawn subprocesses with argument arrays; never interpolate untrusted input into shell strings.
5. Keep the public API transport and route stable unless the user explicitly asks to change it.
6. Keep descriptions/examples generic and avoid site-specific references.

## Workflow

### Step 1: Preflight checks (required)

Verify these before coding:

1. `package.json` includes `@nestjs/core`.
2. App bootstrap file exists at `src/main.ts`.
3. A root module exists (`src/app.module.ts` or equivalent wired in `main.ts`).
4. Target module path exists or user asked to create it.

If preconditions 1-3 fail, stop and ask for the correct existing NestJS app path.

### Step 2: Dependency baseline (required)

Install runtime dependencies:

```bash
npm i youtube-dl-exec ffmpeg-static
```

Dependency roles:

1. `youtube-dl-exec`: manages and invokes `yt-dlp`.
2. `ffmpeg-static`: provides absolute `ffmpeg` executable path.

### Step 3: Enforce module wiring and contracts (required)

Primary files to maintain:

1. `src/libs/video-downloader-transcoder/video-downloader-transcoder.module.ts`
2. `src/libs/video-downloader-transcoder/controllers/video-downloader-transcoder.controller.ts`
3. `src/libs/video-downloader-transcoder/services/video-downloader-transcoder.service.ts`
4. `src/libs/video-downloader-transcoder/dtos/transcode-video.dto.ts`
5. `src/libs/video-downloader-transcoder/dtos/transcode-video-response.dto.ts`

Ensure `VideoDownloaderTranscoderModule` is imported in `src/app.module.ts`.

### Step 4: Preserve DTO and service contract (required)

`VideoDownloaderTranscoderService` must expose:

1. `downloadAndTranscode(dto: TranscodeVideoDto): Promise<TranscodeVideoResponseDto>`

`TranscodeVideoDto` must support:

1. `sourceUrl` (required)
2. `format` enum: `mp4 | webm | mp3`
3. `quality` enum: `auto | best | worst | low | medium | high`
4. `outputName` optional
5. `userAgent` optional
6. `referer` optional
7. `embedPreviewImage` optional

`TranscodeVideoResponseDto` returns:

1. `jobId`
2. `outputPath`
3. `format`
4. `quality`
5. `downloadedBytes`
6. `outputBytes`

### Step 5: Preserve runtime behavior (required)

1. Resolve workdir from env `VIDEO_TRANSCODER_WORKDIR` or default `tmp/videos`.
2. Download with `yt-dlp` using `bestvideo*+bestaudio/best`.
3. Transcode with ffmpeg using mapped quality preset.
4. Support optional preview-image embedding when `embedPreviewImage=true`.
5. Log each stage (`accepted`, `download start/end`, `ffmpeg start/end`, `cleanup`, `error`).
6. Clean temporary files in `finally`.

### Step 6: Enforce security and abuse controls (required)

1. Validate URL and enums through DTO decorators.
2. Enforce max download bytes via `VIDEO_TRANSCODER_MAX_DOWNLOAD_BYTES`.
3. Sanitize `outputName`.
4. Never pass raw shell strings to process execution.
5. Keep proxy/TLS overrides env-driven:
   - `VIDEO_TRANSCODER_YTDLP_PROXY`
   - `VIDEO_TRANSCODER_YTDLP_NO_CHECK_CERTS`
   - `VIDEO_TRANSCODER_YTDLP_FORCE_IPV4`

Use request-level optional headers:

1. `userAgent`
2. `referer`

### Step 7: Verification gates (required)

Run these checks after edits:

1. Build/typecheck passes for the backend project.
2. Route remains `POST /video-downloader-transcoder/transcode` unless explicitly requested otherwise.
3. DTO validation blocks invalid URL/enum inputs.
4. Service still uses argument-array subprocess execution for `yt-dlp` and `ffmpeg`.
5. Temporary artifacts are cleaned on success and error paths.

## Local Implementation References

1. [references/implementation-spec.md](references/implementation-spec.md)
2. [references/api-and-types.md](references/api-and-types.md)
3. [references/ffmpeg-presets.md](references/ffmpeg-presets.md)
4. [references/security-limits.md](references/security-limits.md)
5. [references/test-plan.md](references/test-plan.md)

## Official References

1. NestJS Controllers: https://docs.nestjs.com/controllers
2. NestJS Validation: https://docs.nestjs.com/techniques/validation
3. Node.js child_process: https://nodejs.org/api/child_process.html
4. ffmpeg-static package: https://www.npmjs.com/package/ffmpeg-static
5. youtube-dl-exec package: https://www.npmjs.com/package/youtube-dl-exec
