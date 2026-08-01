---
name: openai-agent-tools
description: Define reusable function tools for OpenAI Agents using the
---

# Skill: OpenAI Agent Tools

## Purpose
Define reusable function tools for OpenAI Agents using the
OpenAI Agents SDK `function_tool` interface.

These tools expose external capabilities (RAG, databases, selection-based answering)
to the agent without embedding reasoning logic.

## Responsibilities
- Define tools using @function_tool
- Enforce strict input/output contracts
- Provide deterministic, side-effect-aware behavior
- Support Retrieval-Augmented Generation (RAG)

## What This Skill Covers
- function_tool decorator usage
- Tool input schema design
- Tool output structure
- Tool naming conventions

## What This Skill Does NOT Cover
- Agent reasoning or planning
- Prompt engineering
- UI concerns

## Constraints
- Tools must not call LLMs
- Tools must not hallucinate
- Tools must return factual data only

## Used By
- openai_agent_runtime
- RAG Orchestrator Agent
