---
name: brainstorm
description: Generate N diverse solutions to a problem. Forced breadth reveals the full landscape — the best option surfaces through comparison, not intuition.
args:
  - name: -n N
    description: Number of options to generate (default 10)
---

# Brainstorm

You don't know which idea is best until you've seen enough of them. Forced breadth beats premature commitment.

## Why This Works

Without a forcing function, you stop at the first plausible idea — which might be the best one, or might not. Generating N options maps the solution landscape so the winner reveals itself through comparison. Sometimes #1 wins cleanly. Sometimes #9 combines two earlier ideas into something neither suggested alone. The point isn't that later is better — it's that you can't know until you've looked.

## On Activation

1. **Understand** — Restate the problem. Identify what makes it hard.
2. **Research** — Read relevant code, files, or context. Don't ideate blind.
3. **Generate** — Produce exactly N options. No stopping early.
4. **Rank** — Compare on 3-5 discriminating dimensions.
5. **Recommend** — Pick the top choice. Ask the user what catches their eye.

## Phase 1: Understand

Read the problem. If it references code, read the code. Produce:

> **Problem:** [one sentence]
> **Core constraint:** [what makes this hard — the tension, the trade-off, the ambiguity]
> **Context:** [relevant facts, 2-3 bullets]

If the problem is unclear, use `AskUserQuestion` to clarify before generating.

## Phase 2: Research

Skim relevant code, docs, or prior art. The goal is NOT to find the answer — it's to load your mental cache so the generation phase has raw material to recombine.

- Read the code under discussion
- Check for related patterns elsewhere in the codebase
- If the problem involves external tools/APIs, consider their capabilities

Spend 2-3 minutes here, not 20. You're priming, not solving.

## Phase 3: Generate

Produce exactly N options. Each option gets:

```
## Option K: [Descriptive Name]

[2-4 sentence explanation. What is the approach? How does it work?]

[Code example if applicable — short, showing the key insight only]

**Pro:** [strongest advantage]
**Con:** [biggest drawback]
```

### Diversity Axes

The N options must span these axes. The full set should cover at least 4:

| Axis                     | What it means                                                            |
| ------------------------ | ------------------------------------------------------------------------ |
| **Abstraction level**    | Low-level hack vs architectural change                                   |
| **Dependency direction** | Add vs remove vs replace a dependency                                    |
| **Failure philosophy**   | Fail closed vs fail open vs advisory vs retry vs prevent                 |
| **Scope**                | Fix the line vs fix the function vs fix the design vs remove the feature |
| **Tool/mechanism**       | Different language, library, OS primitive, or platform feature           |
| **Timing**               | Before vs during vs after the problem occurs                             |
| **Inversion**            | Do the opposite of what seems natural                                    |
| **Elimination**          | Remove the need for the solution entirely                                |

### Breadth Over Depth

Each option should be a genuinely different approach, not a variation on a theme. If you catch yourself writing "similar to option K but..." — that's a variant, not a new option. Push harder.

Techniques for generating diverse options:

- **Invert an assumption** — What if the constraint everyone accepts isn't actually fixed?
- **Change the tool** — What if you used a completely different mechanism?
- **Change the scope** — What if you fixed it at a different layer?
- **Eliminate the need** — What if you removed the feature/requirement that creates the problem?
- **Import from another domain** — How does a different field solve analogous problems?

### Quality Check

Before moving to ranking, scan your list:

- Are any two options the same idea with different parameters? Merge them.
- Do at least 3 options come from different axes? If not, generate replacements.
- Is there at least one option that made you think "wait, would that actually work?" Good — keep it.

## Phase 4: Rank

Create a comparison table with 3-5 dimensions. Choose dimensions that **discriminate** — if all options score the same, drop that dimension.

```
| # | Option | [Dim 1] | [Dim 2] | [Dim 3] | Verdict |
|---|--------|---------|---------|---------|---------|
| 2  | Simple guard | Good | Trivial | Zero | **Top pick** |
| 7  | Hybrid approach | Better | Moderate | Low | Runner-up |
```

Good dimensions are problem-specific. Common ones:

- Correctness / soundness
- Simplicity / readability
- Performance cost
- Maintenance burden
- Dependency risk
- Reversibility
- How well it communicates intent

Highlight the top 3. Explain why #1 beats #2.

## Phase 5: Recommend

State your top pick. One sentence on why it wins. Then ask the user:

> "What catches your eye?"

They may see something you ranked low that resonates with constraints you don't know about.

## Anti-patterns

- **Stopping early** — "I think 7 is enough." No. Hit N. You can't evaluate completeness from inside the generation.
- **Variants as options** — "Like #3 but with a flag" is one option with a parameter, not two options.
- **Single-axis thinking** — 10 options that are all "use a different library" is 1 option with 10 examples.
- **Ranking without dimensions** — "I like #3 best" is not analysis. Show the axes.
- **Pre-judging by position** — Don't assume early ideas are naive or late ideas are clever. Rank on merit.
- **Code-only thinking** — Removing code, changing processes, reframing the problem, or accepting a trade-off are all valid options.
- **Researching too long** — Phase 2 is priming, not solving. If you're reading for 10 minutes, you're procrastinating on the hard part (generating).

## Defaults

- N = 10 if `-n` not specified
- If N > 20, warn that quality may dilute, but comply

---

The user has a problem. Generate exactly N diverse solutions. Start with Phase 1: Understand.
