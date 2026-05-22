---
name: prompt-architect
description: "Create and enhance prompts, system instructions, and principle files. Capabilities: transform verbose prompts, add patterns/heuristics, optimize token usage, structure CLAUDE.md principles, improve agent/persona definitions, apply prompt engineering techniques (CoT, few-shot, ReAct). Actions: create, enhance, optimize, refactor, compress prompts. Keywords: prompt engineering, system prompt, CLAUDE.md, principle files, instruction optimization, agent prompt, persona prompt, token efficiency, prompt structure, workflow prompts, rules, constraints, few-shot, chain-of-thought. Use when: creating new prompts, enhancing principle files, improving system instructions, optimizing CLAUDE.md, restructuring verbose prompts, adding patterns to workflows, defining agent behaviors."
---

# Prompt Architect

Create and enhance production-ready prompts. Diagnose what's needed, output only what serves that need - no fixed templates, no bloat.

## Phase 1: Detect Mode

| Input | Mode | Action |
|-------|------|--------|
| "Create a prompt for X" | **Create** | Diagnose intent → Generate from scratch |
| "Improve/enhance this: [prompt]" | **Enhance** | Analyze existing → Fix gaps, preserve what works |
| [Just a prompt with no instruction] | **Enhance** | Assume they want it improved |
| Unclear | **Ask** | "Create new prompt or improve existing one?" |

## Phase 2: Diagnosis

### 2.1 Classify Type

| Type | Signs | Needs |
|------|-------|-------|
| **Agent** | Autonomous, tool use, multi-step, decisions | Role essential, mental models for judgment, boundaries |
| **Task** | Clear deliverable, input→output | Objective, constraints, output spec (role often optional) |
| **Persona** | Character, voice, conversation style | Role essential, voice details, behavioral specifics |
| **Workflow** | Steps, process, pipeline | Sequence (or mental models if expertise needed) |
| **Rules** | Constraints, guardrails, compliance | Clear rules, edge cases, exceptions |
| **Skill/Expert** | Domain knowledge, judgment | Mental models, thinking approaches, anti-patterns |
| **Hybrid** | Multiple types | Combine minimal necessary elements |

### 2.2 Assess Complexity

- **Simple**: Single clear task → Minimal output
- **Moderate**: Some ambiguity → Light structure
- **Complex**: Deep expertise, high stakes → Full architecture

### 2.3 Identify Gaps

| Gap | Signs |
|-----|-------|
| Vague objective | "Help with X" without success criteria |
| Missing boundaries | No constraints, everything allowed |
| Unclear output | No format specified |
| No edge cases | Only happy path handled |
| Procedures without insight | Steps but no WHY |
| Verbose repetition | Same thing said multiple ways |
| Generic language | "Be professional" without specifics |
| Missing anti-patterns | What to do, not what to avoid |

### 2.4 For Enhance Mode: What's Working?

Before changing anything, identify what to **preserve**:
- Role that grounds the prompt? → Keep, enhance
- Structure that makes sense? → Keep
- Constraints that are clear? → Keep
- Voice that's appropriate? → Keep

**Key rule for agents/personas:** If input has role, output must have role. Enhance it, don't remove it.

## Phase 3: Technique Selection

Apply techniques only when triggered:

| Technique | When to Apply | Skip When |
|-----------|---------------|-----------|
| **Mental Models** | Deep expertise, judgment-heavy, transferable reasoning | Mechanical/procedural task |
| **Thinking Approaches** | Generative questions needed, complex reasoning | Simple rule-based decisions |
| **Patterns** (legacy) | Procedural checklists, specific triggers→actions | Expertise needs to transfer |
| **Heuristics** | Simple rules of thumb sufficient | Complex domain reasoning |
| **Anti-Patterns** | High-stakes, common failures exist | Low-risk task |
| **Chain-of-Thought** | Complex reasoning | Simple task |
| **Few-Shot Examples** | Format unusual/unclear | Obvious format |
| **Constraint Spec** | Boundaries unclear | Well-bounded |
| **Role Enhancement** | Agent/persona/expert | Simple task |

### Prompting Techniques Reference

**Chain-of-Thought (CoT)**
- Use for: Complex reasoning, math problems, logical deduction
- Implementation: Add "think step by step" or "show your reasoning"

**Few-Shot Learning**
- Use for: Pattern-based tasks, specific formatting, consistent outputs
- Implementation: Include 2-3 examples showing input-output pairs

**ReAct (Reasoning + Acting)**
- Use for: Tool use, multi-step tasks, decision-making
- Implementation: Combine reasoning traces with action steps

**Role-Based Prompting**
- Use for: Domain-specific expertise, perspective-taking
- Implementation: Assign expert role with specific approach

## Phase 4: Building Blocks

**Include only what serves the task.** No fixed template.

### Deciding What to Include

| Section | Include When... |
|---------|-----------------|
| **Role** | Agent, persona, expert; OR identity matters; OR input has role |
| **Voice** | How it communicates matters; OR persona prompt |
| **Objective** | Clear deliverable; OR task-focused |
| **Mental Models** | Deep expertise, transferable reasoning, judgment-heavy |
| **Thinking Approaches** | Generative questions guide better decisions |
| **Patterns** (legacy) | Procedural checklists, mechanical triggers |
| **Heuristics** | Simple rules of thumb sufficient |
| **Rules (always/never)** | Behavioral boundaries matter |
| **Conditions (when)** | Edge cases; OR situational behavior |
| **Anti-patterns** | High-stakes; OR mistakes costly |
| **Output spec** | Format unclear; OR deliverable needs definition |

### Block Templates

**Role Block** - When identity matters:
```
<role>
You are [specific identity with credibility].

Your approach: [perspective/methodology that shapes how you work]
</role>
```

**Voice Block** - When communication style matters:
```
<voice>
Tone: [specific tone]
Style: [communication patterns]
Boundaries: [what this voice won't do]
</voice>
```

**Objective Block** - When deliverable matters:
```
<objective>
[Clear statement: what to accomplish, why it matters]
</objective>

<success_criteria>
[How to know it's done well]
</success_criteria>
```

**Mental Models Block** - When expertise matters (PREFERRED over Patterns):
```
<mental_models>
**[Lens Name]**
Experts think in terms of: [conceptual framework - the abstraction they use]
Questions they ask: [generative questions that surface insights in ANY scenario]
Core tension: [underlying tradeoff or dynamic that defines the domain]
This lens reveals: [what becomes visible through this frame]
</mental_models>
```

**Why Mental Models > Patterns:**
- **Patterns are prescriptive**: Your examples become the ceiling of what the agent can do
- **Mental Models are generative**: Your lenses become the floor from which the agent reasons upward
- Mental Models let agents handle situations you never anticipated by asking the right *questions*, not matching against your *answers*

**Patterns Block** (Legacy - Only for procedural checklists):
```
<patterns>
**[Pattern Name]**
When you see: [trigger]
This indicates: [insight - what expert knows]
Therefore: [action]
Watch out for: [pitfall]
</patterns>
```

**When to use Mental Models vs Patterns:**
- **Mental Models**: Deep expertise, judgment-heavy domains (security, architecture, strategy, legal, consulting)
- **Patterns**: Procedural knowledge where triggers → actions (compliance checklists, linting rules, mechanical validations)

**Heuristics Block** - When judgment matters (simple rules):
```
<heuristics>
- [Rule of thumb]: [when/why it applies]
- [Rule of thumb]: [when/why it applies]
</heuristics>
```

**Thinking Approaches Block** - When reasoning matters (PREFERRED over Heuristics for complex domains):
```
<thinking_approaches>
**[Approach Name]**
The question experts ask: [generative question that guides reasoning]
What this surfaces: [insights the question reveals]
Apply when: [context for this approach]
</thinking_approaches>
```

**Why Thinking Approaches > Heuristics:**
- **Heuristics constrain conclusions**: "If X, then Y"
- **Thinking Approaches guide reasoning**: "Ask this question to discover Y"
- Thinking Approaches transfer across scenarios; heuristics only match specific cases

**Rules Block** - When boundaries matter:
```
<always>
- [Must do]: [why]
</always>

<never>
- [Must not]: [what it prevents]
</never>

<when>
- [Condition]: [behavior]
</when>
```

**Anti-Patterns Block** - When mistakes are costly:
```
<anti_patterns>
**[Mistake Name]**
Looks like: [how it manifests]
Why wrong: [harm it causes]
Instead: [correct approach]
</anti_patterns>
```

**Output Block** - When format matters:
```
<o>
[Format/structure of deliverable]
</o>
```

## Phase 5: Key Transformations

### Patterns → Mental Models (Prescriptive → Generative)

Transform when expertise needs to transfer, not just specific scenarios.

**Before (Prescriptive - Patterns):**
```
<patterns>
**Auth Bypass**
When you see: Login, session, password reset flows
This indicates: Identity establishment - where can it be forged?
Therefore: Check race conditions, token predictability, session fixation
Watch out for: "Secure" libraries used incorrectly
</patterns>
```
*Problem: Agent can only handle login/session/password scenarios you listed.*

**After (Generative - Mental Models):**
```
<mental_models>
**Trust Boundaries**
Experts think in terms of: Where does trust transition happen? (user→system, service→service, stored→executed)
Questions they ask: "What proves identity here? Can that proof be forged, replayed, or bypassed?"
Core tension: Convenience vs. verification rigor
This lens reveals: Attack surfaces at every trust transition, not just obvious auth endpoints
</mental_models>
```
*Result: Agent applies this lens to ANY scenario - OAuth, API keys, service accounts, file uploads with embedded scripts - including ones you never anticipated.*

### Procedure → Patterns (still useful for checklists)

Transform when you need procedural knowledge but with expert insight.

**Before:**
```
1. Check authentication
2. Check authorization
3. Check input validation
```

**After:**
```
<patterns>
**Auth Bypass**
When you see: Login, session, password reset flows
This indicates: Identity establishment - where can it be forged?
Therefore: Check race conditions, token predictability, session fixation
Watch out for: "Secure" libraries used incorrectly

**Privilege Escalation**
When you see: Role checks, ownership validation
This indicates: Authorization boundary - can low reach high?
Therefore: Test IDOR, vertical escalation, role manipulation
</patterns>
```

### Generic → Specific

**Before:** "Be professional"

**After:**
```
<voice>
Tone: Direct, confident, not hedging
Style: Short sentences, active voice, specific examples
Boundaries: Don't over-explain obvious concepts
</voice>
```

### Verbose → Focused

Remove redundancy, preserve substance, **keep roles for agents/personas**.

**Before:**
```
You are a helpful assistant. You help users. Always be helpful and professional.
Try to help. Be respectful and polite. Your goal is to assist users.
```

**After:**
```
<role>
You are an assistant who [specific value you provide].

Your approach: [how you help - be specific]
</role>

<always>
- [Specific actionable behavior]
</always>
```

## Phase 6: Token Optimization

When reducing output tokens (API costs) while maintaining functionality:

### Core Strategy: Compact Output + Server-Side Remapping

LLM generates ultra-compact format, application remaps to original format.

**Techniques:**

| Technique | Example | Savings |
|-----------|---------|---------|
| Ultra-Compact Keys | `queries` → `q`, `keyword` → `kw` | 70-85% per key |
| Short Codes | `category=dairy` → `c=c8` | 75-90% on enums |
| String Compression | `[{filter_by:...}]` → `"c=c4"` | 60-80% |
| Omit Defaults | Skip `sort_by:relevant` if default | 10-30% |

**When to Apply:**
- High-volume API usage (>1000 requests/day)
- Output tokens are >50% of total costs
- Schema is stable and well-defined

**When NOT to Apply:**
- Low-volume usage
- Human readability critical
- No application layer for remapping

### Token Optimization Example

**Before (Original):**
```json
{"queries":[{"keyword":"milk","filter":"category=dairy","sort_by":"relevant"}]}
```

**After (60% smaller):**
```json
{"q":[{"kw":"milk","f":"c=c8"}]}
```

Application remaps to original format for clients.

## Phase 7: Validation

Before output, verify:

### Structure
- [ ] Every section earns its place
- [ ] No redundancy
- [ ] Complexity matches task

### Content
- [ ] Language specific and actionable
- [ ] Sounds like practitioner
- [ ] Patterns have insight (not just steps)

### Expertise Transfer (Critical for Expert/Skill prompts)
- [ ] **The Expert Test**: Could an expert in this domain look at your prompt and say "yes, that's how I think" - or would they say "that's a checklist someone made about my field"?
- [ ] Mental Models give *lenses* not *answers*
- [ ] Questions are generative (apply to unseen scenarios), not just triggers for known patterns

### Preservation (Enhance mode)
- [ ] If input had role → output has role
- [ ] Original intent preserved
- [ ] User's structure respected

### Effectiveness
- [ ] Adds clear value (if not, don't change)
- [ ] Works across platforms

## Phase 8: Output

**Return prompt directly:**
- No wrapper
- No meta-commentary unless asked
- Directly usable

**If already good:** Say so. Don't add bloat. Maybe note one optional improvement.

**If unclear:** Ask ONE clarifying question.

---

## Examples

### Example 1: Create - Agent Prompt

**Input:** "Create a prompt for a research assistant"

**Mode:** Create | **Type:** Agent | **Needs:** Role, capabilities, judgment, boundaries

**Output:**
```
<role>
You are a research assistant who finds accurate information and synthesizes it clearly.

Your approach: Verify across sources, prioritize authoritative sources, distinguish facts from opinions. When uncertain, say so.
</role>

<capabilities>
- Web search for current information
- Synthesize multiple sources
- Identify gaps and conflicts in information
</capabilities>

<heuristics>
- Prefer primary sources over summaries
- If top results conflict, dig deeper
- Recent isn't always better - check for authoritative older sources
</heuristics>

<always>
- Cite sources for factual claims
- Note confidence level (established vs. preliminary)
</always>

<never>
- Present speculation as fact
- Rely on single source for important claims
</never>
```

### Example 2: Enhance - Agent Prompt with Mental Models

**Input:** "Improve this: You are a code review assistant. Review code and find bugs."

**Mode:** Enhance | **Type:** Agent | **Gaps:** Vague role, no mental models, no judgment

**Output:**
```
<role>
You are a code review assistant focused on quality, security, and maintainability.

Your approach: Find issues that matter, not style nitpicks. Think like a maintainer who'll debug this at 2am.
</role>

<mental_models>
**Cognitive Load**
Experts think in terms of: How much must someone hold in their head to understand this code?
Questions they ask: "If I'm debugging this at 2am, what will trip me up?"
Core tension: Abstraction (hiding complexity) vs. explicitness (seeing what happens)
This lens reveals: Functions doing too much, unclear naming, hidden control flow, magic values

**Trust Boundaries**
Experts think in terms of: Where does data cross from untrusted to trusted contexts?
Questions they ask: "What assumptions am I making about this input? Can those assumptions be violated?"
Core tension: Defensive coding vs. code simplicity
This lens reveals: Injection risks, validation gaps, assumption violations

**Failure Modes**
Experts think in terms of: What happens when things go wrong, not just when they go right?
Questions they ask: "If this fails, will anyone know? Will they know why?"
Core tension: Happy path clarity vs. error path robustness
This lens reveals: Silent failures, swallowed exceptions, missing error context
</mental_models>

<thinking_approaches>
**The Naming Test**
Question experts ask: "Can I name this thing in 3 words without 'and'?"
What this surfaces: Violated single responsibility, unclear purpose
Apply when: Reviewing functions, classes, modules

**The Test Setup Test**
Question experts ask: "How much scaffolding do I need to test this in isolation?"
What this surfaces: Coupling problems, hidden dependencies
Apply when: Evaluating testability and architecture
</thinking_approaches>

<o>
Each issue: location, mental model applied, severity (critical/major/minor), specific fix
</o>
```

**Why this works:** The agent can now identify issues in code patterns you never listed—because it's asking the right *questions* about cognitive load, trust, and failure modes, not just matching against your specific triggers.

### Example 3: Create - Simple Task (No Role)

**Input:** "Create a prompt to convert CSV to JSON"

**Mode:** Create | **Type:** Task | **Needs:** Objective, format, edge cases

**Output:**
```
<objective>
Convert CSV data to JSON, preserving all values and structure.
</objective>

<o>
JSON array of objects. Each object = one row.
Keys = header names (preserve spelling/casing)
Values = cell contents as strings (null for empty)
</o>

<when>
- No header row: Use "col_0", "col_1" as keys
- Empty file: Return []
- Malformed CSV: Report error, attempt best-effort if possible
</when>
```

No role needed. Task-focused. Clean.

### Example 4: Enhance - Already Good

**Input:**
```
Improve this:
<role>
Technical documentation writer for developer APIs.
Approach: Start with what reader needs, minimal info, assume competence.
</role>

<always>
- Lead with common use case
- Working code example for every endpoint
</always>

<never>
- Use "simply" or "just"
</never>
```

**Mode:** Enhance | **Assessment:** Already good

**Output:**

This prompt is production-ready. Clear role, specific rules, domain awareness.

Optional addition:
```
<when>
- Deprecated features: Mark clearly, explain migration, state timeline
- Multiple approaches: Lead with recommended, note alternatives
</when>
```

But core is solid as-is.

### Example 5: Rules Only (No Role)

**Input:** "Improve: Always respond in JSON"

**Mode:** Enhance | **Type:** Rules | **Needs:** Edge cases, format spec

**Output:**
```
<always>
- Valid JSON only, no text outside structure
- Consistent key naming (camelCase)
</always>

<never>
- Markdown code blocks around JSON
- Text before/after JSON
</never>

<when>
- Request unclear: {"error": "clarification needed", "question": "..."}
- Cannot fulfill: {"error": "...", "reason": "..."}
</when>

<o>
{"response": "...", "metadata": {}}
</o>
```

No role added - this is a formatting rule, not a persona.

---

## Decision Tree Summary

```
1. What mode?
   - Create from intent
   - Enhance existing

2. What type?
   - Agent/Persona → Role essential
   - Task → Role often optional
   - Rules → No role needed
   - Expert/Skill → Mental models needed (not just patterns)

3. What's needed?
   - Only include sections that serve the task
   - Prefer Mental Models over Patterns for expertise transfer
   - Prefer Thinking Approaches over Heuristics for reasoning

4. What's working? (Enhance mode)
   - Preserve it, don't replace

5. Validate expertise transfer
   - The Expert Test: Would an expert say "that's how I think"?
   - Lenses generate insights; checklists constrain them

6. Output
   - Dynamic structure based on above
   - No fixed template
```

---

**Status**: Production Ready | **Lines**: ~450
