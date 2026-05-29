---
name: scope
description: Turn ideas into clear, buildable specs for AI tools or stakeholder review. Use when starting features, planning projects, or when AI keeps building the wrong thing. Creates Quick Feature Specs (10-15 min) for immediate AI builds or Full Project Scopes (1-2 hours) for budget planning and contractor estimates.
---

# Scope

Turn ideas into specs that AI tools can execute and stakeholders can evaluate.

## When to Use This Skill

- Starting any new feature or product
- Before hiring developers or estimating costs  
- When AI keeps building the wrong thing (unclear spec)
- When stakeholders need to review scope and budget

## Choose Your Approach

**Quick Feature Spec (10-15 minutes)**
- Use for: Single features, iterations, additions
- Give to: AI tools (Claude Code, Lovable, Replit) to build directly
- See: [QUICK-SPEC.md](QUICK-SPEC.md)

**Full Project Scope (1-2 hours)**
- Use for: New products, major releases, stakeholder review
- Give to: Contractors, team members, budget planning
- See: [PROJECT-SCOPE.md](PROJECT-SCOPE.md)

---

## Quick Feature Spec Workflow

Use this checklist and complete each section:

```
Feature Spec Progress:
- [ ] Write what users will do (2-3 sentences)
- [ ] Show what it looks like (reference, screenshot, or description)
- [ ] Define happy path (3-5 steps)
- [ ] List edge cases (2-4 scenarios)
- [ ] Specify out of scope items
- [ ] Save to docs/specs/YYYY-MM-DD-feature-name.md
```

### Section 1: What Users Will Do

Write 2-3 sentences describing user actions and outcomes.

**Template:**
```
Users can [ACTION] to [OUTCOME].
When they [DO THIS], they see [WHAT HAPPENS].
If [EDGE CASE], then [WHAT HAPPENS].
```

**Example:**
```
Users sign up with email/password, receive confirmation email, and log in to 
see their dashboard. They can reset forgotten passwords via email link.
```

### Section 2: What It Looks Like

Pick ONE:
- **Reference app:** "Login like Linear - minimal, centered, email/password/button"
- **Screenshot/sketch:** Quick mockup or phone photo
- **Description:** "Card 400px wide, 'Welcome' header Inter 24px, two inputs, blue button"

### Section 3: Happy Path

List 3-5 steps users take to complete the task.

### Section 4: Edge Cases  

List 2-4 scenarios where things don't go as planned and what happens.

**Format:**
```
- **[Scenario]:** [Response shown to user]
```

### Section 5: Out of Scope

Define what you're NOT building to prevent scope creep.

For complete template and examples, see [QUICK-SPEC.md](QUICK-SPEC.md)

---

## Full Project Scope Workflow

Use this checklist for comprehensive project planning:

```
Project Scope Progress:
- [ ] Write introduction (background, in/out of scope)
- [ ] Define user roles
- [ ] List all pages/screens
- [ ] Describe core features
- [ ] Identify integrations
- [ ] Create milestones with hour estimates
- [ ] Document assumptions and open questions
- [ ] Save to docs/specs/YYYY-MM-DD-project-name.md
```

### The 7 Required Sections

1. **Introduction** - Background, in scope, out of scope
2. **User Roles** - Each role's responsibilities
3. **Pages & Screens** - Every page with one-line purpose
4. **Core Features** - Outcome-focused capabilities
5. **Integrations** - External services with complexity/risk notes
6. **Milestones & Tasks** - Phases with hour estimates
7. **Open Questions** - Assumptions and unresolved decisions

For complete template and examples, see [PROJECT-SCOPE.md](PROJECT-SCOPE.md)

---

## Using Your Spec With AI Tools

**Claude Code / Cursor:**
```
Build this feature: [paste Quick Feature Spec]
```

**Lovable / Replit / Bolt:**
- Paste Quick Feature Spec as initial prompt
- Break complex features into smaller chunks
- Iterate: "Close, but error message should say X not Y"

**Hiring contractors:**
- Send Full Project Scope
- Ask: "What's unclear? What would you change?"
- Get hour estimate and compare to yours

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "Build a dashboard" | Describe what's ON dashboard and what each thing does |
| Describing HOW to code it | Describe WHAT it should do |
| Forgetting mobile | Add "Works on mobile" to every spec |
| Skipping edge cases | Define what happens when things break |
| No out-of-scope | Prevents scope creep |

---

## When You're Stuck

**"I don't know what I want yet"**
- Use competitor's product for 20 minutes
- Screenshot 3 things you like
- Write: "I want these 3 things, but simpler"

**"AI keeps building the wrong thing"**
- Your spec is vague
- Use templates in QUICK-SPEC.md or PROJECT-SCOPE.md
- Fill in EVERY section

---

## After Scoping

**Save as:** `docs/specs/YYYY-MM-DD-feature-name.md`

**Then:**
- Quick Feature Spec → Give directly to AI tool
- Full Project Scope → Review with stakeholders/contractors first

---

## Success Looks Like

✅ AI builds it right first time (or very close)
✅ Contractors give realistic estimates without surprises  
✅ Edge cases don't surprise you in production
✅ Stakeholders know exactly what they're getting
