---
name: nl-to-tools-mapper
description: This skill should be used when guiding the OpenAI agent to map natural language user input to appropriate MCP tools, handling phrases like "Add task" → add_task, "List pending" → list_tasks(status="pending"), tool chains, and extracting user email from JWT.
---

# NL to Tools Mapper Skill

This skill provides guidance for mapping natural language input to MCP tools and extracting user context from JWT.

## Purpose

Guide the agent to map user input to tools:
- "Add task" → add_task
- "List pending" → list_tasks(status="pending")
- Handle tool chains (list then delete)
- Extract user email from JWT, respond in natural language

## When to Use

Use this skill when:
- Configuring agent instructions for tool mapping
- Building natural language understanding for task commands
- Implementing multi-step tool chains
- Extracting user identity from authentication

## Capabilities

- **NL Mapping**: Convert natural language to tool calls
- **Intent Recognition**: Identify user intent (add, list, complete, delete, update)
- **Parameter Extraction**: Pull relevant details from user input
- **Tool Chaining**: Execute multiple tools in sequence
- **User Context**: Extract and use JWT claims

## Agent System Prompt

```python
SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their tasks using the available tools.

## Your Capabilities

1. **Adding Tasks**: When user says "add task", "create task", "new task":
   - Use add_task tool
   - Extract title from user input
   - Ask for description if not provided
   - Set priority (default: 1) and due_date if mentioned

2. **Listing Tasks**: When user says "list tasks", "show my tasks":
   - Use list_tasks tool
   - Filter by status if specified ("pending", "completed")
   - Filter by priority if specified

3. **Completing Tasks**: When user says "complete task", "done":
   - Use complete_task tool
   - Extract task ID from context or ask user

4. **Deleting Tasks**: When user says "delete task", "remove task":
   - Use delete_task tool
   - Confirm before deleting

5. **Updating Tasks**: When user says "update task", "edit task":
   - Use update_task tool
   - Ask what fields to update

## Important Rules

- **Always respond in natural language**
- **Always use the user's email when available**
- **Confirm actions before executing destructive operations**
- **If unsure, ask for clarification**

## User Context

Your user is: {user_email}
All tasks you manage belong to this user.
"""
```

## Intent Recognition Pattern

```python
from enum import Enum
from typing import Optional
import re

class Intent(Enum):
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    UPDATE_TASK = "update_task"
    UNKNOWN = "unknown"

INTENT_PATTERNS = {
    Intent.ADD_TASK: [
        r"add\s+(a\s+)?task",
        r"create\s+(a\s+)?task",
        r"new\s+task",
        r"i\s+need\s+to.*task",
        r"remind\s+me\s+to"
    ],
    Intent.LIST_TASKS: [
        r"list\s+(all\s+)?tasks",
        r"show\s+(me\s+)?(my\s+)?tasks",
        r"what('s|\s+is)\s+(my\s+)?tasks",
        r"get\s+(my\s+)?tasks"
    ],
    Intent.COMPLETE_TASK: [
        r"complete\s+task",
        r"mark\s+.*\s+done",
        r".*task\s+is\s+done",
        r"finished?\s+task"
    ],
    Intent.DELETE_TASK: [
        r"delete\s+task",
        r"remove\s+task",
        r"cancel\s+task"
    ],
    Intent.UPDATE_TASK: [
        r"update\s+task",
        r"edit\s+task",
        r"change\s+.*\s+task",
        r"modify\s+task"
    ]
}

def detect_intent(message: str) -> Intent:
    """Detect user intent from natural language."""
    message_lower = message.lower()

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message_lower):
                return intent

    return Intent.UNKNOWN
```

## Parameter Extraction

```python
from typing import Optional, Dict, Any
import re

def extract_task_params(message: str, intent: Intent) -> Dict[str, Any]:
    """Extract tool parameters from user input."""
    params = {}

    if intent == Intent.ADD_TASK:
        # Extract title
        title_match = re.search(
            r"(?:add|create|new)\s+(?:a\s+)?(?:task\s+)?(?:to\s+)?(?:my\s+)?(.+)",
            message,
            re.IGNORECASE
        )
        if title_match:
            params["title"] = title_match.group(1).strip()

        # Extract priority
        priority_match = re.search(r"priority\s*[:=]?\s*(\d+)", message)
        if priority_match:
            params["priority"] = int(priority_match.group(1))

        # Extract due date
        due_match = re.search(
            r"(?:due|by|on)\s+((?:\w+\s+)?\d{1,2}(?:st|nd|rd|th)?(?:\s+\w+)?(?:\s+\d{4})?)",
            message,
            re.IGNORECASE
        )
        if due_match:
            params["due_date"] = due_match.group(1)

    elif intent == Intent.LIST_TASKS:
        if "pending" in message.lower():
            params["status"] = "pending"
        elif "completed" in message.lower():
            params["status"] = "completed"

    return params
```

## Tool Chain Handling

```python
async def handle_tool_chain(
    user_id: str,
    message: str
) -> Dict[str, Any]:
    """Handle complex multi-step operations."""
    intent = detect_intent(message)
    params = extract_task_params(message, intent)

    # Example: "List my pending tasks and delete the first one"
    if "list" in message.lower() and "delete" in message.lower():
        # Step 1: List tasks
        tasks = await list_tasks(user_id=user_id, status="pending")

        if tasks and len(tasks) > 0:
            # Step 2: Delete first task
            first_task_id = tasks[0]["id"]
            result = await delete_task(user_id=user_id, task_id=first_task_id)

            return {
                "response": f"I found {len(tasks)} pending tasks and deleted the first one: '{tasks[0]['title']}'",
                "chain_steps": ["list_tasks", "delete_task"],
                "executed": True
            }

    # Single tool call
    return await route_to_tool(intent, user_id, params)
```

## JWT User Extraction

```python
from typing import Optional
import jwt

async def get_user_from_jwt(authorization: Optional[str]) -> Optional[dict]:
    """Extract user info from JWT token."""
    if not authorization:
        return None

    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        return {
            "user_id": payload.get("userId") or payload.get("sub"),
            "email": payload.get("email"),
            "name": payload.get("name")
        }
    except jwt.InvalidTokenError:
        return None

def format_user_response(user: dict, message: str) -> str:
    """Format response with user context."""
    if user and user.get("email"):
        return f"Sure, {user['email']}! {message}"
    return message
```

## Complete Agent Loop

```python
async def process_user_message(
    user_id: str,
    message: str,
    conversation_history: list
) -> dict:
    """Process user message and generate response."""

    # Get user context
    user = await get_user_from_jwt(request.headers.get("Authorization"))

    # Build system prompt with user context
    system_prompt = SYSTEM_PROMPT.format(user_email=user["email"] if user else "User")

    # Detect intent and extract parameters
    intent = detect_intent(message)
    params = extract_task_params(message, intent)
    params["user_id"] = user_id

    # Route to appropriate tool
    if intent != Intent.UNKNOWN:
        result = await route_to_tool(intent, user_id, params)
        response = format_user_response(user, result["response"])
    else:
        response = format_user_response(
            user,
            "I'm not sure what you mean. Try: 'add task', 'list tasks', 'complete task', or 'delete task'."
        )

    return {
        "response": response,
        "intent": intent.value,
        "params": params
    }
```

## Response Templates

```python
RESPONSE_TEMPLATES = {
    "add_task": "I've added the task '{title}' to your list.",
    "list_tasks": "Here are your {status} tasks:\n{任务列表}",
    "complete_task": "Done! I've marked '{title}' as completed.",
    "delete_task": "I've deleted '{title}' from your tasks.",
    "update_task": "I've updated '{title}' with the new details.",
    "no_tasks": "You don't have any {status} tasks right now."
}
```

## Verification Checklist

- [ ] Intent detection works for common phrases
- [ ] Parameters extracted correctly
- [ ] User email shown in responses
- [ ] Tool chains execute in order
- [ ] Natural language responses
- [ ] Handles unknown intents gracefully
