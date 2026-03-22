---
name: SRT Enhancer
description: This skill should be used when the user asks to "enhance srt subtitles", "optimize srt with original script", "fix srt typos from markdown", "compare srt with origin.md", "improve subtitle accuracy", "add spaces to srt", "優化 srt 逐字稿", "比對原稿修正字幕", or needs to refine SRT subtitle files by comparing them with an original markdown reference document.
version: 0.1.0
---

# SRT Enhancer

This skill provides an AI-driven workflow for enhancing SRT subtitle files by comparing them with an original reference document (`origin.md`). The enhancement process corrects typos, standardizes proper nouns, and adds proper spacing around English text and numbers while preserving the original timeline and structure.

## Purpose

Enhance SRT subtitle files by:
- Comparing subtitle content with reference markdown document (`origin.md`)
- Correcting typos and transcription errors
- Standardizing proper nouns and terminology
- Adding half-width spaces before and after English words and numbers
- Maintaining exact timestamps and SRT structure
- Only including content that appears in the SRT (not adding new content from markdown)

## When to Use This Skill

Use this skill when:
- Refining auto-generated subtitles with a reference script
- Correcting transcription errors in SRT files
- Standardizing terminology across subtitle files
- Improving subtitle formatting for Chinese content with English/numbers
- Ensuring consistency between spoken content and written reference

## Enhancement Principles

1. **Timeline Preservation**: Never modify timestamps or subtitle numbering
2. **Content Fidelity**: Only correct what exists in SRT; don't add content from markdown
3. **Reference Comparison**: Use `origin.md` as the source of truth for spelling and terminology
4. **Spacing Rules**: Add half-width spaces (` `) around English words and numbers in Chinese text
5. **AI-Driven**: Use semantic understanding to match content, not simple string matching

## Core Workflow

### 1. Locate Reference Document

Find `origin.md` in the same directory as the input SRT file:
- Check for `origin.md` in the SRT file's directory
- If not found, prompt user for the reference document location
- Read and parse the markdown content

### 2. Parse SRT File

Load and parse the input SRT file:
- Extract subtitle number
- Extract timestamp (start → end)
- Extract subtitle text
- Preserve exact formatting and structure

### 3. Build Reference Knowledge Base

Analyze `origin.md` to extract:
- Proper nouns and terminology
- Correct spellings and phrasings
- English words and technical terms
- Numbers and their contexts
- Common phrases and expressions

Reference `references/enhancement-rules.md` for detailed extraction strategies.

### 4. Match and Compare Content

For each subtitle segment:
- Identify corresponding content in `origin.md` using semantic matching
- Compare subtitle text with reference text
- Identify discrepancies:
  - Typos and misspellings
  - Incorrect proper nouns
  - Missing spaces around English/numbers
  - Terminology inconsistencies

### 5. Apply Corrections

For each identified issue:
- **Typos**: Replace with correct spelling from `origin.md`
- **Proper Nouns**: Standardize to reference document version
- **English/Numbers**: Add half-width space before and after
- **Terminology**: Use consistent terms from reference

### 6. Validate Enhancements

Before finalizing each correction:
- Ensure the content exists in the original SRT
- Verify no new content is added from markdown
- Confirm timestamps remain unchanged
- Check subtitle numbering is preserved
- Validate spacing follows rules (see Spacing Rules section)

### 7. Generate Output File

Save the enhanced SRT as `enhanced.srt`:
- Maintain all original timestamps
- Preserve subtitle numbering
- Keep exact SRT formatting
- Apply all validated corrections

## Spacing Rules

### Add Half-Width Spaces Around:

1. **English Words in Chinese Text**:
   - Before: `這是一個example範例`
   - After: `這是一個 example 範例`

2. **Numbers in Chinese Text**:
   - Before: `總共有3個步驟`
   - After: `總共有 3 個步驟`

3. **Mixed English and Numbers**:
   - Before: `使用Python3.9版本`
   - After: `使用 Python 3.9 版本`

### Do NOT Add Spaces:

1. **Within English phrases**: `machine learning` (keep as is)
2. **Within numbers**: `123,456` (keep as is)
3. **Between punctuation and text**: Keep original punctuation spacing
4. **When space already exists**: Don't add duplicate spaces

Reference `references/spacing-examples.md` for comprehensive examples.

## Implementation Guidelines

### Semantic Matching Strategy

Use AI to match SRT content with `origin.md`:
- Don't rely on exact string matching
- Understand context and meaning
- Account for transcription variations
- Match concepts, not just words
- Handle paraphrasing and reordering

### Correction Priority

Apply corrections in this order:
1. Critical typos affecting meaning
2. Proper nouns and terminology
3. Spacing around English/numbers
4. Minor spelling variations

### Quality Checks

Before generating output:
- Verify all timestamps are unchanged
- Confirm subtitle count matches original
- Validate no content added from markdown
- Check spacing rules applied consistently
- Ensure proper nouns are standardized
- Validate output filename is `enhanced.srt`

## Example Enhancement

**origin.md**:
```markdown
今天要介紹 Python 3.9 的新功能。首先是 match case 語句，這是一個強大的模式匹配工具。
```

**Input SRT**:
```
1
00:00:00,000 --> 00:00:05,000
今天要介紹Python3.9的新功能

2
00:00:05,000 --> 00:00:10,000
首先是match case語句這是一個強大的模式匹配工俱
```

**Output SRT (`enhanced.srt`)**:
```
1
00:00:00,000 --> 00:00:05,000
今天要介紹 Python 3.9 的新功能

2
00:00:05,000 --> 00:00:10,000
首先是 match case 語句,這是一個強大的模式匹配工具
```

**Changes Made**:
- Added spaces around `Python`, `3.9`, `match case`
- Corrected `工俱` → `工具` (typo fix from reference)
- Preserved all timestamps and numbering

## Important Constraints

### Must NOT:
- Modify timestamps or subtitle numbering
- Add content from `origin.md` that doesn't exist in SRT
- Use Python scripts or automation (AI analysis required)
- Change the meaning or intent of subtitles
- Remove existing content from SRT
- Alter SRT structure or formatting

### Must DO:
- Use AI to semantically match content
- Compare each subtitle with reference document
- Apply spacing rules consistently
- Correct typos based on reference
- Standardize proper nouns and terminology
- Output to `enhanced.srt`
- Preserve exact timestamps and structure

## Error Handling

### Missing origin.md:
- Check same directory as SRT file
- Prompt user for location
- Cannot proceed without reference document

### No Matching Content:
- If SRT content has no match in `origin.md`, leave unchanged
- Don't guess or invent corrections
- Apply spacing rules even without reference match

### Ambiguous Matches:
- Use context to determine best match
- Prefer conservative corrections
- When uncertain, preserve original text

## Additional Resources

### Reference Files
- **`references/enhancement-rules.md`** - Detailed rules for typo detection, proper noun extraction, and semantic matching strategies
- **`references/spacing-examples.md`** - Comprehensive examples of spacing rules with edge cases

## Workflow Summary

To enhance an SRT file with reference document:

1. Locate `origin.md` in the same directory as the SRT file
2. Read and parse both files
3. Build knowledge base from `origin.md` (proper nouns, terminology, correct spellings)
4. For each SRT subtitle segment:
   - Semantically match with reference content
   - Identify typos, incorrect proper nouns, missing spaces
   - Apply corrections while preserving timeline
5. Validate all corrections maintain content fidelity
6. Save output as `enhanced.srt`
7. Verify timestamps unchanged and no content added

Focus on semantic understanding and conservative corrections. The goal is to refine existing subtitle content using the reference document as a guide, not to rewrite or add new content. Maintain the integrity of the original SRT structure while improving accuracy and formatting.
