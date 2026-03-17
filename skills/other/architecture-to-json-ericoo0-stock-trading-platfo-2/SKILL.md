---
name: architecture-to-json
description: Guide for extracting architectural diagrams, flowcharts, and sequence diagrams into a structured JSON format. Use this skill when you need to transform a visual or textual description of a system architecture or workflow into a clear, structured JSON representation.
---

# Architecture/Diagram To JSON

## Overview

This skill provides a standardized workflow for converting various diagram types (System Architecture, Flowcharts, Sequence Diagrams) into a structured JSON format.

## Workflow

1.  **Identify Diagram Type**: Determine if the source is an Architecture Diagram, a Flowchart, or a Sequence Diagram.
2.  **Load Reference**: Based on the identified type, read the corresponding guideline file:
    - **Architecture Diagram**: Read `references/architecture.md`
    - **Flowchart**: Read `references/flowchart.md`
    - **Sequence Diagram**: Read `references/sequence.md`
3.  **Map to JSON**: Use the schema defined in the loaded reference file to structure the data.
4.  **Enforce Constraints**: Ensure nesting and structure follow the guidelines in the reference file.
5.  **Summarize Results**: Provide a brief summary of the extracted elements (e.g., component count, steps, or swimlanes).

## Output Requirements

When using this skill, your output should include:

1.  The complete JSON structure.
2.  A brief summary of the extracted content (relevant to the diagram type).
3.  Notes on any adaptations or assumptions made during extraction.
