---
name: storyboard-generator
description: Create detailed storyboards from ad scripts with 2-4 second elements, B-roll specs, and AI generation prompts. Use when preparing scripts for editors, planning video shoots, or generating production-ready creative specs.
---

# Storyboard Generator

Convert scripts into clip-by-clip production instructions.

## Process

### Step 1: Take Script Input

Accept complete script with: hook, body sections, CTA, target length.

### Step 2: Break Into 2-4 Second Elements

Each element is a discrete visual moment:
- No element shorter than 2 seconds
- No element longer than 4 seconds
- Multiple cuts within elements OK
- Match timing to VO/action

### Step 3: Specify Per Element

**Visual Description**
- What's on screen
- Camera angle/movement
- Framing (wide/medium/close)

**B-Roll Source**
- Stock footage keywords
- Existing footage reference
- UGC needed
- Product shot needed

**Text Overlays**
- On-screen text
- Font/style notes
- Animation (none/fade/pop)

**AI Generation Prompts** (for Sora/Cling/HigsField)
- Full prompt for AI video generation
- Style references
- Movement description

### Step 4: Add Technical Notes

- Transitions between elements
- Music cues
- Sound effects
- Pacing notes

### Step 5: Output Storyboard

```
## STORYBOARD: [Script Name]
Total Length: [Xs] | Elements: [#]

---

### ELEMENT 1 (0:00-0:03)
**VO/Audio:** "[Exact words or sound]"
**Visual:** [Description]
**Shot Type:** [Wide/Medium/Close]
**Source:** [Stock/AI/Shoot/UGC]

**If Stock:** Keywords: [search terms]
**If AI:** Prompt: "[Full generation prompt]"
**If Shoot:** Notes: [What to capture]

**Text Overlay:** "[On-screen text]"
**Transition to next:** [Cut/Dissolve/None]

---

### ELEMENT 2 (0:03-0:06)
**VO/Audio:** "[Exact words]"
**Visual:** [Description]
...

---

### PRODUCTION NOTES
**Music:** [Style/mood/BPM]
**Pacing:** [Fast cuts/Slow/Mixed]
**Color:** [Warm/Cool/Natural]
**Style:** [UGC native/Polished/News-style]

### AI TOOLS RECOMMENDED
- Video gen: [Sora/Cling/HigsField]
- Image edit: [Nano Banana]
- Voice: [11 Labs]

### ASSETS NEEDED
- [ ] Product shots: [List]
- [ ] Stock footage: [List]
- [ ] AI generations: [List]
- [ ] UGC clips: [List]
```

## AI Generation Tips (VISCAP)

**For Stock Replacement:**
- Use Sora 2 for simple UGC-style clips
- Text-to-video works for basic B-roll
- Include "shot on iPhone" in prompts for native feel

**For Impossible Shots:**
- Image-to-video with reference image
- JSON prompting for complex scenes
- Cling O1 Edit for product placement

**For Scientific/Product Animations:**
- AI excels at 3D scientific animations
- Product beauty shots work well
- Stylized/non-realistic clips for hooks

## Platform-Specific Notes

**TikTok/Reels:** Fast cuts (1.5-2s), vertical, native feel
**Facebook Feed:** Can be slower, square or vertical
**YouTube:** Can breathe more, horizontal OK
**Native Ads:** Minimal cuts, straightforward

Source: VISCAP AI Framework
