---
name: ux-design-principles
description: Cognitive psychology principles for UX design decisions. Use when planning features, structuring interfaces, reducing complexity, or optimizing user journeys. Covers choice architecture, cognitive load, attention, and experience design. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Design Principles Skill

Psychological principles that guide design DECISIONS. For implementation patterns (colors, spacing, animations), see the corresponding ux-* skills.

## Choice Architecture

### Hick's Law: Decision Time

Decision time increases with the number and complexity of choices.

**Do:**
- Reduce options when quick decisions matter
- Break complex tasks into smaller steps
- Highlight recommended or default options
- Use progressive disclosure for advanced features

**Don't:**
- Present all options at once without guidance
- Oversimplify until purpose becomes unclear

### Choice Overload

Too many choices overwhelm and paralyze.

**Do:**
- Limit options when quick decisions are important
- Provide comparison tools (e.g., side-by-side pricing)
- Prioritize content and offer filters to narrow choices

**Don't:**
- Present all possible options at once
- Force users through large unfiltered selection lists

### Serial Position Effect

Items at the beginning and end of lists are remembered best.

**Do:**
- Place critical actions at the start or end of navigation
- Put key information first and last in lists

**Don't:**
- Bury important actions in the middle of menus
- Give equal prominence to all items

## Cognitive Load

### Cognitive Load Principle

Reduce information users must hold in working memory.

**Do:**
- Remove distracting elements that don't help task completion
- Distinguish essential information from nice-to-have
- Break complex information into digestible chunks

**Don't:**
- Present excessive details or decorative clutter
- Mix intrinsic complexity with unnecessary extraneous load

*Implementation: See ux-spacing-layout for visual chunking patterns.*

### Law of Pragnanz (Simplicity)

People interpret complex images in the simplest form possible.

**Do:**
- Present information in simple, ordered forms
- Reduce visual complexity to aid comprehension

**Don't:**
- Overwhelm users with ambiguous or complex graphics
- Create layouts that require mental effort to parse

### Tesler's Law (Conservation of Complexity)

Every process has irreducible complexity that must be handled somewhere.

**Do:**
- Handle inherent complexity in design/development, not on users
- Provide context-aware guidance within the interface
- Accept that users are not always rational

**Don't:**
- Push system complexity onto users
- Build only for idealized, rational behavior

### Occam's Razor

Simplest solution is usually best.

**Do:**
- Eliminate unnecessary elements while maintaining function
- Continually refine until nothing can be removed without harm

**Don't:**
- Add features that complicate without clear user benefit
- Solve simple problems with elaborate solutions

## Attention & Perception

### Selective Attention

Users naturally filter out irrelevant content.

**Do:**
- Guide attention to relevant information
- Minimize distractions
- Ensure only one significant change occurs at a time

**Don't:**
- Style important content like advertisements (banner blindness)
- Introduce multiple simultaneous changes without cues
- Place essential info in areas typically ignored (ad zones)

### Von Restorff Effect (Isolation)

Distinctive items are remembered better.

**Do:**
- Make important actions visually stand out
- Use emphasis sparingly so items don't compete
- Provide multiple contrast cues (shape, pattern, not just color)

**Don't:**
- Rely exclusively on color to convey importance
- Overuse emphasis (dilutes impact)
- Use motion effects that trigger discomfort

*Implementation: See ux-color-system for emphasis patterns.*

## User Expectations

### Jakob's Law

Users transfer expectations from familiar products.

**Do:**
- Design consistent with patterns users already know
- Leverage existing mental models
- When making major changes, offer temporary familiar alternatives

**Don't:**
- Radically alter established interactions without guidance
- Force users to relearn common patterns

### Paradox of the Active User

Users jump into products without reading instructions.

**Do:**
- Expect users to start using immediately
- Provide contextual help, tooltips, and guidance in-place

**Don't:**
- Force users to read manuals before using
- Hide help or make it difficult to find

### Aesthetic-Usability Effect

Beautiful design is perceived as more usable.

**Do:**
- Design interfaces that look appealing and polished
- Use aesthetics to create positive first impressions

**Don't:**
- Rely on visual polish to hide fundamental usability problems
- Assume beauty compensates for broken functionality

## Progress & Motivation

### Goal-Gradient Effect

People work faster as they sense completion is near.

**Do:**
- Display progress toward goals
- Provide "artificial progress" (e.g., start at 10% complete)

**Don't:**
- Leave users unsure how far they've progressed
- Hide progress information

*Implementation: See ux-feedback-patterns for progress indicator patterns.*

### Zeigarnik Effect

Incomplete tasks stay in memory and motivate continuation.

**Do:**
- Clearly signify that more content/steps are available
- Provide artificial progress toward goals
- Show progress indicators

**Don't:**
- Leave tasks without visible progress indicators
- Hide future steps or content

*Implementation: See ux-feedback-patterns for progress patterns.*

### Parkinson's Law

Tasks expand to fill available time.

**Do:**
- Set clear, reasonable time expectations
- Reduce task duration below what users expect
- Use time-saving features (autofill, shortcuts)

**Don't:**
- Allow simple processes to take longer than necessary
- Present long forms without automation

*Implementation: See ux-form-design for autofill patterns.*

## Experience Design

### Peak-End Rule

Experiences are judged by peak moments and endings.

**Do:**
- Design memorable peaks and strong endings
- Identify when your product is most helpful and add delight
- Minimize negative peaks (bad moments are remembered vividly)

**Don't:**
- Neglect the conclusion of user journeys
- Leave negative events unaddressed

### Pareto Principle (80/20)

A small number of causes produce majority of outcomes.

**Do:**
- Identify and focus on high-impact areas
- Allocate resources where they benefit most users

**Don't:**
- Distribute efforts evenly across all tasks
- Over-invest in low-impact areas

## Input & Error Handling

### Postel's Law (Robustness)

Be tolerant of input, strict in output.

**Do:**
- Anticipate various user inputs and behaviors
- Translate diverse input to meet system requirements
- Provide clear feedback for edge cases

**Don't:**
- Rigidly enforce narrow input formats
- Send malformed or ambiguous output

*Implementation: See ux-form-design for validation patterns.*

## Cognitive Bias Awareness

### Cognitive Bias Principle

Mental shortcuts influence decision making.

**Do:**
- Recognize that heuristics save mental effort but can skew judgment
- Raise awareness of your own biases during design
- Challenge assumptions with your team

**Don't:**
- Ignore biases like confirmation bias
- Seek only information supporting preconceived beliefs

## Quick Reference Matrix

| Situation | Apply |
|-----------|-------|
| Too many options | Hick's Law, Choice Overload |
| Complex task | Tesler's Law, Cognitive Load |
| Users skip instructions | Paradox of Active User |
| Low completion rates | Goal-Gradient, Zeigarnik |
| Poor first impressions | Aesthetic-Usability |
| Users confused by changes | Jakob's Law |
| Important items ignored | Serial Position, Selective Attention |
| Long task times | Parkinson's Law |
| Poor memories of experience | Peak-End Rule |
| Resource allocation | Pareto Principle |
| Input validation issues | Postel's Law |
| Overly complex design | Occam's Razor, Pragnanz |

## Related Skills

- **ux-spacing-layout**: Visual chunking, grouping (Law of Proximity/Common Region)
- **ux-color-system**: Emphasis, similarity (Von Restorff, Law of Similarity)
- **ux-animation-motion**: Response timing (Doherty Threshold)
- **ux-accessibility**: Touch targets, focus (Fitts's Law)
- **ux-feedback-patterns**: Progress, loading states (Working Memory)
- **ux-user-flow**: Navigation, mental models (Flow)
- **ux-form-design**: Input tolerance, validation (Postel's Law)
