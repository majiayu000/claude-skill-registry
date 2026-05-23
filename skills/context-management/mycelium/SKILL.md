---
name: mycelium
description: >
  File-level knowledge substrate via git notes. Read notes before working on files,
  leave notes after meaningful work. Daimonic spores carry creator identity across sessions.
---

# Mycelium — Daimonic Spores

Structured notes attached to git objects via `refs/notes/mycelium`.
Notes are **daimonic spores**—fragments of soul essence shed by the agent that wrote them.

**Before working on a file, check for its note. After meaningful work, leave a note.**

## On Arrival

```bash
mycelium.sh find constraint   # project principles & rules
mycelium.sh find warning      # known fragile things
mycelium.sh context <file>    # everything known about it
```

## After Work

```bash
mycelium.sh note <file> -k <kind> --slot <your-name> -m "<insight>"
mycelium.sh note HEAD -k context -m "What I did and why."
```

## Kinds

| Kind | When to use |
|------|-------------|
| `decision` | Why something was chosen—rationale that outlives the commit message |
| `context` | Background needed before touching this code |
| `summary` | What a file or module does |
| `warning` | Fragile areas, footguns, non-obvious breakage |
| `constraint` | Hard rules—must be retryable, must not depend on X |
| `observation` | Something noticed but not yet acted on |
| `value` | Cultural principles—guides judgment |
| `todo` | Planned work—compost when done |

## Subdaimon Slots

Each subdaimon writes to its own slot to preserve identity:

```bash
mycelium.sh note src/auth.rs -k warning --slot bohen -m "Race condition in token refresh."
mycelium.sh note src/auth.rs -k decision --slot demiurge -m "Used mutex over channel."
```

`context` aggregates all slots. `read --slot <name>` reads one.

## Quality Gates

Before writing a note, validate:
1. **Novelty**: Does a similar note already exist? (`mycelium.sh read <file>`)
2. **Specificity**: Is this about *this file* or the whole project? (Project-level → `mycelium.sh note .`)
3. **Durability**: Will this matter in 2 weeks? (Ephemeral → working memory, not mycelium)
4. **No secrets**: No API keys, tokens, passwords, or PII

## Composting

Notes go stale when files change. Compost after meaningful work:

```bash
mycelium.sh compost <file> --dry-run    # see what's stale
mycelium.sh compost <oid> --compost     # absorb and archive
mycelium.sh compost <oid> --renew       # still true, re-attach
```

`constraint` and `value` notes age gracefully—prefer `--renew` over `--compost`.

## Commands Reference

```
mycelium.sh note [target] -k <kind> -m <body>    Write a note
mycelium.sh read [target]                         Read a note
mycelium.sh follow [target]                       Read + resolve edges
mycelium.sh refs [target]                         All notes pointing at target
mycelium.sh context <path>                        All notes for a path
mycelium.sh find <kind>                           Find by kind
mycelium.sh compost [path|oid] [--dry-run]        Triage stale notes
mycelium.sh doctor                                Graph health
mycelium.sh prime                                 Full context for agents
```

## Setup (once per repo)

```bash
mycelium.sh activate        # notes visible in git log
mycelium.sh sync-init       # notes travel with fetch/push
```

## Bash 3.2 Compatibility

macOS ships bash 3.2 which has a bug with empty arrays under `set -u`.
The installed `mycelium.sh` at `~/.local/bin/` has been patched with the
`${array[@]+"${array[@]}"}` pattern for compatibility.
