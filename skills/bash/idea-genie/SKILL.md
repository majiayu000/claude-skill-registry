---
name: idea-genie
description: Generate an evidence-grounded opportunity
---
# Idea Genie

Turn an open-ended question into a small, evidenced opportunity portfolio. This
skill explores; it does not select work, create beads, or write Discovery's BDD
intent packet.

## Workflow

1. State the question, constraints, non-goals, and evidence sources. Use
   `research` when the repository facts are not already available.
2. Record observations as claims with repository or executable evidence. Put
   unverified beliefs in `assumptions`; never blend them into observations.
3. Propose candidate mechanisms. Give every candidate its own evidence,
   overlap result against live skills, CLI capabilities, and tracked work, plus
   one Given/When/Then scenario.
4. Run another novelty pass. Merge equivalents and discard unsupported ideas.
   Stop when the pass yields zero materially new candidates, not when an
   arbitrary count is reached.
5. Write `idea-portfolio.v1`, run `scripts/validate-output.sh`, and hand the
   artifact to `discovery`. Discovery alone shapes and persists executable BDD
   intent.

If every candidate overlaps existing work or lacks support, emit
`status: no-new-work`, an empty candidate list, and observations showing why.
An honest empty portfolio is a successful result.

## Artifact contract

Required fields are `schema_version`, `status`, `observations`, `assumptions`,
`candidates`, and `termination`. Candidate portfolios require cited evidence,
an explicit `overlaps` array, and a complete scenario. Termination records the
reason and `novel_candidates_last_pass: 0`.

The validator is the machine boundary:

```bash
skills/idea-genie/scripts/validate-output.sh <portfolio.json>
```

Executable behavior: [references/idea-genie.feature](references/idea-genie.feature).

## Do not

- Pad the result to a requested or customary idea count.
- Create tracker rows, rank a winner, decompose implementation, or claim a
  selection verdict.
- Treat assumptions or attractive mechanisms as observed facts.
