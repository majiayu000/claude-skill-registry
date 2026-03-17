---
name: ai-consultation
description: Provides AI consultation workflows, prompt templates, and best practices for multi-model consultation. Use when user asks for "second opinion", "ask codex", "ask gemini", "AI code review", "external AI consultation", or needs prompt templates for code review, security audit, or architecture analysis.
allowed-tools: Read, Bash
---

# AI Consultation Skill

Methodology and templates for effective AI consultation workflows with external AI tools like Codex and Gemini.

## When to Use

- Getting second opinions from Codex or Gemini CLI
- Code review consultations
- Architecture decision validation
- Security audits with multiple AI perspectives
- Debugging with alternative diagnostic approaches
- Performance reviews needing fresh insights

## Consultation Types

1. **Code Review / Quality Check** - Focus on quality, security, performance, best practices
2. **Architecture / Design Opinion** - Focus on structure, patterns, scalability, tradeoffs
3. **Debugging / Root Cause Analysis** - Focus on finding causes, suggesting diagnostics
4. **Security Audit** - Focus on vulnerabilities, OWASP, auth, data exposure
5. **Performance Review** - Focus on bottlenecks, algorithms, optimization opportunities

## Key Principles

### Safety First
- Always use sandbox/read-only mode for consultations
- External AI tools should not modify files
- Get user confirmation before any write operations

### Critical Thinking
- Never accept AI suggestions blindly
- Compare external AI perspective with your own analysis
- Validate recommendations before presenting
- Acknowledge when uncertain

### Effective Prompts
- Be specific about files and components to analyze
- Provide relevant context and constraints
- Specify desired output format (line numbers, severity ratings)
- Request prioritization by impact or severity

## Resources

See the reference documents for detailed guidance:

- `references/prompt-templates.md` - Ready-to-use prompt templates for all consultation types
- `references/examples.md` - 12 concrete consultation examples with workflows
- `references/decision-tree.md` - Comprehensive decision logic for choosing consultation types
- `references/consultation-checklist.md` - Quality assurance checklist for consultations
- `references/cli-options.md` - AI CLI options reference for Gemini and other tools

## Quick Start

### Basic Consultation Flow

1. **Identify consultation type** - What does the user need?
2. **Prepare the prompt** - Use templates, be specific
3. **Execute safely** - Always read-only/sandbox mode
4. **Evaluate critically** - Don't accept blindly
5. **Synthesize perspectives** - Combine AI insights with your own
6. **Present clearly** - Prioritize findings, provide action items

### Example Prompt Structure

```
[ACTION VERB] [COMPONENT] for [PURPOSE].

Focus on:
- [ASPECT 1]
- [ASPECT 2]
- [ASPECT 3]

For each finding:
- Provide line numbers
- Rate severity (Critical/High/Medium/Low)
- Suggest remediation steps
```

## Output Format

When presenting consultation results:

### Executive Summary
Brief overview of key findings (2-3 sentences)

### AI's Findings
Organized by priority:
- Critical issues
- High priority
- Medium priority
- Low priority

### Your Analysis
Where you agree/disagree, additional insights

### Synthesis & Recommendations
Combined recommendations with actionable next steps
