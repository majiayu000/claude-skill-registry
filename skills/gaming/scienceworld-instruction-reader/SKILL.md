---
name: scienceworld-instruction-reader
description: This skill reads a recipe or note from the inventory using the 'read' action. It should be triggered after acquiring a recipe or document to extract explicit instructions, ingredient lists, or procedural steps. The skill parses the text content and outputs the key information needed to execute the task, such as required components and their combinations.
---
# Instructions
Use this skill when you have acquired a recipe, note, or any readable document in your inventory and need to understand its contents to proceed with a task.

## Core Action
1.  **Read the Document:** Use the `read OBJ` action on the document in your inventory.
    *   **Example:** `read recipe in inventory`

## Skill Logic
After reading, analyze the text to identify:
*   **Goal:** The final product or objective (e.g., "make salt water").
*   **Required Components:** A list of items or substances needed (e.g., "sodium chloride, water").
*   **Procedural Steps:** Any explicit actions or combinations described (e.g., "mix sodium chloride, water").

## Output Format
Present the extracted information clearly. For example:
