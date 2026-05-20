---
name: cve-reachability-analyzer
description: Analyze CVE reachability in software repositories by examining how vulnerable dependencies are imported and used. Determines whether vulnerable components, classes, or functions are reachable from project code through call chain analysis, reflection detection, dynamic loading patterns, and configuration-gated behavior. Classifies each CVE as likely reachable, possibly reachable, or likely unreachable with supporting evidence. Use when analyzing security vulnerabilities in dependencies, performing post-disclosure CVE triage, assessing vulnerability impact, or when users ask to analyze CVE reachability, check if vulnerabilities are exploitable, or evaluate dependency security risks.
---

# Post-Disclosure CVE Reachability Analyzer

## Overview

This skill performs static analysis of software repositories to determine whether disclosed CVEs in dependencies are reachable from the project's code. It analyzes import patterns, call chains, dynamic invocation, and configuration to classify each CVE's reachability with evidence-based justification.

## Workflow

### Step 1: Gather Input Information

Collect and validate the required information:

1. **Repository analysis**:
   - Identify programming language(s)
   - Locate dependency files (package.json, requirements.txt, pom.xml, etc.)
   - Understand project structure and entry points

2. **CVE information**:
   - CVE ID and description
   - Affected package name and version range
   - Vulnerable component (function/class/method)
   - Vulnerability type (injection, overflow, etc.)
   - Fixed version

3. **Configuration information** (optional):
   - Feature flags and their states
   - Build profiles (dev/staging/production)
   - Environment variables
   - Runtime configuration files

### Step 2: Verify Dependency Presence

Check if the vulnerable dependency exists in the project:

1. **Parse dependency files**:
   - Read language-specific dependency files (see [language_guide.md](references/language_guide.md))
   - Extract package names and version constraints
   - Build dependency tree (including transitive dependencies)

2. **Version matching**:
   - Compare installed version against vulnerable version range
   - Check if version falls within affected range
   - Identify if fixed version is available

3. **Early exit**:
   - If package not present → **Not Applicable**
   - If version not in vulnerable range → **Not Vulnerable**
   - Otherwise, proceed to Step 3

### Step 3: Analyze Import Patterns

Determine if vulnerable components are imported:

1. **Search for imports**:
   - Find all import/require/using statements for the vulnerable package
   - Check for direct imports of vulnerable function/class
   - Identify wildcard imports that may include vulnerable component
   - Look for aliased imports

2. **Language-specific patterns**:
   - Consult [language_guide.md](references/language_guide.md) for language-specific import syntax
   - Check for framework-specific import mechanisms (DI, auto-loading)

3. **Assessment**:
   - No imports found → Likely unreachable (but check dynamic loading in Step 5)
   - Imports found → Proceed to Step 4

### Step 4: Trace Call Chains

Identify if vulnerable code is invoked:

1. **Direct usage analysis**:
   - Search for call sites of vulnerable function/method
   - Find instantiations of vulnerable classes
   - Locate references to vulnerable symbols

2. **Indirect usage analysis**:
   - Trace calls through wrapper functions
   - Check for framework auto-invocation (middleware, event handlers, DI)
   - Identify callback registrations
   - Look for inheritance/interface implementations

3. **Build call graph**:
   - Map call chains from entry points to vulnerable code
   - Identify all paths that reach vulnerable component
   - Note the depth and complexity of call chains

4. **Use pattern library**:
   - Consult [reachability_patterns.md](references/reachability_patterns.md) for common patterns
   - Match observed patterns to known reachability scenarios

### Step 5: Analyze Dynamic Invocation

Check for dynamic code execution that may reach vulnerable code:

1. **Reflection/metaprogramming**:
   - Search for reflection APIs (Java: `Class.forName()`, Python: `getattr()`, etc.)
   - Check if vulnerable component could be invoked dynamically
   - Assess likelihood based on how constrained the dynamic calls are

2. **Dynamic loading**:
   - Look for dynamic imports (Python: `importlib`, JS: `require(variable)`)
   - Check plugin systems or extension mechanisms
   - Evaluate if vulnerable package could be loaded dynamically

3. **Eval and code generation**:
   - Search for `eval()`, `exec()`, `Function()` constructor
   - Check if vulnerable code could be executed through eval
   - Assess risk based on input sources

### Step 6: Evaluate Configuration Gates

Determine if vulnerable code is gated by configuration:

1. **Feature flags**:
   - Search for feature flag checks around vulnerable code
   - Determine flag states in production (if configuration provided)
   - Assess if flag could be enabled

2. **Environment-specific code**:
   - Check for environment conditionals (dev/staging/prod)
   - Determine which environments execute vulnerable code
   - Focus on production environment

3. **Build-time conditionals**:
   - Look for build profiles, compilation flags
   - Check if vulnerable code is included in production builds
   - Review preprocessor directives

4. **Runtime configuration**:
   - Check for configuration files that control code paths
   - Determine if vulnerable code path is enabled
   - Assess likelihood of configuration changes

### Step 7: Assess Code Path Reachability

Determine if the code path is actually executed:

1. **Dead code detection**:
   - Check for commented-out code
   - Identify unreachable branches (if False, etc.)
   - Find deprecated/unused functions with no callers

2. **Test-only code**:
   - Identify if usage is only in test files
   - Check for test-specific imports or mocks
   - Distinguish production vs. test code paths

3. **Error handling paths**:
   - Determine if vulnerable code is in error handlers
   - Assess likelihood of error conditions
   - Consider if error paths are reachable in practice

4. **Entry point analysis**:
   - Trace from application entry points (main, HTTP handlers, etc.)
   - Verify vulnerable code is on reachable paths from entry points
   - Consider application flow and typical execution paths

### Step 8: Classify Reachability

Apply classification criteria from [cve_analysis.md](references/cve_analysis.md):

**Likely Reachable** - All of:
- Vulnerable package is present in correct version range
- Vulnerable component is imported (directly or via wildcard)
- Vulnerable code is called (directly or indirectly)
- Code path is in production code (not tests/dead code)
- No configuration gates, or gates are enabled in production

**Possibly Reachable** - One or more of:
- Indirect usage through wrappers or frameworks
- Dynamic invocation (reflection, eval, dynamic imports)
- Configuration-gated (unclear if enabled in production)
- Transitive dependency (not direct)
- Framework auto-invocation (DI, middleware)

**Likely Unreachable** - One or more of:
- Package imported but vulnerable component not used
- Code path is test-only or dead code
- Configuration gate is disabled in production
- Vulnerable component in unused module

### Step 9: Generate Output

For each CVE, provide comprehensive assessment:

1. **Classification**: Likely Reachable / Possibly Reachable / Likely Unreachable

2. **Confidence level**: High / Medium / Low

3. **Supporting evidence**:
   - Import locations (file:line)
   - Call paths from entry points to vulnerable code
   - Configuration assumptions
   - Dynamic invocation patterns found

4. **Reasoning**:
   - Explain why this classification was chosen
   - Describe the analysis performed
   - Note any assumptions made

5. **Uncertainty factors**:
   - What is unknown or unclear
   - What additional information would help
   - Limitations of static analysis

6. **Recommendations**:
   - Suggested next steps (upgrade, investigate, monitor)
   - Additional verification needed
   - Mitigation options if upgrade not possible

## Output Format

Structure the output as follows:

```markdown
## CVE Reachability Analysis for [Repository Name]

### Summary
- Total CVEs analyzed: X
- Likely reachable: X
- Possibly reachable: X
- Likely unreachable: X

---

### CVE-YYYY-XXXXX: [Vulnerability Title]

**Package**: package-name
**Affected versions**: < X.Y.Z
**Installed version**: X.Y.Z
**Vulnerable component**: `function_name()` or `ClassName`

**Classification**: Likely Reachable | Possibly Reachable | Likely Unreachable
**Confidence**: High | Medium | Low

#### Evidence

**Dependency presence**:
- Found in: `path/to/dependency-file:line`
- Version X.Y.Z is in vulnerable range (< X.Y.Z)

**Import analysis**:
- Imported in: `path/to/file.ext:line`
  ```language
  import vulnerable_package
  ```

**Call chain**:
1. Entry point: `main()` in `src/app.py:10`
2. Calls: `process_request()` in `src/handlers.py:45`
3. Calls: `vulnerable_function()` in `vulnerable_package:100`

**Configuration**:
- Feature flag: `enable_feature_x` (state: enabled in production)
- Environment: Used in production code path

#### Reasoning

[Explain why this classification was chosen, referencing the evidence above]

#### Uncertainty

[Describe any uncertainties, unknowns, or limitations]

#### Recommendations

- **Priority**: High | Medium | Low
- **Action**: Upgrade to version X.Y.Z | Investigate further | Monitor
- **Mitigation**: [If upgrade not possible, suggest alternatives]

---

[Repeat for each CVE]

### Analysis Notes

**Methodology**:
- Static analysis of codebase
- Dependency tree analysis
- Call graph construction
- Configuration review

**Limitations**:
- Dynamic behavior not fully captured
- Runtime configuration may differ from repository
- Transitive dependencies may have additional paths

**Assumptions**:
- Production configuration matches [source]
- Build profile is [profile name]
- Feature flags state: [list states]
```

## Important Guidelines

1. **Do not assume exploitability**: Reachability ≠ exploitability. Focus on whether code is reached, not whether it can be exploited.

2. **Justify conclusions**: Every classification must be supported by evidence from the codebase.

3. **Be conservative with "Likely Reachable"**: Only use when evidence is strong and clear.

4. **Acknowledge uncertainty**: When analysis is limited by dynamic behavior, configuration, or complexity, state this clearly.

5. **Distinguish test vs. production**: Usage in test files should not count as production reachability.

6. **Consider configuration**: Code may be present but disabled by configuration.

7. **Check transitive dependencies**: Vulnerable code may be reached through multiple layers.

8. **Language-specific analysis**: Use appropriate analysis techniques for each language.

9. **Provide actionable recommendations**: Help users understand what to do next.

10. **Document assumptions**: Clearly state any assumptions about configuration, environment, or build settings.

## Example Usage

**User request**: "Analyze CVE-2024-12345 affecting log4j in my Java project"

**Process**:
1. Parse `pom.xml` to find log4j version
2. Check if version is in vulnerable range
3. Search for log4j imports in Java files
4. Find calls to vulnerable `lookup()` method
5. Trace call chains from HTTP endpoints
6. Check if JNDI lookup is enabled in configuration
7. Classify as "Likely Reachable" with high confidence
8. Provide evidence: import locations, call paths, configuration
9. Recommend immediate upgrade to fixed version

## References

- [reachability_patterns.md](references/reachability_patterns.md) - Common code patterns and their reachability implications
- [language_guide.md](references/language_guide.md) - Language-specific analysis techniques
- [cve_analysis.md](references/cve_analysis.md) - CVE analysis framework and classification criteria

## Limitations

- Static analysis cannot capture all runtime behavior
- Dynamic code execution may not be fully traceable
- Configuration state may differ between repository and production
- Transitive dependencies may have complex interaction patterns
- Obfuscated or minified code is difficult to analyze
- Some framework magic (AOP, bytecode manipulation) may be missed
