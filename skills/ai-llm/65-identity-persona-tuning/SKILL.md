---
sidebar_position: 0
title: "Build Your Persona Tuning Skill"
chapter: 65
lesson: 0
duration_minutes: 25

# HIDDEN SKILLS METADATA
skills:
  - name: "Creating Reusable LLMOps Skills"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can create a persona-tuning skill from documentation using the Skill-First pattern with LEARNING-SPEC.md"

  - name: "Persona Tuning Skill Foundation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Content Creation"
    measurable_at_this_level: "Student can initialize a skills-lab project and define learning specifications for persona fine-tuning"

  - name: "Documentation-Grounded Skill Building"
    proficiency_level: "B2"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Student can fetch and synthesize official documentation to create verified, production-ready skills"

learning_objectives:
  - objective: "Create a persona-tuning skill from official documentation"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill file created with correct YAML frontmatter and persona tuning patterns"

  - objective: "Define learning specifications before studying content"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "LEARNING-SPEC.md file exists with clear objectives, success criteria, and constraints"

  - objective: "Apply the Skill-First Learning Pattern to LLMOps domain"
    proficiency_level: "B2"
    bloom_level: "Apply"
    assessment_method: "Student demonstrates understanding of why skill creation precedes content learning"

cognitive_load:
  new_concepts: 4
  assessment: "4 concepts (Skill-First pattern, LEARNING-SPEC.md, persona skill structure, documentation fetching) within B1-B2 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Add multi-persona switching logic to your skill specification before learning the implementation"
  remedial_for_struggling: "Focus only on the LEARNING-SPEC.md creation; defer skill file to after L01-L02"
---

# Build Your Persona Tuning Skill

You're about to learn persona fine-tuning. But here's the pattern that will make this knowledge truly yours: **build the skill BEFORE you learn the content**.

This is the Skill-First Learning Pattern you've practiced throughout Part 7. In Chapter 64, you created an `llmops-fine-tuner` skill from Unsloth documentation before learning LoRA theory. That skill now encodes everything you learned about supervised fine-tuning.

This lesson applies the same pattern to persona tuning. By the end of Chapter 65, you'll have:

1. A `persona-tuner` skill encoding style transfer patterns
2. Deep understanding of persona dataset design
3. A working TaskMaster assistant with distinctive personality

But the skill comes first.

## Why Skill-First Works

Traditional learning: **Learn content** -> **Hope to remember** -> **Maybe apply someday**

Skill-First learning: **Define what you need** -> **Create skill scaffold** -> **Learn to improve it** -> **Own production-ready asset**

The difference is ownership. When you build the skill first, every lesson becomes an opportunity to test and improve your skill. You're not passively absorbing information—you're actively building something sellable.

### The Asset You're Building

By the end of this chapter, your `persona-tuner` skill will be able to:

```markdown
Given:
- A base fine-tuned model (from Chapter 64)
- A persona specification (traits, vocabulary, patterns)
- Example conversations

Produce:
- Persona-consistent training data
- Fine-tuning configuration for style transfer
- Evaluation framework for personality consistency
- Multi-persona switching capability
```

This skill becomes a component of your Digital FTE portfolio. When a client asks for a branded AI assistant, you'll have the patterns encoded and ready.

## Step 1: Clone Your Skills Lab Fresh

Every chapter starts clean. This prevents hidden state from previous work affecting your learning.

```bash
# Create fresh workspace for Chapter 65
mkdir -p ~/skills-lab-ch65
cd ~/skills-lab-ch65

# Initialize git repo for version control
git init
git branch -m main

# Create skill directory structure
mkdir -p .claude/skills/persona-tuner
```

**Output:**
```
Initialized empty Git repository in ~/skills-lab-ch65/.git/
```

Why fresh for each chapter? Because accumulated state masks learning. If your persona skill accidentally depends on Chapter 64 artifacts, you won't notice until it breaks in production.

## Step 2: Write Your LEARNING-SPEC.md

Before fetching documentation, define what you want to learn. This is your contract with yourself.

Create `LEARNING-SPEC.md` in your project root:

```markdown
# Learning Specification: Persona Fine-Tuning

## What I Want to Learn

Style transfer through supervised fine-tuning—how to make a model speak
in a specific voice, personality, and tone that's distinctively mine.

## Why It Matters

My Task API Assistant from Chapter 64 works, but it speaks in generic
"AI assistant" voice. I want it to sound like "TaskMaster"—encouraging,
productivity-focused, professional but friendly.

## Success Criteria

By the end of Chapter 65, I can:

1. [ ] Distinguish style tuning from knowledge tuning
2. [ ] Design a persona specification that's trainable
3. [ ] Create 200+ persona-consistent training examples
4. [ ] Fine-tune with style-optimized hyperparameters
5. [ ] Evaluate persona consistency with LLM-as-judge
6. [ ] Build multi-persona switching capability
7. [ ] Deploy TaskMaster with distinctive personality

## Constraints

- **Compute**: Colab Free Tier (T4 GPU)
- **Time**: ~5 hours total for chapter
- **Base Model**: Fine-tuned Task API model from Chapter 64
- **Tools**: Unsloth, HuggingFace, OpenAI API (for data generation)

## Questions I Need Answered

1. How is style tuning different from knowledge tuning?
2. How many examples do I need for personality transfer?
3. What hyperparameters matter most for style vs. knowledge?
4. How do I measure "personality consistency"?
5. Can one model have multiple personas?

## What I Already Know

- Supervised fine-tuning with LoRA (Chapter 64)
- Dataset creation with ChatML format (Chapter 63)
- Training loops with SFTTrainer (Chapter 64)
- Model export to GGUF (Chapter 64)
```

Save this file. You'll return to check off success criteria as you progress through the chapter.

## Step 3: Create Your Skill Scaffold

Now create the initial skill file. This is a scaffold—you'll improve it lesson by lesson.

Create `.claude/skills/persona-tuner/SKILL.md`:

```markdown
---
name: persona-tuner
description: "This skill should be used when fine-tuning for personality, brand voice, or communication style. Use when the goal is HOW a model communicates rather than WHAT it knows."
---

# Persona Tuner Skill

## Purpose

Transform a fine-tuned model into one with distinctive personality traits,
consistent voice, and brand-appropriate communication patterns.

## When to Use This Skill

Activate when:
- Client needs "brand voice" in AI assistant
- Model speaks generically despite knowledge fine-tuning
- Personality consistency matters (customer-facing)
- Multiple personas needed for different user segments

Do NOT use when:
- Goal is domain knowledge (use knowledge fine-tuning)
- No clear personality requirements defined
- Insufficient examples of target voice (<100 conversations)

## Persona Specification Template

[TO BE LEARNED: L02 - Persona Dataset Design]

## Dataset Creation Patterns

[TO BE LEARNED: L03 - Creating Persona Datasets]

## Training Configuration

[TO BE LEARNED: L04 - Persona Fine-Tuning]

## Evaluation Framework

[TO BE LEARNED: L05 - Persona Evaluation]

## Multi-Persona Patterns

[TO BE LEARNED: L06 - Multi-Persona Models]

## Example: TaskMaster Persona

[TO BE LEARNED: L07 - Capstone]
```

Notice the `[TO BE LEARNED]` placeholders. Each lesson will fill in a section, making your progress visible and your skill increasingly complete.

## Step 4: Commit Your Foundation

Version control captures your starting point.

```bash
# Add all files
git add .

# Commit initial structure
git commit -m "chore: init persona-tuner skill scaffold for Ch65"
```

**Output:**
```
[main (root-commit) abc1234] chore: init persona-tuner skill scaffold for Ch65
 3 files changed, 89 insertions(+)
 create mode 100644 .claude/skills/persona-tuner/SKILL.md
 create mode 100644 LEARNING-SPEC.md
```

## Step 5: Fetch Reference Documentation (Optional)

If you have access to Context7 MCP or similar documentation fetching tools, gather official resources:

```
Relevant documentation sources:
- Unsloth documentation (fine-tuning patterns)
- OpenAI fine-tuning guide (persona examples)
- HuggingFace PEFT documentation (LoRA for style)
- Academic papers on personality transfer
```

For now, note these in your LEARNING-SPEC.md under "Resources to Explore." The lessons will provide the essential patterns.

## What You've Built

In 25 minutes, you've established:

| Artifact | Purpose |
|----------|---------|
| `LEARNING-SPEC.md` | Your contract with yourself—what success looks like |
| `persona-tuner/SKILL.md` | Scaffold to fill with patterns as you learn |
| Git history | Starting point for tracking skill evolution |
| Fresh workspace | Clean state preventing hidden dependencies |

## The Learning Loop

For each remaining lesson in Chapter 65:

```
1. Read the lesson content
2. Identify patterns that belong in your skill
3. Update SKILL.md with what you learned
4. Test the pattern (where applicable)
5. Commit your improvements
6. Check off success criteria in LEARNING-SPEC.md
```

By L07 (Capstone), your skill will be complete—not because you copied patterns, but because you discovered them through practice.

## Reflect on Your Skill

After creating your scaffold, consider:

1. **What's already clear?** Looking at your `[TO BE LEARNED]` sections, which ones do you have intuitions about already?

2. **What's confusing?** Which sections have questions you can't even formulate yet?

3. **What's exciting?** Which capability would be most valuable for your work?

Note your answers. They'll guide your attention in the lessons ahead.

## Try With AI

Before moving to L01, use your AI companion to explore your skill's domain.

### Prompt 1: Validate Your Learning Spec

```
I'm about to learn persona fine-tuning. Here's my LEARNING-SPEC.md:

[paste your LEARNING-SPEC.md]

Review my success criteria. Are they:
1. Specific enough to verify?
2. Realistic for 5 hours of learning?
3. Missing anything important for persona tuning?

Challenge me on any criteria that seem vague or over-ambitious.
```

**What you're learning**: Self-assessment through external validation. Your AI partner helps you refine your learning goals before investing time.

### Prompt 2: Preview the Domain

```
I'm building a persona-tuner skill. Before I study the content, help me
develop intuitions:

1. What's the difference between teaching a model WHAT to say vs HOW to say it?
2. How might training data for personality differ from training data for knowledge?
3. What could go wrong if personality training conflicts with knowledge training?

Don't give me complete answers—give me thinking frameworks I can test
against the chapter content.
```

**What you're learning**: Pre-activation of schema. By developing intuitions before learning, you create mental hooks that make new information stick better.

### Prompt 3: Plan Your Skill Evolution

```
My persona-tuner skill has these [TO BE LEARNED] sections:
- Persona Specification Template
- Dataset Creation Patterns
- Training Configuration
- Evaluation Framework
- Multi-Persona Patterns

For each section, suggest:
1. What questions should this section answer?
2. What examples would make the pattern concrete?
3. What common mistakes should it prevent?

I'll use your suggestions to evaluate each lesson—did it answer these questions?
```

**What you're learning**: Active learning preparation. Instead of passive consumption, you're defining criteria for each lesson to meet.

Your skill scaffold is ready. In L01, you'll learn what persona tuning actually is—and add your first real content to the skill.
