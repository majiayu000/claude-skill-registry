---
sidebar_position: 0
title: "Build Your ChatKit Skill"
description: "Create your ChatKit Server skill in one prompt, then learn to improve it throughout the chapter"
chapter: 41
lesson: 0
duration_minutes: 15

skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working ChatKit skill using natural language"

learning_objectives:
  - objective: "Build a ChatKit skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working chatkit-server skill in .claude/skills/"

cognitive_load:
  new_concepts: 1
  assessment: "Single concept: use Claude to build a skill from official docs"

differentiation:
  extension_for_advanced: "Add session persistence patterns during creation"
  remedial_for_struggling: "Follow exact prompt provided"
---

# Build Your ChatKit Skill

You built REST APIs in Chapter 40. But agents are conversational, not request/response. Before learning ChatKit Server, you'll **own** a ChatKit skill.

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
Using your skill creator skill create a new skill for ChatKit Server. I will
use it to build conversational AI backends from hello world to professional
production systems. Use context7 skill to study official documentation and
then build it so no self assumed knowledge.
```

Claude will:
1. Fetch official ChatKit documentation via Context7
2. Ask you clarifying questions (session management, streaming needs, auth patterns)
3. Create the complete skill with references and templates

Your skill appears at `.claude/skills/chatkit-server/`.

---

## Done

You now own a ChatKit skill built from official documentation. The rest of this chapter teaches you what it knows—and how to make it better.

**Next: Lesson 1 — ChatKit Architecture**
