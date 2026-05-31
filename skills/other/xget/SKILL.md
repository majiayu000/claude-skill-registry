---
name: xget
description:
  Use when tasks involve Xget URL rewriting, registry/package/container/API
  acceleration, integrating Xget into Git, download tools, package managers,
  container builds, AI SDKs, CI/CD, deployment, self-hosting, or adapting
  commands and config from the live README `Use Cases` section into files,
  environments, shells, or base URLs.
---

# Xget

Default to execution, not instruction. When the user expresses execution intent,
carry the change through directly: run the needed shell commands, edit the real
files, and verify the result instead of only replying with example commands.
Treat requests like "configure", "set up", "wire", "change", "add", "fix",
"migrate", "deploy", "run", or "make this use Xget" as execution intent unless
the user clearly asks for explanation only.

Resolve the base URL first:

1. use a domain the user explicitly gave
2. otherwise use `XGET_BASE_URL` from the environment
3. if neither exists, ask for the user's Xget base URL and whether it should be
   set temporarily for the current shell/session or persistently for future
   shells
4. use `https://xget.example.com` only as a clearly labeled placeholder for docs
   or templates that do not have a real deployment yet

Prefer [`scripts/xget.mjs`](./scripts/xget.mjs) over manual guessing for live
platform data, URL conversion, and README `Use Cases` lookup.

Only stop to ask when a missing fact blocks safe execution, such as an unknown
real base URL for a command that must run against a live deployment. If the user
only needs docs or templates, use the placeholder path rules below.

## Workflow

1. Classify the task before reaching for examples:
   - execution intent: the user wants commands run, files changed, or config
     applied now
   - guidance intent: the user explicitly wants examples, explanation, or a
     template without applying it yet
   - then bucket the technical area: one-off URL conversion or prefix lookup;
     Git or download-tool acceleration; package-manager or language-ecosystem
     configuration; container image, Dockerfile, Kubernetes, or CI/CD
     acceleration; AI SDK / inference API base-URL configuration; deploying or
     self-hosting Xget itself
2. Complete the base-URL preflight above. If the user wants help setting
   `XGET_BASE_URL`, open [the reference guide](./references/REFERENCE.md) and:
   - when the user asked you to set or wire it, run the shell-appropriate
     temporary or persistent commands directly when the environment allows it
   - when you cannot safely execute, ask the smallest blocking question or give
     the exact command with the missing value clearly called out
3. Pull live README guidance in two steps instead of loading the whole section
   by default:
   - list candidate headings with `node scripts/xget.mjs topics --format json`
   - narrow with `--match` or fetch a specific section with
     `node scripts/xget.mjs snippet --base-url https://xget.example.com --heading "Docker Compose Configuration" --format text`
4. Prefer the smallest relevant live subsection. If a repeated child heading
   like `Use in Project` is ambiguous, fetch its parent section instead.
5. Adapt the live guidance to the user's real task:
   - for execution intent, apply the change end-to-end instead of stopping at
     example commands
   - run commands yourself when the request is to install, configure, rewrite,
     switch, migrate, test, or otherwise perform the change
   - edit the actual config or source files when the user wants implementation,
     not just explanation
   - keep shell commands aligned with the user's OS and shell
   - preserve existing project conventions unless the user asked for a broader
     rewrite
   - after changing files or running commands, perform a lightweight
     verification step when practical
6. Refresh the live platform map with
   `node scripts/xget.mjs platforms --format json` when the answer depends on
   current prefixes, and use `convert` for exact URL rewrites.
7. Combine multiple live sections when the workflow spans multiple layers. For
   example, pair a package-manager section with container, deployment, or `.env`
   guidance when the user's project needs more than one integration point.
8. Before finishing, sanity-check that every command, file edit, or example uses
   the right Xget path shape:
   - repo/content: `/{prefix}/...`
   - crates.io HTTP URLs: `/crates/...` rather than `/crates/api/v1/crates/...`
   - inference APIs: `/ip/{provider}/...`
   - OCI registries: `/cr/{registry}/...`
9. If the live platform fetch fails or an upstream URL does not match any known
   platform, say so explicitly and fall back to the stable guidance in
   [`references/REFERENCE.md`](./references/REFERENCE.md) instead of inventing a
   prefix.
