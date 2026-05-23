---
name: youtube-comment-analysis
description: Use when user requests YouTube comments. Run standalone for comment analysis or sequential with youtube-to-markdown for cross-analysis with video summary.
allowed-tools:
  - Bash
  - Read
  - Write
  - Task
  - AskUserQuestion
  - Skill
---

# YouTube Comment Analysis

Execute all steps sequentially without asking for user approval. Use TodoWrite to track progress, update Todolist.

## Step 0: Check for video summary

Check if `<output_directory>/youtube - * ({video_id}).md` exists. If found, use it for context in later steps.

## Step 1: Extract comments

```bash
python3 ./extract_comments.py "<YOUTUBE_URL>" "<output_directory>"
```

Creates: youtube_{VIDEO_ID}_name.txt, youtube_{VIDEO_ID}_comments.md

## Step 2: Prefilter comments

```bash
python3 ./prefilter_comments.py "<output_directory>/${BASE_NAME}_comments.md" "<output_directory>/${BASE_NAME}_comments_prefiltered.md"
```

Creates: youtube_{VIDEO_ID}_comments_prefiltered.md

## Step 3: Extract Insightful Comments

task_tool:
- subagent_type: "general-purpose"
- model: "sonnet"
- prompt:
```
SUMMARY: "<output_directory>/youtube - * ({video_id}).md" if exists
INPUT: <output_directory>/${BASE_NAME}_comments_prefiltered.md
OUTPUT: <output_directory>/${BASE_NAME}_comment_insights.md

Detect video type from SUMMARY:
- TIPS: gear reviews, rankings, practical advice
- INTERVIEW: podcasts, conversations, Q&A
- EDUCATIONAL: concept explanations, analysis
- TUTORIAL: step-by-step instructions

Write to OUTPUT in format:

## Comment Insights ([2-7 word theme])

**Key Takeaway**: [One paragraph - ONLY if adds value beyond bullets]

[Include type-specific sections if found in comments:]

TUTORIAL:
- **Common Failures**: [what goes wrong, why, how to fix]
- **Success Patterns**: [what worked, time investment]

TIPS:
- **What Worked/Didn't**: [real-world validation]
- **Alternatives Mentioned**: [products, methods]

INTERVIEW:
- **Points of Agreement/Debate**: [where commenters align/clash]
- **Related Stories**: [personal experiences shared]

EDUCATIONAL:
- **Corrections/Extensions**: [where commenters add/fix content]
- **Debates**: [alternative viewpoints]

**[Additional themes as needed]**:
- [insight with **keyword highlights**]

Rules:
- Extract insights NOT already in summary
- Prioritize actionable over opinions
- Include commenter attribution only if expertise matters

ACTION REQUIRED: Use the Write tool NOW to save output to OUTPUT file.
```

## Step 4: Review and tighten comment insights

task_tool:
- subagent_type: "general-purpose"
- model: "sonnet"
- prompt:
```
SUMMARY: "<output_directory>/youtube - * ({video_id}).md" if exists
INPUT: <output_directory>/${BASE_NAME}_comment_insights.md
OUTPUT: <output_directory>/${BASE_NAME}_comment_insights_tight.md

You are an adversarial copy editor. Your job is to ruthlessly cut fluff and enforce quality standards.

Rules:
- Remove insights already in summary file
- Cut filler, prefer lists over prose
- Keep only exceptional value-add insights
- Preserve type-specific sections (Common Failures, What Worked/Didn't, etc.)

ACTION REQUIRED: Use the Write tool NOW to save output to OUTPUT file.
```

## Step 5: Finalize

```bash
python3 ./finalize_comments.py "${BASE_NAME}" "<output_directory>"
```

Output: `youtube - {title} - comments ({video_id}).md`

Use `--debug` flag to keep intermediate work files for inspection.
