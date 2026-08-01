---
name: privacy-guard
description: Prevents private infrastructure details (node hostnames, internal project names, local usernames and personal emails, absolute home paths, private and VPN IP ranges) from leaking into public repositories through commits, PRs, docs or release artifacts. Use when working in a public or soon-to-be-public repo, before commits or releases, when writing deployment docs for an OSS project, or when the user asks to "set up the privacy guard", "install privacy-guard", "check for leaks", "protect this public repo". Bootstraps a pre-commit hook backed by a gitignored local denylist plus gitleaks.
argument-hint: "[setup <repo-path> | check | update-denylist]"
---

# privacy-guard

Guard against accidentally publishing details of your private infrastructure in public
repositories (or in repositories that may become public later). Two legs: behavioral rules
for the Claude session, always on, and a per-repo technical gate: a pre-commit hook backed
by a gitignored local denylist, plus gitleaks.

## Threat model

The public repository is the boundary. Anything that describes your private infrastructure
must not cross it, in any form: committed files, commit messages, branch names, PR and
issue bodies, release notes, published artifacts, screenshots.

**Sensitive, never in a public repo:**
- node hostnames and internal aliases (workstations, VPS, client machines)
- names of internal projects and service instances that were never published
- local usernames, personal and work email addresses
- personal domains and URLs of internal services
- absolute paths of home directories and internal mounts
- private-network IP ranges and VPN address space (for example the Tailscale CGNAT range
  `100.64.0.0/10`)
- cookie files, tokens, credentials (also covered by gitleaks)

**Not sensitive, fine in public docs:**
- public products and technologies named generically (Tailscale, Docker, n8n)
- the maintainer's public GitHub username
- deployment patterns described in generic form ("a Docker host reachable over your private
  network / behind a VPN")

The concrete list of sensitive tokens is yours and stays private. This skill ships
`references/denylist-template.txt`, a placeholder-only starting point: fill it in a private
location (a private dotfiles repo, a private notes repo) and treat that filled copy as the
seed you propagate from. Never commit the filled version to a public repo.

## Behavioral rules (Claude session in a public repo)

1. Never write internal tokens into committed files. Private deployment details are
   documented in a private repo or in a gitignored `.local/` directory, never in the public
   repo's docs.
2. The user mentioning internal names in conversation does NOT authorize writing them into
   the repo: the conversation is private, the repo is not.
3. Before every commit: re-read the diff looking for denylist tokens. The hook is the safety
   net, not the first check.
4. This applies outside files too: commit messages, branch names, PR and issue titles and
   bodies, CHANGELOG entries, published artifacts.
5. If a sensitive token has already reached published git history: tell the user immediately
   (rotation, history rewrite with BFG or filter-repo are their calls), do not just remove it
   from the tip.

## Per-repo setup (`setup <repo-path>`)

From the root of the target repo:

1. Copy `references/check_privacy.sh` to `scripts/check_privacy.sh` and make it executable.
2. Create `.local/privacy-denylist.txt` from your private seed (or from
   `references/denylist-template.txt` on a first run), adapting the patterns to this repo's
   context.
3. Make sure `.gitignore` contains `.local/`.
4. Add the blocks from `references/pre-commit-snippet.yaml` to `.pre-commit-config.yaml`
   (gitleaks + privacy-denylist).
5. Run `pre-commit install`, adding `--hook-type pre-push` if the repo uses push hooks.
6. Verify: create a temporary file containing one token from the denylist and check that
   `scripts/check_privacy.sh <file>` exits with code 1. An unfilled denylist (only comments)
   makes the hook a silent no-op, so this step is what tells you the guard is actually armed.

Design property: the denylist is NOT committed, because publishing the list would reveal the
very tokens it protects. As a consequence the hook is a no-op for external contributors and
in CI. Generic secrets (keys, tokens) stay covered by gitleaks, which runs everywhere.

## Denylist maintenance (`update-denylist`)

When a new sensitive token appears (a new node, a new instance, a new domain):
1. update your private seed, the single source of truth;
2. propagate it to the `.local/privacy-denylist.txt` of every public repo active on the node.

## Known limits

- The guard is client-side: it protects commits made from a node that has the denylist.
- It does not cover manual pastes into the GitHub web UI. Only the behavioral rules do.
- Word-boundary patterns (`\bfoo\b`) can produce false positives inside hashes and IDs. The
  hook prints the matched lines, so judge case by case.
