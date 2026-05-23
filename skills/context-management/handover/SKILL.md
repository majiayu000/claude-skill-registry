---
name: handover
description: Generate a comprehensive markdown summary of our conversation for seamless handoff to another AI agent. Use when ending a session or transferring work.
---

# Conversation Handoff Summary

## Required Output

This command generates and saves a markdown file. Always:

1. Analyze the conversation
2. Create the file using Write tool
3. Save to: `./handoff-summary-YYYYMMDD-HHMMSS.md`

The purpose is file creation, not just information display.

Generate comprehensive summary for AI agent handoff: $ARGUMENTS

## What This Command Does

This command creates a detailed markdown summary of our entire conversation, structured to enable another AI agent to seamlessly continue the work. The summary includes:

- **Context and Background**: Initial problem statement and user requirements
- **Work Completed**: Detailed list of all tasks accomplished
- **Technical Decisions**: Key architectural and implementation choices made
- **Code Changes**: Summary of files modified, created, or refactored
- **Current State**: Where the project stands now
- **Pending Items**: Any unfinished tasks or future considerations
- **Important Notes**: Critical information for continuation

## Output Format

The command generates a markdown file with the following structure:

```markdown
# Project Handoff Summary

Generated: [timestamp]

---

## 📋 Overview

Brief description of the project and main objectives

## 👤 User Context

- User's technical background and preferences
- Specific requirements and constraints
- Communication style preferences

## 🎯 Original Requirements

- Initial problem statement
- Key goals and objectives
- Success criteria

## ✅ Completed Work

### Task 1: [Description]

- What was done
- Why this approach was chosen
- Key code changes
- Files affected

### Task 2: [Description]

...

## 🏗️ Project Structure

Current state of the codebase:

- Directory structure
- Key files and their purposes
- Dependencies added/modified

## 🔧 Technical Decisions

### Decision 1: [Topic]

- Options considered
- Chosen approach
- Rationale

### Decision 2: [Topic]

...

## 💻 Code Examples

Key code snippets demonstrating important implementations

## 🚧 Current State

- What's working
- What's being worked on
- Known issues or limitations

## 📝 Pending Tasks

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## ⚠️ Important Warnings

- Critical information to avoid breaking changes
- Security considerations
- Performance implications

## 🔄 Next Steps

Recommended actions for continuing the work

## 🗂️ Related Files

- File 1: Purpose and recent changes
- File 2: Purpose and recent changes

## 💡 Additional Context

Any other relevant information for smooth continuation
```

## Benefits of This Summary

- **Continuity**: New agent can pick up exactly where we left off
- **Context Preservation**: All important decisions and rationale are documented
- **Efficiency**: Reduces need to re-explain or rediscover information
- **Clarity**: Structured format makes information easy to find
- **Completeness**: Captures both technical and conversational context

## Usage Examples

**Basic usage:**

```
/handover
```

**With specific focus:**

```
/handover focusing on authentication implementation
```

**For specific date range:**

```
/handover for work done today
```

## Key Sections Explained

### User Context

Captures communication preferences, technical level, and any specific requirements mentioned during conversation

### Technical Decisions

Documents why certain approaches were chosen over others, preventing future agents from undoing intentional choices

### Code Examples

Includes actual code snippets for complex implementations, ensuring the next agent understands the implementation style

### Important Warnings

Highlights any critical information that could cause issues if not known (e.g., "Don't modify X because it will break Y")

### Related Files

Lists all files that were created or modified, with brief descriptions of their purpose and changes

## Notes for the Next Agent

The summary will include:

- Conversation tone and style preferences
- Any tools or commands created during the session
- User's stated preferences (e.g., no emojis, no conventional commit prefixes)
- Current working directory and environment setup
- Any external dependencies or API keys mentioned

## Output Options

The command will:

- Generate a comprehensive markdown file
- Save it as `handoff-summary-[timestamp].md`
- Display the content for review
- Optionally include conversation transcript excerpts for critical decisions

This ensures perfect continuity when switching between AI agents or resuming work after a break.
