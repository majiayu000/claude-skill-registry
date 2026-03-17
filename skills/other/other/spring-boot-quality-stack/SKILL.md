---
name: spring-boot-quality-stack
description: >
  Scan a JVM project to detect configured quality and testing tools,
  cross-reference against research-backed recommendations, and assist with setup.
  Use when user asks to "audit tooling", "recommend tools", "quality stack",
  "what tools am I missing", "setup detekt", "add coverage", "configure CI quality pipeline".
---

# Spring Boot Quality Stack

Scan a project's build configuration, cross-reference against curated research documents, and assist with tool setup.

## Pre-flight

1. **Verify build files exist** — run the scanner. If it returns `"error": "no_build_file"`, check `nearby_build_files` for subproject paths.
2. **Monorepo?** — if the Spring Boot project is nested, either pass the subproject path directly or use `--recursive`:
   ```bash
   python3 <skill-path>/scripts/scan_tooling.py --recursive <project-root>
   ```

## Two-Phase Workflow

### Phase 1: Recommend

1. **Run the scanner** on the project root:
   ```bash
   python3 <skill-path>/scripts/scan_tooling.py <project-root>
   ```

2. **Fetch the research documents** via WebFetch:
   ```
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/research/jvm-quality-tools-evaluation.md
   https://raw.githubusercontent.com/joaquimscosta/arkhe-claude-plugins/main/docs/research/kotlin-spring-boot-testing-ecosystem.md
   ```
   If WebFetch fails (network error, 404), warn the user and proceed using scanner results + LLM knowledge only.

3. **Cross-reference** scanner JSON output against research recommendations:
   - Identify tools recommended by research but missing from the project
   - Check tool `status` field: `disabled` or `config-only` tools need attention
   - Flag tools that are present but outdated or superseded
   - Note tools to SKIP based on project profile (language, Spring Boot version)
   - Review `tool_config` for threshold values and reporter settings

4. **Generate the recommendation report** using the format in [WORKFLOW.md](WORKFLOW.md).

### Phase 2: Setup

After presenting the report, use `AskUserQuestion` (multiSelect: true) with the top NOW/SOON recommendations as options. After the user selects tools:

1. Read the relevant section from the research document for setup instructions
2. For each selected tool, apply changes:
   - Add Gradle plugin or Maven plugin declaration
   - Add test dependencies
   - Create config files (detekt.yml, .trivyignore, etc.)
   - Add CI/CD workflow steps if applicable
3. Re-run the scanner to confirm detection

## Priority Classification

Classify each recommendation based on project context:

| Priority | Criteria |
|----------|----------|
| **NOW** | Essential missing tools, zero-dependency additions, items marked NOW in research |
| **SOON** | High-value additions requiring minor setup, items marked SOON in research |
| **LATER** | Nice-to-have tools with prerequisites, items marked LATER in research |
| **SKIP** | Not applicable for this project (wrong language, incompatible version, deprecated) |

**Language-aware rules:**
- Pure Kotlin: SKIP Error Prone, SpotBugs (Java-only or bytecode-only value)
- Pure Java: SKIP Detekt, ktlint, Kover, MockK, kotlin-faker
- Spring Boot 4+: SKIP REST Assured spring-mock-mvc (broken with jakarta)
- Spring Boot 4+: NOW MockMvcTester (built-in replacement)

### Category: Git Hooks

| Tool | When to Recommend | Priority |
|------|------------------|----------|
| Lefthook | No git hook manager + has linters (ktlint/detekt) | SOON |
| Lefthook | Husky or pre-commit already present | SKIP (note: migration possible) |

**Note:** When setting up Lefthook (Phase 2), the scanner also detects frontend tools
(ESLint, Prettier, Tailwind CSS) in `package.json` files at the project root and in
monorepo sibling directories. These are wired into `lefthook.yml` alongside JVM hooks
but do not appear in the recommendation phase.

## Research Documents

Fetch these via WebFetch at runtime — do not cache or embed their content:

- **Quality Tools**: `jvm-quality-tools-evaluation.md` — Error Prone, SpotBugs, Detekt, ktlint, SonarQube, JaCoCo, PIT, ArchUnit, Testcontainers, Spring Cloud Contract, Pact, Gradle Cache, GitHub Actions, OpenRewrite, Renovate, JMH, OWASP DC, Trivy, Snyk
- **Testing Ecosystem**: `kotlin-spring-boot-testing-ecosystem.md` — Assertions, Test Data, Coverage, Property Testing, API Testing, Contract Testing, DB Testing, Mutation Testing, Spring Modulith Testing

## References

- **Workflow**: See [WORKFLOW.md](WORKFLOW.md) for detailed phase descriptions, classification logic, and report template
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for realistic audit scenarios
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for scanner issues
- **Scanner Script**: See [scripts/scan_tooling.py](scripts/scan_tooling.py) for detection patterns
