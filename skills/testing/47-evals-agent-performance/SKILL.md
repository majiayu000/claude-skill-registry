---
sidebar_position: 0
title: "Build Your Evals Skill"
description: "Create your agent-evals skill from official documentation before learning evaluation concepts. This skill-first approach ensures you build production-ready evaluation capabilities grounded in authoritative sources."
keywords: [agent evaluation, evals, AI testing, graders, error analysis, regression testing, evaluation frameworks]
chapter: 47
lesson: 0
duration_minutes: 25

# HIDDEN SKILLS METADATA
skills:
  - name: "Understanding Evaluation Fundamentals"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Remember"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Student can identify the difference between TDD (code testing) and evals (agent evaluation) and explain why evals produce probabilistic scores rather than PASS/FAIL outcomes"

  - name: "Writing Learning Specifications"
    proficiency_level: "A2"
    category: "Technical"
    bloom_level: "Understand"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can articulate what they want to learn about agent evaluation in a structured LEARNING-SPEC.md document with clear success criteria"

  - name: "Building Skills from Documentation"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student can use AI tools to fetch official documentation and create an initial skill structure following the SKILL.md format"

learning_objectives:
  - objective: "Identify why systematic evaluation distinguishes good agents from great ones"
    proficiency_level: "A2"
    bloom_level: "Remember"
    assessment_method: "Recognition of Andrew Ng's core thesis about disciplined evaluation processes"

  - objective: "Create a LEARNING-SPEC.md document articulating evaluation learning goals"
    proficiency_level: "A2"
    bloom_level: "Apply"
    assessment_method: "Written specification with clear intent, success criteria, and questions to answer"

  - objective: "Build an initial agent-evals skill structure using AI-assisted documentation fetching"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Functional SKILL.md file that passes basic structure validation"

cognitive_load:
  new_concepts: 4
  assessment: "4 concepts (evals vs TDD distinction, LEARNING-SPEC pattern, skill structure, documentation-first approach) within A2-B1 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Research OpenAI's Evals framework and Google ADK's evaluation module; compare grader patterns across frameworks"
  remedial_for_struggling: "Focus on the LEARNING-SPEC.md creation only; defer skill building to next session"
---

# Build Your Evals Skill

You have built agents that generate outputs, make decisions, and take actions. But how do you know if those outputs are actually good? How do you measure whether your agent made the right decision, not just a decision? This is where most developers struggle, and it separates effective AI builders from the rest.

Andrew Ng, one of the pioneers of modern AI, identified the critical pattern: "One of the biggest predictors for whether someone is able to build agentic workflows really well is whether or not they're able to drive a really disciplined evaluation process." The developers who master evaluation build agents that improve systematically. The developers who skip evaluation build agents that seem to work until they fail in production.

This lesson follows the Skill-First pattern. Instead of learning evaluation concepts first and building a skill later, you will create your `agent-evals` skill immediately. Why? Because building the skill forces you to engage with official documentation from the start. Your skill becomes grounded in authoritative sources rather than general knowledge. Every lesson in this chapter will then test and improve your skill, and by the capstone, you will own a production-ready evaluation capability.

## Why Skill-First for Evals

The traditional approach to learning agent evaluation looks like this:

1. Read about evaluation concepts
2. See some examples
3. Maybe build something later
4. Forget most of it within a week

The Skill-First approach inverts this:

1. Define what you want to learn (specification)
2. Build a skill structure from official documentation
3. Learn concepts by improving your skill
4. End the chapter owning a valuable asset

The difference is ownership. In traditional learning, knowledge lives in your head (temporarily). In Skill-First learning, knowledge lives in a reusable skill that you can apply to every future agent project.

For evaluations specifically, this matters more than most topics. Evaluation requires discipline, and discipline requires structure. By encoding evaluation methodology into a skill, you create a forcing function that ensures you actually do the work rather than skipping it when deadlines pressure you.

## Clone skills-lab Fresh

Every chapter starts with a clean slate. This prevents confusion from leftover files and ensures reproducible results.

Open your terminal and navigate to your workspace directory:

```bash
cd ~/workspace
```

If you have a previous `skills-lab` directory, remove it:

```bash
rm -rf skills-lab
```

Clone a fresh copy:

```bash
git clone https://github.com/panaversity/skills-lab.git
cd skills-lab
```

**Output:**
```
Cloning into 'skills-lab'...
remote: Enumerating objects: 156, done.
remote: Counting objects: 100% (156/156), done.
remote: Compressing objects: 100% (89/89), done.
Receiving objects: 100% (156/156), 24.18 KiB | 1.21 MiB/s, done.
```

Verify the directory structure:

```bash
ls -la
```

**Output:**
```
total 16
drwxr-xr-x   6 user  staff   192 Dec 30 10:00 .
drwxr-xr-x  12 user  staff   384 Dec 30 10:00 ..
drwxr-xr-x   8 user  staff   256 Dec 30 10:00 .git
-rw-r--r--   1 user  staff   234 Dec 30 10:00 README.md
drwxr-xr-x   3 user  staff    96 Dec 30 10:00 skills
drwxr-xr-x   2 user  staff    64 Dec 30 10:00 specs
```

You now have a clean environment ready for skill development.

## Write Your LEARNING-SPEC.md

Before fetching documentation or building anything, articulate what you want to learn. This specification becomes your learning contract. It defines success criteria that you can measure at the end of the chapter.

Create the specification file:

```bash
mkdir -p specs/agent-evals
touch specs/agent-evals/LEARNING-SPEC.md
```

Open the file in your editor and add:

```markdown
# LEARNING-SPEC: Agent Evaluations

## Intent

I want to learn how to systematically evaluate AI agent performance so that I can:
1. Measure whether my agents make good decisions (not just any decisions)
2. Catch quality regressions before they reach production
3. Improve agent performance through data-driven iteration

## Success Criteria

By the end of Chapter 47, I will be able to:

- [ ] Explain the difference between TDD (testing code) and evals (testing reasoning)
- [ ] Design an evaluation dataset with typical, edge, and error cases
- [ ] Create graders that turn subjective quality into measurable scores
- [ ] Perform error analysis to find which component caused failures
- [ ] Set up regression protection that runs on every agent change
- [ ] Choose between end-to-end and component-level evals appropriately

## Questions to Answer

1. How do I define "good" for an agent output when there's no single right answer?
2. Why do LLM graders fail with 1-5 scales, and what works instead?
3. How do I trace errors back to specific agent components?
4. When should I use end-to-end evals vs component-level evals?
5. How many test cases do I actually need to start?

## Constraints

- Focus on framework-agnostic concepts (apply to any SDK)
- Start with 10-20 test cases, not 1000
- Prioritize quick-and-dirty evals over perfect ones
- Use binary criteria instead of numeric scales

## Non-Goals

- Building a complete evaluation framework from scratch
- Learning every evaluation library in detail
- Achieving perfect agent performance (iterative improvement instead)
```

**Output:**
```
(No output - file created silently)
```

Verify the file exists:

```bash
cat specs/agent-evals/LEARNING-SPEC.md | head -20
```

**Output:**
```
# LEARNING-SPEC: Agent Evaluations

## Intent

I want to learn how to systematically evaluate AI agent performance so that I can:
1. Measure whether my agents make good decisions (not just any decisions)
2. Catch quality regressions before they reach production
3. Improve agent performance through data-driven iteration

## Success Criteria

By the end of Chapter 47, I will be able to:

- [ ] Explain the difference between TDD (testing code) and evals (testing reasoning)
- [ ] Design an evaluation dataset with typical, edge, and error cases
- [ ] Create graders that turn subjective quality into measurable scores
```

You now have a clear learning contract that defines what success looks like.

## Create Initial Skill Structure

With your learning specification in place, create the skill directory and file:

```bash
mkdir -p skills/agent-evals
touch skills/agent-evals/SKILL.md
```

Add the initial skill structure. This is a skeleton that you will develop throughout the chapter:

```markdown
---
name: agent-evals
description: Design and implement evaluation frameworks for AI agents. Use when testing agent reasoning quality, building graders, performing error analysis, or establishing regression protection.
---

# Agent Evaluations Skill

## Core Thesis

"One of the biggest predictors for whether someone is able to build agentic workflows really well is whether or not they're able to drive a really disciplined evaluation process." - Andrew Ng

## When to Activate

Use this skill when:
- Building quality checks for any AI agent
- Designing evaluation datasets
- Creating graders to define "good" automatically
- Performing error analysis to find failure patterns
- Setting up regression protection for agent changes

## Key Concepts (To Be Developed)

### Evals vs TDD

| Aspect | TDD (Code Testing) | Evals (Agent Evaluation) |
|--------|-------------------|-------------------------|
| **Tests** | Does function return correct output? | Did agent make the right decision? |
| **Outcome** | PASS or FAIL (deterministic) | Scores (probabilistic) |
| **Analogy** | Testing if calculator works | Testing if student knows WHEN to use multiplication |

### Graders (TODO)

- Binary criteria over 1-5 scales
- LLM-as-Judge patterns
- Position bias awareness

### Error Analysis (TODO)

- Build-Analyze loop
- Trace and span terminology
- Error classification patterns

### Dataset Design (TODO)

- Quality over quantity (10-20 cases to start)
- Three categories: typical, edge, error
- Use real data, not synthetic

### Regression Protection (TODO)

- Run evals on every change
- Baseline comparison
- Eval-driven development loop

## Integration

This skill connects to:
- SDK-specific evaluation modules (OpenAI, Claude, Google ADK)
- Observability skills for trace analysis
- CI/CD skills for automated eval runs

---

*Status: Initial skeleton - to be developed through Chapter 47*
```

**Output:**
```
(No output - file created silently)
```

Verify the skill structure:

```bash
cat skills/agent-evals/SKILL.md | head -30
```

**Output:**
```
---
name: agent-evals
description: Design and implement evaluation frameworks for AI agents. Use when testing agent reasoning quality, building graders, performing error analysis, or establishing regression protection.
---

# Agent Evaluations Skill

## Core Thesis

"One of the biggest predictors for whether someone is able to build agentic workflows really well is whether or not they're able to drive a really disciplined evaluation process." - Andrew Ng

## When to Activate

Use this skill when:
- Building quality checks for any AI agent
- Designing evaluation datasets
```

## Verify Your Skill Works

A skill needs to be invokable. Test that your skill loads correctly by checking its structure:

```bash
# Check YAML frontmatter is valid
head -5 skills/agent-evals/SKILL.md
```

**Output:**
```
---
name: agent-evals
description: Design and implement evaluation frameworks for AI agents. Use when testing agent reasoning quality, building graders, performing error analysis, or establishing regression protection.
---
```

The skill has valid frontmatter with `name` and `description` fields. This is the minimum requirement for a Claude Code skill.

Check the file size to ensure content exists:

```bash
wc -l skills/agent-evals/SKILL.md
```

**Output:**
```
62 skills/agent-evals/SKILL.md
```

You now have a working skill skeleton. Each subsequent lesson in this chapter will add content to specific sections, transforming this skeleton into a production-ready evaluation capability.

## What You Built Today

| Artifact | Purpose | Location |
|----------|---------|----------|
| Clean skills-lab | Reproducible starting point | `~/workspace/skills-lab/` |
| LEARNING-SPEC.md | Learning contract with success criteria | `specs/agent-evals/LEARNING-SPEC.md` |
| SKILL.md skeleton | Initial skill structure to develop | `skills/agent-evals/SKILL.md` |

You have not learned evaluation concepts yet. That is intentional. You have built the container that will hold that knowledge. As you progress through this chapter, every concept you learn gets encoded into your skill. By the end, you own something valuable: a reusable evaluation methodology grounded in official documentation and tested through practice.

## Try With AI

Use Claude Code, Gemini CLI, or your preferred AI tool. These prompts help you verify understanding and begin developing your skill.

### Prompt 1: Validate Your Learning Specification

```
Review my LEARNING-SPEC.md for agent evaluations:

[Paste your LEARNING-SPEC.md content]

Questions:
1. Are my success criteria measurable? Which ones are vague?
2. What questions am I missing that I should add?
3. Do my constraints make sense for a beginner learning evals?
```

**What you're learning:** Specification quality matters. Clear success criteria let you measure progress. Vague criteria like "understand evaluations" cannot be measured. AI helps identify which criteria need sharpening before you invest time learning.

### Prompt 2: Expand Your Skill's "When to Activate" Section

```
I'm building an agent-evals skill. Here's my current "When to Activate" section:

Use this skill when:
- Building quality checks for any AI agent
- Designing evaluation datasets
- Creating graders to define "good" automatically
- Performing error analysis to find failure patterns
- Setting up regression protection for agent changes

What specific scenarios am I missing? Give me 3-5 additional triggers
that would indicate someone should use this skill. Focus on situations
a developer might not immediately recognize as evaluation problems.
```

**What you're learning:** Skill activation triggers determine when your skill gets used. Comprehensive triggers ensure you apply evaluation methodology in all relevant situations, not just obvious ones. AI suggests scenarios you might overlook.

### Prompt 3: Connect Evals to Your Domain

```
I'm learning agent evaluation. My domain is [describe your field:
customer support, content generation, data analysis, etc.].

Help me think through:
1. What would "good" mean for an agent in my domain?
2. What are 3 typical cases I should test?
3. What are 2 edge cases that might break my agent?
4. What's 1 error case where the agent should gracefully fail?

Use these to help me draft the "Dataset Design" section of my skill.
```

**What you're learning:** Evaluation is domain-specific. "Good" for a customer support agent differs from "good" for a code review agent. AI helps you translate abstract concepts to your specific context, making your skill immediately applicable.

### Safety Note

Evaluation skills require judgment about what constitutes "good" agent behavior. AI can suggest patterns and criteria, but you must validate that evaluation frameworks align with your actual requirements. Do not assume AI-suggested grading criteria match your domain's definition of quality. Test evaluation approaches with real examples from your use case before trusting them in production.

