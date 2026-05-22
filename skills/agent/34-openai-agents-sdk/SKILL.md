---
sidebar_position: 0
title: "Build Your OpenAI Agents Skill"
description: "Create your OpenAI Agents SDK skill in one prompt, then learn to improve it throughout the chapter"
chapter: 34
lesson: 0
duration_minutes: 15

skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working OpenAI Agents skill using natural language"

learning_objectives:
  - objective: "Build an OpenAI Agents skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working openai-agents skill in .claude/skills/"

cognitive_load:
  new_concepts: 1
  assessment: "Single concept: use Claude to build a skill from official docs"

differentiation:
  extension_for_advanced: "Add multi-agent handoff patterns during creation"
  remedial_for_struggling: "Follow exact prompt provided"
---

# Build Your OpenAI Agents Skill

Before learning OpenAI's Agents SDK, you'll **own** an OpenAI Agents skill.

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
Using your skill creator skill create a new skill for OpenAI Agents SDK.
I will use it to build AI agents from hello world to professional production
systems. Use context7 skill to study official documentation and then build
it so no self assumed knowledge.
```

Claude will:
1. Fetch official OpenAI Agents SDK documentation via Context7
2. Ask you clarifying questions (tool patterns, handoff needs, guardrails)
3. Create the complete skill with references and templates

Your skill appears at `.claude/skills/openai-agents/`.

---

## Done

You now own an OpenAI Agents skill built from official documentation. The rest of this chapter teaches you what it knows—and how to make it better.

**Next: Lesson 1 — Agent Fundamentals**
