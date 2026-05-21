# Source Attribution

This skill is a derivation, not original work. Honest
attribution belongs at the front, not the back.

## Primary Source: Andrej Karpathy

The underlying observations about LLM coding pitfalls
trace to Andrej Karpathy on X (formerly Twitter).
The most-cited verbatim quote, anchoring principles 1
and 2, is the one Karpathy posted on agentic coding
failure modes:

> The models make wrong assumptions on your behalf
> and just run along with them without checking. They
> don't manage their confusion, don't seek
> clarifications, don't surface inconsistencies, don't
> present tradeoffs, don't push back when they
> should.

Source: <https://x.com/karpathy/status/2015883857489522876>

Principles 3 (surgical changes) and 4 (goal-driven
execution) are inferred from adjacent Karpathy posts
and talks rather than a single tweet. Useful adjacent
sources:

- Karpathy on AI-assisted coding rhythm (April 2025):
  <https://x.com/karpathy/status/1915581920022585597>
- Karpathy "Software 3.0" / YC AI Startup School
  (June 2025):
  <https://www.ycombinator.com/library/MW-andrej-karpathy-software-is-changing-again>
- Karpathy 2025 LLM Year in Review (Dec 2025), framing
  Reinforcement Learning from Verifiable Rewards as the
  paradigm shift:
  <https://karpathy.bearblog.dev/year-in-review-2025/>

## Distillation Source: Forrest Chang

The four-principle wording (Think Before Coding,
Simplicity First, Surgical Changes, Goal-Driven
Execution) is **Forrest Chang's** synthesis, not
Karpathy's. The skill name "karpathy-guidelines"
upstream describes derivation, not authorship.

Upstream repository:

- <https://github.com/forrestchang/andrej-karpathy-skills>
- License: MIT
- Files distilled from: `CLAUDE.md`, `EXAMPLES.md`,
  `skills/karpathy-guidelines/SKILL.md`

This night-market skill rewrites prose in the
project's own voice and conventions. No upstream
prose is copied verbatim. Principles, naming, and
attribution structure constitute facts and
methodology, not protected expression.

## Attribution Caveat

When citing this skill, prefer "derived from
Karpathy's observations" over "Karpathy's
principles." Karpathy named the failure modes; the
four-principle architecture is a community
distillation. Conflating the two is sloppy citation.

## Adjacent Prior Art Surveyed

A tome:code-search pass surveyed nine adjacent
repositories. Patterns absorbed or deferred are
documented in the project specification. The repos:

| Repo | Stars | Key Pattern |
|------|-------|-------------|
| TheRealSeanDonahoe/agents-md | 511 | Append-only Project Learnings |
| shamanakin/VIBERAIL | n/a | Drift-rails per failure mode |
| yzhao062/agent-style | 325 | Tone-to-evidence calibration |
| bmad-code-org/BMAD-METHOD | n/a | PromptSentinel scope-creep verbs |
| Aider-AI/conventions | 190 | Read-only pinned context |
| agentsmd/agents.md | n/a | Hierarchical nearest-wins overrides |
| continuedev/awesome-rules | 169 | Role-based model configuration |
| PatrickJS/awesome-cursorrules | 39300 | Stack-keyed rule libraries |
| Piebald-AI/claude-code-system-prompts | n/a | Versioned system-prompt archive |

Two patterns were absorbed into this skill: the
drift-rail framing for anti-patterns and the
calibration sub-rule under Think Before Coding. Two
were deferred to follow-up issues: the agent-writable
Project Learnings store and the PromptSentinel
verb-detection hook.

## Contrarian Voices Cited

The tradeoff acknowledgment module cites three
voices that push back on rigorous-by-default LLM
coding rules:

1. Simon Willison, "Not all AI-assisted programming
   is vibe coding" (March 2025):
   <https://simonwillison.net/2025/Mar/19/vibe-coding/>
2. Mastering Product HQ, "What Karpathy's CLAUDE.md
   misses":
   <https://www.masteringproducthq.com/p/what-karpathys-claudemd-misses-and>
3. NMN.gl, "Vibe Coding Considered Harmful" (March
   2025): <https://nmn.gl/blog/dangers-vibe-coding>

These are referenced for intellectual honesty, not
to undermine the principles.

## License

Upstream repository: MIT (Forrest Chang).
This derivation: same plugin license as the
night-market repository (MIT).
