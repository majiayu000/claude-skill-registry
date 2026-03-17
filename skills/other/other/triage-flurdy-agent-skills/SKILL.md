---
name: triage
description: "Create bead(s) from a user prompt or Jira ticket. Investigates relevance, checks for duplicates, and may split complex requests into multiple focused beads."
allowed-tools: "Read,Bash(bd:*),Grep,Glob,Task"
version: "1.1.0"
author: "flurdy"
---

# Triage - Smart Bead Creation from Prompts

Analyze user requests and create appropriate beads with intelligent investigation.

## When to Use

- User describes a feature, bug, or task to track
- User provides a Jira ticket to convert into bead(s)
- Raw idea needs analysis before becoming actionable work
- Need to check if work is already tracked or duplicated
- Complex request might need to be split into multiple beads

## Usage

```
/triage <description of feature, bug, or task>
/triage ABC-123                          # Create bead(s) from a Jira ticket
/triage ABC-123 break into subtasks      # Jira ticket with additional instructions
```

## What This Skill Does

1. **Investigate Relevance**
   - Search codebase to understand if request is feasible
   - Check if the feature/fix location is obvious
   - Identify any related existing code

2. **Check for Duplicates**
   - Run `bd list --status=open` to see existing work
   - Search bead titles and descriptions for similar items
   - Flag potential duplicates or related beads

3. **Analyze Complexity**
   - Determine if single bead or multiple beads needed
   - Identify natural task boundaries
   - Consider dependencies between potential beads

4. **Create Beads**
   - Create focused, actionable beads
   - Set appropriate type (task/bug/feature)
   - Set reasonable priority (P2 default, adjust based on context)
   - Add dependencies if creating multiple related beads

5. **Report Summary**
   - List newly created beads
   - Show current open beads count
   - Highlight any duplicates or related work found

## Examples

```bash
# Simple feature request
/triage Add dark mode toggle to settings page

# Bug report
/triage Users seeing 500 error when saving profile with emoji in name

# Complex request (may split)
/triage Implement user authentication with OAuth, session management, and password reset

# From a Jira ticket
/triage SP-123

# Jira ticket broken into subtasks
/triage SP-123 break into subtasks
```

## Output Format

After triage, provide:

1. **Investigation Summary**: What was checked, relevance assessment
2. **Duplicate Check**: Any similar existing beads found
3. **Created Beads**: List of new beads with IDs
4. **Open Beads Summary**: Quick stats on current workload

## Implementation

When invoked:

1. Parse the input to determine the source:
   - **Jira ticket**: Input matches pattern `[A-Z]{2,4}-\d+` (e.g., `SP-123`, `ABC-45`)
   - **Free text**: Everything else — a description of a feature, bug, or task

2. **If Jira ticket detected**, look up the ticket:
   ```
   mcp__jira__jira_get with:
     path: /rest/api/3/issue/{ticketNumber}
     jq: "{key: key, summary: fields.summary, type: fields.issuetype.name, description: fields.description}"
   ```

   Map the Jira issue type to bead type:

   | Jira Issue Type | Bead Type |
   |-----------------|-----------|
   | Story           | feature   |
   | Task            | task      |
   | Bug             | bug       |
   | Sub-task        | task      |
   | Improvement     | feature   |
   | Spike           | task      |
   | Technical Debt  | task      |
   | Default         | task      |

   Use the ticket summary and description to populate the bead title and description. Any additional text after the ticket ID in the prompt is treated as extra instructions (e.g., "break into subtasks").

3. Quick codebase investigation:
   ```bash
   # Search for related code/files
   # Check if area of code exists
   ```

4. Check for duplicates:
   ```bash
   bd list --status=open
   bd search "<keywords from description>"
   ```

5. Decide on bead structure:
   - Single focused task → one bead
   - Multi-part work → multiple beads with dependencies
   - Vague request → ask clarifying questions first

6. Create bead(s):
   ```bash
   # For Jira-sourced beads, include --external-ref and --labels
   bd create --title="..." --type=feature|bug|task --priority=2 \
     --description="..." \
     --external-ref "jira-SP-123" \
     --labels "jira"

   # For free-text beads (no Jira reference)
   bd create --title="..." --type=feature|bug|task --priority=2 --description="..."
   ```

7. If multiple beads, set dependencies:
   ```bash
   bd dep add <dependent> <dependency>
   ```

   When creating multiple beads from a single Jira ticket, all beads get the same `--external-ref` and `jira` label so they can be traced back to the source ticket.

8. Report results with summary of open beads

## Priority Guidelines

- **P0-P1**: Critical/urgent (user explicitly says urgent, or blocking issue)
- **P2**: Default for most work (standard feature/task)
- **P3**: Lower priority (nice-to-have, minor improvements)
- **P4**: Backlog (future work, ideas to consider)
