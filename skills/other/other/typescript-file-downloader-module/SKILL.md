---
name: typescript-file-downloader-module
description: Add, repair, or standardize an in-repo Node.js TypeScript file downloader module (plain TS or NestJS) with required Referer/User-Agent headers, optional cookie normalization, streamed disk writes, deterministic `DownloadResult` states, and non-throwing error mapping. Use when users ask to build/fix downloader services, enforce safe path and protocol controls, or align existing downloader behavior with stable response contracts.
---

# TypeScript File Downloader Module

## Overview

Implement downloader functionality inside the existing repository structure with a `FileDownloadService` that exposes `download(req): Promise<DownloadResult>`.
Return deterministic `DownloadResult` objects for both success and failure states, including timing, HTTP metadata, file metadata, and normalized error codes.

## Preflight

1. Detect project style first: plain TypeScript app, NestJS app, or mixed monorepo.
2. Reuse existing package manager, scripts, and lint/test tooling already present in the repository.
3. Locate existing downloader-related code and integrate there instead of creating parallel abstractions.
4. Read and apply these references before implementation:
   - `references/implementation-spec.md`
   - `references/error-codes.md`
   - `references/test-plan.md`

## Required Output

When executing this skill, always deliver:

1. In-repo implementation integrated into the existing system (new/updated files in current app structure).
2. Reuse existing workspace/package configuration; do not scaffold a new standalone npm package unless explicitly requested.
3. Export points and module wiring needed for current architecture (plain TS exports or Nest module/provider wiring).
4. A short usage example aligned with the current project style.
5. A statement of the selected HTTP client (`undici` preferred) and why.
6. A sample `DownloadResult` JSON for success and failure.

## Workflow

1. Define or align types first (`DownloadRequest`, `DownloadResult`, progress/event types, options).
2. Implement input validation and path/protocol safety gates before any network call.
3. Implement HTTP download via streaming file writes (never full-memory buffering).
4. Map all known failure paths to standardized `error.code` values and return `state: "failed"` instead of throwing.
5. Add checksum generation for completed downloads and keep result shape stable across outcomes.
6. Add or align module wiring and exports:
   - Plain TS: stable exports from existing index/entry files.
   - NestJS: provider/module wiring and exports for `FileDownloadService`.
7. Add or update tests for minimum acceptance behavior from `references/test-plan.md`.
8. Update existing project docs only if required for discoverability in the current repository.

## Verification Gates

1. Build/typecheck passes with the repository's existing command set.
2. New/updated tests for downloader behavior pass (or clearly report blocker and failing case).
3. Downloader returns deterministic `DownloadResult` objects for both success and failure.
4. No path traversal outside allowed root unless explicit override is enabled.
5. No `file:` or non-HTTP(S) URL acceptance.
6. No default console logging unless logger/callback is explicitly configured.

## Guardrails

1. Never throw for expected failure cases. Return `state: "failed"` and a structured `error`.
2. Keep response shape stable across all outcomes.
3. Stay silent by default (no console logging unless logger or callback is provided).
4. Default to safe path behavior: deny traversal outside `process.cwd()` unless explicitly allowed by options.
5. Forbid non-HTTP(S) protocols and reject `file:` URLs.
6. Prefer minimal-change integration into existing folders, naming, and module boundaries.

## Reference Files

1. Use `references/implementation-spec.md` for DTO contract, layout, behaviors, and defaults.
2. Use `references/error-codes.md` for standardized `error.code` mapping.
3. Use `references/test-plan.md` for minimum acceptance tests.
