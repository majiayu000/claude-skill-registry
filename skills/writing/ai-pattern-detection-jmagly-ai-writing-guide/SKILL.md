---
name: ai-pattern-detection
description: Detects AI-generated writing patterns and suggests authentic alternatives. Auto-applies when reviewing content, editing documents, generating text, or when user mentions writing quality, AI detection, authenticity, or natural voice.
version: 1.0.0
---

# AI Pattern Detection Skill

## Purpose

Automatically scan content for AI-generated writing patterns and provide authentic alternatives. This skill activates when Claude generates or reviews text content, ensuring outputs maintain human-like authenticity.

## When This Skill Applies

- Generating any prose, documentation, or written content
- Reviewing or editing existing documents
- User mentions "AI detection", "writing quality", "authentic voice"
- User asks to "make it sound more natural" or "less robotic"
- Creating marketing copy, documentation, or communications

## Detection Categories

### Critical Patterns (Always Flag)

These immediately identify content as AI-generated:

1. **Corporate Buzzwords**: "seamlessly integrates", "cutting-edge", "revolutionary", "next-generation", "comprehensive solution"
2. **Vague Intensifiers**: "dramatically improves", "significantly enhances", "vastly superior"
3. **Formulaic Transitions**: "Moreover,", "Furthermore,", "Additionally,", "In conclusion,"
4. **Performative Language**: "aims to provide", "strives to achieve", "designed to enhance"
5. **Academic Passive**: "It has been observed that...", "It can be argued that..."

### Structural Patterns (Flag When Overused)

1. **Three-item lists**: "reliable, scalable, and secure"
2. **Em-dash overuse**: Multiple em-dashes in a paragraph
3. **Identical paragraph structure**: Topic → 3 points → conclusion repeated
4. **Balanced hedging**: "While X has challenges, it also offers opportunities"

### Contextual Patterns (Check Frequency)

Words acceptable at 1:1000 ratio but problematic at 1:100:
- manifest, revolutionary, next-generation
- robust, scalable, comprehensive
- synergy, leverage, utilize

## Replacement Guidelines

| Instead of | Use |
|-----------|-----|
| "plays a crucial role" | "handles" / "manages" / "does" |
| "seamlessly integrates" | "works with" / "connects to" |
| "cutting-edge" | "new" / "recent" / specific tech name |
| "Moreover," | [just start the next sentence] |
| "comprehensive solution" | [specific description of what it does] |
| "dramatically improves" | [specific metric: "reduces latency by 40%"] |
| "robust" | "handles X requests/second" / "99.9% uptime" |

## Authenticity Markers to Include

Strong authentic content includes:

1. **Specific opinions**: "I prefer X because..." not "X is preferred"
2. **Acknowledged trade-offs**: "This approach sacrifices Y for Z"
3. **Real-world constraints**: "Budget limited us to..."
4. **Uncertainty where appropriate**: "We're not sure yet whether..."
5. **Varied sentence structure**: Mix short and long, different openings
6. **Domain-specific vocabulary**: Use actual technical terms, not generic descriptions

## Application Process

When generating or reviewing content:

1. **Scan** for critical banned patterns
2. **Count** contextual pattern frequency
3. **Check** structural variety
4. **Suggest** specific replacements
5. **Verify** authenticity markers present

## Examples

### Before (AI-Detected)
> The platform seamlessly integrates cutting-edge technology to dramatically improve workflow efficiency. Moreover, it plays a crucial role in enabling next-generation solutions. In conclusion, this comprehensive approach transforms how teams collaborate.

### After (Authentic)
> The platform connects to existing tools through standard APIs. Initial tests show 40% faster task completion. Teams report fewer context switches between applications.

## Script Reference

For automated scanning, use `scripts/pattern_scanner.py` which:
- Counts pattern frequencies
- Flags critical violations
- Generates replacement suggestions
- Produces authenticity score (0-100)

## Integration

This skill works with:
- `/writing-validator` command for explicit validation
- `writing-validator` agent for deep analysis
- Any content generation task automatically
