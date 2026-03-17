---
name: ux-sound-design
description: "Create functional and emotionally resonant audio for digital products using Audio UX methodology—from notification sounds to complete sonic systems. Use when: Designing notification sounds for an app; Creating a complete audio system for a digital product; Adding audio feedback to UI interactions; Building accessible audio cues; Defining audio guidelines for product teams"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# UX Sound Design

> Create functional and emotionally resonant audio for digital products using Audio UX methodology—from notification sounds to complete sonic systems.

## When to Use This Skill

- Designing notification sounds for an app
- Creating a complete audio system for a digital product
- Adding audio feedback to UI interactions
- Building accessible audio cues
- Defining audio guidelines for product teams
- Evaluating and improving existing product sounds

## Methodology Foundation

**Source**: Audio UX + Design Thinking Principles

**Core Principle**: "Audio UX is the strategic and intentional use of sound to enhance the user experience." Unlike music or entertainment audio, UX sound design serves a function first. The best product sounds are invisible when working correctly and noticeable only when something needs attention.

**Why This Matters**: Sound is the most underutilized tool in digital product design. Research shows audio feedback improves task completion, reduces errors, and creates stronger brand associations. Yet most products either ignore sound entirely or use generic, forgettable audio.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Designs functional audio cues** - Sounds that communicate status, confirmation, and errors
2. **Creates emotional connections** - Audio that reinforces brand personality
3. **Builds audio systems** - Coherent families of related sounds
4. **Ensures accessibility** - Audio for users with visual impairments
5. **Documents audio guidelines** - Specifications for consistent implementation

## How to Use

### Design Product Sounds
```
Help me design audio for [product/feature].
Interaction: [what the user does]
Feedback needed: [what the sound should communicate]
Brand personality: [tone/feeling]
```

### Create Audio System
```
Create an audio system for [app/product].
Key interactions: [list]
Brand: [personality traits]
Constraints: [technical limitations]
```

### Review Existing Audio
```
Review these product sounds for UX effectiveness:
[describe current sounds]
Issues: [problems you've noticed]
```

## Instructions

When designing UX sounds, follow this methodology:

### Step 1: Understand the Function Categories

Every product sound serves one of these purposes.

```
## UX Sound Categories

### 1. FEEDBACK SOUNDS
Confirm that an action was registered.

| Type | Purpose | Example |
|------|---------|---------|
| Confirmation | Action completed | Send button click |
| Progress | Something is happening | Upload progress |
| Success | Task finished successfully | Payment confirmed |
| Error | Something went wrong | Form validation error |
| Warning | Attention needed | Low battery |

### 2. NOTIFICATION SOUNDS
Alert user to external events.

| Type | Purpose | Example |
|------|---------|---------|
| Alert | Immediate attention | New message |
| Reminder | Scheduled prompt | Calendar event |
| Update | Information available | Download complete |
| Social | Human interaction | Someone liked your post |

### 3. NAVIGATION SOUNDS
Spatial orientation and movement.

| Type | Purpose | Example |
|------|---------|---------|
| Transition | Moving between views | Screen change |
| Selection | Choosing an option | Menu item hover |
| Boundary | End of scrollable content | List bottom reached |

### 4. AMBIENT/BACKGROUND
Context and mood.

| Type | Purpose | Example |
|------|---------|---------|
| Presence | App is running | Subtle background tone |
| Mode | Current state | Focus mode active |
| Celebration | Achievement | Goal reached |
```

---

### Step 2: Apply Design Principles

Core principles for effective UX audio.

```
## UX Sound Design Principles

### 1. FUNCTION FIRST
- Sound must communicate something useful
- Ask: "What information does this convey?"
- If no clear function, consider no sound

### 2. DISTINCT BUT RELATED
- Each sound should be recognizably different
- All sounds should feel like a family
- Use consistent:
  - Tonal palette (key/scale)
  - Timbral characteristics
  - Duration ranges
  - Dynamic levels

### 3. APPROPRIATE URGENCY
- Match sound urgency to message urgency
- Error ≠ always alarming
- Success ≠ always celebratory
- Scale:
  1. Subtle acknowledgment
  2. Gentle notification
  3. Attention-getting alert
  4. Urgent alarm

### 4. CONTEXT AWARE
- Consider when/where users hear this
- Public spaces: shorter, more subtle
- Private: can be more expressive
- Frequency: often-heard sounds must be less intrusive

### 5. ACCESSIBLE
- Don't rely solely on sound
- Always pair with visual feedback
- Consider frequency range (avoid only high frequencies)
- Ensure distinctiveness for users who can't see visual cues

### 6. CONTROLLABLE
- Users must be able to mute/adjust
- Provide volume controls
- Respect system settings
- Never surprise with unexpected sound
```

---

### Step 3: Create the Sound Palette

Define the raw materials for your audio system.

```
## Sound Palette Development

### Step 3.1: Define Brand Sound Attributes

Translate brand personality into audio terms:

| Brand Attribute | Sound Translation |
|-----------------|-------------------|
| Playful | Bouncy, melodic, varied pitch |
| Professional | Clean, precise, consonant |
| Innovative | Modern synthesis, unique timbres |
| Warm | Rounded, organic, mid-range |
| Energetic | Fast attack, bright, rhythmic |
| Calm | Soft attack, slow decay, filtered |

### Step 3.2: Choose Your Palette Elements

**Tonal Center**
- Pick a key (e.g., C major, F major)
- All sounds should relate to this key
- Create harmonic cohesion

**Timbre Family**
- Acoustic (piano, bells, wood)
- Synthetic (sine, FM, wavetable)
- Hybrid (processed acoustic)
- Choose based on brand

**Duration Range**
- Micro: 50-150ms (feedback)
- Short: 150-500ms (notifications)
- Medium: 500-1500ms (transitions)
- Long: 1500ms+ (celebrations)

**Dynamic Range**
- Define min/max volume levels
- Relative loudness between sound types
- Error > Notification > Feedback (typically)

### Step 3.3: Document the Palette

```markdown
## [Product] Sound Palette

**Tonal Center**: F major
**Character**: Warm, professional, approachable

**Primary Timbre**: Rounded sine with subtle harmonics
**Secondary Timbre**: Soft mallet (marimba-like)
**Accent Timbre**: Clean bell tone

**Durations**:
- Feedback: 80-120ms
- Notification: 200-400ms
- Transition: 300-600ms
- Celebration: 800-1500ms

**Loudness Hierarchy** (relative to baseline):
1. Alerts: +3dB
2. Notifications: 0dB (baseline)
3. Feedback: -6dB
4. Ambient: -12dB
```
```

---

### Step 4: Design Individual Sounds

Process for creating each sound.

```
## Sound Design Process

### For Each Sound:

**1. Define the Function**
- What exactly does this communicate?
- What action triggered it?
- What should user understand?

**2. Determine Urgency Level**
- 1 (subtle) → 5 (urgent)
- This affects: loudness, duration, pitch, complexity

**3. Consider Context**
- How often is it heard?
- Where is user when hearing it?
- What's user's emotional state?

**4. Design Parameters**

| Parameter | Low Urgency | High Urgency |
|-----------|-------------|--------------|
| Duration | Shorter | Longer |
| Attack | Soft | Sharp |
| Pitch | Neutral | Higher or dissonant |
| Complexity | Simple | More layers |
| Volume | Quieter | Louder |

**5. Create Variations**
- Design 3-5 options
- Test in context
- Get user feedback
- Iterate

### Common Patterns

**Confirmation/Success**:
- Rising pitch (positive)
- Clean, resolved harmony
- Quick, satisfying
- Example: Two notes ascending a third

**Error/Warning**:
- Falling or dissonant
- More complex/harsh
- Attention-getting but not alarming
- Example: Minor second interval, longer duration

**Notification**:
- Distinct melodic motif
- Balanced urgency
- Memorable but not annoying
- Example: 3-4 note sequence
```

---

### Step 5: Build the System

Create a coherent family of related sounds.

```
## Audio System Architecture

### Core Sound Set (Minimum Viable)

1. **Generic feedback** - Neutral acknowledgment
2. **Success** - Positive confirmation
3. **Error** - Something went wrong
4. **Notification** - New information
5. **Alert** - Requires attention

### Extended Sound Set

**Feedback family**:
- Tap/click (lightest)
- Selection
- Confirmation
- Success (fullest)

**Notification family**:
- Subtle update
- Standard notification
- Message received
- Urgent alert

**Navigation family**:
- Transition in
- Transition out
- Boundary reached
- Mode change

### Sound Relationships

```
         QUIET ←───────────────────→ LOUD

    Feedback    Notification    Alert    Alarm
      ○            ●             ◉        ◎

         SUBTLE ←────────────────→ URGENT
```

### Variation Strategy

For each core sound, create:
- Standard version
- Subtle version (-6dB, shorter)
- Emphasized version (+3dB, fuller)
- This allows contextual flexibility
```

---

### Step 6: Document and Deliver

Specifications for implementation.

```
## Audio Guidelines Document

### Overview
[Product] uses sound to enhance user experience through
clear feedback, gentle notifications, and brand presence.

### Sound Files

| Sound Name | File | Duration | Usage |
|------------|------|----------|-------|
| feedback_tap | tap.wav | 80ms | Button presses |
| feedback_success | success.wav | 250ms | Completed actions |
| feedback_error | error.wav | 350ms | Validation errors |
| notif_message | message.wav | 400ms | New messages |
| notif_alert | alert.wav | 600ms | Important updates |

### Implementation Guidelines

**When to Play**:
- Play sounds AFTER visual feedback, not before
- Never play sounds on page load
- Respect system mute settings
- Throttle rapid-fire triggers (max 1 per 100ms)

**Volume Control**:
- All sounds respect master volume
- Users can disable sound in settings
- Haptic feedback should accompany (mobile)

**Accessibility**:
- Every sound has visual equivalent
- Screen reader announcements pair with audio
- Don't rely on sound alone for critical info

### File Specifications

- Format: WAV (for development), MP3/AAC (production)
- Sample rate: 44.1kHz
- Bit depth: 16-bit minimum
- Channels: Mono (reduces file size, consistent playback)
- Peak level: -1dB (avoid clipping)
```

## Examples

### Example 1: Mobile App Notification System

**Context**: Designing sounds for a productivity app.

**Input**:
> Help me design an audio system for a task management app. Key moments: task created, task completed, reminder, all tasks done for the day. Brand is calm, focused, professional.

**Output**:

## Task App Audio System

### Brand Sound Translation

**Brand attributes**: Calm, focused, professional
**Sound translation**:
- Calm → Soft attacks, rounded tones, major/neutral harmony
- Focused → Clean, uncluttered, single-element sounds
- Professional → Refined, not playful, no novelty sounds

### Sound Palette

**Tonal Center**: C major (neutral, universal)
**Primary Timbre**: Soft mallet/vibraphone character
**Duration Range**: 100ms - 800ms
**Character**: Clear, wood-like resonance with gentle decay

### Sound Designs

**1. Task Created** (feedback_subtle)
- Function: Confirm task was added
- Urgency: 1/5 (subtle)
- Design: Single mallet note (G4), soft attack, 120ms
- Feeling: Gentle acknowledgment, like a soft "got it"

**2. Task Completed** (feedback_success)
- Function: Celebrate completion, reward action
- Urgency: 2/5 (satisfying but not disruptive)
- Design: Two notes ascending (C4 → E4), 250ms total
- Feeling: Positive, forward momentum, clean resolution

**3. Reminder** (notification_standard)
- Function: Alert user to scheduled reminder
- Urgency: 3/5 (needs attention but not alarming)
- Design: Three-note melodic pattern (G4 → C5 → E5), 400ms
- Feeling: Friendly tap on shoulder, "hey, don't forget"

**4. All Tasks Complete** (celebration)
- Function: Reward daily completion
- Urgency: 2/5 (celebratory but not over the top)
- Design: Ascending arpeggio (C4 → E4 → G4 → C5), 800ms
- With subtle reverb tail for satisfaction
- Feeling: Achievement unlocked, day well done

### Audio Guidelines

```yaml
Sound System: TaskFlow v1.0

Palette:
  tonal_center: C_major
  timbre: mallet_vibraphone
  character: calm_professional

Sounds:
  - name: task_created
    file: sounds/task_created.wav
    duration_ms: 120
    trigger: task.create
    volume: -9dB (relative)

  - name: task_completed
    file: sounds/task_completed.wav
    duration_ms: 250
    trigger: task.complete
    volume: -6dB (relative)

  - name: reminder
    file: sounds/reminder.wav
    duration_ms: 400
    trigger: reminder.fire
    volume: 0dB (baseline)

  - name: daily_complete
    file: sounds/daily_complete.wav
    duration_ms: 800
    trigger: tasks.all_complete
    volume: 0dB (baseline)

Rules:
  - Respect system mute
  - Pair all sounds with haptic (mobile)
  - Throttle: max 1 sound per 200ms
  - No sound on app open
```

---

### Example 2: E-commerce Checkout Sounds

**Context**: Adding audio feedback to checkout flow.

**Input**:
> Design sounds for an e-commerce checkout: add to cart, remove from cart, apply coupon, payment processing, purchase complete. Brand is modern, trustworthy, slightly playful.

**Output**:

## E-commerce Checkout Audio

### Brand Sound Translation

**Modern**: Clean synthesis, not acoustic
**Trustworthy**: Consonant, resolved, stable
**Slightly playful**: Small melodic interest, not sterile

### Sound Palette

**Tonal Center**: F major (warm, friendly)
**Timbre**: Rounded digital tones, slight shimmer
**Character**: Friendly but professional, like a good salesperson

### Sound Designs

**Add to Cart** ✚
- Function: Confirm item added
- Frequency: High (many per session)
- Design: Quick upward pitch sweep + soft "pop" (100ms)
- Very light, satisfying, not attention-grabbing
- Like dropping something into a soft bag

**Remove from Cart** ✕
- Function: Confirm removal
- Design: Inverse of add—short downward sweep (80ms)
- Neutral, not negative (removing isn't bad)
- Quieter than add (-3dB)

**Coupon Applied** 🎟️
- Function: Reward, confirmation of savings
- Design: Small celebratory motif (C5 → A5 → F5), 200ms
- Sparkle element—feels like found money
- Distinct from regular feedback

**Payment Processing** ⏳
- Function: Indicate activity, reduce anxiety
- Design: Subtle pulsing tone, loopable
- Calm, confident, "things are happening"
- Volume very low, background presence

**Purchase Complete** 🎉
- Function: Major success moment, emotional peak
- Design: Triumphant arpeggio with sustained chord (1000ms)
- The biggest sound in the system
- Triggers genuine satisfaction response
- Pairs with visual celebration

### Implementation Notes

```javascript
// Sound trigger logic

// Add to cart - play immediately on success
cartAPI.add(item).then(() => {
  playSound('cart_add', { volume: 0.4 });
  // Throttle: won't play again within 150ms
});

// Purchase complete - play after visual confirmation
if (purchaseSuccess) {
  // Short delay so visual leads
  setTimeout(() => {
    playSound('purchase_complete', { volume: 0.8 });
  }, 200);
}

// Processing - loop while waiting
const processingSound = playSound('processing', {
  loop: true,
  volume: 0.2
});
// Stop when complete
paymentAPI.process().finally(() => {
  processingSound.stop();
});
```

## Checklists & Templates

### UX Sound Audit Checklist

```
## Current State Assessment

□ What sounds exist currently?
□ Are they consistent (family feel)?
□ Do users complain about any sounds?
□ Are sounds controllable (mute option)?
□ Are visual alternatives provided?

## Function Check

□ Every sound serves a clear purpose
□ Users understand what each sound means
□ Urgency matches message importance
□ Frequency considered (annoying over time?)

## Brand Check

□ Sounds match brand personality
□ Sounds distinct from competitors
□ Consistent with visual design language
□ Appropriate for target audience

## Technical Check

□ Files optimized for platform
□ Plays reliably across devices
□ Respects system audio settings
□ No clipping or distortion
```

---

### Sound Design Specification Template

```
## Sound: [Name]

### Function
- Purpose:
- Trigger:
- User action that causes this:

### Context
- How often heard:
- User emotional state:
- Environment:

### Design
- Urgency level: _/5
- Duration: _ms
- Tonal content:
- Timbre description:

### Technical
- File: [filename.wav]
- Sample rate: 44.1kHz
- Channels: Mono
- Peak level: -1dB
- Relative volume:

### Relationships
- Replaces: [if replacing existing sound]
- Similar to: [related sounds in system]
- Distinct from: [sounds it must differ from]
```

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- Audio UX. "The Future of Sonic Branding" (Lippincott partnership)
- LANDR. "Audio UX Sound Design" - Practical methodology
- UX Collective. "How Sound Design Can Make Wonders with Your Brand"
- Apple Human Interface Guidelines - Sound design section
- Material Design - Sound in UI

## Related Skills

- [sonic-branding](../sonic-branding/) - Brand-level audio identity
- [audio-logo-design](../audio-logo-design/) - Creating sonic logos
- [sound-design-murch](../sound-design-murch/) - Film sound principles
- [voice-design](../voice-design/) - Voice interfaces

---

## Skill Metadata (Internal Use)

```yaml
name: ux-sound-design
category: audio
subcategory: sound-design
version: 1.0
author: MKTG Skills
source_expert: Audio UX
source_work: Audio UX Methodology
difficulty: intermediate
estimated_value: $2,000-10,000 per audio system (equivalent design work)
tags: [ux, sound-design, product, notifications, audio-feedback]
created: 2026-01-26
updated: 2026-01-26
```
