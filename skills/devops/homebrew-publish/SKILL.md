---
name: homebrew-publish
description: Publish CLIs/TUIs to Homebrew via a personal tap. Use when asked to create or manage a Homebrew tap repo, generate or update formulae, compute sha256, test installs, or ship new releases for Go, Rust, Node/TypeScript, Python, or prebuilt binaries.
---

# Homebrew Publish

## Overview
Create or update a Homebrew tap and formulae so users can install a project's CLI/TUI with `brew install OWNER/tap/<formula>`.

## Workflow

### 1) Gather inputs
- Confirm GitHub owner, tap name, and whether the tap repo already exists.
- Collect project repo URL, release tag/version, and the source tarball URL or prebuilt asset URL(s).
- Identify build system and language (Go, Rust, Node/TypeScript, Python, or other).
- Define binary name and a minimal `test do` command.
- Confirm target platforms/architectures and whether bottles are desired.

### 2) Ensure tap repo exists (skip if already set)
- Create a tap repo using the short form `OWNER/tap` when possible.
- Run:
  - `brew tap-new OWNER/homebrew-tap` (or `homebrew-<tapname>`)
  - `gh repo create OWNER/homebrew-tap --push --public --source "$(brew --repository OWNER/homebrew-tap)"`

### 3) Create the formula skeleton
- Prefer stable source tarballs from release tags.
- Run:
  - `brew create <url-to-tarball> --tap OWNER/homebrew-tap --set-name <formula>`

### 4) Implement the formula
- Edit `Formula/<formula>.rb` and wire build/install/test.
- Pick a language template from references:
  - `references/formula-go.md`
  - `references/formula-rust.md`
  - `references/formula-node.md`
  - `references/formula-python.md`
  - `references/formula-prebuilt.md`
- Ensure `desc`, `homepage`, `url`, `sha256`, and `license` are correct.

### 5) Compute sha256
- Use `shasum -a 256 <file>` for local files.
- For remote URLs, run `curl -L <url> | shasum -a 256`.

### 6) Test locally
- Run `brew install --build-from-source OWNER/tap/<formula>`.
- Run `brew test OWNER/tap/<formula>`.
- Optionally run `brew audit --strict --online OWNER/tap/<formula>`.

### 7) Commit and push
- Commit in the tap repo and push to GitHub.

### 8) Update for new releases
- Update `url` and `sha256` (and `version` if needed).
- Re-run tests, commit, and push.

## Notes
- Prefer source builds unless a prebuilt binary is required.
- If bottles are enabled, keep the default workflows created by `brew tap-new` and follow their publish instructions.
