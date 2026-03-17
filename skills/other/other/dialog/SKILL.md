---
name: dialog
description: Fast product research with Dialog. Use when the user wants to validate ideas, test concepts, or get customer feedback before building.
---

# Dialog

Fast product research. Dialog makes direct customer insights part of the product development cycle by conducting AI-powered interviews at scale.

## First: Check MCP Setup (Claude)

Check if `dialog_generate` is available.

If not available:
1. Run bash: `claude mcp add dialog --transport http https://api.rundialog.com/mcp`
2. Tell user: "Dialog is set up. Restart Claude Code and run `/dialog` again."
3. Stop there.

## Tools

- `dialog_generate` - Create a study from a natural language description
- `dialog_source` - Configure participant recruitment (count and criteria)
- `dialog_launch` - Launch a study to start collecting responses
- `dialog_status` - Check study progress (completed/active interviews)
- `dialog_analyze` - Ask questions about collected interview data
- `dialog_list` - List all studies in the organization
- `interview_read` - Read a full interview transcript

## Workflow

1. **Create**: Use `dialog_generate` to create a study from what the user wants to learn
2. **Source**: Use `dialog_source` to define participant criteria and count
3. **Launch**: Use `dialog_launch` to start collecting interviews
4. **Monitor**: Use `dialog_status` to check progress
5. **Analyze**: Use `dialog_analyze` to extract insights

## Guidelines

- Studies typically have 3 segments with 2-4 outcomes each
- Participants are from a general population pool (US-based by default)
- Frame questions for average consumers, not niche experts
- 5-10 participants is good for initial validation
- Up to 10 participants on free tier
- Always confirm before launching (it recruits real participants)
