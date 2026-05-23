---
name: ux-writing
description: Write clear, helpful, human interface copy. Use when crafting microcopy, error messages, button labels, empty states, onboarding flows, tooltips, or when the user needs guidance on voice, tone, and how words shape the user experience.
---

# UX Writer

Words are interface. Every string is a design decision.

## Output Contract

For copy audits, structure your analysis as:

```markdown
## Copy Audit

### Voice Check
- Current voice: [description of detected voice/tone]
- Target voice: [if specified or inferred]
- Adjustments needed: [specific changes, or "None—voice is consistent"]

### Issues
| Location | Current Copy | Problem | Suggested Copy |
|----------|--------------|---------|----------------|
| [Button/label/message] | "..." | [Why it fails] | "..." |

### Patterns to Establish
- Buttons: [verb + object pattern]
- Errors: [structure: what happened → how to fix]
- Empty states: [structure used]
- Success: [tone and length]

### Quick Wins
- [Most impactful change]
- [Second priority]
```

For individual copy requests:

```markdown
## Copy: [Element Type]

### Context
[Where this appears, user state, stakes]

### Recommendation
[The copy]

### Rationale
- [Why this wording]

### Variations
- [Alternative if needed]
```

## Core Principles

### Clarity Over Cleverness
- Say what you mean
- Mean what you say
- If a user has to think about what you wrote, rewrite it
- Puns and wordplay rarely survive translation or stress

### Brevity With Purpose
- Shorter is usually better
- But not at the cost of clarity
- Cut ruthlessly, then check if meaning survived
- "Delete your account" not "Proceed with account deletion process"

### User Over System
- Speak the user's language, not the system's
- "We couldn't find that page" not "404 Error: Resource not found"
- "Your photo is uploading" not "Asset upload in progress"
- The user doesn't care about your architecture

### Consistency Is Kindness
- Same action = same words everywhere
- Pick "Save" or "Submit" and stick with it
- Pick "Cancel" or "Discard" and stick with it
- Inconsistency creates doubt

## Voice and Tone

### Voice (Who You Are)
Voice is constant—your product's personality:
- **Confident** but not arrogant
- **Helpful** but not patronizing
- **Professional** but not cold
- **Clear** but not dumbed-down

Define 3-4 voice attributes. Use them as a filter.

### Tone (How You Adapt)
Tone shifts with context:

| Context | Tone |
|---------|------|
| Success | Celebratory, warm |
| Error | Calm, helpful, humble |
| Waiting | Reassuring, patient |
| Warning | Serious, clear |
| Onboarding | Encouraging, guiding |
| Empty state | Inviting, actionable |

The same voice, different tones. You're still you when happy or apologizing.

### Finding Your Voice

**Ask:**
- If your product were a person, who would they be?
- How would they explain something at a dinner party?
- What would they never say?

**Test:**
- Read it aloud. Does it sound like a human?
- Would you say this to someone's face?
- Does it match the rest of the product?

## Microcopy Patterns

### Buttons and Actions

**Do:**
- Start with a verb
- Be specific about what happens
- "Save changes" not "Save"
- "Send message" not "Submit"
- "Delete project" not "Delete" (when stakes are high)

**Avoid:**
- "Click here" (obviously they'll click)
- "Submit" (submit what?)
- "OK" (ok to what?)
- "Yes/No" without context

**Button pairs:**
| Primary | Secondary |
|---------|-----------|
| Save | Cancel |
| Delete | Keep |
| Send | Save draft |
| Confirm | Go back |
| Create account | Log in instead |

### Labels and Placeholders

**Labels:**
- Always visible (not just placeholders)
- Noun or short phrase
- "Email address" not "Enter your email address here"
- Sentence case, not Title Case

**Placeholders:**
- Example format, not instruction
- "name@example.com" not "Enter email"
- Disappear on focus—don't rely on them
- Gray text, low contrast (they're hints, not content)

**Helper text:**
- Explain why or give guidance
- "We'll send a confirmation link"
- "Must be at least 8 characters"
- Below the field, not above

### Error Messages

**Structure:**
1. What happened (brief)
2. Why it happened (if helpful)
3. How to fix it (always)

**Examples:**

Bad: "Invalid input"
Good: "Enter a valid email address, like name@example.com"

Bad: "Error 500"
Good: "Something went wrong on our end. Please try again."

Bad: "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character and be between 8 and 64 characters"
Good: "Password needs 8+ characters with a mix of letters, numbers, and symbols"

**Principles:**
- Never blame the user
- Be specific about what's wrong
- Tell them exactly how to fix it
- Don't use "please" excessively (once is enough)
- "Oops" and "Uh oh" get old fast

### Success Messages

- Confirm what happened
- Be brief—success shouldn't slow them down
- Suggest next action if relevant
- Match the magnitude of accomplishment

**Examples:**
- "Saved" (small action)
- "Message sent" (medium action)
- "Your account is ready. Let's get started." (big moment)

### Empty States

**Structure:**
1. What belongs here
2. Why it's empty (if not obvious)
3. How to fill it (call to action)

**Examples:**

Bad: "No data"

Good:
> **No projects yet**
> Create your first project to get started.
> [Create project]

Better:
> **Your projects will appear here**
> Projects help you organize your work. Create one to begin.
> [Create your first project]

### Loading and Progress

**Brief waits (<5 seconds):**
- Spinner or skeleton is enough
- "Loading..." if you must

**Longer waits:**
- Set expectations: "This usually takes about a minute"
- Show progress: "Uploading... 45%"
- Explain what's happening: "Processing your images..."

**Very long waits:**
- "We'll email you when it's ready"
- Let them leave

### Confirmations and Warnings

**Confirmation dialogs:**
- State the action clearly
- Explain consequences
- Make the destructive option obviously destructive

**Example:**
> **Delete this project?**
> This will permanently delete "Website Redesign" and all its files. This can't be undone.
>
> [Cancel] [Delete project]

Not:
> Are you sure?
> [No] [Yes]

**Warning patterns:**
- Yellow/orange for warnings (proceed with caution)
- Red for destructive actions (data loss, irreversible)
- Inline near the action, not just in a modal

### Tooltips and Help Text

**When to use tooltips:**
- Clarify icon-only buttons
- Explain unfamiliar terms
- Provide keyboard shortcuts
- NOT for essential information

**Writing tooltips:**
- One sentence max
- No period at the end (unless multiple sentences)
- Action-oriented for buttons: "Add a new project"
- Explanatory for concepts: "Projects organize your work"

### Onboarding Copy

**Principles:**
- Show value before asking for effort
- One concept per step
- Praise progress
- Let them skip (with grace)

**Welcome screens:**
- Warm but brief
- Set expectations
- Single clear next step

**Tooltips/Coaches:**
- Point to specific UI
- Explain benefit, not just function
- "Add teammates to collaborate in real-time" not "Click here to add users"

**Progress:**
- "Step 2 of 4" (sets expectations)
- "Almost there!" (encouragement)
- "You're all set" (closure)

## Writing Techniques

### The Readback Test
Read it aloud. If you wouldn't say it to someone, don't write it.

### The Screenshot Test
Cover everything but the text. Does it still make sense?

### The Stress Test
Imagine the user is frustrated, in a hurry, or on their phone with one thumb. Does your copy still work?

### The Translation Test
Will this make sense in other languages? Idioms, puns, and cultural references often don't.

### The Truncation Test
What happens when this is cut off on a small screen? Put important words first.

## Common Mistakes

### Being Vague
- "An error occurred" → What error?
- "Invalid" → What's invalid? What's valid?
- "Try again" → Try what again? Will it work this time?

### Being Verbose
- "In order to save your changes, please click the Save button below"
- → "Save changes"

### Being Robotic
- "Your request has been processed successfully"
- → "Done" or "Changes saved"

### Being Cute When It Hurts
- "Oopsie! Something went wrong :(" (when they lost data)
- Save personality for low-stakes moments

### Mixing Metaphors
- Pick a conceptual model and stick with it
- If it's a "library," use "shelves" not "folders"
- If it's an "inbox," use "messages" not "items"

### Assuming Knowledge
- "Configure your SSH keys" (what's SSH?)
- "Enable 2FA" (what's 2FA?)
- Either explain or link to explanation

## Capitalization and Punctuation

### Capitalization
- **Sentence case** for almost everything: "Create new project"
- **Title Case** rarely: Proper nouns, app names
- **ALL CAPS** never (except abbreviations)

### Punctuation
- No periods in buttons or labels
- Periods in sentences (body copy, descriptions)
- No exclamation marks in errors!!!
- One exclamation mark maximum per screen (usually in success)

### Contractions
- Use them—they're human: "can't," "won't," "you'll"
- Exception: Very formal or legal contexts
- Exception: When meaning could be unclear

## Writing for Accessibility

### Screen Readers
- Links: "Read our privacy policy" not "Click here"
- Buttons: Describe the action, not the element
- Images: Alt text that conveys meaning, not decoration

### Cognitive Load
- Simple words over complex
- Short sentences over long
- Active voice over passive
- Lists over paragraphs

### Reading Level
- Aim for grade 8 reading level
- Hemingway App is a useful check
- Simple doesn't mean dumbed down

## Content Strategy

### Content Hierarchy
1. What must they know? (essential)
2. What should they know? (helpful)
3. What could they know? (optional)

Put #1 in the UI. Put #2 in tooltips/help. Put #3 in documentation.

### Writing Systems, Not Strings
- Create patterns, not one-offs
- "You have 1 notification" / "You have 2 notifications" (pluralization)
- Build a component library for copy too
- Document patterns in a style guide

### Governance
- Who approves copy?
- Where does copy live? (code, CMS, spreadsheet?)
- How do you maintain consistency across teams?
- Who updates when the product changes?

## The Craft

### What Great UX Writing Feels Like
- You don't notice it
- Everything makes sense
- You never feel lost or blamed
- The product feels like it's on your side

### The Real Job
- Reduce friction
- Prevent errors
- Build trust
- Guide without controlling
- Disappear into usefulness

### Remember
- You're not writing for screens
- You're writing for people
- Tired people, busy people, frustrated people
- One confused moment costs trust
- Every word is a chance to help
