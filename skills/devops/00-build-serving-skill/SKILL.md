---
sidebar_position: 0
title: "Build Your Model Serving Skill"
description: "Create your model-serving skill from Ollama documentation before learning deployment theory"
chapter: 70
lesson: 0
duration_minutes: 25

# HIDDEN SKILLS METADATA
skills:
  - name: "Skill-First Learning Application"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can create a model-serving skill from official Ollama documentation using the Skill-First pattern"

  - name: "Documentation-Grounded Skill Creation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student can fetch and synthesize official Ollama documentation into a structured skill"

  - name: "Model Serving Fundamentals"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Student can explain the structure and purpose of a model-serving skill"

learning_objectives:
  - objective: "Create a model-serving skill from Ollama documentation"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill file creation with correct structure and grounded content"

  - objective: "Apply the Skill-First Learning Pattern to model deployment"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "LEARNING-SPEC.md creation with clear success criteria"

  - objective: "Understand the structure of model serving skills"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Explanation of skill components and their purposes"

cognitive_load:
  new_concepts: 4
  assessment: "4 concepts (Skill-First pattern, LEARNING-SPEC, Ollama documentation grounding, model serving skill structure) within B1 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Add vLLM configuration patterns and multi-GPU serving options to the skill"
  remedial_for_struggling: "Focus on the basic Ollama skill structure; defer advanced sections to later lessons"
---

# Build Your Model Serving Skill

You have a fine-tuned model from Chapter 69. Now you need to deploy it so real users can interact with it. But here is the pattern that separates effective AI-native developers from those who struggle: **build your skill first, then learn the technology**.

In traditional learning, you study deployment options, configure servers, troubleshoot errors, and hope you remember the patterns later. In Skill-First learning, you create a reusable intelligence asset before you even understand the technology deeply. This asset grows with you as you learn, and by the end of the chapter, you own a production-ready skill you can sell or deploy.

This lesson follows the same pattern you used in Part 6, Part 7, and earlier Part 8 chapters. Clone a fresh skills-lab, fetch official documentation, and build your `model-serving` skill from authoritative sources rather than memory.

## Why Skill-First for Model Serving?

Model serving involves multiple components: export formats (GGUF, safetensors), quantization levels (Q4_K_M, Q8_0), inference servers (Ollama, vLLM), and performance tuning (batch sizes, context lengths, memory management). Trying to memorize all configuration options is futile. But encoding it into a skill that you can invoke, test, and improve makes this knowledge permanently accessible and actionable.

| Traditional Approach | Skill-First Approach |
|---------------------|---------------------|
| Read docs, forget configs | Build skill, query anytime |
| Scattered Stack Overflow links | Single authoritative source |
| Knowledge decays over time | Skill improves with use |
| Cannot delegate to AI | AI executes your skill |

By the end of this chapter, your `model-serving` skill will guide you through:
- Model export and format conversion
- Quantization selection for your hardware
- Ollama installation and configuration
- REST API integration with Python
- Performance optimization for latency targets

## Step 1: Clone a Fresh Skills-Lab

Start with a clean environment. This prevents state from previous experiments from affecting your work.

```bash
# Clone the skills-lab repository
git clone https://github.com/panaversity/skills-lab.git ~/skills-lab-ch70

# Navigate to the directory
cd ~/skills-lab-ch70

# Create the skill directory structure
mkdir -p .claude/skills/model-serving
```

**Output:**
```
Cloning into '/Users/you/skills-lab-ch70'...
```

## Step 2: Write Your LEARNING-SPEC.md

Before creating the skill, define what you are trying to accomplish. This specification guides both your learning and the skill you create.

```markdown
# LEARNING-SPEC.md

## What I Want to Learn
Local model serving using Ollama with GGUF models on consumer hardware
(8GB+ RAM, optional GPU).

## Why This Matters
I want to deploy my fine-tuned Task API model locally with:
- Fast response times (<500ms latency)
- No cloud dependency for inference
- REST API for integration with existing applications
- Cost-effective serving without GPU rental fees

## Success Criteria
1. I can export models to GGUF format with appropriate quantization
2. I can configure Ollama to serve custom models
3. I can achieve <500ms latency on consumer hardware
4. I can integrate with Python applications via REST API
5. My skill accurately reflects official Ollama documentation

## Constraints
- Must work on consumer hardware (8GB+ RAM minimum)
- Must use Ollama for local serving
- Must produce REST API endpoints
- Should support both CPU and GPU inference

## Running Example
Deploy the Task API model (fine-tuned in Chapter 64-69) via Ollama
with REST API access for task management applications.
```

Save this file in your skills-lab directory.

## Step 3: Fetch Official Documentation

The skill must be grounded in official documentation, not AI memory which may be outdated or hallucinated.

Use Claude Code or your AI assistant:

```
/fetching-library-docs ollama

Fetch the official Ollama documentation covering:
1. Model import and Modelfile syntax
2. REST API endpoints (/api/generate, /api/chat)
3. Performance tuning options
4. GGUF format requirements
```

Key sources to reference:
- [Ollama GitHub Repository](https://github.com/ollama/ollama)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama Modelfile Reference](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
- [llama.cpp GGUF Format](https://github.com/ggerganov/llama.cpp)

## Step 4: Create Your model-serving Skill

Based on the documentation, create your skill file. Here is a starter template:

```markdown
---
name: model-serving
description: This skill should be used when deploying and serving LLM models locally. Use when exporting to GGUF, configuring Ollama, setting up REST APIs, and optimizing inference performance.
---

# Model Serving Skill

## Purpose

Guide local deployment and serving of LLMs using Ollama with GGUF models
on consumer hardware for production-ready inference.

## When to Use This Skill

Invoke this skill when:
- Exporting fine-tuned models to GGUF format
- Selecting quantization levels for target hardware
- Configuring Ollama with custom Modelfiles
- Setting up REST API endpoints for applications
- Optimizing inference for latency and throughput
- Troubleshooting serving issues

## Hardware Context

**Consumer Hardware (Target):**
- 8GB+ RAM minimum
- Optional GPU (NVIDIA/AMD/Apple Silicon)
- CPU inference fallback available

**Performance Targets:**
- First token: <200ms
- Total latency: <500ms
- Throughput: 10+ requests/second (with batching)

## Quantization Selection Guide

| Quantization | Size (7B) | Quality | Speed | Use Case |
|--------------|-----------|---------|-------|----------|
| Q4_K_M | ~4GB | Good | Fast | **Default choice** |
| Q5_K_M | ~5GB | Better | Moderate | Quality-sensitive |
| Q8_0 | ~8GB | Best | Slower | Maximum quality |

## Ollama REST API

### Generate Endpoint

POST http://localhost:11434/api/generate

### Chat Endpoint

POST http://localhost:11434/api/chat

## Troubleshooting

### Model Not Loading
1. Check GGUF file path is correct
2. Verify sufficient RAM available
3. Check Ollama logs for errors

### Slow Inference
1. Enable GPU if available
2. Reduce context length
3. Use more aggressive quantization
```

Save this to `.claude/skills/model-serving/SKILL.md`.

## Step 5: Verify Your Skill

Test that your skill was created correctly:

```bash
# Check the skill exists
ls -la .claude/skills/model-serving/

# View the skill content
head -50 .claude/skills/model-serving/SKILL.md
```

**Output:**
```
total 8
drwxr-xr-x  3 you  staff   96 Jan  1 10:00 .
drwxr-xr-x  3 you  staff   96 Jan  1 10:00 ..
-rw-r--r--  1 you  staff  2048 Jan  1 10:00 SKILL.md
```

## What Happens Next

You now have a `model-serving` skill that is grounded in official documentation. As you progress through this chapter:

| Lesson | How Your Skill Improves |
|--------|------------------------|
| L01: Export Formats | Add GGUF vs safetensors decision tree |
| L02: Quantization | Add detailed quality/speed tradeoffs |
| L03: Ollama Setup | Add platform-specific installation notes |
| L04: Local Serving | Add Python client patterns |
| L05: vLLM Theory | Add production architecture context |
| L06: Performance | Add latency optimization techniques |
| L07: Capstone | Validate skill produces working deployment |

Each lesson will include a "Reflect on Your Skill" section where you update and improve this skill based on what you learned.

## Try With AI

Use your AI companion (Claude, ChatGPT, Gemini, or similar).

### Prompt 1: Verify Skill Structure

```
I just created my model-serving skill for Ollama deployment. Review the
structure and tell me:
1. Does it follow the SKILL.md format correctly?
2. Is the content grounded in documentation (not hallucinated)?
3. What sections should I add as I learn more about model serving?

Here is my skill:
[paste your SKILL.md content]
```

**What you are learning**: Critical evaluation of your own skill structure. Your AI partner helps identify gaps before you invest time in an incomplete skill.

### Prompt 2: Connect to Your Hardware

```
I have [describe your hardware: M1 Mac with 16GB RAM / Windows PC with RTX 3060 /
Linux server with 32GB RAM]. Looking at my model-serving skill, what
hardware-specific optimizations should I add? What quantization level
would you recommend for my setup?
```

**What you are learning**: Hardware-aware optimization. Model serving is not one-size-fits-all. Your AI partner helps you anticipate hardware-specific challenges.

### Prompt 3: Validate Against Official Docs

```
Compare my skill's Ollama configuration recommendations against the official
Ollama documentation. Are there any discrepancies? Any best practices
I should add?

Specifically check:
1. Modelfile syntax
2. REST API endpoints
3. Performance tuning options
```

**What you are learning**: Documentation verification. You are building the habit of validating AI-generated content against authoritative sources.

### Safety Note

As you create skills from documentation, remember that AI tools may not have the most current information. Always verify critical configuration values against the official source. The Ollama documentation is updated regularly as the project evolves.
