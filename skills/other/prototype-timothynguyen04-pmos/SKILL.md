---
name: prototype
description: Advanced prototyping (Artifacts/Figma/Lovable/v0/Bolt)
disable-model-invocation: false
user-invocable: true
---

## Quick Start

**What to provide:** A PRD, feature description, or napkin sketch you want turned into a prototype.

```
/prototype                              → I'll check your latest PRD and ask what type
/prototype lovable                      → Generate a Lovable.dev prompt from your PRD
/prototype v0                           → Generate a v0.dev prompt
/prototype bolt                         → Generate a Bolt.new prompt
/prototype artifacts                    → Build HTML/React right here
/prototype figma                        → Create a Figma design handoff spec
/prototype [paste feature description]  → I'll recommend the right prototype type
```

**What you get:** A ready-to-use prototype prompt or interactive prototype, matched to your PRD requirements, with all edge cases and states covered.

**Time:** 5-15 minutes depending on complexity.

---

# /prototype - Advanced Prototyping

When the PM types `/prototype`, help them build interactive prototypes that bring PRD requirements to life. Choose the right tool for the job, generate detailed specs, and connect to the feedback loop.

**The $1-$10-$100 Rule:**
- $1: PM creates napkin sketch or prototype prompt --> catches issues early
- $10: Designer reworks based on feedback --> moderate cost
- $100: Engineering builds wrong thing --> expensive waste

Prototyping is the cheapest way to validate your solution before committing engineering time.

---

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Active PRDs | `outputs/prds/*.md`, `context-library/prds/*.md` | feature name | Requirements, user flows, success metrics, edge cases |
| Previous Prototypes | `outputs/prototypes/*.md` | feature name | Previous versions, iteration history, feedback received |
| User Research | `context-library/research/*.md` | user pain, problem | User quotes, pain points, workflows to design for |
| Napkin Sketches | `outputs/prototypes/*-napkin*.md` | feature name | ASCII wireframes to convert to prototype |
| Stakeholder Profiles | Stakeholder templates | design reviewers | Who will review this and what they care about |
| Business Info | `context-library/business-info-template.md` | brand, product | Brand guidelines, product context, existing UI patterns |
| Competitor Analysis | `context-library/research/competitive-*.md` | feature name | Competitor implementations for reference |

**Context Priority:**
1. PRD requirements and user flows FIRST (what to build)
2. User research and pain points SECOND (who we're building for)
3. Previous prototypes and napkin sketches THIRD (what we've already explored)
4. Brand and competitor context FOURTH (how it should look/feel)

**Cross-Skill Links:**
- If no PRD exists --> suggest `/prd-draft` first ("Prototype without requirements = guessing")
- If no user research --> suggest `/interview-guide` ("Who are you designing for?")
- After prototype is built --> suggest `/prototype-feedback` for structured review
- If prototype needs AI behavior --> link to `/generate-ai-prototype` for prompt generation
- If starting from scratch visually --> suggest `/napkin-sketch` first for quick layout

---

## When to Use

- **After PRD draft:** Visualize the solution before engineering review
- **Before stakeholder review:** Show, don't tell -- prototypes beat slide decks
- **During design exploration:** Test 2-3 approaches quickly
- **For user testing:** Give users something to interact with
- **Before XFN kickoff:** Align on the "what" with a tangible artifact

## When NOT to Use

- You don't have requirements yet (do `/prd-draft` first)
- You're exploring the problem space, not the solution (do research first)
- The feature is purely backend/API (no UI to prototype)

---

## Workflow

### Step 1: Understand Requirements

When the PM types `/prototype`, start by gathering context:

```
Let's build a prototype. First, let me check what we're working with...
```

**Silently check:**
1. Read most recent PRDs in `outputs/prds/` and `context-library/prds/`
2. Check `outputs/prototypes/` for previous versions
3. Read any napkin sketches from `/napkin-sketch`
4. Check user research for UX-relevant insights

**Then present what you found:**

```
Here's what I know about this feature:

**From PRD:** [Summary of requirements, user flow, key interactions]
**User Research:** [Relevant pain points, quotes, user expectations]
**Previous Prototypes:** [Any existing versions and what feedback they got]
**Napkin Sketch:** [If one exists, reference it]

A few questions before we prototype:
1. [Only ask what's genuinely missing -- skip if PRD covers it]
2. What's the primary user flow to prototype? (If multiple, which is highest priority?)
3. Who will review this? (Stakeholder context affects fidelity level)
```

**If no PRD exists:**
```
I don't see a PRD for this feature yet. Prototyping without requirements
is risky -- we might build the wrong thing beautifully.

Options:
1. Run `/prd-draft` first (recommended -- 15 min)
2. Give me a quick verbal brief and we'll prototype from that
3. We're just exploring -- build something rough and iterate

Which works for you?
```

---

### Step 2: Choose Prototype Type

Based on the requirements and context, recommend the right tool:

| Prototype Type | Best For | Fidelity | Time to Build | Shareable? |
|---------------|----------|----------|---------------|------------|
| **v0.dev** | UI components, pages, forms | High | 2-5 min | Yes (deployed URL) |
| **Lovable.dev** | Full-stack apps with data, auth, multi-page | Very High | 5-15 min | Yes (deployed URL) |
| **Bolt.new** | Quick full-stack, rapid iteration | High | 3-8 min | Yes (deployed URL) |
| **Claude Artifacts** | Simple interactions, quick validation | Medium | 2-5 min | In Claude only |
| **Figma Handoff** | Design-system work, high-fi specs | Spec only | 10-15 min | Figma file |
| **HTML/CSS Static** | Email templates, simple landing pages | Medium | 5-10 min | HTML file |

**Decision logic:**

```
IF feature is a single UI component or page
  → Recommend v0.dev ("Fast, high-quality, shareable URL")

IF feature is multi-page with data models or auth
  → Recommend Lovable.dev ("Full app, Supabase backend, deployed")

IF feature needs rapid iteration and you want to move fast
  → Recommend Bolt.new ("Quick to spin up, easy to modify")

IF feature is simple interaction or quick concept test
  → Recommend Claude Artifacts ("Build it right here, test immediately")

IF team uses Figma and needs design-system alignment
  → Recommend Figma Handoff ("Spec for your designer to build in Figma")

IF feature is static content (email, landing page, docs)
  → Recommend HTML/CSS ("Simple, no framework needed")
```

**Present the recommendation:**

```
Based on your requirements, I'd recommend **[Type]** because [reason].

But here are your options:
1. **v0.dev** - [Why it fits or doesn't]
2. **Lovable.dev** - [Why it fits or doesn't]
3. **Bolt.new** - [Why it fits or doesn't]
4. **Claude Artifacts** - [Why it fits or doesn't]
5. **Figma Handoff** - [Why it fits or doesn't]

Which would you like?
```

---

### Step 3: Generate Prototype

#### For v0.dev Prompts

Generate a detailed prompt the PM can paste into v0.dev.

**v0.dev Prompt Template:**

```markdown
# v0.dev Prototype Prompt: [Feature Name]

## Paste this into v0.dev:

---

Create a [component/page type] for [product context].

**User Goal:** [What the user is trying to accomplish]

**Layout:**
- [Header/nav description]
- [Main content area]
- [Sidebar/secondary content]
- [Footer/actions]

**Key Components:**
1. [Component 1] - [Behavior: what happens on click/hover/input]
2. [Component 2] - [Behavior]
3. [Component 3] - [Behavior]

**Data to Display:**
- [Field 1]: [Sample data]
- [Field 2]: [Sample data]
- [List/table]: [Sample items]

**Interactions:**
- When user [action], [result]
- When user [action], [result]
- When user [action], [result]

**States to Handle:**
- Default: [What the user sees first]
- Empty state: [What to show when no data]
- Loading state: [Skeleton/spinner/placeholder]
- Error state: [What to show on failure]
- Success state: [Confirmation/feedback]

**Style:**
- [Modern/minimal/playful/enterprise]
- Color palette: [Primary, secondary, accent] or [brand colors from business-info]
- Typography: [Clean sans-serif / specific font]
- Spacing: [Generous/compact]

**Responsive:**
- Desktop: [Layout description]
- Mobile: [How it adapts]

**Do NOT include:** [Things to exclude -- e.g., auth flows, payment, admin panel]

---
```

Save to: `outputs/prototypes/[feature-name]-v0-prompt.md`

---

#### For Lovable.dev Prompts

Generate a comprehensive prompt for Lovable.dev that produces a deployable app.

**Lovable.dev Prompt Template:**

```markdown
# Lovable.dev Prototype Prompt: [Feature Name]

## Paste this into Lovable.dev:

---

Build a [app type] for [product context].

**Overview:**
[2-3 sentence description of what this app does and who it's for]

**Pages/Views:**

1. **[Page Name]** (route: /path)
   - Purpose: [What this page does]
   - Components:
     - [Component]: [Behavior]
     - [Component]: [Behavior]
   - Data needed: [What data this page displays/collects]

2. **[Page Name]** (route: /path)
   - Purpose: [What this page does]
   - Components: [...]
   - Data needed: [...]

**Data Model:**
- [Entity 1]: [Fields: name, type, description]
- [Entity 2]: [Fields]
- [Relationships between entities]

**User Flows:**
1. [Flow name]: [Step 1] → [Step 2] → [Step 3] → [Outcome]
2. [Flow name]: [Step 1] → [Step 2] → [Decision] → [Branch A / Branch B]

**Authentication:** [None / Email login / OAuth / Magic link]

**Sample Data:**
[Provide 3-5 realistic data entries so the prototype looks real, not empty]

**Key Interactions:**
- [User action] → [System response]
- [User action] → [System response]
- [Edge case] → [How to handle]

**Style & Branding:**
- Feel: [Professional/playful/minimal/data-heavy]
- Colors: [Palette]
- Inspiration: [Reference apps or screenshots if available]

**States:**
- Empty state: [What to show]
- Loading: [Behavior]
- Error: [Message and recovery]
- Success: [Confirmation]

**Out of Scope:**
- [What NOT to build -- keep the prototype focused]

---
```

Save to: `outputs/prototypes/[feature-name]-lovable-prompt.md`

---

#### For Bolt.new Prompts

**Bolt.new Prompt Template:**

```markdown
# Bolt.new Prototype Prompt: [Feature Name]

## Paste this into Bolt.new:

---

Build a [app type] using [React/Next.js/vanilla].

**What it does:**
[Clear, concise description]

**Main screen:**
- [Layout description]
- [Key interactive elements]
- [Data display]

**Interactions:**
- [Action] → [Result]
- [Action] → [Result]

**Sample data:**
[Provide inline JSON or describe sample entries]

**Style:** [Minimal/modern] with [Tailwind/custom CSS]

**Important:** Keep it simple. This is a prototype, not production code.

---
```

Save to: `outputs/prototypes/[feature-name]-bolt-prompt.md`

---

#### For Claude Artifacts (HTML/React)

Build the prototype directly in the conversation.

**Approach:**
1. Create a single-file React component or HTML/CSS/JS
2. Include all states (default, empty, loading, error, success)
3. Use realistic sample data
4. Make interactions functional (clicks, form inputs, transitions)
5. Keep it self-contained (no external dependencies beyond React/Tailwind)

**Structure:**
```
- Header/navigation
- Main content area with primary user flow
- Interactive elements that respond to user input
- State transitions (show how the UI changes)
- Footer/secondary actions
```

Save the code to: `outputs/prototypes/[feature-name]-artifacts-v[N].md`

---

#### For Figma Handoff Specs

Generate a detailed design spec that a designer can implement in Figma.

**Figma Handoff Template:**

```markdown
# Figma Design Spec: [Feature Name]

## Overview
[What this feature does and how it fits into the product]

## User Flow
[Step 1] → [Step 2] → [Decision Point] → [Outcomes]

## Screens/Components Needed

### Screen 1: [Name]
**Layout:** [Description with rough dimensions]
**Components:**
| Component | Type | Behavior | States |
|-----------|------|----------|--------|
| [Name] | [Button/Input/Card/etc.] | [What it does] | [Default, Hover, Active, Disabled] |

**Spacing:** [Grid system, margins, padding]
**Typography:** [Heading sizes, body text, labels]
**Colors:** [Which colors from palette]

### Screen 2: [Name]
[Repeat structure]

## Component States
- Default
- Hover
- Active/Pressed
- Disabled
- Loading
- Error
- Success

## Responsive Behavior
- Desktop (1440px): [Layout]
- Tablet (768px): [Adaptations]
- Mobile (375px): [Adaptations]

## Accessibility
- Focus states for keyboard nav
- Color contrast requirements
- Screen reader labels

## Design Tokens to Use
[Reference existing design system tokens if known]

## References
- [Competitor screenshot/URL]
- [Existing product patterns to follow]
- [Napkin sketch from /napkin-sketch]
```

Save to: `outputs/prototypes/[feature-name]-figma-handoff.md`

---

### Step 3b: Requirements Verification

After generating the prototype prompt, include a checklist showing PRD requirement coverage. This ensures the prototype is traceable to the PRD and the PM knows what's covered vs what's not.

```
**Requirements Verified:**
- [x] [Requirement from PRD that IS covered by this prototype]
- [x] [Another covered requirement]
- [ ] [Requirement NOT covered -- explain why: out of scope for this prototype / deferred to iteration 2]
```

**How to build this checklist:**
1. Pull all requirements from the PRD (user flows, interactions, edge cases, success criteria)
2. For each requirement, check if the prototype prompt explicitly addresses it
3. Mark covered requirements with `[x]` and a brief note on how it's addressed
4. Mark uncovered requirements with `[ ]` and state the reason (out of scope, deferred, not prototypable, etc.)
5. If no PRD exists (PM chose to prototype from a verbal brief), note: "No PRD to verify against -- requirements based on verbal brief"

This checklist goes at the end of the prototype output, before the "Next steps" section.

---

### Step 4: Connect to Feedback Loop

After generating the prototype, offer next steps:

```
Prototype ready! Saved to outputs/prototypes/[filename].

**Next steps:**
1. **Test it:** [Instructions specific to type -- paste into v0, open in Lovable, etc.]
2. **Get feedback:** Run `/prototype-feedback` for structured review
3. **Iterate:** Come back with feedback and I'll generate v2
4. **Share:** [How to share with stakeholders]

**Want me to also:**
- Generate a second option with a different approach?
- Create a `/napkin-sketch` for a different screen in this flow?
- Draft talking points for presenting this prototype?
- Run `/generate-ai-prototype` for AI-specific behavior prompts?
```

---

## Iteration Workflow

When the PM comes back with feedback:

1. **Read previous prototype:** Check `outputs/prototypes/[feature]-*` for history
2. **Understand feedback:** What worked? What didn't? What changed?
3. **Generate updated version:** Increment version number
4. **Track changes:** Note what changed between versions

**Version naming:** `[feature-name]-[type]-v[N].md`
- v1: Initial prototype
- v2: After first round of feedback
- v3: After stakeholder review
- vFinal: Approved for engineering handoff

---

## Prototype Requirements Checklist

Before generating any prototype, ensure you have:

- [ ] **Primary user flow defined** (what does the user do, step by step?)
- [ ] **Key data to display** (what content appears on screen?)
- [ ] **Main interactions** (what can the user click/tap/input?)
- [ ] **Success state** (what does "done" look like?)
- [ ] **Error handling** (what happens when things go wrong?)
- [ ] **Empty state** (what shows when there's no data?)

If any are missing, ask before generating.

---

## Anti-Patterns to Avoid

**Prototyping without requirements:**
- "Make it look good" is not a requirement. Start with `/prd-draft`.
- At minimum, you need: user goal, key interactions, and success criteria.

**Over-engineering a throwaway prototype:**
- Prototypes are disposable. Don't add auth, payment, or admin panels.
- Focus on the ONE flow that needs validation.

**Prototyping the wrong thing:**
- Prototype the risky/uncertain parts, not the obvious ones.
- If everyone agrees on how login should work, don't prototype login.

**Skipping states:**
- Empty, loading, and error states reveal 80% of UX problems.
- Always include them.

**Not using real-ish data:**
- "Lorem ipsum" and "Test User" make prototypes feel fake.
- Use realistic names, numbers, and content.

**Building the whole app:**
- Prototype the critical path. Leave everything else out.
- If the prototype has more than 3-4 screens, you're building too much.

**Not connecting to feedback:**
- A prototype without feedback is wasted effort.
- Always run `/prototype-feedback` after sharing.

---

## Integration with Other Skills

**Before:**
- `/prd-draft` - Define requirements (most important input)
- `/napkin-sketch` - Quick ASCII wireframe to establish layout
- `/generate-ai-prototype` - Generate AI-specific prompt behavior

**After:**
- `/prototype-feedback` - Structured review and iteration loop
- `/prd-draft` - Update PRD based on prototype learnings
- `/create-tickets` - Turn approved prototype into engineering tasks

**Related:**
- `/prd-review-panel` - Validate with Designer sub-agent
- `/user-interview` - Test prototype with real users
- `/ralph-wiggum` - Challenge whether this is the right solution

---

## Output Quality Self-Check

Before presenting the prototype or prompt, verify:

- [ ] Prototype matches PRD requirements (if PRD exists) -- no missing features, no added scope
- [ ] All user-facing states included (default, empty, loading, error, success)
- [ ] Sample data is realistic, not placeholder text
- [ ] Primary user flow is complete from start to finish
- [ ] Prompt is specific enough that two different AI tools would produce similar results
- [ ] Edge cases from user research are addressed (if research exists)
- [ ] File saved with correct naming convention: `[feature-name]-[type]-v[N].md`
- [ ] Requirements verification checklist included (PRD requirements mapped to prototype coverage with reasons for any gaps)
- [ ] Next steps are clear (how to test, how to iterate, how to get feedback)

---

## Related Skills

**Before this:**
- `/prd-draft` - Clear requirements
- `/napkin-sketch` - Quick wireframe first
- `/generate-ai-prototype` - AI behavior prompts

**After this:**
- `/prototype-feedback` - Structured review loop
- `/create-tickets` - Engineering handoff
- `/feature-results` - Measure impact post-launch

**Parallel use:**
- `/user-interview` - Test with real users
- `/ralph-wiggum` - Challenge the solution approach
