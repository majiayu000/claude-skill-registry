---
sidebar_position: 0
title: "Build Your Testing Skill"
description: "Create your agent-tdd skill in one prompt, then learn to improve it throughout the chapter"
keywords: [pytest, testing, tdd, agent testing, skill-first learning]
chapter: 46
lesson: 0
duration_minutes: 15

skills:
  - name: "Skill-First Learning Pattern"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working agent-tdd skill using natural language"

learning_objectives:
  - objective: "Build an agent-tdd skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working agent-tdd skill in .claude/skills/"

cognitive_load:
  new_concepts: 1
  assessment: "Single concept: use Claude to build a skill from official docs"

differentiation:
  extension_for_advanced: "Add pytest-mockllm patterns during skill creation"
  remedial_for_struggling: "Follow exact prompt provided"
---

# Build Your Testing Skill

Before learning how to test AI agents, you'll **own** a testing skill.

This chapter teaches TDD (Test-Driven Development) for agent code—the deterministic tests that verify your code works correctly, runs fast, and costs nothing. By the end, you'll have a comprehensive test suite for your Task API with 80%+ coverage and zero LLM API calls during testing.

But you won't learn testing patterns and then maybe build a skill later. You'll build the skill **first**, then spend the chapter improving it with every lesson.

---

## Step 1: Get the Skills Lab

1. Go to [github.com/panaversity/claude-code-skills-lab](https://github.com/panaversity/claude-code-skills-lab)
2. Click the green **Code** button
3. Select **Download ZIP**
4. Extract the ZIP file
5. Open the extracted folder in your terminal

```bash
cd claude-code-skills-lab
claude
```

---

## Step 2: Create Your Skill

Copy and paste this prompt:

```
Using your skill creator skill create a new skill for testing AI agent code
with pytest. I will use it to test FastAPI endpoints, mock LLM calls, and
test agent pipelines from hello world to production test suites.
Use context7 skill to study official pytest-asyncio and respx documentation
and then build it so no self assumed knowledge.
```

Claude will:
1. Fetch official pytest-asyncio and respx documentation via Context7
2. Ask you clarifying questions (testing patterns, async preferences, coverage goals)
3. Create the complete skill with fixtures, mocking patterns, and templates

Your skill appears at `.claude/skills/agent-tdd/`.

---

## Done

You now own an `agent-tdd` skill built from official documentation. The rest of this chapter teaches you what it knows—and how to make it better.

Every lesson ends with a "Reflect on Your Skill" section where you'll test your skill, identify gaps, and improve it. By the capstone, your skill will generate complete test suites from specifications.

**Next: Lesson 1 — TDD Philosophy for Agents**
