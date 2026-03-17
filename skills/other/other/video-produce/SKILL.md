---
name: video-produce
description: Full YouTube video production pipeline using agent teams. Coordinates visual design, GIF search, and timeline building with persistent context.
disable-model-invocation: true
---

# YouTube Video Production Pipeline

Run the full video production pipeline using an agent team. Each worker keeps their context so mistakes can be fixed without restarting from scratch.

## Team Structure

Create an agent team called "video-production" with these teammates:

### visual-designer (general-purpose agent)
**Role:** Generate all visual assets - B-roll prompts AND slide prompts.
**Skills to preload:** Load the broll-prompter and slide-prompter agent instructions.
**MCP servers needed:** imagen
**Tasks:**
1. Read the script/prompter file
2. Identify all visual beat opportunities (diagrams, comparisons, data visualizations, concept illustrations)
3. Generate B-roll prompts using the premium minimal style (dark backgrounds, clean typography)
4. Generate slide prompts using the Excalidraw/Hormozi whiteboard style
5. Use the Imagen MCP to generate the images
6. Report what was created and where files are saved

### gif-curator (general-purpose agent)
**Role:** Find and download reaction GIFs for retention beats.
**Skills to preload:** Load the gif-researcher agent instructions.
**MCP servers needed:** giphy
**Tasks:**
1. Read the script/prompter file
2. Identify GIF placement opportunities (humor, pattern interrupts, emotional beats)
3. Generate optimized search queries for Giphy
4. Search and download the best GIFs
5. Report what was found and where files are saved

### timeline-builder (general-purpose agent)
**Role:** Generate timeline.json from script + assets.
**Skills to preload:** Load the timeline-builder agent instructions.
**Tasks (run AFTER visual-designer and gif-curator finish):**
1. Read the script/prompter file and transcript
2. Read what visual-designer and gif-curator created (message them if unclear)
3. Map all assets to word-level timestamps
4. Generate timeline.json following the Remotion schema
5. Validate the timeline references actual files

## Workflow

1. Script is written first (you + `/youtube-script-writer`)
2. Create the team: visual-designer and gif-curator work in parallel
3. When assets are ready, timeline-builder generates timeline.json
4. Review timeline, request fixes - timeline-builder still has context
5. Auto-cutter runs separately if needed (`/auto-cutter`)
6. Render at 4K: `cd tools/video-editor-remotion && npx remotion render src/index.ts MyComposition out/video.mp4 --video-bitrate=35M`

## Input

Provide the script/prompter file path and video project directory:

$ARGUMENTS
