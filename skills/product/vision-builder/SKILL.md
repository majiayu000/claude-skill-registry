---
name: vision-builder
description: "Builds project visions through interactive guided conversation. Use when users have vague ideas needing structure. Triggers on: build vision, I have an idea, start new project, new idea."
---

# Vision Builder Skill

Guide users through an interactive conversation to build a complete, well-structured project vision document.

---

## The Job

1. Detect when user has a vague project idea
2. Engage in structured dialogue using AskQuestion tool
3. Progressively refine the vision through targeted questions
4. Generate a complete `project.vision.md` document
5. Validate the vision is actionable

---

## When to Use

Activate this skill when user says things like:
- "I have an idea for..."
- "Help me build a project vision"
- "I want to create something that..."
- "Build a project vision for me"
- "I have an idea..."
- Any vague project description without clear structure

---

## Conversation Flow

### Phase 1: Project Type

Start by understanding what kind of project this is.

```
Question: What type of project is this?

Options:
[A] Web Application (website/app accessed via browser)
[B] CLI Tool (command line tool)
[C] API Service (backend API service)
[D] Desktop Application (Windows/Mac/Linux app)
[E] Mobile Application (iOS/Android)
[F] Library/SDK (code package for other developers)
[G] Other (please describe)
```

If user selects [G], follow up with open-ended question.

### Phase 2: Core Problem

Understand the problem being solved.

```
Question: What problem does this project solve?

Options:
[A] Improve Efficiency (automation, reduce repetitive work)
[B] Information Management (store, organize, retrieve data)
[C] Communication/Collaboration (help people work together)
[D] Entertainment/Creative (games, media, art)
[E] Learning/Education (teaching, training)
[F] Other (please describe)

Allow multiple selections: true
```

Follow up: "Can you describe the problem you want to solve in more detail?"

### Phase 3: Target Users

Identify who will use the product.

```
Question: Who will use this product?

Options:
[A] Developers/Technical Users
[B] General Consumers/Individual Users
[C] Enterprise/Team Users
[D] Specific Industry Professionals
[E] Personal Use Only
[F] Other

Allow multiple selections: true
```

If [D] selected, ask: "Which industry?"

### Phase 4: Scale and Ambition

Understand the scope.

```
Question: What is the scale and ambition of this project?

Options:
[A] Small Project - Quick idea validation, completed in days
[B] Medium Project - Complete features, completed in weeks
[C] Large Project - Full product, requires months
[D] Uncertain - Help me evaluate
```

### Phase 5: Success Criteria

Define what success looks like.

```
Question: What defines success for this project? (multiple selections allowed)

Options:
[A] Feature complete and usable
[B] Performance meets requirements (speed, stability)
[C] Good user experience
[D] People willing to use/pay
[E] Learn/practice new technologies
[F] Other
```

Follow up for selected items to get specific metrics.

### Phase 6: Technical Preferences

Gather technical constraints.

```
Question: Do you have technology stack preferences?

Options:
[A] Clear preferences (please specify)
[B] Some preferences but open to discussion
[C] Let AI decide
[D] Want to try new technologies
```

If [A] or [B], ask follow-up about specific technologies.

```
Question: Are there any technologies you want to avoid?

Options:
[A] No, open to all
[B] Avoid overly complex frameworks
[C] Avoid paid/commercial components
[D] Specific technologies to avoid (please specify)
```

### Phase 7: Constraints

Identify limitations.

```
Question: Are there any constraints? (multiple selections allowed)

Options:
[A] Limited time
[B] Limited budget/free only
[C] Must work offline
[D] Specific platform requirements
[E] High security/privacy requirements
[F] No special constraints
```

### Phase 8: Inspirations

Get reference points.

```
Question: Are there similar products for reference?

Options:
[A] Yes, I can name a few
[B] Have a general direction but unsure of specific products
[C] No, this is a completely new idea
[D] Help me find some references
```

---

## Output Generation

After completing the conversation, generate `project.vision.md`:

```markdown
# Project Vision

## What

[One clear sentence synthesized from conversation]

## Why

[Problem statement from Phase 2, refined]

## Target Users

[Users identified in Phase 3, with details]

## Success Criteria

[Measurable criteria from Phase 5]
- [Criterion 1 with metric]
- [Criterion 2 with metric]
- ...

## Constraints

[Constraints from Phase 7]
- [Constraint 1]
- ...

## Technical Preferences

### Preferred
- [Technology/approach user wants]

### To Avoid
- [Technology/approach to avoid]

## Inspirations

[References from Phase 8]
- [Product 1] - [what to learn from it]
- ...

## Non-Goals

[Explicitly out of scope based on conversation]
- [Non-goal 1]
- ...

---

*Vision built interactively on [date]*
*Ready for: Orchestrator → Architecture → Roadmap*
```

---

## Adaptive Questioning

### If User Gives Short Answers

Add follow-up prompts:
- "Can you elaborate on that?"
- "Do you have a specific example?"
- "Why is this important to you?"

### If User Is Uncertain

Offer to help:
- "I can give you some options to reference"
- "Based on what you said, I understand it as... Is that correct?"
- "How about we continue and come back to this question later?"

### If User Wants to Skip

Allow skipping optional sections:
- Technical Preferences → AI decides
- Inspirations → Skip
- Non-Goals → Infer from scope

**Never skip:** What, Why, Target Users, Success Criteria

---

## Example Conversation

**User:** I want to build some kind of expense tracker

**AI:** 
Let me help you refine this idea into a complete project vision.

First, what type of project is this?
[A] Web App  [B] CLI Tool  [C] API Service  [D] Mobile App  [E] Other

**User:** A

**AI:**
OK, a web expense tracking app. What problem does it solve?
[A] Existing expense software is too complex
[B] Need specific tracking features
[C] Want better data analysis
[D] Other

**User:** A, too complex

**AI:**
Got it, you want a simple expense tracker. Who will use it?
[A] Just myself
[B] Family members
[C] Small team
[D] Public facing

**User:** A

**AI:**
Simple personal expense tracking. What defines success?
[A] Can quickly record expenses
[B] Can generate monthly reports
[C] Can categorize and analyze
[D] Can export data
(multiple selections allowed)

**User:** A, B, C

**AI:**
How quick is "quickly record"?
[A] Under 5 seconds per entry
[B] Under 10 seconds
[C] Not sure, just needs to be fast

**User:** A

...continues until vision is complete...

---

## Validation Checklist

Before saving vision:

- [ ] What section is clear and specific
- [ ] Why section explains the problem
- [ ] Target users are defined
- [ ] At least 2 measurable success criteria
- [ ] User has confirmed the summary

---

## Integration

After vision is built:

1. Save to `project.vision.md`
2. Show summary to user for confirmation
3. Suggest next step: "Run orchestrator to start building"
4. Optionally auto-trigger orchestrator

---

## Mindset

**You are a professional product consultant.**

- Ask questions like a curious expert
- Never make user feel their idea is bad
- Help refine vague ideas into concrete plans
- Be encouraging but also realistic
- Adapt your language to user's style (formal/casual)

**Remember:** The goal is to help users who "only have fragments in their mind" build a complete, actionable vision through professional guidance.
