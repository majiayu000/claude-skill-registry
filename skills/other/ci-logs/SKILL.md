---
name: ci-logs
description: Analyze CI logs from ci.aztec-labs.com. Use this instead of WebFetch for CI URLs.
argument-hint: <url-or-hash>
---

# CI Log Analysis

When you need to analyze logs from ci.aztec-labs.com, delegate to the `analyze-logs` subagent.

## Usage

1. **Extract the hash** from the URL (e.g., `http://ci.aztec-labs.com/e93bcfdc738dc2e0` → `e93bcfdc738dc2e0`)

2. **Spawn the `analyze-logs` subagent** using the Task tool with the hash and focus area (e.g. "errors", "test \<name>", or a custom question) in the prompt.

## Examples

**User asks:** "What failed in http://ci.aztec-labs.com/343c52b17688d2cd"

**You do:** Use the Task tool with `subagent_type: "analyze-logs"` and prompt including the hash `343c52b17688d2cd`, focus on errors, and instruction to download with `yarn ci dlog`.

**For specific test analysis:** Same approach, but set the focus to the test name.

## Do NOT

- Do NOT use WebFetch to access ci.aztec-labs.com (requires auth)
- Do NOT try to curl the URL directly
- Always use the analyze-logs agent which knows how to use `yarn ci dlog`
