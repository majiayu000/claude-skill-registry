---
name: video-remotion
description: |
  Comprehensive skill for programmatic video generation using the Remotion framework.
  Enables creating, scaffolding, and rendering React-based videos via Python orchestration.
  Supports both Local (CLI) and Cloud (Lambda) rendering.
---

# 🎬 Remotion Video Generation Skill

This skill provides the capabilities to generate videos programmatically using **Remotion** (React-based video framework). It bridges the gap between Python agents and the Node.js/React rendering engine.

## 📦 Dependencies & Setup

**System Requirements:**
- Node.js (v16+) and npm/yarn/pnpm
- FFmpeg (usually handled by Remotion, but good to have)
- Python 3.8+ (for the wrapper script)

**Python Packages:**
run `uv add remotion-lambda python-dotenv`

**Remotion Project Setup:**
If no project exists, initialize one:
```bash
npx create-remotion@latest ./remotion_projects/my-video --template=helloworld
```

## 🏗️ Workflows

### 1. Scouting Composition Schemas
Before rendering, you must understand what data the video needs.
1.  Locate `src/Root.tsx` or `src/compositions/`.
2.  Look for `z.object` schemas used in `<Composition schema={...} />`.
3.  **Crucial**: These schemas define the structure of the JSON props you must generate.

### 2. Rendering Videos (The Hybrid Approach)

Use the provided helper script: `.claude/skills/video-remotion/scripts/remotion_wrapper.py`.

#### Option A: Local Rendering (Development/Preview)
Best for quick checks, debugging, or when offline.

1.  **Generate Props**: Create a JSON file (e.g., `props.json`) matching the composition's schema.
2.  **Run Wrapper**:
    ```bash
    python .claude/skills/video-remotion/scripts/remotion_wrapper.py \
      --mode local \
      --project-dir /path/to/remotion-project \
      --composition MyCompId \
      --props props.json \
      --output out/video.mp4
    ```

#### Option B: Lambda Rendering (Production)
Best for long videos, final outputs, and speed. Requires AWS Setup.

1.  **Ensure Policies**: User needs `remotion-lambda-user` and `remotion-lambda-role`.
2.  **Deploy (Once)**:
    ```bash
    npx remotion lambda sites create src/index.ts
    npx remotion lambda functions deploy
    ```
    *Capture the Serve URL and Function Name.*
3.  **Run Wrapper**:
    ```bash
    # Ensure env vars are set: REMOTION_APP_REGION, REMOTION_APP_SERVE_URL, REMOTION_APP_FUNCTION_NAME
    python .claude/skills/video-remotion/scripts/remotion_wrapper.py \
      --mode lambda \
      --project-dir /path/to/remotion-project \
      --composition MyCompId \
      --props props.json
    ```

### 3. Creating New Templates
To create a NEW type of video:
1.  Create a React component file in `src/compositions/`.
2.  Define a Zod schema for its props.
3.  Register it in `src/Root.tsx`.
4.  **Pattern**: Use `AbsoluteFill` for layout, `Sequence` for timing, and `spring`/`interpolate` for motion.

## 🧠 Best Practices

- **Props as Files**: Always write props to a temporary JSON file and pass the path. Passing complex JSON strings in CLI arguments is fragile.
- **Assets**:
    - **Local**: Use `staticFile('image.png')` (put files in `public/`).
    - **Lambda**: Use public HTTP URLs (e.g., S3 buckets, Unsplash) or ensuring `public/` folder is correctly deployed with the site.
- **Duration**: If the video length depends on the text/content, use `calculateMetadata` in the composition to dynamically set `durationInFrames`.

## 🐛 Troubleshooting

- **"Command not found: remotion"**: Ensure you run commands inside the project directory where `node_modules` are installed, or use `npx remotion`.
- **Lambda Permissions**: 90% of Lambda failures are AWS IAM issues. Run `npx remotion lambda policies user` to fix.
- **Timeout**: If Local render hangs, try reducing `--concurrency`.
