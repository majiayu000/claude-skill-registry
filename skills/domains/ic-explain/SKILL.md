---
name: ic-explain
description: Explain IC10 code behavior in plain English. Use when user pastes IC10 code and asks what it does, how it works, or wants to understand existing Stationeers scripts.
---

# IC10 Code Explanation

Explain IC10 code behavior in clear, understandable language.

## Workflow

1. **Analysis Phase**
   Use Task tool to spawn:
   - `code-analyzer` - Analyze code structure, execution flow, and behavior

2. **Explanation Phase**
   Take the analysis output and create a human-readable explanation

## Instructions

When the user asks to explain IC10 code:

1. Launch `code-analyzer` agent with the provided code

2. From the analysis, create a clear explanation that includes:
   - **Overview**: 1-2 sentences describing what the code does
   - **Device Setup**: What devices need to be connected where
   - **How It Works**: Step-by-step explanation of the logic
   - **Key Behaviors**: What happens under different conditions

3. Keep the explanation accessible:
   - Use plain language, not just code terms
   - Relate to real-world behavior (e.g., "when pressure is too high")
   - Highlight important thresholds and values

4. If issues are found, mention them but don't fix (that's for ic-debug)

## Example Triggers

- "What does this code do?"
- "Explain this script"
- "How does this work?"
- "Can you walk me through this?"
- "I don't understand this code"
