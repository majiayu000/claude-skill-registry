---
name: Accessibility and UX
description: This skill should be used when the user asks about "accessibility", "control scheme", "controller mapping", "difficulty options", "colorblind", "UI design", "UX", "user experience", "menu design", "information hierarchy", "readable text", "controller remapping", or needs to make their game more accessible and user-friendly.
version: 1.0.0
---

# Accessibility and UX

Practical frameworks for controller-based games that more people can play and enjoy.

## Core Principle: Accessibility is Design

Accessibility isn't extra work—it's good design. Features that help disabled players often improve experience for everyone.

---

## Controller Design

### Button Mapping Principles

| Principle | Example |
|-----------|---------|
| Primary actions on face buttons | Jump = A, Attack = X |
| Modifiers on shoulders | Sprint = L1, Aim = L2 |
| Menu on Start/Options | Pause, inventory |
| Movement on left stick | Always |
| Camera on right stick | When applicable |

### Controller Template

```
CONTROLLER LAYOUT

LEFT                    RIGHT
L2: _________          R2: _________
L1: _________          R1: _________

D-Pad:                 Face:
  Up: _______            Y: _______
  Down: _____            A: _______
  Left: _____            B: _______
  Right: ____            X: _______

Left Stick: _______    Right Stick: _______
L3 (click): _______    R3 (click): _______

Start: _______         Select: _______
```

### Remapping Checklist

- [ ] All buttons remappable
- [ ] Presets available (e.g., "lefty," "one-handed")
- [ ] Settings saved per profile
- [ ] Preview before confirming

---

## Difficulty Options

### Difficulty Spectrum

| Approach | Description | Accessibility |
|----------|-------------|---------------|
| Single difficulty | One experience | Low |
| Presets | Easy/Normal/Hard | Medium |
| Granular options | Individual sliders | High |
| Assist modes | Specific helpers | Very High |

### Granular Options Template

| Option | Range | Default |
|--------|-------|---------|
| Damage taken | 50-200% | 100% |
| Damage dealt | 50-200% | 100% |
| Enemy aggression | Low-High | Normal |
| Timing windows | Generous-Strict | Normal |
| Auto-aim strength | Off-Strong | Light |

### Assist Modes

| Assist | Helps With | Implementation |
|--------|------------|----------------|
| Invincibility | Can't die | No damage taken |
| Skip encounter | Stuck on fight | Button to bypass |
| Auto-complete QTE | Reaction time | Always succeeds |
| Increased coyote time | Precision | More forgiving jumps |
| Contrast mode | Visibility | High contrast colors |

---

## Visual Accessibility

### Colorblind Modes

| Type | Population | Solution |
|------|------------|----------|
| Protanopia (red) | ~1% male | Avoid red/green distinction |
| Deuteranopia (green) | ~6% male | Avoid red/green distinction |
| Tritanopia (blue) | ~0.01% | Avoid blue/yellow distinction |

### Solutions

- [ ] Multiple colorblind presets
- [ ] Shapes/patterns in addition to colors
- [ ] Text labels on colored elements
- [ ] Customizable UI colors

### Text Readability

| Element | Minimum | Recommended |
|---------|---------|-------------|
| Body text | 18pt | 24pt |
| Headers | 24pt | 32pt |
| HUD elements | 20pt | 28pt |
| Contrast ratio | 4.5:1 | 7:1 |

---

## Audio Accessibility

### Subtitles and Captions

| Feature | Description |
|---------|-------------|
| Subtitles | Dialogue text |
| Closed captions | All audio described |
| Speaker names | Who is speaking |
| Direction indicators | Where sound comes from |

### Audio Options

- [ ] Separate volume: Master, Music, SFX, Voice
- [ ] Mono audio option
- [ ] Visual cues for important sounds
- [ ] Haptic feedback for audio events

---

## Motor Accessibility

### One-Handed Play

- [ ] All actions possible with one hand
- [ ] OR alternative control scheme for one-handed
- [ ] No simultaneous button requirements

### Reduced Input

- [ ] Hold instead of mash
- [ ] Auto-run option
- [ ] Simplified combo inputs
- [ ] Toggle vs hold options

---

## Information Design

### HUD Hierarchy

```
CRITICAL (always visible)
├── Health
├── Current objective
└── Immediate threats

IMPORTANT (visible when relevant)
├── Resources
├── Minimap
└── Active effects

OPTIONAL (toggle or menu)
├── Detailed stats
├── Quest log
└── Full map
```

### Information Checklist

- [ ] Most important info most visible
- [ ] Redundant cues (audio + visual)
- [ ] Nothing purely color-dependent
- [ ] Font is readable at all sizes
- [ ] UI scales with resolution

---

## Menu Design

### Menu Navigation

| Best Practice | Reason |
|---------------|--------|
| D-pad navigation | Precise, accessible |
| Clear current selection | Know where you are |
| Back button always works | Easy escape |
| Confirm = A/X | Convention |
| Cancel = B/Circle | Convention |

### Settings Checklist

- [ ] Accessible from pause menu
- [ ] Changes apply immediately (or preview)
- [ ] Reset to defaults available
- [ ] Settings persist across sessions

---

## Quick Accessibility Audit

### Must Have
- [ ] Remappable controls
- [ ] Subtitle option
- [ ] Multiple difficulty levels
- [ ] Pause during gameplay

### Should Have
- [ ] Colorblind modes
- [ ] Scalable UI/text
- [ ] Separate volume controls
- [ ] Control scheme presets

### Nice to Have
- [ ] Full assist mode
- [ ] One-handed mode
- [ ] High contrast mode
- [ ] Screen reader support

---

## Additional Resources

### Reference Files

- **`references/controller-mapping.md`** — Detailed controller templates
- **`references/difficulty-options.md`** — Granular difficulty design
- **`references/accessibility-checklist.md`** — Full audit checklist

### Related Skills

- **`player-psychology`** — Understanding player needs
- **`game-balance`** — Difficulty design
