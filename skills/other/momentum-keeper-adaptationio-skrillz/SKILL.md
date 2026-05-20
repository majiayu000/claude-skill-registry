---
name: momentum-keeper
description: Maintain development momentum and prevent project stalls through progress tracking, blocker resolution, quick wins identification, energy management, and continuation strategies. Task-based operations for detecting stalls, breaking through obstacles, maintaining forward progress, and ensuring completion. Use when progress stalling, facing blockers, losing energy, needing motivation, or ensuring project continuation to completion.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Momentum Keeper

## Overview

momentum-keeper provides systematic strategies for maintaining forward progress and preventing development stalls. It helps detect momentum loss early, identify and resolve blockers, find quick wins, manage energy, and ensure projects continue to completion.

**Purpose**: Keep development moving forward consistently until objectives achieved

**The 6 Momentum Operations**:
1. **Detect Stalls** - Identify momentum loss early before it becomes critical
2. **Resolve Blockers** - Systematically address obstacles preventing progress
3. **Find Quick Wins** - Identify achievable tasks for momentum boost
4. **Manage Energy** - Maintain sustainable pace, prevent burnout
5. **Ensure Continuation** - Strategies for resuming after interruptions
6. **Track to Completion** - Monitor progress toward objectives, ensure finish

**Key Principles**:
- **Prevention Over Recovery**: Detect stalls early, prevent rather than fix
- **Forward Progress**: Any progress > no progress, even small wins matter
- **Systematic Approach**: Use frameworks, not willpower alone
- **Completion Focus**: Start with end in mind, drive toward done
- **Sustainable Pace**: Marathon not sprint, manage energy strategically

**Research Foundation**: Based on productivity research, momentum psychology, and project management best practices

## When to Use

Use momentum-keeper when:

1. **Progress Has Stalled** - No meaningful progress in 24-48 hours
2. **Facing Major Blockers** - Obstacles preventing forward movement
3. **Losing Energy/Motivation** - Feeling stuck, losing interest
4. **After Interruptions** - Resuming work after breaks, context loss
5. **Complex Long Projects** - Multi-week efforts need momentum management
6. **Approaching Completion** - Final push to finish (often hardest part)
7. **Multiple Competing Priorities** - Risk of abandoning projects
8. **Team Coordination** - Keeping group momentum aligned

## Operations

### Operation 1: Detect Stalls

**Purpose**: Identify momentum loss early through progress indicators and warning signs

**When to Use This Operation**:
- Daily/weekly progress checks
- When progress feels slow
- Before it becomes critical stall
- Preventive monitoring

**Stall Indicators**:

**Objective Indicators** (Measurable):
- No completed tasks in 24-48 hours
- Same task "in progress" for >4 hours without completion
- Multiple blocked tasks accumulating
- Burn rate << completion rate (falling behind)
- No commits/updates in 48+ hours

**Subjective Indicators** (Feeling-based):
- Avoiding work on project
- Decreased interest/enthusiasm
- Difficulty starting sessions
- Frequent context switching to other work
- Feeling stuck or overwhelmed

**Process**:

1. **Check Objective Metrics**
   - Last task completed: when?
   - Current task duration: how long?
   - Blocked tasks: how many?
   - Completion rate: on track?

2. **Assess Subjective State**
   - Energy level: high/medium/low?
   - Interest level: high/medium/low?
   - Confidence: high/medium/low?
   - Stuck feeling: yes/no?

3. **Identify Cause Category**
   - **Technical Blocker**: Don't know how, need information
   - **Decision Blocker**: Uncertain about approach, need decision
   - **Complexity Blocker**: Task too large, need breakdown
   - **Energy Blocker**: Low motivation, need energy boost
   - **Context Blocker**: Lost context after interruption

4. **Assess Severity**
   - **Mild** (<48h stall): Early detection, easy recovery
   - **Moderate** (2-4 days): Needs intervention
   - **Severe** (>4 days): Critical, risk of abandonment

5. **Trigger Appropriate Operation**
   - Technical/Decision blocker → Operation 2 (Resolve Blockers)
   - Energy low → Operation 4 (Manage Energy)
   - After interruption → Operation 5 (Ensure Continuation)
   - Need boost → Operation 3 (Find Quick Wins)

**Validation Checklist**:
- [ ] Objective indicators checked (metrics)
- [ ] Subjective state assessed (how you feel)
- [ ] Stall cause identified (blocker type)
- [ ] Severity assessed (mild/moderate/severe)
- [ ] Appropriate operation selected
- [ ] Intervention plan created

**Outputs**:
- Stall assessment (yes/no, severity)
- Identified cause (blocker type)
- Recommended intervention
- Action plan

**Time Estimate**: 10-15 minutes

**Example**:
```
Stall Detection: Skill Development Project
===========================================

Objective Indicators:
✅ Last completed task: 2 hours ago (healthy)
❌ Current task "in progress": 6 hours (too long - should be 1-2h)
❌ Blocked tasks: 2 accumulating
⚠️ Completion rate: 40% but burn rate: 60% (falling behind)

Subjective State:
⚠️ Energy: Medium (not low, but not high)
❌ Interest: Low (avoiding this task)
❌ Confidence: Low (unsure how to proceed)
✅ Stuck: Yes (don't know next step)

Stall Assessment: ⚠️ MODERATE STALL DETECTED

Cause: Technical + Decision Blocker
- Don't know how to implement feature (technical)
- Uncertain about architecture approach (decision)

Severity: Moderate (2 days since meaningful progress)

Recommended Intervention:
1. Operation 2: Resolve Blockers (address technical/decision blockers)
2. Operation 3: Find Quick Win (complete something achievable for momentum boost)

Action Plan:
1. Break current task into smaller pieces (1-2h each)
2. Seek help/research for technical blocker (skill-researcher)
3. Make architecture decision (planning-architect review)
4. Complete one small task today (quick win)
```

---

### Operation 2: Resolve Blockers

**Purpose**: Systematically address obstacles preventing forward progress

**When to Use This Operation**:
- Task blocked >4 hours
- Clear blocker identified
- Progress stopped by specific obstacle
- Multiple blockers accumulating

**Blocker Types and Resolutions**:

**1. Technical Blocker** ("I don't know how to do this")

**Resolution Process**:
- Research: Use skill-researcher to find patterns/solutions
- Ask: Get help from documentation, team, or expert
- Learn: Study similar implementations
- Experiment: Try approaches in isolated test
- Simplify: Reduce scope, do minimal viable version first

**2. Decision Blocker** ("I don't know which approach to take")

**Resolution Process**:
- List options: Enumerate possible approaches
- Criteria: Define decision criteria (speed, quality, maintainability)
- Evaluate: Score options against criteria
- Decide: Choose highest-scoring option
- Move forward: Accept "good enough" decision, iterate if needed

**3. Complexity Blocker** ("This task is too big/complex")

**Resolution Process**:
- Break down: Use task-development to decompose
- Start smallest: Pick simplest piece, complete it
- Build incrementally: Add complexity gradually
- Validate frequently: Ensure each piece works before adding more

**4. Dependency Blocker** ("Waiting on external dependency")

**Resolution Process**:
- Parallel work: Find independent tasks to work on
- Mock/stub: Create temporary placeholder for dependency
- Escalate: Follow up on dependency if delayed
- Adjust plan: If critical, may need to replan

**5. Context Blocker** ("Lost context after interruption")

**Resolution Process**:
- Review artifacts: Read plan, task list, recent work
- Check progress: Use todo-management to see status
- Quick summary: Scan quick references, not full deep dive
- Resume gradually: Start with small task to rebuild context

**Process**:

1. **Identify Blocker Specifically**
   - What exactly is blocking progress?
   - What type of blocker?
   - How long has it blocked?

2. **Apply Resolution Strategy**
   - Use appropriate strategy for blocker type
   - Take concrete action (not just think about it)
   - Set time limit (e.g., 1 hour to resolve or escalate)

3. **Validate Resolution**
   - Is blocker resolved? Can you proceed?
   - If not, escalate or try different approach
   - Update task status (unblock)

4. **Resume Progress**
   - Start working on previously blocked task
   - Mark task in_progress
   - Complete it

5. **Document Learning**
   - What was the blocker?
   - How was it resolved?
   - How to prevent similar blockers?

**Validation Checklist**:
- [ ] Blocker identified specifically
- [ ] Blocker type determined
- [ ] Appropriate resolution strategy applied
- [ ] Concrete action taken (not just planning)
- [ ] Resolution validated (blocker actually resolved)
- [ ] Progress resumed (task in progress again)
- [ ] Learning documented (prevent recurrence)

**Outputs**:
- Resolved blocker
- Resumed progress
- Documented resolution approach
- Prevention strategies

**Time Estimate**: 30-90 minutes (varies by blocker complexity)

**Example**:
```
Blocker Resolution: API Integration Implementation
===================================================

Blocker: Don't know how to handle OAuth token refresh

Type: Technical Blocker
Duration: Blocked for 8 hours
Impact: Can't proceed with implementation

Resolution Strategy: Research + Experiment

Actions Taken:
1. Used skill-researcher Operation 2 (GitHub) - 20 min
   - Found 3 OAuth refresh implementations
   - Identified pattern: refresh before expiry

2. Read OAuth RFC documentation - 15 min
   - Understood refresh token flow
   - Clear on required parameters

3. Implemented minimal test - 25 min
   - Created isolated refresh function
   - Tested with dummy tokens
   - Validated approach works

Resolution Time: 60 minutes

Result: ✅ BLOCKER RESOLVED
- Now understand OAuth refresh flow
- Have working implementation pattern
- Can proceed with integration

Task Status: Unblocked → In Progress → Completed in 2h

Learning: When facing technical blocker, research first (don't experiment blindly)

Prevention: Research OAuth patterns at start of auth work (not when stuck)
```

---

### Operation 3: Find Quick Wins

**Purpose**: Identify and complete achievable tasks for momentum boost and psychological win

**When to Use This Operation**:
- Energy/motivation low
- After completing difficult task (need breather)
- Stalled on complex work (need confidence boost)
- Multiple failures/setbacks (need success)
- Beginning of session (warm up)

**What is a Quick Win?**

**Characteristics**:
- Completable in 15-60 minutes
- Clear, well-defined outcome
- Low complexity
- High confidence can complete
- Tangible result (something done)

**Examples**:
- Add Quick Reference section
- Write README file
- Run validation script
- Fix simple bug
- Update documentation
- Add one example
- Refactor small function

**NOT Quick Wins**:
- Complex features (too big)
- Ambiguous tasks (unclear outcome)
- Blocked tasks (has obstacles)
- Exploratory work (no clear completion)

**Process**:

1. **Scan Todo List**
   - Look for simple, clear tasks
   - Identify tasks you're confident about
   - Find tasks requiring 15-60 minutes
   - Prefer tasks with tangible output

2. **Select Quick Win**
   - Must be achievable now
   - Must have clear completion
   - Prefer visible progress (user-facing)
   - Should feel satisfying when done

3. **Complete It**
   - Focus 100% on this task
   - Complete fully (not partially)
   - Mark as completed
   - Verify done (validation criteria)

4. **Celebrate**
   - Acknowledge completion
   - Note the win (psychological boost)
   - Feel the momentum

5. **Build on Success**
   - Use energy from win for next task
   - Tackle slightly harder task next
   - Ride the momentum wave

**Validation Checklist**:
- [ ] Quick win task identified (15-60 min, achievable)
- [ ] Task completed 100% (not partial)
- [ ] Clear outcome achieved
- [ ] Marked as completed
- [ ] Psychological boost felt
- [ ] Momentum increased
- [ ] Ready for next task

**Outputs**:
- Completed task (quick win)
- Momentum boost
- Increased confidence
- Energy for next tasks

**Time Estimate**: 15-60 minutes (the quick win itself)

**Example**:
```
Quick Win Session: Low Energy Day
==================================

State: Low energy, avoiding complex task (API integration)

Quick Win Search:
- Write README for skill? → 30 min ✅ Achievable
- Add validation to operation? → 45 min ✅ Achievable
- Implement OAuth refresh? → 4h ❌ Too complex (not quick win)
- Run structure validation? → 10 min ✅ Very achievable

Selected Quick Win: Write README for skill (30 min)

Execution:
- Focused on README only
- Completed in 28 minutes
- Result: README.md fully written and validated

Impact:
✅ Tangible progress (README done)
✅ Momentum boost (completed something)
✅ Confidence increase (I can finish things)
✅ Energy higher (ready for next task)

Next Task: Add validation to operations (riding momentum)
- Started immediately after README
- Completed in 42 minutes
- Two wins in one session!

Outcome: Low energy day → 2 completions (README + validation)
Without quick win: Might have stalled all day on complex API task
```

---

### Operation 4: Manage Energy

**Purpose**: Maintain sustainable pace and prevent burnout through strategic energy management

**When to Use This Operation**:
- Feeling fatigued or low energy
- Long sessions (>4 hours)
- After intense work periods
- Planning work sessions
- Sustainable pace needed

**Energy Management Strategies**:

**1. Energy Matching** (Match task to energy level)

**High Energy** (Morning, start of session):
- Complex tasks (architecture, design)
- Creative work (planning, problem-solving)
- High-focus work (critical implementations)
- Decision-making

**Medium Energy** (Mid-session):
- Implementation tasks (following plan)
- Testing and validation
- Documentation writing
- Standard operations

**Low Energy** (End of session, tired):
- Quick wins (simple completions)
- Mechanical tasks (formatting, cleanup)
- Reading/research (passive)
- TODO updates, progress tracking

**2. Strategic Breaks**

**Pomodoro-Style** (25 min work, 5 min break):
- Good for sustained focus
- Regular energy renewal
- Prevents fatigue buildup

**Natural Breaks** (after completing tasks):
- Take break after completing task
- Celebrate completion
- Return refreshed for next task

**Longer Breaks** (every 2-3 hours):
- 15-30 minute breaks
- Physical movement
- Full context switch
- Return energized

**3. Session Planning**

**Ideal Session Structure**:
```
Hour 1: High-energy complex work (architecture, critical decisions)
Hour 2: Medium-energy implementation (following plan)
Hour 3: Break (15-30 min)
Hour 4: Medium-energy continued implementation
Hour 5: Low-energy quick wins, documentation
Hour 6: Wrap-up, todo updates, planning next session
```

**Avoid**: 6+ hours continuous without significant breaks

**4. Momentum Riding**

**Strategy**: Use completion energy for next task immediately

**Application**:
- Complete Task 1 → Immediately start Task 2 (ride momentum)
- Don't take break after completion if energy high
- Chain completions for maximum momentum

**Caution**: Monitor for fatigue, don't override exhaustion signals

**5. Sustainable Pace**

**Marathon Mindset**:
- Consistent progress > sporadic heroics
- 3-4 hours quality work/day > 10 hours mediocre work
- Regular schedule > irregular bursts
- Completion focus > perfection focus

**Process**:

1. **Assess Current Energy**
   - High/medium/low?
   - Trending up or down?
   - Sustainable or approaching burnout?

2. **Match Work to Energy**
   - High energy → complex work
   - Medium energy → implementation
   - Low energy → quick wins, mechanical

3. **Plan Strategic Breaks**
   - Schedule breaks before fatigue
   - Take breaks when energy drops
   - Don't power through exhaustion

4. **Monitor Sustainability**
   - Can you maintain this pace?
   - Are you burning out?
   - Is progress consistent?

5. **Adjust as Needed**
   - Reduce pace if unsustainable
   - Take longer break if fatigued
   - Resume when energy returns

**Validation Checklist**:
- [ ] Energy level assessed honestly
- [ ] Work matched to energy (not fighting fatigue)
- [ ] Breaks taken strategically
- [ ] Pace sustainable (can maintain for duration)
- [ ] No burnout signals (exhaustion, avoidance, errors)
- [ ] Consistent progress maintained

**Outputs**:
- Energy assessment
- Work-energy matching plan
- Break schedule
- Sustainable pace
- Maintained momentum

**Time Estimate**: Ongoing (throughout session)

---

### Operation 5: Ensure Continuation

**Purpose**: Resume work effectively after interruptions, breaks, or context loss

**When to Use This Operation**:
- Returning after overnight/weekend break
- Resuming after interruption (meeting, task switch)
- Starting new session on existing project
- Lost context and need to rebuild

**Continuation Strategies**:

**1. Context Rebuilding** (15-30 min)

**Quick Context Rebuild**:
```
1. Check todo-management (what's in progress? what's next?)
2. Read Quick Reference of relevant skill (not full re-read)
3. Review last completed task (what was I doing?)
4. Check plan/task breakdown (where am I in overall flow?)
5. Start with small task (rebuild flow gradually)
```

**Avoid**: Reading everything from scratch (time-consuming, not necessary)

**2. Momentum Restart**

**Strategy**: Start with quick win to rebuild momentum

**Process**:
1. Don't start with hardest task
2. Pick 30-minute achievable task
3. Complete it (warm up, rebuild context)
4. Use completion energy for harder tasks

**3. Session Preparation** (Before interruption)

**Leave Breadcrumbs**:
```markdown
## Session End Notes (For Resume)

Completed Today:
- Finished X
- Made progress on Y

Next Session Start Here:
- Continue with task #7: [specific next action]
- Context: [brief reminder of what you're doing]
- Quick start: [first concrete step to take]

Blockers to Note:
- [Any blockers to remember]
```

**Benefit**: Reduces resume time from 30 min to 5-10 min

**4. Fresh Start When Needed**

**When to Fresh Start**:
- Context completely lost (>1 week interruption)
- Major context bloat (>70% context window)
- Switching from planning to execution
- Clean slate needed for focus

**How**:
1. Save all artifacts (plans, code, todos)
2. End current session
3. Start fresh session
4. Load only: CLAUDE.md + plan docs + current task
5. Much cleaner context (better performance)

**Process**:

1. **Assess Interruption**
   - How long was break?
   - How much context lost?
   - What was I working on?

2. **Quick Context Rebuild**
   - Check todo status (in progress? next up?)
   - Read Quick References (not full docs)
   - Review session end notes (if left)
   - Check plan for current phase

3. **Select Restart Task**
   - Easy warm-up task (15-30 min)
   - Or continue in-progress task if context clear
   - Not hardest task on list

4. **Execute Restart**
   - Complete restart task
   - Rebuild momentum
   - Proceed to normal work

5. **Maintain Going Forward**
   - Update todos regularly
   - Leave session end notes
   - Keep artifacts organized

**Validation Checklist**:
- [ ] Interruption duration assessed
- [ ] Context rebuilt (todos, quick refs, plans)
- [ ] Restart task selected (achievable warm-up)
- [ ] Momentum rebuilding (not jumping to hardest task)
- [ ] Session end notes left (for future resume)
- [ ] Artifacts organized (plans, todos, code)

**Outputs**:
- Rebuilt context
- Resumed momentum
- Clear next steps
- Progress continuing

**Time Estimate**: 15-45 minutes (context rebuild + warm-up)

---

### Operation 6: Track to Completion

**Purpose**: Monitor progress toward objectives, maintain completion focus, and ensure finish

**When to Use This Operation**:
- Beginning of project (set completion criteria)
- Weekly progress reviews
- When nearing completion (final push)
- When at risk of abandonment

**Completion Tracking Framework**:

**1. Define "Done"**

**At Project Start**:
```markdown
Definition of Done:
- [ ] All planned features implemented
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Quality review passed (score ≥4.0)
- [ ] Deployed/published
```

**Characteristics of Good "Done"**:
- Specific and measurable
- Achievable and realistic
- Clearly defined (not ambiguous)
- Verifiable (can check if met)

**2. Track Completion Metrics**

**Key Metrics**:
```
Completion Rate = Completed Tasks / Total Tasks × 100%

Example: 25 completed / 40 total = 62.5% complete

Remaining Effort = Sum of remaining task estimates

Example: 15 tasks × avg 2h = 30 hours remaining

Estimated Completion Date = Today + (Remaining Effort / Daily Capacity)

Example: 30h remaining ÷ 4h/day = 7.5 days → Complete ~Nov 15
```

**3. The "90% Done" Trap**

**Problem**: Last 10% often takes 50% of time

**Warning Signs**:
- "Almost done" for multiple days
- Completion rate stalled at 85-95%
- Many small tasks remaining
- Polish and perfection seeking

**Solution**:
- Define minimum viable complete (not perfect)
- Time-box final polish (e.g., 2 hours max)
- Ship and iterate (done > perfect)
- Focus on completion, not perfection

**4. Final Push Strategies**

**When**: 90%+ complete, final tasks remaining

**Strategies**:
- **Batch Final Tasks**: Complete all remaining in one focused session
- **Deadline Setting**: "Will finish by Friday" (commitment)
- **Eliminate Scope Creep**: No new features, finish planned work
- **Accept Good Enough**: 90% perfect is shippable, 100% is diminishing returns

**Process**:

1. **Set Completion Criteria**
   - Define what "done" means specifically
   - Create completion checklist
   - Make criteria measurable

2. **Track Progress**
   - Use todo-management for completion rate
   - Calculate remaining effort
   - Estimate completion date
   - Monitor velocity

3. **Maintain Focus**
   - Keep end goal visible
   - Review completion criteria regularly
   - Resist scope creep
   - Celebrate milestones (50%, 75%, 90%)

4. **Final Push**
   - When 90%+ complete, push to finish
   - Batch remaining tasks
   - Accept good enough
   - Ship it

5. **Validate Completion**
   - Check all "done" criteria met
   - Run final validation
   - Confirm ready to ship

**Validation Checklist**:
- [ ] "Done" criteria defined at start
- [ ] Completion rate tracked regularly
- [ ] Progress visible (todos, metrics)
- [ ] Remaining effort estimated
- [ ] Final push executed (when 90%+)
- [ ] Completion criteria met
- [ ] Project actually finished (not abandoned at 95%)

**Outputs**:
- Completion tracking metrics
- Estimated completion date
- Validated completion
- Finished project

**Time Estimate**: Ongoing (throughout project) + final push (varies)

**Example**:
```
Completion Tracking: review-multi Skill
========================================

Definition of Done:
- [ ] All 13 files created
- [ ] SKILL.md complete with 5 operations
- [ ] All reference guides written
- [ ] All scripts functional
- [ ] Structure validation passes (score ≥4)
- [ ] README complete

Progress Tracking:

Week 1:
- Tasks completed: 15/31 (48%)
- Remaining effort: 9 hours estimated
- On track: Yes (projected complete in 3 days)

Week 2:
- Tasks completed: 28/31 (90%)
- Remaining effort: 2 hours
- Final push: 3 tasks remain

Final Push (Day 10):
- Remaining: Validation + testing + summary
- Time-boxed: 2 hours maximum
- Result: All completed in 1.5 hours

Final Validation:
✅ All 13 files created
✅ SKILL.md complete (1,156 lines)
✅ References complete (7 files, 3,690 lines)
✅ Scripts functional (4 files tested)
✅ Structure score: 5/5 (validated)
✅ README complete (421 lines)

Status: ✅ COMPLETE - All completion criteria met
Time: 13 hours actual (14-18h estimated)
Quality: Production ready

SHIPPED! 🎉
```

---

## Best Practices

### 1. Detect Stalls Early
**Practice**: Check progress daily, intervene before critical

**Rationale**: Early detection = easier recovery (mild stall 1h fix, severe stall 1 day+)

**Application**: Daily check: "Made progress? Completed task? Blocked?"

### 2. Resolve Blockers Immediately
**Practice**: Don't let blockers accumulate, address within 4 hours

**Rationale**: Fresh blockers easier to resolve than old ones

**Application**: Task blocked >2 hours → Stop and resolve blocker

### 3. Maintain Quick Win Reserve
**Practice**: Keep list of achievable quick win tasks

**Rationale**: Always have option for momentum boost when energy low

**Application**: Identify 3-5 quick wins at planning phase, save for low-energy moments

### 4. Match Work to Energy
**Practice**: Do complex work when energy high, simple work when low

**Rationale**: Energy is finite resource, use strategically

**Application**: Morning → complex work, afternoon → implementation, evening → documentation

### 5. Leave Breadcrumbs
**Practice**: End each session with notes for next resume

**Rationale**: Reduces resume time from 30 min to 5-10 min

**Application**: Write "Next session start here" notes at end of every session

### 6. Focus on Completion
**Practice**: Finish tasks fully before starting new ones

**Rationale**: Partial completions drain energy, full completions energize

**Application**: Resist temptation to start new task before completing current

### 7. Celebrate Wins
**Practice**: Acknowledge completions, even small ones

**Rationale**: Psychological boost maintains motivation

**Application**: Mark tasks ✅, note achievement, feel the win

### 8. Accept Good Enough
**Practice**: 90% perfect is shippable, don't pursue 100%

**Rationale**: Last 10% often takes 50% of time, diminishing returns

**Application**: When 90%+ done, time-box final polish, then ship

---

## Common Mistakes

### Mistake 1: Ignoring Stall Signals
**Symptom**: Realize week later that no progress made

**Cause**: Not monitoring progress, letting drift happen

**Fix**: Daily progress check, intervene when stall detected

**Prevention**: Operation 1 (Detect Stalls) daily

### Mistake 2: Fighting Blockers Alone Too Long
**Symptom**: Stuck on blocker for days, frustration mounting

**Cause**: Pride, not wanting to ask for help

**Fix**: 4-hour rule - if blocked >4 hours, seek help/research/escalate

**Prevention**: Operation 2 (Resolve Blockers) with time limit

### Mistake 3: No Quick Wins Reserve
**Symptom**: Low energy, no achievable tasks, stall

**Cause**: No backup plan for low-energy moments

**Fix**: Identify 3-5 quick wins now for future low-energy days

**Prevention**: Operation 3 (Find Quick Wins) during planning

### Mistake 4: Powering Through Exhaustion
**Symptom**: Long hours, declining quality, mistakes

**Cause**: Believing more hours = more progress

**Fix**: Stop, take break, resume when energized (quality > quantity)

**Prevention**: Operation 4 (Manage Energy), respect energy limits

### Mistake 5: Not Leaving Resume Notes
**Symptom**: 30+ minutes lost every session rebuilding context

**Cause**: Not documenting session end state

**Fix**: Spend 3 minutes leaving "start here" notes

**Prevention**: Session end routine (Operation 5)

### Mistake 6: Perfectionism Preventing Completion
**Symptom**: Project 95% done for weeks, never ships

**Cause**: Pursuing perfection, afraid to ship

**Fix**: Define "good enough", time-box polish, ship it

**Prevention**: Operation 6 (Track to Completion), accept 90% perfect

---

## Quick Reference

### The 6 Operations

| Operation | Purpose | When to Use | Time | Key Action |
|-----------|---------|-------------|------|------------|
| **Detect Stalls** | Identify momentum loss early | Daily checks, preventive | 10-15m | Check progress indicators |
| **Resolve Blockers** | Address obstacles | Task blocked >4h | 30-90m | Apply resolution strategy |
| **Find Quick Wins** | Momentum boost tasks | Low energy, need win | 15-60m | Complete achievable task |
| **Manage Energy** | Sustainable pace | Long sessions, fatigue | Ongoing | Match work to energy |
| **Ensure Continuation** | Resume after breaks | After interruptions | 15-45m | Rebuild context, warm up |
| **Track to Completion** | Drive to finish | Throughout project | Ongoing | Monitor metrics, final push |

### Stall Indicators

| Indicator | Threshold | Severity |
|-----------|-----------|----------|
| No completed tasks | >24-48h | ⚠️ Moderate |
| Task "in progress" | >4h without completion | ⚠️ Moderate |
| Blocked tasks accumulating | >2 blocked | ⚠️ Moderate |
| Burn rate vs completion | Falling >15% behind | ❌ Severe |
| Feeling stuck | Persistent avoidance | ⚠️ Moderate |

### Energy Levels & Work Matching

| Energy | Work Type | Examples |
|--------|-----------|----------|
| **High** | Complex, creative, decisions | Architecture, design, planning |
| **Medium** | Implementation, standard tasks | Coding, testing, documentation |
| **Low** | Simple, mechanical, passive | Quick wins, cleanup, reading |

### Blocker Resolution Times

| Blocker Type | Typical Resolution | Strategy |
|--------------|-------------------|----------|
| **Technical** | 30-90 min | Research, experiment, ask |
| **Decision** | 15-45 min | List options, criteria, decide |
| **Complexity** | 30-60 min | Break down, start small |
| **Dependency** | Variable | Parallel work, mock, escalate |
| **Context** | 15-30 min | Review artifacts, warm up |

### Completion Metrics

| Metric | Formula | Good Target |
|--------|---------|-------------|
| Completion Rate | Completed / Total × 100% | Trending up |
| Remaining Effort | Sum of remaining estimates | Trending down |
| Velocity | Tasks completed / Time | Stable or increasing |
| Burn Rate | Time spent / Total estimated × 100% | ≈ Completion rate (±10%) |

### Session Structure (Ideal)

```
Hour 1: High-energy complex work
Hour 2: Medium-energy implementation
Hour 3: Break (15-30 min)
Hour 4: Medium-energy continued work
Hour 5: Low-energy quick wins
Hour 6: Wrap-up, session notes
```

**Sustainable**: 3-6 hours focused work/day
**Avoid**: >8 hours continuous (quality degrades)

### Quick Decision Aids

**Should I take a break?**
- Energy dropping? → Yes
- Completed major task? → Yes (celebrate)
- 2+ hours continuous? → Yes (prevention)
- Errors increasing? → Yes (fatigue signal)

**Which task should I do now?**
- High energy? → Most complex available task
- Medium energy? → Standard implementation task
- Low energy? → Quick win or documentation
- Blocked? → Different task or resolve blocker

**Should I ship or continue polishing?**
- >90% complete? → Ship (accept good enough)
- All "done" criteria met? → Ship
- Polishing >4 hours? → Ship (diminishing returns)
- Otherwise → Continue to done criteria

### For More Information

- **Stall detection**: references/stall-detection-guide.md
- **Energy management**: references/energy-management-guide.md
- **Completion strategies**: references/completion-strategies-guide.md

---

**momentum-keeper** ensures continuous forward progress from start to completion through systematic stall prevention, blocker resolution, and strategic energy management.
