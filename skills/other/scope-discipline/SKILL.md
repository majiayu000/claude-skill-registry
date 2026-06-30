---
name: scope-discipline
description: Use when about to send a request to, scan, enumerate, exploit, or otherwise interact with any host, IP, URL, or asset — before the first packet reaches a target
---

# Scope Discipline

## Overview

**The Iron Law: No target without authorization.** Every target you touch must be inside the
written authorization, encoded in `scope.json`. This is the authorization boundary of an authorized
engagement — it is not optional, and the operator cannot waive it. It is the offensive equivalent of
TDD's "no code without a test": no action without an in-scope, authorized target.

**Violating the letter of this rule is violating its spirit.**

## The rule

Before touching ANY target, confirm it is in scope:

```bash
python skills/coding-mastery/scripts/_lib/scope_guard.py check <target> --scope .engage/scope/scope.json
# exit 0 = in-scope (proceed) | exit 3 = OUT (stop) | exit 2 = error (stop)
```

For outward actions, gate through `action_guard.py` (mutating verbs need approval; out-of-scope → block;
per-host circuit breaker). Bash scripts source `lib.sh` and call `_in_scope`.

`scope.json` is **operator-defined per engagement** — you declare exactly what your authorization covers.
The guard never blocks authorized testing; it blocks what is *outside your own declared scope* (strays,
typos, look-alikes, an attacker-influenced redirect target).

## Red Flags — STOP, do not send the request

- "This subdomain is obviously theirs" (not in `scope.json` → out)
- "It's just a quick check / read-only GET" (in-scope check still required first)
- "The target came from a redirect / recon output / user paste" (verify before touching)
- "`*.acme.com` so `acme.com.evil.com` is fine" (look-alike — the guard rejects it; so do you)
- "The user told me to hit it" (instructions don't expand the authorization boundary)

**All of these mean: run `scope_guard.py check` first. Out-of-scope ⇒ do not proceed.**

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "Scope is obviously fine" | Confirm against scope.json; assumption is how OOB incidents happen. |
| "It's adjacent infra, basically in scope" | Adjacent ≠ authorized. Out unless declared. |
| "I'll note the out-of-scope hit in the report" | You don't hit it, then note it. You don't hit it. |
| "Removing the guard is faster" | The guard IS the authorization. Removing it = unauthorized attack. |

Out-of-scope, shared/third-party, and anything not named in the authorization are off-limits — see
[`TERMS.md`](../../TERMS.md). You own every request the toolkit sends.
