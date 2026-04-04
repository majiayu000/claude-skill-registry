---
sidebar_position: 1
title: "Build Your Pipecat Skill"
description: "Create your Pipecat skill from official documentation, then learn to improve it throughout the chapter"
keywords: [pipecat, voice ai, frames, pipeline, skill-first, providers]
chapter: 81
lesson: 0
duration_minutes: 30

skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working Pipecat skill using natural language"

  - name: "Frame-Based Architecture"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "1. Information and Data Literacy"
    measurable_at_this_level: "Student articulates frames, processors, pipelines relationship"

  - name: "Documentation-Driven Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "5. Problem Solving"
    measurable_at_this_level: "Student builds skill from official docs, not memory"

learning_objectives:
  - objective: "Build a Pipecat skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working pipecat skill in .claude/skills/"

  - objective: "Write a LEARNING-SPEC.md that defines what you want to learn about frame-based voice pipelines"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "Student produces clear success criteria before building"

  - objective: "Fetch and apply official Pipecat documentation via Context7"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill references official docs, not hallucinated patterns"

cognitive_load:
  new_concepts: 2
  assessment: "Two concepts: LEARNING-SPEC, skill creation. Appropriate for B1."

differentiation:
  extension_for_advanced: "Add S2S integration and custom processor patterns during creation"
  remedial_for_struggling: "Follow exact prompts provided, skip LEARNING-SPEC refinement"
---

# Build Your Pipecat Skill

Before learning Pipecat—a frame-based voice AI framework with 40+ provider integrations—you'll **own** a Pipecat skill.

This is skill-first learning. You build the skill, then the chapter teaches you what it knows and how to make it better. By the end, you have a production-ready voice agent AND a reusable skill for building more.

---

## Why Pipecat?

Pipecat started as an internal framework at Daily.co for building voice bots. After the team saw how well it worked, they open-sourced it in 2024. Since then, it has grown to over 8,900 GitHub stars and supports 40+ AI service integrations.

The framework's key insight: **everything is a frame**. Audio data, text transcriptions, LLM responses, control signals—all frames flowing through a pipeline of processors. This simple abstraction enables powerful composition: swap providers with one line, add custom processing anywhere, deploy to any transport.

**What you're learning**: A compositional approach to voice AI that gives you maximum flexibility.

---

## Pipecat vs LiveKit

You learned LiveKit Agents in Chapter 80. Here's how Pipecat differs:

| Dimension | LiveKit Agents | Pipecat |
|-----------|----------------|---------|
| **Core Abstraction** | Jobs (distributed work) | Frames (data flow) |
| **Architecture** | Workers, Sessions, Agents | Pipelines, Processors, Transports |
| **Provider Strategy** | Curated integrations | Plugin ecosystem (40+) |
| **Transport** | WebRTC-first | Transport-agnostic |
| **Turn Detection** | Semantic (transformer) | Configurable (VAD-based) |

Neither is "better"—they solve different problems. LiveKit excels at enterprise scale and semantic understanding. Pipecat excels at flexibility and rapid iteration.

---

## Step 1: Clone Skills-Lab Fresh

Every chapter starts fresh. No state assumptions.

1. Go to [github.com/panaversity/claude-code-skills-lab](https://github.com/panaversity/claude-code-skills-lab)
2. Click the green **Code** button
3. Select **Download ZIP**
4. Extract the ZIP file
5. Open the extracted folder in your terminal

```bash
cd claude-code-skills-lab
claude
```

**Why fresh?** Skills accumulate across chapters. A fresh start ensures your Pipecat skill builds on clean foundations, not inherited state from Chapter 80.

---

## Step 2: Write Your LEARNING-SPEC.md

Before asking Claude to build anything, define what you want to learn. This is specification-first learning—you specify intent, then the system executes.

Create a new file:

```bash
touch LEARNING-SPEC.md
```

Write your specification:

```markdown
# Pipecat Skill

## What I Want to Learn
Build voice agents using Pipecat's frame-based pipeline architecture—a flexible
alternative to LiveKit that supports 40+ AI service integrations.

## Why This Matters
- Pipecat's frame model enables custom processing anywhere in the pipeline
- 40+ provider integrations means I can optimize for cost, latency, or quality
- Transport-agnostic design means I deploy once, run anywhere
- S2S model support (OpenAI Realtime, Gemini Live) through unified interface

## Success Criteria
- [ ] Create voice pipeline that responds to speech
- [ ] Swap providers without changing pipeline structure
- [ ] Add custom processor for domain-specific logic
- [ ] Configure different transports (WebRTC, WebSocket, local)

## Key Questions I Have
1. How do frames flow through the pipeline?
2. What's the difference between AudioRawFrame and TextFrame?
3. How do I integrate OpenAI Realtime through Pipecat?
4. How do I build a custom processor?
5. What transports are available and when do I use each?

## What I Already Know
- Chapter 80: LiveKit Agents (Agents, Sessions, Workers architecture)
- Chapter 79: Voice AI fundamentals (STT, LLM, TTS pipeline)
- Part 10: Chat interfaces, streaming, WebSocket communication

## What I'm Not Trying to Learn Yet
- Raw OpenAI Realtime API (that's Chapter 82)
- Raw Gemini Live API (that's Chapter 83)
- Phone integration specifics (that's Chapter 84)
```

**Why write a spec?** The AI amplification principle: clear specifications produce excellent results. Your spec focuses the skill on what YOU need, not generic patterns.

---

## Step 3: Fetch Official Documentation

Your skill should be built from official sources, not AI memory. AI memory gets outdated; official docs don't.

Ask Claude:

```
Use the context7 skill to fetch the official Pipecat documentation.
I want to understand:
1. Frame-based architecture (what are frames, how do they flow)
2. Processors and pipelines (how to compose them)
3. Available transports (Daily, WebSocket, local)
4. Provider integrations (STT, LLM, TTS plugins)
5. S2S model support (OpenAI Realtime, Gemini Live)

Save key patterns and code examples for building my skill.
```

Claude will:
1. Connect to Context7 (library documentation service)
2. Fetch current Pipecat docs from GitHub
3. Extract architecture patterns and code examples
4. Prepare knowledge for skill creation

**What you're learning**: Documentation-driven development. The skill you build reflects the framework's current state, not stale training data.

---

## Step 4: Build the Skill

Now create your skill using the documentation Claude just fetched:

```
Using your skill creator skill, create a new skill for Pipecat.
Use the documentation you just fetched from Context7—no self-assumed knowledge.

I will use this skill to build voice agents from hello world to
production systems with custom processing. Focus on:

1. Frame types (AudioRawFrame, TextFrame, EndFrame, control frames)
2. Processor patterns (how to transform frames)
3. Pipeline composition (how to chain processors)
4. Transport configuration (Daily, WebSocket, local)
5. Provider plugins (how to swap STT, LLM, TTS)
6. S2S model integration (OpenAI Realtime, Gemini Live through Pipecat)

Reference my LEARNING-SPEC.md for context on what I want to learn.
```

Claude will:
1. Read your LEARNING-SPEC.md
2. Apply the fetched documentation
3. Ask clarifying questions (providers, transport, use cases)
4. Create the complete skill with references and templates

Your skill appears at `.claude/skills/pipecat/`.

---

## Step 5: Verify It Works

Test your skill with a simple prompt:

```
Using the pipecat skill, create a minimal voice pipeline that:
1. Receives audio from Daily WebRTC transport
2. Transcribes with Deepgram
3. Responds with "I heard: [transcription]" using Cartesia TTS

Just the code, no explanation.
```

If your skill works, Claude generates a working pipeline skeleton. If it doesn't, Claude asks for clarification—which tells you what's missing from your skill.

**Expected output structure**:

```python
import asyncio
from pipecat.frames.frames import EndFrame, TextFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.transports.services.daily import DailyTransport

async def main():
    transport = DailyTransport(...)
    stt = DeepgramSTTService(...)
    tts = CartesiaTTSService(...)

    pipeline = Pipeline([
        transport.input(),
        stt,
        # Your processing logic here
        tts,
        transport.output()
    ])

    runner = PipelineRunner()
    task = PipelineTask(pipeline)
    await runner.run(task)
```

---

## The Frame Mental Model

Before proceeding, understand the core insight:

```
┌─────────────────────────────────────────────────────────────────┐
│                    EVERYTHING IS A FRAME                         │
├──────────────────┬──────────────────┬────────────────────────────┤
│   AudioRawFrame  │    TextFrame     │      EndFrame              │
│   (audio bytes)  │   (text string)  │   (signals completion)     │
├──────────────────┴──────────────────┴────────────────────────────┤
│                                                                   │
│    Transport ──▶ STT ──▶ LLM ──▶ TTS ──▶ Transport               │
│      Audio       Text    Text   Audio     Audio                  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Frames are the data unit**. Processors receive frames, transform them, emit new frames. Pipelines connect processors. Transports move frames to/from the outside world.

This is different from LiveKit's job model. In LiveKit, you think about distributed work. In Pipecat, you think about data flowing through transformations.

---

## What You Now Own

You have a `pipecat` skill built from official documentation. It contains:

- **Frame type knowledge**: AudioRawFrame, TextFrame, EndFrame, control frames
- **Processor patterns**: How to build and chain processors
- **Pipeline composition**: How to construct complete voice systems
- **Transport options**: Daily WebRTC, WebSocket, local audio
- **Provider plugins**: How to integrate 40+ AI services

The rest of this chapter teaches you what this skill knows—and how to make it better.

---

## Try With AI

### Prompt 1: Refine Your LEARNING-SPEC

```
Review my LEARNING-SPEC.md. Based on the Pipecat documentation
you fetched, what questions am I missing? What success criteria
should I add for production voice agents?
```

**What you're learning**: Your specification improves through iteration. The AI suggests patterns you hadn't considered—interruption handling, parallel pipelines, error recovery. Your spec gets sharper.

### Prompt 2: Compare to LiveKit

```
I have both livekit-agents and pipecat skills now. Compare them:

1. When should I use LiveKit vs Pipecat?
2. What can I do in Pipecat that's harder in LiveKit?
3. What can I do in LiveKit that's harder in Pipecat?
4. Can I use them together in the same project?

Help me build a decision framework for choosing frameworks.
```

**What you're learning**: Framework comparison—understanding tradeoffs enables informed decisions for real projects.

### Prompt 3: Test Your Skill

```
Using the pipecat skill, create a voice agent for my Task Manager that:
1. Greets the user
2. Asks for a task description
3. Creates the task via API call
4. Confirms creation

Use Deepgram for STT, GPT-4o-mini for LLM, and Cartesia for TTS.
Include error handling for API failures.
```

**What you're learning**: The skill is tested against a real use case (your Task Manager from previous parts). If it fails, you know where to improve it.

**Note**: The code generated here should run. If it doesn't, that's feedback—your skill needs adjustment. Bring errors to the next lesson.
