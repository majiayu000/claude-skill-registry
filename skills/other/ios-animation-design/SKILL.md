---
name: ios-animation-design
description: Design and plan iOS animations with structured specs covering transitions, micro-interactions, gesture-driven motion, and loading states. Use when the user asks to plan, design, or spec out animations for an iOS app — including screen transitions, navigation animations, interactive gestures, onboarding flows, or any motion design work. Also use when the user wants animation recommendations or wants to decide between animation approaches before writing code.
---

# iOS Animation Design

Plan animations that feel intentional, not decorative. Apple's HIG is clear: "Don't add motion for the sake of adding motion. Gratuitous or excessive animation can distract people and may make them feel disconnected or physically uncomfortable." Every animation must serve a purpose — guide attention, communicate state changes, reinforce spatial relationships, or provide feedback.

Before adding any custom animation, ask: does the system already handle this? Many system components include motion automatically — Liquid Glass (iOS 26) responds to touch with greater emphasis and produces more subdued effects for trackpad interaction. Standard controls, navigation transitions, and sheets already animate. Custom motion should fill gaps the system doesn't cover, not replace what it already does well.

## Design Process

### Gates (sequenced)

Advance only after each pass condition is met in the working artifact (chat or doc). Do not rationalize compliance without evidence.

1. **Gate — Context captured** — **Pass when** there are written answers for: what triggers the motion, its purpose, where it lives in the app, how often it runs, minimum iOS version, and primary input methods (or explicit **N/A** where not applicable). **Pass when** you have stated whether system-provided motion already covers this or which gap custom animation fills.
2. **Gate — Options differ meaningfully** — **Pass when** there are 2–3 approaches and each differs in **at least two** of: named API/technique, motion character, complexity band, or iOS floor — not minor timing tweaks of the same idea.
3. **Gate — Spec is implementation-ready** — **Pass when** the compiled spec includes concrete entries for **Trigger**, **Interruption** (cancel/reverse/queue), **Reduce Motion** fallback, **Haptics** (or explicit none with rationale), and **Recommended API**.

### Step 1: Understand the Animation Context

Before proposing options, gather context about what needs to animate and why:

- **What triggers it?** User action (tap, swipe, drag), state change (data loaded, error), or lifecycle event (appear, disappear)?
- **What's the purpose?** Feedback, spatial orientation, content transition, delight, or status communication?
- **Where in the app?** Navigation flow, in-screen state change, overlay/modal, or background ambient?
- **How frequent?** Once per session (onboarding), every interaction (tab switch), or continuous (progress indicator)? Apple's HIG warns: "In apps, generally avoid adding motion to UI interactions that occur frequently. The system already provides subtle animations for interactions with standard interface elements."
- **Deployment target?** Which iOS version floor determines available APIs.
- **Input methods?** Touch, trackpad, keyboard, VoiceOver? iOS 26's Liquid Glass adapts motion intensity based on input — direct touch gets more emphasis, indirect input is more subdued. Custom animations should follow the same principle.

### Step 2: Present 2-3 Animation Approaches

For each animation need, present 2-3 distinct approaches. Each option should feel meaningfully different — not minor variations of the same idea. Structure each option as:

```markdown
### Option [N]: [Name]

**Approach**: [1-2 sentences describing the motion design]
**Technique**: [Which Apple API — SwiftUI animation, KeyframeAnimator, matchedGeometryEffect, etc.]
**Character**: [How it feels — snappy, playful, elegant, subtle, dramatic]
**Complexity**: [Low / Medium / High — implementation and maintenance cost]
**iOS floor**: [Minimum iOS version required]
```

Then provide a **Recommendation** with rationale tied to the gathered context. The recommendation should consider:

- API availability relative to the deployment target
- Complexity budget — simpler is better unless the animation is a signature moment
- Whether the system already handles it — prefer system-provided motion over custom implementations
- Consistency with existing app motion language
- Cancellability — can users interrupt or skip it? ("Don't make people wait for an animation to complete before they can do anything" — Apple HIG)
- Accessibility (can it gracefully degrade with Reduce Motion?)
- Multimodal feedback — animation alone shouldn't be the only signal. "Supplement visual feedback by also using alternatives like haptics and audio" (Apple HIG)

### Step 3: Compile the Animation Spec

Once the user selects an approach (or confirms the recommendation), produce a structured spec. This spec is the contract between design and implementation — it should contain everything needed to write the code without ambiguity.

## Animation Spec Format

```markdown
# Animation Spec: [Name]

## Overview
[1-2 sentences: what this animation does and why it exists]

## Trigger
- **Event**: [What initiates the animation — tap, state change, appear, gesture, etc.]
- **Direction**: [Forward / Reverse / Bidirectional]

## Motion Design

### Properties
| Property | From | To | Curve | Duration |
|----------|------|----|-------|----------|
| opacity | 0 | 1 | .easeOut | 0.25s |
| scale | 0.8 | 1.0 | .spring(duration: 0.5, bounce: 0.3) | — |
| offset.y | 20 | 0 | .spring(duration: 0.5, bounce: 0.3) | — |

### Timing
- **Total duration**: [end-to-end time]
- **Stagger**: [if multiple elements, delay between each]
- **Interruption**: [What happens if triggered again mid-animation — cancel, reverse, queue]

### Gesture Binding (if interactive)
- **Gesture type**: [drag, long press, rotation, magnification]
- **Progress mapping**: [How gesture progress maps to animation progress]
- **Threshold**: [When the animation commits vs. cancels]
- **Velocity handling**: [How release velocity affects completion]

## Accessibility & Multimodal Feedback
- **Reduce Motion**: [What happens — crossfade, instant, simplified version]
- **VoiceOver**: [Any announcement needed for the state change]
- **Haptics**: [Which sensoryFeedback type pairs with this animation — .impact, .selection, .success, etc.]
- **Audio**: [Optional sound cue if the state change is important enough]
- **Dynamic Type**: [Does layout shift affect the animation?]

## Implementation Notes
- **Recommended API**: [SwiftUI withAnimation, KeyframeAnimator, PhaseAnimator, matchedGeometryEffect, UIViewPropertyAnimator, etc.]
- **State model**: [What @State/@Binding drives this animation]
- **Extractable component**: [Yes/No — should this be a reusable ViewModifier or View?]
```

## Animation Categories

When designing, think in terms of these categories. Each has different expectations for timing, easing, and purpose.

### Navigation & Scene Transitions
Screen-to-screen movement. Users expect spatial consistency — where did I come from, where am I going? These should feel fast and confident.

- Push/pop with hero elements (`matchedGeometryEffect`, `navigationTransition(.zoom)`)
- Full-screen covers and sheets (custom `Transition` protocol)
- Tab switches (crossfade, slide, or matched geometry)
- Onboarding flows (page-based with progressive reveal)

Timing: 0.3–0.5s. Easing: spring-based (`.snappy` or `.smooth`). Interruption: must handle back-gesture gracefully.

### Micro-Interactions
Small, immediate feedback for user actions. Apple's HIG emphasizes brevity: "When animated feedback is brief and precise, it tends to feel lightweight and unobtrusive, and it can often convey information more effectively than prominent animation." These should be near-instant and never block interaction. For frequent interactions, strongly consider whether the system's built-in animation is sufficient before adding custom motion.

- Button press states (scale + haptic)
- Toggle/switch animations
- Like/favorite/bookmark responses
- Pull-to-refresh indicators
- Text field focus transitions
- Swipe action reveals

Timing: 0.1–0.3s. Easing: `.snappy` or `.spring(duration: 0.2, bounce: 0.4)`. Always pair with `sensoryFeedback` — haptics reinforce the visual feedback and communicate to users who can't see the animation.

### Content Transitions
When data changes within a view — numbers updating, content swapping, list reordering.

- Numeric text transitions (`.contentTransition(.numericText)`)
- Image crossfades
- List item insertion/removal
- Skeleton-to-content reveal
- Error/empty/loaded state switches

Timing: 0.2–0.35s. Easing: `.smooth` or `.easeInOut`. Use `animation(_:value:)` tied to the changing data.

### Gesture-Driven Animations
Interactive animations where the user directly controls progress. These need to feel physically connected to the finger — no lag, no disconnection.

- Card dismiss (swipe to remove)
- Drawer/sheet drag
- Pinch-to-zoom
- Rotation interactions
- Scroll-linked parallax (`scrollTransition`)

Spring-based completion is essential. Track velocity on release. Use `UIViewPropertyAnimator` for UIKit or `GestureState` + spring for SwiftUI.

### Loading & Progress
Communicate waiting and progress. Should feel alive without being distracting.

- Skeleton screens (shimmer with gradient mask)
- Indeterminate spinners (SF Symbol `.symbolEffect(.pulse)`)
- Determinate progress (animated bar/ring)
- Content placeholder pulse (`PhaseAnimator`)

Keep looping animations lightweight — they run continuously and must not drain battery or cause hitches.

### Ambient & Decorative
Background motion that establishes mood. Use sparingly — these are the easiest to overdo.

- Animated gradients (`MeshGradient` with timer-driven point shifts)
- Floating particle effects
- Subtle parallax on device tilt
- Background blur transitions

Always disable or simplify with Reduce Motion. These are the first to cut for performance.

## Principles

1. **Purpose over polish** — If you can't articulate why something animates, it shouldn't. Apple's HIG: "Don't add motion for the sake of adding motion."
2. **System first** — Many system components already include motion (Liquid Glass, navigation transitions, sheets, SF Symbol effects). Check whether the system handles it before designing custom motion. Custom animation should fill gaps, not duplicate the system.
3. **Brevity over spectacle** — "Aim for brevity and precision in feedback animations" (Apple HIG). Brief animations convey information more effectively than prominent ones. A succinct response tied to the action beats an elaborate sequence.
4. **Springs over curves** — Spring animations feel physical. Use `duration` + `bounce` parameters, not bezier curves, unless you have a specific reason.
5. **Reduce Motion is not optional** — Every animation spec must include a Reduce Motion fallback. Apple's HIG: "Make motion optional. Not everyone can or wants to experience the motion in your app." This also means never using animation as the only way to communicate important information.
6. **Multimodal feedback** — Supplement animation with haptics (`.sensoryFeedback`) and audio where appropriate. Animation alone shouldn't carry critical state changes.
7. **Cancellation is a right** — "Don't make people wait for an animation to complete before they can do anything, especially if they have to experience the animation more than once" (Apple HIG). Every animation must be interruptible.
8. **Realistic spatial feedback** — Motion should follow the user's gesture and expectations. If someone slides a view down, they expect to dismiss it by sliding down, not sideways. Feedback that defies spatial logic disorients people.
9. **Speed earns trust** — Animations under 0.3s feel responsive. Over 0.5s feels sluggish unless it's a signature moment. When in doubt, go faster.
10. **Consistency compounds** — Use the same spring parameters across similar interactions. A consistent motion language makes the whole app feel cohesive. Define a small set of timing presets and reuse them.
