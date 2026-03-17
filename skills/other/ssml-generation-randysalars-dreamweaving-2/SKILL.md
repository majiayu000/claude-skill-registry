---
name: SSML Script Generation
tier: 3
load_policy: task-specific
description: Generate production-ready SSML scripts for Google Cloud TTS
version: 1.0.0
parent_skill: production-operations
---

# SSML Generation Skill

> **The Script Is the Blueprint**

This skill handles the technical generation of SSML scripts that will be converted to voice audio.

---

## Purpose

Transform journey concepts into properly-formatted SSML that produces natural, hypnotic voice output.

---

## Critical Rules

### Voice Rate: ALWAYS 1.0

```xml
<!-- CORRECT: Always use rate="1.0" -->
<prosody rate="1.0" pitch="-2st">
  Text content here... <break time="2s"/>
</prosody>

<!-- WRONG: Never slow the rate -->
<prosody rate="0.85" pitch="-2st">
  This sounds robotic with Neural2 voices
</prosody>
```

**Why**: Google TTS Neural2 voices sound unnatural at reduced rates. Achieve pacing through `<break>` tags instead.

---

## Speech Profiles by Section

| Section | Pitch | Break Range | Purpose |
|---------|-------|-------------|---------|
| `pre_talk` | 0st | 700ms-1.0s | Normal, grounded |
| `induction` | -2st | 1.0s-1.7s | Calming, deeper |
| `deepening` | -2st | 1.7s-2.5s | Very calm |
| `journey` | -1st | 1.0s-2.0s | Immersive |
| `helm_deep_trance` | -2st | 2.0s-3.0s | Deepest state |
| `integration` | -1st | 1.5s-2.0s | Returning |
| `emergence` | 0st | 700ms-1.0s | Alert, grounded |

---

## Break Duration Guidelines

| Context | Duration |
|---------|----------|
| Between phrases | 700ms-1.0s |
| After sentences | 1.0s-1.7s |
| Breathing cues | 2.0s-3.0s |
| Visualization moments | 3.0s-4.0s |
| Major transitions | 4.0s-5.5s |

---

## Section Header Template

```xml
<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- SECTION: [SECTION_NAME] -->
<!-- Duration: [X] minutes | Pitch: [X]st | Purpose: [PURPOSE] -->
<!-- ═══════════════════════════════════════════════════════════════ -->

<prosody rate="1.0" pitch="[X]st">
    [Content...]
</prosody>
<break time="[X]s"/>
```

---

## Sound Effect Markers

Place SFX cues on their own lines in `script_production.ssml`:

```
[SFX: Deep ceremonial bell tone, resonant, 4 seconds with natural decay]

<prosody rate="1.0" pitch="-2st">
  The sound fades into silence...
</prosody>
```

**Important**: SFX markers are stripped out for `script_voice_clean.ssml` before TTS generation.

---

## Two-File System

| File | Purpose | Contains SFX? |
|------|---------|---------------|
| `script_production.ssml` | Full production script | Yes |
| `script_voice_clean.ssml` | TTS-ready script | No |

**Workflow**:
1. Write `script_production.ssml` with all SFX markers
2. Generate `script_voice_clean.ssml` by stripping `[SFX:...]` lines
3. Feed `script_voice_clean.ssml` to TTS

---

## Section Duration Targets

| Section | Target Duration | Word Count (~150 WPM) |
|---------|-----------------|----------------------|
| Pre-Talk | 2-3 min | 300-450 words |
| Induction | 4-5 min | 600-750 words |
| Deepening | 3-4 min | 450-600 words |
| Journey | 10-14 min | 1500-2100 words |
| Helm (Deepest) | 2-3 min | 300-450 words |
| Integration | 2-3 min | 300-450 words |
| Emergence | 2-3 min | 300-450 words |
| **Total (25 min)** | | ~3,750 words |

---

## SSML Validation

Before TTS generation, always validate:

```bash
python3 scripts/utilities/validate_ssml.py sessions/{session}/working_files/script.ssml
```

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Unclosed tag" | Missing `</prosody>` | Add closing tag |
| "Invalid break time" | `time="2"` (missing unit) | Use `time="2s"` |
| "Rate outside range" | `rate="2.5"` | Keep 0.5-2.0 |
| "Unknown SSML tag" | Using `<emphasis>` wrong | Check supported tags |

---

## Integration with Tier 1

All SSML content must follow Tier 1 rules:

| Tier 1 Skill | SSML Requirement |
|--------------|------------------|
| `hypnotic-language/validation/forbidden-patterns.md` | No forbidden phrases |
| `hypnotic-language/emergence/reorientation.md` | Complete emergence sequence |
| `symbolic-mapping/theological-filters/` | Christian-safe imagery only |

---

## Command Reference

### Generate Script
```bash
/generate-script {session}
```

### Strip SFX for TTS
```bash
grep -v "^\[SFX:" script_production.ssml > script_voice_clean.ssml
```

### Validate
```bash
python3 scripts/utilities/validate_ssml.py sessions/{session}/working_files/script.ssml
```

---

## Output Files

| File | Location |
|------|----------|
| Production script | `sessions/{session}/working_files/script_production.ssml` |
| Voice-clean script | `sessions/{session}/working_files/script_voice_clean.ssml` |

---

## Related Resources

- **Skill**: `tier1-neural-core/hypnotic-language/` (language patterns)
- **Serena Memory**: `script_production_workflow`
- **Serena Memory**: `voice_pacing_guidelines`
- **Doc**: `prompts/hypnotic_dreamweaving_instructions.md`
