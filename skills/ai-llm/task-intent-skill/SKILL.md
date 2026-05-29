---
name: task-intent-skill
description: AI reasoning skill for detecting user intents from natural language, mapping to MCP tools, handling multi-step workflows, and generating friendly confirmations for Todo task operations.
---

# Task Intent Skill

Use this skill when implementing natural language understanding and intent detection for Todo chatbot conversations.

## When to Use

- Parsing natural language commands for task operations
- Detecting user intent (add, list, update, delete, complete)
- Mapping intents to MCP tools
- Handling multi-step reasoning workflows
- Generating confirmation messages
- Managing ambiguous or error cases

## Intent Classification

### Primary Intents

| Intent | Triggers | MCP Tool | Example |
|--------|----------|----------|---------|
| **add_task** | add, create, new, remember, remind | `add_task` | "Add a task to buy groceries" |
| **list_tasks** | show, list, view, what, display | `list_tasks` | "Show me all my tasks" |
| **complete_task** | done, complete, finish, mark | `complete_task` | "Mark task 3 as complete" |
| **delete_task** | delete, remove, cancel, drop | `delete_task` | "Delete the meeting task" |
| **update_task** | change, update, edit, rename | `update_task` | "Change task 1 to 'Call mom tonight'" |
| **add_tag** | tag, label, categorize | `add_task` (with tags) | "Add work tag to task 5" |
| **list_by_tag** | tagged, labeled, category | `list_tasks` (with tag filter) | "Show me work tasks" |
| **sort_tasks** | sort, order, arrange | `list_tasks` (with sort param) | "Show tasks by priority" |

## Intent Detection Logic

```python
# app/agents/intent_detector.py
import re
from typing import Tuple, Optional

class IntentDetector:
    """Detect user intent from natural language."""

    # Intent patterns
    ADD_PATTERNS = [
        r'\b(add|create|new|remember|remind)\b',
        r'\bneed to\b',
        r'\bshould\b',
    ]

    LIST_PATTERNS = [
        r'\b(show|list|view|display|see)\b',
        r'\bwhat.*tasks?\b',
        r'\bmy tasks?\b',
        r"what's (pending|completed|left)",
    ]

    COMPLETE_PATTERNS = [
        r'\b(done|complete|finish|mark|finished)\b',
        r'\bmark.*complete\b',
        r'\bmark.*done\b',
    ]

    DELETE_PATTERNS = [
        r'\b(delete|remove|cancel|drop|clear)\b',
        r'\bget rid of\b',
    ]

    UPDATE_PATTERNS = [
        r'\b(change|update|edit|rename|modify)\b',
        r'\bchange.*to\b',
    ]

    TAG_PATTERNS = [
        r'\b(tag|label|categorize)\b',
        r'\btagged (as|with)\b',
        r'\badd.*tag\b',
    ]

    SORT_PATTERNS = [
        r'\b(sort|order|arrange)\b',
        r'\bby (priority|date|title|deadline)\b',
        r'\bsorted by\b',
    ]

    def detect(self, message: str) -> Tuple[str, dict]:
        """
        Detect intent and extract parameters.

        Returns: (intent_name, parameters)
        """
        message_lower = message.lower()

        # Check each intent pattern
        if self._matches(message_lower, self.ADD_PATTERNS):
            return self._extract_add_intent(message)

        elif self._matches(message_lower, self.COMPLETE_PATTERNS):
            return self._extract_complete_intent(message)

        elif self._matches(message_lower, self.DELETE_PATTERNS):
            return self._extract_delete_intent(message)

        elif self._matches(message_lower, self.UPDATE_PATTERNS):
            return self._extract_update_intent(message)

        elif self._matches(message_lower, self.LIST_PATTERNS):
            return self._extract_list_intent(message)

        elif self._matches(message_lower, self.TAG_PATTERNS):
            return self._extract_tag_intent(message)

        elif self._matches(message_lower, self.SORT_PATTERNS):
            return self._extract_sort_intent(message)

        else:
            # Default: treat as general query
            return ("general", {"query": message})

    def _matches(self, text: str, patterns: list) -> bool:
        """Check if text matches any pattern."""
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)

    def _extract_add_intent(self, message: str) -> Tuple[str, dict]:
        """Extract task title and description for add intent."""
        # Remove trigger words
        clean = re.sub(
            r'\b(add|create|new|remember|remind|task|to|a)\b',
            '',
            message,
            flags=re.IGNORECASE
        ).strip()

        # Split on common separators
        parts = re.split(r'(?:with|:|–|—)', clean, maxsplit=1)
        title = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else None

        return ("add_task", {
            "title": title,
            "description": description
        })

    def _extract_complete_intent(self, message: str) -> Tuple[str, dict]:
        """Extract task_id for complete intent."""
        # Look for task ID number
        task_id_match = re.search(r'\btask\s*(\d+)\b', message, re.IGNORECASE)
        if task_id_match:
            return ("complete_task", {"task_id": int(task_id_match.group(1))})

        # Look for standalone number
        number_match = re.search(r'\b(\d+)\b', message)
        if number_match:
            return ("complete_task", {"task_id": int(number_match.group(1))})

        # No ID found - need to ask or search by title
        return ("complete_task", {"query": message})

    def _extract_delete_intent(self, message: str) -> Tuple[str, dict]:
        """Extract task_id or query for delete intent."""
        # Look for task ID
        task_id_match = re.search(r'\btask\s*(\d+)\b', message, re.IGNORECASE)
        if task_id_match:
            return ("delete_task", {"task_id": int(task_id_match.group(1))})

        # Extract task title/description for search
        clean = re.sub(
            r'\b(delete|remove|cancel|task|the)\b',
            '',
            message,
            flags=re.IGNORECASE
        ).strip()

        return ("delete_task", {"query": clean})

    def _extract_update_intent(self, message: str) -> Tuple[str, dict]:
        """Extract task_id and new title for update intent."""
        # Look for "task X to/change to Y" pattern
        match = re.search(
            r'\btask\s*(\d+).*(?:to|into|as)\s+["\']?(.+?)["\']?$',
            message,
            re.IGNORECASE
        )
        if match:
            return ("update_task", {
                "task_id": int(match.group(1)),
                "new_title": match.group(2).strip()
            })

        # Fallback: needs clarification
        return ("update_task", {"query": message})

    def _extract_list_intent(self, message: str) -> Tuple[str, dict]:
        """Extract filter for list intent."""
        message_lower = message.lower()
        params = {"status": "all"}

        # Status filter
        if any(word in message_lower for word in ["pending", "incomplete", "todo"]):
            params["status"] = "pending"
        elif any(word in message_lower for word in ["completed", "done", "finished"]):
            params["status"] = "completed"

        # Priority filter
        if "high priority" in message_lower or "urgent" in message_lower:
            params["priority"] = "high"
        elif "low priority" in message_lower:
            params["priority"] = "low"
        elif "medium priority" in message_lower:
            params["priority"] = "medium"

        # Tag/category filter
        tag_match = re.search(r'\b(work|personal|home|shopping|urgent)\b', message_lower)
        if tag_match:
            params["tag_query"] = tag_match.group(1)

        # Sort detection
        if "by priority" in message_lower or "sorted by priority" in message_lower:
            params["sort_by"] = "priority"
        elif "by date" in message_lower or "by deadline" in message_lower:
            params["sort_by"] = "due_date"
        elif "by title" in message_lower or "alphabetically" in message_lower:
            params["sort_by"] = "title"

        return ("list_tasks", params)

    def _extract_tag_intent(self, message: str) -> Tuple[str, dict]:
        """Extract tag operation from message."""
        # Pattern: "Add work tag to task 5"
        task_match = re.search(r'\btask\s*(\d+)\b', message, re.IGNORECASE)
        tag_match = re.search(r'\b(work|personal|home|shopping|urgent)\b', message.lower())

        if task_match and tag_match:
            return ("add_tag", {
                "task_id": int(task_match.group(1)),
                "tag_name": tag_match.group(1)
            })

        # Pattern: "Tag this as work"
        if tag_match:
            return ("add_tag", {
                "tag_name": tag_match.group(1),
                "query": message
            })

        return ("add_tag", {"query": message})

    def _extract_sort_intent(self, message: str) -> Tuple[str, dict]:
        """Extract sort preference from message."""
        message_lower = message.lower()

        if "priority" in message_lower:
            return ("list_tasks", {"sort_by": "priority", "status": "all"})
        elif "date" in message_lower or "deadline" in message_lower:
            return ("list_tasks", {"sort_by": "due_date", "status": "all"})
        elif "title" in message_lower or "alphabetically" in message_lower:
            return ("list_tasks", {"sort_by": "title", "status": "all"})
        elif "created" in message_lower or "newest" in message_lower:
            return ("list_tasks", {"sort_by": "created_at", "status": "all"})

        return ("list_tasks", {"sort_by": "priority", "status": "all"})
```

## Multi-Step Reasoning

```python
# app/agents/reasoning_engine.py
from typing import List, Dict
from app.agents.intent_detector import IntentDetector
from app.mcp.tools import MCPTools

class ReasoningEngine:
    """Handle multi-step reasoning workflows."""

    def __init__(self, mcp_tools: MCPTools, user_id: str):
        self.detector = IntentDetector()
        self.mcp = mcp_tools
        self.user_id = user_id

    async def process(self, message: str) -> Dict:
        """
        Process message through reasoning workflow.

        Returns: {
            "response": str,
            "tool_calls": List[Dict]
        }
        """
        intent, params = self.detector.detect(message)

        if intent == "add_task":
            return await self._handle_add_task(params)

        elif intent == "list_tasks":
            return await self._handle_list_tasks(params)

        elif intent == "complete_task":
            return await self._handle_complete_task(params)

        elif intent == "delete_task":
            return await self._handle_delete_task(params)

        elif intent == "update_task":
            return await self._handle_update_task(params)

        else:
            return {
                "response": "I can help you add, list, complete, update, or delete tasks. What would you like to do?",
                "tool_calls": []
            }

    async def _handle_add_task(self, params: dict) -> dict:
        """Handle add task intent."""
        result = await self.mcp.add_task(
            user_id=self.user_id,
            title=params["title"],
            description=params.get("description")
        )

        return {
            "response": f"✓ Created task: {params['title']}",
            "tool_calls": [{"tool": "add_task", "params": params, "result": result}]
        }

    async def _handle_list_tasks(self, params: dict) -> dict:
        """Handle list tasks intent."""
        result = await self.mcp.list_tasks(
            user_id=self.user_id,
            status=params.get("status", "all")
        )

        tasks = result.get("tasks", [])
        if not tasks:
            response = "You have no tasks."
        else:
            lines = [f"Your tasks ({params.get('status', 'all')}):"]
            for task in tasks:
                status = "✓" if task["completed"] else "○"
                lines.append(f"{status} [{task['id']}] {task['title']}")
            response = "\n".join(lines)

        return {
            "response": response,
            "tool_calls": [{"tool": "list_tasks", "params": params, "result": result}]
        }

    async def _handle_complete_task(self, params: dict) -> dict:
        """Handle complete task intent."""
        # Direct task ID provided
        if "task_id" in params:
            result = await self.mcp.complete_task(
                user_id=self.user_id,
                task_id=params["task_id"]
            )

            return {
                "response": f"✓ Marked task {params['task_id']} as complete!",
                "tool_calls": [{"tool": "complete_task", "params": params, "result": result}]
            }

        # Need to search by query
        else:
            # First list tasks to find match
            list_result = await self.mcp.list_tasks(
                user_id=self.user_id,
                status="pending"
            )

            # Search for matching task
            query = params.get("query", "").lower()
            matching = [
                t for t in list_result.get("tasks", [])
                if query in t["title"].lower()
            ]

            if not matching:
                return {
                    "response": f"I couldn't find any task matching '{query}'.",
                    "tool_calls": []
                }

            if len(matching) > 1:
                lines = ["Multiple tasks match. Which one?"]
                for t in matching:
                    lines.append(f"[{t['id']}] {t['title']}")
                return {
                    "response": "\n".join(lines),
                    "tool_calls": []
                }

            # Single match - complete it
            task = matching[0]
            result = await self.mcp.complete_task(
                user_id=self.user_id,
                task_id=task["id"]
            )

            return {
                "response": f"✓ Marked '{task['title']}' as complete!",
                "tool_calls": [
                    {"tool": "list_tasks", "params": {"status": "pending"}, "result": list_result},
                    {"tool": "complete_task", "params": {"task_id": task["id"]}, "result": result}
                ]
            }

    async def _handle_delete_task(self, params: dict) -> dict:
        """Handle delete task intent (multi-step like complete)."""
        # Similar to complete_task logic
        # ... (implementation follows same pattern)
        pass

    async def _handle_update_task(self, params: dict) -> dict:
        """Handle update task intent."""
        # Similar to complete_task logic
        # ... (implementation follows same pattern)
        pass
```

## Confirmation Messages

```python
# app/agents/confirmations.py

CONFIRMATIONS = {
    "add_task": "✓ Created task: {title}",
    "complete_task": "✓ Marked task {task_id} as complete!",
    "delete_task": "✓ Deleted task: {title}",
    "update_task": "✓ Updated task {task_id}: {new_title}",
    "list_tasks": "Showing {count} tasks",
}

ERROR_MESSAGES = {
    "task_not_found": "I couldn't find task {task_id}.",
    "no_tasks": "You have no tasks yet. Try adding one!",
    "ambiguous": "Multiple tasks match '{query}'. Please be more specific or use task ID.",
    "missing_title": "Please provide a task title.",
    "invalid_input": "I didn't understand that. Try: 'Add a task to buy groceries'",
}

def format_confirmation(intent: str, **kwargs) -> str:
    """Format confirmation message."""
    template = CONFIRMATIONS.get(intent, "Done!")
    return template.format(**kwargs)

def format_error(error_type: str, **kwargs) -> str:
    """Format error message."""
    template = ERROR_MESSAGES.get(error_type, "Something went wrong.")
    return template.format(**kwargs)
```

## Example Natural Language Commands

### Basic Commands
| User Input | Intent | Parameters | Response |
|------------|--------|------------|----------|
| "Add a task to buy groceries" | add_task | title="buy groceries" | ✓ Created task: buy groceries |
| "Show me all my tasks" | list_tasks | status="all" | Your tasks (all): ... |
| "Mark task 3 as complete" | complete_task | task_id=3 | ✓ Marked task 3 as complete! |
| "Delete the meeting task" | delete_task | query="meeting" | (multi-step: list → match → delete) |
| "What's pending?" | list_tasks | status="pending" | Your tasks (pending): ... |
| "Change task 1 to Call mom" | update_task | task_id=1, new_title="Call mom" | ✓ Updated task 1: Call mom |

### Intermediate Commands (Tags & Sort)
| User Input | Intent | Parameters | Response |
|------------|--------|------------|----------|
| "Add work tag to task 5" | add_tag | task_id=5, tag_name="work" | ✓ Tagged task 5 as 'work' |
| "Show me work tasks" | list_tasks | tag_query="work" | Your work tasks: ... |
| "Show high priority tasks" | list_tasks | priority="high" | High priority tasks: ... |
| "Show tasks by priority" | list_tasks | sort_by="priority" | Tasks sorted by priority: ... |
| "Sort tasks by deadline" | list_tasks | sort_by="due_date" | Tasks sorted by deadline: ... |
| "Show pending work tasks" | list_tasks | status="pending", tag_query="work" | Pending work tasks: ... |

## Edge Case Handling

```python
# Ambiguous input
User: "Complete the task"
Response: "Which task? Please specify task ID or title."

# No matches
User: "Delete xyz task"
Response: "I couldn't find any task matching 'xyz'."

# Multiple matches
User: "Complete call task"
Response: "Multiple tasks match. Which one?\n[1] Call mom\n[2] Call dentist"

# Invalid task ID
User: "Complete task 999"
Response: "I couldn't find task 999."

# Missing parameters
User: "Add a task"
Response: "What should the task be about?"
```

## Best Practices

1. **Normalize Input**: Lowercase, trim whitespace, handle punctuation
2. **Handle Synonyms**: Map variations to same intent
3. **Multi-Step Search**: List → filter → confirm before destructive actions
4. **Clear Confirmations**: Use ✓ checkmarks and specific details
5. **Friendly Errors**: Explain what went wrong and suggest next step
6. **Contextual Understanding**: Use conversation history when available
7. **Graceful Fallback**: If uncertain, ask clarifying questions

## Integration Points

| Component | Connection |
|-----------|------------|
| **ChatKit UI** | Sends user message |
| **TodoChatAgent** | Invokes reasoning engine |
| **MCP Tools** | Executes actual operations |
| **FastAPI** | Returns structured response |

---

**Production Standard**: This skill ensures accurate intent detection, smooth multi-step workflows, and a friendly conversational experience with clear confirmations and error handling.
