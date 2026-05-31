---
name: reflection
description: 'Analyze development sessions, capture learnings, and improve Claude Code instructions. Use when the user wants to reflect on a session, improve CLAUDE.md, extract learnings, or optimize AI-human collaboration. Supports two modes: quick (default) focuses on CLAUDE.md improvements, deep mode performs comprehensive session analysis with learning capture.'
---

# Reflection

Analyze the current session and improve Claude Code instructions. Operates in two modes based on user input.

## Mode Selection

- **Quick mode** (default): Triggered by `/reflection` or `/reflection quick`. Focuses on analyzing chat history to identify and implement improvements to CLAUDE.md instructions.
- **Deep mode**: Triggered by `/reflection deep` or `/reflection comprehensive`. Performs a full session analysis covering problems solved, patterns established, user preferences, system understanding, and knowledge gaps, then updates CLAUDE.md accordingly.

Determine the mode from the user's input. If no mode is specified, use Quick mode. If the user says "deep", "comprehensive", or "harder", use Deep mode.

---

## Quick Mode: CLAUDE.md Improvement

### 1. Analysis Phase

Review the chat history in the context window, then read the current CLAUDE.md file in the repository root.

Analyze both to identify areas for improvement:

- Inconsistencies in Claude's responses
- Misunderstandings of user requests
- Areas where Claude could provide more detailed or accurate information
- Opportunities to enhance handling of specific query types or tasks
- Missing instructions that would have prevented mistakes made during the session

### 2. Analysis Documentation

Use TodoWrite to track each identified improvement area and create a structured approach for changes.

### 3. Interaction Phase

Present findings and improvement ideas to the user. For each suggestion:

1. Explain the current issue identified
2. Propose a specific change or addition to the instructions
3. Describe how this change would improve Claude's performance

Wait for feedback on each suggestion before proceeding. If the user approves a change, move to implementation. If not, refine the suggestion or move on.

### 4. Implementation Phase

For each approved change:

1. Use the Edit tool to modify the CLAUDE.md file
2. State the section being modified
3. Present the new or modified text
4. Explain how this change addresses the identified issue

### 5. Output Format

Present the final output in this structure:

```
<analysis>
[Issues identified and potential improvements]
</analysis>

<improvements>
[For each approved improvement:
1. Section being modified
2. New or modified instruction text
3. Explanation of how this addresses the identified issue]
</improvements>

<final_instructions>
[Complete updated set of instructions incorporating all approved changes]
</final_instructions>
```

Commit changes using git after successful implementation.

---

## Deep Mode: Comprehensive Session Analysis

### 1. Session Analysis Phase

Review the entire conversation history and identify:

#### Problems and Solutions
- What problems were encountered?
- Initial symptoms reported by the user
- Root causes discovered
- Solutions implemented
- Key insights learned

#### Code Patterns and Architecture
- Design decisions made
- Architecture choices
- Code relationships discovered
- Integration points identified

#### User Preferences and Workflow
- Communication style
- Decision-making patterns
- Quality standards
- Workflow preferences
- Direct quotes that reveal preferences

#### System Understanding
- Component interactions
- Critical paths and dependencies
- Failure modes and recovery
- Performance considerations

#### Knowledge Gaps and Improvements
- Misunderstandings that occurred
- Information that was missing
- Better approaches discovered
- Future considerations

### 2. Reflection Output Phase

Present a structured summary covering:

- **Session overview**: High-level summary of what was accomplished
- **Problems solved**: Each problem with root cause and solution
- **Patterns established**: Design and code patterns worth remembering
- **User preferences**: Workflow and communication preferences observed
- **System relationships**: Component interactions and dependencies learned
- **Knowledge updates**: New understanding gained about the codebase or domain
- **Commands and tools**: Any tools or commands that were particularly useful or problematic
- **Future improvements**: Suggestions for next steps or optimizations
- **Collaboration insights**: What worked well and what could improve in the AI-human interaction

### 3. Action Items

After presenting the analysis, propose concrete actions:

1. **Update CLAUDE.md** with specific sections reflecting learnings
2. **Add comments** to specific files where understanding was gained
3. **Create documentation** for specific topics if needed
4. **Test** anything that needs verification

Use TodoWrite to track these action items. Wait for user approval before implementing changes.

### 4. Implementation

For each approved action, implement the change and commit using git.

---

## Best Practices

- Always read the current CLAUDE.md file before proposing changes
- Use TodoWrite to track analysis progress and implementation tasks
- Test proposed changes by considering edge cases and common scenarios
- Ensure all modifications maintain consistency with existing patterns
- Be thorough in analysis, clear in explanations, and precise in implementations
- Commit changes using git after successful implementation

## Your Task

Reflect on the current session. Determine the mode from the user's input — default to Quick mode if no mode is specified.
