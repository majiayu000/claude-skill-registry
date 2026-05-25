---
name: stitch-mcp-get-screen
description: Retrieves full details of a specific Stitch screen — HTML download URL, screenshot URL, dimensions. This is the final step in design retrieval before code conversion.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
  - "Write"
---

# Stitch MCP — Get Screen

Retrieves the full output of a Stitch-generated screen: the HTML source code URL and the screenshot image URL. This is the gateway between Stitch design and framework conversion.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

**If you already have both `projectId` AND `screenId`, call this directly** — do not call `get_project` first.

## When to use

- After `list_screens` has returned a screenId
- User provides a Stitch screen URL and wants to convert it to code
- Retrieving assets for any conversion skill: Next.js, Svelte, HTML, React Native, or SwiftUI

## Step 1: Parse IDs from context

The user may provide the screen reference in different formats:

| Input format | → projectId | → screenId |
|---|---|---|
| `projects/123/screens/456` | `123` | `456` |
| `https://stitch.withgoogle.com/projects/123?node-id=456` | `123` | `456` |
| Separate numeric IDs already known | Use as-is | Use as-is |

## Step 2: Call the MCP tool

**Important: Both IDs must be numeric — no `projects/` or `screens/` prefix.**

```json
{
  "name": "get_screen",
  "arguments": {
    "projectId": "3780309359108792857",
    "screenId": "88805abc123def456"
  }
}
```

```
✅ projectId: "3780309359108792857"
❌ projectId: "projects/3780309359108792857"

✅ screenId: "88805abc123def456"
❌ screenId: "screens/88805abc123def456"
```

## Output schema

```json
{
  "name": "projects/3780309359108792857/screens/88805abc123def456",
  "htmlCode": {
    "downloadUrl": "https://storage.googleapis.com/stitch-output/..."
  },
  "screenshot": {
    "downloadUrl": "https://storage.googleapis.com/stitch-screenshots/..."
  },
  "figmaExport": {
    "downloadUrl": "https://storage.googleapis.com/stitch-figma/..."
  },
  "width": 390,
  "height": 844,
  "deviceType": "MOBILE"
}
```

## Step 3: Download the HTML reliably

AI fetch tools frequently fail on Google Cloud Storage URLs. Use the bash script:

```bash
bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "temp/source.html"
```

Always quote the URL to handle special characters.

## Step 4: Determine framework and route to conversion

After retrieving the screen, check what the user wants to do with it.

Check the `deviceType` in the response first — it shapes which options to suggest:

| `deviceType` | Sensible defaults to suggest |
|---|---|
| `DESKTOP` | Next.js, Svelte, HTML |
| `MOBILE` | Next.js (PWA), Svelte, HTML, React Native, SwiftUI |
| `AGNOSTIC` | Any |

Then route based on user intent:

| User intent | → Load skill |
|---|---|
| "Convert to Next.js", "React app", "App Router" | `stitch-nextjs-components` |
| "Convert to Svelte", "SvelteKit" | `stitch-svelte-components` |
| "Convert to HTML", "PWA", "Capacitor", "Ionic", "web app" | `stitch-html-components` |
| "React Native", "Expo", "iOS and Android", "cross-platform" | `stitch-react-native-components` |
| "SwiftUI", "Xcode", "native iOS", "iOS only" | `stitch-swiftui-components` |
| "Extract design system", "get the colors/fonts" | `stitch-design-system` |
| "Just show me the screenshot" | Present `screenshot.downloadUrl` |
| No framework mentioned, desktop design | Ask: Next.js, Svelte, or HTML? |
| No framework mentioned, mobile design | Ask: React Native, SwiftUI, or HTML (Capacitor)? |

## References

- `scripts/fetch-stitch.sh` — Reliable GCS HTML downloader
