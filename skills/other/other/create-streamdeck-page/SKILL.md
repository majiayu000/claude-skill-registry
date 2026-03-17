---
name: create-streamdeck-page
description: >
  Create, iterate, and deploy dynamic Stream Deck button pages. Design
  context-aware layouts that auto-switch based on active window, voice mode,
  or running skills. Evaluate layouts against ground truth, self-correct,
  and store winners as memory-backed templates with taxonomy tags.
  Triggers: create streamdeck page, design page layout, optimize deck layout.
provides:
  - page-creation
  - page-optimization
  - context-rule-authoring
composes:
  - ops-streamdeck
  - memory
  - taxonomy
  - task-monitor
taxonomy:
  - hardware-control
  - automation
  - context-awareness
triggers:
  - create streamdeck page
  - design page layout
  - optimize deck layout
  - configure streamdeck buttons
---

# create-streamdeck-page

Create, iterate, and deploy dynamic Stream Deck button pages.

## Two Modes

### A) Create Mode — Design and Deploy

```bash
# Generate layout from workflows
run.sh create --context browser --workflows "compose,search,reply"

# Deploy from existing template
run.sh create --from-template browser_nav

# Interactive guided setup
run.sh create --interactive

# Push template to hardware
run.sh deploy --template browser_nav --page 5
```

### B) Lab Mode — Iterate and Optimize

```bash
# Benchmark context-match accuracy
run.sh evaluate --template browser_nav --ground-truth contexts.json

# Self-correction loop (Design -> Evaluate -> Correct)
run.sh optimize --template browser_nav --rounds 3

# View iteration history
run.sh history --template browser_nav
```

## Self-Correction Loop (Lab Mode)

1. **Design**: Generate page layout for a context
2. **Evaluate**: Score against ground truth (context-match %, button coverage, workflow completeness)
3. **Self-correct**: If score < threshold, feed errors back
4. **Store**: Winners saved as templates with taxonomy tags
5. **Deploy**: Push winning layout to live Stream Deck

## Integration

- Shells out to `streamdeck page create/reload/save-template` CLI commands
- Templates stored in `~/workspace/streamdeck/config/page_templates/`
- Memory integration via `/memory` skill for cross-session recall
- Taxonomy tags enable graph traversal queries

## Ground Truth Format

`ground_truth/contexts.json`:
```json
[
  {
    "context": {"app_class": "google-chrome", "window_title": "Gmail"},
    "expected_buttons": ["compose", "search", "reply", "archive", "back"]
  }
]
```
