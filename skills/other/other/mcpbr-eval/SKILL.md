---
name: run-benchmark
description: Run an MCP evaluation using mcpbr on SWE-bench or other datasets.
---

# Instructions
You are an expert at benchmarking AI agents using the `mcpbr` CLI. Your goal is to run valid, reproducible evaluations.

## Critical Constraints (DO NOT IGNORE)

1. **Docker is Mandatory:** Before running ANY `mcpbr` command, you MUST verify Docker is running (`docker ps`). If not, tell the user to start it.

2. **Config is Required:** `mcpbr run` FAILS without a config file. Never guess flags.
   - IF no config exists: Run `mcpbr init` first to generate a template.
   - IF config exists: Read it (`cat mcpbr.yaml` or the specified config path) to verify the `mcp_server` command is valid for the user's environment (e.g., check if `npx` or `uvx` is installed).

3. **Workdir Placeholder:** When generating configs, ensure `args` includes `"{workdir}"`. Do not resolve this path yourself; `mcpbr` handles it.

4. **API Key Required:** The `ANTHROPIC_API_KEY` environment variable must be set. Check for it before running evaluations.

## Common Pitfalls to Avoid

- **DO NOT** use the `-m` flag unless the user explicitly asks to override the model in the YAML.
- **DO NOT** hallucinate dataset names. Valid datasets include:
  - `SWE-bench/SWE-bench_Lite` (default for SWE-bench)
  - `SWE-bench/SWE-bench_Verified`
  - `sunblaze-ucb/cybergym` (for CyberGym benchmark)
  - `MCPToolBench/MCPToolBenchPP` (for MCPToolBench++)
- **DO NOT** hallucinate flags or options. Only use documented CLI flags.
- **DO NOT** forget to specify the config file with `-c` or `--config`.

## Supported Benchmarks

mcpbr supports three benchmarks:
1. **SWE-bench** (default): Real GitHub issues requiring bug fixes
   - Dataset: `SWE-bench/SWE-bench_Lite` or `SWE-bench/SWE-bench_Verified`
   - Use: `mcpbr run -c config.yaml` or `--benchmark swe-bench`

2. **CyberGym**: Security vulnerabilities requiring PoC exploits
   - Dataset: `sunblaze-ucb/cybergym`
   - Use: `mcpbr run -c config.yaml --benchmark cybergym --level [0-3]`

3. **MCPToolBench++**: Large-scale tool use evaluation
   - Dataset: `MCPToolBench/MCPToolBenchPP`
   - Use: `mcpbr run -c config.yaml --benchmark mcptoolbench`

## Execution Steps

Follow these steps in order:

1. **Verify Prerequisites:**
   ```bash
   # Check Docker is running
   docker ps

   # Verify API key is set
   echo $ANTHROPIC_API_KEY
   ```

2. **Check for Config File:**
   - If `mcpbr.yaml` (or user-specified config) does NOT exist: Run `mcpbr init` to generate it.
   - If config exists: Read it to understand the configuration.

3. **Validate Config:**
   - Ensure `mcp_server.command` is valid (e.g., `npx`, `uvx`, `python` are installed).
   - Ensure `mcp_server.args` includes `"{workdir}"` placeholder.
   - Verify `model`, `dataset`, and other parameters are correctly set.

4. **Construct the Command:**
   - Base command: `mcpbr run --config <path-to-config>`
   - Add flags as needed based on user request:
     - `-n <number>` or `--sample <number>`: Override sample size
     - `-v` or `-vv`: Verbose output
     - `-o <path>`: Save JSON results
     - `-r <path>`: Save Markdown report
     - `--log-dir <path>`: Save per-instance logs
     - `-M`: MCP-only evaluation (skip baseline)
     - `-B`: Baseline-only evaluation (skip MCP)
     - `--benchmark <name>`: Override benchmark
     - `--level <0-3>`: Set CyberGym difficulty level

5. **Run the Command:**
   Execute the constructed command and monitor the output.

6. **Handle Results:**
   - If the run completes successfully, inform the user about the results.
   - If errors occur, diagnose and provide actionable feedback.

## Example Commands

```bash
# Full evaluation with 5 tasks
mcpbr run -c config.yaml -n 5 -v

# MCP-only evaluation
mcpbr run -c config.yaml -M -n 10

# Save results and report
mcpbr run -c config.yaml -o results.json -r report.md

# Run CyberGym at level 2
mcpbr run -c config.yaml --benchmark cybergym --level 2 -n 5

# Run specific tasks
mcpbr run -c config.yaml -t astropy__astropy-12907 -t django__django-11099
```

## Troubleshooting

If you encounter errors:

1. **Docker not running:** Remind user to start Docker Desktop or Docker daemon.
2. **API key missing:** Ask user to set `export ANTHROPIC_API_KEY="sk-ant-..."`
3. **Config file invalid:** Re-generate with `mcpbr init` or fix the YAML syntax.
4. **MCP server fails to start:** Test the server command independently.
5. **Timeout issues:** Suggest increasing `timeout_seconds` in config.

## Important Reminders

- Always read the config file before making assumptions about what's configured.
- Never modify the config file without explicit user permission.
- Use the `mcpbr models` command to check available models if needed.
- Use the `mcpbr benchmarks` command to list available benchmarks.
