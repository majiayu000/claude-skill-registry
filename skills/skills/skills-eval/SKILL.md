---
name: skills-eval
description: |

Triggers: quality-assurance, skills, optimization, tool-use, performance-metrics
  Evaluate and improve Claude skill quality through auditing.

  Triggers: skill audit, quality review, compliance check, improvement suggestions,
  token usage analysis, skill evaluation, skill assessment, skill optimization,
  skill standards, skill metrics, skill performance

  Use when: reviewing skill quality, preparing skills for production, auditing
  existing skills, generating improvement recommendations, checking compliance
  with standards, analyzing token efficiency, benchmarking skill performance

  DO NOT use when: creating new skills from scratch - use modular-skills instead.
  DO NOT use when: writing prose for humans - use writing-clearly-and-concisely.
  DO NOT use when: need architectural design patterns - use modular-skills.

  Use this skill BEFORE shipping any skill to production. Check even if unsure.
version: 2.0.0
category: skill-management
tags: [evaluation, improvement, skills, optimization, quality-assurance, tool-use, performance-metrics]
dependencies: [modular-skills, performance-optimization]
tools: [skills-auditor, improvement-suggester, compliance-checker, tool-performance-analyzer, token-usage-tracker]
provides:
  infrastructure: ["evaluation-framework", "quality-assurance", "improvement-planning"]
  patterns: ["skill-analysis", "token-optimization", "modular-design"]
  sdk_features:
    - "agent-sdk-compatibility"
    - "advanced-metrics"
    - "dynamic-discovery"
estimated_tokens: 1800
usage_patterns:
  - skill-audit
  - quality-assessment
  - improvement-planning
  - skills-inventory
  - tool-performance-evaluation
  - dynamic-discovery-optimization
  - advanced-tool-use-analysis
  - programmatic-calling-efficiency
  - context-preservation-quality
  - token-efficiency-optimization
  - modular-architecture-validation
  - integration-testing
  - compliance-reporting
  - performance-benchmarking
complexity: advanced
evaluation_criteria:
  structure_compliance: 25     # Modular architecture, progressive disclosure
  metadata_quality: 20         # Complete frontmatter, clear descriptions
  token_efficiency: 25         # Context optimization, response compression
  tool_integration: 20         # Tool effectiveness, error handling, performance
  claude_sdk_compliance: 10    # API compatibility, best practices adherence
---
## Table of Contents

- [Overview](#overview)
- [Tools](#tools)
- [What It Is](#what-it-is)
- [Quick Start](#quick-start)
- [Basic Skill Audit](#basic-skill-audit)
- [Skill Analysis](#skill-analysis)
- [Generate Improvements](#generate-improvements)
- [Typical Workflow](#typical-workflow)
- [Common Tasks](#common-tasks)
- [Quality Assessment](#quality-assessment)
- [Performance Analysis](#performance-analysis)
- [Standards Compliance](#standards-compliance)
- [Improvements and Optimization](#improvements-and-optimization)
- [Evaluation Framework](#evaluation-framework)
- [Quality Metrics Overview](#quality-metrics-overview)
- [Scoring System](#scoring-system)
- [Priority Levels](#priority-levels)
- [Detailed Resources](#detailed-resources)
- [Shared Modules (Cross-Skill Patterns)](#shared-modules-(cross-skill-patterns))
- [Skill-Specific Modules](#skill-specific-modules)
- [Tools and Automation](#tools-and-automation)


# Skills Evaluation and Improvement

## Overview

Analyze and improve Claude skills. Tools audit skills against quality standards, measure token usage, and generate improvement recommendations.

### Tools

The evaluation process uses `skills-auditor` for structural analysis and `improvement-suggester` for prioritized fixes. `compliance-checker` validates standards, `tool-performance-analyzer` measures tool patterns, and `token-usage-tracker` monitors context efficiency.

## What It Is

Evaluates and improves existing skills by running quality assessments, performance analysis, and generating improvement plans.

## Quick Start

### Basic Skill Audit
```bash
# Run detailed audit of all skills
python scripts/skills_eval/skills_auditor.py --scan-all --format markdown

# Audit specific skill
python scripts/skills_eval/skills_auditor.py --skill-path path/to/skill/SKILL.md

# Or use Makefile:
make audit-skill PATH=path/to/skill/SKILL.md
make audit-all
```

### Skill Analysis
```bash
# Deep analysis of single skill
python scripts/skill_analyzer.py --path path/to/skill/SKILL.md --verbose

# Check token usage
python scripts/token_estimator.py --file path/to/skill/SKILL.md

# Or use Makefile:
make analyze-skill PATH=path/to/skill/SKILL.md
make estimate-tokens PATH=path/to/skill/SKILL.md
```

### Generate Improvements
```bash
# Get prioritized improvement suggestions
python scripts/skills_eval/improvement_suggester.py --skill-path path/to/skill/SKILL.md --priority high

# Check standards compliance
python scripts/skills_eval/compliance_checker.py --skill-path path/to/skill/SKILL.md --standard all

# Or use Makefile:
make improve-skill PATH=path/to/skill/SKILL.md
make check-compliance PATH=path/to/skill/SKILL.md
```

### Typical Workflow
1. **Discovery**: Run `make audit-all` to find and audit all skills
2. **Analysis**: Use `make audit-skill PATH=...` for specific skills
3. **Deep Dive**: Run `make analyze-skill PATH=...` for complexity analysis
4. **Improvements**: Generate plan with `make improve-skill PATH=...`
5. **Compliance**: Verify standards with `make check-compliance PATH=...`
6. **Optimization**: Check tokens with `make estimate-tokens PATH=...`

## Common Tasks

### Quality Assessment
```bash
# Detailed evaluation with scoring
./scripts/skills-auditor --scan-all --format table --priority high

# Detailed analysis of specific skill
./scripts/improvement-suggester --skill-path path/to/skill/SKILL.md --priority all --format markdown
```

### Performance Analysis
```bash
# Token usage and efficiency
./scripts/token-usage-tracker --skill-path path/to/skill/SKILL.md --context-analysis

# Advanced tool performance metrics
./scripts/tool-performance-analyzer --skill-path path/to/skill/SKILL.md --metrics all
```

### Standards Compliance
```bash
# Validate against Claude Skills standards
./scripts/compliance-checker --skill-path path/to/skill/SKILL.md --standard all --format summary

# Auto-fix common issues
./scripts/compliance-checker --skill-path path/to/skill/SKILL.md --auto-fix --severity high
```

### Improvements and Optimization
```bash
# Generate prioritized improvement plan
./scripts/improvement-suggester --skill-path path/to/skill/SKILL.md --priority critical,high

# Benchmark performance
./scripts/token-usage-tracker --skill-path path/to/skill/SKILL.md --benchmark optimization-targets
```

## Evaluation Framework

### Quality Metrics Overview
The framework evaluates skills on weighted dimensions: structure compliance and content quality (20 points each), token efficiency and activation reliability (15 points each), and remaining points for tool integration, trigger isolation, and enforcement language.

### Scoring System
Scores categorize quality: 91-100 (Excellent), 76-90 (Good), 51-75 (Basic), 26-50 (Below Standards), and 0-25 (Critical Issues).

### Priority Levels
Improvements are prioritized to address the most critical issues first. Critical priority is assigned to security vulnerabilities, broken functionality, or missing required metadata. High priority concerns poor structure or incomplete documentation, while medium priority identifies missing best practices and optimization opportunities. Minor enhancements, such as formatting issues or improved examples, are categorized as low priority.

## Detailed Resources

For detailed implementation details and advanced techniques:

### Shared Modules: Cross-Skill Patterns
- **Anti-Rationalization Patterns**: See [anti-rationalization.md](../../shared-modules/anti-rationalization.md) for red flags table and bypass patterns
- **Enforcement Language**: See [enforcement-language.md](../../shared-modules/enforcement-language.md) for tiered intensity templates
- **Trigger Patterns**: See [trigger-patterns.md](../../shared-modules/trigger-patterns.md) for description field structure and CSO

### Skill-Specific Modules
- **Trigger Isolation Analysis**: See `modules/trigger-isolation-analysis.md` for evaluating frontmatter compliance
- **Skill Authoring Best Practices**: See `modules/skill-authoring-best-practices.md` for official Claude guidance
- **Authoring Checklist**: See `modules/authoring-checklist.md` for quick-reference validation checklist
- **Implementation Guide**: See `modules/evaluation-workflows.md` for detailed workflows
- **Quality Metrics**: See `modules/quality-metrics.md` for scoring criteria and evaluation levels
- **Advanced Tool Use Analysis**: See `modules/advanced-tool-use-analysis.md` for specialized evaluation techniques
- **Evaluation Framework**: See `modules/evaluation-framework.md` for detailed scoring and quality gates
- **Integration Patterns**: See `modules/integration.md` for workflow integration with other skills
- **Troubleshooting**: See `modules/troubleshooting.md` for common issues and solutions
- **Pressure Testing**: See `modules/pressure-testing.md` for adversarial validation methodology

### Tools and Automation
- **Tools**: Executable analysis utilities in `scripts/` directory
- **Automation**: Setup and validation scripts in `scripts/automation/`
