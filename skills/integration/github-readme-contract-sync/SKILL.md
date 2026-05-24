---
name: "github-readme-contract-sync"
description: "Write a public README that stays aligned with live build, runtime, and installer contracts"
domain: "documentation"
confidence: "high"
source: "2026-03-16 README rewrite"
---

## Context

Use this when a repository needs a GitHub-facing README for an actively developed product with different requirements for source builds, local runs, and installed runtime support.

## Pattern

1. Verify the actual stack and seams from live project files, not memory.
2. Separate **build prerequisites** from **installed-app runtime prerequisites**.
3. Document any dev-time content-loading seam that changes what contributors see locally.
4. Prefer architecture, workflow, and caveat sections over marketing copy.
5. Only claim capabilities that are visible in source, tests, or validated build output.
6. If the product is mid-flight, state that directly and name what is complete versus still being hardened.

## Why It Matters

Public READMEs drift quickly when they collapse installer requirements, developer setup, and runtime dependencies into one section. That causes bad first-run guidance and makes the repo look less trustworthy than the code actually is.

## PanelNester Example

- Build requirements: `.NET 8 SDK`, Node.js/npm
- Installed-app requirements: x64 `.NET 8 Desktop Runtime`, `Microsoft Edge WebView2 Runtime`
- Local-run seam: desktop host prefers `src\PanelNester.WebUI\dist` and falls back to `src\PanelNester.Desktop\WebApp`
- Public status: core workflows implemented; repo is still in active hardening
