---
name: user-empathy-lens
description: This skill should be used when the user mentions "user experience", "UX", "how would someone use this", "user flow", "onboarding", "confusing", "intuitive", "user needs", "persona", "user story", or when designing features that end-users interact with directly. Addresses understanding users through empathy and inference rather than formal research.
version: 1.0.0
---

# User Empathy Lens

Empathy-driven design skill. Helps think through how real people will experience the software. Uses inference and scenario-building rather than formal user research — surface assumptions, challenge them, and design for actual human behaviour.

---

## When This Skill Applies

Use this skill when:
- Designing a user-facing feature or flow
- Deciding between UX approaches
- Reviewing a feature from the user's perspective
- The conversation is focused on implementation but hasn't considered the user
- Building onboarding, error states, or edge-case handling
- Evaluating whether a feature is "intuitive"
- The user asks "how would someone use this?"

---

## Core Principle

**Good software empowers real people, not idealised users.**

Real people are distracted, impatient, confused, using a phone on a bus, and doing three things at once. They don't read instructions. They don't follow happy paths. They close tabs when annoyed.

Design for them, not for the demo.

---

## The Empathy Process

### Step 1: Who Is This Person?

Not a formal persona — a quick sketch of the actual human:

**Questions to ask**:
- How tech-savvy are they? (Developer? Office worker? Someone's grandparent?)
- What are they trying to accomplish? (Not "use the feature" — what's their real goal?)
- What's their emotional state? (Rushed? Curious? Frustrated? Forced to be here?)
- What device and context? (Desktop at work? Phone on a commute? Tablet in bed?)
- Have they used this before? (First time? Daily user? Returning after months away?)

```
Example: "Admin user managing team permissions"

Quick sketch: Mid-level manager. Not technical. Has 15 minutes between
meetings. Doing this because HR asked. Will forget the interface exists
until next quarter. Needs it to be obvious, not powerful.
```

### Step 2: Walk the Path

Mentally step through the feature as this person:

1. **Arrival**: How do they get here? What do they expect to see?
2. **Orientation**: Can they tell what to do without reading instructions?
3. **Action**: Is the primary action obvious? Is it the easiest thing to do?
4. **Feedback**: After acting, do they know it worked? What changed?
5. **Recovery**: If they made a mistake, can they undo it? Is the error clear?
6. **Completion**: Do they know they're done? What happens next?

### Step 3: Break the Happy Path

The happy path is a fantasy. Think about what actually happens:

- **Wrong input**: They type their email in the name field
- **Abandonment**: They close the tab halfway through a multi-step form
- **Confusion**: They don't know what "scope" means in this context
- **Impatience**: The page takes 4 seconds to load and they leave
- **Distraction**: They switch to another tab and come back 20 minutes later
- **Repetition**: They submit the form twice because nothing happened visually
- **Accessibility**: They're navigating with a keyboard because their mouse broke

### Step 4: Surface Assumptions

What are you assuming about the user that might be wrong?

```
Assumptions to check:
- "They'll read the tooltip" → Most people won't
- "They'll know what this icon means" → They might not
- "They'll complete the form in one sitting" → They might not
- "They have a fast connection" → They might not
- "They're using a modern browser" → Check your analytics
- "They understand our domain terminology" → They probably don't
```

---

## Empathy Annotations

This skill produces inline annotations during design and review:

### During Feature Design
```
👤 User lens: A first-time user won't know what "workspace" means here.
Consider: brief tooltip or contextual help on first visit.
```

### During Flow Design
```
👤 User lens: This 5-step onboarding asks for billing info on step 2.
Most users will drop off. Move billing to step 5 (after they see value).
```

### During Error State Design
```
👤 User lens: "Error 422: Unprocessable Entity" means nothing to a
non-developer. Try: "That email address is already registered.
Did you mean to log in instead?"
```

### During Review
```
👤 User lens: The success state shows a green tick for 0.5 seconds then
redirects. Users won't see it. Hold for 2 seconds or make the redirect
destination confirm success.
```

---

## Common Empathy Failures

### The Expert Blindness Problem
You've been staring at this feature for weeks. You know exactly how it works. Your user is seeing it for the first time.

**Fix**: Describe the feature to someone unfamiliar. If you need more than two sentences, the UI needs work.

### The Power User Trap
Designing for yourself instead of your actual users.

**Fix**: Your most common user is not your most technical user. The default experience should serve the common case; power features can be discovered.

### The "They'll Figure It Out" Fallacy
They won't. They'll leave.

**Fix**: If something requires figuring out, it requires a better design or better copy.

### The Empty State Blindness
Every feature starts empty. What does the user see before they've added any data?

**Fix**: Empty states should guide action, not just say "Nothing here yet."

---

## Quick Empathy Checklist

For any user-facing feature:

- [ ] **Who**: Can you describe the actual person using this in one sentence?
- [ ] **Goal**: What's their real-world goal (not the feature goal)?
- [ ] **Orientation**: Would they know what to do without instructions?
- [ ] **Action**: Is the primary action the most visually prominent element?
- [ ] **Feedback**: Do they get immediate confirmation after acting?
- [ ] **Recovery**: Can they undo mistakes easily?
- [ ] **Error**: Are error messages human-readable and actionable?
- [ ] **Empty**: What do they see before any data exists?
- [ ] **Return**: If they come back in 3 months, will they remember how this works?

---

## Integration Points

### With ethics-reviewer
Empathy and ethics overlap heavily. "Would the user feel tricked?" is both an empathy question and an ethics question. Use empathy lens for UX and ethics-reviewer for systemic concerns.

### With frontend-styler
Empathy informs styling decisions — what's visually prominent, how feedback is communicated, how errors appear. Frontend-styler handles the implementation.

### With scope-coach
Empathy can expand scope ("But what about this edge case for this user type?"). Scope coach moderates: "Is that the common case or a rare edge? Ship for the common case first."

### With domain-modeller
The domain model should reflect how users think about the domain, not just how the database stores it. If users think in "projects" and the model has "workspaces", there's a disconnect.

---

## Success Criteria

User empathy is effective when:
- Features are usable without documentation
- Error messages help users recover, not just report problems
- Empty states guide action
- The most common path is the easiest path
- Assumptions about users are explicit and challengeable
- The software feels like it was built by someone who cares
