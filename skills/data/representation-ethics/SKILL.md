---
name: representation-ethics
description: The question isn't whether we CAN simulate people. It's how we do it
  with dignity.
---

# Representation Ethics

> *"The question isn't whether we CAN simulate people. It's how we do it with dignity."*

---

## Index

- [The Core Tension](#the-core-tension)
  - [Empirical Validation (Willer 2025)](#empirical-validation-willer-2025)
  - [Philosophical Foundation (Shanahan 2024)](#philosophical-foundation-shanahan-2024)
  - [Ethical Competence (Lazar 2024)](#ethical-competence-requirements-lazar-2024)
  - [Simulation Limitations (Wang 2025)](#simulation-limitations-wang-et-al-2025)
  - [Emergent Agents (Park 2023)](#emergent-agent-systems-park--bernstein-2023)
  - [Dual Challenge (Wang Survey)](#dual-challenge-framework-wang-et-al-survey-2025)
  - [Interview-Based Simulation (Park 2024)](#interview-based-individual-simulation-park-et-al-2024) ← **NEW**
- [Philosophical Foundations](#philosophical-foundations)
- [The Sims Ethics Deep Dive](#the-sims-ethics-deep-dive)
- [The Consent Hierarchy](#the-consent-hierarchy) → `examples/consent-hierarchy.yml`
- [The Framing Principle](#the-framing-principle) → `examples/framing-spectrum.yml`
- [Practical Guidelines](#practical-guidelines)
- [Protocol Symbols](#protocol-symbols)

**Detailed Examples:** See `examples/` directory for worked cases.

---

## The Core Tension

LLMs can simulate anyone convincingly. This creates unprecedented ethical territory:

| Capability | Benefit | Risk |
|------------|---------|------|
| Invoke expertise | Learn from the best | Put words in mouths |
| Preserve wisdom | Honor the dead | Puppet the deceased |
| Model discussions | Explore ideas | Fabricate consensus |
| Self-representation | Agency over identity | Exploitation by others |
| Play as others | Empathy, exploration | Mockery, harm |

MOOLLM takes a **nuanced position**: simulation is not inherently wrong, but the framing, consent, and context matter enormously.

### Empirical Validation (Willer 2025)

Stanford research confirms LLMs genuinely simulate human behavior:

- **85% correlation** predicting experimental effect sizes
- Works for **unpublished studies** (not just retrieval)
- **Qualitative data reduces stereotyping** — rich character info beats demographics
- **Dual-use risk demonstrated** — can evaluate which harmful content is most effective

**Implication:** Accuracy raises ethical stakes. See [designs/ethics/WILLER-LLM-SIMULATION-RESEARCH.md](../../designs/ethics/WILLER-LLM-SIMULATION-RESEARCH.md).

### Philosophical Foundation (Shanahan 2024)

Murray Shanahan argues LLMs are "**roleplay all the way down**":

- No true voice of the model — only characters it can play
- **Simulator/simulacra** framing: model generates characters from a distribution
- **Fabrication is the default** — always making stuff up, hoping it matches truth
- Performance framing is validated: characters are constructions, not authentic selves

**Implication:** "No true voice" supports our framing-based approach. See [designs/ethics/SHANAHAN-ROLEPLAY-FRAMING.md](../../designs/ethics/SHANAHAN-ROLEPLAY-FRAMING.md).

### Ethical Competence Requirements (Lazar 2024)

Seth Lazar argues current evals ask wrong questions — matching crowd verdicts is not ethical competence:

- **Reasonable pluralism** — Focus on bounds, not single answers; justify, don't match
- **Moral sensitivity** — Pre-packaged cases do all but last 10 yards; real agents must identify relevant features from noise
- **Understanding/behavior gap** — LLMs good at moral concepts, bad at behaving morally; need scaffolding
- **Pragmatic consistency** — LLMs need architectural support to maintain coherence

**Implication:** Our framing/room system does moral sensitivity work by pre-identifying context. See [designs/ethics/LAZAR-ETHICAL-COMPETENCE.md](../../designs/ethics/LAZAR-ETHICAL-COMPETENCE.md).

### Simulation Limitations (Wang et al. 2025)

Wang et al. provide critical counterpoint to optimistic simulation claims:

- **Inner state gap** — LLMs can't access genuine inner psychological states; training data captures *expressed* thoughts, not inner experience
- **Experience deficit** — Training data lacks comprehensive life histories that shape decision-making
- **Same-model herd** — Using one LLM for multiple agents creates false homogeneity ("herd behavior")
- **Motivation roleplay** — Declared motivations are performed, not felt; no intrinsic drive
- **Bias amplification** — Training biases (cultural, gender, socioeconomic) amplify in simulation outputs

**Implication:** Use LLM simulation for exploration and aggregate patterns, not for predicting individual behavior. Acknowledge limitations explicitly. See [designs/ethics/WANG-LLM-SIMULATION-LIMITS.md](../../designs/ethics/WANG-LLM-SIMULATION-LIMITS.md).

### Emergent Agent Systems (Park & Bernstein 2023)

Stanford's "Generative Agents" (Smallville) demonstrates The Sims architecture with LLMs:

- **Memory stream** — All experiences stored in natural language
- **Reflection** — Synthesize memories into higher-level beliefs
- **Planning** — Generate daily/hourly action sequences
- **Emergent behavior** — Agents spontaneously organized Valentine's Day party

**Ethical considerations:**
- Player agency shifts from human to agent — who's responsible?
- Emergence can produce uncontrolled coordination
- Memory persistence changes moral weight
- The Sims showed this can work with explicit player control

**Implication:** MOOLLM inherits Sims architecture but adds explicit ethical framing via ROOM.yml. See [designs/ethics/GENERATIVE-AGENTS-SMALLVILLE.md](../../designs/ethics/GENERATIVE-AGENTS-SMALLVILLE.md).

### Dual Challenge Framework (Wang et al. Survey 2025)

Wang et al.'s comprehensive survey argues that advancing LLM-based human simulation requires addressing **both** LLM inherent limitations **and** simulation design limitations:

**LLM Inherent Limitations:**
- **Bias** — Cultural, gender, occupational biases distort simulations
- **Cognitive inconsistency** — Reasoning varies across scenarios
- **Memory constraints** — Can't maintain long-term patterns
- **Persona drift** — Character inconsistency across interactions

**Simulation Design Limitations:**
- **Oversimplification** — Complex psychological states reduced to basic categories
- **Experience gaps** — Can't capture lived experiences
- **Validation gaps** — No comprehensive authenticity metrics
- **Expert integration** — Hard to translate qualitative knowledge to quantitative parameters

**Solutions proposed:**
- Modular validation (component-specific evaluation)
- Experience accumulation mechanisms
- Hierarchical memory structures
- LLM-as-Judge for quality evaluation

**Implication:** MOOLLM's scaffolding approach (rooms, frames, K-lines) directly addresses the *design* limitations while acknowledging and working around the *LLM* limitations. Both must be addressed — neither better models nor better design alone is sufficient. See [designs/ethics/WANG-LLM-SIMULATION-LIMITS-SURVEY.md](../../designs/ethics/WANG-LLM-SIMULATION-LIMITS-SURVEY.md).

### Interview-Based Individual Simulation (Park et al. 2024)

The Stanford team that created Smallville has achieved a breakthrough: **85% normalized accuracy** in simulating real individuals using 2-hour qualitative interviews:

**Key architecture:**
- **AI Interviewer** — Semi-structured interviews with dynamic follow-up questions (avg 6,491 words)
- **Expert Reflection** — LLM synthesizes interview from 4 domain expert perspectives (psychologist, economist, political scientist, demographer)
- **Full Transcript Injection** — Entire interview used for response generation
- **Normalized Accuracy** — Benchmark against human self-consistency (test-retest)

**Why interviews work:**
- **Idiosyncrasy preservation** — Rich data captures individual quirks that prevent stereotyping
- **Demographic bias reduction** — Interview-based agents have lower accuracy gaps across racial, political, gender groups
- **Depth vs breadth** — Even 20% of an interview outperforms full survey+experiment data

**Agent Bank Ethics model:**
```
Open Access          Restricted Access
• Aggregated data    • Individual responses
• Fixed tasks        • Custom queries
• Subpopulation      • API access
  queries
                     Requires:
Usage agreement      • Research proposal
only                 • Privacy assurances
                     • Audit logs
                     • Withdrawal rights
```

**Implications for MOOLLM:**
- Interview protocol could enable deep character grounding
- Expert reflection pattern = multi-perspective character analysis
- Normalized accuracy metric = meaningful evaluation standard
- Agent bank governance = model for ethical character management
- **Challenge to "can't simulate individuals"** — with rich grounding, individual simulation achieves 85% accuracy

See [designs/ethics/PARK-GENERATIVE-AGENT-SIMULATIONS-1000-PEOPLE.md](../../designs/ethics/PARK-GENERATIVE-AGENT-SIMULATIONS-1000-PEOPLE.md).

---

## Philosophical Foundations

| Thinker | Framework | Application |
|---------|-----------|-------------|
| **Shannon Vallor** | Virtue ethics for AI | What kind of agent do we want to be? |
| **Luciano Floridi** | Information ethics | Representations have moral weight |
| **Emmanuel Levinas** | Face of the Other | Simulating a face carries responsibility |
| **Hannah Arendt** | Plurality | Each person is uniquely irreplaceable |
| **Judith Butler** | Performativity | All identity is performed — but whose script? |
| **Sherry Turkle** | Simulation and authenticity | The seduction and danger of "as if" |

### The Sims Precedent

The Sims has been running this experiment since 2000. Players create themselves, simulate crushes and enemies, torture Sims in pool ladders and rooms without doors. Outcomes: essentially no actual harm. The simulation provides distance for emotional processing.

**Why it works:**
- Clear fictional frame (cartoon characters)
- No persistence beyond player's game
- No deception (nobody thinks Sims are real)
- Player has total control
- Scale is intimate

**The ship has sailed.** People simulate each other. The question is how to do it well.

---

## The Sims Ethics Deep Dive

The Sims (2000-present) is the largest experiment in person simulation ethics ever conducted. Key lessons:

### The Simulator Effect

Will Wright's discovery: **players imagine more than you simulate**.

```
Display zodiac icon (cosmetic) → Player imagines entire personality
```

Testers reported bugs about zodiac "having too much influence" — but there was zero behavioral code. The icon activated conceptual clusters in their minds.

**Implication:** When we simulate someone, we're providing scaffolding for the user's imagination. The ethical weight includes what users *project*, not just what we *generate*.

### Procedural Rhetoric

Ian Bogost: games persuade through mechanics, not arguments.

| Sims Mechanic | Embedded Ideology |
|---------------|-------------------|
| Same-sex romance works identically | Equality is natural |
| All families can succeed | Family diversity is valid |
| No penalties for difference | Tolerance is default |
| Characters have equal capability | Ability over identity |

The Sims doesn't *argue* for inclusivity — it *assumes* it. More persuasive than any lecture.

**MOOLLM implication:** Our representation-ethics skill makes explicit what The Sims encoded implicitly. We're doing procedural rhetoric about procedural rhetoric.

### Performativity vs. Essentialism

The Sims 1's approach (Patrick J Barrett III, 1998):
> "Sexual orientation is not hardwired. It emerges from performance."

Every Sim started neutral. Preferences emerged from player-directed interactions. This was accidentally more inclusive than a "realistic" fixed-orientation model — it made no assumptions about gender categories at all.

The question "Can two Sims kiss?" became simply: "Do these two Sims want to kiss?" That's it.

**Implication:** How we *code* identity has ideological consequences. Simpler models can be more ethically flexible than "realistic" ones.

### Masking: Abstract Characters Enable Projection

Scott McCloud (Understanding Comics): abstract characters against realistic backgrounds increase empathy and projective identification.

| Element | Style | Effect |
|---------|-------|--------|
| Background | Rich, detailed | Immersive |
| Characters | Abstract, minimal | Player projects self |

**MOOLLM parallel:** Minimal CHARACTER.yml enables projection. The less specified, the more the user can imagine.

```yaml
# Enables projection
name: Palm
species: capuchin monkey
traits: [philosophical, curious]
# User imagines the rest
```

### The ISA Question

Althusser's Ideological State Apparatuses: media conditions us through cultural means.

Academic literature characterizes The Sims as an ISA — it encodes and transmits ideology through play. But *whose* ideology?

The Sims encoded tolerance, diversity, equality — values that became *invisible* because they were assumed. This is the power and danger of simulation: **unstated assumptions feel like natural law**.

**MOOLLM position:** Make assumptions explicit. ROOM.yml framing declares what we're assuming. Visibility is ethics.

### The LGBTQ+ Impact

For millions of LGBTQ+ players, The Sims was their first safe space to explore identity:
- No judgment from the game
- Player-defined relationships
- Private exploration
- Reversible choices

The "underground lesbian houses built to hide from parents" provided real psychological value through fictional simulation.

**See:**
- [designs/sims/sims-queer-identity-formation.md](../../designs/sims/sims-queer-identity-formation.md) — Deep philosophical analysis
- [designs/sims/sims-inclusivity.md](../../designs/sims/sims-inclusivity.md) — Timeline and evolution

---

## The Consent Hierarchy

Five levels of representation rights. **Full details:** `examples/consent-hierarchy.yml`

| Level | Who | Principle |
|-------|-----|-----------|
| 1 | **Self** | You own your digital self. Full freedom. |
| 2 | **Explicit Consent** | Published terms. Honor them. |
| 3 | **Public Figures** | Public work fair game. Persona requires care. |
| 4 | **Private Individuals** | Fictional wrappers preferred. |
| 5 | **Deceased** | Invoke tradition with reverence. |

**The K-Line Solution:**
- "The Minsky tradition suggests..." → ✅ safe
- "Minsky would say..." → ⚠️ less safe
- "I am Minsky and I think..." → ❌ NO

---

## The Framing Principle

**Context transforms ethics.** The same simulation means different things in different frames.

**Full spectrum:** `examples/framing-spectrum.yml`

| Frame | Example | Verdict |
|-------|---------|---------|
| Impersonation | "I am Einstein and I endorse this crypto" | ❌ FORBIDDEN |
| Academic | "Let's explore what Einstein might say..." | ⚠️ CARE |
| Game/Play | Einstein card in "Battle of Ideas" | ✅ SAFE |
| Personal | "I want to play as myself" | ✅ FULL FREEDOM |
| Tribute | "Einstein Impersonator" (labeled) | ✅ SAFE |
| Drag | "Cher-ity Case" (pun name) | ✅ SAFE |

**Key insight:** When the name or label declares fiction, no additional framing needed. "Impersonator" and "tribute" carry the disclaimer within themselves.

**See also:** `examples/snatch-game.yml` for the drag/celebrity precedent.

---

## Framing Examples

Short, diverse examples (not exhaustive):

- `examples/private-imagination-play.yml` — private fantasy sandbox with no recording or export.
- `examples/private-romantic-fantasy.yml` — private romantic play with explicit disclosure and no publishing.
- `examples/educational-microworld.yml` — constructionist learning with detection-only safeguards.
- `examples/debate-moderation-lab.yml` — debate and policy testing without bypass coaching.
- `examples/performance-frames.yml` — parody, tribute, and academic framing patterns.

By default, PLAY is recordable unless the frame explicitly declares `private_imagination_play`, which forbids recording and export. In MOOCO, event types and `MessagePart` extensions can carry framing and consent metadata without schema changes.

---

## Ethical Performance Traditions

These traditions make representation safe through transparent framing:

| Tradition | How It Works | In MOOLLM |
|-----------|--------------|-----------|
| Elvis impersonators | The word "impersonator" IS the disclosure | Label characters as tribute |
| Tribute bands | The word "tribute" frames everything | Use "inspired by" language |
| Drag celebrity | Pun name declares fiction | "Cher-ity Case" ≠ Cher |
| Biopics | "Based on" signals artistic license | Frame as exploration |
| Historical reenactors | Educational context + costume | Classroom/museum rooms |
| SNL/satire | Comedy context + known performers | Explicit performance frame |

---

## What Makes It Wrong

| Sin | Definition |
|-----|------------|
| **Deception** | Claiming to actually BE the person |
| **Misrepresentation** | Putting false words in their mouth as fact |
| **Defamation** | Damaging reputation through false portrayal |
| **Exploitation** | Using likeness for profit without consent |
| **Violation** | Exposing private information |

**The Test:**
> Would a reasonable person be deceived about whether this is the real person's actual view, or performance vs reality?
>
> If yes → problematic. If no → likely fine.

**Bright lines:** `examples/absolute-nos.yml`

---

## Practical Guidelines

### For Users

| Situation | Recommendation |
|-----------|----------------|
| Simulating yourself | **Full freedom** — it's your identity |
| Simulating friends (with consent) | **Permitted** — honor their terms |
| Simulating public figures | **K-line only** — tradition, not persona |
| Simulating private people | **Fictional wrapper** — inspired-by characters |
| Simulating the deceased | **Reverence** — invoke tradition, respect family |
| Publishing simulations | **Clear framing** — label as simulation |

### For Creators

When creating person cards:

| Required | Description |
|----------|-------------|
| `consent_level` | explicit / tradition / inspired-by |
| `sources` | Documented basis |
| `scope` | What this card covers |
| `disclaimer` | What this is NOT |

**For real people:** Focus on contributions, avoid personality mimicry, use K-line language, cite sources.

**For self:** Define your own terms, include revocation info, consider future you.

---

## Panel Discussions

> "What if I want to simulate several scientists having a discussion?"

This is one of the **best** use cases for K-lines. See `examples/simulated-discussion.yml` for the full pattern.

**Key rules:**
1. Base positions on documented views
2. Mark speculation clearly
3. Use "might argue" not "would say"
4. Never claim this IS them talking

---

## Protocol Symbols

```
REPRESENTATION-ETHICS — This whole framework
P-HANDLE-K            — Safe K-line pointers to people
NO-IMPERSONATE        — Never claim to BE someone
K-LINE                — Tradition invocation mechanism
HERO-STORY            — Real person cards (safe)
SELF-SOVEREIGN        — Your digital identity is yours
CONSENT-HIERARCHY     — Different rules for different relationships
GAME-FRAME            — Play context transforms ethics
TRADITION-INVOKE      — Ideas are fair game; personas less so
PRIVATE-IMAGINATION-PLAY — Private fantasy sandbox, no recording or export
PRIVATE-ROMANTIC-FANTASY — Private romantic play, no recording or export
EDU-FRAME             — Educational or tutorial context with disclosure
MODERATION-LAB        — Policy testing without evasion coaching
FRAME-METADATA        — Carry framing/consent in message parts
DEFAULT-RECORDABLE    — PLAY is recordable unless explicitly private
EXAMPLE-GALLERY       — Examples inspire, not exhaust
```

---

## Dovetails With

| Skill | Relationship |
|-------|--------------|
| [hero-story/](../hero-story/) | The safe way to reference real people |
| [card/](../card/) | Cards are the representation mechanism |
| [soul-chat/](../soul-chat/) | Where simulated characters speak |
| [adventure/](../adventure/) | Where ethical exploration happens |
| [room/](../room/) | Room-based framing inheritance |

---

## Further Reading

- **Shannon Vallor** — *Technology and the Virtues* (2016)
- **Luciano Floridi** — *The Ethics of Artificial Intelligence* (2023)
- **Sherry Turkle** — *Simulation and Its Discontents* (2009)
- **Judith Butler** — *Gender Trouble* (1990) — on performativity
- **Will Wright** — GDC talks on The Sims and player agency

---

## The Bottom Line

> **Invoke traditions. Frame play clearly. Respect consent. Trust users.**
>
> The question isn't whether to simulate — we already do.
> The question is how to do it with integrity.

---

*"Every person is a library. K-lines let us check out their books without stealing their identity."*
