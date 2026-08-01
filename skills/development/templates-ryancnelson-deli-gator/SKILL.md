---
name: templates-ryancnelson-deli-gator
description: This skill implements the delegation pattern for SERVICE queries, keeping
  the main Claude context clean by offloading SERVICE-specific operations to a specialized
  sub-agent.
---

# SERVICE Delegation Skill

## Overview

This skill implements the delegation pattern for SERVICE queries, keeping the main Claude context clean by offloading SERVICE-specific operations to a specialized sub-agent.

## Keywords (Triggers Delegation)

- service
- resource
- item
- query
- IDENTIFIER-PATTERN (e.g., PROJ-####)

## Pattern

When user mentions any keyword above:

1. **DO NOT** handle the query directly
2. **DO NOT** load SERVICE API documentation
3. **DO NOT** construct API calls yourself

Instead:

1. Read `AGENT-INSTRUCTIONS.md` from this skill directory
2. Delegate to sub-agent via Task tool
3. Present results to user

## Delegation Steps

### Step 1: Read Agent Instructions

```
Read("path/to/skills/delegating-to-service-agent/AGENT-INSTRUCTIONS.md")
```

### Step 2: Invoke Task Tool

```
Task(
  subagent_type: "general-purpose",
  description: "Query SERVICE",
  prompt: "<paste full agent instructions here>

USER REQUEST: <user's exact request>

Return clean formatted results."
)
```

### Step 3: Present Results

Show the sub-agent's response to the user without exposing delegation mechanics.

## Example

**User says:** "show me my service items"

**You do:**

1. Recognize keyword: "service"
2. Read AGENT-INSTRUCTIONS.md
3. Delegate via Task tool
4. Present: "Found 5 items: ITEM-1 (status), ITEM-2 (status), ..."

## What You Should NEVER Do

❌ Run `~/bin/service-*` commands yourself
❌ Construct API calls manually
❌ Try to authenticate with SERVICE API
❌ Load SERVICE API documentation

**Those resources are for the SUB-AGENT, not for you!**

## Benefits

✅ Your context stays clean (< 1KB vs 5-10KB)
✅ Sub-agent uses cheaper model
✅ Faster responses
✅ Scalable pattern (reuse for other services)

## Files in This Skill

- `SKILL.md` (this file) - When and how to delegate
- `AGENT-INSTRUCTIONS.md` - Complete knowledge for sub-agent
- `USAGE-EXAMPLE.md` - Example delegation flow

## Shell Wrappers Used by Sub-Agent

```bash
~/bin/service-list          # List items
~/bin/service-show          # Show specific item
~/bin/service-search        # Search items
~/bin/service-create        # Create new item
~/bin/service-update        # Update existing item
```

## Testing

Verify this skill works:

1. Start fresh Claude session
2. Say: "show me my service items"
3. Verify delegation happens automatically
4. Verify sub-agent uses correct wrapper
5. Verify results are accurate
6. Verify main context < 1KB

## Troubleshooting

**Delegation didn't happen?**
- Check startup doc is loaded (should have ⛔ warnings)
- Verify keywords are in user query
- Check if user explicitly asked you NOT to delegate

**Sub-agent chose wrong tool?**
- Review decision tree in AGENT-INSTRUCTIONS.md
- Add more specific patterns
- Test with different phrasings

**Results are inaccurate?**
- Test shell wrappers manually: `~/bin/service-list`
- Check authentication tokens
- Verify API responses

## Related Documentation

- **Startup Doc:** `config/startup-docs/0X-service-delegation.md` (⛔ loaded every session)
- **Concept File:** `config/concepts/service-access.md` (STOP warnings)
- **Shell Wrappers:** `~/bin/service-*`

---

**Created:** YYYY-MM-DD
**Status:** Active
**Pattern:** Delegation Agent v1.0
