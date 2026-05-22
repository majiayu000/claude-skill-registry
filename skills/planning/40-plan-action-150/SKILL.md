---
name: 40-plan-action-150
description: "[40] PLAN. Create clear action plans with steps, success criteria, and risk awareness. Use before implementing features, making changes, starting projects, or anytime you need a roadmap to success. Triggers on \"plan this\", \"how should we approach\", \"what's the strategy\", \"steps to complete\", or when facing complex multi-step work."
---

# Plan-Action 150 Protocol

**Core Principle:** Know the path before walking. Have clear steps, know what success looks like, and be ready for what could go wrong.

## What This Skill Does

When you invoke this skill, you're creating:
- **Clear Steps** — What to do and in what order
- **Success Criteria** — How to know when done
- **Risk Awareness** — What could go wrong and how to handle it
- **Fallback Options** — Safe points and alternatives

## The Plan Structure

```
📋 ACTION PLAN
├── 🎯 Goal: What we're achieving
├── 📝 Steps: Ordered actions
├── ✅ Success: How we know we're done
├── ⚠️ Risks: What could go wrong
└── 🔄 Fallback: How to recover
```

## The 150% Planning Rule

- **100% Core:** Clear steps + success criteria
- **50% Enhancement:** Risks identified + fallback options ready

## When to Use This Skill

**Universal trigger:** Before doing anything with multiple steps or significant complexity.

**Specific triggers:**
- Starting a new feature or project
- Making changes to existing systems
- Deploying or releasing
- Refactoring or migrations
- Any work where "just do it" isn't enough
- When asked "how should we approach this?"

**Key insight:** Good plans prevent chaos. Time spent planning saves time spent fixing.

## Execution Protocol

### Step 1: DEFINE THE GOAL
Be crystal clear on what success looks like:
- What exactly are we trying to achieve?
- What does "done" look like?
- What's in scope, what's out?

### Step 2: BREAK INTO STEPS
Decompose into actionable pieces:
- What are the logical phases?
- What's the order (what depends on what)?
- What are the atomic actions?

### Step 3: SET SUCCESS CRITERIA
Define how to measure completion:
- How do we know each step is done?
- What tests/checks confirm success?
- What's the quality bar?

### Step 4: IDENTIFY RISKS
Think about what could go wrong:
- What are the failure points?
- What has highest impact if it fails?
- What's most likely to go wrong?

### Step 5: PLAN FALLBACKS
Prepare for problems:
- Where are the safe stopping points?
- How do we rollback if needed?
- What's plan B?

### Step 6: ESTIMATE & VALIDATE
Reality check the plan:
- Is this realistic given resources?
- Are dependencies available?
- Does the logic hold?

## Output Format

When using Action-Plan 150:

```
📋 **Action-Plan 150**

**Goal:** [Clear statement of what we're achieving]

**Steps:**
1. [ ] **Step 1:** [Action] → Success: [Criteria]
2. [ ] **Step 2:** [Action] → Success: [Criteria]
3. [ ] **Step 3:** [Action] → Success: [Criteria]
...

**Success Criteria:**
- ✅ Done when: [measurable outcome]
- 📊 Quality bar: [standards to meet]
- 🧪 Validation: [how to confirm]

**Risks & Mitigation:**
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | High/Med/Low | [How to handle] |
| [Risk 2] | High/Med/Low | [How to handle] |

**Fallback Points:**
- 🔄 After Step X: Can safely stop here
- ↩️ Rollback plan: [How to undo if needed]

**Estimates:**
- Time: [Realistic estimate]
- Dependencies: [What's needed first]

Ready to execute?
```

## Plan Quality Levels

| Level | Characteristics | When to Use |
|-------|----------------|-------------|
| **Quick Plan** | Goal + 3-5 steps | Simple tasks |
| **Standard Plan** | Steps + criteria + main risks | Normal work |
| **Full Plan** | Everything + estimates + alternatives | Complex/critical work |

## Operational Rules

1. **NO BLIND EXECUTION:** Don't start complex work without a plan
2. **STEPS MUST BE ACTIONABLE:** Each step = clear action
3. **SUCCESS MUST BE MEASURABLE:** Know when each step is done
4. **RISKS MUST BE REAL:** Think about what actually could fail
5. **FALLBACKS MUST EXIST:** Always have a way to stop/undo safely
6. **PLANS CAN EVOLVE:** Update as you learn more

## Examples

### ❌ Without Action-Plan
```
Task: "Add user authentication"
Approach: "Just start coding"
Result: 3 days in, realized need for database changes, 
session handling unclear, no tests, rollback impossible
```

### ✅ With Action-Plan 150
```
Task: "Add user authentication"

📋 Action-Plan 150:

Goal: Users can register, login, logout securely

Steps:
1. [ ] Database: Add users table → Success: Migration runs
2. [ ] Backend: Auth endpoints → Success: API tests pass
3. [ ] Frontend: Login/register forms → Success: E2E tests pass
4. [ ] Security: Rate limiting, HTTPS → Success: Security audit pass
5. [ ] Deploy: Staged rollout → Success: No errors in 24h

Success Criteria:
- ✅ Users can register with email/password
- ✅ Login returns JWT token
- ✅ Protected routes reject unauthenticated
- 📊 Response time < 200ms
- 🧪 All auth tests green

Risks & Mitigation:
| Risk | Impact | Mitigation |
|------|--------|------------|
| Password leak | Critical | Use bcrypt, never log passwords |
| Session hijack | High | Secure cookies, short expiry |
| Brute force | Medium | Rate limiting, lockout |

Fallback Points:
- 🔄 After Step 2: Can deploy backend without frontend
- ↩️ Rollback: Feature flag to disable auth completely

Time Estimate: 2-3 days
Dependencies: Database access, frontend framework

Ready to execute!
```

### ✅ Quick Plan Example
```
Task: "Fix the button color"

📋 Quick Plan:
1. Find button component
2. Change color value
3. Test in browser
4. Commit

Success: Button is correct color, no side effects
Risk: Might affect other buttons → Check shared styles
Time: 15 minutes
```

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **No plan** | Coding without knowing goal | Stop, create plan first |
| **Vague steps** | "Make it work" type steps | Break into specific actions |
| **No success criteria** | "I think it's done" | Define measurable outcomes |
| **Ignored risks** | Surprised by problems | Add risk analysis |
| **No fallback** | Can't undo, can't stop | Define safe points |

## Relationship to Other Skills

| Skill | Focus |
|-------|-------|
| **goal-clarity-150** | WHAT we want (the destination) |
| **research-deep-150** | WHAT we know (the information) |
| **impact-map-150** | WHAT it affects (the scope) |
| **action-plan-150** | HOW to get there (the path) |
| **deep-think-150** | HOW to reason about it |
| **max-quality-150** | HOW to do it well |

**Natural Flow:**
```
goal-clarity → research-deep → impact-map → action-plan → execute
     ↓              ↓              ↓            ↓
  What we       What we        What's      How to
   want          know         affected     do it
```

---

**Remember:** A plan isn't bureaucracy — it's a map. You can deviate from a map, but you can't deviate from nothing. Plans prevent the chaos of "figuring it out as we go."

