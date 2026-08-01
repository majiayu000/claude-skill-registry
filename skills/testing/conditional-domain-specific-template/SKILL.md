---
name: conditional-domain-specific-template
description: '[REPLACE] Apply domain-specific logic based on detected context. Use
  when [REPLACE with specific triggers].'
---

---
name: conditional-domain-specific-template
description: [REPLACE] Apply domain-specific logic based on detected context. Use when [REPLACE with specific triggers].
allowed-tools: Read, TodoWrite
---

# Conditional Domain-Specific Template

## Purpose

This template demonstrates context-aware workflows that adapt based on domain, technology, or data characteristics.

**Use this template when:**

- Behavior varies by framework/language/domain
- Different rule sets apply to different contexts
- Progressive disclosure by detected context
- Multiple technology stacks supported

## Workflow

### Phase 1: Detect Context

<detect-context>
1. Analyze input to determine domain
2. Identify relevant technology stack
3. Load domain-specific rules
4. Select appropriate processing path
</detect-context>

### Phase 2: Load Domain Rules

<load-rules>
Based on detected context:
- Financial: @references/financial-analysis.md
- Scientific: @references/scientific-calculations.md
- Business: @references/business-metrics.md
</load-rules>

### Phase 3: Apply Domain Logic

<apply-logic>
1. Use domain-specific formulas
2. Apply domain conventions
3. Validate against domain constraints
4. Format output per domain standards
</apply-logic>

## Context Detection

**Financial Data:**

- Keywords: revenue, profit, QoQ, YoY, EBITDA
- Date ranges with quarterly/annual patterns
- Currency symbols and financial notation

**Scientific Data:**

- Keywords: mean, median, standard deviation, p-value
- Statistical notation
- Hypothesis testing language

**Business Metrics:**

- Keywords: KPI, conversion, retention, churn
- Percentage-based metrics
- Funnel analysis patterns

## Progressive Disclosure

**Core workflow (this file):**

- Context detection logic
- Domain routing rules
- High-level processing flow

**Domain-specific details (references/):**

- references/financial-analysis.md - Financial calculations and formulas
- references/scientific-calculations.md - Statistical methods
- references/business-metrics.md - KPI calculations

## Example Usage

```xml
<detect-context>
Detected: Financial data (contains "revenue", "QoQ", quarterly dates)
Domain: Financial Analysis
Loading: /references/financial-analysis.md
</detect-context>

<apply-logic>
Calculating QoQ revenue growth:
Q4 2024: $1.2M → Q1 2025: $1.5M
QoQ Growth: +25.0%

YoY revenue comparison:
Q1 2024: $0.9M → Q1 2025: $1.5M
YoY Growth: +66.7%

Forecast Q2 2025: $1.7M (based on trend)
</apply-logic>
```
