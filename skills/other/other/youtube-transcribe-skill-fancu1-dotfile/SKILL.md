---
name: youtube-transcribe-skill
description: 'Extract subtitles/transcripts from a YouTube video URL and save as a local file. Use when you need to extract subtitles from a YouTube video.'
---

# YouTube Transcript Extraction

Extract subtitles/transcripts from a YouTube video URL and save them as a local file.

Input YouTube URL: $ARGUMENTS

## Step 1: Verify URL and Get Video Information

1. **Verify URL Format**: Confirm the input is a valid YouTube URL (supports `youtube.com/watch?v=` or `youtu.be/` formats).

2. **Get Video Information**:
   - If `yt-dlp` is available, prefer `yt-dlp --get-title "[VIDEO_URL]"`.
   - If using browser automation, extract the title from the page (via snapshot or `document.title`) for file naming.

## Step 2: CLI Quick Extraction (Priority Attempt)

Use command-line tools to quickly extract subtitles.

1. **Check Tool Availability**:
   Execute `which yt-dlp`.

   - If `yt-dlp` is **found**, proceed to subtitle download.
   - If `yt-dlp` is **NOT found**, skip immediately to **Step 3**.

2. **Execute Subtitle Download** (Only if `yt-dlp` is found):

   - **Tip**: Always add `--cookies-from-browser` to avoid sign-in restrictions. Default to `chrome`.
   - **Retry Logic**: If `yt-dlp` fails with a browser error (e.g., "Could not open Chrome"), ask the user to specify their available browser (e.g., `firefox`, `safari`, `edge`) and retry.

   ```bash
   # Get the title first (try chrome first)
   yt-dlp --cookies-from-browser=chrome --get-title "[VIDEO_URL]"

   # Download subtitles
   yt-dlp --cookies-from-browser=chrome --write-auto-sub --write-sub --sub-lang zh-Hans,zh-Hant,en --skip-download --output "<Video Title>.%(ext)s" "[VIDEO_URL]"
   ```

3. **Verify Results**:
   - Check the command exit code.
   - **Exit code 0 (Success)**: Subtitles have been saved locally, task complete.
   - **Exit code non-0 (Failure)**:
     - If error is related to browser/cookies, ask user for correct browser and retry Step 2.
     - If other errors (e.g., video unavailable), proceed to **Step 3**.

## Step 3: Browser Automation (Fallback)

When the CLI method fails or `yt-dlp` is missing, use browser UI automation to extract subtitles.

1. **Check Tool Availability**:

   - Check if `chrome-devtools-mcp` tools (specifically `mcp__chrome__new_page`) are available.
   - **CRITICAL CHECK**: If `chrome-devtools-mcp` is **NOT** available AND `yt-dlp` was **NOT** found in Step 2:
     - **STOP** execution.
     - **Notify the User**: "Unable to proceed. Please either install `yt-dlp` (for fast CLI extraction) OR configure `chrome-devtools-mcp` (for browser automation)."

2. **Initialize Browser Session** (If tools are available):

   Call `mcp__chrome__new_page` to open the video URL.

### 3.2 Analyze Page State

Call `mcp__chrome__take_snapshot` to read the page accessibility tree.

### 3.3 Expand Video Description

_Reason: The "Show transcript" button is usually hidden within the collapsed description area._

1. Search the snapshot for a button labeled **"...more"**, **"...更多"**, or **"Show more"** (usually located in the description block below the video title).
2. Call `mcp__chrome__click` to click that button.

### 3.4 Open Transcript Panel

1. Call `mcp__chrome__take_snapshot` to get the updated UI snapshot.
2. Search for a button labeled **"Show transcript"**, **"显示转录稿"**, or **"内容转文字"**.
3. Call `mcp__chrome__click` to click that button.

### 3.5 Extract Content via DOM

_Reason: Directly reading the accessibility tree for long lists is slow and consumes many tokens; DOM injection is more efficient._

Call `mcp__chrome__evaluate_script` to execute the following JavaScript:

```javascript
() => {
  // Select all transcript segment containers
  const segments = document.querySelectorAll("ytd-transcript-segment-renderer");
  if (!segments.length) return "BUFFERING"; // Retry if empty

  // Iterate and format as "timestamp text"
  return Array.from(segments)
    .map((seg) => {
      const time = seg.querySelector(".segment-timestamp")?.innerText.trim();
      const text = seg.querySelector(".segment-text")?.innerText.trim();
      return `${time} ${text}`;
    })
    .join("\n");
};
```

If it returns "BUFFERING", wait a few seconds and retry.

### 3.6 Save and Cleanup

1. Use the Write tool to save the extracted text as a local file (e.g., `<Video Title>.txt`).
2. Call `mcp__chrome__close_page` to release resources.

## Output Requirements

- Save the subtitle file to the current working directory.
- Filename format: `<Video Title>.txt`
- File content format: Each line should be `Timestamp Subtitle Text`.
- Report upon completion: File path, subtitle language, total number of lines.
