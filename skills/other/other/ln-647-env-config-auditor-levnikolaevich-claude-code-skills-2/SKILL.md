---
name: ln-647-env-config-auditor
description: "Checks env var config sync, missing defaults, naming conventions, startup validation. Use when auditing environment configuration."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_symbols, mcp__hex-graph__find_references
license: MIT
model: claude-haiku-4-5
---

> **Paths:** File paths (`shared/`, `references/`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Env Config Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing environment variable configuration, synchronization, and hygiene.

## Purpose & Scope

- Audit **env var configuration** across code, .env files, docker-compose, CI configs
- 4 check categories: File Inventory, Variable Synchronization, Naming & Quality, Startup Validation
- 11 checks total (C1.1-C1.3, C2.1-C2.3, C3.1-C3.3, C4.1-C4.2)
- Calculate compliance score (X/10)
- Stack-adaptive detection (JS, Python, Go, .NET, Java, Ruby, Rust)

**Out of Scope:**

- Hardcoded secrets detection in source code (security auditor domain)
- .gitignore/.dockerignore patterns (project structure auditor domain)
- Env file generation/scaffolding (bootstrap domain)

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with tech stack, codebase root, output_dir, domain_mode, scan_path.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

**MANDATORY READ:** Load `references/config_rules.md` for detection patterns.

### Phase 1: Parse Context + Detect Stack

```
1. Parse: codebase_root, output_dir, tech_stack, domain_mode, scan_path
2. Determine primary language from tech_stack -> select env usage patterns from config_rules.md
3. Determine project type:
   - web_service: Express/FastAPI/ASP.NET/Spring -> all checks apply
   - cli_tool: Click/Typer/Commander/cobra -> C1.3 optional, C4.1 optional
   - library: exports only -> C1.1 optional, C4.1 skip
```

### Phase 2: File Inventory (Layer 1 only)

```
# C1.1: .env.example or .env.template exists
example_files = Glob("{scan_root}/.env.example") + Glob("{scan_root}/.env.template")
IF len(example_files) == 0:
  findings.append(severity: "MEDIUM", check: "C1.1",
    issue: "No .env.example or .env.template",
    recommendation: "Create .env.example documenting all required env vars",
    effort: "S")

# C1.2: .env files committed (secrets risk)
env_committed = Glob("{scan_root}/**/.env") + Glob("{scan_root}/**/.env.local")
  + Glob("{scan_root}/**/.env.*.local")
# Exclude safe templates
env_committed = filter_out(env_committed, [".env.example", ".env.template", ".env.test"])
FOR EACH file IN env_committed:
  findings.append(severity: "CRITICAL", check: "C1.2",
    issue: ".env file committed: {file}",
    location: file,
    recommendation: "Remove from tracking (git rm --cached), add to .gitignore",
    effort: "S")

# C1.3: Environment-specific file structure
docker_compose = Glob("{scan_root}/docker-compose*.yml") + Glob("{scan_root}/docker-compose*.yaml")
IF len(docker_compose) > 0:
  env_specific = Glob("{scan_root}/.env.development") + Glob("{scan_root}/.env.production")
    + Glob("{scan_root}/.env.staging")
  IF len(env_specific) == 0 AND len(example_files) == 0:
    findings.append(severity: "LOW", check: "C1.3",
      issue: "Docker Compose present but no env-specific files or .env.example",
      recommendation: "Create .env.example with documented vars per environment",
      effort: "S")
```

### Phase 3: Variable Synchronization (Layer 1 + Layer 2)

```
# Step 3a: Extract vars from code (Layer 1)
code_vars = {}  # {var_name: [{file, line, has_default, default_value}]}
FOR EACH pattern IN config_rules.env_usage_patterns[tech_stack.language]:
  matches = Grep(pattern, scan_root, glob: source_extensions)
  FOR EACH match IN matches:
    var_name = extract_var_name(match)
    code_vars[var_name].append({file: match.file, line: match.line,
      has_default: check_default(match), default_value: extract_default(match)})

# Pydantic Settings (Layer 2): detect BaseSettings subclasses
IF tech_stack.language == "python":
  settings_classes = Grep("class\s+\w+\(.*BaseSettings", scan_root, glob: "*.py")
  FOR EACH cls IN settings_classes:
    Read class body -> extract fields -> convert to SCREAMING_SNAKE_CASE
    Apply env_prefix if configured
    Add to code_vars

# Step 3b: Extract vars from .env.example
example_vars = {}  # {var_name: value_or_empty}
IF exists(.env.example):
  FOR EACH line IN Read(.env.example):
    IF line matches r'^([A-Z_][A-Z0-9_]*)=(.*)':
      example_vars[$1] = $2

# Step 3c: Extract vars from docker-compose environment
docker_vars = {}  # {var_name: value}
FOR EACH compose_file IN docker_compose:
  Parse environment: section(s) -> extract var=value pairs
  docker_vars.update(parsed)

# C2.1: Code->Example sync (Layer 2 mandatory)
missing_from_example = code_vars.keys() - example_vars.keys()
FOR EACH var IN missing_from_example:
  # Layer 2: filter false positives
  IF var IN config_rules.framework_managed[tech_stack.framework]:
    SKIP  # Auto-managed by framework
  ELIF var appears only in test files:
    SKIP  # Test-only variable
  ELSE:
    findings.append(severity: "MEDIUM", check: "C2.1",
      issue: "Env var '{var}' used in code but missing from .env.example",
      location: code_vars[var][0].file + ":" + code_vars[var][0].line,
      recommendation: "Add {var} to .env.example with documented default",
      effort: "S")

# C2.2: Example->Code sync (dead vars, Layer 2 mandatory)
dead_vars = example_vars.keys() - code_vars.keys()
FOR EACH var IN dead_vars:
  # Layer 2: check infrastructure usage
  IF Grep(var, docker_compose + Dockerfiles + CI_configs):
    SKIP  # Used in infrastructure, not dead
  ELIF var IN config_rules.framework_managed:
    SKIP  # Framework auto-reads it
  ELSE:
    findings.append(severity: "MEDIUM", check: "C2.2",
      issue: "Dead var in .env.example: '{var}' (unused in code and infrastructure)",
      location: ".env.example",
      recommendation: "Remove from .env.example or add usage in code",
      effort: "S")

# C2.3: Default desync (Layer 2 mandatory)
# Limit to top 50 vars for token budget
sync_candidates = code_vars where has_default == true AND
  (var IN example_vars OR var IN docker_vars)
FOR EACH var IN sync_candidates[:50]:
  defaults = {}
  IF var has default in code: defaults["code"] = code_default
  IF var in example_vars with non-empty value: defaults["example"] = example_value
  IF var in docker_vars: defaults["docker-compose"] = docker_value

  IF len(defaults) >= 2 AND NOT all_equal(defaults.values()):
    findings.append(severity: "HIGH", check: "C2.3",
      issue: "Default desync for '{var}': " + format_defaults(defaults),
      location: code_vars[var][0].file + ":" + code_vars[var][0].line,
      recommendation: "Unify defaults across code, .env.example, docker-compose",
      effort: "M")
```

### Phase 4: Naming & Quality (Layer 1 + Layer 2)

```
all_vars = set(code_vars.keys()) | set(example_vars.keys())

# C3.1: Naming convention
non_screaming = [v for v in all_vars if NOT matches(r'^[A-Z][A-Z0-9_]*$', v)]
IF len(non_screaming) > 0:
  findings.append(severity: "LOW", check: "C3.1",
    issue: "Non-SCREAMING_SNAKE_CASE vars: " + join(non_screaming[:10]),
    recommendation: "Rename to SCREAMING_SNAKE_CASE for consistency",
    effort: "S")

# Prefix consistency check (Layer 2)
prefixes = group_by_concept(all_vars)
# e.g., {database: [DB_HOST, DB_PORT, DATABASE_URL]} -> conflicting prefixes
conflicting = find_conflicting_prefixes(prefixes)
IF conflicting:
  FOR EACH group IN conflicting:
    findings.append(severity: "LOW", check: "C3.1",
      issue: "Inconsistent prefixes: " + join(group.vars),
      recommendation: "Standardize to one prefix (e.g., DB_ or DATABASE_)",
      effort: "S")

# C3.2: Redundant variables (Layer 2 mandatory)
# Conservative: only flag vars with identical suffixes + overlapping prefixes
FOR EACH suffix IN common_suffixes(all_vars):  # e.g., _CACHE_TTL, _TIMEOUT
  vars_with_suffix = filter(all_vars, suffix)
  IF len(vars_with_suffix) >= 2:
    # Layer 2: read usage context
    IF vars serve same purpose with same or similar values:
      findings.append(severity: "LOW", check: "C3.2",
        issue: "Potentially redundant vars: " + join(vars_with_suffix),
        recommendation: "Consider unifying into single var",
        effort: "M")

# C3.3: Missing comments in .env.example
IF exists(.env.example):
  lines = Read(.env.example)
  uncommented_vars = 0
  FOR EACH var_line IN lines:
    IF is_var_declaration(var_line):
      preceding = get_preceding_line(var_line)
      IF NOT is_comment(preceding) AND NOT is_self_explanatory(var_name):
        uncommented_vars += 1
  IF uncommented_vars > 3:
    findings.append(severity: "LOW", check: "C3.3",
      issue: "{uncommented_vars} vars in .env.example lack explanatory comments",
      location: ".env.example",
      recommendation: "Add comments for non-obvious vars; include generation instructions for secrets",
      effort: "S")
```

### Phase 5: Startup Validation (Layer 1 + Layer 2)

```
# C4.1: Required vars validated at boot
# Layer 1: detect validation frameworks
validation_found = false
FOR EACH framework IN config_rules.validation_frameworks[tech_stack.language]:
  IF Grep(framework.detection_pattern, scan_root, glob: source_extensions):
    validation_found = true
    BREAK

IF NOT validation_found:
  # Layer 2: check for manual validation patterns
  manual_patterns = [
    r'process\.env\.\w+.*throw|if\s*\(!process\.env',        # JS
    r'os\.getenv.*raise|if not os\.getenv|if\s+os\.environ',  # Python
    r'os\.Getenv.*panic|os\.Getenv.*log\.Fatal',              # Go
  ]
  FOR EACH pattern IN manual_patterns:
    IF Grep(pattern, scan_root):
      validation_found = true
      BREAK

IF NOT validation_found AND project_type == "web_service":
  findings.append(severity: "MEDIUM", check: "C4.1",
    issue: "No startup validation for required env vars",
    recommendation: "Add validation at boot (pydantic-settings, envalid, zod, or manual checks)",
    effort: "M")

# C4.2: Sensitive defaults (Layer 1 + Layer 2)
sensitive_patterns = config_rules.sensitive_var_patterns
FOR EACH var IN code_vars WHERE var.has_default == true:
  var_upper = var.name.upper()
  IF any(pattern IN var_upper for pattern IN sensitive_patterns):
    # Layer 2: verify this is truly sensitive
    context = Read(var.file, var.line +- 10 lines)
    IF default_value is not empty string AND not "changeme" AND not placeholder:
      findings.append(severity: "HIGH", check: "C4.2",
        issue: "Sensitive default for '{var.name}': hardcoded fallback bypasses env config",
        location: var.file + ":" + var.line,
        recommendation: "Remove default; require explicit env var or fail at startup",
        effort: "S")
```

### Phase 6: Score + Report + Return

```
1. Calculate score:
   penalty = (CRITICAL * 2.0) + (HIGH * 1.0) + (MEDIUM * 0.5) + (LOW * 0.2)
   score = max(0, 10 - penalty)

2. Build report per shared/templates/audit_worker_report_template.md
   Include AUDIT-META, Checks table, Findings table
   Include DATA-EXTENDED with:
   {
     tech_stack_detected: string,
     env_files_inventory: [{file, type, committed}],
     code_vars_count: number,
     example_vars_count: number,
     sync_stats: {missing_from_example, dead_in_example, default_desync},
     validation_framework: string | null
   }

3. Write to {output_dir}/ln-647--{identifier}.md (atomic single Write call)
   IF domain_mode == "domain-aware": 647-env-config-{domain}.md

4. Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
   Report written: {output_dir}/ln-647--{identifier}.md
   Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-647--{identifier}.md` with `category: "Env Configuration"` and checks: env_example_exists, env_committed, env_specific_files, code_to_example_sync, example_to_code_sync, default_desync, naming_convention, redundant_vars, missing_comments, startup_validation, sensitive_defaults.

## Reference Files

- **Detection patterns:** `references/config_rules.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only, never modify .env files or code
- **Stack-adaptive:** Select detection patterns based on tech_stack language/framework
- **Layer 2 mandatory for C2.x and C4.x:** No Layer 1 match is valid without context verification
- **C2.3 token budget:** Limit default desync analysis to top 50 variables
- **Domain-aware scoping:** .env files scanned globally (project root); code vars scoped to `scan_path`
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip test files for C2.1, skip framework-managed vars per config_rules.md

## Definition of Done

- [ ] contextStore parsed (tech stack, framework, output_dir)
- [ ] All 11 checks completed (C1.1-C1.3, C2.1-C2.3, C3.1-C3.3, C4.1-C4.2)
- [ ] Findings collected with severity, location, check ID, effort, recommendation
- [ ] Score calculated per `shared/references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-647--{identifier}.md` (atomic single Write call)
- [ ] Summary written per contract

---
**Version:** 1.0.0
**Last Updated:** 2026-03-15
