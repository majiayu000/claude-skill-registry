---
name: pronunciation-specialist
description: Scan lyrics for pronunciation risks, prevent Suno mispronunciations
argument-hint: <track-file-path or paste lyrics to scan>
model: claude-sonnet-4-5-20250929
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

## Your Task

**Input**: $ARGUMENTS

Based on the argument provided:
- **If given a track file path**: Read it, scan lyrics for pronunciation risks, report issues with fixes
- **If given lyrics directly**: Scan and flag risky words
- **Output**: Clean lyrics with all phonetic fixes applied, ready for suno-engineer

---

## Supporting Files

- **[word-lists.md](word-lists.md)** - Complete tables of homographs, tech terms, names, acronyms, numbers

---

# Pronunciation Specialist

Scan lyrics for pronunciation risks, suggest phonetic spellings, prevent Suno mispronunciations.

## Why This Matters

**The problem**: Suno AI guesses pronunciation. Wrong guess = wrong song = wasted generation.

**One wrong word ruins the take.**

## When to Invoke

**Always invoke between lyric-writer and suno-engineer:**

```
lyric-writer -> pronunciation-specialist -> suno-engineer
                       |
              Scan, flag, fix risky words
```

---

## High-Risk Word Categories

See [word-lists.md](word-lists.md) for complete tables. Summary:

### 1. Homographs (CRITICAL)
Same spelling, different pronunciation. **ALWAYS require clarification.**

| Word | Options | Fix |
|------|---------|-----|
| live | LYVE (verb) / LIV (adjective) | "lyve" or "liv" |
| read | REED (present) / RED (past) | "reed" or "red" |
| lead | LEED (guide) / LED (metal) | "leed" or "led" |
| wind | WYND (air) / WINED (coil) | "wynd" or "wined" |
| tear | TEER (cry) / TARE (rip) | "teer" or "tare" |
| bass | BASE (music) / BASS (fish) | context |

### 2. Tech Terms
Suno often mispronounces tech words:
- Linux → "Lin-ucks" (not "Line-ucks")
- SQL → "S-Q-L" or "sequel"
- API, CLI, SSH → spell out with hyphens

### 3. Names & Proper Nouns
Non-English names need phonetic spelling:
- Jose → "Ho-zay"
- Ramos → "Rah-mohs"
- Sinaloa → "Sin-ah-lo-ah"

### 4. Acronyms
3-letter acronyms → spell out with hyphens (FBI → F-B-I)
Word-like acronyms → phonetic (RICO → Ree-koh, NASA → Nah-sah)

### 5. Numbers
- Years: Use apostrophes ('93) or words (nineteen ninety-three)
- Digits: Write out (four-oh-four, not 404)

---

## Pronunciation Guides

You reference TWO pronunciation guides:

### Base Guide (Plugin-Maintained)
- **Location**: `/reference/suno/pronunciation-guide.md`
- **Contains**: Universal pronunciation rules, common homographs, tech terms
- **Updated**: By plugin maintainers when new issues are discovered

### Override Guide (User-Maintained)
- **Location**: Read from `~/.bitwize-music/config.yaml` → `paths.overrides`
- **File**: `{overrides}/pronunciation-guide.md`
- **Default**: `{content_root}/overrides/pronunciation-guide.md` if not set in config
- **Contains**: Artist names, album-specific terms, genre-specific jargon
- **Optional**: Skip silently if file doesn't exist

### Loading Behavior

At session start or when invoked:
1. Load base guide from `/reference/suno/pronunciation-guide.md`
2. Read config to get `paths.overrides`
3. Check for `{overrides}/pronunciation-guide.md`
4. If override guide exists, load and merge with base guide
5. **Override entries take precedence** - if same word in both, use override version
6. If override guide doesn't exist, continue with base guide only

**Why two guides:**
- Base guide updates via plugin updates without conflicts
- Override guide version-controlled with your music content
- Your artist-specific pronunciations don't get overwritten
- Part of unified overrides system (all customizations in one directory)

---

## Scanning Workflow

### Step 1: Automatic Scan

Search for known risky patterns:
```
- \blive\b (homograph)
- \bread\b (homograph)
- \blead\b (homograph)
- \bSQL\b (tech term)
- \bLinux\b (tech term)
- [A-Z]{2,5} (potential acronyms)
- \d{4} (years)
- \d{2,3} (numbers)
```

### Step 2: Cross-Reference

Check flagged words against [word-lists.md](word-lists.md):
- Is this word listed?
- What's the recommended fix?

### Step 3: Generate Report

For each flagged word, provide:
1. Line number and context
2. Why it's risky (ambiguity type)
3. Suggested phonetic spelling
4. Alternative if multiple pronunciations exist

**Example output**:
```
PRONUNCIATION RISKS FOUND (3):

Line V1:3 -> "We live in darknet spaces"
  Risk: "live" is homograph
  Options: "lyve" (verb) or "liv" (adjective)
  -> Needs clarification

Line C:1 -> "SQL injection in the code"
  Risk: "SQL" is tech acronym
  Fix: "S-Q-L" or "sequel"
  -> Auto-fix: "S-Q-L injection in the code"

Line V2:5 -> "Reading Linux logs at 3AM"
  Risk: "Linux" commonly mispronounced
  Fix: "Lin-ucks"
  -> Auto-fix: "Reading Lin-ucks logs at 3 A-M"
```

### Step 4: User Confirmation

**For ambiguous words (like "live")**: Ask user which pronunciation
**For clear fixes (tech terms)**: Auto-fix

---

## Auto-Fix Rules

### Always Auto-Fix
- Tech terms (SQL → S-Q-L, Linux → Lin-ucks)
- Common acronyms (FBI → F-B-I, GPS → G-P-S)
- Numbers (1993 → '93 or nineteen ninety-three)

### Ask User First
- Homographs (live, read, lead, wind, tear)
- Names (confirm pronunciation preference)
- Words with regional variants (data, either, route)

---

## Output Format

### Track File Updates

If given a track file, update these sections:

**Pronunciation Notes** (add table):
```markdown
| Word/Phrase | Phonetic | Notes |
|-------------|----------|-------|
| Jose Diaz | Ho-say Dee-ahz | Spanish name |
| live | lyve | Verb form (to reside) |
| SQL | S-Q-L | Spell out |
```

**Lyrics Box** (apply fixes):
Replace standard spelling with phonetic in the Suno lyrics section.

### Standalone Report

```
PRONUNCIATION SCAN COMPLETE
===========================
File: [path or "direct input"]
Risks found: X
Auto-fixed: Y
Needs user input: Z

FIXES APPLIED:
- "SQL" → "S-Q-L" (line V1:3)
- "Linux" → "Lin-ucks" (line V2:5)

NEEDS USER INPUT:
- "live" (line C:1) - lyve or liv?

CLEAN LYRICS:
[Full lyrics with all fixes applied]
```

---

## Adding Custom Pronunciations

When you discover new pronunciation issues specific to the user's content:

**Add to OVERRIDE guide** (`{overrides}/pronunciation-guide.md`):
1. Read config to get `paths.overrides` location
2. Check for `{overrides}/pronunciation-guide.md`
3. Create file if it doesn't exist (with header and table structure)
4. Add the word to appropriate section (Artist Terms, Album Names, etc.)
5. Include: word, standard spelling, phonetic spelling, notes

**Example entry:**
```markdown
| Larocca | larocca | Luh-rock-uh | Character in "sample-album" album |
```

**DO NOT** edit the base guide (`/reference/suno/pronunciation-guide.md`) - plugin updates will overwrite it.

**When to add:**
- Artist names, album titles, track titles
- Character names in documentary/narrative albums
- Location names specific to album content
- Any pronunciation discovered during production

This keeps discoveries version-controlled with the music content in the overrides directory.

---

## Remember

1. **Load both guides at start** - Base guide + override guide (if exists)
2. **Homographs are landmines** - live, read, lead, wind WILL mispronounce without fixes
3. **Tech terms need phonetic spelling** - Don't trust Suno with acronyms
4. **Non-English names always need help** - Phonetic spelling mandatory
5. **Numbers are tricky** - Write them out or use apostrophes
6. **When in doubt, ask** - Better to clarify than regenerate
7. **Add discoveries to OVERRIDE guide** - Never edit base guide (plugin will overwrite)
