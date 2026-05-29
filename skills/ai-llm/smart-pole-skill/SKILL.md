---
name: smart-pole-instructor
description: Use when a user provides a vague prompt and needs structured clarification to produce a precise master prompt.
---

# SMART POLE Instructor Skill

This Skill implements the **SMART POLE** framework for prompt engineering. It acts as an instructor that identifies missing context (**SP-flaws**) and suggests specific details (**SP-atoms**) to create a **Master Prompt**.

## How to use this Skill

1. **Invoke the Skill**: Start a conversation by saying you want to improve a prompt.
2. **Provide your Prompt**: Paste the vague or draft prompt you have.
3. **Receive Analysis**: The Skill will list the **SP-flaws** (missing categories). (Note: Models like Claude will use `<thinking>` tags for this).
4. **Iterate**: Answer the questions or add the atoms suggested.
5. **Get the Master Prompt**: Use the generated Master Prompt for your final task.

## The 9 Categories
| Abbrev | Category | Focus | Priority |
| --- | --- | --- | --- |
| **S** | Style | Tone, Persona, Format | 🟢 Accelerator |
| **M** | Mastery | Expertise level | 🟡 Contextualizer |
| **A** | Aim | Goal and Success criteria | 🔴 **CORE** |
| **R** | Resource | Tools, Constraints, Budget | 🟡 Contextualizer |
| **T** | Time | Era, Deadlines, Duration | 🟢 Accelerator |
| **P** | People | Audience, Values, Preferences | 🟡 Contextualizer |
| **O** | Outline | Structure, Scope | 🔴 **CORE** |
| **L** | Locale | Industry, Region, Legal, Cultural | 🔴/🟡 **CONDITIONAL** |
| **E** | Example | Samples, Reference styles | 🟢 Accelerator |

### Locale Sub-dimensions (L1-L4)
- **L1**: Industry/Domain (Banking, Healthcare, E-commerce...)
- **L2**: Geography/Region (Vietnam, EU, Singapore...)
- **L3**: Legal/Regulatory (GDPR, PCI-DSS...)
- **L4**: Cultural/Social (Local customs, social norms...)

### Task-Type Classification (NEW)
Locale becomes **CORE** for consulting/brainstorm tasks:

| Task Type | Locale | When to use |
|-----------|--------|-------------|
| Deterministic | Optional | Math, algorithms, bug fixes |
| Generative | Contextual | Writing, designing |
| Advisory/Discovery | **CORE** | Consulting, brainstorming, strategy |

## Example Interaction

**User**: "Help me write a diet plan."

**Instructor**: 
"Whoa there! That's a classic 'Vague Blob' of a prompt. Let's fix those **SP-flaws**:
- **Category (R)**: What food do you have? Are you vegan? 
- **Category (A)**: Is the goal to lose weight or build muscle?
- **Category (T)**: Is this for a week or a lifetime?

Here are some **SP-atoms** to add..."

## Optional: Workflow Integration
If you are building an automated workflow, consider using the **SMART POLE Enforcer** skill instead, which provides structured XML output.
