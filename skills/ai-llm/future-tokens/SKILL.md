---
name: future-tokens
description: Every AI output has structural blind spots determined by the generation process itself. Future Tokens operations are named, composable instruments that target specific blind spots. They surface new information on every pass because expanding the output changes the blind spot geometry.
---

# Future Tokens: Corrective Instruments for AI Reasoning

Every AI output has structural blind spots. Coherence optimization suppresses gaps. Token-level generation locks in frames before alternatives are considered. Confidence distributes smoothly over claims that deserve scrutiny in different places. These aren't random errors — they're predictable artifacts of how generation works.

Future Tokens operations are named, composable instruments that target specific blind spot types. Each one reliably surfaces information that the generation process systematically omits, because the blind spots are structural, not random. And they're generative — every pass changes the consideration space, shifting the blind spot geometry so the next pass finds new material.

Part of the [FUTURE TOKENS](https://jordanmrubin.substack.com/p/future-tokens) project.

This collection is compatible with both Claude and Codex workflows.

## When to use

If you just produced an output, it has predictable gaps. Match what you built to the operation that catches what it missed.

| you just built…                    | it probably missed…                                                    | run this                |
|------------------------------------|------------------------------------------------------------------------|-------------------------|
| a questionnaire or survey          | questions you couldn't think to ask because coherence suppresses gaps   | @negspace               |
| an evaluation plan or rubric       | hidden assumptions that must be true for it to work                     | @excavate               |
| a recommendation or proposal       | the strongest case against your conclusion                              | @antithesize            |
| a strategy or business case        | dimensions you're not scoring on                                        | @dimensionalize         |
| a first draft of anything          | blind spots that coherence optimization created                         | @negspace               |
| an analysis that feels complete    | the argument that should be there but isn't                             | @negspace               |
| a set of options or alternatives   | structural diversity — variations on a theme instead of real branches   | @rhyme → @metaphorize   |
| multiple competing analyses        | a unified frame that preserves what each one gets right                  | @synthesize             |

## Key properties

Three properties distinguish Future Tokens operations from generic "think harder" prompting:

1. **Reliability** — operations work every time because they target structural features of generation, not random errors. Coherence suppression, frame lock, and confidence smoothing are always present in AI outputs, so instruments that target them always find material.
2. **Generativity** — each pass surfaces new information because expanding the output changes the blind spot geometry. Run @negspace on an analysis, then run it again on the expanded version — the second pass finds different gaps. Diminishing returns are minimal.
3. **Composability** — operations chain (e.g., @excavate → @antithesize → @synthesize) to produce analysis no single pass can reach. Each operation's output becomes well-formed input for the next, and the sequence matters: different orderings expose different structure.

## Core Skills

The following reasoning moves are available. Each skill is self-contained with its own directory containing the full procedural definition and worked examples.

- **[antithesize](./antithesize/ANTITHESIZE.md)** — Generate standalone opposition to any proposition. Antithesis must be comprehensible without reading thesis—it's an alternative complete worldview, not refutation.
- **[excavate](./excavate/EXCAVATE.md)** — Perform assumption archaeology. Reveal the layered structure of "what must be true" beneath a claim, plan, belief, or principle. The goal is to surface implicit premises, map dependencies, identify cruxes, and expose where disagreement or uncertainty actually lives. Unlike attack (looking for breakage) or antithesize (generating opposition), excavate is diagnostic. It lights up the skeleton beneath the stance.
- **[dimensionalize](./dimensionalize/DIMENSIONALIZE.md)** — Transform complex decisions or systems into 3-7 measurable dimensions that score high on fidelity (validity+stability), leverage (actionability+impact), and low on complexity (cognitive load+overfitting). Use when facing multi-factor choices, analyzing systems, or comparing non-obvious options.
- **[handlize](./handlize/HANDLIZE.md)** — Extract the executable residue from an argument or map by isolating handles—concepts with operational grip—while discarding rhetorical mass. Answers: "what here could actually change what I do?" Not summary, not critique—just residue extraction.
- **[inductify](./inductify/INDUCTIFY.md)** — Extract non-obvious structural commonalities across multiple substantial examples. Identify latent mechanisms, shared constraint-structures, and pattern families with predictive slack rather than surface vibes. Heavy induction: decomposing each case, cross-referencing mechanisms, and stress-testing emergent generalizations.
- **[metaphorize](./metaphorize/METAPHORIZE.md)** — Build explicit, high-coverage mapping from familiar source domain onto target domain to systematically port rules, heuristics, formulas, and metrics. Heavier than rhyme, lighter than formal proof. When source has math, carry the math with units and dimensional analysis.
- **[negspace](./negspace/NEGSPACE.md)** — Detect the argument, conclusion, or premise that *should* be present given the statistical structure of the text, but is conspicuously absent. Reads the "shadow" of the text by comparing what was written to what was overwhelmingly likely to be written next, revealing hidden content via information asymmetry.
- **[rhetoricize](./rhetoricize/RHETORICIZE.md)** — Extract rhetorical skeleton + fact ledger, then map the "spin-space" around an argument by applying controlled connotation and syntax transforms across multiple passes. Ranks variants by rhetorical surprise and surfaces the hidden fulcrum words and grammatical moves that do the persuasive work. Diagnostic, not generative.
- **[rhyme](./rhyme/RHYME.md)** — Fast structural similarity detection that maps novel inputs onto known patterns through echo recognition. Use for understanding unfamiliar domains, creative seeding, intuition framing, or finding parallel structures across different contexts. Upstream move before metaphor or detailed mapping.
- **[synthesize](./synthesize/SYNTHESIZE.md)** — Compress conflicting positions into decision-sufficient generative frame with explicit distortion tracking. Produces tiered outputs (quick/medium/deep), tracks what was dropped, and validates via round-trip testing. Use when thesis + antithesis exist and you need portable framework that explains both while generating novel predictions.

## Using These Skills

Each skill directory contains:

- **Main skill file** (e.g., `ANTITHESIZE.md`) — Complete procedural definition including:
  - When to use the skill
  - Step-by-step process
  - Quality criteria
  - Common failure modes
  - Integration with other skills
  - Worked examples embedded throughout

## Philosophy

The core design goal: make cognitive operations **invocable on demand rather than sporadic**. Good reasoners sometimes check assumptions, sometimes steelman the opposition, sometimes look for what's missing. Future Tokens makes these operations named, procedural, and callable — transforming unreliable intuition into reliable instruments.

These skills embody several principles:

1. **Composability** — Skills chain and combine; each operation's output is well-formed input for others
2. **Explicitness** — Each move has clear mechanics, not just vibes
3. **Epistemic hygiene** — Built-in uncertainty tracking and failure mode awareness
4. **Context efficiency** — Designed to minimize token waste while maximizing insight
5. **Clear attribution** — Maintain distinctions between three entities in any assessment context:
   - **The user** — who requests the analysis or reasoning move
   - **The author(s)** — whose content, claims, or work is being assessed
   - **Claude/Codex** — who performs the reasoning operation and generates outputs

   Never misattribute Claude/Codex outputs to the author or user. Never misattribute the author's positions to the user. Keep the three roles distinct throughout all operations.

## Repository Structure

```
Future Tokens/
  install.sh            ← One-line installer for agents
  SKILL.md              ← You are here
  LICENSE               ← CC BY 4.0 license
  TRADEMARK.md          ← Trademark usage guidelines
  .claude-plugin/       ← Marketplace configuration
    marketplace.json
  antithesize/
    ANTITHESIZE.md      ← Full procedural body
  dimensionalize/
    DIMENSIONALIZE.md
  excavate/
    EXCAVATE.md
  ...
```

## Contributing

Skills start as experiments and are refined through use.

---

For the broader vision, see the [FUTURE TOKENS Substack](https://jordanmrubin.substack.com/p/future-tokens).
