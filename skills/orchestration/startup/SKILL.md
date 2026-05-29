---
name: startup
description: Run full Contextium session startup sequence with all agents
allowed-tools: Bash, Read
---

# Contextium Session Startup

Run the full startup agent pipeline to initialize this session.

## Execution

Run the startup orchestrator:

```bash
./agents/run-startup.sh
```

This executes three agents in sequence:
1. **Initializer** - Verify environment, create state files
2. **Task Determiner** - Analyze state, determine current task
3. **Context Fetcher** - Load minimal relevant context

## After Startup

Review the output and:
- Note the current task (if any)
- Check for any missing tools
- Review loaded context

Logs are available at:
- `/tmp/contextium-startup.log` - Full startup output
- `/tmp/contextium/*.log` - Individual agent logs
