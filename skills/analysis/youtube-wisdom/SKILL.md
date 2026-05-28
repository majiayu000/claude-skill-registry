---
name: youtube-wisdom
description: Extract wisdom, insights, and actionable takeaways from YouTube videos. Use when asked to analyse, summarise, or extract key learnings from YouTube content. Downloads video transcripts, performs analysis including summarisation, extracts key insights, notable quotes, structured summaries, and actionable takeaways.
---

# YouTube Wisdom Extraction

## Overview

Extract meaningful insights, key learnings, and actionable wisdom from YouTube videos. This skill handles the complete workflow: downloading transcripts using yt-dlp (no video files), parsing subtitle data, performing comprehensive analysis, and saving results to organised markdown files.

## When to Use This Skill

This skill is useful when users request:
- Analysis or summary of YouTube video content
- Extraction of key insights or learnings from videos
- Identification of notable quotes or important statements
- Structured breakdown of video content
- Actionable takeaways from educational or informational videos

## Workflow

### Step 1: Download Transcript

Execute the download script to fetch only the transcript (no video file):

```bash
bash ~/.claude/skills/youtube-wisdom/scripts/download_video.sh <youtube-url>
```

The script will:
- Extract the video ID from the URL
- Create directory structure: `~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Wisdom/<video-id>/`
- Download English subtitles or auto-generated transcripts (no video file)
- Convert subtitle JSON3 format to clean text files
- Save transcript to the video ID directory

**Note:** The script uses Firefox cookies to handle age-restricted or login-required videos.

### Step 2: Locate and Read Transcript

The script outputs the location of the transcript. Read the transcript file from the video ID directory:

```bash
# The transcript will be at:
~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Wisdom/<video-id>/<video-title> - transcript.txt
```

Read the transcript file to analyse content. Transcripts are cleaned and formatted as continuous text with minimal whitespace.

**Note:** The download script uses `--restrict-filenames` to sanitise special characters (brackets, quotes, etc.) in filenames for safer handling.

#### Step 2.1: Rename the directory

Rename the directory to use today's date and concise description instead of the video ID for easier identification on the filesystem.

- Keep the description used for the file name as short and relevant as possible (1-3 words or up 6 words if they're short).
- Avoid spaces, special characters, or punctuation in the file name.
- Take the video content as well as the title into consideration.

E.g:

- Example video:
  - Title: "My Interview With Demis Hassabis, CEO of DeepMind. We Talk AI, AGI, and the Future"
  - Content: The video is an interview, but really mostly focuses on his career and views.
- Example file name: "2025-12-05-Demis-Hassabis-Interview.md"

```bash
DATE=$(date +%Y-%m-%d)
mv ~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Wisdom/<video-id>/ "~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Wisdom/${DATE}-<concise-description>/"
```

### Step 3: Analyse and Extract Wisdom

IMPORTANT: One of your goals is to avoid signal dilution, context collapse, quality degradation and degraded reasoning for future understanding of the content by ensuring you keep the signal to noise ratio high and that domain insights are preserved while not introducing unnecessary filler or fluff in documentation.

Perform comprehensive analysis on the transcript, extracting:

#### 1. Key Insights & Takeaways
- Identify the main ideas, core concepts, and central arguments
- Extract fundamental learnings and important revelations
- Highlight expert advice, best practices, or recommendations
- Note any surprising or counterintuitive information

#### 2. Notable Quotes
- Extract memorable, impactful, or particularly well-articulated statements
- Include context for each quote when relevant
- Focus on quotes that encapsulate key ideas or provide unique perspectives
- Preserve the original wording exactly as spoken, except correct American spellings to Australian English

#### 3. Structured Summary
- Create hierarchical organisation of content
- Break down into logical sections or themes
- Provide clear section headings that reflect content structure
- Include high-level overview followed by detailed breakdowns
- Note any important examples, case studies, or demonstrations

#### 4. Actionable Takeaways
- List specific, concrete actions viewers can implement
- Frame as clear, executable steps
- Prioritise practical advice over theoretical concepts
- Include any tools, resources, or techniques mentioned
- Distinguish between immediate actions and longer-term strategies

### Step 4: Write Analysis to Markdown File

Write the complete analysis to a markdown file in the video's directory:

**File location:** `~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Wisdom/<date>-<description>/<title> - analysis.md`

Format the analysis using this structure:

```markdown
# Video Analysis: [Video Title]

**Video URL:** [YouTube URL]
**Analysis Date:** [Current date in YYYY-MM-DD]

## Summary
[Brief 2 sentence overview of the video's main topic and purpose]

### Simplified Explanation
[Explain It Like I'm 10: A simple 1-2 sentence explanation of the core concept in a way a 10-year-old could understand]

### Key Takeaways
- [Concise takeaway 1]
- [Concise takeaway 2]
- [Concise takeaway 3]

## Key Insights
- [Insight 1]
  - [Supporting detail]
- [Insight 2]
  - [Supporting detail]
- [Insight 3]
  - [Supporting detail]
- etc..

## Notable Quotes (Only add this if there are notable quotes / statements)
> "[Quote 1]"

Context: [Brief context if needed]

> "[Quote 2]"

Context: [Brief context if needed]

## Structured Breakdown
### [Section 1 Title]
[Content summary]

### [Section 2 Title]
[Content summary]

## Actionable Takeaways
1. [Specific action item 1]
2. [Specific action item 2]
3. [Specific action item 3]

## Additional Resources
[Any tools, links, or references mentioned in the video]

_Wisdom Extraction Skill Generated: [Current date in YYYY-MM-DD]_
```

After writing the analysis file, inform the user of the location:
- Analysis location: `~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Wisdom/<date>-<description>/<title> - analysis.md`

## Step 5: Critical Self-Review

Conduct a critical self-review of YOUR summarisation and analysis.

Create tasks to track the following (mechanical checks first, then content quality):
- [ ] No American English spelling - check and fix (e.g. judgment→judgement, practicing→practising, organize→organise)
- [ ] No em-dashes, smart quotes, or non-standard typography
- [ ] Proper markdown formatting
- [ ] Accuracy & faithfulness to the original content
- [ ] Completeness
- [ ] Concise, clear content with no fluff, marketing speak, filler, or padding (ensure the content has a high signal to noise ratio)
- [ ] Logical organisation & structure

Re-read the analysis file, verify each item, fix any issues found, then mark tasks completed.

## Step 6: Send Completion Notification

Use `scripts/send_notification.sh` to send a desktop notification to the user that the analysis is complete and provide the file location:

```bash
TITLE="Wisdom Extracted" MESSAGE="<short 3-5 word description of the video>" PLAY_SOUND=true DIR="/path/to/extracted/wisdom/" bash ~/.claude/skills/youtube-wisdom/scripts/send_notification.sh
```

Then stop unless further instructions are given.

## Additional Capabilities

### Multiple Video Analysis
When analysing multiple videos:
- Process each video sequentially using the workflow above
- Each video gets its own directory by video ID
- Create comparative analysis highlighting common themes or contrasting viewpoints
- Synthesise insights across multiple sources in a separate summary file
- Notify once only at the end of the entire batch process

### Time-Stamped Analysis
If timestamps are needed:
- Note that basic transcripts don't preserve timestamps
- Can reference general flow (beginning, middle, end) of content
- For precise timestamps, may need to cross-reference with the actual video

### Topic-Specific Focus
When user requests focused analysis on specific topics:
- Search transcript for relevant keywords and themes
- Extract only content related to specified topics
- Provide concentrated analysis on areas of interest

## Tips

- Don't add new lines between items in a list
- Avoid marketing speak or fluff
- Always use Australian English spelling
- Do not use em-dashes or smart quotes
- Only use **bold** where emphasis is truly needed
- Ensure clarity and conciseness in summaries and takeaways
- Consider if the text you're adding actually adds value to the analysis, don't add filler or padding
- If the video mentions a specific tool, resource or website, task a sub-agent to look it up and provide a brief summary, then include it in the Additional Resources section

## Resources

### scripts/
- `download_video.sh`: Bash script that downloads YouTube transcripts (no video files) using yt-dlp with optimised settings. Organises files by video ID in `~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Wisdom/<video-id>/`.
