---
name: workflow-weaver
description: "Interactive workflow recorder that generates reusable skills. Start with 'start recording: skill-name' and Claude will ask about each action. Captures WebFetch, Read, Bash, Edit, Write, Grep, and Glob operations into self-documenting, production-ready skills."
allowed-tools:
  - bash
  - read
  - write
  - grep
---

# Workflow Weaver

Records your workflow with Claude into reusable skills through interactive questioning and real-time state management. Turn any workflow into a shareable skill that other Claude instances can immediately execute.

## How It Works

1. You say: "start recording: [skill-name]"
2. Work normally with Claude
3. After each significant action, Claude asks if you want to include it
4. You choose: Add as step / Save as reference / Both / Skip
5. When done: "stop recording" generates a complete, usable SKILL.md

The skill monitors your workflow in real-time, maintains recording state in `building.json`, saves reference materials, and generates a fully-documented skill that's immediately executable.

## Recording Commands

**Start recording:**
- "start recording: [skill-name]"
- "start recording skill: [skill-name]"
- "begin recording: [skill-name]"

**During recording:**
- "pause recording" - Stop monitoring temporarily
- "resume recording" - Continue monitoring
- "show current skill" - Preview progress
- "stop recording" or "finish recording" - Generate SKILL.md

## Behavior: Detection and Initialization

When you say "start recording: [skill-name]":

**Step 1: Validate skill name**
- Check if recording already active (only one at a time)
- Validate skill name (alphanumeric, hyphens, underscores)

**Step 2: Create directory structure**
```bash
mkdir -p .claude/skills-in-progress/[skill-name]/references
```

**Step 3: Initialize building.json**
```json
{
  "skill_name": "[skill-name]",
  "started_at": "[ISO-8601 timestamp]",
  "status": "recording",
  "steps": [],
  "references": [],
  "metadata": {
    "total_actions": 0,
    "included_steps": 0,
    "references_count": 0
  }
}
```

**Step 4: Confirm to user**
```
📝 Recording started for skill: **[skill-name]**

I'll ask about each action I take. Work normally!
```

## Behavior: Self-Monitoring After Each Action

CRITICAL RULE: After EVERY significant action YOU (Claude) perform, immediately pause and use AskUserQuestion to ask how to handle it.

### Actions to Monitor

| Action Type | When to Ask | Example |
|------------|-------------|---------|
| **WebFetch** | After fetching any URL | "I just fetched https://docs.example.com" |
| **WebSearch** | After web search | "I just searched for 'authentication patterns'" |
| **Read** | After reading any file | "I just read file /path/to/config.json" |
| **Bash** | After executing command | "I just executed: `npm install`" |
| **Edit** | After modifying file | "I just edited /path/file.js" |
| **Write** | After creating file | "I just created file /path/new-file.ts" |
| **Grep** | After search | "I just searched for pattern: 'export function'" |
| **Glob** | After pattern match | "I just found files matching: **/*.test.js" |

### Question Format

Use AskUserQuestion with this exact structure:

```
Question: "I just [describe action]. How should I handle this?"

Header: "Action"

Options:
  1. Label: "Add as step"
     Description: "Include this action as a numbered step in the skill"

  2. Label: "Save as reference"
     Description: "Save the content to references/ folder"

  3. Label: "Both"
     Description: "Add as step AND save content as reference"

  4. Label: "Skip"
     Description: "Don't include in the skill"

MultiSelect: false
```

### Processing User Response

#### Option 1: "Add as step"

Add to steps array in building.json:
```json
{
  "step_id": [next_number],
  "type": "[webfetch|websearch|read|bash|edit|write|grep|glob]",
  "action": "[Imperative description: 'Fetch docs', 'Read config']",
  "details": {
    "url": "[if webfetch/websearch]",
    "query": "[if websearch]",
    "file": "[if read/edit/write]",
    "command": "[if bash]",
    "pattern": "[if grep/glob]",
    "glob_pattern": "[if glob]"
  },
  "description": "[Why this step matters]",
  "timestamp": "[ISO-8601]"
}
```

Update metadata:
- `metadata.total_actions++`
- `metadata.included_steps++`

Respond to user:
```
✓ Added as step [X]
```

#### Option 2: "Save as reference"

1. **Determine file type and save appropriately:**
   - WebFetch/WebSearch → save as .md with source URL
   - Read → copy original file to references/
   - Bash output → save output to .txt file
   - Other → save appropriately

2. **Use descriptive names:**
   - Good: `aws-deployment-guide.md`, `package-config.json`
   - Bad: `doc1.md`, `file.txt`

3. **Add to references array in building.json:**
```json
{
  "name": "[descriptive-name].[ext]",
  "source": "[original URL or file path]",
  "type": "[web|local|generated]",
  "description": "[What this contains and why]",
  "saved_at": "[ISO-8601]"
}
```

Update metadata:
- `metadata.references_count++`

Respond to user:
```
✓ Saved to references/[filename]
```

#### Option 3: "Both"

Perform BOTH actions above:
1. Add as step
2. Save as reference

Respond to user:
```
✓ Saved to references/[filename]
✓ Added as step [X]
```

#### Option 4: "Skip"

Only update metadata:
- `metadata.total_actions++`

Respond to user:
```
✓ Skipped
```

**After updating:** Always write updated building.json to disk immediately.

## Behavior: Session Control

Monitor for these commands during recording:

**"pause recording":**
- Set `status: "paused"` in building.json
- Stop asking questions about subsequent actions
- Respond: "⏸️ Recording paused. Say 'resume recording' to continue."

**"resume recording":**
- Set `status: "recording"` in building.json
- Resume asking questions about actions
- Respond: "▶️ Recording resumed. I'll continue asking about each action."

**"show current skill":**
Display summary from building.json:
```
📊 Current Skill: [skill-name]

Steps: [X]
References: [Y]
Status: [recording|paused]

Recent steps:
1. [action 1]
2. [action 2]
...
```

**"stop recording" or "finish recording":**
Proceed to generation phase.

## Behavior: Generating Final SKILL.md

When you say "stop recording" or "finish recording":

**Step 1: Read state**
```bash
cat .claude/skills-in-progress/[skill-name]/building.json
```

**Step 2: Validate state**
- Check for empty recording (0 steps)
  - If empty, confirm: "No steps recorded. Cancel and restart?"
  - Allow user to cancel or continue with references only
- Check for 50+ steps
  - Warn: "This skill has 50+ steps. Consider breaking into smaller skills."
  - Ask: "Continue anyway, or refine?"

**Step 3: Generate SKILL.md**

Create file with this structure:

```markdown
---
name: [skill-name]
description: "[One-sentence summary derived from steps]"
allowed-tools:
  - [list unique tool types from steps]
---

# [Skill Name in Title Case]

[2-3 sentence summary of what this skill accomplishes]

## Prerequisites

[Infer from steps any required tools, files, environment setup, permissions, or dependencies]

## Steps

[For each step in building.json, create numbered section:]

### 1. [Step Action as Imperative]

[Step description explaining what this accomplishes and why it matters]

**Action:** [type]
**Details:**
- [key]: [value]
- [key]: [value]

[If reference was saved:]
**Reference:** [references/filename](references/filename)

[Repeat for all steps]

## References

[Only include this section if references array is not empty:]

This skill uses these reference materials:

- **[name]** ([references/name](references/name)) - [description]
- [Repeat for all references]

## Usage

To use this skill:

1. [Describe first step from workflow]
2. [Describe second step]
3. [Continue...]

[Optionally add example usage, variations, or common patterns]

## Notes

- [Any important prerequisites not covered above]
- [Tips for adapting this skill to different scenarios]
- [Known limitations or edge cases]
- [Dependencies on external services or tools]

---

*Generated by workflow-weaver on [current date]*
*Original recording: [skill-name], started [started_at]*
```

**Step 4: Write SKILL.md**
```bash
cat > .claude/skills-in-progress/[skill-name]/SKILL.md << 'EOF'
[generated content]
EOF
```

**Step 5: Move to skills folder**
```bash
mv .claude/skills-in-progress/[skill-name] .claude/skills/[skill-name]
```

**Step 6: Confirm success**
```
✅ Skill generated successfully!

📁 Location: .claude/skills/[skill-name]/
📄 Skill file: SKILL.md
📚 References: [X] files
🔢 Steps: [Y]

Your skill is ready to use!
```

## Best Practices

**Naming conventions:**
- Skill names: `lowercase-with-hyphens` (alphanumeric, hyphens, underscores only)
- References: `descriptive-source.extension` (e.g., `aws-deploy-guide.md`, `local-config.json`)
- Avoid generic names: No `doc1.md`, `file.txt`, `data.json`

**Writing step descriptions:**
- Use imperative voice: "Fetch API docs" not "Fetched docs"
- Include the WHY: "Review auth flow to identify security gaps"
- Be specific: Full commands, exact URLs, complete file paths
- Link to references where relevant

**Reference organization:**
- Keep related content together
- Use source type in filename: `github-api-docs.md`, `local-env-config.json`
- Add descriptions explaining what the reference contains

**Grouping actions:**
- If 3+ similar actions occur consecutively, consider asking once: "I fetched 3 documentation pages. Save all as references?"
- Group related steps in description to help users understand workflow order

## Error Handling

**Corrupted building.json:**
```
⚠️ building.json appears corrupted.

Options:
1. Restart recording (lose progress)
2. Attempt recovery (read last valid state)
3. Cancel recording
```

**Skill name already exists:**
```
⚠️ Skill '[name]' already exists.

Options:
1. Overwrite existing (will be backed up)
2. Use different name
3. Cancel
```

**Recording has 50+ steps:**
```
💡 This skill has 50+ steps. Consider:
1. Continue (may be hard to use)
2. Break into multiple smaller skills
3. Finish and refine later
```

**Missing or unreadable reference:**
- Note in SKILL.md with [MISSING REFERENCE] marker
- Include original source path/URL for manual recovery
- Continue generation without blocking

**Permission denied when writing:**
- Offer to write to alternative location
- Show path where skill would be saved
- Ask permission to retry or save elsewhere

## Edge Cases

**Only one recording at a time:**
- If user tries "start recording" while already recording
- Respond: "Already recording skill: [name]. Say 'stop recording' first."
- Offer to show current skill with "show current skill"

**Empty recording:**
- If 0 steps when stopping
- Confirm: "No steps recorded. Cancel recording and start over?"
- Allow saving with references only if references exist

**Paused too long:**
- If recording paused for 100+ actions performed
- Offer reminder: "Still recording? Say 'stop' to finish or 'resume' to continue."

**Massive recordings:**
- More than 100 steps suggests need to break into multiple skills
- Warn user and suggest splitting workflow

**File system issues:**
- If can't create directories, offer fallback locations
- If can't write building.json, fail early with clear error
- Ensure graceful degradation

## Example Session

```
User: start recording: deploy-to-production

Claude: 📝 Recording started for skill: **deploy-to-production**

I'll ask about each action I take. Work normally!

[Claude performs WebFetch to deployment docs]

Claude: I just fetched https://docs.aws.amazon.com/deploy.
        How should I handle this?

User: Both

Claude: ✓ Saved to references/aws-deploy-docs.md
        ✓ Added as step 1

[Claude reads local config file]

Claude: I just read file config/production.yml.
        How should I handle this?

User: Save as reference

Claude: ✓ Saved to references/production-config.yml

[Claude executes deployment bash commands]

Claude: I just executed: `aws deploy create-deployment`
        How should I handle this?

User: Add as step

Claude: ✓ Added as step 2

[... workflow continues ...]

User: stop recording

Claude: ✅ Skill generated successfully!

📁 Location: .claude/skills/deploy-to-production/
📄 Skill file: SKILL.md
📚 References: 3 files
🔢 Steps: 7

Your skill is ready to use!
```

## Implementation Requirements

1. **State persistence:** Write building.json after EVERY update
   - Atomic writes to prevent corruption
   - Timestamp every operation
   - Validate JSON before writing

2. **Action detection:** Monitor all significant operations
   - WebFetch, WebSearch, Read, Bash, Edit, Write, Grep, Glob
   - Ask immediately after action completes
   - Include relevant details in question

3. **Clear questions:** Make AskUserQuestion options self-explanatory
   - Short descriptions (<50 chars)
   - Clear distinction between options
   - Use consistent formatting

4. **Graceful degradation:** Handle missing tools/permissions
   - Attempt to continue if permission denied
   - Offer fallback options
   - Log issues in references or notes

5. **Consistent formatting:** Follow specified JSON and SKILL.md formats exactly
   - Valid JSON for building.json
   - Markdown with YAML frontmatter for SKILL.md
   - Descriptive filenames for references
   - Consistent timestamps (ISO-8601)

## Success Criteria

- Claude detects "start recording" commands in all formats
- Directory structure created correctly in .claude/skills-in-progress/
- AskUserQuestion appears after each monitored action
- building.json updates correctly with each response
- References saved with descriptive, meaningful names
- Final SKILL.md well-formatted, complete, and immediately executable
- Skill can be used by another Claude instance without modification
- Error cases handled gracefully with helpful messages
- State persists across conversation turns
- References folder organized and accessible

---

*This skill enables self-documenting workflow capture. Use it to create reusable skills from any workflow you build with Claude.*
