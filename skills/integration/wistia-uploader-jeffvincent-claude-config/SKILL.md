---
name: wistia-uploader
description: Upload video files to Wistia projects using the Data API. Use when user wants to upload videos to their Wistia account for hosting, transcription, or sharing.
version: 1.0.0
dependencies:
  - node >= 18
  - form-data
  - axios
  - dotenv
allowed-tools: [Bash, Read]
---

# Wistia Video Uploader

## Overview
This Skill uploads video files to Wistia using the Wistia Data API. It handles authentication, file upload, and returns the hosted video URL with transcription capabilities. Wistia automatically generates transcripts for uploaded videos.

## When to Apply
Use this Skill when:
- User wants to upload a video file to their Wistia account
- User asks to "upload this to Wistia"
- User needs to host a video for transcription or sharing
- User mentions uploading interview recordings, demos, or other videos to Wistia
- User wants to organize videos into specific Wistia projects

Do NOT use this Skill for:
- Uploading to other video platforms (YouTube, Vimeo, etc.)
- Downloading videos from Wistia
- Editing or processing videos before upload
- Managing Wistia projects (only uploads to existing projects)

## Inputs
1. **Video file path** (required) - Absolute path to the video file (mp4, mov, avi, etc.)
2. **Project ID** (optional) - Wistia project ID to upload to (if not provided, uploads to account root)
3. **Video name** (optional) - Display name for the video in Wistia (defaults to filename)
4. **Video description** (optional) - Description text for the video

## Outputs
- **Wistia video URL** - Direct link to view the video
- **Video ID** (hashed_id) - Unique identifier for the video
- **Transcript URL** - Link to access the auto-generated transcript
- **Upload status** - Success/failure with error details if applicable

## Setup Instructions

### First Time Setup
Before using this Skill, you need to configure your Wistia API credentials:

1. **Get your Wistia API Token**:
   - Log in to your Wistia account
   - Go to Account Settings → API Access
   - Generate a new API token or copy existing one

2. **Configure the Skill**:
   - Copy `.env.example` to `.env` in the skill directory
   - Add your Wistia API token to the `.env` file:
     ```
     WISTIA_API_TOKEN=your_api_token_here
     ```

3. **Install dependencies**:
   ```bash
   cd ~/.claude/skills/wistia-uploader
   npm install
   ```

4. **Find your Project ID** (optional):
   - Log in to Wistia
   - Navigate to the project you want to upload to
   - The project ID is in the URL: `https://yourname.wistia.com/projects/{project_id}`
   - Or use the Wistia API to list projects: `curl -u api:{token} https://api.wistia.com/v1/projects.json`

## Instructions for Claude

### Step 1: Validate Setup
- Check that `.env` file exists with `WISTIA_API_TOKEN`
- If not configured, provide setup instructions to the user
- Verify the video file path exists and is accessible
- Check file extension is a supported video format (.mp4, .mov, .avi, .mkv, .webm)

### Step 2: Gather Upload Parameters
Ask the user for any missing information:
- **Video file path**: If not provided, ask "What is the path to the video file?"
- **Project ID** (optional): "Do you want to upload to a specific Wistia project? If so, provide the project ID, otherwise I'll upload to your account root."
- **Video name** (optional): "What should I name this video in Wistia? (Press Enter to use the filename)"
- **Description** (optional): "Would you like to add a description for this video?"

### Step 3: Execute Upload
Run the upload script:
```bash
cd ~/.claude/skills/wistia-uploader
node upload.js --file="/path/to/video.mp4" [--project=project_id] [--name="Video Name"] [--description="Description text"]
```

Parameters:
- `--file` (required): Absolute path to video file
- `--project` (optional): Wistia project ID
- `--name` (optional): Display name for the video
- `--description` (optional): Video description

### Step 4: Parse and Report Results
The script outputs JSON with:
```json
{
  "success": true,
  "video_id": "abc123xyz",
  "name": "Video Name",
  "url": "https://yourname.wistia.com/medias/abc123xyz",
  "thumbnail_url": "https://...",
  "duration": 120.5,
  "transcript_url": "https://yourname.wistia.com/medias/abc123xyz/captions"
}
```

Report to the user:
- Video uploaded successfully
- Video URL (for viewing)
- Video ID (for reference)
- Transcript URL (Wistia auto-generates transcripts)
- Note: "Wistia will automatically generate a transcript for this video. It may take a few minutes to process."

### Step 5: Handle Errors
If upload fails, check common issues:
- **401 Unauthorized**: API token is invalid or missing
- **404 Not Found**: Project ID doesn't exist
- **413 Payload Too Large**: File exceeds Wistia's size limit
- **Unsupported format**: File type not supported by Wistia

Provide specific error message and guidance to user.

### Step 6: Next Steps
After successful upload, suggest:
- "The video is now hosted on Wistia and processing. Would you like me to download the transcript once it's ready?"
- "Would you like to upload any other videos to this project?"
- If this is a customer interview, suggest: "Would you like me to analyze the transcript once Wistia generates it?"

## Examples

### Example 1: Upload with Default Settings
**User says:** "Upload this video to Wistia: ~/Downloads/customer-interview.mp4"

**Claude does:**
1. Checks `.env` for API token
2. Validates file exists
3. Asks: "Do you want to upload to a specific Wistia project? (Provide project ID or press Enter for account root)"
4. User: "Press Enter"
5. Runs: `node upload.js --file="~/Downloads/customer-interview.mp4"`
6. Reports results:
   ```
   Video uploaded successfully to Wistia!

   📹 Video: customer-interview.mp4
   🔗 URL: https://yourname.wistia.com/medias/abc123xyz
   🆔 Video ID: abc123xyz
   📝 Transcript: https://yourname.wistia.com/medias/abc123xyz/captions

   Note: Wistia is generating a transcript automatically. It should be ready in a few minutes.
   ```

### Example 2: Upload to Specific Project with Custom Name
**User says:** "Upload ~/Downloads/demo.mp4 to Wistia project xyz789 and name it 'Q4 Product Demo'"

**Claude does:**
1. Validates setup and file
2. Runs: `node upload.js --file="~/Downloads/demo.mp4" --project="xyz789" --name="Q4 Product Demo"`
3. Reports success with URL and transcript link

### Example 3: First Time Use (Not Configured)
**User says:** "Upload this video to Wistia"

**Claude checks** `.env` file and finds it missing.

**Claude responds:**
```
I need to configure your Wistia API credentials first. Here's how:

1. Get your Wistia API token:
   - Log in to your Wistia account
   - Go to Account Settings → API Access
   - Generate a new API token

2. Once you have the token, I'll create a .env file for you.

Please provide your Wistia API token and I'll set this up.
```

### Example 4: Upload and Analyze Workflow
**User says:** "Upload this interview to Wistia and then analyze the transcript"

**Claude does:**
1. Uploads video to Wistia
2. Reports upload success
3. Says: "The video is uploaded and Wistia is generating the transcript. This typically takes 1-2 minutes per minute of video."
4. Suggests: "Once the transcript is ready, I can download it and analyze it using the video-transcript-analyzer skill. Would you like me to wait a few minutes and then fetch the transcript?"

## Related Skills (Workflow Chain)

This skill is part of the **video processing workflow**:

```
┌─────────────────────┐
│   wistia-uploader   │  ← YOU ARE HERE
│   (upload video)    │
└──────────┬──────────┘
           │ transcript ready
           ▼
┌─────────────────────────────┐
│  video-transcript-analyzer  │  → Analyze transcript, extract themes
└──────────┬──────────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌──────────┐ ┌───────────────────────────┐
│  video-  │ │ interview-synthesis-      │
│  clipper │ │ updater                   │
│          │ │ (update synthesis docs)   │
└──────────┘ └───────────────────────────┘
```

**Next steps after upload:**
- Use `video-transcript-analyzer` to analyze the transcript once ready
- Use `video-clipper` to create clips from timestamps

## Testing Checklist
- [ ] `.env` file exists with valid `WISTIA_API_TOKEN`
- [ ] Can upload video file successfully
- [ ] Returns valid Wistia video URL
- [ ] Returns video ID (hashed_id)
- [ ] Provides transcript URL
- [ ] Handles missing file path gracefully
- [ ] Handles invalid API token with clear error
- [ ] Handles non-existent project ID with clear error
- [ ] Supports common video formats (mp4, mov, avi)
- [ ] Can specify custom video name
- [ ] Can specify custom description
- [ ] Can upload to specific project ID
- [ ] Provides helpful next steps after successful upload

## Security and Privacy
- **API Token**: Never log or display the API token in output
- **Secure Storage**: API token stored in `.env` file (gitignored)
- **Customer Data**: Video files may contain sensitive customer information
  - Warn user if uploading to shared/public Wistia projects
  - Recommend using private projects for customer interviews
- **File Paths**: Validate file paths to prevent directory traversal
- **Error Messages**: Don't expose full file paths in error messages to user
- **Cleanup**: Consider asking user if they want to delete local file after successful upload

## Wistia API Reference
- Upload endpoint: `https://upload.wistia.com/`
- Authentication: HTTP Basic Auth with API token as password
- Supported formats: mp4, mov, avi, wmv, flv, mkv, webm, ogv, mpg, mpeg
- Size limit: Varies by account (typically up to 8GB)
- Transcription: Automatic for all uploaded videos
- Documentation: https://wistia.com/support/developers/upload-api
