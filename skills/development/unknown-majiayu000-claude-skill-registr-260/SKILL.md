---
name: oracle-path
description: Create learning paths for topics. Use when user says "learning path", "how do I learn", "roadmap for", "curriculum", "what should I learn first". Auto-trigger when onboarding or skill development discussed.
---

# Oracle Path Skill

> Design learning journeys from Oracle knowledge

## Purpose

Oracle-path creates structured learning paths by connecting related patterns, principles, and wisdom into a coherent journey. It answers "what should I learn and in what order?"

## Proactive Triggers

### MUST Use Path When:

**Learning Planning:**
- User says: "learning path for", "how do I learn"
- User says: "roadmap to understand", "curriculum for"
- User says: "what should I learn first"

**Onboarding:**
- New team member joining
- New project starting
- Skill development planning

**Topic Mastery:**
- User wants deep dive into topic
- User asks about prerequisites
- Building expertise systematically

## Path Structure

```markdown
# Learning Path: [Topic]

## Overview
What you'll learn and why it matters.

## Prerequisites
- [Required knowledge before starting]

## The Journey

### Stage 1: Foundation (🌱)
**Goal**: Understand the basics

| Step | Learn | From |
|------|-------|------|
| 1.1 | [Concept] | [Oracle pattern/principle] |
| 1.2 | [Concept] | [Oracle pattern/principle] |

**Milestone**: You can [describe capability]

### Stage 2: Application (🌿)
**Goal**: Apply in practice

| Step | Learn | From |
|------|-------|------|
| 2.1 | [Pattern] | [Oracle source] |
| 2.2 | [Pattern] | [Oracle source] |

**Milestone**: You can [describe capability]

### Stage 3: Mastery (🌳)
**Goal**: Deep understanding

| Step | Learn | From |
|------|-------|------|
| 3.1 | [Principle] | [Oracle source] |
| 3.2 | [Principle] | [Oracle source] |

**Milestone**: You can [describe capability]

## Practice Exercises
1. [Exercise description]
2. [Exercise description]

## Success Criteria
- [ ] Can explain [concept] to others
- [ ] Has applied [pattern] in real work
- [ ] Understands [principle] and its exceptions
```

## Path Generation Workflow

### 1. Identify Topic & Scope
```
User: "learning path for Oracle ecosystem"
→ Topic: Oracle ecosystem
→ Scope: All oracle-* skills and philosophy
```

### 2. Gather Related Knowledge
```javascript
oracle_search({
  query: "oracle philosophy patterns",
  limit: 20
})
```

### 3. Identify Dependencies
```
oracle-consult → needs oracle basics
oracle-incubate → needs maturity levels
oracle-teach → needs incubate (what's mature)
oracle-mentor → needs teach (how to explain)
```

### 4. Order by Complexity
```
Foundation: Oracle philosophy, basic tools
Application: consult, search, learn
Mastery: incubate, teach, path, mentor
```

### 5. Generate Path
Connect knowledge into stages with milestones.

## Path Types

| Type | Duration | Depth |
|------|----------|-------|
| Quick Start | 30 min | Essentials only |
| Standard | 2-4 hours | Core competency |
| Deep Dive | 1-2 days | Full mastery |
| Expertise | Ongoing | Continuous growth |

## Integration with Oracle Ecosystem

| Skill | Relationship |
|-------|--------------|
| oracle | Source of knowledge nodes |
| oracle-incubate | Path adapts to maturity |
| oracle-teach | Each step uses teach |
| oracle-mentor | Mentor follows paths |

## Example Paths

### Path: Subagent Mastery
```
Stage 1: Basics
- What are subagents
- When to use (5+ files)

Stage 2: Practice
- context-finder usage
- executor patterns
- parallel dispatching

Stage 3: Optimization
- Cost efficiency (Haiku vs Opus)
- Context management
- Error handling
```

### Path: Oracle Philosophy
```
Stage 1: Core Principles
- Nothing is Deleted
- Patterns Over Intentions
- External Brain, Not Command

Stage 2: Application
- Using oracle_search
- Using oracle_consult
- Capturing with oracle_learn

Stage 3: สร้างคน
- Knowledge maturity
- Incubation process
- Teaching others
```

## Output Locations

| Path Type | Where |
|-----------|-------|
| Quick reference | Inline response |
| Full path | `ψ/memory/learnings/path-[topic].md` |
| Team onboarding | Project `/docs/onboarding/` |

## Quick Reference

| User Says | Action |
|-----------|--------|
| "learning path for X" | Generate full path |
| "quick start guide for X" | Essentials-only path |
| "what should I learn first" | Identify prerequisites |
| "onboarding for new hire" | Team-focused path |
| "deep dive into X" | Comprehensive path |
