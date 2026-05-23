---
name: amcs-producer-notes-generator
description: Generate production notes defining song structure, hooks, instrumentation hints, per-section tags, and mix parameters. Aligns with style spec and blueprint production guidelines. Use when creating arrangement, dynamics, and audio engineering guidance for composition and rendering.
---

# AMCS Producer Notes Generator

Creates comprehensive production notes that define arrangement structure, hook placement, instrumentation details, per-section dynamics, and mix parameters aligned with style specifications.

## When to Use

Invoke this skill after PLAN and STYLE generation to create production notes. Runs in parallel with LYRICS node and feeds into COMPOSE.

## Input Contract

```yaml
inputs:
  - name: sds_producer
    type: amcs://schemas/producer-notes-1.0.json
    required: true
    description: Producer notes entity from SDS with user preferences
  - name: plan
    type: amcs://schemas/plan-1.0.json
    required: true
    description: Section order and duration targets
  - name: style
    type: amcs://schemas/style-1.0.json
    required: true
    description: Musical style for alignment
  - name: seed
    type: integer
    required: true
    description: Determinism seed (use seed+3 for this node)
```

## Output Contract

```yaml
outputs:
  - name: producer_notes
    type: amcs://schemas/producer-notes-1.0.json
    description: |
      Complete production spec with:
      - structure: Section arrangement string
      - hooks: Hook count and placement
      - instrumentation: Additional instrument notes
      - section_meta: Per-section tags and durations
      - mix: LUFS, space, stereo width parameters
```

## Determinism Requirements

- **Seed**: `run_seed + 3` for any stochastic section tag selection
- **Temperature**: 0.2 if LLM used for production recommendations
- **Top-p**: 0.8
- **Retrieval**: None (blueprint and style are local)
- **Hashing**: Hash final producer_notes JSON for provenance

## Constraints & Policies

- Structure MUST match `plan.section_order`
- Per-section `target_duration_sec` MUST sum to within ±30s of `sds.constraints.duration_sec`
- Section names in `section_meta` MUST exist in `structure`
- Hook count (`hooks`) MUST be ≥1 for genres requiring memorable elements
- Instrumentation MUST NOT conflict with style instrumentation
- Per-section tags MUST NOT conflict with global style tags
- If `hooks = 0`, log warning about memorability risk

## Implementation Guidance

### Step 1: Build Structure String

1. Extract `plan.section_order`
2. Format as hyphen-separated string: `"Intro–Verse–PreChorus–Chorus–..."`
3. Store in `producer_notes.structure`
4. Validate all sections from plan are included

### Step 2: Determine Hook Count and Placement

1. Read `sds_producer.hooks` as base count
2. If `plan.evaluation_targets.hook_density` exists:
   - Calculate recommended hooks: `num_chorus_sections * 1.5`
   - Use max(sds_hooks, recommended_hooks)
3. If hooks < 1 and genre requires hooks (Pop, Hip-Hop), log warning
4. Store final count in `producer_notes.hooks`

### Step 3: Expand Instrumentation

1. Copy `style.instrumentation` as base
2. Add `sds_producer.instrumentation` if provided
3. Remove duplicates
4. For each section in `plan.section_order`:
   - Determine section-specific instruments from blueprint production guidelines
   - Example: "Bridge" often features minimal instrumentation
   - Add to `section_meta[section].tags` as instrument tags

### Step 4: Generate Per-Section Metadata

For each section in `structure`:

1. **Determine Tags**:
   - Load blueprint production guidelines for section type
   - Example guidelines:
     - Intro: ["instrumental", "low energy", "atmospheric"]
     - Verse: ["storytelling", "moderate energy"]
     - PreChorus: ["build-up", "rising energy", "add percussion"]
     - Chorus: ["anthemic", "full instrumentation", "hook-forward"]
     - Bridge: ["minimal", "dramatic shift", "breakdown"]
     - Outro: ["fade-out", "reflective"]
   - Merge with `sds_producer.section_meta[section].tags` if provided
   - Validate no conflicts with global style tags

2. **Set Duration**:
   - Use `sds_producer.section_meta[section].target_duration_sec` if provided
   - Otherwise calculate proportionally from `sds.constraints.duration_sec`
   - Store in `section_meta[section].target_duration_sec`

3. **Store Section Metadata**:
   ```json
   {
     "section_meta": {
       "Intro": {
         "tags": ["instrumental", "low energy"],
         "target_duration_sec": 10
       },
       "Chorus": {
         "tags": ["anthemic", "hook-forward", "full instrumentation"],
         "target_duration_sec": 25
       }
     }
   }
   ```

### Step 5: Define Mix Parameters

1. **LUFS Target**:
   - Default: -12.0 LUFS (modern streaming standard)
   - Adjust for genre:
     - Electronic/Hip-Hop: -9.0 to -11.0 (louder)
     - Jazz/Classical: -14.0 to -16.0 (more dynamic range)
   - Use `sds_producer.mix.lufs` if provided

2. **Space/Reverb**:
   - Map from style mood:
     - "intimate" → "dry"
     - "epic" → "lush"
     - "vintage" → "vintage tape"
   - Use `sds_producer.mix.space` if provided

3. **Stereo Width**:
   - Default: "normal"
   - "anthemic" energy → "wide"
   - "intimate" mood → "narrow"
   - Use `sds_producer.mix.stereo_width` if provided

4. Store in `producer_notes.mix`

### Step 6: Validate and Return

1. Validate structure matches plan section order
2. Check section duration sum: `abs(sum - duration_sec) ≤ 30`
3. Ensure all `section_meta` keys exist in `structure`
4. Validate against `amcs://schemas/producer-notes-1.0.json`
5. Compute SHA-256 hash
6. Return producer_notes with hash metadata

## Examples

### Example 1: Christmas Pop Production

**Input**:
```json
{
  "sds_producer": {
    "structure": "",
    "hooks": 2,
    "instrumentation": ["sleigh bells"],
    "section_meta": {
      "Chorus": {"tags": ["crowd-chant"]}
    },
    "mix": {"lufs": -12.0, "space": "lush"}
  },
  "plan": {
    "section_order": ["Intro", "Verse", "PreChorus", "Chorus", "Bridge", "Chorus"]
  },
  "style": {
    "energy": "anthemic",
    "instrumentation": ["brass", "upright bass", "handclaps"],
    "mood": ["upbeat", "cheeky"]
  },
  "seed": 45
}
```

**Output**:
```json
{
  "structure": "Intro–Verse–PreChorus–Chorus–Bridge–Chorus",
  "hooks": 2,
  "instrumentation": ["brass", "upright bass", "handclaps", "sleigh bells"],
  "section_meta": {
    "Intro": {
      "tags": ["instrumental", "low energy", "sleigh bells"],
      "target_duration_sec": 10
    },
    "Verse": {
      "tags": ["storytelling", "moderate energy"],
      "target_duration_sec": 30
    },
    "PreChorus": {
      "tags": ["build-up", "handclaps", "rising energy"],
      "target_duration_sec": 15
    },
    "Chorus": {
      "tags": ["anthemic", "hook-forward", "full instrumentation", "crowd-chant"],
      "target_duration_sec": 25
    },
    "Bridge": {
      "tags": ["minimal", "dramatic shift", "brass feature"],
      "target_duration_sec": 20
    }
  },
  "mix": {
    "lufs": -12.0,
    "space": "lush",
    "stereo_width": "wide"
  },
  "_hash": "jkl012...",
  "_total_duration": 175
}
```

## Common Pitfalls

1. **Structure Mismatch**: Not matching plan section order breaks composition
2. **Duration Overflow**: Section durations summing >30s beyond target causes rendering issues
3. **Missing Sections**: Not including section_meta for all sections in structure
4. **Tag Conflicts**: Per-section tags conflicting with global style tags
5. **Zero Hooks**: Setting hooks=0 for hook-dependent genres fails validation
6. **Invalid LUFS**: Using LUFS values outside reasonable range (-20 to -6)
7. **Instrumentation Duplication**: Not deduplicating combined instrument lists
