---
name: generate-ai-prototype
description: Generate v0.dev, Lovable, or Bolt.new prompts for AI-powered prototyping
---

# Generate AI Prototype Skill

Create optimized prompts for AI prototyping tools (v0.dev, Lovable, Bolt.new) to quickly build working prototypes from PRDs or feature specs.

## Quick Start

1. Tell me what you want to prototype (feature name, PRD link, or description)
2. I'll ask which tool: **v0.dev** (UI only), **Lovable** (full-stack), or **Bolt.new** (quick demo)
3. I check your PRD, design system, and user research for context
4. I generate a copy-paste-ready prompt optimized for the tool
5. You paste it, get a working prototype, and share the link

**Example:** "Generate a prototype prompt for the onboarding wizard from PRD-2024-05"

**Output:** Saved to `outputs/prototypes/[feature]-prototype-prompt.md`

**Time:** 10-15 minutes to generate prompt, 1-2 minutes to build prototype

## When to Use This Skill

- Converting PRDs into functional prototypes
- Rapid iteration on UI concepts
- Demonstrating features to stakeholders
- Testing user flows before engineering starts

## Supported AI Prototyping Tools

### v0.dev (Vercel)
- **Best for:** React/Next.js apps, modern UI components
- **Strengths:** Clean design, shadcn/ui integration, responsive
- **Limits:** Frontend only, no backend logic
- **Cost:** Free tier, then paid

### Lovable (formerly GPT Engineer)
- **Best for:** Full-stack apps with backend
- **Strengths:** Complete apps, authentication, database
- **Limits:** Opinionated stack (React + Supabase)
- **Cost:** Free tier, then $20/mo

### Bolt.new (StackBlitz)
- **Best for:** Quick demos, isolated components
- **Strengths:** Instant preview, no account needed
- **Limits:** Simpler apps, less customization
- **Cost:** Free

## Workflow

### Step 1: Gather Requirements

Ask the PM:
1. **Feature scope:** What are we prototyping?
2. **Target tool:** v0.dev, Lovable, or Bolt.new?
3. **Fidelity level:** Quick sketch or polished demo?
4. **Key user flows:** What paths must work?
5. **Design system:** Match existing product or generic?

### Step 2: Analyze Context

Read relevant files:
- PRD or feature spec
- Design system docs (if available)
- Existing UI screenshots (if provided)
- User journey maps

Extract:
- Core user flows
- UI components needed
- Data models (if backend)
- Key interactions
- Edge cases to demonstrate

### Step 3: Generate Prompt

Create a structured prompt optimized for the target tool.

#### v0.dev Prompt Template

```
Build a [feature name] interface with the following requirements:

## Core Functionality
[List 3-5 key features]

## User Flow
1. [Step 1: User action]
2. [Step 2: System response]
3. [Step 3: Next action]

## UI Components Needed
- [Component 1: Description]
- [Component 2: Description]
- [Component 3: Description]

## Design Specifications
- **Style:** [Modern, minimal, professional, etc.]
- **Colors:** [Primary: #hex, Secondary: #hex, or "use default shadcn palette"]
- **Layout:** [Desktop-first, mobile-first, responsive]
- **Components:** Use shadcn/ui components

## Key Interactions
- [Interaction 1: e.g., "Click 'Add Item' opens modal"]
- [Interaction 2: e.g., "Drag to reorder list items"]

## Data Structure (mock)
```typescript
interface [DataType] {
  [field]: [type];
  [field]: [type];
}
```

## Edge Cases to Show
- [Empty state]
- [Loading state]
- [Error state]
- [Success state]

## Example Content
[Provide realistic sample data]

Technical preferences:
- Use TypeScript
- Tailwind CSS for styling
- React hooks for state
- Responsive design (mobile + desktop)
```

#### Lovable Prompt Template

```
Create a [feature name] application with the following specs:

## App Overview
[1-2 sentence description]

## User Stories
1. As a [user type], I want to [action] so that [benefit]
2. As a [user type], I want to [action] so that [benefit]
3. As a [user type], I want to [action] so that [benefit]

## Pages/Views
1. **[Page Name]**
   - Purpose: [What this page does]
   - Components: [List key UI elements]
   - Actions: [User can do X, Y, Z]

2. **[Page Name]**
   - Purpose: [What this page does]
   - Components: [List key UI elements]
   - Actions: [User can do X, Y, Z]

## Database Schema
```sql
-- [Table Name]
CREATE TABLE [table_name] (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  [field_name] [TYPE] [CONSTRAINTS],
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Authentication
- [x] User signup/login required
- [x] Protected routes: [list routes]
- [ ] Public access allowed

## Key Features
1. [Feature 1]: [Description]
2. [Feature 2]: [Description]
3. [Feature 3]: [Description]

## Business Logic
- [Rule 1: e.g., "Users can only edit their own items"]
- [Rule 2: e.g., "Max 10 items per user on free tier"]

## Sample Data
[Provide realistic examples for testing]

Tech Stack Preferences:
- Frontend: React + TypeScript
- Backend: Supabase
- Styling: Tailwind CSS
- State: React hooks/context
```

#### Bolt.new Prompt Template

```
Build a simple [feature name] component:

**What it does:**
[2-3 sentence description]

**UI Layout:**
[Describe the visual structure]

**User Interactions:**
1. [User does X] → [System responds Y]
2. [User does A] → [System responds B]

**Functionality:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Styling:**
[Modern/minimal/colorful/etc. + any color preferences]

**Example Data:**
[Provide 2-3 sample items]

Keep it simple and functional. Focus on core flow.
```

### Step 4: Optimization Tips

**For all tools:**
- ✅ Be specific about functionality
- ✅ Provide example data
- ✅ Describe interactions clearly
- ✅ Specify edge cases (empty, loading, error states)
- ❌ Don't overload with features (start simple)
- ❌ Don't assume technical knowledge (be explicit)

**v0.dev specific:**
- Use shadcn/ui component names
- Specify responsive behavior
- Request TypeScript for better quality

**Lovable specific:**
- Define database schema clearly
- Specify authentication requirements
- Describe business logic rules

**Bolt.new specific:**
- Keep scope small (single feature/component)
- Focus on visual demo over complex logic

### Step 5: Deliver Prompt

Present the generated prompt to the PM with:

1. **The Prompt** (formatted for copy-paste)
2. **Instructions:**
   - Where to paste (v0.dev/Lovable/Bolt.new)
   - Expected output
   - How to iterate (what to tweak if needed)
3. **Next Steps:**
   - "Share prototype link with stakeholders"
   - "Use as spec for engineering"
   - "Iterate based on feedback"

## Advanced Techniques

### Matching Existing Design Systems

If PM provides screenshots or design system docs:

```
Use this design system:

**Colors:**
- Primary: [extracted from screenshot]
- Secondary: [extracted from screenshot]
- Text: [extracted from screenshot]

**Typography:**
- Headings: [font family, size]
- Body: [font family, size]

**Components:**
- Buttons: [describe style]
- Inputs: [describe style]
- Cards: [describe style]

**Spacing:**
- Use [4px/8px/16px] grid system

Reference the attached screenshot for visual style.
```

### Multi-Screen Flow Guidance

For features with multiple screens or states (e.g., onboarding wizard, checkout flow, settings panels), structure the prompt to produce a cohesive multi-step experience rather than isolated pages.

**Include in the prompt:**

1. **Screen/step list with descriptions** -- List every screen by name, its purpose, and what the user sees
2. **Navigation between screens** -- Specify how users move forward, back, and skip (buttons, tabs, swipe, URL routing)
3. **State management (what data carries forward)** -- Clarify which inputs persist across screens (e.g., "selections from Step 1 appear in Step 3 summary")
4. **Edge cases per screen** -- Define empty, error, loading, and validation states for each screen individually

**Prompt structure for multi-step flows:**

```
Build a multi-step flow with [N] screens:

## Screen 1: [Name]
- Purpose: [What happens here]
- UI: [Key components]
- Data collected: [Fields, selections]
- Validation: [Required fields, format rules]
- Next: [Button label] → Screen 2

## Screen 2: [Name]
- Purpose: [What happens here]
- UI: [Key components]
- Data from previous: [What carries forward]
- Next: [Button label] → Screen 3
- Back: [Button label] → Screen 1

## Screen [N]: [Name - usually Confirmation/Review]
- Purpose: Review and submit
- Shows: Summary of all previous inputs
- Actions: [Submit], [Edit Step X]
- Success state: [What user sees after completion]

## Global Requirements
- Progress indicator showing current step (e.g., "Step 2 of 4")
- Persist data if user navigates back
- Handle browser back button gracefully
- Mobile responsive (stack layout vertically on small screens)
```

**Avoid:** Generating separate, disconnected prompts for each screen. The AI tool produces better results when it understands the full flow context in a single prompt.

### Prototype Iteration

After initial prototype:

```
Refine the existing prototype:

**What's working:**
- [Keep feature X]
- [Keep interaction Y]

**What to change:**
- [Modify feature A: description]
- [Add feature B: description]
- [Remove feature C: reason]

**Specific updates:**
1. [Detailed change 1]
2. [Detailed change 2]
```

## Common Use Cases

### 1. Dashboard Prototype
```
Build a dashboard showing:
- [Metric 1] as a card with trend
- [Metric 2] as a line chart
- [Recent activity] as a list
- Filters for date range
```

### 2. Form/Wizard Prototype
```
Create a multi-step form:
Step 1: [Collect basic info]
Step 2: [Collect detailed info]
Step 3: [Review & confirm]
Include validation and progress indicator
```

### 3. Settings Page Prototype
```
Build a settings interface with:
- Tabbed navigation (Profile, Preferences, Billing)
- Toggle switches for boolean settings
- Dropdowns for choices
- Save/Cancel buttons
```

### 4. Onboarding Flow Prototype
```
Create an onboarding flow:
Screen 1: [Welcome + value prop]
Screen 2: [Key feature explanation]
Screen 3: [Setup requirements]
Screen 4: [Success state]
```

## Output Template

```
# AI Prototype Prompt

**Target Tool:** [v0.dev / Lovable / Bolt.new]

**Feature:** [Feature Name]

---

## Prompt (Copy-Paste Ready)

[FULL PROMPT HERE]

---

## Instructions

1. Go to [tool URL]
2. Paste the prompt above
3. Click "Generate" or "Build"
4. Wait ~30-60 seconds for prototype
5. Share the generated link

## Expected Output

The prototype will include:
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Iteration Tips

If the prototype needs changes:
- **To adjust styling:** Add "Use [color/font/spacing] instead"
- **To add features:** List new features clearly
- **To remove clutter:** Specify "Remove [feature X]"

## Next Steps

- [ ] Share prototype link with team
- [ ] Gather feedback from stakeholders
- [ ] Iterate on design based on feedback
- [ ] Use as specification for engineering
```

## Pro Tips

1. **Start simple:** Prototype core flow first, add polish later
2. **Use real data:** Sample data should look production-ready
3. **Show edge cases:** Empty states, errors, loading
4. **Be specific:** "Large blue button" > "call-to-action button"
5. **Iterate quickly:** Generate → test → refine → repeat
6. **Share early:** Get feedback on prototype before engineering starts
7. **Document learnings:** Note what works/doesn't for future prototypes

## Common Mistakes to Avoid

❌ Too many features in first prompt (overwhelming)
✅ Core flow first, add features incrementally

❌ Vague descriptions ("nice interface")
✅ Specific details ("Card layout, 3 columns, shadcn components")

❌ No example data (generic placeholders)
✅ Realistic sample data (actual user names, realistic numbers)

❌ Forgetting edge cases (only happy path)
✅ Include empty, loading, error states

❌ No iteration plan (one-and-done)
✅ Expect 2-3 rounds of refinement

## When to Use Each Tool

**Use v0.dev when:**
- Need polished UI components
- Building React/Next.js apps
- Want shadcn/ui integration
- Frontend-only prototype

**Use Lovable when:**
- Need full-stack prototype
- Require authentication/database
- Building complete app MVP
- Want production-ready code

**Use Bolt.new when:**
- Need quick demo (< 10 min)
- Simple component/feature
- No account setup time
- Throwaway prototype

## Output Quality Self-Check

Before delivering the prototype prompt, verify:

- [ ] **Prompt is copy-paste ready** -- No placeholders like "[insert X]" remain; all values are filled in
- [ ] **Tool-specific best practices followed** -- shadcn/ui for v0, Supabase schema for Lovable, simplicity for Bolt
- [ ] **Core user flow is complete** -- The main happy path is fully described, not just individual screens
- [ ] **Edge states specified** -- Empty, loading, error, and success states are included
- [ ] **Sample data is realistic** -- Uses production-like names, numbers, and content (not "Lorem ipsum")
- [ ] **Multi-screen flows are cohesive** -- If multiple screens, navigation, state persistence, and progress indicators are specified
- [ ] **PRD requirements addressed** -- Cross-checked against PRD acceptance criteria (if PRD exists)
- [ ] **Design context included** -- Colors, fonts, and component styles match the product (if design system exists)
- [ ] **Instructions are clear** -- PM knows exactly where to paste, what to expect, and how to iterate

If any check fails, fix it before delivering. The prompt should work on the first try.

---

Remember: A 5-minute prototype can save 2 weeks of engineering waste. Invest in prototyping before building.
