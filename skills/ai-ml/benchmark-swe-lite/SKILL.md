---
name: swe-bench-lite
description: Quick-start command to run SWE-bench Lite evaluation with sensible defaults.
---

# Instructions
This skill provides a streamlined way to run the SWE-bench Lite benchmark with pre-configured defaults.

## What This Skill Does

This skill runs a quick SWE-bench Lite evaluation with:
- 5 sample tasks (configurable)
- Verbose output for visibility
- Results saved to `results.json`
- Report saved to `report.md`

## Prerequisites Check

Before running, verify:

1. **Docker is running:**
   ```bash
   docker ps
   ```

2. **API key is set:**
   ```bash
   echo $ANTHROPIC_API_KEY
   ```

3. **Config file exists:**
   - Check for `mcpbr.yaml` in the current directory
   - If missing, run `mcpbr init` to generate it

## Default Command

The default command for SWE-bench Lite:

```bash
mcpbr run -c mcpbr.yaml --dataset SWE-bench/SWE-bench_Lite -n 5 -v -o results.json -r report.md
```

## Customization Options

Users can customize the run by modifying:

- **Sample size:** Change `-n 5` to any number (or remove for full dataset)
- **Config file:** Change `-c mcpbr.yaml` to point to a different config
- **Verbosity:** Use `-vv` for very verbose output
- **Output files:** Change `results.json` and `report.md` to different paths

## Example Variations

### Minimal quick test (1 task)
```bash
mcpbr run -c mcpbr.yaml -n 1 -v
```

### Full evaluation (all ~300 tasks)
```bash
mcpbr run -c mcpbr.yaml --dataset SWE-bench/SWE-bench_Lite -v -o results.json
```

### MCP-only (skip baseline)
```bash
mcpbr run -c mcpbr.yaml -n 5 -M -v -o results.json
```

### Specific tasks
```bash
mcpbr run -c mcpbr.yaml -t astropy__astropy-12907 -t django__django-11099 -v
```

## Expected Runtime & Cost

For 5 tasks with default settings:
- **Runtime:** 15-30 minutes (depends on task complexity)
- **Cost:** $2-5 (depends on task complexity and model used)

## What to Do If It Fails

1. **Docker not running:** Start Docker Desktop
2. **API key missing:** Set with `export ANTHROPIC_API_KEY="sk-ant-..."`
3. **Config missing:** Run `mcpbr init` to generate default config
4. **Config invalid:** Check that `{workdir}` placeholder is in the `args` array
5. **MCP server fails:** Test the server command independently

## After the Run

Once complete, you'll have:
- **results.json:** Full evaluation data with metrics, token usage, and per-task results
- **report.md:** Human-readable summary with resolution rates and comparisons
- **Console output:** Real-time progress and summary table

Review the results to see how your MCP server performed compared to the baseline!

## Pro Tips

- Start with `-n 1` to verify everything works before running larger evaluations
- Use `--log-dir logs/` to save detailed per-task logs for debugging
- Compare multiple runs by changing the MCP server config between runs
- Use `--baseline-results baseline.json` to detect regressions between versions
