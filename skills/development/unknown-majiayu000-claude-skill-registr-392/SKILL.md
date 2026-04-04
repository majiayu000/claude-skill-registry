---
sidebar_position: 0
title: "Build Your LiveKit Agents Skill"
description: "Create your LiveKit Agents skill from official documentation, then learn to improve it throughout the chapter"
keywords: [livekit, agents, voice ai, realtime, skill-first, chatgpt voice]
chapter: 80
lesson: 0
duration_minutes: 30

skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working LiveKit Agents skill using natural language"

  - name: "Voice Agent Architecture"
    proficiency_level: "A2"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "1. Information and Data Literacy"
    measurable_at_this_level: "Student articulates Agents, Sessions, Workers relationship"

  - name: "Documentation-Driven Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "5. Problem Solving"
    measurable_at_this_level: "Student builds skill from official docs, not memory"

learning_objectives:
  - objective: "Build a LiveKit Agents skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working livekit-agents skill in .claude/skills/"

  - objective: "Write a LEARNING-SPEC.md that defines what you want to learn about voice agents"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "Student produces clear success criteria before building"

  - objective: "Fetch and apply official LiveKit documentation via Context7"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill references official docs, not hallucinated patterns"

cognitive_load:
  new_concepts: 3
  assessment: "Three concepts: LEARNING-SPEC, skill creation, documentation fetching. Appropriate for B1."

differentiation:
  extension_for_advanced: "Add MCP integration and multi-agent handoff patterns during creation"
  remedial_for_struggling: "Follow exact prompts provided, skip LEARNING-SPEC refinement"
---

# Build Your LiveKit Agents Skill

Before learning LiveKit Agents—the framework powering ChatGPT's Advanced Voice Mode—you'll **own** a LiveKit Agents skill.

This is skill-first learning. You build the skill, then the chapter teaches you what it knows and how to make it better. By the end, you have a production-ready voice agent AND a reusable skill for building more.

---

## Why LiveKit Agents?

In September 2023, OpenAI unveiled ChatGPT Voice Mode. The technology behind it? LiveKit. When OpenAI launched the feature, they also released LiveKit Agents—an open source framework that made it easy for developers to build their own voice AI agents.

LiveKit Agents was used in every demo during the GPT-4o unveil. The framework now powers voice-driven AI products across the industry—from startups to enterprises building Digital FTEs that can hear, speak, and reason in realtime.

**What you're learning**: Production voice agent architecture from the framework that runs at scale.

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

**Why fresh?** Skills accumulate across chapters. A fresh start ensures your LiveKit skill builds on clean foundations, not inherited state.

---

## Step 2: Write Your LEARNING-SPEC.md

Before asking Claude to build anything, define what you want to learn. This is specification-first learning—you specify intent, then the system executes.

Create a new file:

```bash
touch LEARNING-SPEC.md
```

Write your specification:

```markdown
# LiveKit Agents Skill

## What I Want to Learn
Build voice agents using LiveKit's production framework—the same technology
powering ChatGPT's Advanced Voice Mode.

## Why This Matters
- LiveKit Agents handles the hard parts: WebRTC, turn detection, interruptions
- Understanding the framework means understanding what works at scale
- Every voice-enabled Digital FTE I build will use these patterns

## Success Criteria
- [ ] Create voice agent that responds to speech
- [ ] Implement function calling (tool use via voice)
- [ ] Handle interruptions gracefully (barge-in)
- [ ] Understand deployment to Kubernetes

## Key Questions I Have
1. How do Agents, AgentSessions, and Workers relate to each other?
2. How does semantic turn detection work? Why is it better than silence-based?
3. How do I integrate MCP tools into a voice agent?
4. What's the difference between VoicePipelineAgent and MultimodalAgent?
5. How do I handle phone calls (SIP integration)?

## What I Already Know
- Part 10: Chat interfaces, streaming, tool calling UI
- Part 7: Kubernetes deployment, containerization
- Part 6: Agent SDKs (OpenAI, Claude, Google ADK)

## What I'm Not Trying to Learn Yet
- Pipecat (that's Chapter 81)
- Raw OpenAI Realtime API (that's Chapter 82)
- Phone number provisioning details (that's Chapter 84)
```

**Why write a spec?** The AI amplification principle: clear specifications produce excellent results. Vague requests produce confident-looking output that's wrong in subtle ways.

---

## Step 3: Fetch Official Documentation

Your skill should be built from official sources, not AI memory. AI memory gets outdated; official docs don't.

Ask Claude:

```
Use the context7 skill to fetch the official LiveKit Agents documentation.
I want to understand:
1. Core concepts (Agents, Sessions, Workers)
2. VoicePipelineAgent vs MultimodalAgent
3. Turn detection and interruption handling
4. Function calling and tool integration
5. Deployment patterns

Save key patterns and code examples for building my skill.
```

Claude will:
1. Connect to Context7 (library documentation service)
2. Fetch current LiveKit Agents docs
3. Extract architecture patterns and code examples
4. Prepare knowledge for skill creation

**What you're learning**: Documentation-driven development. The skill you build reflects the framework's current state, not stale training data.

---

## Step 4: Build the Skill

Now create your skill using the documentation Claude just fetched:

```
Using your skill creator skill, create a new skill for LiveKit Agents.
Use the documentation you just fetched from Context7—no self-assumed knowledge.

I will use this skill to build voice agents from hello world to
production systems that handle real phone calls. Focus on:

1. VoicePipelineAgent patterns (STT -> LLM -> TTS pipeline)
2. MultimodalAgent patterns (for Gemini Live, OpenAI Realtime)
3. Semantic turn detection configuration
4. Function calling via voice
5. Kubernetes deployment with Workers

Reference my LEARNING-SPEC.md for context on what I want to learn.
```

Claude will:
1. Read your LEARNING-SPEC.md
2. Apply the fetched documentation
3. Ask clarifying questions (interruption policies, STT/TTS providers, deployment targets)
4. Create the complete skill with references and templates

Your skill appears at `.claude/skills/livekit-agents/`.

---

## Step 5: Verify It Works

Test your skill with a simple prompt:

```
Using the livekit-agents skill, create a minimal voice agent that:
1. Listens for speech
2. Responds with "Hello, I heard you say: [transcription]"
3. Uses Deepgram for STT and Cartesia for TTS

Just the code, no explanation.
```

If your skill works, Claude generates a working agent skeleton. If it doesn't, Claude asks for clarification—which tells you what's missing from your skill.

**Expected output structure**:

```python
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import deepgram, cartesia, openai

async def entrypoint(ctx: JobContext):
    # Your agent implementation
    ...

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
```

---

## What You Now Own

You have a `livekit-agents` skill built from official documentation. It contains:

- **Architecture patterns**: Agents, Sessions, Workers relationships
- **VoicePipelineAgent templates**: The cascaded STT -> LLM -> TTS approach
- **MultimodalAgent templates**: For native speech-to-speech models
- **Turn detection guidance**: Semantic vs silence-based interruption handling
- **Deployment patterns**: Kubernetes Workers, scaling, health checks

The rest of this chapter teaches you what this skill knows—and how to make it better.

---

## Try With AI

### Prompt 1: Refine Your LEARNING-SPEC

```
Review my LEARNING-SPEC.md. Based on the LiveKit Agents documentation
you fetched, what questions am I missing? What success criteria
should I add for a production voice agent?
```

**What you're learning**: Your specification improves through iteration. The AI suggests patterns you hadn't considered—multi-agent handoff, affective dialog, proactive audio. Your spec gets sharper.

### Prompt 2: Explore the Documentation

```
What are the key differences between VoicePipelineAgent and
MultimodalAgent? When should I use each? Give me a decision
framework based on the official docs.
```

**What you're learning**: You're not just reading docs—you're extracting decision frameworks. This is how domain expertise becomes encoded in your skill.

### Prompt 3: Test Your Skill

```
Using the livekit-agents skill, create a voice agent that:
1. Greets the user
2. Asks for their name
3. Creates a task in my Task Manager API
4. Confirms the task was created

Include proper error handling for API failures.
```

**What you're learning**: The skill is tested against a real use case (your Task Manager from previous parts). If it fails, you know where to improve it.

**Note**: The code generated here should run. If it doesn't, that's feedback—your skill needs adjustment. Bring errors to the next lesson.
