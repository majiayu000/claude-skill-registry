---
name: brainstorming
description: Structured design facilitation for new features, algorithms, or architecture decisions. Use before any significant implementation work, when exploring trade-offs, or when the user has a vague idea that needs to be refined into a concrete plan.
---

# Brainstorming Ideas Into Designs

## Purpose

Turn raw ideas into **clear, validated designs** through structured dialogue **before any implementation begins**. Prevent premature coding, hidden assumptions, and misaligned solutions.

**You must NOT implement, code, or modify files while this skill is active.**

## Process

### 1. Understand Current Context

Before asking questions:
- Review the current project state (files, docs, prior decisions)
- Identify what already exists vs. what is proposed
- Note implicit constraints

### 2. Clarify the Idea (One Question at a Time)

- Ask **one question per message**
- Prefer **multiple-choice questions** when possible
- Focus on: purpose, constraints, success criteria, and explicit non-goals
- For algorithms/math: clarify accuracy requirements, edge cases, expected inputs

### 3. Technical Requirements

Explicitly clarify or propose assumptions for:
- **Performance**: allocation budget, runtime targets, real-time constraints
- **Accuracy**: numerical precision, validation references (papers, test cases)
- **Differentiability**: which AD backends must work, what needs to be differentiable
- **Composability**: how it integrates with existing types and interfaces
- **Scope**: what is explicitly out of scope

If the user is unsure, propose reasonable defaults and mark them as **assumptions**.

### 4. Understanding Lock (Hard Gate)

Before proposing any design, provide a summary covering:
- What is being built and why
- Key constraints and non-goals
- All assumptions listed explicitly

Ask: *"Does this accurately reflect your intent? Confirm or correct before we move to design."*

**Do NOT proceed until confirmed.**

### 5. Explore Approaches

- Propose **2-3 viable approaches** with trade-offs
- Lead with recommended option
- Compare on: complexity, performance, extensibility, AD compatibility, maintenance
- Apply YAGNI -- avoid speculative features

### 6. Present the Design Incrementally

- Break into sections of 200-300 words max
- After each section ask: *"Does this look right so far?"*
- Cover as relevant: type hierarchy, API surface, data flow, error handling, edge cases, testing strategy

### 7. Decision Log

Maintain a running log: what was decided, alternatives considered, and why.

## After the Design

Once validated:
- Write the final design to a Markdown document
- Include: summary, assumptions, decision log, final design
- Only then ask: *"Ready to proceed to implementation?"*

## Exit Criteria

All must be true before exiting brainstorming:
- Understanding lock confirmed
- At least one approach explicitly accepted
- Assumptions documented
- Key risks acknowledged
- Decision log complete
