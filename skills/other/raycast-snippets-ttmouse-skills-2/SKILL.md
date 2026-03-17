---
name: raycast-snippets
description: Create and manage Raycast Snippets automatically. Use this skill when the user wants to save a prompt, template, or text snippet to their Raycast configuration.
---

# Raycast Snippet Generator

## Capabilities
This skill allows you to generate and save Raycast Snippets directly to the user's configuration file.

## Usage Process

1.  **Analyze Request**:
    - Identify the core content the user wants to save.
    - If the user asks for a "prompt" or "role", generate a high-quality, structured system prompt.
    - If the user asks for a "template", ensure it has placeholders (e.g., `{date}`).

2.  **Generate Metadata**:
    - **Name**: Create a short, descriptive title (e.g., "Python Logger").
    - **Keyword**: Suggest a short abbreviation for quick access (e.g., `!log`, `;py`).
    - **Text**: The actual content.

3.  **Execute Storage**:
    - You have a helper script located at: `~/.claude/skills/raycast-snippets/scripts/manage_snippets.py`
    - Construct the command using the following format:
      ```bash
      python3 ~/.claude/skills/raycast-snippets/scripts/manage_snippets.py --name "Snippet Name" --text "Snippet Content" --keyword "optional_keyword"
      ```
    - **IMPORTANT**: You must use the `Bash` tool to execute this command. Do not just display it.

4.  **Confirm**:
    - Inform the user that the snippet has been saved.
    - Remind them to **Import** the JSON file in Raycast if they haven't set up auto-sync for that specific file (though this script modifies the source file directly, Raycast might need a re-import if it's not the live database).

## Example

**User**: "Save a snippet for a standard git commit message."

**Assistant**:
1. Generates content: `feat: <description>\n\n[optional body]\n\n[optional footer]`
2. Generates command:
   `python3 ~/.claude/skills/raycast-snippets/scripts/manage_snippets.py --name "Git Commit" --text "feat: ..." --keyword ";gc"`
3. Executes command via Bash.
4. Responds: "Saved 'Git Commit' snippet with keyword ';gc'."
