---
name: amcs-prompt-composer
description: Merge style, lyrics, and producer notes into render-ready composed prompt. Enforces character limits, resolves tag conflicts, normalizes living artist influences, and formats with clear section tags. Use when creating final prompts for music rendering engines with strict format and policy compliance.
---

# AMCS Prompt Composer

Assembles validated style specifications, lyrics, and production notes into a single render-ready prompt that adheres to engine-specific character limits, tag formatting, and policy constraints.

## When to Use

Invoke this skill after STYLE, LYRICS, and PRODUCER nodes complete. This is the final artifact generation step before VALIDATE and RENDER.

## Input Contract

```yaml
inputs:
  - name: style
    type: amcs://schemas/style-1.0.json
    required: true
    description: Validated style specification
  - name: lyrics
    type: string
    required: true
    description: Complete lyrics with section markers
  - name: producer_notes
    type: amcs://schemas/producer-notes-1.0.json
    required: true
    description: Production arrangement and mix guidance
  - name: engine_limits
    type: /limits/engine_limits.json
    required: true
    description: Target engine character limits and format rules
  - name: seed
    type: integer
    required: true
    description: Determinism seed (use seed+4 for this node)
```

## Output Contract

```yaml
outputs:
  - name: composed_prompt
    type: amcs://schemas/composed-prompt-0.2.json
    description: |
      Render-ready prompt containing:
      - text: Complete formatted prompt string
      - meta: {title, genre, tempo_bpm, structure, style_tags, section_tags, model_limits}
  - name: issues
    type: array[string]
    description: List of warnings or constraint violations (e.g., "exceeded style_max by 50 chars")
```

## Determinism Requirements

- **Seed**: `run_seed + 4` for any tag prioritization decisions
- **Temperature**: N/A (template-based composition, no LLM generation)
- **Top-p**: N/A
- **Retrieval**: None
- **Hashing**: Hash final composed_prompt.text for provenance

## Constraints & Policies

- Total prompt length MUST NOT exceed `engine_limits.prompt_max` (e.g., 5000 chars for Suno)
- Style tags length MUST NOT exceed `engine_limits.style_max` (e.g., 1000 chars)
- Section tags MUST use engine-specific format: `[Intro]`, `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]`
- NO conflicting tags allowed (enforced by tag_conflict_matrix)
- NO "style of [living artist]" phrasing when `policy.release.strict = true`
- Normalize living artist influences to generic: "Drake" → "contemporary hip-hop"
- Include BPM, mood, and instrumentation in meta section (≤2 sentences)
- Use concise descriptions, avoid verbose explanations

## Implementation Guidance

### Step 1: Build Meta Header

Format template:
```
Title: {style.meta.title or "Untitled"}
Genre/Style: {style.genre_detail.primary} | BPM: {style.tempo_bpm} | Mood: {style.mood[0-2]}
```

Example:
```
Title: Elf On Overtime
Genre/Style: Christmas Pop | BPM: 120 | Mood: upbeat, cheeky
```

### Step 2: Assemble Style Tags

1. **Collect Tags**:
   - Start with `style.tags`
   - Add genre, subgenres, fusions
   - Add instrumentation (max 3)
   - Add vocal_profile

2. **Order by Category**:
   - Era → Genre/Subgenre/Fusion → Energy → Instrumentation → Rhythm → Vocal → Mix

3. **Format**:
   ```
   Influences: {comma-separated ordered tags}
   ```

4. **Enforce style_max**:
   - If length > `engine_limits.style_max`:
     - Drop lowest-weight tags from least critical categories (Mix, Era)
     - Log warning in `issues`

Example:
```
Influences: 2010s, Christmas Pop, big band, electro swing, anthemic, brass, upright bass, four-on-the-floor, male/female duet, modern bright mix
```

### Step 3: Normalize Living Artist Influences

1. Scan `style.tags` and `style.vocal_profile` for artist names
2. For each living artist detected:
   - If `policy.release.strict = true`:
     - Replace with generic influence: "Drake" → "contemporary hip-hop artist"
     - Log replacement in `issues`
   - If `policy.release.strict = false`:
     - Keep original (for private/internal use)

### Step 4: Format Structure and Vocal

```
Structure: {producer_notes.structure}
Vocal: {style.vocal_profile}
Hooks: {producer_notes.hooks}
```

Example:
```
Structure: Intro–Verse–PreChorus–Chorus–Verse–PreChorus–Chorus–Bridge–Chorus
Vocal: male/female duet, crooner + bright pop
Hooks: 2
```

### Step 5: Embed Lyrics with Section Tags

1. Parse `lyrics` to identify section markers (e.g., `[Verse]`, `[Chorus]`)
2. For each section:
   - Get `producer_notes.section_meta[section].tags`
   - Format section header with tags:
     ```
     [Intro: instrumental, low energy, sleigh bells]
     ```
   - Append section lyrics

3. Complete lyrics block example:
   ```
   Lyrics:
   [Intro: instrumental, low energy, sleigh bells]
   (instrumental intro)

   [Verse: storytelling, moderate energy]
   Gathering 'round on Christmas Eve
   The kids decorate, we all believe

   [Chorus: anthemic, hook-forward, full instrumentation]
   Family time is what we need
   Love and joy in every deed
   ```

### Step 6: Add Production Notes

Format:
```
Production Notes:
- Arrangement: {producer_notes.instrumentation joined}
- Mix: {producer_notes.mix.space}, {producer_notes.mix.stereo_width} stereo
- Clean = {!sds.constraints.explicit}; Language = {sds.lyrics.language}
```

Example:
```
Production Notes:
- Arrangement: sleigh bells, upright bass, brass stabs; handclaps in pre-chorus
- Mix: lush, wide stereo
- Clean = TRUE; Language = en
```

### Step 7: Check Character Limits

1. Measure total prompt length
2. If > `engine_limits.prompt_max`:
   - Trim production notes (remove least critical details)
   - Trim style tags (drop low-weight tags)
   - If still over, log error in `issues` and truncate with "..."
   - Mark as validation failure

3. Log final character counts in meta

### Step 8: Resolve Tag Conflicts

1. Collect all tags from style + section_meta
2. For each tag pair, check `tag_conflict_matrix.json`
3. If conflict detected:
   - Drop lower-weight tag
   - Log in `issues`: "Dropped 'whisper' due to conflict with 'anthemic'"

### Step 9: Assemble Final Output

Build `composed_prompt`:

```json
{
  "text": "[complete formatted prompt from steps 1-6]",
  "meta": {
    "title": "Elf On Overtime",
    "genre": "Christmas Pop",
    "tempo_bpm": 120,
    "structure": "Intro–Verse–PreChorus–Chorus–...",
    "style_tags": ["2010s", "Christmas Pop", "anthemic", "brass", ...],
    "negative_tags": ["muddy low-end"],
    "section_tags": {
      "Intro": ["instrumental", "low energy"],
      "Chorus": ["anthemic", "hook-forward"]
    },
    "model_limits": {
      "style_max": 1000,
      "prompt_max": 5000
    }
  }
}
```

### Step 10: Validate and Return

1. Validate against `amcs://schemas/composed-prompt-0.2.json`
2. Compute SHA-256 hash of `text`
3. Return `{composed_prompt, issues, _hash}`

## Examples

### Example 1: Christmas Pop Composition

**Input**:
```json
{
  "style": {
    "genre_detail": {"primary": "Christmas Pop"},
    "tempo_bpm": 120,
    "mood": ["upbeat", "cheeky"],
    "tags": ["2010s", "anthemic", "brass"],
    "vocal_profile": "male/female duet"
  },
  "lyrics": "[Intro]\n...\n[Verse]\nGathering 'round...\n[Chorus]\nFamily time is what we need...",
  "producer_notes": {
    "structure": "Intro–Verse–Chorus",
    "hooks": 2,
    "instrumentation": ["brass", "sleigh bells"],
    "section_meta": {
      "Intro": {"tags": ["instrumental", "low energy"]},
      "Chorus": {"tags": ["anthemic", "hook-forward"]}
    },
    "mix": {"space": "lush", "stereo_width": "wide"}
  },
  "engine_limits": {"style_max": 1000, "prompt_max": 5000}
}
```

**Output**:
```json
{
  "composed_prompt": {
    "text": "Title: Elf On Overtime\nGenre/Style: Christmas Pop | BPM: 120 | Mood: upbeat, cheeky\nInfluences: 2010s, Christmas Pop, anthemic, brass, male/female duet\nStructure: Intro–Verse–Chorus\nVocal: male/female duet\nHooks: 2\n\nLyrics:\n[Intro: instrumental, low energy, sleigh bells]\n...\n\n[Verse: storytelling]\nGathering 'round on Christmas Eve\n...\n\n[Chorus: anthemic, hook-forward, full instrumentation]\nFamily time is what we need\n...\n\nProduction Notes:\n- Arrangement: brass, sleigh bells\n- Mix: lush, wide stereo\n- Clean = TRUE; Language = en",
    "meta": {
      "title": "Elf On Overtime",
      "genre": "Christmas Pop",
      "tempo_bpm": 120,
      "structure": "Intro–Verse–Chorus",
      "style_tags": ["2010s", "Christmas Pop", "anthemic", "brass"],
      "section_tags": {
        "Intro": ["instrumental", "low energy"],
        "Chorus": ["anthemic", "hook-forward"]
      },
      "model_limits": {"style_max": 1000, "prompt_max": 5000}
    }
  },
  "issues": [],
  "_hash": "mno345...",
  "_char_counts": {"style": 85, "total": 487}
}
```

## Common Pitfalls

1. **Character Overflow**: Not checking limits before assembly causes truncation
2. **Tag Conflicts**: Missing conflict resolution produces contradictory prompts
3. **Artist Naming**: Leaving living artist names in public prompts violates policy
4. **Missing Section Tags**: Omitting per-section tags reduces rendering control
5. **Verbose Production Notes**: Over-explaining arrangement wastes character budget
6. **Section Mismatch**: Using section names not in lyrics or structure
7. **Format Violations**: Not using `[Section: tags]` format breaks engine parsing
