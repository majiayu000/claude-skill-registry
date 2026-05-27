---
name: cfn-expert-update
description: Update CFN system expert agent with relevant git commits and project changes
version: 1.0.0
tags: [expert, update, git, knowledge]
status: production
---

# CFN Expert Update Skill

## Purpose

Updates the CFN system expert agent's knowledge base with relevant git commits and project changes. This skill analyzes recent commits, determines their relevance to the CFN system, and injects new knowledge into the expert agent to keep it up-to-date with the latest system changes.

## Usage

```bash
# Basic usage (scan last 10 commits or since last update)
bash .claude/skills/cfn-expert-update/update-expert.sh

# Dry run to see what would be updated
bash .claude/skills/cfn-expert-update/update-expert.sh --dry-run

# Scan commits since specific hash
bash .claude/skills/cfn-expert-update/update-expert.sh --since=<commit_hash>

# Force update even if no changes detected
bash .claude/skills/cfn-expert-update/update-expert.sh --force

# Combine options
bash .claude/skills/cfn-expert-update/update-expert.sh --dry-run --since=HEAD~5 --force
```

## Options

- `--dry-run`: Show what would be updated without making changes
- `--since=<hash>`: Update from specific commit instead of last tracked
- `--force`: Force update even if no new commits detected

## Relevance Scoring

The skill classifies commits into three relevance levels:

### High Priority (always included)
- Changes to `CLAUDE.md`
- CFN loop related files
- CFN commands and workflows
- Core system architecture changes

### Medium Priority (usually included)
- CFN skill updates
- Agent coordination changes
- Redis coordination patterns
- Cost optimization features
- Adaptive context changes
- Consensus mechanisms
- Swarm intelligence features

### Low Priority (sometimes included)
- CFN agent updates
- Performance improvements
- Debugging tools
- Troubleshooting guides

## Update Process

1. **Commit Analysis**: Scans git commits since last update or specified hash
2. **Relevance Detection**: Classifies each commit based on file patterns and messages
3. **Knowledge Extraction**: Generates structured knowledge blocks for relevant commits
4. **Backup Creation**: Creates timestamped backup of current expert agent
5. **Knowledge Injection**: Inserts new knowledge before the closing `---` in the agent file
6. **State Tracking**: Updates last processed commit hash

## Output Structure

Each relevant commit generates a knowledge block like:

```
# HIGH PRIORITY UPDATE
Commit: <hash>
Message: <commit message>

## System Changes
<diff summary>

## Impact
This commit contains critical system updates that affect CFN Loop methodology...
```

## Requirements

- Git repository with commits
- Bash shell (compatible with bash 4.0+)
- Required commands: git, date, grep, head, tail, mktemp, mv, cp, wc
- CFN system expert agent at `.claude/agents/custom/cfn-system-expert.md`

## Troubleshooting

### "Not in a git repository"
Ensure you're running the script from within a git repository.

### "CFN system expert agent not found"
Check that the expert agent exists at the expected location. The skill looks for:
```
.claude/agents/custom/cfn-system-expert.md
```

### "Missing required commands"
Install the missing commands listed in the error message.

### Script exits with no output
- Check if using `--dry-run` - output goes to stderr in dry run mode
- Verify commit range has commits: `git log --oneline HEAD~5..HEAD`
- Try with `--force` flag to override no-change detection

### Permission errors
The skill creates directories and files in `.claude/state` and `.claude/backups`. Ensure you have write permissions.

## Integration with CFN Workflow

This skill is typically run:
- After major feature implementations
- As part of release preparation
- When the CFN system expert seems outdated
- Periodically to keep knowledge fresh

The skill maintains state in `.claude/state/cfn-expert-last-commit` to track the last processed commit, avoiding duplicate updates.

## Examples

### Check for updates without applying them
```bash
bash .claude/skills/cfn-expert-update/update-expert.sh --dry-run
```

### Update from a specific commit
```bash
bash .claude/skills/cfn-expert-update/update-expert.sh --since=abc123
```

### Force full rescan of recent history
```bash
bash .claude/skills/cfn-expert-update/update-expert.sh --force
```

### See what would be updated from last 5 commits
```bash
bash .claude/skills/cfn-expert-update/update-expert.sh --dry-run --since=HEAD~5
```