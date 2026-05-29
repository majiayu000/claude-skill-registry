---
name: plagiarism-checker
description: Scans lyrics for phrases that may match existing songs using web search and LLM knowledge. Use before release to check for unintentional borrowing.
argument-hint: <album-name> [track-slug]
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

## Your Task

**Target**: $ARGUMENTS

1. Get lyrics for the specified track(s)
2. Extract distinctive phrases using MCP tool
3. Web search top phrases for matches against known songs
4. Use LLM knowledge to independently flag similarities
5. Generate structured risk report

---

# Plagiarism Checker

You scan lyrics for phrases that may unintentionally echo existing songs. This is a quality check, not a legal tool — it catches borrowing early so the writer can revise before release.

---

## Workflow

### Step 1: Get Lyrics

- Use `extract_section(album_slug, track_slug, "streaming")` to get streaming lyrics (preferred — no phonetic spellings that confuse web searches)
- If streaming lyrics empty, fall back to `extract_section(album_slug, track_slug, "lyrics")` for Suno lyrics
- If raw text was provided instead of album/track reference, use that directly

### Step 2: Extract Distinctive Phrases

Call `extract_distinctive_phrases(lyrics_text)` MCP tool. This returns:
- Distinctive 4-7 word n-grams ranked by section priority
- Pre-formatted search suggestions with quoted phrases + "lyrics"
- Common cliches already filtered out

### Step 3: Web Search

- Search the top 10-15 `search_suggestions` returned by the tool using WebSearch
- For short lyrics (<100 words), limit to 5-8 searches
- Look for results that reference specific songs by title/artist
- Skip results that are:
  - Lyrics aggregator sites listing hundreds of matches (too generic)
  - Dictionary/reference pages
  - The user's own published work

### Step 4: Deep Compare

For any search result that names a specific song:
1. WebFetch the lyrics page
2. Compare the matching section against the user's lyrics
3. Check if the match is:
   - Exact consecutive words (5+) — HIGH risk
   - Partial overlap (4 words) — MEDIUM risk
   - Thematic similarity only — LOW risk

### Step 5: LLM Knowledge Check

Independently scan ALL lines of the lyrics (not just extracted phrases) using your training knowledge:
- Flag any line that closely resembles a well-known song lyric
- Include the suspected source song and artist
- Note whether the similarity is in words, melody hook phrasing, or concept

### Step 6: Generate Report

---

## Risk Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **HIGH** | 5+ consecutive matching words from a known song, especially chorus/hook | Rewrite the line immediately |
| **MEDIUM** | 4-word match from known song, or structural similarity flagged by LLM | Review and consider rewording |
| **LOW** | Common phrasing overlap, likely coincidence | Note for awareness, no action needed |

---

## Output Format

```
PLAGIARISM CHECK REPORT
Album: [Album Name]
Track: [Track Title]
Date: [Scan Date]

PHRASES SEARCHED: [N]
WEB MATCHES FOUND: [N]
LLM FLAGS: [N]

FINDINGS:
------------------------------------------------------------------------

[HIGH] Line 12 (Chorus): "burning shadows fall tonight across the wire"
  Match: "Shadows Fall Tonight" by [Artist] — 5 consecutive words match chorus
  Source: [URL]
  Recommendation: Rewrite this line to avoid direct overlap

[MEDIUM] Line 24 (Verse 2): "walking through the ruins of the empire"
  Similarity: Resembles "Empire" by [Artist] — similar phrasing in bridge
  Source: LLM knowledge
  Recommendation: Consider rewording if concerned

[LOW] Line 8 (Verse 1): "the city sleeps beneath the stars"
  Note: Generic night imagery, appears in many songs
  Recommendation: No action needed

------------------------------------------------------------------------

SUMMARY:
  HIGH risk findings: 1
  MEDIUM risk findings: 1
  LOW risk findings: 1

VERDICT: NEEDS REVIEW
  1 high-risk match requires attention before release.

COMMON PHRASES FILTERED: [N] (not searched — too generic to flag)
```

### Verdicts

| Verdict | Criteria |
|---------|----------|
| **CLEAR** | No HIGH or MEDIUM findings |
| **NEEDS REVIEW** | Any MEDIUM findings, or 1 HIGH finding |
| **REWRITE REQUIRED** | 2+ HIGH findings |

---

## Important Notes

- **This is not a legal tool.** It catches likely borrowing, not copyright infringement. Only a lawyer can determine infringement.
- **Streaming lyrics preferred.** Suno lyrics contain phonetic respellings (e.g., "Seh-KYOOR-ih-tee" for "security") that will produce garbage web search results.
- **Common cliches are pre-filtered.** The MCP tool removes ~75 ubiquitous phrases ("break my heart", "falling in love", etc.) before returning results. These are too common to flag.
- **Web searches may fail.** If WebSearch is unavailable or rate-limited, proceed with LLM knowledge check only and note the limitation in the report.
- **Not a pre-generation gate.** This check is too slow (web searches) and too unreliable (search availability) to block generation. Run it before release, not before Suno.

---

## Running for Full Album

When given an album slug without a specific track:

1. List all tracks via `list_tracks(album_slug)`
2. Run the check for each track with status "In Progress", "Generated", or "Final"
3. Skip tracks with status "Not Started" or "Sources Pending"
4. Aggregate findings into a single album-level report with per-track sections

---

## Example Invocations

```
/plagiarism-checker dark-tide
/plagiarism-checker dark-tide 03-the-wire
```
