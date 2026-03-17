---
name: update-skill
description: Update an existing skill based on troubleshooting or improvements discovered during usage. Use when user asks to "update a skill", "improve the skill", "fix the skill instructions", or after resolving issues with a skill execution.
---

# Update Skill

## Overview

This skill helps improve existing Claude Code skills by analyzing what went wrong during execution and updating the skill documentation to prevent similar issues in the future. It reviews recent conversation history, identifies problems and solutions, and incorporates learnings into the skill's SKILL.md file.

## When to Use

Invoke this skill when:
- A skill execution failed and you've resolved the issue with the user
- User says "update the skill" or "improve the skill based on what we learned"
- User mentions "fix the skill instructions" or "make the skill better"
- After troubleshooting a skill and finding root causes
- When patterns emerge that should be documented in the skill

## Prerequisites

- An existing skill in `.claude/skills/skill-name/`
- Recent conversation showing the problem and solution
- Clear understanding of what went wrong and how it was fixed

## Instructions

### 1. Identify the Target Skill

Ask the user which skill needs updating if not explicitly mentioned:
- What skill did we just troubleshoot?
- Which skill's documentation needs improvement?

Locate the skill file:
```bash
ls -la .claude/skills/SKILL_NAME/
```

### 2. Review the Current Skill Documentation

Read the existing SKILL.md to understand its current state:
```bash
# Read the current skill
Read(.claude/skills/SKILL_NAME/skill.md)
```

Note:
- Current instructions and their structure
- What the skill is supposed to do
- Known prerequisites and requirements
- Existing troubleshooting sections

### 3. Analyze What Went Wrong

Review the recent conversation to identify:
- **Root Cause**: What was the actual problem?
- **Symptoms**: How did the failure manifest?
- **Context**: What was missing or incorrect?
- **Solution**: What fixed it?
- **Prevention**: How can we avoid this in the future?

Common categories of issues:
- Missing prerequisites (tools, environment variables, dependencies)
- Incomplete instructions (skipped steps, unclear commands)
- Platform-specific requirements not documented
- Error handling gaps (what to do when X fails)
- Assumptions about environment or state

### 4. Determine Update Type

Choose the appropriate update approach:

**A. Add to Prerequisites Section**
- Missing tools or dependencies
- Required environment variables
- Expected directory structure
- Needed permissions or access

**B. Enhance Instructions Section**
- Add missing steps
- Clarify ambiguous steps
- Add platform-specific variations
- Include command examples

**C. Add/Expand Troubleshooting Section**
- Document the specific error encountered
- Explain the root cause
- Provide the solution
- Add diagnostic commands

**D. Update Frontmatter**
- Add missing trigger phrases
- Adjust description for clarity
- Add `delegate: true` if skill is complex

**E. Add Notes/Warnings Section**
- Critical gotchas discovered
- Environment-specific behaviors
- Known limitations

### 5. Update the Skill Documentation

Make targeted edits to the SKILL.md file:

```bash
# Use Edit tool to update specific sections
Edit(
    file_path=".claude/skills/SKILL_NAME/skill.md",
    old_string="[section to update]",
    new_string="[improved section with learnings]"
)
```

**Guidelines for updates:**
- Be specific and actionable
- Include actual commands and examples
- Explain *why* something is needed, not just *what*
- Use clear headings and formatting
- Add code blocks for commands
- Reference specific error messages when relevant

**Example update patterns:**

```markdown
## Prerequisites

[BEFORE]
- Xcode installed
- Device connected

[AFTER]
- Xcode installed with Command Line Tools
- iPhone connected via USB and trusted (unlock device and tap "Trust")
- LD="clang" must be used in xcodebuild to avoid Homebrew linker conflicts
```

```markdown
## Troubleshooting

[NEW SECTION]
### Error: "No devices found"

**Symptom**: xcodebuild fails with "No devices found" despite device being connected

**Cause**: Device is locked, not trusted, or USB restriction mode is enabled

**Solution**:
1. Unlock the iPhone
2. When "Trust This Computer?" appears, tap "Trust"
3. Re-run the skill
```

### 6. Validate the Update

After editing, verify the changes:

```bash
# Read the updated skill to confirm changes
Read(.claude/skills/SKILL_NAME/skill.md)
```

Check:
- YAML frontmatter is still valid
- Formatting is correct (markdown, code blocks)
- Instructions flow logically
- New content integrates smoothly with existing content
- Examples are accurate and testable

### 7. Summarize Changes

Provide a clear summary to the user:
- What was wrong originally
- What sections were updated
- What the skill will now handle better
- Any remaining limitations or known issues

Example summary:
```
Updated ios-deploy-usb skill:
- Added prerequisite about device trust requirement
- Expanded troubleshooting section with "No devices found" error
- Clarified the LD="clang" requirement and why it's needed
- Added example showing how to verify device connection

The skill should now handle the USB trust issue more gracefully in future runs.
```

## Update Patterns

### Pattern 1: Missing Prerequisite

**Scenario**: Skill failed because tool wasn't installed

**Update**:
```markdown
## Prerequisites

- [NEW] Install scrcpy: `brew install scrcpy`
- [NEW] Verify installation: `which scrcpy`
```

### Pattern 2: Incomplete Instructions

**Scenario**: Step was assumed but not documented

**Update**:
```markdown
### 3. Start Port Forwarding

[BEFORE]
Run the deployment script.

[AFTER]
First ensure port forwarding is active:
\`\`\`bash
# Check if port 8081 is forwarded
lsof -ti:8081

# If not running, start it:
pymobiledevice3 usbmux forward 8081 8081 &
\`\`\`

Then run the deployment script.
```

### Pattern 3: Error Without Context

**Scenario**: Cryptic error needed explanation

**Update**:
```markdown
## Troubleshooting

### Error: "clang: error: linker command failed"

This typically means Homebrew's linker is conflicting with Xcode.

**Solution**: Always use `LD="clang"` in xcodebuild commands:
\`\`\`bash
xcodebuild ... LD="clang" build
\`\`\`

This forces use of Apple's linker instead of Homebrew's.
```

### Pattern 4: Platform-Specific Behavior

**Scenario**: Works differently on different setups

**Update**:
```markdown
## Notes

- **macOS Sonoma+**: May require granting terminal permissions in System Settings > Privacy & Security
- **Apple Silicon**: Use `/opt/homebrew/opt/openjdk` for JAVA_HOME
- **Intel Mac**: Use `/usr/local/opt/openjdk` for JAVA_HOME
```

## Best Practices

1. **Be Specific**: Don't just say "ensure device is ready" - list exact steps
2. **Show Don't Tell**: Include actual commands and example output
3. **Explain Why**: Help users understand the reasoning
4. **Test Before Saving**: Verify commands and examples are correct
5. **Preserve Structure**: Keep existing organization unless there's a good reason to change
6. **One Issue Per Update**: Don't combine unrelated changes
7. **Keep It Concise**: Add only what's necessary, avoid verbose explanations

## Common Pitfalls to Avoid

- Don't remove working instructions - enhance them
- Don't duplicate information already in CLAUDE.md
- Don't add generic advice - be specific to this skill
- Don't forget to test YAML frontmatter validity
- Don't make assumptions - document what you verified

## Example: Complete Update Flow

**User**: "The iOS deploy skill failed because my device wasn't trusted. Can we update the skill?"

**Process**:

1. **Identify**: Updating `ios-deploy-usb`
2. **Review**: Read current skill.md
3. **Analyze**: Root cause = device not trusted, solution = trust device and retry
4. **Determine**: Add to Prerequisites + add to Troubleshooting
5. **Update**:
   - Edit Prerequisites to mention device trust
   - Add Troubleshooting section for "Device not trusted" error
6. **Validate**: Read updated file, check YAML
7. **Summarize**: "Updated ios-deploy-usb with device trust requirements and troubleshooting"

## Integration with Other Skills

This skill complements:
- `make-skill` - Creates new skills, this improves existing ones
- `miso` - As miso evolves, update its skill documentation
- All platform skills - Keep them current as issues are discovered

## Notes

- Skills should evolve based on real-world usage
- Document what you learned from failures
- Future Claude instances benefit from your troubleshooting
- Good skill documentation reduces repeated troubleshooting
- Update incrementally - don't wait for perfect knowledge
