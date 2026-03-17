---
name: dep-audit
description: >
  Audit project dependencies for known vulnerabilities (CVEs).
  Supports npm, pip, Cargo, and Go. Zero API keys required.
  Safe-by-default: report-only mode, fix commands require confirmation.
version: 0.1.4
author: Anvil AI
tags: [security, audit, dependencies, cve, supply-chain, discord, discord-v2]
---

# Dependency Audit Skill

Detect and report known vulnerabilities in your project's dependency tree.
Supports **npm**, **pip (Python)**, **Cargo (Rust)**, and **Go** out of the box.
No API keys. No config. Just point it at a project.

## Activation

This skill activates when the user mentions:
- "audit", "vulnerability", "CVE", "dependency check", "supply chain", "security scan"
- Checking dependencies, lockfiles, or packages for issues
- Generating an SBOM (Software Bill of Materials)

## Example Prompts

1. "Audit this project for vulnerabilities"
2. "Check all my repos in ~/projects for known CVEs"
3. "Are there any critical vulnerabilities I should fix right now?"
4. "Generate an SBOM for this project"
5. "What dependencies need updating in this project?"
6. "Audit only the Python dependencies"

## Permissions

```yaml
permissions:
  exec: true          # Required to run audit CLIs
  read: true          # Read lockfiles
  write: on-request   # SBOM generation writes sbom.cdx.json when user asks
  network: true       # Tools fetch advisory DBs
```

## Agent Workflow

Follow this sequence exactly:

### Step 1: Detect

Run the detection script to discover lockfiles and available tools:

```bash
bash <skill_dir>/scripts/detect.sh <target_directory>
```

If no target directory is given, use the current working directory (`.`).

Parse the JSON output. Note which ecosystems have lockfiles and which tools are available.

### Step 2: Audit Each Ecosystem

For each ecosystem detected in Step 1:

- **If the audit tool is available**, run the corresponding script:
  ```bash
  bash <skill_dir>/scripts/audit-npm.sh <directory>
  bash <skill_dir>/scripts/audit-pip.sh <directory>
  bash <skill_dir>/scripts/audit-cargo.sh <directory>
  bash <skill_dir>/scripts/audit-go.sh <directory>
  ```

- **If the tool is missing**, tell the user which tool is needed and the install command from the detect output. Skip that ecosystem and continue with others.

> **Note:** `yarn.lock` and `pnpm-lock.yaml` are detected as `yarn` and `pnpm` ecosystems respectively. Audit support is npm-only in v0.1.x (`package-lock.json`). If only a `yarn.lock` or `pnpm-lock.yaml` is present, inform the user that dedicated yarn/pnpm audit is not yet supported and suggest running `yarn audit` or `pnpm audit` manually.

Each script outputs normalized JSON to stdout.

### Step 3: Aggregate

Pipe or pass all per-ecosystem JSON results to the aggregator:

```bash
bash <skill_dir>/scripts/aggregate.sh <npm_result.json> <pip_result.json> ... 1>unified.json 2>report.md
```

The aggregator outputs unified JSON to **stdout** and a Markdown report to **stderr**.
Capture both: `2>report.md` for the Markdown, `1>unified.json` for the JSON.

### Step 4: Present Results

Show the user the Markdown report from the aggregator. Highlight:
- Total vulnerability count by severity
- Critical and High findings first (these need attention)
- Which ecosystems were scanned vs skipped

If **zero vulnerabilities** found: report "✅ No known vulnerabilities found."
If **no lockfiles** found: report "No lockfiles found in <dir>. This skill works with npm, pip, Cargo, and Go projects."

### Discord v2 Delivery Mode (OpenClaw v2026.2.14+)

When the user is in a Discord channel:

- Send a short first response with totals and only Critical/High findings.
- Keep the first message under ~1200 characters and avoid large Markdown tables up front.
- If Discord components are available, include quick actions:
  - `Show Full Report`
  - `Show Fix Commands`
  - `Generate SBOM`
- If components are unavailable, provide the same options as a numbered list.
- Send long details in short chunks (<=15 lines) to improve readability.

### Step 5: Fix Suggestions (only if user asks)

If the user asks to fix vulnerabilities:

1. List every fix command with the package name, current version, and target version.
2. **Suggest** creating a branch first: `git checkout -b dep-audit-fixes`
3. **Ask for explicit confirmation** before running ANY fix command.
4. Never batch-run fix commands silently.

Example interaction:
```
I found these fix commands:
  1. cd /home/user/project && npm audit fix
  2. pip install requests>=2.31.0

I recommend creating a branch first:
  git checkout -b dep-audit-fixes

Shall I run them? (yes/no)
```

### Step 6: SBOM (only if user asks)

```bash
bash <skill_dir>/scripts/sbom.sh <directory>
```

Report the file location and component count.

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Tool not found | Print which tool is missing + install command. Continue with available tools. |
| Audit tool fails | Capture stderr, report "audit failed for [ecosystem]: [error]". Continue with others. |
| Timeout (>30s per tool) | When `timeout`/`gtimeout` is available, report "audit timed out for [ecosystem], skipping". Continue. |
| Invalid target directory | Report "directory not found or not accessible" and stop that ecosystem scan (do **not** report false "clean"). |
| No lockfiles found | Report "No lockfiles found" + list supported ecosystems. |
| `jq` not available | Detection works without jq. Audit and aggregation **require** jq — install it first. |
| Malformed lockfile | Report parse error for that ecosystem. Continue with others. |

### Aggregation Robustness

- `aggregate.sh` now tolerates mixed inputs (valid results + error objects).
- Invalid input objects are listed under `errors` in unified JSON and rendered in a "Skipped / Error Inputs" Markdown section.
- If no valid ecosystem results are provided, aggregate output sets `status: "error"` instead of crashing.

## Safety

- **Default mode is report-only.** The skill never modifies files unless you explicitly ask for a fix and confirm.
- Audit tools read lockfiles — they do not execute project code.
- Fix commands (`npm audit fix`, `pip install --upgrade`) are printed as suggestions. The agent will ask for confirmation before running them.
- This skill checks known advisory databases (OSV, GitHub Advisory DB, RustSec). It does not detect zero-days or runtime vulnerabilities.
- No data is sent to third-party services beyond what the native audit tools do (they query public advisory databases).
- No telemetry. No tracking. No phone-home.
