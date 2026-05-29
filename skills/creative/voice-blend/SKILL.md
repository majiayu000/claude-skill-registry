---
name: voice-blend
description: Combine multiple voice profiles with weighted mixing to create hybrid voices. Use when relevant to the task.
---

# voice-blend

Combine multiple voice profiles with weighted mixing to create hybrid voices.

## Triggers

- "blend X and Y voices"
- "mix technical with friendly"
- "combine executive and casual"
- "70% technical, 30% friendly"
- "merge these voices..."

## Behavior

When triggered, this skill:

1. **Loads source voice profiles** from:
   - Built-in templates (`voices/templates/`)
   - Project voices (`.aiwg/voices/`)
   - User voices (`~/.config/aiwg/voices/`)

2. **Parses blend specification**:
   - Equal blend: "blend X and Y" → 50%/50%
   - Weighted blend: "70% X, 30% Y" → explicit weights
   - Multi-voice: "blend X, Y, and Z" → equal thirds

3. **Interpolates dimensions**:
   - Weighted average of tone values (formality, confidence, etc.)
   - Merged vocabulary lists (union of prefer, intersection of avoid)
   - Dominant structure patterns from highest-weighted voice

4. **Generates hybrid profile** with clear lineage tracking

## Usage Examples

### Equal Blend
```
User: "Blend technical-authority and friendly-explainer"

Result: 50/50 blend
- formality: 0.45 (avg of 0.7 and 0.2)
- confidence: 0.8 (avg of 0.9 and 0.7)
- warmth: 0.55 (avg of 0.3 and 0.8)
- vocabulary: merged from both
```

### Weighted Blend
```
User: "80% executive-brief, 20% casual-conversational"

Result: Weighted blend
- formality: 0.7 (0.8*0.85 + 0.2*0.15)
- confidence: 0.86 (0.8*0.9 + 0.2*0.6)
- Dominant structure from executive-brief
```

### Multi-Voice Blend
```
User: "Combine technical-authority, friendly-explainer, and executive-brief"

Result: Equal thirds (33.3% each)
- All dimensions averaged across three profiles
- Vocabulary merged from all three
```

## Blend Algorithm

### Dimension Interpolation

For each tone dimension:
```
blended_value = Σ(weight_i × value_i) / Σ(weight_i)
```

### Vocabulary Merging

- **prefer**: Union of all prefer lists, deduplicated
- **avoid**: Intersection of all avoid lists (only avoid if ALL sources avoid)
- **signature_phrases**: Top N from each source (weighted by blend ratio)

### Structure Resolution

Structure settings use the **dominant voice** (highest weight):
- sentence_length: from dominant
- paragraph_length: from dominant
- use_lists: from dominant
- use_examples: averaged (rarely=0, when-appropriate=1, frequently=2)

### Perspective Handling

- **person**: Majority vote (tie goes to second person)
- **voice**: Active unless all sources use passive
- **tense**: Present unless all sources use past

## Output Format

```yaml
name: technical-friendly-blend
version: 1.0.0
description: Blended voice profile
blend_sources:
  - name: technical-authority
    weight: 0.7
  - name: friendly-explainer
    weight: 0.3
tone:
  formality: 0.55  # interpolated
  confidence: 0.84 # interpolated
  warmth: 0.45     # interpolated
  energy: 0.49     # interpolated
  complexity: 0.65 # interpolated
vocabulary:
  prefer:
    - precise technical terminology  # from technical
    - concrete examples              # from friendly
  avoid:
    - marketing superlatives         # common to both
  signature_phrases:
    - "The system handles..."        # from technical (70%)
    - "Think of it like..."          # from friendly (30%)
structure:
  sentence_length: medium            # from dominant (technical)
  use_examples: frequently           # averaged
```

## Output Location

Blended profiles are saved to:
1. `.aiwg/voices/{name}.yaml` (default)
2. Custom path with `--output` flag
3. `~/.config/aiwg/voices/` with `--global` flag

## Integration

- **Input**: Takes profiles created by `voice-create` or built-in templates
- **Output**: Creates profiles usable by `voice-apply`
- **Chain**: `voice-analyze` → `voice-blend` → `voice-apply`

## CLI Usage

```bash
# Equal blend of two voices
python voice_blender.py --voices "technical-authority,friendly-explainer"

# Weighted blend
python voice_blender.py --voices "technical-authority:0.7,friendly-explainer:0.3"

# Custom output name
python voice_blender.py --voices "..." --name my-hybrid-voice

# Output to specific directory
python voice_blender.py --voices "..." --output .aiwg/voices/

# JSON output for inspection
python voice_blender.py --voices "..." --json
```

## Error Handling

- **Profile not found**: Lists available profiles and suggests closest match
- **Invalid weights**: Normalizes weights to sum to 1.0
- **Incompatible profiles**: Warns but proceeds with best-effort blend

## References

- Voice loader: `../voice-apply/scripts/voice_loader.py`
- Schema: `../../../schemas/voice-profile.schema.json`
- Built-in templates: `../../voices/templates/`
