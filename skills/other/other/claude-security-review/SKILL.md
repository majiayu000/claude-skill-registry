---
name: claude-security-review
description: Security-focused review for Hyperlane protocol code. Use for Solidity contracts, Rust agents, and infrastructure changes.
---

# Security Review Skill

Use this skill for security-focused code review of Hyperlane protocol code.

## When to Use

- Reviewing Solidity smart contracts
- Reviewing Rust agent code
- Checking cross-chain security concerns
- Infrastructure or config changes

## Instructions

Read and apply the security guidelines from `.github/prompts/security-scan.md` to review the code changes.

Report findings with severity ratings (Critical/High/Medium/Low/Informational) and suggested fixes.

### For PR Reviews

When reviewing a PR, deliver feedback using `/inline-pr-comments` to post inline comments on specific lines.
