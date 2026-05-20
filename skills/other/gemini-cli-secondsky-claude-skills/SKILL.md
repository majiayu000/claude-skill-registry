---
name: gemini-cli
description: "Google Gemini CLI for second opinions, architectural advice, code reviews, security audits. Leverage 1M+ context for comprehensive codebase analysis via command-line tool."
license: MIT
metadata:
  version: 2.1.0
  production_tested: true
  gemini_cli_version: 0.13.0+
  last_verified: 2025-11-13
  token_savings: ~60-70%
  errors_prevented: 6+
  keywords:
    - gemini-cli
    - google gemini
    - gemini command line
    - second opinion
    - model comparison
    - gemini-2.5-flash
    - gemini-2.5-pro
    - architectural decisions
    - debugging assistant
    - code review gemini
    - security audit gemini
    - 1M context window
    - AI pair programming
    - gemini consultation
    - flash vs pro
    - AI-to-AI prompting
    - peer review
    - codebase analysis
    - gemini CLI tool
    - shell gemini
    - command line AI assistant
    - gemini architecture advice
    - gemini debug help
    - gemini security scan
    - gemini code compare
---
# Gemini CLI

**Leverage Gemini's 1M+ context window as your AI pair programmer within Claude Code workflows.**

This skill teaches Claude Code how to use the official Google Gemini CLI (`gemini` command) to get second opinions, architectural advice, debugging help, and comprehensive code reviews. Based on production testing with the official CLI tool.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [When to Use Gemini Consultation](#when-to-use-gemini-consultation)
3. [Installation](#installation)
4. [Model Selection: Flash vs Pro](#model-selection-flash-vs-pro)
5. [Top 3 Use Cases](#top-3-use-cases)
6. [Integration Example](#integration-example)
7. [Top 3 Errors & Solutions](#top-3-errors--solutions)
8. [When to Load References](#when-to-load-references)
9. [Production Rules](#production-rules)

---

## Quick Start

**Prerequisites**:
- Gemini CLI installed (`bun add -g @google/gemini-cli`)
- Authenticated with Google account (run `gemini` once to authenticate)

**Core Command Patterns**:

```bash
# Quick question (non-interactive with -p flag)
gemini -p "Should I use D1 or KV for session storage?"

# Code review with file context
cat src/auth.ts | gemini -p "Review this authentication code for security vulnerabilities"

# Architecture advice using Pro model
gemini -m gemini-2.5-pro -p "Best way to handle WebSockets in Cloudflare Workers?"

# With all files in directory
gemini --all-files -p "Review this auth implementation for security issues"

# Interactive mode for follow-up questions
gemini -i "Help me debug this authentication error"
```

**Critical**: Always use `-p` flag for non-interactive commands in automation/scripts.

---

## When to Use Gemini Consultation

### ALWAYS Consult (Critical Scenarios)

Claude Code should **automatically invoke Gemini** in these situations:

1. **Major Architectural Decisions**
   - Example: "Should I use D1 or KV for session storage?"
   - Example: "Durable Objects vs Workflows for long-running tasks?"
   - **Pattern**: `gemini -m gemini-2.5-pro -p "[architectural question]"`

2. **Security-Sensitive Code Changes**
   - Authentication systems, payment processing, PII handling
   - API key/secret management
   - **Pattern**: `cat [security-file] | gemini -m gemini-2.5-pro -p "Security audit this code"`

3. **Stuck Debugging (2+ Failed Attempts)**
   - Error persists after 2 debugging attempts
   - Stack trace unclear or intermittent bugs
   - **Pattern**: `gemini -p "Help debug: [error message]" < error.log`

4. **Large Refactors (5+ Files)**
   - Core architecture changes, database schema migrations
   - **Pattern**: `gemini --all-files -m gemini-2.5-pro -p "Review this refactoring plan"`

5. **Context Window Pressure (70%+ Full)**
   - Approaching token limit, need to offload analysis
   - **Pattern**: `cat large-file.ts | gemini -p "Analyze this code structure"`

### OPTIONALLY Consult

6. **Unfamiliar Technology** - Using library/framework for first time
7. **Code Reviews** - Before committing major changes

---

## Installation

### 1. Install Gemini CLI

```bash
bun add -g @google/gemini-cli
```

### 2. Authenticate

```bash
gemini
```

Follow the authentication prompts to link your Google account.

### 3. Verify Installation

```bash
gemini --version  # Should show 0.13.0+
gemini -p "What is 2+2?"  # Test connection
```

---

## Model Selection: Flash vs Pro

### gemini-2.5-flash (Default)
- **Speed**: ~5-25 seconds
- **Quality**: Good for most tasks
- **Use For**: Code reviews, debugging, quick questions
- **Cost**: Lower

```bash
gemini -m gemini-2.5-flash -p "Review this function for performance issues"
```

### gemini-2.5-pro
- **Speed**: ~15-30 seconds
- **Quality**: Excellent, thorough analysis
- **Use For**: Architecture decisions, security audits, major refactors
- **Cost**: Higher

```bash
gemini -m gemini-2.5-pro -p "Security audit this authentication system"
```

### Quick Decision Guide

```
Quick question? → Flash
Security/architecture? → Pro
Debugging? → Flash (try Pro if stuck)
Refactoring 5+ files? → Pro
```

**CRITICAL FINDING**: Flash and Pro can give **opposite recommendations** on the same question (both valid, different priorities). Flash prioritizes performance, Pro prioritizes consistency/correctness. For details, load `references/models-guide.md`.

---

## Top 3 Use Cases

### 1. Security Audit

```bash
# Audit authentication code
cat src/middleware/auth.ts | gemini -m gemini-2.5-pro -p "
Security audit this authentication middleware. Check for:
1. Token validation vulnerabilities
2. Timing attack risks
3. Error handling leaks
4. CSRF protection
5. Rate limiting
"
```

### 2. Architecture Decision

```bash
# Compare technologies with context
gemini -m gemini-2.5-pro -p "
Context: Building Cloudflare Worker with user authentication.

Question: Should I use D1 or KV for storing session data?

Considerations:
1. Session reads on every request
2. TTL-based expiration
3. Cost under 10M requests/month
4. Deployment complexity
"
```

### 3. Debugging Root Cause

```bash
# Analyze error logs with context
tail -100 error.log | gemini -p "
These errors started after deploying auth changes. What's the likely root cause?

Context:
- Added JWT validation middleware
- Using @cloudflare/workers-jwt
- Errors only on /api/* routes
"
```

**For more use cases**: Load `references/models-guide.md` for performance optimization, refactoring plans, and code reviews.

---

## Integration Example

### Claude Consulting Gemini Automatically

**Scenario**: User asks architectural question

```
User: "Should I use D1 or KV for storing user sessions?"

Claude (internal): This is an architectural decision. Consult Gemini for second opinion.

[Runs: gemini -m gemini-2.5-pro -p "Compare D1 vs KV for user session storage in Cloudflare Workers. Consider: read/write patterns, cost, performance, complexity."]

Claude (to user): "I've consulted Gemini for a second opinion. Here's what we both think:

My perspective: [Claude's analysis]
Gemini's perspective: [Gemini's analysis]

Key differences: [synthesis]
Recommendation: [combined recommendation]"
```

**Key Pattern**: Synthesize both perspectives, don't just forward Gemini's response.

---

## Top 3 Errors & Solutions

### Error 1: Not Authenticated

**Error**: `Error: Not authenticated`

**Solution**:
```bash
gemini  # Follow authentication prompts
```

### Error 2: Model Not Found

**Error**: `Error: Model not found: gemini-2.5-flash-lite`

**Cause**: Model deprecated or renamed (flash-lite doesn't exist)

**Solution**: Use stable models only:
```bash
gemini -m gemini-2.5-flash -p "Your question"
gemini -m gemini-2.5-pro -p "Your question"
```

### Error 3: Command Hangs

**Cause**: Interactive mode when expecting non-interactive

**Solution**: Always use `-p` flag for non-interactive commands

```bash
# ✅ Correct
gemini -p "Question"

# ❌ Wrong (will hang waiting for input)
gemini "Question"
```

**For more troubleshooting**: Load `references/models-guide.md` for rate limits, large file context issues, and performance tips.

---

## When to Load References

Load reference files in these scenarios:

### Load `references/models-guide.md` when:
- User asks about Flash vs Pro differences
- Models give conflicting recommendations
- Need detailed performance comparison
- Choosing model for specific task type
- Want to understand why models disagree

### Load `references/prompting-strategies.md` when:
- Crafting complex prompts to Gemini
- Need AI-to-AI prompting format template
- Want to improve prompt quality
- Comparing old vs new prompting approaches

### Load `references/gemini-experiments.md` when:
- Need historical context on testing
- Investigating edge cases
- Understanding design decisions
- Troubleshooting unusual behavior

**Note**: `helper-functions.md` is obsolete (references old gemini-coach wrapper, not the official `gemini` CLI).

---

## Production Rules

### 1. Always Use `-p` for Automation
```bash
# ✅ Good for scripts
gemini -p "Question"

# ❌ Bad (interactive)
gemini
```

### 2. Select Model Based on Criticality
```bash
# Architecture/security → Pro
gemini -m gemini-2.5-pro -p "[critical question]"

# Debugging/review → Flash
gemini -m gemini-2.5-flash -p "[general question]"
```

### 3. Provide Context in Prompts
```bash
# ✅ Good: Context + Question + Considerations
gemini -p "Context: Building Cloudflare Worker. Question: Best auth pattern? Considerations: 1) Stateless, 2) JWT, 3) <100ms overhead"

# ❌ Bad: Vague
gemini -p "Best auth?"
```

### 4. Pipe File Content for Reviews
```bash
# ✅ Efficient
cat src/auth.ts | gemini -p "Review for security"

# ❌ Less efficient
gemini -p "Review src/auth.ts"
```

### 5. Synthesize, Don't Just Forward

**❌ BAD**: Just paste Gemini's response
```
Claude: [runs gemini] "Gemini says: [paste]"
```

**✅ GOOD**: Synthesize both perspectives
```
Claude: "I've consulted Gemini for a second opinion:

My analysis: [Claude's perspective]
Gemini's analysis: [Gemini's perspective]
Key differences: [synthesis]
Recommendation: [unified answer]"
```

### 6. Handle Errors Gracefully
```bash
if output=$(gemini -p "Question" 2>&1); then
  echo "Gemini says: $output"
else
  echo "Gemini consultation failed, proceeding with Claude's recommendation"
fi
```

---

## Version History

**2.1.0** (2025-12-15):
- Optimized to <500 lines (Phase 12.5 → 13 condensation)
- Extracted detailed content to references/
- Added "When to Load References" section
- Condensed to top 3 errors, top 3 use cases

**2.0.0** (2025-11-13):
- Complete rewrite for official Gemini CLI (removed gemini-coach wrapper)
- Direct CLI integration patterns
- Updated command examples for `gemini` CLI v0.13.0+

**1.0.0** (2025-11-08):
- Initial release with gemini-coach wrapper

---

## Related Skills

- [google-gemini-api](../google-gemini-api/) - Gemini API integration via SDK
- [google-gemini-embeddings](../google-gemini-embeddings/) - Gemini embeddings for RAG
- [google-gemini-file-search](../google-gemini-file-search/) - Managed RAG with Gemini

---

## License

MIT - See [LICENSE](../../LICENSE)

---

## Support

- **Issues**: https://github.com/jezweb/claude-skills/issues
- **Email**: jeremy@jezweb.net
- **Official Gemini CLI**: https://github.com/google-gemini/gemini-cli
