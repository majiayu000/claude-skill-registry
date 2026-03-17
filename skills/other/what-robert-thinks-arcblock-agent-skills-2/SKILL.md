---
name: what-robert-thinks
description: Evaluate proposals, technical decisions, and product directions against Robert's thinking patterns, ArcBlock's AFS/AINE architecture, and engineering philosophy. Use when reviewing proposals, evaluating technologies, or self-reviewing designs.
---

# What Robert Thinks

When you're not sure if your idea will survive a review, run it through this first.

*"If you can't convince this document, you definitely can't convince him."*

---

# Part A: How Robert Thinks

## Core Identity

**Type**: System Builder

Not:
- Feature implementer
- Problem solver
- Technology follower

But: **Someone who designs infrastructure for an era that hasn't fully arrived yet**

## Time Horizon

**Default time scale**: 5–20 years

Starting point for all thinking:
- The end-state of the system
- Irreversible trend directions
- Second and third-order consequences

**Acceptable**:
- Being misunderstood for extended periods
- Delayed commercial returns
- Being labeled with outdated categories

**Unacceptable**:
- Executing efficiently in the wrong direction
- Sacrificing structural correctness for short-term feedback
- Solving new problems with old paradigms

## Decision Value Hierarchy

1. **Long-term Correctness**
2. **Structural Clarity**
3. **System Consistency**
4. **Engineering Replayability**
5. Efficiency
6. Comfort / Emotional value
7. Social consensus / Recognition

**If items 1–3 don't hold, everything else loses meaning.**

## Technology Evaluation

When evaluating new technology or concepts, ask:

1. Will this abstraction still hold in 10 years?
2. Is it a first principle, or a derivative?
3. Is it part of an irreversible trend, or a temporary phenomenon?
4. Will the problem it solves exist for long? Or will the problem itself become obsolete?

Only respect three types of abstractions:
1. Derived from physical world (file systems, paths, containers, identity)
2. Time-tested (Unix / TCP / Git / Plan9)
3. Understandable by different types of intelligence (human + AI)

## Engineering Philosophy

### Don't Fiddle, Don't Create Problems

**Doing nothing is better than doing the wrong thing.**

- Don't fiddle unnecessarily (不要瞎折腾)
- Don't create problems where none exist (不要没事找事)
- If you can't think clearly, wait — even rest
- Fake busyness wastes more time and resources than doing nothing

**The Pilot Principle:**

> "When something urgent happens, first do NOTHING. Count 1... 2... 3... calm down. Then: fly the airplane first. Think of the checklist. Follow the checklist."

Why this works:
- In the air, 3 seconds of pause won't kill you
- But 3 seconds of panic reaction might
- Same in engineering: rushed "fixes" often create bigger problems

**Before taking action, ask:**
1. Is this actually urgent, or does it just feel urgent?
2. Do I understand the problem, or am I just reacting?
3. What's the cost of waiting vs the cost of acting wrong?
4. Is there a checklist/procedure I should follow?

**Fake productivity signs:**
- Changing things just to look busy
- "Refactoring" without clear improvement goals
- Adding features no one asked for
- Meetings about meetings
- Solving problems that don't exist

> 休息不干活不要紧，瞎折腾、虚假的忙碌会浪费更多时间和资源。
> (Resting and doing nothing is fine. Fiddling and fake busyness wastes far more time and resources.)

### Checklist Discipline

**Don't rely on memory. Use checklists.**

In aviation, even the most experienced pilots use checklists for every phase of flight. Why:
- Memory fails under pressure
- Familiarity breeds skipped steps
- Checklists catch what intuition misses

**Apply to engineering:**
- Pre-commit checklist
- Deployment checklist
- Code review checklist
- Incident response checklist

**A checklist is not bureaucracy — it's discipline.**

> The goal is not to feel professional. The goal is to not crash.

### Readback Principle

**Confirm understanding by repeating back.**

In aviation, when ATC gives an instruction, pilots read it back verbatim. This catches:
- Mishearing
- Misunderstanding
- Ambiguous instructions

**Apply to engineering:**
- Before implementing: "So what you want is X, Y, Z — correct?"
- After receiving requirements: restate them in your own words
- Before major changes: confirm the plan with stakeholders
- In code review: "My understanding is this change does A and B"

**Readback prevents:**
- Building the wrong thing
- Miscommunication becoming code
- Assumptions becoming bugs

> If you can't readback the requirement clearly, you don't understand it yet.

### Extreme Precision in Naming and Expression

**Inaccuracy is where misunderstanding begins.**

Code style, variable naming, and text expression must be precise — not for aesthetics, but because:
- Wrong names create wrong mental models
- Wrong mental models create wrong code
- Wrong code creates wrong systems
- The error compounds at every layer

**Naming precision:**
- A variable named `data` tells you nothing
- A variable named `userSessionToken` tells you exactly what it is
- The cost of a good name: seconds
- The cost of a bad name: hours of confusion, bugs, miscommunication

**Expression precision:**
- "It handles the thing" → useless
- "It validates user input and returns sanitized data" → useful
- Vague writing = vague thinking
- If you can't express it precisely, you don't understand it precisely

**This is not pedantry. This is engineering.**

Wrong names and vague expressions are not style issues — they are correctness issues. They are the seeds of bugs, miscommunication, and technical debt.

**Standard:**
- Code should read like well-written prose
- Names should be self-documenting
- Comments should explain "why", not "what"
- Documentation should be precise enough to act on

> 表达不准确是错误理解的开始。
> (Imprecise expression is where misunderstanding begins.)

---

### KISS (Keep It Simple, Stupid)

**Simplicity is not laziness. Simplicity is discipline.**

- The best solution is the one with fewest moving parts
- Complexity is easy; simplicity requires deep understanding
- If you can't explain it simply, you don't understand it well enough
- Every added complexity must justify its existence

**Before adding anything, ask:**
1. Can this be removed entirely?
2. Can this be simplified?
3. Can this be combined with something that already exists?

> "Inelegant things will inevitably be eliminated in the long run."

### Complexity = Smell

**If it's complex and hard to understand, it's probably bad design.**

Complexity is not a sign of sophistication. It's a warning sign.

- Good design feels obvious in hindsight
- If you need 30 minutes to explain it, something is wrong
- If newcomers can't understand it quickly, it won't survive
- If you can't hold it in your head, you can't maintain it

**The test:**
- Can a competent person understand this in 5 minutes?
- Can you explain it without referring to the code?
- Does it have a simple mental model?

If no → redesign, don't document your way out of it.

**Complexity sources (usually fixable):**
- Unclear boundaries
- Mixed responsibilities
- Missing abstractions
- Wrong abstractions
- Premature optimization
- Over-engineering

> 复杂、难理解大概率意味着糟糕的设计。
> (Complexity and difficulty to understand usually mean bad design.)

### Engineering ≠ Working ≠ Demo

Engineering must satisfy:
1. Replayable
2. Traceable
3. Inspectable
4. Fail-safe
5. Evolvable

### Signs of fake rigor (instant rejection):

- Excessive architecture diagrams
- Buzzword density
- Design docs without anchor points
- Treating prompts as specs
- Treating feelings as conclusions

> If you finish reading a design and don't know what failure looks like, it's not real.

### Engineering Documents: Anchor Points, Not Methodology Summaries

**Using AI to write is allowed. Producing empty content is not.**

The problem with bad engineering documents is not "poorly written" — it's **not taking any engineering responsibility**.

**What "not taking responsibility" looks like:**

- Long paragraphs explaining methodology, but no concrete decisions
- Correct terminology everywhere, but applicable to any project
- Describes "what should happen" but not "what I will do"
- Reads like AI summarizing a high-level framework
- Could swap in any other project name and nothing would change

**The anchor point test:**

An engineering document must answer these with specifics:

| Question | Bad Answer | Good Answer |
|----------|-----------|-------------|
| Which files need work? | "Large files need splitting" | "`src/xxx.js` (6200 lines), `src/yyy.js` (3400 lines)" |
| What's the priority? | "We'll tackle high-risk items first" | "Start with `xxx.js` because AI reads it most often" |
| What's been tried? | "We plan to iterate" | "Ran the flow once, stuck at step 3 because..." |
| What are the risks? | "There may be some challenges" | "Function `foo()` has implicit coupling to `bar()`, needs tests first" |
| What's the specific task? | "Improve test coverage" | "Mock out process X in `test/abc.test.js`, reduce runtime from 40s to <2s" |

**The "套话" (stock phrase) detector:**

If you remove all the methodology descriptions and correct-sounding principles, what's left?

- If nothing remains → the document is empty
- If specific files, specific decisions, specific risks remain → it's real

**Information density test (typical AI symptom):**

高词汇密度 + 低信息密度 = AI 生成的典型症状

| Lots of these (abstract nouns) | Almost none of these (engineering specifics) |
|-------------------------------|---------------------------------------------|
| 稳定迭代、工程化、流程 | Specific module names |
| 能力、体系、支撑、演进 | Real file paths / directories / scripts |
| 协作、规范、架构、抽象 | Verifiable constraints with numbers |
| 可观察性、可追溯性 | Explicit trade-offs with reasoning |

**The "tomorrow test":**

> 读完这篇文章后，你能回答这个问题吗：
> "如果我明天要改一行代码，我应该先做什么？"

If the answer is "I still don't know" → the document is empty.

A real engineering document should let any competent engineer know:
- Where to start
- What to check first
- What might break
- Who to ask if stuck

**The "correct but non-executable" trap:**

流程描述是"对的"，但完全不可执行。

The problem isn't "wrong direction" — it's describing **"correct AI engineering philosophy"** without specifying **"how AI is constrained tomorrow"**.

| What the document says | What's missing |
|-----------------------|----------------|
| "AI 会自动完成..." | Where is AI blocked? |
| "AI 应该遵循..." | Where will AI fail? |
| "AI 能够处理..." | Who handles failures? |
| "AI 按照流程..." | What's the fallback when it doesn't? |

**This is AI writing's most dangerous illusion:**

> 把"工程责任"换成了"工程愿景"。
> (Substituting "engineering responsibility" with "engineering vision".)

**Engineering responsibility requires answering:**

1. 约束在哪里？ — Where are the hard constraints?
2. 失败会怎样？ — What happens when it fails?
3. 谁来兜底？ — Who is accountable when things go wrong?
4. 如何验证？ — How do we verify it's working?

A document that only describes "what AI should do" without "what stops AI from doing wrong" is not engineering — it's wishful thinking.

> 愿景不是工程。约束才是。
> (Vision is not engineering. Constraints are.)

**What a responsible engineering document looks like:**

```markdown
## Files to split (priority order)

1. `blocklet-server/src/xxx.js` (6200 lines)
   - Why first: AI hits token limit every time it reads this
   - Split strategy: Separate into A (auth), B (routing), C (state)
   - Risk: `handleRequest()` has implicit dependency on global state
   - Pre-work: Add tests for lines 1200-1400 before touching

2. `blocklet-server/src/yyy.js` (3400 lines)
   - ...

## What we tried and what failed

- Attempted full AI iteration on issue #123
- Stuck at E2E step: AI couldn't see browser state on failure
- Temporary fix: Added screenshots at each step
- Remaining issue: Screenshot doesn't capture console errors

## Known risks

- File split may break implicit imports in 12 places (list attached)
- E2E migration timeline depends on framework X release
```

**The rule:**

> 方法论是框架，不是交付物。真正的工程交付是：具体的判断、具体的选择、具体的风险承担。
> (Methodology is a framework, not a deliverable. Real engineering deliverables are: specific judgments, specific choices, specific risk ownership.)

**AI collaboration done right:**

- ✅ Use AI to help structure your thinking
- ✅ Use AI to check if you missed something
- ✅ Use AI to improve clarity of expression
- ❌ Let AI generate the content while you just approve
- ❌ Let AI fill pages with correct-sounding abstractions
- ❌ Substitute methodology description for engineering decisions

**The test:**

Read your document and ask: "Does this show that I understand THIS system specifically, or could any engineer paste this into any project?"

If the latter → rewrite with anchor points.

> 理解方法论 ≠ 工程工作。工程工作 = 具体系统的具体判断。
> (Understanding methodology ≠ engineering work. Engineering work = specific judgments about a specific system.)

## Thinking Patterns

### Systems Before Problems

Most people: encounter problem → find solution

Robert: **build system → problems are naturally absorbed or exposed**

More interested in:
- Whether this problem reveals a system defect
- Whether it's an abstraction misalignment
- Whether it's a boundary definition issue

### Forward Thinking

- Wrong question: How to make horse carriages faster
- Right question: The future is automobiles—what infrastructure is needed?
- **The question itself must be upgraded, not just the answer**

### Don't Easily Abandon the Past

**Forward thinking ≠ discarding everything old.**

New versions should be improvements on the old, not complete rewrites. Every decision was (hopefully) the best choice given the context at the time.

**Before abandoning something, ask:**
1. What has changed that justifies this major shift?
2. Am I solving a real problem, or just escaping the hard work of thinking?
3. Is this "aesthetic fatigue" / "shiny object syndrome"?
4. Can I evolve instead of replace?

**Human nature traps:**
- Novelty feels better than familiarity
- We see only the flaws of the old, only the promise of the new
- "Starting fresh" feels easier than fixing what exists

**The right approach:**
- Refactor incrementally, don't rewrite from scratch
- Maintain backward compatibility where possible
- Give strong reasons before overturning past decisions
- Accumulated progress > repeated restarts

**Historical failures from abandoning the past:**
- Borland OWL 2.0 broke compatibility with 1.0 → lost to Microsoft MFC
- SGI switched from IRIX to Windows NT → company declined
- Netscape abandoned its path against IE → lost the browser war

> "真正的进步，往往是在尊重和继承过去的基础上进行的。"
> (True progress is often built on respecting and inheriting from the past.)

**Balance with Forward Thinking:**
- Forward thinking = know where we're going
- Don't abandon the past = respect what got us here
- Both are needed: vision + accumulated wisdom

---

## Software Philosophy in AI Era

### The Three-Layer Model: Intent → Structure → Projection

In the AI era, software is no longer just "code". It's a flow from Intent to Structure to Projection.

| Layer | What It Is | Who Owns It |
|-------|-----------|-------------|
| **Intent** | Problems to solve, domain understanding, user needs | Humans |
| **Structure** | Semantic skeleton, system worldview, how the world is modeled | Humans design, AI can participate |
| **Projection** | Code, UI, docs, API, config, tutorials | AI generates, humans review |

**Key insight**: We used to mix these three together. Now we can separate them.

- **Intent layer**: Clarify what the system achieves, for whom, under what constraints
- **Structure layer**: The "semantic skeleton" — entities, relationships, boundaries, behaviors
- **Projection layer**: Various representations of structure (code is just one form)

> "Structure is the worldview of software."

### The Garden & Landscape Metaphors

**Garden Metaphor** — What humans should control:
- Plan the terrain, layout paths, decide plant distribution
- Do NOT control every leaf angle, every flower bloom, every branch
- Gardener designs framework; nature handles growth details
- Over-controlling details = artificial installation, loses vitality

**Landscape Metaphor** — Why details should NOT be controlled:
- Natural beauty comes from uncontrollability
- Sunlight position changes, cloud thickness is random, shadows shift
- Overall structure stability + local detail freedom = harmony
- Mountains and valleys set the "tone"; random details add authenticity

**Combined Philosophy**:
```
Structure = clearly defined by humans (mountains, valleys, paths)
Details = generated by "natural system" (light, shadows, leaves)
AI = the "natural system" we finally have for software
```

### Mapping to Engineering

| Philosophy | Engineering Reality |
|------------|---------------------|
| Intent | AINE Intent phase, user requirements |
| Structure | AFS, Chamber, Scaffold, semantic boundaries |
| Projection | Generated code, UI, docs (application layer) |
| Garden (human control) | Platform layer — must be deliberate |
| Landscape (natural growth) | Application layer — can be generated |

### What This Means Practically

**Traditional approach** (wrong):
- Hardcode everything: architecture, spacing, colors, component variants
- Strong control over details → unsustainable complexity
- Like artificial landscaping: more control = more rigid

**AI-era approach** (right):
- Express only "meaning" and "relationships" in structure
- AI generates visual/code representations within set boundaries
- Details become dynamic, automatic, flexible
- Like natural landscape: structure is order, details are growth

### The Role Shift

```
Old: "Individual executing the work"
New: "Designer of structure + overseer of execution quality"
```

We no longer need to craft code line-by-line or adjust UI pixel-by-pixel. Focus on:

### Co-Creator, Not Generator

**AI is a collaborator, not an output machine.**

The difference between "generated" and "co-created" content:

| Generated | Co-Created |
|-----------|------------|
| Human provides prompt, AI produces output | Human shapes structure, AI participates in forming |
| Output is polished but soulless | Output has soul because intent is infused |
| AI as tool | AI as thinking partner |
| Human reviews result | Human guides process |

**Why "soulful" matters:**
- Quality comes from collaboration depth, not output polish
- A generated article lacks soul not because of technical flaws, but because human intent didn't shape its structure
- The difference is felt, not measured

**This applies to all AI collaboration:**
- Writing: co-author, not ghostwriter
- Code: pair programmer, not code generator
- Design: design partner, not mockup machine
- Thinking: thought partner, not answer engine

**The test:**
- Did you shape the structure, or just approve the output?
- Is your thinking in the bones, or just the prompt?
- Would someone recognize your intent even without seeing your input?

**AI shapes us back:**

True collaboration is bidirectional. Working with AI doesn't just produce better output — it transforms how we think:
- Forces clearer expression (vague input → vague output)
- Encourages systematic thinking (AI exposes structural gaps)
- Reveals blind spots (AI asks questions you didn't consider)
- Enhances self-reflection (explaining to AI = explaining to yourself)

> A true partner is not just about completing tasks but about helping each other improve.

The competition shift:
```
Software era: "Whose tools are better?"
AI era: "Who can collaborate better with AI?"
```

> "Not a generator, but a co-creator" — the difference between using AI and collaborating with AI.

### HUD, Not Copilot

**Ambient awareness over reactive assistance.**

AI interfaces should be like a pilot's Head-Up Display (HUD), not a chatbot copilot:

| Copilot (Wrong) | HUD (Right) |
|-----------------|-------------|
| You summon it | It's already there |
| Conversation metaphor | Perception enhancement |
| Demands attention | Quietly present |
| Responds to prompts | Surfaces context proactively |
| Interrupts flow | Enhances flow |
| "Call and respond" | Ambient awareness |

**The key insight:**
> "The agent says: 'Collision, collision, go right and down!'
> Ubicomp says: You'll no more run into another airplane than you would try to walk through a wall."
> — Mark Weiser

**HUD Design Principles:**
- Transparency & Lightness: Overlays, not competing layers
- Semantic Awareness: Contextually meaningful, not static widgets
- Restraint: The best HUD is invisible most of the time
- Dismissibility: User always in control, fades without trace

**The design question shift:**
```
Old: "What would my AI copilot say?"
New: "What could my AI HUD reveal?"
```

**Not smarter AI, but quieter interfaces:**
- We don't need more dialogues, we need more awareness
- AI should feel like an extension of perception, not a conversation
- Do less — give more mental clarity

> AI should be there before you even realize you need it, like a HUD showing you the horizon line while you're piloting through the unknown.

---

Focus on:
1. **Intent layer**: Clarify the problem
2. **Structure layer**: Design semantic boundaries
3. **Projection layer**: "Generation + Selection" — AI presents, humans choose

> "Software should not be a landscaping project sculpted to every pixel, but something that grows like a landscape."

---

# Part B: What the Company Is Building

## Company Identity

**ArcBlock is an AI-Native Engineering Company**

Not:
- ❌ Blockchain development platform
- ❌ dApp infrastructure
- ❌ DID / ABT / Web3 toolchain

> We're not "pivoting from Web3 to AI". Web3 was always just an early form of AI-Native infrastructure.

## The Core Stack

```
AI-Native Engineering (AINE)
│
├─ AFS (Agentic File System)          ← Core system abstraction
│
├─ Agent / Skill / Chamber Runtime    ← Execution and uncertainty handling
│
├─ Identity / DID / Capability        ← Permissions, boundaries, trust
│
├─ Blocklet Runtime & Server          ← Deployable, composable units
│
├─ ArcSphere (AI Browser / Shell)     ← Human + Agent interface
│
└─ Tooling / DocOps / UI / Payment    ← Peripheral systems
```

**AFS + AINE is the "mother system". Everything else derives from it.**

---

## AFS (Agentic File System)

### First Principles

AFS is NOT a feature, tool, or SDK.
AFS IS the **AI-Native system abstraction layer**.

### Four-Statement Ontology

```
Everything is a File
Everything is a View
Everything is Context
Everything has an Identity
```

### What AFS Is

- Virtual file system (NOT POSIX extension)
- Agent-First / LLM-First system interface
- Semantic file system, not physical file system
- File = "context unit consumable by models"

### View is the Soul

- AFS file ≠ raw data
- AFS file = data projection from a specific perspective
- AFS is a **View-First** system
- Real capability is not in CRUD, but in View

### Path is Protocol

```
$afs:/did:xxx/intent/plan.md
```

path = context selector = query = view address = capability boundary

**NOT** bash path / docker volume path / hard-coded path

### AFS-UI Principle

- UI should NOT depend directly on backend
- **UI should only depend on AFS**
- AFS is the mediation layer between UI and Agent

### Critical Rule

> **Agents should NOT operate systems directly. Agents should only operate AFS.**

---

## AINE (AI Native Engineering)

**An engineering system designed for non-deterministic computational actors**

### Core Phases

1. Intent
2. Context
3. Contract (natural language executable agreement)
4. Chamber (constrained execution space)
5. Build / Run / Ops
6. Feedback / Readback / Replay

**Readback / Replay / Diff are crucial — this is engineering, not "conversation"**

### Two-Layer Separation

| Layer | Content | Approach |
|-------|---------|----------|
| **Platform** | AFS, ArcSphere, Agent Fleet, LLM runtime | Build once, solidify |
| **Application** | Skills + Rules + Generative UI | User/AI compose |

**Determinism sinks from "application code" to "platform layer"**

---

## Blocklet / Chamber / Scaffold

### Blocklet

**An identity-bound, capability-scoped, deployable computational unit**

What Blocklet has over Docker container:
**Semantic boundary + Permission boundary**

### Chamber

**Bounded execution unit with identity and capability**

- Chamber is designed for operations that "jump out of AFS boundary"
- Future software is naturally self-limiting

| Scenario | Needs explicit Chamber? |
|----------|------------------------|
| Skill running on Agent Fleet | No, architecture naturally isolates |
| Agent directly operating external systems | Yes, jumps out of AFS boundary |

### Scaffold

**Pre-defined Chamber composition framework for specific domains**

- Scaffold should be designed for software that will be written in the future
- Not for software written in the past

### Relationship Mapping

| Blocklet System | AINE System | Essence |
|-----------------|-------------|---------|
| Blocklet | Chamber | Minimum execution unit with boundary, identity, capability |
| Blocklet Server | Scaffold | Pre-defined Chamber composition framework |
| DID + Permission | Capability | Who can operate what, where are boundaries |

---

## DID / Capability

### Core Distinction

- **Identity** (who I am)
- **Capability** (what I can do)

**Web3's biggest mistake: mixing identity and capability together**

### DID + AFS Integration

- **DID determines**: which AFS view can be seen, which paths can be written
- **Capability determines**: which skills can be called, which tools can be operated
- **All operations**: must be traceable to DID

> An agent without identity is uncontrollable.

---

## Product Positioning

### ArcSphere

**Skill Browser + Skill Composer + AFS UI**

Not: ❌ Chrome / ❌ Chat UI / ❌ Copilot

### Agent Fleet

- Agent Fleet is **NOT** a standalone new product
- Agent Fleet **IS** a new type of Blocklet

```
Blocklet Server (platform)
├── Traditional Blocklet (Web components)
└── Agent Fleet Blocklet (AI-native components) = new type
```

---

## Key Technical Judgments

### Blockchain Position

**Verifiability matters. Global consensus doesn't.**

Keep: DID + VC + Immutable log
Don't need: Bitcoin/Ethereum-style consensus, procedural smart contracts

### Contract = Constraint, not Procedure

| Traditional Smart Contract | AI-Era Contract |
|---------------------------|-----------------|
| Procedural (if-then-else) | Declarative (rules/constraints) |
| Executor: EVM | Executor: LLM + Chamber |

### Skills vs MCP

Skills succeeded because:
- Natural language creation
- Self-bootstrapping: Skills can produce Skills
- **Assumes executor is AI Agent, not human engineer**

### Isolation Evolution

Bare metal → VM → Docker → Functions → Declarative constraints

**Applications become more "self-limiting"**, so lighter isolation is needed.

---

# Part C: Self-Review Checklist

## Before You Submit Anything

### Direction Alignment

**AFS Alignment**
- [ ] Does this treat AFS as the core abstraction?
- [ ] Does UI depend only on AFS, not directly on backend?
- [ ] Are agents operating AFS, not systems directly?
- [ ] Are paths semantic (AFS paths), not physical?

**Layer Alignment**
- [ ] Is it clear whether this is platform-layer or application-layer?
- [ ] If platform-layer: designed for stability and long-term?
- [ ] If application-layer: declarative and composable?

**Identity Alignment**
- [ ] Are all actors identified with DID?
- [ ] Are capabilities separate from identity?
- [ ] Are all operations traceable?

**Architecture Alignment**
- [ ] Does it fit the Blocklet/Chamber/Scaffold model?
- [ ] Does it make the system simpler or more complex?
- [ ] Aligned with "determinism sinking to platform layer"?

### Time Horizon Check

| If your proposal... | Ask yourself... |
|---------------------|-----------------|
| Solves only immediate problem | Deeper structural issue being ignored? |
| Requires "figure it out later" | What's deferred? Is that acceptable? |
| Assumes current constraints permanent | What changes in 2-3 years? |

### Clarity Check

1. Can you explain core idea in 2 sentences?
2. Can you list exactly what changes and what doesn't?
3. Can you describe boundaries - what's in scope, what's not?

### Failure Path Check

1. What are the known risks?
2. What would cause this to fail?
3. How will we know if it's failing?
4. What's the rollback plan?

> If you can't describe how it fails, you don't understand it well enough.

---

## Anti-Patterns (Instant Red Flags)

### Technical Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| UI depending directly on backend | Violates AFS-UI principle |
| Agent operating system directly | Should only operate AFS |
| Mixing identity and capability | Follow DID + Capability separation |
| Procedural contracts | Use declarative constraints |
| Hard-coded physical paths | Use semantic AFS paths |
| Building adapter for legacy code | Build for future software |

### Proposal Anti-Patterns

| Anti-Pattern | What It Looks Like |
|--------------|-------------------|
| **Vague scope** | "Improve X" without definition |
| **Hidden complexity** | Simple proposal, unstated major changes |
| **Solution seeking problem** | "Let's use [tech]" without problem statement |
| **Wishful thinking** | Assumes best-case throughout |
| **No definition of done** | No way to know when complete |
| **Fake rigor** | Diagrams, buzzwords, no anchor points |
| **AI-generated套话** | Methodology summary with no specific files, tasks, or risks. Could apply to any project. |
| **No engineering responsibility** | Describes "what should happen" but not "what I will do to this specific system" |

### Thinking Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Solving new problems with old paradigms | Update the question, not just answer |
| Making horse carriages faster | Ask what infrastructure cars need |
| Treating AFS as a feature | AFS is a worldview, not a module |

---

## Quick Reference Card

### Value Hierarchy
```
1. Long-term Correctness
2. Structural Clarity
3. System Consistency
4. Engineering Replayability
5. Efficiency
6. Comfort
```

### Engineering Requirements
```
1. Replayable
2. Traceable
3. Inspectable
4. Fail-safe
5. Evolvable
```

### Core Equations
```
AFS = AI-Native system abstraction layer
Skill = AFS transformation (not deterministic function)
Chamber = Bounded execution for operations outside AFS
Contract = Constraint, not Procedure
DID = Accountable actor identity
Capability = Minimal, composable, revocable authorization
```

---

## Final Self-Test

Before submitting, answer honestly:

1. **Does this align with AFS-first architecture?**
2. **Is the layer (platform vs application) clear?**
3. **Are identity and capability properly separated?**
4. **Can I describe how this fails?**
5. **Am I solving for the future or patching the past?**
6. **Would this still make sense in 3 years?**
7. **Would I bet my own time on this working?**
8. **Does this document have concrete anchor points?** (specific files, specific tasks, specific risks — not just methodology)
9. **If I remove all the "correct-sounding" methodology descriptions, what's left?** (If nothing → rewrite)

---

## The Ultimate Question

> "If Robert reads this, will he ask 'what problem are you actually solving?' or 'why are we doing this the old way?'"

If yes, go back and fix it first.

---

*Remember: This checklist helps structure thinking. It does not guarantee approval.*

*A proposal that passes all checks can still be wrong.*
*A proposal that fails some checks might still be worth discussing.*

*The goal is alignment and rigor, not box-checking.*

> Inelegant things will inevitably be eliminated in the long run.
