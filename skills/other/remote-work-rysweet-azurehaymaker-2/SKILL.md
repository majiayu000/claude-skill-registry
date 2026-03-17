---
name: remote-work
description: Execute amplihack work on remote Azure VMs with automatic region and resource selection
version: 1.0.0
author: amplihack
activation_keywords:
  - remote
  - remotely
  - Azure VM
  - offload
  - distribute
min_tokens: 800
max_tokens: 2000
---

# Remote Work Skill

Execute amplihack tasks on remote Azure VMs using the `/amplihack:remote` command.

## When to Use

Use this skill when you want to:
- Run long-running tasks on remote VMs
- Leverage more powerful Azure compute
- Distribute work across multiple machines
- Isolate experimental or risky work
- Work in specific Azure regions

## How It Works

When you say things like:
- "Run this remotely"
- "Execute on an eastus VM"
- "Offload this to Azure"
- "Use a remote machine for this"

I will:
1. Extract your task description
2. Detect region preferences (if mentioned)
3. Recommend appropriate VM size based on task complexity
4. Execute `/amplihack:remote` with proper options
5. Guide you on accessing results

## Region Detection

I automatically detect Azure regions from your request:
- "eastus", "east us" → --region eastus
- "westus", "west us" → --region westus
- "centralus" → --region centralus
- (and other Azure regions)

## VM Size Recommendations

Based on your task complexity keywords:

**Small (size s)**: Quick analysis, simple fixes
- Keywords: "quick", "simple", "small", "analyze"
- Size: s (8GB RAM)

**Medium (size m)**: Standard development work
- Keywords: "implement", "feature", "refactor"
- Size: m (64GB RAM) - **default**

**Large (size l)**: Complex refactoring, large codebases
- Keywords: "large", "comprehensive", "complex", "entire codebase"
- Size: l (128GB RAM)

**Extra Large (size xl)**: Intensive compute tasks
- Keywords: "intensive", "heavy", "massive"
- Size: xl (256GB RAM)

## Instructions

When activated:

1. **Parse the user's request** to extract:
   - The task description
   - Region preference (if mentioned)
   - Complexity hints for VM sizing

2. **Determine VM size** based on keywords:
   - Default to "m" unless keywords suggest otherwise
   - Use "s" for simple/quick tasks
   - Use "l" for large/complex tasks
   - Use "xl" for intensive/massive tasks

3. **Construct the command**:
   ```
   /amplihack:remote --region {region} --vm-size {size} auto "{task}"
   ```

   If no region mentioned, omit --region (uses azlin default)

4. **Execute the command** using the SlashCommand tool

5. **Guide the user** on next steps:
   - Results will be in `.claude/runtime/logs/remote/`
   - Git branches in `remote-exec/` namespace
   - How to view logs and integrate changes

## Examples

### Example 1: Simple with Region

**User**: "Run this analysis remotely on an eastus VM"

**Your Response**:
```
I'll execute this analysis on a remote Azure VM in eastus.

Detected:
- Task: analysis work
- Region: eastus
- Size: s (small - suitable for analysis)

Executing: /amplihack:remote --region eastus --vm-size s auto "analysis work"
```

Then use SlashCommand tool to execute it.

### Example 2: Large Refactoring

**User**: "I need to offload this comprehensive refactoring to Azure, use westus2"

**Your Response**:
```
I'll execute this comprehensive refactoring on a remote Azure VM in westus2.

Detected:
- Task: comprehensive refactoring
- Region: westus2
- Size: l (large - for comprehensive work)

Executing: /amplihack:remote --region westus2 --vm-size l auto "comprehensive refactoring"
```

### Example 3: No Region Specified

**User**: "Run this remotely"

**Your Response**:
```
I'll execute this task on a remote Azure VM using your default region.

Detected:
- Task: [extract from context]
- Region: default (from azlin config)
- Size: m (medium - standard)

Executing: /amplihack:remote --vm-size m auto "[task]"
```

## Result Integration

After execution completes, guide the user:

```
Remote execution complete!

Results:
- Logs: .claude/runtime/logs/remote/
- Branches: Check `git branch -r | grep remote-exec`
- Integration: Review changes and merge if ready

To view logs:
  cat .claude/runtime/logs/remote/remote-exec-*.log

To merge remote changes:
  git fetch
  git merge remote-exec/main
```

## Error Handling

If the command fails, explain common issues:

**Secrets Detected**:
"Remote execution blocked - secrets found in repository. Please remove hardcoded secrets and use .env files instead."

**Azlin Not Configured**:
"Azlin is not configured. Please run: `azlin configure`"

**Timeout**:
"Task timed out. The VM has been preserved for inspection. Use `azlin connect <vm-name>` to investigate."

## Best Practices

Remind users:
- Keep git state clean before remote execution
- Use `.env` for secrets (never hardcode)
- Monitor Azure costs with `azlin list`
- Clean up VMs after debugging with `azlin kill <vm-name>`

## Token Budget

- Core instructions: ~1,200 tokens
- Examples and guidance: ~400 tokens
- Total: ~1,600 tokens (well under 2,000 limit)

## See Also

- `/amplihack:remote` - Direct command interface
- Azlin documentation: https://github.com/rysweet/azlin
- Remote execution module: `.claude/tools/amplihack/remote/README.md`
