---
name: review-design
description: Multi-provider AI design review skill. Submits UI screenshots + design
  tokens to vision-capable LLMs for structured UX audits.
---

---
name: review-design
description: >
  Multi-provider AI design review of UI screenshots and design tokens for UX audits.
triggers:
  - review design
  - design review
  - UX audit
  - audit this UI
  - review this UI
  - review the design
  - critique this design
  - compare to raycast
  - design comparison
  - visual review
  - UI review
  - check the UX
  - assess the design
  - design feedback
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Vision-driven UX design review

provides:
  - review-design
composes: [, task-monitor]
---

# review-design

Multi-provider AI design review skill. Submits UI screenshots + design tokens to vision-capable LLMs for structured UX audits.

## Triggers

- review design
- design review
- UX audit
- audit this UI
- review this UI
- review the design
- critique this design
- compare to raycast
- design comparison
- visual review
- UI review
- check the UX
- assess the design
- design feedback

## Description

Iterative 3-step design review pipeline inspired by `review-code`:

1. **Audit** - Analyze screenshots against design tokens + reference images, identify gaps
2. **Judge** - Critique the audit findings for accuracy and prioritization
3. **Finalize** - Produce actionable recommendations with specific token/layout changes

Supports multiple vision-capable providers:
- **Claude** (`claude`) - claude-sonnet-4-20250514 (vision)
- **OpenAI** (`openai`) - gpt-4o (vision)
- **Gemini** (`gemini`) - gemini-2.0-flash (vision)

## Requirements

**Screenshots are MANDATORY.** This skill will fail if no screenshots are provided. A design review without visual evidence is impossible — it would be pure speculation.

Capture screenshots before running a review:
- `/surf snap` — Browser screenshot via CDP
- `/surf-qml` — QML/Qt app screenshot via AT-SPI
- `flameshot full --path ./screenshots/current.png` — System screenshot

The `--screenshots` directory must contain at least one PNG/JPG image.

## Usage

```bash
# Basic design review (single round)
./run.sh review --screenshots ./screenshots/ --tokens ./design-tokens.json

# With reference images (compare to target design)
./run.sh review --screenshots ./current/ --reference ./raycast/ --tokens ./tokens.json

# Multi-round iterative review (recommended)
./run.sh review-full --screenshots ./current/ --reference ./target/ --tokens ./tokens.json --rounds 2

# Specific provider
./run.sh review --provider claude --screenshots ./ui/

# Generate review request bundle (for manual submission)
./run.sh bundle --screenshots ./ui/ --tokens ./tokens.json --output review_request.md
```

## Input Format

### Design Tokens (JSON)
```json
{
  "meta": { "name": "...", "description": "..." },
  "colors": { ... },
  "typography": { ... },
  "layout": { ... },
  "animation": { ... },
  "effects": { ... },
  "interactions": { ... }
}
```

### Screenshots
- PNG/JPG files in a directory
- Named descriptively: `full-launcher-empty.png`, `result-list-hover.png`
- Include both current UI and reference/target UI if comparing

## Output Format

### Per-Round Files (in `review_output/`)
```
roundN_step1.md      # Initial audit findings
roundN_step2.md      # Judge critique
roundN_final.md      # Finalized recommendations
roundN_audit.json    # Structured findings (machine-readable)
```

### Audit JSON Structure
```json
{
  "summary": "Overall assessment",
  "findings": [
    {
      "severity": "high|medium|low",
      "category": "color|typography|layout|spacing|animation|interaction",
      "element": "search-bar",
      "issue": "Description of the gap",
      "current": "Current value or behavior",
      "recommended": "Suggested fix",
      "token_change": { "path": "colors.text.primary", "from": "#fff", "to": "#f5f5f5" }
    }
  ],
  "token_changes": [ ... ],
  "praise": [ "Things done well" ]
}
```

## Provider Capabilities

| Provider | Model | Vision | Cost | Session |
|----------|-------|--------|------|---------|
| claude | claude-sonnet-4-20250514 | Yes | Paid | Yes |
| openai | gpt-4o | Yes | Paid | No |
| gemini | gemini-2.0-flash | Yes | Free tier | No |

## Commands

### `review` - Single-round design audit
Basic audit with optional reference comparison.

### `review-full` - Multi-round iterative audit (recommended)
Runs the 3-step pipeline for N rounds, each round refining findings.

### `bundle` - Generate review request
Creates a markdown file with embedded images (base64) for manual submission to any LLM.

### `compare` - Side-by-side comparison
Generates a visual comparison report between current and target design.

### `check` - Verify provider access
Tests that the selected provider has vision capability and valid credentials.

## Example Workflow

```bash
# 1. Capture screenshots of your UI
flameshot full --path ./screenshots/current.png

# 2. Gather reference screenshots (e.g., Raycast)
cp ~/raycast-ref/*.png ./screenshots/reference/

# 3. Create/update design tokens
cat > design-tokens.json << 'EOF'
{ "colors": { ... }, "typography": { ... } }
EOF

# 4. Run iterative design review
./run.sh review-full \
  --screenshots ./screenshots/ \
  --reference ./screenshots/reference/ \
  --tokens ./design-tokens.json \
  --rounds 2 \
  --provider claude

# 5. Apply recommendations
# Read review_output/round2_final.md for actionable changes
```

## Integration with review-code

After design review produces token changes, you can:
1. Update your style files (QML, CSS, etc.) based on recommendations
2. Run `review-code` to validate the implementation changes
3. Iterate until both design and code reviews pass

## Allowed Tools

- Bash (for provider CLI invocation)
- Read (for loading tokens and configs)
- WebFetch (for fetching remote design specs)

## Notes

- Screenshots should be captured at 1x scale for consistent analysis
- Include the full UI context (not just cropped elements) for better spatial reasoning
- Reference images help but aren't required. However, screenshots ARE required — the skill will fail without them.
- Large images are automatically resized to fit provider limits
