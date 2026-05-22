---
name: document-business-rule
description: Generate business rule documentation from domain knowledge and requirements. Use when documenting complex business logic.
allowed-tools: Write, Read, Glob, Grep
disable-model-invocation: true
---

# Business Rule Documentation Generator

Generate structured documentation for business logic and domain knowledge.

## User Request

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## What This Command Does

1. Interpret user's natural language request to understand documentation needs
2. Research existing codebase for related implementations
3. Generate structured business rule documentation
4. Save to appropriate location based on project structure

## Input Interpretation

Analyze the user's natural language input to intelligently extract:

- **Domain/Topic**: What business area needs documentation
- **Context**: Background information, related systems, stakeholders
- **Scope**: Specific aspects, rules, or processes to focus on
- **Output preferences**: File location, format preferences if mentioned

**Interpretation Guidelines:**

- Accept any natural language description - no strict format required
- Infer domain name from context if not explicitly stated
- Ask clarifying questions only when truly ambiguous
- If input is empty, ask user to describe what they want to document

## Documentation Structure

### Basic Principles

- **Concise and clear**: Avoid verbose explanations
- **With actionable examples**: Include code references
- **Focus on the "why"**: Explain reasoning behind rules

### Generated Document Template

````markdown
# [Domain Name]

## Overview

The business area covered by this domain (1-2 sentences)

## Core Concepts

### [Concept Name]

**Definition:** Clear definition

**Example:**

```typescript
// Actual usage example code
```
````

**Code Location:** `src/domain/concept.ts`

## Business Rules

### [Rule Name]

- **Content:** Rule description
- **Reason:** Why this rule is necessary
- **Exceptions (if any):** Exception scenarios
- **Code Location:** `src/domain/rules.ts:45-67`

## Process Flow (Complex cases only)

### [Process Name]

1. Step 1 → `src/service/step1.ts`
2. Step 2 → `src/service/step2.ts`
3. Step 3 → `src/service/step3.ts`

## Cautions (if any)

- Common mistake areas
- Things to watch for when making changes

## Glossary (if needed)

- **Term 1:** Definition
- **Term 2:** Definition

```

## Output Location

Determine appropriate location:

```

project-root/
├── docs/
│ └── domain/ # Primary location for domain docs
│ └── {domain-name}.md
└── src/
└── {module}/
└── README.md # Alternative: module-specific docs

````

**Decision logic:**
- If `docs/domain/` exists → use `docs/domain/{domain-name}.md`
- If documenting specific module → use module's `README.md`
- Ask user if unclear

## Execution Steps

1. **Parse Input**: Extract domain info from `$ARGUMENTS`
2. **Research Codebase**:
   - Search for related files: `Glob src/**/*{domain}*`
   - Find existing documentation: `Glob docs/**/*.md`
   - Check for related code patterns: `Grep {domain keywords}`
3. **Generate Document**: Create documentation following template
4. **Write File**: Save to determined location
5. **Report**: Show created file path and summary

## Usage Examples

```bash
# Simple domain name
/document-business-rule user-authentication

# Natural language description
/document-business-rule 주문 처리 로직 문서화해줘. 결제 검증이랑 재고 확인 규칙 포함해서

# Conversational style
/document-business-rule 우리 billing 모듈에 있는 구독 관련 비즈니스 규칙들 정리해줘

# Detailed context
/document-business-rule We need to document the refund policy rules. Customer can request refund within 7 days, partial refunds allowed for digital goods
```

## Important Notes

- This command generates documentation based on user input and codebase analysis
- Review generated content for accuracy before committing
- Update documentation when business rules change
- Keep documentation close to related code
- Use code references (`file:line`) for traceability
````
