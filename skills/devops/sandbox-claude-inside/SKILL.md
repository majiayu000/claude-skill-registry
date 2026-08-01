---
name: sandbox-claude-inside
description: Run Claude Code INSIDE a ca-sandbox box (`--with-claude`). Routed to when the user wants an agent loop running against an isolated, ephemeral sandbox rather than the host. Authenticates via an env-injected CLAUDE_CODE_OAUTH_TOKEN with no host bind of ~/.claude; the image pins the CLI and disables the autoupdater; HOME is backed by a named volume so the .claude state persists across restart. Five gated phases — posture, image, token, run, teardown. The hard default is offline or Anthropic-domains-only egress, and the token volume is NEVER co-mounted with an untrusted-code run; both are enforced, not advised.
---

# sandbox-claude-inside

Put Claude Code in the box, not the box on your machine. `--with-claude` runs the
CLI inside a host-FS-isolated ca-sandbox container, authenticating from an
env-injected token with no host bind of `~/.claude` — the mechanism proven by
Spike B (`.codearbiter/spikes/ca-sandbox-claude-auth.md`, CONFIRM-07). It is the
deliberately-hardened lane: a token in a box is stealable, so the posture is locked
down by construction (offline or Anthropic-only egress, token volume never shared
with untrusted code), never left to operator discipline.

## Pre-flight

Read these, or STOP and surface the gap — never guess the token source, the egress
posture, or the persistence mechanism:

- `${CLAUDE_PROJECT_DIR}/.codearbiter/spikes/ca-sandbox-claude-auth.md` — the
  proven auth path (env token → real `401` on a dummy), the named-volume HOME
  persistence mechanism, and the load-bearing caveat that fixes the hard default.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/spikes/ca-sandbox-egress.md` — why the
  egress allowlist is EXPERIMENTAL (CDN drift + DNS-exfil hole), so `offline` is
  the only GUARANTEED posture for a token-bearing box.
- `${CLAUDE_PROJECT_DIR}/.codearbiter/decisions/0007-second-plugin-ca-sandbox.md`
  — the governing decision; ca-sandbox is infrastructure, sibling to `ca`.

The driver lives at `plugins/ca-sandbox/tools/claude-inside.ts`
(`buildClaudeImageDockerfile`, `buildClaudeRunArgs`, `runClaudeInside`,
`TokenCoMountRejectedError`). The token MUST come from the approved store as
`CLAUDE_CODE_OAUTH_TOKEN`; in tests use a DUMMY token only.

## Phase 1 — Posture · gate: BLOCK

Fix the egress posture and the trust boundary BEFORE anything is built or started.
A token-bearing box is the one place ca-sandbox's FS-isolation invariant and a live
credential are in direct tension — resolve it here, explicitly.

- **Egress** — choose exactly one: `offline` (default, GUARANTEED — no interface at
  all) or `anthropic-only` (the EXPERIMENTAL Anthropic-domains allowlist, for
  interactive inference). No third option exists; a wide-open policy is rejected.
- **Trust boundary** — the box runs Claude, NOT the untrusted source repo. Confirm
  the run mounts only the token/home volume, never the source volume at
  `/work/repo`. If the user wants Claude to read an untrusted repo, that is a
  SEPARATE, source-only box without the token — say so.

Gate: a named egress posture (`offline` or `anthropic-only`) AND an explicit
statement that this box carries the token and NOT untrusted source. If the user
asks for both at once, STOP and split them — the co-mount is forbidden (Phase 4).

## Phase 2 — Image · gate: BLOCK

Build (or reuse) the pinned `--with-claude` image via `buildClaudeImageDockerfile`.

- The image installs `@anthropic-ai/claude-code@<pinned>` — a PINNED semver,
  never `@latest` — and bakes `DISABLE_AUTOUPDATER=1` so the box never silently
  pulls an unreviewed CLI into a token-bearing environment.
- The base is `node:22-slim` (Spike B installed the CLI cleanly there), bound to a
  reviewed content DIGEST — `node:22-slim@sha256:…`, the `CLAUDE_BASE_IMAGE`
  constant. The tag is kept only as human-readable provenance; docker resolves the
  digest. This is the driver's highest-stakes pin: the base image's code runs in
  the SAME container as `CLAUDE_CODE_OAUTH_TOKEN`, so a retag or registry
  compromise would otherwise execute unreviewed code alongside a live credential.
  Pinning the CLI version alone is not enough. HOME is baked to the in-container
  claude home so the named volume has a writable mount point.

Gate: the image carries the exact pinned version (`claude --version` reports it),
`DISABLE_AUTOUPDATER=1`, and a digest-pinned base. A floating or unpinned CLI —
or an unpinned base image — fails the gate; image reproducibility is
non-negotiable for a token box. Changing the digest is a reviewed dependency
change: re-resolve it with `docker buildx imagetools inspect`, then re-run the
credential-boundary and isolation suites.

## Phase 3 — Token · gate: BLOCK

Source the OAuth token and confirm it is injected as ENV, never bound from the host.

- The token comes from the approved secret store as `CLAUDE_CODE_OAUTH_TOKEN`
  (auth-precedence #5, from `claude setup-token`). It is env-injected
  (`-e CLAUDE_CODE_OAUTH_TOKEN=…`) — this IS the auth path; no host bind of
  `~/.claude` is required or permitted.
- The token MUST NOT be echoed to logs, written to a file the source volume can
  read, or passed into any LLM prompt. Prefer a scoped/short-lived setup-token.
- Persistence: HOME is backed by a docker NAMED VOLUME, so the credential store
  `$HOME/.claude/.credentials.json` survives a restart on the volume — not on the
  host. A fresh container on the same volume resumes the session.

Gate: the token is from the approved store, env-injected (not bound), and never
logged/persisted to a host-readable location. The home volume is a NAMED VOLUME,
not a bind.

## Phase 4 — Run · gate: BLOCK

Start the box via `buildClaudeRunArgs` / `runClaudeInside`. The builder enforces the
guarantees by construction — do not hand-roll a `docker run`.

- Mounts go through the one chokepoint (`mounts.ts`): the home named volume at HOME
  and a tmpfs `/tmp`. NO bind mount, NO `/var/run/docker.sock`, NEVER
  `--privileged`. Read-only root, non-root, `no-new-privileges`, resource caps —
  the same structural lockdown as any sandbox.
- The egress posture from Phase 1 is applied: `offline` → `--network none`;
  `anthropic-only` → the experimental Anthropic-domains allowlist (custom bridge +
  `NET_ADMIN`/`NET_RAW` + the init-firewall script applied inside the box).
- The CO-MOUNT GUARD: supplying a `sourceVolume` throws `TokenCoMountRejectedError`.
  The token volume is NEVER co-mounted with an untrusted-code run. This is the
  load-bearing Spike B caveat made structural — it is not optional.

Gate: the run argv was produced by the builder (not hand-rolled), the co-mount
guard was not bypassed, the posture matches Phase 1, and a dummy token reaches AUTH
(a real `401 Invalid bearer token`) — proving the env token is the auth path before
any real credential is used.

## Phase 5 — Teardown · gate: BLOCK

Tear down per the lifecycle rules, deciding the fate of the credential volume.

- Remove the container (`docker rm -f`). By default REMOVE the home/token volume
  too — a persisted credential store is a standing exfil target; keep it only on an
  explicit, recorded `--keep-volume` decision.
- Every object created carries the `ca.sandbox=1` label (plus a build marker in
  tests); the lifecycle/registry surfaces (`destroy`, `prune`) reclaim them.
- Confirm zero leaked labeled containers/volumes after teardown (cached images
  excepted).

Gate: container removed; the credential volume removed unless `--keep-volume` was
explicitly chosen and recorded; no leaked `ca.sandbox=1` objects remain.

## Hard rules

- MUST authenticate via an env-injected `CLAUDE_CODE_OAUTH_TOKEN` — NEVER a host
  bind of `~/.claude`.
- MUST install a PINNED `@anthropic-ai/claude-code@<semver>` with
  `DISABLE_AUTOUPDATER=1`; MUST NOT use `@latest` or an unpinned CLI.
- MUST default `--with-claude` egress to `offline` or `anthropic-only`; MUST NOT
  give a token-bearing box wide-open egress.
- MUST NEVER co-mount the token/credential volume with an untrusted-code run (a run
  that mounts the source volume at `/work/repo`) — `buildClaudeRunArgs` throws
  `TokenCoMountRejectedError` and that throw MUST NOT be bypassed.
- MUST back HOME with a docker NAMED VOLUME (never a bind) so the `.claude`
  credential store persists across restart on the volume, not on the host.
- MUST NOT give the box a host bind mount, the docker socket, or `--privileged`;
  read-only root, non-root, and cap-drop hold as for any sandbox.
- MUST source the token from the approved store; MUST NOT log it, write it to a
  host-readable file, or pass it into any LLM prompt. Use a DUMMY token in tests.
- MUST remove the credential volume on teardown unless `--keep-volume` is an
  explicit, recorded decision.
- MUST treat the egress allowlist as EXPERIMENTAL (Spike C): for a token-bearing
  box, `offline` is the only GUARANTEED posture.
