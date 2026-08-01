---
name: stitch-mcp-upload-design-md
description: Uploads a DESIGN.md file to a Stitch project as the first half of turning it into a Stitch Design System. Always paired with stitch-mcp-create-design-system-from-design-md, which must be called immediately after.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
---

# Stitch MCP — Upload DESIGN.md

Uploads a DESIGN.md file into a Stitch project. This is step one of a two-step pair: the upload creates a screen instance holding the design doc, and `create_design_system_from_design_md` then turns that instance into a real Design System.

**On its own, this tool does nothing useful.** Uploading without the follow-up leaves an orphan screen instance and no design system. Always run both.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch"** in their request. Never trigger Stitch operations silently during regular conversation.

## When to use

- The user has a DESIGN.md and wants it applied as a Stitch Design System
- You've just produced a DESIGN.md with `stitch-design-md` and want it driving generation
- The user says "use my design doc in Stitch", "make a design system from DESIGN.md"

## Step 1: Read and encode the file

The tool takes base64, not raw markdown. The decoded content **must be valid UTF-8** — uploads with invalid bytes are rejected outright.

```bash
# macOS (BSD base64 — no -w flag, and it does not wrap by default)
base64 -i DESIGN.md
```

```bash
# Linux (GNU base64 — -w 0 disables line wrapping)
base64 -w 0 DESIGN.md
```

> Google's tool description says `base64 -w 0`, which fails on macOS with `invalid option -- w`. Use `-i` there. Getting this wrong produces a confusing shell error rather than an API error, so check your platform first.

Wrapped base64 (with embedded newlines) is a common cause of rejected uploads. Both commands above emit a single unbroken line.

## Step 2: Call the MCP tool

```json
{
  "name": "upload_design_md",
  "arguments": {
    "projectId": "3780309359108792857",
    "designMdBase64": "IyBEZXNpZ24gU3lzdGVtCgpDb2xvcnM6IC4uLg=="
  }
}
```

`projectId` is **numeric only** — no `projects/` prefix. Passing the prefixed path here fails.

## Step 3: Capture the screen instance — CRITICAL

The upload creates a **screen instance**, and the next tool needs two identifiers from it. Fetch them with `get_project` (which does take the `projects/` prefix):

```json
{
  "name": "get_project",
  "arguments": { "name": "projects/3780309359108792857" }
}
```

From the returned `screenInstances`, take the newest entry and record both:

| Field | Example | Notes |
|-------|---------|-------|
| `id` | `a1b2c3d4e5f6` | The **screen instance** id |
| `sourceScreen` | `projects/3780.../screens/98b5...` | Full resource path |

**The trap:** `id` is the screen *instance* id, **not** the source screen id. They are different values and passing the source screen id as `id` fails. Google's own schema calls this out in bold, which is usually a sign it bites people.

## Step 4: Immediately call the follow-up

Hand both values straight to `stitch-mcp-create-design-system-from-design-md`. Don't stop between the two steps or report success to the user yet — there's no design system until the second call returns.

## ID format rules (critical — different tools need different formats)

| Tool | ID format required |
|------|-------------------|
| `upload_design_md` | Numeric only: `3780309359108792857` |
| `create_design_system_from_design_md` | Numeric only, plus the screen-instance pair |
| `get_project` | Full path: `projects/3780309359108792857` |

## Integration

- Produce the DESIGN.md first with `stitch-design-md`
- Always follow with `stitch-mcp-create-design-system-from-design-md`
- Once the design system exists, apply it with `stitch-mcp-apply-design-system` or pass its asset id to `generate_screen_from_text`
