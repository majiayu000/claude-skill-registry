---
name: ln-646-project-structure-auditor
description: "Checks file hygiene, ignore files, framework conventions, domain/layer organization, naming. Use when auditing project structure."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__analyze_architecture
license: MIT
model: claude-haiku-4-5
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Project Structure Auditor

**Type:** L3 Worker

L3 Worker that audits the physical directory structure of a project against framework-specific conventions and hygiene best practices.

## Purpose & Scope

- Auto-detect tech stack and apply framework-specific structure rules
- Audit 5 dimensions: file hygiene, ignore files, framework conventions, domain/layer organization, naming
- Detect project rot: leftover artifacts, inconsistent naming, junk drawer directories
- Complement code-level layer analysis with physical structure analysis
- Score and report findings per standard `audit_scoring.md` formula
- Output: file-based report to `{output_dir}/646-structure[-{domain}].md`

**Out of Scope:**
- Code-level layer boundary violations (import analysis)
- Platform artifact cleanup (removal of files)
- Structure migration (creation/movement of directories)
- Dependency vulnerability scanning

## Input

```
- codebase_root: string        # Root directory to scan
- output_dir: string           # e.g., ".hex-skills/runtime-artifacts/runs/{run_id}/audit-report"

# Domain-aware (optional, from coordinator)
- domain_mode: "global" | "domain-aware"   # Default: "global"
- current_domain: string                   # e.g., "users", "billing" (only if domain-aware)
- scan_path: string                        # e.g., "src/users/" (only if domain-aware)
```

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

### Phase 1: Detect Tech Stack

**MANDATORY READ:** Load `../ln-700-project-bootstrap/references/stack_detection.md` -- use Detection Algorithm, Frontend Detection, Backend Detection, Structure Detection.

```
scan_root = scan_path IF domain_mode == "domain-aware" ELSE codebase_root

# Priority 1: Read docs/project/tech_stack.md if exists
IF exists(docs/project/tech_stack.md):
  tech_stack = parse(tech_stack.md)

# Priority 2: Auto-detect from project files
ELSE:
  Check package.json -> React/Vue/Angular/Express/NestJS
  Check *.csproj/*.sln -> .NET
  Check pyproject.toml/requirements.txt -> Python/FastAPI/Django
  Check go.mod -> Go
  Check Cargo.toml -> Rust
  Check pnpm-workspace.yaml/turbo.json -> Monorepo

  tech_stack = {
    language: "typescript" | "python" | "csharp" | "go" | ...,
    framework: "react" | "fastapi" | "aspnetcore" | ...,
    structure: "monolith" | "clean-architecture" | "monorepo" | ...
  }
```

### Phase 2: File Hygiene Audit

**MANDATORY READ:** Load `references/structure_rules.md` -- use "File Hygiene Rules" section. Also reference: `../ln-724-artifact-cleaner/references/platform_artifacts.md` (Platform Detection Matrix, Generic Prototype Artifacts).

```
# Check 2.1: Build artifacts tracked in git
FOR EACH artifact_dir IN structure_rules.build_artifact_dirs:
  IF Glob("{scan_root}/**/{artifact_dir}"):
    findings.append(severity: "HIGH", issue: "Build artifact directory in repo",
      location: path, recommendation: "Add to .gitignore, remove from tracking")

# Check 2.2: Temp/log files
FOR EACH pattern IN structure_rules.temp_junk_patterns:
  IF Glob("{scan_root}/**/{pattern}"):
    findings.append(severity: "MEDIUM", ...)

# Check 2.3: Platform remnants (from platform_artifacts.md)
FOR EACH platform IN [Replit, StackBlitz, CodeSandbox, Glitch]:
  IF platform indicator files found:
    findings.append(severity: "MEDIUM", issue: "Platform remnant: {file}",
      principle: "File Hygiene / Platform Artifacts")

# Check 2.4: Multiple lock files
lock_files = Glob("{scan_root}/{package-lock.json,yarn.lock,pnpm-lock.yaml,bun.lockb}")
IF len(lock_files) > 1:
  findings.append(severity: "HIGH", issue: "Multiple lock files: {lock_files}",
    recommendation: "Keep one lock file matching your package manager")

# Check 2.6: Large binaries tracked by git
FOR EACH file IN Glob("{scan_root}/**/*.{zip,tar,gz,rar,exe,dll,so,dylib,jar,war}"):
  findings.append(severity: "MEDIUM", issue: "Binary file tracked: {file}",
    recommendation: "Use Git LFS or remove from repository")
```

### Phase 3: Ignore File Quality

**MANDATORY READ:** Load `references/structure_rules.md` -- use "Ignore File Rules" section. Also reference: `../ln-733-env-configurator/references/gitignore_secrets.template` (secrets baseline), `../ln-731-docker-generator/references/dockerignore.template` (dockerignore baseline).

```
# Check 3.1: .gitignore exists
IF NOT exists(.gitignore):
  findings.append(severity: "HIGH", issue: "No .gitignore file")
ELSE:
  content = Read(.gitignore)

  # Check 3.1a: Stack-specific entries present
  required_entries = get_required_gitignore(tech_stack)
  FOR EACH entry IN required_entries:
    IF entry NOT covered in .gitignore:
      findings.append(severity: "MEDIUM", issue: ".gitignore missing: {entry}")

  # Check 3.1b: Secrets protection (compare with gitignore_secrets.template)
  secrets_patterns = [".env", ".env.local", "*.pem", "*.key", "secrets/"]
  FOR EACH pattern IN secrets_patterns:
    IF pattern NOT in .gitignore:
      findings.append(severity: "HIGH", issue: ".gitignore missing secrets: {pattern}",
        principle: "Ignore Files / Secrets")

  # Check 3.1c: IDE/OS entries
  ide_patterns = [".vscode/", ".idea/", "*.swp", ".DS_Store", "Thumbs.db"]
  missing_ide = [p for p in ide_patterns if p NOT covered in .gitignore]
  IF len(missing_ide) > 2:
    findings.append(severity: "LOW", issue: ".gitignore missing IDE/OS: {missing_ide}")

# Check 3.2: .dockerignore
IF exists(Dockerfile) AND NOT exists(.dockerignore):
  findings.append(severity: "MEDIUM", issue: "Dockerfile exists but no .dockerignore",
    recommendation: "Create .dockerignore to reduce build context")
ELIF exists(.dockerignore):
  FOR EACH required IN [node_modules, .git, .env, "*.log"]:
    IF required NOT in .dockerignore:
      findings.append(severity: "LOW", ...)
```

### Phase 4: Framework Convention Compliance

**MANDATORY READ:** Load `references/structure_rules.md` -- use framework-specific section matching detected tech_stack.

```
rules = get_framework_rules(tech_stack, structure_rules.md)
# Returns: {expected_dirs, forbidden_placements, co_location_rules}

# Check 4.1: Expected directories exist
FOR EACH dir IN rules.expected_dirs WHERE dir.required == true:
  IF NOT exists(dir.path):
    findings.append(severity: "MEDIUM", issue: "Expected directory missing: {dir.path}",
      principle: "Framework Convention / {tech_stack.framework}")

# Check 4.2: Source code in wrong locations
FOR EACH rule IN rules.forbidden_placements:
  matches = Glob(rule.glob_pattern, scan_root)
  FOR EACH match IN matches:
    IF match NOT IN rules.exceptions:
      findings.append(severity: "HIGH", issue: "Source file in wrong location: {match}",
        recommendation: "Move to {rule.expected_location}")

# Check 4.3: Co-location rules (React feature folders)
IF tech_stack.framework IN ["react", "vue", "angular", "svelte"]:
  component_dirs = Glob("{scan_root}/**/components/*/")
  colocation_count = 0
  FOR EACH dir IN component_dirs:
    has_test = Glob("{dir}/*.{test,spec}.{ts,tsx,js,jsx}")
    IF has_test: colocation_count += 1

  # Only flag if project already uses co-location (>50%)
  IF colocation_count > len(component_dirs) * 0.5:
    FOR EACH dir IN component_dirs:
      IF NOT has_test_for(dir):
        findings.append(severity: "LOW", issue: "Component missing co-located test: {dir}")
```

### Phase 5: Domain/Layer Organization

```
# Check 5.1: Junk drawer detection
junk_thresholds = structure_rules.junk_drawer_thresholds
FOR EACH dir IN Glob("{scan_root}/**/"):
  dir_name = basename(dir)
  IF dir_name IN junk_thresholds:
    file_count = len(Glob("{dir}/*.*"))
    IF file_count > junk_thresholds[dir_name].max_files:
      findings.append(severity: junk_thresholds[dir_name].severity,
        issue: "Junk drawer directory: {dir} ({file_count} files)",
        principle: "Organization / Module Cohesion",
        recommendation: "Split into domain-specific modules or feature folders")

# Check 5.2: Root directory cleanliness
root_files = Glob("{scan_root}/*")  # Direct children only
source_in_root = [f for f in root_files
  if f.ext IN source_extensions AND basename(f) NOT IN allowed_root_files]
IF len(source_in_root) > 0:
  findings.append(severity: "MEDIUM", issue: "Source files in project root: {source_in_root}",
    recommendation: "Move to src/ or appropriate module directory")

config_in_root = [f for f in root_files if is_config_file(f)]
IF len(config_in_root) > 15:
  findings.append(severity: "LOW",
    issue: "Excessive config files in root ({len(config_in_root)})",
    recommendation: "Move non-essential configs to config/ directory")

# Check 5.3: Consistent module structure across domains
IF domain_mode == "global" AND len(detect_domains(scan_root)) >= 2:
  domains = detect_domains(scan_root)
  structures = {d.name: set(subdirectory_names(d.path)) for d in domains}
  all_subdirs = union(structures.values())
  FOR EACH domain IN domains:
    missing = all_subdirs - structures[domain]
    IF 0 < len(missing) < len(all_subdirs) * 0.5:
      findings.append(severity: "LOW",
        issue: "Inconsistent domain structure: {domain.name} missing {missing}",
        recommendation: "Align domain module structures for consistency")
```

### Phase 6: Naming Conventions

**MANDATORY READ:** Load `references/structure_rules.md` -- use "Naming Convention Rules" section.

```
naming_rules = get_naming_rules(tech_stack)
# Returns: {file_case, dir_case, test_pattern, component_case}

# Check 6.1: File naming consistency
violations = []
FOR EACH file IN Glob("{scan_root}/**/*.{ts,tsx,js,jsx,py,cs,go}"):
  expected_case = naming_rules.file_case
  IF is_component(file) AND NOT matches_case(basename(file), expected_case):
    violations.append(file)

IF len(violations) > 0:
  pct = len(violations) / total_source_files * 100
  severity = "HIGH" if pct > 30 else "MEDIUM" if pct > 10 else "LOW"
  findings.append(severity, issue: "Naming violations: {len(violations)} files ({pct}%)",
    principle: "Naming / {naming_rules.file_case}")

# Check 6.2: Directory naming consistency
dirs = get_all_source_dirs(scan_root)
dir_cases = classify_cases(dirs)  # Count per case style
dominant = max(dir_cases)
inconsistent = [d for d in dirs if case_of(d) != dominant]
IF len(inconsistent) > 0:
  findings.append(severity: "LOW",
    issue: "Inconsistent directory naming: {len(inconsistent)} dirs use mixed case")

# Check 6.3: Test file naming pattern
test_files = Glob("{scan_root}/**/*.{test,spec}.{ts,tsx,js,jsx}")
  + Glob("{scan_root}/**/*_test.{py,go}")
IF len(test_files) > 0:
  patterns_used = detect_test_patterns(test_files)  # .test. vs .spec. vs _test
  IF len(patterns_used) > 1:
    findings.append(severity: "LOW", issue: "Mixed test naming patterns: {patterns_used}",
      recommendation: "Standardize to {dominant_test_pattern}")
```

### Phase 7: Score + Report + Return

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`, `shared/references/audit_scoring.md`, and `shared/templates/audit_worker_report_template.md`.

When summaryArtifactPath is present, write the JSON summary to that exact path.
When summaryArtifactPath is absent, write the standalone runtime summary under .hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json and optionally echo the same summary in structured output.

```
# 7a: Calculate score via shared formula
# 7b: Build report in memory using the shared audit worker template
# 7c: Populate DATA-EXTENDED with:
#   tech_stack
#   dimensions.file_hygiene / ignore_files / framework_conventions / domain_organization / naming_conventions
#   junk_drawers
#   naming_dominant_case
#   naming_violations_pct
# 7d: Write report (atomic single Write call)
Write to {output_dir}/ln-646--{identifier}.md

# 7e: Return summary
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-646--{identifier}.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Scoring

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

Severity mapping:
- **HIGH:** Build artifacts tracked, missing .gitignore, source in wrong location, multiple lock files, missing secrets in .gitignore. **Exception:** Build artifacts in Git LFS -> skip
- **MEDIUM:** Missing framework dirs, junk drawers, temp files, platform remnants, missing stack-specific gitignore entries, naming violations >10%
- **LOW:** IDE/OS patterns missing, inconsistent dir naming, mixed test patterns, minor config issues

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Auto-detect, never assume:** Always detect tech stack before applying framework rules
- **No false positives on conventions:** Apply framework rules ONLY for detected stack
- **Security-first:** Missing secrets in .gitignore = HIGH
- **Complement, not overlap:** Do NOT check import-level layer violations (separate worker scope)
- **Report only, never modify:** Never move/delete files (separate migration/cleanup workers)
- **Reuse platform detection:** Reference platform artifact patterns from references
- **Co-location awareness:** Only flag missing co-location if project already uses the pattern (>50%)
- **Evidence always:** Include file paths for every finding

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] Tech stack detected (from `docs/project/tech_stack.md` or auto-detection)
- [ ] File hygiene checked: build artifacts, temp files, platform remnants, lock files, binaries
- [ ] Ignore files audited: .gitignore completeness, secrets protection, .dockerignore if Dockerfile present
- [ ] Framework conventions applied: expected dirs, forbidden placements, co-location rules
- [ ] Domain/layer organization checked: junk drawers, root cleanliness, cross-domain consistency
- [ ] Naming conventions validated: file/dir/test naming patterns
- [ ] If domain-aware: all Glob scoped to `scan_path`, findings tagged with domain
- [ ] Score calculated per `audit_scoring.md`
- [ ] Report written to `{output_dir}/646-structure[-{domain}].md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Structure rules:** `references/structure_rules.md`
- **Stack detection:** `../ln-700-project-bootstrap/references/stack_detection.md`
- **Platform artifacts:** `../ln-724-artifact-cleaner/references/platform_artifacts.md`
- **Gitignore secrets:** `../ln-733-env-configurator/references/gitignore_secrets.template`
- **Dockerignore baseline:** `../ln-731-docker-generator/references/dockerignore.template`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-28
