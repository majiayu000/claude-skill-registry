---
name: quality-stack
description: >
  Scan a project to detect configured quality and testing tools across JVM
  (Gradle/Maven), Android (AGP/Compose/KMP), Node.js/TypeScript, and Python
  ecosystems. Cross-reference against research-backed recommendations and assist
  with setup. Auto-detects project type(s) including monorepos with mixed
  ecosystems. Use when user asks to "audit tooling", "recommend tools", "quality
  stack", "what tools am I missing", "setup eslint", "setup detekt", "add
  coverage", "add ruff", "configure CI quality pipeline", "scan project tools",
  "tooling audit", "android tooling", "android quality", "compose testing",
  "kmp testing", or "screenshot testing".
disable-model-invocation: true
---

# Quality Stack

Scan a project's build configuration across JVM, Android, Node.js, and Python ecosystems, cross-reference against curated research documents, and assist with tool setup.

## Pre-flight

1. **Run the orchestrator** — it auto-detects ecosystems:
   ```bash
   python3 <skill-path>/scripts/scan_project.py <project-root>
   ```
2. If `"error": "no_ecosystem_detected"`, check `nearby_project_files` for subproject paths.
3. **Monorepo?** — use `--recursive` or `--ecosystem` to force a specific scanner:
   ```bash
   python3 <skill-path>/scripts/scan_project.py --recursive <project-root>
   python3 <skill-path>/scripts/scan_project.py --ecosystem node <project-root>
   ```
4. **Legacy (JVM only)** — `scan_tooling.py` still works as a backwards-compatible wrapper.

## Two-Phase Workflow

### Phase 1: Recommend

1. **Run the scanner** on the project root (see Pre-flight above).

2. **Fetch research documents** via WebFetch — only for detected ecosystems:

   **Android** (when `ecosystems` contains `"android"`):
   ```
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/research/android-ecosystem-tooling.md
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/research/android-testing-ecosystem.md
   ```

   **JVM** (when `ecosystems` contains `"jvm"`):
   ```
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/research/jvm-quality-tools-evaluation.md
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/research/kotlin-spring-boot-testing-ecosystem.md
   ```

   **Node.js** (when `ecosystems` contains `"node"`):
   ```
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/research/node-quality-tools-evaluation.md
   ```

   **Python** (when `ecosystems` contains `"python"`):
   ```
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/research/python-quality-tools-evaluation.md
   ```

   **Cross-cutting** (always):
   ```
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/research/cross-cutting-devtools-evaluation.md
   ```

   If WebFetch fails, warn the user and proceed using scanner results + LLM knowledge only.

3. **Cross-reference** scanner output against research recommendations per ecosystem:
   - Identify tools recommended but missing from the project
   - Check `status` field: `disabled` or `config-only` tools need attention
   - Flag outdated or superseded tools
   - Apply ecosystem-specific SKIP rules (see [WORKFLOW.md](WORKFLOW.md))
   - Review `tool_config` for threshold values and settings

4. **Generate the recommendation report** using the format in [WORKFLOW.md](WORKFLOW.md).

### Phase 2: Setup

After presenting the report, present tools for selection using the multi-round
protocol in [WORKFLOW.md](WORKFLOW.md). Group by ecosystem and priority tier.
Include effort estimates. After user completes selection across all rounds:

1. Read the relevant research doc section for setup instructions
2. Apply [Setup Guards](WORKFLOW.md) — resolve versions, check compatibility
3. For each selected tool, apply changes per ecosystem:
   - **JVM**: Add Gradle/Maven plugin, test deps, config files
   - **Node.js**: `pnpm add -D`, tsconfig edits, config file creation
   - **Python**: `uv add --dev`, pyproject.toml edits, config file creation
   - **Cross-cutting**: CI/CD workflow steps, Lefthook config, EditorConfig
4. **Verify each tool** after configuration — run the tool's check command,
   verify filter patterns against actual codebase paths, and check for config
   inheritance conflicts. See [WORKFLOW.md](WORKFLOW.md) Post-Setup Verification.
5. Re-run the scanner to confirm all tools detected

## Priority Classification

| Priority | Criteria |
|----------|----------|
| **NOW** | Essential missing tools, zero-dependency additions |
| **SOON** | High-value additions requiring minor setup |
| **LATER** | Nice-to-have with prerequisites |
| **SKIP** | Not applicable (wrong ecosystem, incompatible version, deprecated) |

**Ecosystem-aware rules** — see [WORKFLOW.md](WORKFLOW.md) for full classification tables per ecosystem.

**Key rules:**
- Android Compose project: NOW Compose UI testing, SOON Roborazzi; SKIP Espresso
- Android KMP project: NOW commonTest setup, NOW Turbine; SOON Ktor MockEngine
- Android no lint config: NOW Android Lint baseline; SOON custom lint rules
- JVM Pure Kotlin: SKIP Error Prone, SpotBugs; JVM Pure Java: SKIP Detekt, ktlint, MockK
- JVM Spring Boot 4+: SKIP REST Assured, NOW MockMvcTester
- Node.js no linter: NOW ESLint; no formatter + no Biome: NOW Prettier
- Node.js TypeScript not strict: NOW enable strict
- Python no linter: NOW Ruff; no type checker + has type annotations: NOW mypy

### Cross-Cutting Tools

| Tool | When to Recommend | Priority |
|------|------------------|----------|
| Lefthook | No git hook manager + has linters | SOON |
| commitlint | No commit conventions + has team | LATER |
| EditorConfig | Missing `.editorconfig` | NOW |
| Renovate/Dependabot | No dependency automation | SOON |
| Trivy/gitleaks | No security scanning | SOON |

## Research Documents

Fetch via WebFetch at runtime — only for detected ecosystems:

- **Android Ecosystem Tooling**: `android-ecosystem-tooling.md`
- **Android Testing Ecosystem**: `android-testing-ecosystem.md`
- **JVM Quality Tools**: `jvm-quality-tools-evaluation.md`
- **JVM Testing Ecosystem**: `kotlin-spring-boot-testing-ecosystem.md`
- **Node.js Quality Tools**: `node-quality-tools-evaluation.md`
- **Python Quality Tools**: `python-quality-tools-evaluation.md`
- **Cross-Cutting Tools**: `cross-cutting-devtools-evaluation.md`

## Scanner Architecture

```
scripts/
  scan_project.py          # Orchestrator — auto-detects + merges
  scan_jvm.py              # JVM scanner (Gradle/Maven)
  scan_android.py          # Android scanner (AGP/Compose/KMP)
  scan_node.py             # Node.js/TypeScript scanner
  scan_python.py           # Python scanner
  scan_cross_cutting.py    # Cross-cutting tools (CI, hooks, security)
  shared.py                # Shared utilities
  scan_tooling.py          # Legacy wrapper → scan_jvm.py
```

## References

- **Workflow**: See [WORKFLOW.md](WORKFLOW.md) for classification rules and report format
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for realistic audit scenarios
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for scanner issues
