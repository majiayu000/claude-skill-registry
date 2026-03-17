---
name: sketch-security-guardrails
description: Security and privacy guardrails for Sketch Magic. Use when handling API keys, logs, uploads, telemetry, or when debugging errors to avoid leaking secrets or user images.
---

# Sketch Security Guardrails

## Overview
Provide safe handling rules for keys, logs, and user uploads while debugging or adding telemetry.

## Workflow
1. **Never log secrets**: API keys, bearer tokens, or auth headers.
2. **Never log raw images**: no base64 image bytes or file payloads.
3. **Avoid full prompts**: log only prompt length or hash.
4. **Telemetry minimalism**: only metadata (duration, provider, error code).
5. **Review logs before sharing**: scrub console output in proof videos or screenshots.

## Safe Debug Patterns
- Log **error codes** instead of full stack traces when user-visible.
- Use **sample files** or stubbed requests for proof videos.
- Keep logs off by default unless `ENABLE_TELEMETRY=true`.

## References
- `references/security-guardrails.md`
