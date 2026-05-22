---
sidebar_position: 0
title: "Build Your Data Engineering Skill"
description: "Create your LLMOps data engineering skill in one prompt, then learn to improve it throughout the chapter"
chapter: 63
lesson: 0
duration_minutes: 25

# HIDDEN SKILLS METADATA
skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working llmops-data-engineer skill using natural language and official documentation"

  - name: "Documentation-Grounded Skill Creation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student uses Context7/DeepWiki to ground skill in authoritative sources rather than AI memory"

learning_objectives:
  - objective: "Build a data engineering skill using natural conversation with Claude, grounded in official documentation"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working llmops-data-engineer skill in .claude/skills/"

  - objective: "Write a LEARNING-SPEC.md that articulates what the skill should achieve before creation"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "LEARNING-SPEC.md contains clear success criteria, constraints, and expected capabilities"

cognitive_load:
  new_concepts: 2
  assessment: "Two concepts: (1) writing a LEARNING-SPEC before skill creation, (2) using documentation fetching to ground skills. Well within B1 limit of 7-10 concepts."

differentiation:
  extension_for_advanced: "Add Hugging Face datasets library patterns during skill creation"
  remedial_for_struggling: "Follow exact prompts provided, skip LEARNING-SPEC customization"
---

# Build Your Data Engineering Skill

Before learning data engineering for fine-tuning—preparing training datasets that transform generic models into domain specialists—you'll **own** a data engineering skill.

This isn't downloading someone else's notes. You're building expertise from official documentation, creating a reusable asset that will guide you through the entire chapter and beyond.

---

## Why Skill-First?

Traditional learning: Read about data engineering, then maybe create a skill later.

**Skill-First learning**: Create your skill NOW, then use the chapter to test and improve it.

The difference matters because:

1. **You learn faster** when you have a knowledge base to consult
2. **You retain more** when you actively improve what you've built
3. **You own an asset** at the end—not just knowledge, but reusable intelligence

By Part 8, you've seen this pattern repeatedly. This chapter is no different: create the skill first, then battle-test it through real data engineering work.

---

## Step 1: Get a Fresh Skills Lab

Start clean. Don't reuse old state—clone fresh:

1. Go to [github.com/panaversity/claude-code-skills-lab](https://github.com/panaversity/claude-code-skills-lab)
2. Click the green **Code** button
3. Select **Download ZIP** (or `git clone` if you prefer)
4. Extract the ZIP file to a new location
5. Open the extracted folder in your terminal

```bash
cd claude-code-skills-lab
claude
```

**Why clone fresh?** State from previous chapters can interfere. A clean skills-lab means your skill starts from verified documentation, not cached assumptions.

---

## Step 2: Write Your LEARNING-SPEC

Before asking Claude to create your skill, articulate what you need. Create a file called `LEARNING-SPEC.md`:

```markdown
# LEARNING-SPEC: LLMOps Data Engineering Skill

## What I'm Building
A skill that helps me create high-quality training datasets for fine-tuning LLMs.

## Why I Need It
I want to fine-tune models on domain-specific tasks (like Task API operations) but need to understand:
- How to structure training data (formats like Alpaca, ShareGPT, ChatML)
- How to ensure data quality (accuracy, consistency, coverage, diversity)
- How to generate synthetic data cost-effectively (GPT-4o-mini, under $0.15)
- How to clean and validate datasets before training

## Success Criteria
My skill should be able to:
1. Explain when to use Alpaca vs ShareGPT vs ChatML format
2. Guide me through creating JSONL datasets with Pydantic validation
3. Help me generate synthetic training examples
4. Implement quality filtering (deduplication, LLM-as-Judge scoring)
5. Prepare train/validation/test splits correctly

## Constraints
- Must work within Colab Free Tier (T4 GPU, 15GB VRAM)
- Synthetic data generation costs must stay under $0.15 for 500 examples
- Should use Unsloth and Hugging Face, not vendor-locked platforms

## What I Already Know
- Python fundamentals (Part 5)
- Pydantic for data validation
- OpenAI API basics for generation
```

Save this file. It becomes your specification for what the skill should achieve.

---

## Step 3: Create Your Skill

Now ask Claude to create the skill, grounded in official documentation:

```
I want to create an llmops-data-engineer skill for preparing training datasets.

First, read my LEARNING-SPEC.md to understand what I need.

Then use Context7 to fetch documentation from:
1. Hugging Face datasets library
2. Unsloth fine-tuning documentation
3. OpenAI fine-tuning data format guide

Finally, create the skill using the skill-creator skill.
Ground everything in the official docs, not assumed knowledge.
```

Claude will:
1. Read your LEARNING-SPEC.md
2. Fetch authoritative documentation via Context7
3. Ask clarifying questions if needed
4. Create the complete skill with references, templates, and examples

Your skill appears at `.claude/skills/llmops-data-engineer/`.

---

## Step 4: Verify Your Skill Exists

Check that the skill was created correctly:

```bash
ls -la .claude/skills/llmops-data-engineer/
cat .claude/skills/llmops-data-engineer/SKILL.md
```

You should see a SKILL.md file with:
- A clear description of when to use the skill
- References to official documentation sources
- Practical guidance for dataset creation
- Examples of common formats

---

## What You've Built

You now own an `llmops-data-engineer` skill built from:

| Source | What It Contributes |
|--------|---------------------|
| **Hugging Face docs** | Dataset formats, loading patterns, Hub integration |
| **Unsloth docs** | Training data requirements, efficiency patterns |
| **OpenAI fine-tuning guide** | Instruction format, conversation structure |
| **Your LEARNING-SPEC** | Your specific constraints and success criteria |

This skill isn't generic AI knowledge. It's grounded in authoritative sources and tailored to your needs.

---

## The Rest of This Chapter

Lessons 1-4 teach you what your skill already knows—but through hands-on practice that reveals nuances:

| Lesson | What You Learn | How Your Skill Improves |
|--------|----------------|-------------------------|
| L01: Data Quality Principles | Garbage-in-garbage-out realities | Add quality dimension checklist |
| L02: Instruction Formats | Alpaca vs ShareGPT vs ChatML | Test: can it recommend the right format? |
| L03: Synthetic Data Generation | GPT-4o-mini cost-effective patterns | Add generation templates |
| L04: Data Cleaning | Deduplication, validation, filtering | Add cleaning pipeline guidance |

By the chapter's end, your skill is battle-tested and production-ready.

---

## Try With AI

### Prompt 1: Test Your Skill Immediately

```
I want to create a training dataset for a Task API assistant.
The assistant should help users create, update, and complete tasks.

Using my llmops-data-engineer skill, help me decide:
1. Should I use Alpaca or ShareGPT format?
2. How many examples do I need for effective fine-tuning?
3. What quality dimensions should I check?
```

**What you're learning**: Whether your skill can give useful guidance right now. If it can't answer these questions well, you'll know exactly what to improve as you work through the chapter.

### Prompt 2: Identify Skill Gaps

```
Look at my llmops-data-engineer skill and compare it to what we'll learn in this chapter:
- Data quality principles
- Instruction formats (Alpaca, ShareGPT, ChatML)
- Synthetic data generation with GPT-4o-mini
- Data cleaning and validation

What's missing from my skill that the chapter will teach?
Create a checklist of improvements I should make as I learn.
```

**What you're learning**: Self-assessment through AI dialogue. Your skill has gaps—that's expected. Identifying them upfront makes the chapter more purposeful.

### Prompt 3: Connect to Your Domain

```
I work in [your domain: healthcare/legal/finance/education/other].

Help me think about what training data I would need to fine-tune a model
for my specific use case. Ask me questions about:
- What tasks do I need the model to perform?
- What knowledge does it need that base models lack?
- Where would I get training examples?
```

**What you're learning**: Pattern transfer—applying data engineering concepts to your actual work. The Task API example teaches the mechanics; your domain is where the value lies.

### Safety Note

Your skill is created from AI interpretation of documentation. It may have gaps or inaccuracies. The chapter exists to surface these gaps through practice. Don't trust the skill blindly—verify its guidance against your own understanding as you learn.
