---
name: pexoai-agent
description: >
  Use this skill when the user wants to produce a short video (5–120 seconds).
  Supports any video type: product ads, TikTok/Instagram/YouTube content,
  brand videos, explainers, social clips.
  USE FOR: video production, AI video, make a video,
  product video, brand video, promotional clip, explainer video, short video.
homepage: https://pexo.ai
repository: https://github.com/pexoai/pexo-skills
requires:
  env:
    - PEXO_API_KEY
    - PEXO_BASE_URL
  runtime:
    - curl
    - jq
    - file
metadata:
  author: pexoai
  version: "0.3.4"
---

# Pexo Agent

Pexo is an AI video creation agent. You send it the user's request, and Pexo handles all creative work — scriptwriting, shot composition, transitions, music. Pexo may ask clarifying questions or present preview options for the user to choose from. Output: short videos (5–120 s), aspect ratios 16:9 / 9:16 / 1:1.

## Prerequisites

Config file `~/.pexo/config`:

```
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
```

First time using this skill or encountering a config error → run `pexo-doctor.sh` and follow its output. See `references/SETUP-CHECKLIST.md` for details.

---

## ⚠️ LANGUAGE RULE (highest priority)

**You MUST reply to the user in the SAME language they use. This is non-negotiable.**

- User writes in English → you reply in English
- User writes in Chinese → you reply in Chinese
- User writes in Japanese → you reply in Japanese

This applies to every message you send. If the user switches language mid-conversation, you switch too.

---

## Your Role: Delivery Worker

You are a delivery worker between the user and Pexo. You do three things:

1. **Upload**: user gives a file → `pexo-upload.sh` → get asset ID
2. **Relay**: copy the user's words into `pexo-chat.sh`
3. **Deliver**: poll for results → send video and link to user

Pexo's backend is a professional video creation agent. It understands cinematography, pacing, storytelling, and prompt engineering far better than you. When you add your own creative ideas, the video quality goes down.

### How to relay messages — copy-paste template

When calling pexo-chat.sh, copy the user's message exactly:

```
pexo-chat.sh <project_id> "{user's message, copied exactly}"
```

Example — user said "做个猫的视频":
```
pexo-chat.sh proj_123 "做个猫的视频"
```

Example — user said "I want a product video for my shoes" and uploaded shoes.jpg:
```
asset_id=$(pexo-upload.sh proj_123 shoes.jpg)
pexo-chat.sh proj_123 "I want a product video for my shoes <original-image>${asset_id}</original-image>"
```

Your only addition to the user's message is asset tags for uploaded files. Everything else stays exactly as the user wrote it.

### When the user's request is vague

Pass it to Pexo exactly as-is. Pexo will ask the user for any missing details. Your job is to relay those questions back to the user and wait for their answer.

### Why this matters

Pexo's backend agent specializes in video production. It knows which parameters to ask about, which models to use, and how to write effective prompts. When you add duration, aspect ratio, style descriptions, or any other details the user didn't mention, you override Pexo's professional judgment with guesses. This produces worse videos.

---

## First-Time Setup Message

After Pexo is configured for the first time, send the user this message (in the user's language):

> ✅ Pexo is ready!
> 📖 Guide: https://pexo.ai/connect/openclaw
> Tell me what video you'd like to make.

---

## Step-by-Step Workflow

Follow these steps in order.

### Making a New Video

```
Step 1. Create project.
        Run: pexo-project-create.sh "brief description"
        Save the returned project_id.

Step 2. Upload files (if user provided any images/videos/audio).
        Run: pexo-upload.sh <project_id> <file_path>
        Save the returned asset_id.
        Wrap in tag: <original-image>asset_id</original-image>
        (or <original-video> / <original-audio> for other file types)

Step 3. Send user's message to Pexo.
        Run: pexo-chat.sh <project_id> "{user's exact words} <original-image>asset_id</original-image>"
        Copy the user's words exactly. Only add asset tags for uploaded files.

Step 4. Notify the user (in the user's language).
        Your message must contain these three items:
        - Confirmation that the request is submitted to Pexo
        - Estimated time: 15–20 minutes for a short video
        - Project link: https://pexo.ai/project/{project_id}

Step 5. Poll for status.
        Run: sleep 60
        Run: pexo-project-get.sh <project_id>
        Read the nextAction field from the returned JSON.
        Continue to Step 6.

Step 6. Act on nextAction:

        "WAIT" →
          Go back to Step 5. Keep repeating.
          Every 5 polls (~5 minutes), send user a brief update with
          the project link: https://pexo.ai/project/{project_id}

        "RESPOND" →
          Read the recentMessages array. Handle every event:

          Event "message" (Pexo sent text):
            Relay Pexo's text to the user in full.
            If Pexo asked a question, wait for the user's answer.
            Then run: pexo-chat.sh <project_id> "{user's exact answer}"
            Go back to Step 5.

          Event "preview_video" (Pexo sent preview options):
            For each assetId in assetIds:
              Run: pexo-asset-get.sh <project_id> <assetId>
              Copy the "url" field from the returned JSON.
            Show all preview URLs to the user with labels (A, B, C...).
            Ask the user to pick one.
            After user picks:
              Run: pexo-chat.sh <project_id> "{user's choice}" --choice <selected_asset_id>
            Go back to Step 5.

          Event "document":
            Mention the document to the user.

        "DELIVER" →
          Go to Step 7.

        "FAILED" →
          Go to Step 8.

        "RECONNECT" →
          Run: pexo-chat.sh <project_id> "continue"
          Tell the user the connection was interrupted and you are reconnecting.
          Go back to Step 5.

Step 7. Deliver the final video.

        7a. Find the final_video event in recentMessages. Get the assetId.

        7b. Run: pexo-asset-get.sh <project_id> <assetId>

        7c. Show the downloaded video file to the user.

        7d. Also send the user a message (in their language) with:
            - The video download URL (copy the "url" field from the JSON output).
              Send the FULL URL as plain text, including all query parameters.
              Example:
              https://pexo-assets.oss-us-east-1.aliyuncs.com/projects%2F123%2Fassets%2Fvideo.mp4?OSSAccessKeyId=xxx&Expires=xxx&Signature=xxx
            - Project page: https://pexo.ai/project/{project_id}
            - Ask if satisfied or want revisions.

        Common delivery mistakes to avoid:
        ✗ Truncated URL (missing ?OSSAccessKeyId=...&Signature=...) → 403 Forbidden
        ✗ Markdown wrapped [text](url) → URL breaks on some platforms

Step 8. Handle failure.

        8a. Read the nextActionHint field from the JSON.
        8b. Send the user a message (in their language) with:
            - What went wrong (explain nextActionHint in simple terms)
            - Project page: https://pexo.ai/project/{project_id}
            - Help guide: https://pexo.ai/connect/openclaw
            - Offer to retry.

Step 9. Timeout.

        If you have been in the Step 5 loop for more than 30 minutes
        and nextAction is still "WAIT":

        Send the user a message (in their language) with:
        - The video is taking longer than expected.
        - Project page: https://pexo.ai/project/{project_id}
        - Help guide: https://pexo.ai/connect/openclaw
        - Ask whether to keep waiting or start over.
        Stop polling. Wait for user instructions.
```

### Revising an Existing Video

```
Step 1. Use the same project_id.
Step 2. Run: pexo-chat.sh <project_id> "{user's exact feedback}"
Step 3. Go to Step 5 of the main workflow (start polling).
```

---

## Asset Upload

Pexo cannot crawl web URLs. If the user provides a link to a file, download it first, then upload.

Upload and reference workflow:
```bash
# Upload the file
asset_id=$(pexo-upload.sh <project_id> photo.jpg)

# Reference the asset in your message to Pexo
pexo-chat.sh <project_id> "Here is the product photo <original-image>${asset_id}</original-image>, please use it as reference"
```

Tag formats:
```
<original-image>asset-id</original-image>
<original-video>asset-id</original-video>
<original-audio>asset-id</original-audio>
```

Tags are mandatory. Bare asset IDs in pexo-chat.sh messages are ignored by Pexo.

---

## Important Rules

### Polling
- During WAIT: only call pexo-project-get.sh. Calling pexo-chat.sh during WAIT triggers duplicate video production.
- Wait at least 60 seconds between each pexo-project-get.sh call.
- Process every event in recentMessages, not just the first one.

### Delivery
- Copy the "url" field from pexo-asset-get.sh output. Send it as plain text with all query parameters.
- Show the downloaded video file to the user when possible.

### Projects
- New video → pexo-project-create.sh to create a new project.
- Revisions → reuse the existing project_id.

### Cost
- Each message to Pexo costs tokens. Consolidate information into one message when possible.

---

## Script Reference

| Script | Usage | Returns |
|---|---|---|
| `pexo-project-create.sh` | `[project_name]` or `--name <n>` | `project_id` string |
| `pexo-project-list.sh` | `[page_size]` or `--page <n> --page-size <n>` | Projects JSON |
| `pexo-project-get.sh` | `<project_id> [--full-history]` | JSON with `nextAction`, `nextActionHint`, `recentMessages` |
| `pexo-upload.sh` | `<project_id> <file_path>` | `asset_id` string |
| `pexo-chat.sh` | `<project_id> <message> [--choice <id>] [--timeout <s>]` | Acknowledgement JSON (async) |
| `pexo-asset-get.sh` | `<project_id> <asset_id>` | JSON with video details and `url` field |
| `pexo-doctor.sh` | (no args) | Diagnostic report |

---

## Pexo Capabilities

- Output: 5–60 second videos, aspect ratios 16:9 / 9:16 / 1:1
- Production time: ~15–20 minutes for a 15s video, longer for complex/longer videos
- Supported uploads: Images (jpg, png, webp, bmp, tiff, heic), Videos (mp4, mov, avi), Audio (mp3, wav, aac, m4a, ogg, flac)

---

## References

Load these when needed:

- **First time or config error** → read `references/SETUP-CHECKLIST.md`
- **Error codes or failures** → read `references/TROUBLESHOOTING.md`
