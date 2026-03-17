---
name: Session Creation
tier: 3
load_policy: task-specific
description: Initialize new session directories with scaffolding and manifest
version: 1.0.0
parent_skill: production-operations
---

# Session Creation Skill

> **The Starting Point of Every Journey**

This skill handles creating new session directories with all required scaffolding.

---

## Purpose

Initialize properly-structured session directories ready for content creation.

---

## Quick Command

```bash
./scripts/utilities/create_new_session.sh "session-name"
```

Or use the slash command:

```bash
/new-session session-name
```

---

## Directory Structure Created

```
sessions/{session-name}/
├── manifest.yaml          # Session configuration
├── notes.md               # Design notes and references
├── midjourney-prompts.md  # Image generation prompts
├── working_files/
│   ├── script_production.ssml  # Full script with SFX
│   └── script_voice_clean.ssml # TTS-ready script
├── images/
│   ├── uploaded/          # Final images for video
│   └── stock_cache/       # Downloaded stock images
└── output/
    ├── video/             # Assembled video files
    └── youtube_package/   # Upload-ready package
```

---

## Naming Conventions

### Session Names

| Rule | Example |
|------|---------|
| Use kebab-case | `inner-child-healing` |
| Lowercase only | `deep-sleep-forest` |
| Descriptive but concise | `confidence-morning-boost` |
| Include outcome if clear | `anxiety-release-theta` |

### Avoid

- Spaces: `inner child healing` ❌
- Underscores: `inner_child_healing` ❌
- CamelCase: `InnerChildHealing` ❌
- Numbers at start: `001-session` ❌

---

## Manifest Template

```yaml
# manifest.yaml
session:
  name: "Session Name"
  slug: "session-slug"
  duration_target: 25  # minutes
  depth_level: "Layer2"  # Layer1, Layer2, Layer3, Ipsissimus

  # Core content
  desired_outcome: "healing"  # healing, transformation, confidence, etc.
  theme: "Description of the journey theme"
  archetypes:
    - "Guide"
    - "Healer"

  # Audio settings
  voice:
    voice_id: "en-US-Neural2-H"
    speaking_rate: 0.88
    pitch: 0

  binaural:
    carrier_frequency: 200
    start_hz: 10
    end_hz: 4

  # Metadata
  youtube:
    title: "Title for YouTube"
    description: "YouTube description..."
    tags:
      - "hypnosis"
      - "meditation"
```

---

## Full Pipeline Command

For complete session creation through packaging:

```bash
/full-build session-name
```

This runs:
1. Session directory creation
2. Manifest generation
3. SSML script generation
4. Audio build (voice + binaural + mix)
5. Hypnotic post-processing
6. Scene image generation
7. Video assembly
8. YouTube packaging

---

## Manifest Generation

Generate manifest from topic description:

```bash
/generate-manifest session-name
```

Provide:
- Topic/theme description
- Target duration
- Desired outcome
- Any specific archetypes or imagery

---

## Quality Gates

### After Creation

- [ ] Directory structure complete
- [ ] `manifest.yaml` has all required fields
- [ ] Session slug matches directory name
- [ ] No template placeholders remaining

### Before Script Generation

- [ ] Manifest validated
- [ ] Outcome defined
- [ ] Duration target set
- [ ] Archetypes selected

---

## Knowledge Base Check

Before creating a new session, check lessons learned:

```bash
cat knowledge/lessons_learned.yaml | head -50
```

Apply insights from past sessions:
- Successful themes
- Optimal durations
- Effective archetypes
- Audio settings that work

---

## Next Steps After Creation

1. **Edit Manifest**: Customize `manifest.yaml` with session details
2. **Generate Script**: `/generate-script session-name`
3. **Create Images**: Generate prompts or use stock images
4. **Build Audio**: `/build-audio session-name`
5. **Build Video**: `/build-video session-name`

---

## Related Resources

- **Skill**: `tier3-production/ssml-generation/` (next step)
- **Doc**: `docs/CANONICAL_WORKFLOW.md`
- **Script**: `scripts/utilities/create_new_session.sh`
- **Schema**: `config/manifest.schema.json`
