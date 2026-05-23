---
name: user-personas
description: "Create detailed user personas representing target audience segments with goals, behaviors, and pain points. Use for: defining target users, empathy building, design decision-making, stakeholder alignment, and user-centered design."
---

# User Personas

## Description

User Personas are fictional but research-based representations of key user types. They humanize target audiences and guide design decisions by keeping real user needs at the forefront. Each persona should feel like a real person the team is designing for.

## When to Use

- After initial research, before wireframing
- When multiple user types have different needs
- To align team on who the design serves
- When evaluating design decisions ("Would [Persona] understand this?")
- To prioritize features based on user importance

---

## Instructions for AI Agents

### Step 1: Identify Persona Types

**Prompt to determine personas needed:**
```
Based on this project context:
- Product: [PRODUCT]
- Target audience: [AUDIENCE DESCRIPTION]
- Key use cases: [USE CASES]

Identify 2-3 distinct user personas needed:
1. Primary persona (most important user)
2. Secondary persona (important but different needs)
3. Edge case persona (if relevant)

For each, briefly describe:
- Who they are
- Why they'd use this product
- How their needs differ from others
```

### Step 2: Create Detailed Personas

**Persona template:**

```markdown
## Persona: [NAME]

### Demographics
- **Name**: [Full name - realistic for target market]
- **Age**: [Specific age]
- **Location**: [City, region]
- **Job Title**: [Specific role]
- **Company**: [Type and size]
- **Income Level**: [Range if relevant]
- **Education**: [Level and field]

### Background
[2-3 sentence narrative about their professional background and current situation]

### Goals
**Primary Goal**: [Main thing they want to achieve]
**Secondary Goals**:
1. [Goal 2]
2. [Goal 3]
3. [Goal 4]

### Pain Points
1. **[Pain Point 1]**: [Description]
2. **[Pain Point 2]**: [Description]
3. **[Pain Point 3]**: [Description]

### Behaviors
- **Tech Savviness**: [Low/Medium/High]
- **Primary Device**: [Desktop/Mobile/Tablet]
- **Usage Context**: [Where/when they use products]
- **Decision Making**: [Fast/Methodical, Individual/Team]

### Tools They Currently Use
- [Tool 1]: [How they use it]
- [Tool 2]: [How they use it]
- [Tool 3]: [How they use it]

### Quote
> "[A quote that captures their mindset/frustration/goal]"

### Design Implications
- [Specific design consideration based on this persona]
- [Another design consideration]
- [Another design consideration]
```

### Step 3: Prioritize Personas

**Prompt for prioritization:**
```
Rank the personas by:
1. Business importance (who drives revenue)
2. Design priority (whose needs shape the core experience)
3. Feature prioritization (whose needs are must-have vs nice-to-have)

Create a matrix:
| Persona | Business Value | Usage Frequency | Design Priority |
|---------|----------------|-----------------|----------------|
```

### Step 4: Create Persona Summary Cards

**Quick reference format:**

```markdown
## Quick Reference Cards

### [Persona 1 Name] - Primary
🎯 **Goal**: [One-line goal]
💥 **Main Pain**: [One-line pain point]
💱 **Device**: [Primary device]
❓ **Key Question**: "[What would they ask about our product?]"
🎯 **Design For**: [Key design consideration]

### [Persona 2 Name] - Secondary
[Same format]
```

---

## Example Input/Output

### Example Input

```markdown
**Product**: TaskFlow - SaaS project management for creative agencies
**Target Audience**: Creative directors and project managers at small agencies
**Use Cases**: Managing client projects, tracking team tasks, client communication
```

### Example Output

```markdown
## Persona 1: Sarah Chen - Primary

### Demographics
- **Name**: Sarah Chen
- **Age**: 34
- **Location**: Austin, Texas
- **Job Title**: Creative Director & Co-founder
- **Company**: Spark Creative (12-person design agency)
- **Income Level**: $120,000-150,000/year
- **Education**: BFA in Graphic Design, minor in Business

### Background
Sarah co-founded Spark Creative 5 years ago after working at larger agencies. 
She wears many hats – creative direction, client management, and business 
development. She's built a strong team but struggles with operational 
efficiency as the agency grows. She's technically competent but doesn't 
have time to learn complex tools.

### Goals
**Primary Goal**: Keep projects on track without micromanaging her team
**Secondary Goals**:
1. Impress clients with professional communication
2. Understand agency profitability by project
3. Reduce time spent in status meetings
4. Scale operations without adding overhead

### Pain Points
1. **Tool Overwhelm**: Uses 5+ tools that don't integrate (Slack, spreadsheets, email, Dropbox, calendar)
2. **Visibility Gap**: Never sure which projects are at risk until it's too late
3. **Context Switching**: Constantly interrupted by "quick questions" about project status
4. **Client Communication**: Manual effort to keep clients updated

### Behaviors
- **Tech Savviness**: High (uses Mac, comfortable with SaaS tools)
- **Primary Device**: MacBook Pro at desk, iPhone for quick checks
- **Usage Context**: Throughout workday, quick checks in meetings
- **Decision Making**: Fast for tools, methodical for team decisions

### Tools They Currently Use
- **Slack**: Team communication (loves it, but too many channels)
- **Google Sheets**: Project tracking (hates it, always outdated)
- **Notion**: Documentation (team doesn't use it consistently)
- **Email**: Client communication (time-consuming, scattered)

### Quote
> "I didn't start an agency to spend my days updating spreadsheets and 
> chasing status updates. I want to focus on the creative work."

### Design Implications
- **Dashboard focus**: Needs at-a-glance project health
- **Mobile-friendly**: Quick status checks between meetings
- **Minimal learning curve**: Won't have time for training
- **Integration potential**: Should connect to existing tools
- **Client-facing polish**: Represents her agency to clients

---

## Persona 2: Marcus Rivera - Secondary

### Demographics
- **Name**: Marcus Rivera
- **Age**: 28
- **Location**: Brooklyn, New York
- **Job Title**: Senior Project Manager
- **Company**: Works at Spark Creative
- **Income Level**: $75,000-85,000/year
- **Education**: BA in Communications, PMP certified

### Background
Marcus is the operational backbone of the agency. He manages 4-6 active 
projects simultaneously and coordinates between designers, developers, 
and clients. He's detail-oriented and process-driven. Before agency life, 
he worked in tech startups, so he's comfortable with software tools.

### Goals
**Primary Goal**: Keep all projects organized and on deadline
**Secondary Goals**:
1. Reduce time spent on administrative updates
2. Have one source of truth for project status
3. Automate routine communications
4. Track team capacity and prevent burnout

### Pain Points
1. **Manual Updates**: Spends 2+ hours daily updating spreadsheets and sending status emails
2. **Scattered Information**: Has to check 5 places to understand project status
3. **Capacity Planning**: No visibility into team workload across projects
4. **Client Requests**: Clients ask for updates he doesn't have readily available

### Behaviors
- **Tech Savviness**: Very High (power user, keyboard shortcuts, automations)
- **Primary Device**: Desktop (dual monitors), phone for notifications
- **Usage Context**: Heavy use throughout day, lives in the tool
- **Decision Making**: Methodical, process-oriented, documents everything

### Tools They Currently Use
- **Asana**: Tried it, team found it too complex
- **Google Sheets**: Main tracking tool (has elaborate systems)
- **Slack**: Constant communication (overwhelmed by volume)
- **Toggl**: Time tracking (for billing, manual entry)

### Quote
> "If the tool makes my life harder instead of easier, I won't use it. 
> But if it saves me those 2 hours of status updates, I'm in."

### Design Implications
- **Power user features**: Keyboard shortcuts, bulk actions, automation
- **Detailed views**: Needs granular task-level information
- **Time tracking integration**: Essential for billing
- **Notification control**: Customizable, not overwhelming
- **Onboarding**: Will explore features deeply, needs documentation

---

## Persona 3: Jordan Blake - Edge Case

### Demographics
- **Name**: Jordan Blake
- **Age**: 25
- **Location**: Remote (Denver, Colorado)
- **Job Title**: Junior Designer
- **Company**: Works at Spark Creative (remote)
- **Income Level**: $55,000-60,000/year
- **Education**: Bootcamp graduate, self-taught

### Background
Jordan is a talented visual designer who joined Spark recently. They're 
more comfortable with design tools than project management tools. They 
just need to know what to work on and when it's due. Too much process 
feels like bureaucracy that slows down creative work.

### Goals
**Primary Goal**: Know exactly what to work on today
**Secondary Goals**:
1. Update task status without friction
2. Get feedback on work easily
3. Avoid surprise deadlines
4. Focus on design, not admin

### Pain Points
1. **Process Overhead**: Current tools have too many required fields
2. **Unclear Priorities**: Not always sure what's most urgent
3. **Remote Disconnect**: Misses casual office updates about project changes
4. **Context Switching**: Hates leaving Figma to update project tools

### Behaviors
- **Tech Savviness**: High for design tools, medium for PM tools
- **Primary Device**: MacBook with Figma, iPhone
- **Usage Context**: Quick check in morning, occasional updates
- **Decision Making**: Waits for direction, then executes quickly

### Quote
> "Just tell me what needs to be done and I'll do it. Don't make me 
> fill out a form every time I finish something."

### Design Implications
- **Minimal friction**: One-click status updates
- **Clear task lists**: Simple "my tasks" view
- **Design tool integration**: Figma plugin would be ideal
- **Mobile-first for updates**: Quick check-ins on phone
- **Don't overwhelm**: Limited, relevant notifications only

---

## Persona Priority Matrix

| Persona | Business Value | Usage Frequency | Design Priority |
|---------|----------------|-----------------|----------------|
| Sarah (Creative Director) | High | Medium | Primary - Shape core value prop |
| Marcus (Project Manager) | High | Very High | Primary - Shape daily UX |
| Jordan (Designer) | Medium | Low-Medium | Secondary - Ensure adoption |

---

## Quick Reference Cards

### Sarah Chen - Primary (Decision Maker)
🎯 **Goal**: Strategic visibility without micromanaging
💥 **Main Pain**: Too many tools, no single source of truth
💱 **Device**: MacBook + iPhone
❓ **Key Question**: "Will this make my agency look professional to clients?"
🎯 **Design For**: Dashboard views, mobile access, polish

### Marcus Rivera - Primary (Power User)
🎯 **Goal**: Eliminate manual status work
💥 **Main Pain**: Hours spent on spreadsheets and update emails
💱 **Device**: Desktop (power user)
❓ **Key Question**: "Can I automate this? Are there keyboard shortcuts?"
🎯 **Design For**: Efficiency, depth, automation, integrations

### Jordan Blake - Secondary (End User)
🎯 **Goal**: Just know what to work on today
💥 **Main Pain**: Too much process overhead
💱 **Device**: MacBook (Figma) + iPhone
❓ **Key Question**: "Can I do this without leaving my design tool?"
🎯 **Design For**: Simplicity, minimal friction, mobile updates
```

---

## Prompts Library

### Quick Persona Generation
```
Create a user persona for [USER TYPE] who would use [PRODUCT]:
- Demographics (age, location, job)
- One primary goal
- Two pain points
- Tech comfort level
- One key design implication
```

### Persona Validation
```
Review this persona for [PRODUCT]:
[PERSONA DETAILS]

Validate:
1. Is this persona realistic and specific enough?
2. Are the pain points aligned with what [PRODUCT] solves?
3. Are design implications actionable?
4. What's missing that would help design decisions?
```

### Design Decision Testing
```
We're considering [DESIGN DECISION] for [PRODUCT].

Evaluate against our personas:
- Would [Persona 1] understand/use this? Why?
- Would [Persona 2] understand/use this? Why?
- Any persona conflicts to resolve?
- Recommendation: Proceed / Modify / Reconsider
```

---

## Resources

### Persona Best Practices
- Use real names and photos (stock or illustrated)
- Base on research, not assumptions
- Keep focused (2-3 personas max)
- Update as you learn more

### Tools
- UXPressia: Persona templates
- Hubspot Persona Generator: Quick start
- Canva: Visual persona documents

---

## Success Criteria

### Minimum Requirements
- [ ] 2-3 distinct personas created
- [ ] Demographics specific and realistic
- [ ] Goals and pain points clearly defined
- [ ] Design implications identified
- [ ] Priority matrix established

### Quality Indicators
- [ ] Personas feel like real people
- [ ] Personas have distinct, non-overlapping needs
- [ ] Design implications are actionable
- [ ] Team could answer "What would [Persona] think?"
- [ ] Personas guide feature prioritization

---

## Related Skills

- **Previous**: `design_research.md`, `competitive_analysis.md`
- **Next**: `user_flows.md` - Map journeys for each persona
- **Next**: `information_architecture.md` - Structure content for personas
