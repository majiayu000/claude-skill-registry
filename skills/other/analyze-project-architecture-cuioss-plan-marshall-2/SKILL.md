---
name: analyze-project-architecture
description: LLM-based architectural analysis that transforms raw project data into meaningful structure
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Analyze Project Architecture Skill

## Enforcement Rules

### Script Execution
1. Run scripts EXACTLY as documented - no improvisation
2. All scripts use: `python3 .plan/execute-script.py {notation} ...`

### Workflow Behavior
1. Complete all steps in sequence
2. After each module enrichment → proceed to next module
3. Only stop when all modules are enriched

### Prohibited Actions
- Skipping modules without enrichment
- Leaving `responsibility` or `key_packages` empty
- Omitting `--reasoning` parameters (traceability is required)
- Summarizing what you're about to do instead of doing it

---

## What This Skill Provides

**Discovery**: Run extension API to collect raw module data

**Enrichment**: LLM analyzes documentation and code to add semantic understanding

**Persistence**: Store enriched data for solution-outline consumption

---

## Scripts

| Script | Notation | Purpose |
|--------|----------|---------|
| architecture | `plan-marshall:analyze-project-architecture:architecture` | Main CLI for all operations |

### Command Groups

| Group | API | Purpose |
|-------|-----|---------|
| `discover`, `init` | [manage-api](standards/manage-api.md) | Setup commands |
| `derived`, `derived-module` | [manage-api](standards/manage-api.md) | Read raw discovered data |
| `enrich *` | [manage-api](standards/manage-api.md) | Write enrichment data |
| `info`, `module`, `modules`, `commands`, `resolve` | [client-api](standards/client-api.md) | Consumer queries |

---

## Step 1: Discover Modules

Run extension API discovery:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture discover --force
```

**Output**: `.plan/project-architecture/derived-data.json`

Always overwrites existing data to ensure fresh discovery.

---

## Step 1.5: Review Build Profiles (Maven Only)

**Condition**: Only if any module has `build_systems` containing `maven`.

Check derived-data.json for NO-MATCH-FOUND profiles in `modules.*.metadata.profiles`.

**If Maven modules exist AND unmatched profiles found**:

Load skill `pm-dev-java:manage-maven-profiles` and follow its workflow to:
1. Ask user about each unmatched profile (Ignore/Skip/Map)
2. Apply configuration via `run_config` commands
3. Re-run discovery to apply changes

**If no Maven modules OR no unmatched profiles** → Skip to Step 2.

---

## Step 2: Initialize Enrichment File

Check if `llm-enriched.json` already exists:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture init --check
```

**If file exists**, ask user:

```yaml
AskUserQuestion:
  question: "llm-enriched.json already exists. What do you want to do?"
  header: "Enrichment"
  options:
    - label: "Skip"
      description: "Keep existing enrichments, continue to next step"
    - label: "Replace"
      description: "Discard existing enrichments, start fresh"
  multiSelect: false
```

**Based on user choice**:

| Choice | Command |
|--------|---------|
| Skip | Proceed to Step 3 |
| Replace | `architecture init --force` |

**If file does not exist**:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture init
```

This creates empty enrichment structure for each module found in derived-data.json.

---

## Step 3: Load Discovered Data

Load the raw discovered data in TOON format:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture derived
```

**Output (TOON)**:
```toon
project:
  name: {project-name}
  root: {project-root}

modules[N]{name,path,build_systems,readme,description}:
module-a,module-a,maven,module-a/README.adoc,Description from pom
module-b,module-b,maven,,
module-c,module-c,maven+npm,module-c/README.md,
```

The output shows raw extension API discovery results:
- Module names and paths
- Build systems (joined with `+` for hybrid)
- README paths (if detected)
- Descriptions (from build files, if available)

Read referenced READMEs for modules that have them:
```bash
Read {readme path from derived output}
```

---

## Step 4: Enrich Project Description

Based on the README and module descriptions, write a 1-2 sentence project description.

**Always provide reasoning** to document the source:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  enrich project --description "{extracted project description}" \
  --reasoning "{source: README.md introduction | inferred from module names | pom.xml description}"
```

**Reasoning examples**:
- "From README.md first paragraph"
- "Inferred from module structure and pom.xml descriptions"
- "Aggregated from child module responsibilities"

---

## Step 5: Get Module List

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture modules
```

**Output (TOON)**:
```toon
modules[N]:
  - module-a
  - module-b
  - ...
```

---

## Step 6: Enrich Each Module

**For each module in the list**, execute Steps 6a-6e:

### Step 6a: Read Module Documentation

Get raw discovered data for the module:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture derived-module --name {module-name}
```

**Output (TOON)**:
```toon
module:
  name: {module-name}
  path: {module-path}
  build_systems: maven

paths:
  readme: {module}/README.adoc
  sources[N]:
    - src/main/java
  tests[N]:
    - src/test/java

metadata:
  description: {from build file if available}
  packaging: jar

packages[N]{name,path,package_info}:
com.example.core,src/main/java/com/example/core,src/main/java/com/example/core/package-info.java
com.example.util,src/main/java/com/example/util,

dependencies[N]:
  - groupId:artifactId:scope
```

Read the referenced documentation:
```bash
Read {paths.readme}
Read {package_info path}  # for packages with package_info
```

If no documentation available, sample 2-3 source files from packages.

### Step 6b: Determine Module Purpose

Analyze to determine `purpose` value:

| Signal | Purpose Value |
|--------|---------------|
| packaging=jar, no runtime deps | `library` |
| Quarkus extension annotations | `extension` |
| Build-time processor, deployment | `deployment` |
| Main class, application entry | `runtime` |
| packaging=pom at root | `parent` |
| Only test files | `integration-tests` |
| JMH benchmarks | `benchmark` |

### Step 6c: Write Module Responsibility

Write 1-3 sentences describing what the module does.

**Good examples**:
- "Validates JWT tokens from multiple identity providers using a pipeline approach"
- "Provides Quarkus CDI integration for the core validation library"
- "Coordinates build configuration for all child modules"

**Bad examples** (avoid):
- "Core module" (too vague)
- "Main package for processing" (says nothing)

**Always provide reasoning** for traceability:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  enrich module --name {module-name} \
  --responsibility "{1-3 sentence description}" \
  --responsibility-reasoning "{source: README overview | package-info.java | inferred from class names}" \
  --purpose {purpose-value} \
  --purpose-reasoning "{signal: packaging=jar with no main class | Quarkus extension annotations}"
```

**Reasoning examples**:
- Responsibility: "From module README.adoc overview section"
- Responsibility: "Inferred from package-info.java and primary class names"
- Purpose: "packaging=jar, no runtime dependencies, no main class"
- Purpose: "Contains @BuildStep annotations indicating Quarkus deployment module"

### Step 6d: Identify Key Packages

Select 2-4 architecturally significant packages per module.

For each key package, write 1-2 sentence description:

**Good examples**:
- "Provides the token validation pipeline with pluggable validators"
- "Contains domain models for tokens, claims, and validation results"

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  enrich package --module {module-name} \
  --package {full.package.name} \
  --description "{1-2 sentence description}"
```

Repeat for each key package (2-4 packages).

### Step 6d-2: Identify Key Dependencies

From the derived-module output (Step 6a), analyze the `dependencies` list to identify architecturally significant dependencies.

**Selection criteria** - Include dependencies that:
- Define the module's core technology (frameworks, runtime libraries)
- Provide essential APIs the module builds upon
- Define the runtime contract (provided-scope dependencies like `quarkus-core`, `servlet-api`)
- Are unique to this module's purpose (not ubiquitous across all modules)

**Exclude from key dependencies**:
- Ubiquitous utilities (commons-lang, guava, slf4j) unless central to module purpose
- Pure code-generation tools (lombok) that don't define architecture
- Standard test frameworks (junit, mockito) - implied by testing profile
- Transitive dependencies not directly used

**Include despite scope**:
- Provided-scope framework APIs (these define the runtime contract)
- Test-scope if architecturally distinctive (testcontainers, wiremock, arquillian)
- Compile-scope annotation libraries that define contracts (jspecify, checker-qual)

**For multi-module projects**, also identify `internal_dependencies`:
- Other modules in this project that this module depends on
- Look for dependencies with same groupId as the project

**Good examples**:
- `io.quarkus:quarkus-core` (provided) - Defines runtime framework contract
- `jakarta.servlet-api` (provided) - Defines servlet container contract
- `org.eclipse.microprofile.jwt:microprofile-jwt-auth-api` - Core API this module implements
- `org.jspecify:jspecify` - Defines null-safety contract
- `org.testcontainers:testcontainers` (test) - Architecturally distinctive testing approach

**Bad examples** (exclude):
- `org.junit.jupiter:junit-jupiter-api` - Standard test framework, implied by profile
- `org.projectlombok:lombok` - Code generation tool, doesn't define architecture
- `org.slf4j:slf4j-api` - Ubiquitous logging facade
- `org.apache.commons:commons-lang3` - Generic utility, not distinctive

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  enrich dependencies --module {module-name} \
  --key "{comma-separated list of groupId:artifactId}" \
  --internal "{comma-separated list of internal module names}" \
  --reasoning "{why these dependencies are architecturally significant}"
```

**Example**:
```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  enrich dependencies --module oauth-sheriff-core \
  --key "io.quarkus:quarkus-core,org.eclipse.microprofile.jwt:microprofile-jwt-auth-api" \
  --reasoning "Quarkus runtime and MicroProfile JWT API define the module's integration contract"
```

For single-module projects or leaf modules with no internal dependencies, omit `--internal`.

### Step 6e: Determine Skills by Profile

Assign skills organized by execution profile (implementation, unit-testing, integration-testing, benchmark-testing, documentation).

**Step 6e.1: List Available Domains**

Get all configured skill domains:

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  skill-domains list
```

**Output (TOON)**:
```toon
status: success
domains:
  - system
  - java
  - javascript
  - plan-marshall-plugin-dev
count: 4
```

**Step 6e.2: Determine Applicable Domain**

Based on the module analysis from Steps 6a-6d, determine which domain applies.

**Signals to consider** (from derived-module output and documentation):
- Source file extensions (`.java`, `.kt`, `.js`, `.ts`)
- Dependencies (groupId/artifactId patterns, npm packages)
- Framework annotations in code
- Build file configurations
- Module description and purpose

**Examples of domain applicability**:

| Signal | Domain |
|--------|--------|
| Java sources, javax/jakarta imports | `java` |
| Kotlin sources, kotlin-stdlib | `java` (or future `kotlin`) |
| JavaScript/TypeScript sources | `javascript` |
| plugin.json, marketplace structure | `plan-marshall-plugin-dev` |
| Quarkus dependencies | `java` |
| CUI dependencies (`de.cuioss:*`) | `java` + `java-cui` (merged skills) |
| `doc/` or `docs/` with `.adoc` files | `documentation` (as additional profile) |

**Step 6e.3: Get Skills by Profile**

For the applicable domain, get the pre-assembled skills by profile:

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  get-skills-by-profile --domain {domain-key}
```

**Output (TOON)**:
```toon
status: success
domain: java
skills_by_profile:
  implementation:
    - pm-dev-java:java-core
    - pm-dev-java:java-null-safety
    - pm-dev-java:java-lombok
    - pm-dev-java:java-cdi
    - pm-dev-java:java-maintenance
  unit-testing:
    - pm-dev-java:java-core
    - pm-dev-java:java-null-safety
    - pm-dev-java:java-lombok
    - pm-dev-java:junit-core
    - pm-dev-java:junit-integration
  integration-testing:
    - pm-dev-java:java-core
    - pm-dev-java:java-null-safety
    - pm-dev-java:java-lombok
    - pm-dev-java:junit-core
    - pm-dev-java:junit-integration
  benchmark-testing:
    - pm-dev-java:java-core
    - pm-dev-java:java-null-safety
    - pm-dev-java:java-lombok
    - pm-dev-java:junit-core
    - pm-dev-java:junit-integration
```

**Step 6e.4: Filter Skills Based on Module Signals**

Optionally filter the skills based on module signals:

| Module Signal | Action |
|---------------|--------|
| No CDI annotations | Remove `java-cdi` from implementation |
| No Lombok annotations | Remove `java-lombok` from all profiles |
| No integration tests (*IT.java) | Remove integration-testing profile entirely |
| No benchmarks (*Benchmark.java) | Remove benchmark-testing profile entirely |

**Step 6e.4b: Add Documentation Profile (Cross-Domain)**

If module has AsciiDoc documentation, add `documentation` profile from `documentation` domain:

**Detection**: Check if module has `doc/` or `docs/` directory with `.adoc` files.

```bash
# Check for AsciiDoc docs in module
ls {module-path}/doc/*.adoc 2>/dev/null || ls {module-path}/docs/*.adoc 2>/dev/null
```

**If `.adoc` files found**:

1. Get documentation skills:
```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  get-skills-by-profile --domain documentation
```

2. Add `documentation` profile to the module's `skills_by_profile`:
```json
{
  "implementation": [...],
  "module_testing": [...],
  "documentation": ["pm-documents:ref-documentation", "pm-documents:manage-adr", ...]
}
```

**Key principle**: Documentation is a separate task type (like testing), not a variant of implementation. A module can have both `implementation` AND `documentation` profiles.

**Step 6e.4c: Add CUI Extension Domain (Java Only)**

If module uses CUI libraries, add `java-cui` domain alongside `java`:

**Detection signals** (from module dependencies):
- `de.cuioss:cui-java-tools` or `de.cuioss:cui-*`
- `de.cuioss.portal:*` or `de.cuioss.jsf:*`

**If CUI dependencies found**:

1. Get CUI-specific skills:
```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  get-skills-by-profile --domain java-cui
```

2. Merge with base java skills in `skills_by_profile`:
```json
{
  "implementation": {
    "defaults": [
      {"skill": "pm-dev-java:java-core", "description": "..."},
      {"skill": "pm-dev-java-cui:cui-logging", "description": "..."}
    ],
    "optionals": [
      {"skill": "pm-dev-java:java-cdi", "description": "..."},
      {"skill": "pm-dev-java-cui:cui-http", "description": "..."}
    ]
  }
}
```

**Key principle**: `java-cui` is an ADDITIVE domain that extends `java`. Both domains contribute skills to the same profiles. The java-cui domain does NOT provide its own triage - it relies on `pm-dev-java:ext-triage-java`.

**Step 6e.5: Apply Skills by Profile**

**Include reasoning** about filtering decisions:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  enrich skills-by-profile --module {module-name} \
  --skills-json '{"implementation": ["pm-dev-java:java-core", "pm-dev-java:java-cdi"], "module_testing": ["pm-dev-java:java-core", "pm-dev-java:junit-core"]}' \
  --reasoning "{filtering applied: removed java-lombok (no @Data annotations found), kept java-cdi (CDI beans present)}"
```

**Reasoning examples**:
- "Base java domain, no filtering applied"
- "Removed java-cdi (no CDI annotations), removed integration_testing (no *IT.java files)"
- "Added cui-testing-http based on MockWebServer test dependency"
- "Added documentation profile (module has doc/*.adoc files)"

The `skills_by_profile` structure flows to:
1. **solution-outline**: Copies to deliverable as `skills-implementation`, `skills-testing`, etc.
2. **task-plan**: Uses pre-resolved skills when creating tasks (no runtime lookup)

---

## Step 7: Verify Enrichment

After all modules are enriched, verify completeness:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture info
```

Check that:
- [ ] Every module has non-empty `responsibility`
- [ ] Every module has valid `purpose`
- [ ] Every module has 2-4 `key_packages` with descriptions
- [ ] Every module has `key_dependencies` identified (unless module has no compile-scope deps)
- [ ] Every module has `skills_by_profile` with at least `implementation` and `unit-testing` profiles

If any module is incomplete → return to Step 6 for that module.

---

## Step 8: Output Summary

Display completion summary:

```
Architecture analysis complete.

Project: {project name}
Modules enriched: {count}

Files created:
  - .plan/project-architecture/derived-data.json
  - .plan/project-architecture/llm-enriched.json

Next steps:
  - Solution outline will use this data for placement decisions
  - Run 'architecture.py module --name X' to query module details
```

---

## Error Handling

### Extension API Not Available

```
Error: Extension API not found.

Resolution:
1. Verify domain bundles installed (pm-dev-java, pm-dev-frontend)
2. Run /marshall-steward to configure project
3. Re-run this skill
```

### No Modules Discovered

```
Error: No modules found in project.

Resolution:
1. Verify project has build files (pom.xml, package.json, build.gradle)
2. Check that domain bundle matches project type
3. Re-run discovery
```

### Documentation Not Found

If module has no README or package-info:
1. Analyze source code directly
2. Check parent module for context
3. Note in responsibility: "Inferred from source analysis"

---

## Deferred Loading

For detailed specifications, load on demand:

| Reference | When to Load |
|-----------|--------------|
| [manage-api.md](standards/manage-api.md) | Manage commands (setup, read raw, enrich) |
| [client-api.md](standards/client-api.md) | Client commands (merged data for consumers) |
| [architecture-persistence.md](standards/architecture-persistence.md) | Field schemas and formats |
| [architecture-workflow.md](standards/architecture-workflow.md) | Workflow phase details |
| [documentation-sources.md](standards/documentation-sources.md) | Reading strategy details |
| `pm-dev-java:manage-maven-profiles` | Maven profile classification (Step 1.5) |

---

## Integration

This skill is invoked by:
- **marshall-steward wizard** Step 6b (after discovery)
- **Direct activation** when regenerating project structure

Output is consumed by:
- **solution-outline** Step 0 (module placement)
- **task-plan** (command resolution)

---

## Post-Implementation Enrichment

During verification phase or after implementation, capture learnings:

### Add Implementation Tip

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  enrich tip --module {module-name} --tip "Use @ApplicationScoped for singleton services"
```

### Add Learned Insight

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  enrich insight --module {module-name} --insight "Heavy validation happens in boundary layer"
```

### Add Best Practice

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture \
  enrich best-practice --module {module-name} --practice "Always validate tokens before extracting claims"
```

These accumulate over time and are included in module output for future reference.
