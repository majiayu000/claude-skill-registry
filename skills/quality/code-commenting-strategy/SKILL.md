---
name: code-commenting-strategy
description: Apply strategic approaches to code commenting including when to comment, optimal comment density, performance considerations, and integration with development workflow. Use when establishing commenting standards, addressing performance concerns, implementing Pseudocode Programming Process (PPP), or determining appropriate comment frequency.
---

# Code Commenting Strategy

## When to Use This Skill
- Establishing or updating code commenting standards for a project
- Addressing concerns about comment performance impact
- Implementing Pseudocode Programming Process (PPP)
- Determining optimal comment density for codebases
- Training developers on commenting best practices

## Core Principles

### 1. Integrate Comments with Development Workflow

**Write comments synchronously with code, not as a separate task.**

**Why delay comments?**
- **Perceived workload**: Commenting at the end becomes a separate, overwhelming task
- **Time cost**: Requires recalling or re-understanding code logic
- **Accuracy loss**: Design assumptions and nuances are forgotten

**Handling the "interruption" objection:**
- If commenting interrupts your coding flow, this is a warning sign of complexity
- Use pseudocode for design first
- Convert pseudocode to comments
- Fill in the code implementation
- High concentration needs indicate overly complex design—simplify first

### 2. Performance Considerations

**For interpreted languages and resource-constrained environments:**
- Comments can add measurable performance overhead
- **Never skip comments to improve performance**
- Create separate build/release versions
- Use build tools to strip comments during the build process

**For compiled languages:**
- Comments are typically stripped automatically during compilation
- No performance impact concern

### 3. Optimal Comment Density

**Research-based guideline:**
- IBM research shows clarity peaks at approximately **1 comment per 10 statements**
- **Below this density**: Code becomes difficult to understand
- **Above this density**: Also reduces code comprehensibility

**Avoid arbitrary standards:**
- Don't use mandatory rules like "1 comment per 5 lines"
- Arbitrary standards address symptoms, not root causes
- Focus on code clarity, not comment quotas

### 4. Pseudocode Programming Process (PPP) Integration

When using PPP effectively:
- You may naturally achieve high comment density (every few lines)
- This is a **side effect**, not a goal
- **Focus on efficiency**, not quantity

**Evaluate each comment:**
- Does it describe **why** the code was written?
- Does it meet established quality standards?
- If yes, you have sufficient comments

## Decision Flow

```
IF writing code
    THEN write comments synchronously
    IF concentration is too high for commenting
        THEN simplify design using pseudocode first

IF concerned about comment performance
    IF compiled language
        THEN no action needed (auto-stripped)
    IF interpreted language
        THEN implement build-time comment stripping

IF evaluating comment density
    THEN aim for ~1 comment per 10 statements
    Avoid arbitrary minimum quotas

IF using PPP
    THEN focus on comment efficiency (describing "why")
    Not on achieving specific quantity
```

## Warning Signs
- Coding requires such extreme concentration that commenting feels disruptive
- Comment density significantly deviates from 1:10 ratio without justification
- Comments are treated as a separate "cleanup" phase
- Performance concerns lead to reduced commenting