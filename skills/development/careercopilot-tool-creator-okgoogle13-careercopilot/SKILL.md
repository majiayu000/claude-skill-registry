---
name: careercopilot-tool-creator
description: "Scaffolds a new Python tool utility in 'src/tools/' for agents to call. Tools are utility functions (web scraping, PDF parsing, database queries) that agents use. Use when creating utilities that agents depend on."
---

# Tool Creator Workflow

1.  Ask for the tool's file name (e.g., `web_search_tool`).
2.  Read the template: `cat .claude/skills/careercopilot-tool-creator/templates/tool.py.tpl`
3.  Replace placeholders like `{{TOOL_NAME}}` with the file name.
4.  Write the new file to `src/tools/{{TOOL_NAME}}.py`.
5.  Advise the user to now add the tool to `src/tools/__init__.py` and to the agent file.
