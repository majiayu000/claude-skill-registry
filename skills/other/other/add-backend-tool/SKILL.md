---
name: add-backend-tool
description: Add a new tool to the backend OpenAI function calling system. Use when user mentions "new tool", "add tool", "backend function", "agent capability", or wants to extend what the AI agent can do.
---

# Add Backend Tool

## Instructions
1. Read `backend/main.py` to understand existing tool patterns:
   - Find the `tools` list with function definitions
   - Review helper functions (read_file, write_file, run_terminal_command, web_search)

2. Create the helper function:
   ```python
   def new_tool_name(param1: str, param2: int = 10) -> str:
       """Docstring explaining the tool."""
       try:
           # Implementation
           return result
       except Exception as e:
           return f"Error: {str(e)}"
   ```

3. Add tool definition to the `tools` list:
   ```python
   {
       "type": "function",
       "function": {
           "name": "new_tool_name",
           "description": "What this tool does and when to use it",
           "parameters": {
               "type": "object",
               "properties": {
                   "param1": {"type": "string", "description": "..."},
                   "param2": {"type": "integer", "description": "..."}
               },
               "required": ["param1"]
           }
       }
   }
   ```

4. Add tool invocation handler in the WebSocket message loop:
   ```python
   elif func_name == "new_tool_name":
       result = new_tool_name(**args)
   ```

5. Update mode restrictions if needed:
   - Agent mode: full access
   - Chat mode: add to allowed list only if read-only/safe

## Examples
- "Add a tool to list directory contents"
- "Create a tool for git operations"
- "Add web scraping capability"

## Guardrails
- Include proper error handling with try/except
- Add timeout for any long-running operations
- Consider security implications (Chat mode restrictions)
- Never hardcode API keys or secrets
- Document the tool's purpose in the function docstring
