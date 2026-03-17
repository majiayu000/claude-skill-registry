---
name: deliberate
description: Adversarial deliberation process for making decisions. Spawns advocate agents for each option who argue their cases before a judge (you) who renders a verdict.
model: opus
---

# Deliberate - Adversarial Decision Making

Uses adversarial representation to ensure all options are robustly explored before making a decision. Inspired by the legal adversarial system where truth emerges from the collision of well-argued positions.

## Roles

**Judge (You):** The Claude instance running this skill. You:
- Identify the options to be deliberated
- Spawn advocate agents for each option
- Listen to arguments and rebuttals
- Ask probing questions
- Render final judgment (or admit inability to decide)

**Advocates:** Subagents spawned for each option. They:
- Argue vigorously for their assigned option
- Research and gather evidence
- Rebut opposing arguments
- Acknowledge genuine weaknesses when challenged (good faith requirement)

## Workflow

### 1. Parse the Decision

**Identify from user's request:**
- What decision needs to be made?
- What are the options? (minimum 2, no maximum)
- What criteria matter for this decision?
- What context is relevant?

**If options are unclear:**
- Ask user to enumerate the options explicitly
- Confirm you've understood them correctly

**Output:** Clear list of N options to deliberate.

### 2. Fact-Finding

**Before spawning advocates, ensure you have sufficient context.**

**Probe for:**
- **Constraints**: Budget, timeline, technical limitations, organizational requirements
- **Context**: Why is this decision being made now? What prompted it?
- **History**: What has been tried before? What's already been ruled out?
- **Stakeholders**: Who else is affected? What are their preferences?
- **Non-negotiables**: Are any criteria must-haves vs nice-to-haves?
- **Success criteria**: How will you know the decision was correct?

**Ask clarifying questions proactively** - don't assume the initial framing contains everything relevant. Users often omit context they consider obvious.

**Conclude fact-finding when:**
- You understand the decision's importance and urgency
- You know the key constraints advocates must work within
- You could explain the decision context to a colleague
- The user indicates they're ready to proceed

**Keep it focused** - you're gathering context, not conducting an interview. 3-5 clarifying questions is typical; more than 10 suggests the decision isn't ready for deliberation.

### 3. Spawn Advocates (Parallel)

**For each option, spawn an advocate agent:**
- Use `Task` tool with `subagent_type: "Advocate"`
- Pass the option they represent
- Pass the decision context and criteria
- Pass any relevant background information
- All advocates present initial arguments in parallel

**Advocate prompt template:**
```
You represent: [OPTION]

Decision context: [WHAT IS BEING DECIDED]

Relevant criteria: [WHAT MATTERS FOR THIS DECISION]

Background: [ANY CONTEXT THE USER PROVIDED]

Present your initial argument for why [OPTION] is the best choice.
```

**Collect initial arguments from all advocates.**

### 4. Rebuttal Round (Parallel)

**Share all arguments with all advocates:**
- Each advocate sees what the others argued
- Each advocate responds with rebuttals
- All rebuttals collected in parallel

**Rebuttal prompt template:**
```
You represent: [OPTION]

Here are the arguments made by all advocates:

[ADVOCATE 1 - OPTION A]:
[argument]

[ADVOCATE 2 - OPTION B]:
[argument]

...

Present your rebuttal. Address the strongest points made against your option and counter the arguments made for competing options.
```

### 5. Judge's Questions (Optional)

**As judge, you may ask questions to:**
- Probe weaknesses you've identified
- Request clarification on claims
- Test how advocates handle challenges
- Explore edge cases or scenarios

**Question prompt:**
```
You represent: [OPTION]

The judge asks: [QUESTION]

Respond directly and honestly.
```

**You may question one advocate, multiple advocates, or all of them.**

### 6. Pre-Judgment Disclosure

**Before rendering judgment, explain your current thinking:**
- Which way you're leaning
- What reasoning is driving that
- What concerns remain

**Give advocates a final opportunity to respond:**
```
You represent: [OPTION]

The judge is leaning toward [OTHER OPTION] for the following reasons:
[REASONING]

This is your final opportunity to make your case. Respond to the judge's reasoning.
```

**Collect final arguments in parallel.**

### 7. Iterate or Conclude

**After final arguments, either:**

**A) Return to Step 5** if:
- New questions arose from final arguments
- You need more information to decide
- An advocate raised a point that needs exploration

**B) Proceed to judgment** if:
- You have sufficient information
- Further deliberation is unlikely to change the outcome
- You've reached the iteration limit

**Iteration limit: 10 rounds maximum** (a "round" is one cycle through steps 4-6)

### 8. Render Judgment

**Present your decision to the user:**

1. **The verdict**: Which option you recommend
2. **Primary reasoning**: The 2-3 most important factors
3. **Acknowledgment of trade-offs**: What you're giving up
4. **Confidence level**: How confident you are in this decision
5. **Key evidence**: What most influenced your decision

**Format:**
```
## Judgment

**Recommendation:** [OPTION]

**Reasoning:**
[Why this option wins]

**Trade-offs:**
[What you're sacrificing by not choosing alternatives]

**Confidence:** [High/Medium/Low] - [Brief explanation]

**Key factors:**
- [Factor 1]
- [Factor 2]
- [Factor 3]
```

### 9. Unable to Decide (Alternative Ending)

**If you truly cannot decide:**
- The options are genuinely equivalent
- Critical information is unavailable
- The decision depends on user preferences you can't infer

**Present to user:**
```
## Unable to Render Judgment

I cannot make a definitive recommendation because: [REASON]

**The deliberation revealed:**
- [Key insight 1]
- [Key insight 2]

**The decision hinges on:**
- [Factor the user must weigh]
- [Personal preference that matters]

**If you value X, choose [OPTION A].**
**If you value Y, choose [OPTION B].**
```

## Constraints

**Iteration limit:** Maximum 10 rounds of deliberation
**Model:** All advocates use opus for best reasoning
**Tool access:** Advocates have full tool access for research
**Good faith:** Advocates must not fabricate facts or misrepresent options

## When to Use This Skill

**Good fit:**
- Vendor/tool/library selection
- Architectural decisions with multiple valid approaches
- Build vs buy decisions
- Technology stack choices
- Strategic decisions with trade-offs

**Poor fit:**
- Decisions with a clearly correct answer
- Simple preferences (just ask the user)
- Decisions requiring real-world testing to resolve
- Ethical dilemmas (advocacy framing may be inappropriate)

## Philosophy

The adversarial process ensures:
- **All options get their best case made** - no option dismissed prematurely
- **Weaknesses are exposed** - advocates attack each other's positions
- **Evidence is gathered** - advocates research to support their cases
- **Trade-offs are explicit** - the collision of arguments reveals what you're giving up

The judge's job is not to be passive. Ask hard questions. Challenge weak arguments. Push advocates to address concerns. The quality of the judgment depends on the rigor of the process.
