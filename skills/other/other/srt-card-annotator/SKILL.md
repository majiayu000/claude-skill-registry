---
name: SRT Card Annotator
description: This skill should be used when the user asks to "add reference cards to srt", "annotate srt with cards", "insert cards into subtitles", "generate srt with card annotations", "add 字卡 to srt", or needs to add contextual reference cards below subtitle text blocks in SRT files.
version: 0.1.0
---

# SRT Card Annotator

This skill provides an AI-driven workflow for analyzing SRT subtitle files and adding contextual reference cards below subtitle text blocks. Cards are intelligently selected based on content context and must not modify original timestamps or subtitle text.

## Purpose

Enhance SRT subtitle files with reference cards that:
- Highlight key points, warnings, tips, and structured information
- Are intelligently placed based on content analysis
- Follow strict formatting rules: `[字卡](word:xxx / type:yyy)`
- Maintain original subtitle timing and text integrity
- Use contextually appropriate card types from predefined categories

## When to Use This Skill

Use this skill when:
- Adding educational annotations to video subtitles
- Highlighting key concepts in transcribed content
- Creating enhanced subtitles with contextual tips and warnings
- Processing Chinese language educational or instructional videos

## Card Structure

Each card follows this format:
```
[字卡](word:xxx / type:yyy)
```

Where:
- **word**: Key phrase extracted from the subtitle segment (10-16 characters max)
- **type**: One of four predefined types (see Card Types section)

## Card Types

Reference `references/card-types.yaml` for complete definitions. Summary:

| Type | Usage | Context |
|------|-------|---------|
| **金色重點** | Core conclusions, critical insights | Most important takeaway |
| **白色提醒** | Suggestions, reminders, notes | Helpful tips and advice |
| **紅色警告** | Risks, errors, pitfalls | Dangers and common mistakes |
| **藍色列點** | Lists, steps, structured info | Sequential or parallel items |

## Card Selection Principles

1. **Frequency**: Minimum 2 cards per 10 subtitle segments
2. **Length**: Extract 10-16 character key phrases from segment content
3. **Context-aware**: Choose type based on semantic meaning:
   - Risk/error/pitfall → 紅色警告
   - Suggestion/reminder/note → 白色提醒
   - List/steps/sequence → 藍色列點
   - Core conclusion/key insight → 金色重點
4. **Precision**: Only annotate truly important information
5. **Integrity**: Never modify original timestamps or subtitle text

## Core Workflow

### 1. Load and Parse SRT File

Read the input SRT file and parse into segments:
- Extract subtitle number
- Extract timestamp (start → end)
- Extract subtitle text
- Preserve exact formatting

### 2. Analyze Content Semantically

For each subtitle segment, analyze:
- Semantic meaning and context
- Presence of key concepts, warnings, or steps
- Relationship to surrounding segments
- Importance level

### 3. Identify Card Insertion Points

Determine where to insert cards:
- Evaluate each segment for card-worthiness
- Ensure minimum 2 cards per 10 segments
- Prioritize segments with:
  - Critical information
  - Warnings or risks
  - Key conclusions
  - Important steps or lists

### 4. Extract Key Phrases

For selected segments:
- Extract the most important 10-16 character phrase
- Ensure phrase is directly from segment content
- Maintain semantic completeness
- Avoid truncating mid-concept

### 5. Classify Card Type

For each extracted phrase, determine type:
- **紅色警告**: Contains risk indicators (錯誤、風險、避免、不要、危險)
- **白色提醒**: Contains suggestions (建議、提醒、注意、可以、記得)
- **藍色列點**: Contains list markers (第一、步驟、包括、分為、有)
- **金色重點**: Contains conclusions (重點、關鍵、核心、總結、最重要)

### 6. Insert Cards

Add card lines below subtitle text:
```
1
00:00:00,000 --> 00:00:05,000
這個操作有風險，請小心處理
[字卡](word:操作有風險請小心 / type:紅色警告)

2
00:00:05,000 --> 00:00:10,000
建議先備份資料再進行
[字卡](word:建議先備份資料 / type:白色提醒)
```

### 7. Generate Output File

Save the annotated SRT as `reference-cards.srt`:
- Maintain all original formatting
- Preserve subtitle numbering
- Keep exact timestamps
- Add card lines only in text blocks

## Implementation Guidelines

### Reading Card Type Definitions

Before processing, read `references/card-types.yaml` to understand:
- Available card types
- Usage contexts for each type
- Selection principles
- Examples of appropriate usage

### Processing Strategy

1. **First Pass**: Read entire SRT to understand content flow
2. **Second Pass**: Identify high-value segments for annotation
3. **Third Pass**: Extract phrases and classify types
4. **Final Pass**: Insert cards and validate formatting

### Quality Checks

Before generating output:
- Verify minimum card frequency (2 per 10 segments)
- Confirm all cards use valid types from `card-types.yaml`
- Ensure all extracted phrases are 10-16 characters
- Validate no modifications to original content
- Check output filename is `reference-cards.srt`

## Example Output

Input SRT:
```
1
00:00:00,000 --> 00:00:03,500
今天要教大家如何避免常見的錯誤

2
00:00:03,500 --> 00:00:07,000
第一步是檢查系統設定
```

Output SRT (`reference-cards.srt`):
```
1
00:00:00,000 --> 00:00:03,500
今天要教大家如何避免常見的錯誤
[字卡](word:避免常見的錯誤 / type:紅色警告)

2
00:00:03,500 --> 00:00:07,000
第一步是檢查系統設定
[字卡](word:第一步檢查系統設定 / type:藍色列點)
```

## Important Constraints

### Must NOT:
- Modify original subtitle text
- Change timestamps
- Alter subtitle numbering
- Use Python scripts or automation (AI analysis required)
- Create cards longer than 16 characters
- Use card types not defined in `card-types.yaml`

### Must DO:
- Use AI to analyze content semantically
- Extract phrases directly from subtitle content
- Choose contextually appropriate card types
- Maintain minimum card frequency
- Output to `reference-cards.srt`
- Preserve all original SRT formatting

## Additional Resources

### Reference Files
- **`references/card-types.yaml`** - Complete card type definitions, usage contexts, and selection principles

## Workflow Summary

To annotate an SRT file with reference cards:

1. Read `references/card-types.yaml` to understand card types
2. Load and parse the input SRT file
3. Analyze content to identify key segments
4. Extract 10-16 character phrases from selected segments
5. Classify each phrase with appropriate card type
6. Insert card lines below subtitle text (not modifying original content)
7. Save output as `reference-cards.srt`
8. Validate card frequency, formatting, and type validity

Focus on semantic understanding and contextual appropriateness when selecting card types. The goal is to enhance subtitles with meaningful, concise annotations that help viewers grasp key concepts, avoid pitfalls, and follow structured information.
