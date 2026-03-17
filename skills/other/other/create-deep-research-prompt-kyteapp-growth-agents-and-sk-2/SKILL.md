---
name: CREATE_DEEP_RESEARCH_PROMPT
description: Generate a structured deep research prompt. USE WHEN the user needs to research a complex topic, market, or bug deeply. Capabilities include objective clarification, tech stack validation, and prompt generation.
---

# CREATE DEEP RESEARCH PROMPT

**Owner:** Manny (Product Manager)

## Goal
To translate a vague user request (e.g., "Research AI frameworks") into a highly specific, effective prompt for a Deep Research tool or agent.

## Core Principles
- **Context is King:** A research prompt without clear objectives yields noise.
- **Tech Validation:** If researching technology, use `context7` to ensure terms and versions are correct.
- **Classification:** Different research (Market vs. Bug vs. Tech) requires different prompt structures.

## Workflow Instructions

### 1. Classification
- **Action:** Determine the research type.
  - *Product Validation* (Do users actually need this?)
  - *Technical Review* (Is this feasible?)
  - *Bug Diagnosis* (Why is this breaking?)
  - *Market Analysis* (Who are the benchmarks?)

### 2. Objective Clarification
- **Action:** Elicit the "Why."
- **Prompt:** "What decision will this research enable?" or "What is the single most important question to answer?"
- **Constraint:** Stop if the goal is "just curious." Push for actionable intent.

### 3. Context & Tech Validation
- **Action:** If the research involves specific tools/libraries:
  - Call `context7` MCP to verify the library names and current versions.
  - *Example:* If user says "Research Next.js router," verify if they mean Pages or App Router.

### 4. Constructing the Prompt
- **Action:** Assemble the research directive.
- **Structure:**
  - **Objective:** The "North Star" question.
  - **Key Questions:** 3-5 specific sub-questions.
  - **Methodology:** How to search (e.g., "Compare documentation," "Search forums," "Read whitepapers").
  - **Sources:** Define authorized sources (e.g., "Official docs only," "GitHub issues," "Reddit").
  - **Deliverable:** What the output should look like (Table, Summary, Code snippets).

### 5. Review & Export
- **Action:** Present the draft prompt to the user.
- **Refine:** Incorporate feedback.
- **Output:** Save the final prompt as a Markdown file in `outputs/research_prompts/`.

## Anti-Patterns
- **NEVER** generate a generic "Tell me about X" prompt.
- **NEVER** include hallucinated library versions in a research prompt.
- **NEVER** skip the "Success Criteria" definition.

## Output Format
A Markdown file containing the structured prompt, ready to be fed into a reasoning model or research agent.
