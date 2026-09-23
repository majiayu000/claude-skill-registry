---
name: deploy-landed
description: Prove a deploy landed — the served revision is the commit you meant, its env is present, and the product does its job — instead of trusting the deploy command's exit code. Also catches server drift before a pull or deploy. Use after any deploy, rollout, restart or server-side fix ("задеплой", "выкати", "проверь на проде", "почему не обновилось"). Loaded by devops, l3-support, infra-provisioner.
when_to_use: |
  Apply when:
  - you ran, or are about to report, a deploy, a rollout, a container restart, a hot-fix on a server
  - the operator asks whether something is live, or says it "did not update" / "still broken"
  - you are about to `git pull` or build on a server that someone may have patched by hand
  Do NOT apply to:
  - a change that does not reach a runtime (docs, tests only) — CI is the check there
effort: low
allowed-tools: Read, Bash, Grep
---

# deploy-landed — a deploy is done when the running thing is the thing you meant

A deploy command's exit code says the command finished. It does not say the new code
is serving, that its configuration arrived, or that the product works. Every trap
below produced a green exit and a broken or stale product on a real project:

| Trap | What happened |
|---|---|
| `git pull` failed, the build went on | The build succeeded from the **old** code and reported success |
| `nohup … &` | Exit 0 twice for a process that died at once |
| `docker exec` into a container | It does not inherit the entrypoint's env: two "config is missing" readings were false |
| `sed -i` / `docker cp` on a bind-mounted file | Replaced the inode; the container kept reading the old file |
| A fix applied only on the server | Lost on the next deploy — it was never in git |
| wrangler / Pages | `functions/` not deployed, `_headers` ignored, five deploys to notice |
| Prod behind SSO | Answers 401/302 to **every** path, including ones that do not exist — proves nothing about a route |
| `/health` green | For six hours while the engine made no trades |

## Before: is the server what git says it is?

Before pulling or building on a host someone can reach by hand:

```bash
git -C /srv/app status --porcelain        # anything here is a patch that is not in git
git -C /srv/app log -1 --format=%H        # what the host thinks it runs
```

Anything uncommitted on the host is either committed first or reported as drift — never
overwritten silently, and never left as the only copy of a fix.

## After: four checks, each with its evidence

1. **Revision.** What is serving equals the commit you meant.
   - Cloud Run / k8s: the live revision's image tag or digest, then
     `git merge-base --is-ancestor <commit> <image-tag-sha>`.
   - Pages / Workers / Vercel: the deployment id and its commit.
   - A plain host: the running process's start time is after the deploy, and the file
     it serves has the new content (`grep` for a string the change introduced).
   - A `/version` endpoint, when the app has one, beats all of the above.
2. **Configuration.** The variables and secrets the new code reads are present in the
   **running process** — count them against the list the code expects. In a container,
   read them from PID 1 (`cat /proc/1/environ | tr '\0' '\n'`), not from `docker exec env`.
   After `--set-secrets`/`--set-env-vars`, check that the ones you did not name are still
   there: those flags replace the whole set.
3. **Function.** One request that does the product's job and returns something you can
   compare to a known value — an order created, a row written, a trade placed on paper.
   A health endpoint proves the process is up, nothing more.
4. **Startup errors.** Logs for the new revision since it started, at WARNING and above.
   Zero lines is a finding only if you saw the logs flowing at all.

## Report

End the deploy report with this block. A check you could not run is `NOT CHECKED` with
the reason — never omitted, never `PASS`.

```
DEPLOY-LANDED <service> @ <commit>
  revision : PASS — serving <revision/deployment id> built from <sha>
  config   : PASS — 14/14 expected vars present in PID 1
  function : PASS — POST /orders → 201, row id 8812 visible in DB
  startup  : PASS — 0 WARNING+ lines since 12:04:10
```

A FAIL in any line means the deploy is not done, whatever the command printed.
