---
name: youtube-upload
description: Upload videos to YouTube via browser automation
allowed-tools:
  - mcp__claude-in-chrome__*
  - Read
  - Write
---

# YouTube Upload Skill

Upload videos to YouTube using browser automation.

## Prerequisites

- Chrome extension connected (`/chrome` command)
- Logged into YouTube/Google in the browser
- Video file ready in `output/` directory

## Upload Workflow

### Step 1: Navigate to YouTube Studio

```
1. Navigate to https://studio.youtube.com
2. Wait for page to load
3. Take screenshot to verify logged in
4. If not logged in, inform user to log in manually
```

### Step 2: Start Upload

```
1. Find and click the "Create" button (camera icon with +)
2. Select "Upload video" from dropdown
3. Wait for upload dialog to appear
```

### Step 3: Select Video File

```
1. Find the file input or drop zone
2. Use mcp__claude-in-chrome__upload_image with the video file path
   (Note: This tool works for any file, not just images)
3. Wait for upload to start
4. Monitor upload progress
```

### Step 4: Fill Video Details

```
1. Wait for "Details" step to appear

2. Title:
   - Find title input field
   - Enter video title (max 100 characters)

3. Description:
   - Find description textarea
   - Enter description (max 5000 characters)
   - Include links, hashtags, timestamps if needed

4. Thumbnail (optional):
   - Click "Upload thumbnail"
   - Select thumbnail image
   - Wait for upload

5. Playlists (optional):
   - Click "Add to playlist"
   - Select or create playlist

6. Tags (in "Show more"):
   - Click "Show more"
   - Find tags input
   - Enter comma-separated tags
```

### Step 5: Audience Settings

```
1. Scroll to "Audience" section
2. Select "Yes, it's made for kids" or "No, it's not made for kids"
3. For most content, select "No, it's not made for kids"
```

### Step 6: Visibility

```
1. Click "Next" to go through Video elements (skip or add end screens)
2. Click "Next" to go through Checks
3. Click "Next" to reach Visibility

4. Select visibility:
   - Public: Available to everyone
   - Unlisted: Only those with link
   - Private: Only you

5. Optional: Schedule for later
   - Select "Schedule"
   - Set date and time
```

### Step 7: Publish

```
1. Verify all details are correct
2. Take screenshot for confirmation
3. Ask user: "Ready to publish? [screenshot]"
4. If confirmed, click "Publish" or "Schedule"
5. Wait for confirmation
6. Extract and return the video URL
```

## Metadata Templates

### Standard Upload Metadata

```markdown
**Title**: {Clear, descriptive title} (max 100 chars)

**Description**:
{Hook sentence}

{Main content description}

{Timestamps if applicable}
0:00 - Intro
0:30 - Section 1
...

{Links}
🔗 Related links...

{Tags/Hashtags}
#tag1 #tag2 #tag3

**Tags**: tag1, tag2, tag3, tag4, tag5 (max 500 chars total)

**Visibility**: Public/Unlisted/Private/Scheduled
```

## Confirmation Flow

**IMPORTANT**: Always confirm before publishing.

```
1. Fill all details
2. Take screenshot of preview
3. Show user: "Video ready to publish:
   - Title: {title}
   - Visibility: {visibility}
   - Description preview: {first 100 chars}...

   Proceed with upload?"
4. Wait for explicit confirmation
5. Only then click Publish
6. Return video URL when complete
```

## Supported Formats

| Format | Recommended |
|--------|-------------|
| MP4 (H.264) | Yes - Best compatibility |
| MOV | Yes |
| AVI | Okay |
| WebM | Okay |
| MKV | Okay |

**Max file size**: 256GB or 12 hours (whichever is less)
**Recommended resolution**: 1920x1080 (1080p) or higher

## Error Handling

| Issue | Solution |
|-------|----------|
| Not logged in | Ask user to log in manually |
| Upload stuck | Check file format, refresh and retry |
| Processing taking long | Large files take time, wait or come back later |
| Copyright claim | May need to edit or dispute |
| Details not saving | Check for required fields |

## Best Practices

1. **Optimize before upload**: Compress to reasonable size
2. **Prepare metadata**: Have title, description, tags ready
3. **Custom thumbnail**: Increases click-through rate
4. **Add timestamps**: Helps viewers navigate
5. **Include CTA**: Subscribe, like, comment reminders
6. **SEO optimization**: Keywords in title and first 2 lines of description
