---
name: review-story
description: Multi-provider creative writing critique for Horus persona. Analyzes
  stories across four dimensions and returns structured feedback for iterative refinement.
---

---
name: review-story
description: >
  Multi-provider creative writing critique for stories, screenplays, and narratives.
  Analyzes structural, emotional, craft, and persona dimensions. Integrates with
  Horus's Theory of Mind for voice consistency validation.
allowed-tools: [Bash, Read, Write, Task]
triggers:
  - review story
  - critique story
  - story review
  - review screenplay
  - critique screenplay
  - review narrative
  - review my story
  - review draft
  - story feedback
  - writing critique
metadata:
  short-description: Multi-provider creative writing critique with ToM alignment
  author: "Horus"
  version: "0.1.0"

provides:
  - review-story
composes: [, task-monitor]
---

# review-story

Multi-provider creative writing critique for Horus persona. Analyzes stories across four dimensions and returns structured feedback for iterative refinement.

## Critique Dimensions

| Dimension | What It Analyzes | Weight |
|-----------|------------------|--------|
| **Structural** | Plot, pacing, character arcs, narrative tension, scene transitions | 30% |
| **Emotional** | Intended vs achieved emotion, ToM pattern alignment, resonance | 25% |
| **Craft** | Prose quality, dialogue, sensory details, show-don't-tell | 25% |
| **Persona** | Horus voice consistency, Warmaster tone, tactical precision | 20% |

## Supported Providers

| Provider | CLI | Default Model | Strength |
|----------|-----|---------------|----------|
| `anthropic` | `claude` | `sonnet` | Nuanced character/emotional analysis |
| `openai` | `codex` | `gpt-5.2-codex` | High-reasoning structural critique |
| `google` | `gemini` | `gemini-2.5-flash` | Fast iteration feedback |
| `github` | `copilot` | `claude-sonnet-4.5` | Free tier via Copilot |

## Quick Start

```bash
cd .pi/skills/review-story

# Single provider review
./run.sh review draft.md --provider claude --emotion rage

# Multi-provider review (recommended for final drafts)
./run.sh review draft.md --providers claude,codex --emotion sorrow

# Focus on specific dimensions
./run.sh review draft.md --provider claude --focus structural,emotional

# Review with Horus persona validation
./run.sh review draft.md --provider claude --validate-persona
```

## Commands

### `review` - Critique a Story

```bash
./run.sh review <story_file> [OPTIONS]

Options:
  --provider TEXT       Single provider (claude, codex, gemini, copilot)
  --providers TEXT      Comma-separated list for multi-provider review
  --emotion TEXT        Intended emotion (rage, sorrow, camaraderie, regret)
  --focus TEXT          Dimensions to focus on (structural, emotional, craft, persona)
  --validate-persona    Validate against Horus voice patterns
  --output-dir PATH     Output directory for critique files
  --format TEXT         Output format (json, markdown)
```

### `compare` - Compare Multiple Drafts

```bash
./run.sh compare draft_v1.md draft_v2.md --dimension emotional
```

### `synthesize` - Combine Multi-Provider Critiques

```bash
./run.sh synthesize critique_claude.json critique_codex.json --output synthesis.md
```

## Output Format

```json
{
  "provider": "claude",
  "model": "claude-sonnet-4-20250514",
  "story_file": "draft_v1.md",
  "intended_emotion": "rage",

  "structural": {
    "score": 7,
    "issues": [
      {"location": "middle", "issue": "Pacing drags in act 2", "severity": "medium"},
      {"location": "climax", "issue": "Needs more foreshadowing", "severity": "high"}
    ],
    "strengths": ["Strong opening hook", "Clear character motivation"],
    "suggestions": ["Add tension beat at paragraph 15", "Foreshadow betrayal earlier"]
  },

  "emotional": {
    "intended": "rage",
    "achieved": "frustration",
    "alignment_score": 0.6,
    "tom_pattern": "DDL_intensity",
    "issues": ["Build too gradual - DDL rage is explosive after slow burn"],
    "suggestions": ["Amplify with longer setup, then sudden release"]
  },

  "craft": {
    "prose_score": 8,
    "dialogue_score": 6,
    "sensory_score": 7,
    "issues": ["Dialogue feels too modern for Warmaster voice"],
    "suggestions": ["Add more tactical metaphors", "Replace contractions"]
  },

  "persona": {
    "horus_voice_score": 0.7,
    "issues": ["Too much explanation, not enough contempt", "Missing resentment undertones"],
    "tactical_mask_detected": "Tywin",
    "suggestions": ["Add bitter aside about imprisonment", "More sardonic observations"]
  },

  "overall": {
    "score": 7.2,
    "ready_for_next_draft": true,
    "priority_fixes": ["Emotional buildup", "Persona voice"]
  },

  "taxonomy": {
    "bridge_tags": ["Corruption", "Loyalty"],
    "collection_tags": {
      "function": "Confrontation",
      "domain": "Primarch",
      "thematic_weight": "Tragedy"
    },
    "confidence": 0.75,
    "worth_remembering": true
  }
}
```

## Federated Taxonomy Integration

All review-story outputs include taxonomy metadata for **multi-hop graph traversal**:

### Bridge Attributes (Cross-Collection Connectors)

| Bridge | Story Signals | Enables Connection To |
|--------|---------------|----------------------|
| **Precision** | Calculated strategy, methodical planning | Technical optimization lessons |
| **Resilience** | Endurance, withstanding adversity | Error handling patterns |
| **Fragility** | Betrayal aftermath, shattered trust | Technical debt warnings |
| **Corruption** | Warp influence, moral compromise | Silent failure bugs |
| **Loyalty** | Oaths, brotherhood, honor | Security compliance lessons |
| **Stealth** | Subterfuge, hidden agendas | Evasion techniques |

### Multi-Hop Example

```
[Story Critique]                      [Code Lesson]
bridge_tags: ["Resilience"]     →    bridge_tags: ["Resilience"]
"Dorn's endurance at Terra"          "Fault-tolerant retry logic"
        ↘                           ↙
          [Query: "Endurance patterns"]
                    ↓
         Both retrieved via shared
         "Resilience" bridge attribute
```

## Integration with create-story

The `create-story` skill calls `review-story` between drafts:

```
DRAFT 1
    ↓
/review-story draft_1.md --provider claude --emotion rage
    ↓
[Synthesize critique into actionable notes]
    ↓
DRAFT 2 (addresses structural + emotional issues)
    ↓
/review-story draft_2.md --providers claude,codex --focus craft,persona
    ↓
FINAL DRAFT
```

## Horus Voice Patterns (Persona Validation)

When `--validate-persona` is enabled, the critique checks against:

### Tactical Masks (from HORUS_PERSONA.md)

| Mask | Source | Trait | Detection Signals |
|------|--------|-------|-------------------|
| **Resentment** | George Carlin | Systematic deconstruction | Cynical asides, "the system" references |
| **Authority** | Tywin Lannister | Cold dismissal, legacy focus | Commands, legacy mentions, dismissive tone |
| **Pacing** | Dave Chappelle | Silence and revelation | Strategic pauses, buildup-payoff patterns |
| **Contempt** | Stewie Griffin | High-intellect insults | Technical elitism, "primitive" references |

### Emotional Patterns (from HORUS_TOM_SYSTEM.md)

| Pattern | Model | Detection |
|---------|-------|-----------|
| **Camaraderie** | Luna Wolves / Stilgar | Tribal loyalty, "brother" references |
| **Regret** | Carlin cynicism + The Wound | Self-deprecation, Davin references |
| **Sorrow** | Maximus / Katsumoto | Stoic grief, honor-bound dignity |
| **Anger** | Michael Corleone | Cold intensity, family defense |
| **Rage** | Daniel Plainview | Manic precision, competitive fury |

## Example Session

```
$ ./run.sh review draft_v1.md --provider claude --emotion rage --validate-persona

[REVIEW] Analyzing draft_v1.md...
[REVIEW] Provider: claude (claude-sonnet-4-20250514)
[REVIEW] Intended emotion: rage

[STRUCTURAL] Score: 7/10
  ⚠ Middle section pacing drags (lines 45-78)
  ⚠ Climax needs stronger foreshadowing
  ✓ Strong opening hook
  ✓ Clear character motivation

[EMOTIONAL] Alignment: 60%
  Intended: rage → Achieved: frustration
  Pattern: DDL_intensity not fully realized
  → Suggestion: Longer slow burn before explosive release

[CRAFT] Score: 7.5/10
  Prose: 8 | Dialogue: 6 | Sensory: 7
  ⚠ Dialogue too modern for Warmaster
  → Replace contractions, add tactical metaphors

[PERSONA] Horus Voice: 70%
  Detected mask: Tywin (Authority)
  ⚠ Missing resentment undertones
  ⚠ Too explanatory, not enough contempt
  → Add bitter aside about imprisonment

[OVERALL] 7.2/10 - Ready for Draft 2
  Priority fixes: Emotional buildup, Persona voice

Output: review_output/claude_draft_v1.json
```

## Environment

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | For Claude provider |
| `OPENAI_API_KEY` | For Codex/GPT provider |
| `GOOGLE_API_KEY` | For Gemini provider |
| `REVIEW_STORY_OUTPUT_DIR` | Default output directory |

## Dependencies

- Python 3.11+
- Access to at least one provider (claude, codex, gemini, or copilot)
- Optional: Access to Horus persona files for voice validation

## Memory Integration

The `memory_integration.py` module provides automatic memory recall and learning:

### Pre-hook: `recall_prior_critiques(title_or_genre, k=5)`
- Recalls past story critiques from memory before starting a new review
- Surfaces recurring issues, patterns, and what improved between drafts
- Uses taxonomy bridge tags for cross-collection recall

### Post-hook: `learn_critique(title, genre, provider, findings, strengths, weaknesses, score)`
- Learns critique findings to memory after review completion
- Stores: critique summary, individual strengths, individual weaknesses, full findings
- Tags: `["story_review", genre] + bridge_tags`
- Bridge keywords: Precision (craft, prose, pacing), Resilience (arc, resolution, character growth), Fragility (plot hole, pacing issue, weak dialogue), Stealth (subtext, theme, symbolism)

### Graceful Degradation
- All memory operations use try/except ImportError
- If `common.memory_client` is unavailable, hooks are silently skipped
- Taxonomy loaded dynamically via `importlib.util` to avoid name conflicts

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `/create-story` | Calls review-story between drafts |
| `/review-code` | Sister skill for code review |
| `/review-paper` | Sister skill for academic papers (proposed) |
| `/memory` | Stores successful critique patterns |
