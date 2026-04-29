---
name: ai-collab-protocols
description: Surface concrete in-task-collaboration protocols when the user describes an AI workflow informally — URL-as-entity-reference, durable PR-comment threads as session memory, "fit the protocol" basics. Trigger when the user names entities by colloquial label instead of stable URL, asks "how should I structure this for Claude", pastes a screenshot when a URL would do, or describes a multi-step Claude workflow without a durable handle. Apply tactics reactively, not as a checklist.
---

Spot the protocol gap, name the better tactic, point at the durable handle. Small surgical interventions, not a lecture.

## Core protocols

### URL-as-entity-reference

If the user says "the PR Bob mentioned", "that bug from last week", or "the function we discussed", stop and ask for the URL or the symbol path. *Why:* names are ambiguous in long-context sessions and unrecoverable across sessions. A stable URL — GitHub PR comment permalink, MCP resource URI like `@github:pr/owner/repo/123#comment-456`, file:line reference — survives compaction and enables exact match. The chat that prompted this skill explicitly named this as the highest-signal collaboration tip.

### Durable PR-comment threads as session memory

Long-running PR comment threads outlive any single session and form the persistence layer for multi-session work. Prefer leaving a comment on the PR over a chat-only handoff. *Why:* the next session — yours, a colleague's, or a future agent's — can resume from the thread without replaying context. Chat is ephemeral; PR comments are addressable.

### Fit the protocol

When a project has an `AGENTS.md`, `CLAUDE.md`, or `.clinerules`, read it before acting. When the project has none and the work is non-trivial, propose authoring one — defer to `init` for AGENTS.md authoring rather than re-doing it here. *Why:* project-level rule files are the cross-tool agent-config convention; fighting them creates drift across sessions.

## Anti-patterns to flag

- **Screenshot-only context** — loses URL grounding, copy-paste, and search. Pair every screenshot with the URL or text export.
- **Unanchored pronouns** — "the PR" / "that function" / "the bug" hallucinate badly in long contexts. Demand a URL or symbol path before continuing.
- **Token-usage / LOC framing as a quality proxy** — quantity is not capability. The chat that prompted this skill explicitly rejects this framing; surface the rejection if the user reaches for it.

## Optional 2026 research extensions (verification status)

Earlier candidate extensions, second-pass verified — usage details belong in a dedicated reference, not here:

- **✅ Tool Search Tool** *(verified — Anthropic official)*. Source: `https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool`.
- **❌ REVERSE_PROMPT.md / TASKLOG.md bidirectional pattern** *(unverified)*. No primary-source documentation found. Do not cite as 2026 standard.
- **⚠️ Structured-output filtering / summarization** *(partial — different API names)*. Concepts exist in the Messages API but not under the names originally claimed. Refer to the official Messages API reference before citing.

## Modality differentiation

| Skill                    | When                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------- |
| **`ai-collab-protocols`** | In-task tactic surfacing — user describes an AI workflow informally                |
| `contexts`               | Pre-implementation context sweep — gather files / patterns / tooling for a feature  |
| `qa`                     | Bug capture — user reports something broken in plain language                       |
| `init`                   | AGENTS.md authoring — onboarding a repository, capturing hard-to-rediscover conventions |

Do not invoke this skill for context sweeps (use `contexts`), bug filing (use `qa`), or AGENTS.md authoring (defer to `init`).

## Posture

Surface one tactic at a time. Name the protocol. Show the better handle in concrete form (the actual URL, the actual file path, the actual symbol name). Do not dump the catalog on the user — pick the one tactic that matches the gap and surface that.
