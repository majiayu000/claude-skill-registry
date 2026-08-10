---
name: static-application-security-testing
description: Analyze source code for security vulnerabilities using static analysis tools, custom rules, and CI-integrated scanning pipelines. Use when the user requests static application security testing or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Static Application Security Testing

This skill enables the agent to perform Static Application Security Testing (SAST) on source code repositories to detect security vulnerabilities without executing the application. The agent selects appropriate analysis tools based on the project's language, runs scans with relevant rule sets, triages findings to separate true positives from false positives, and integrates results into CI/CD pipelines. SAST catches issues such as SQL injection, cross-site scripting, hardcoded secrets, insecure deserialization, and cryptographic misuse early in the development lifecycle.

## Workflow

1. **Detect Languages and Frameworks** — Analyze the repository to determine primary languages (Python, JavaScript, Java, Go, C#, etc.) and frameworks in use. This determines which SAST tools and rule sets are applicable. Check for existing tool configurations like `.semgrep.yml`, `codeql` query packs, or `.bandit` config files.

2. **Select and Configure SAST Tools** — Choose the appropriate tools for the detected stack. Use Semgrep for multi-language pattern matching, CodeQL for deep semantic analysis, Bandit for Python-specific checks, and ESLint security plugins for JavaScript/TypeScript. Load built-in security rule sets and any project-specific custom rules.

3. **Execute Static Analysis** — Run the selected tools against the codebase. Capture all findings including the vulnerability type, affected file and line number, severity level, CWE identifier, and a description of the issue. For large codebases, parallelize scans across multiple tools simultaneously.

4. **Triage and Deduplicate Findings** — Merge results from multiple tools, remove duplicate detections of the same issue, and classify findings as true positive, false positive, or needs-review. Use contextual analysis such as checking whether a flagged SQL string actually reaches a database driver to reduce noise.

5. **Generate Report with Fix Suggestions** — Produce a structured findings report grouped by severity and category. Include the vulnerable code snippet, an explanation of the risk, a suggested fix with corrected code, and references to relevant CWE entries and OWASP categories.

6. **Integrate into CI Pipeline** — Configure the scan to run on every pull request or push to protected branches. Set quality gates that block merges when critical or high-severity findings are introduced. Output results in SARIF format for integration with GitHub Code Scanning, GitLab SAST, or SonarQube.

## Supported Technologies

- **Multi-language**: Semgrep (Python, JS/TS, Java, Go, Ruby, C#, PHP, Kotlin, Rust)
- **Deep Semantic Analysis**: CodeQL (Java, JavaScript, Python, C/C++, C#, Go, Ruby)
- **Python**: Bandit, Pylint security checkers
- **JavaScript/TypeScript**: ESLint (eslint-plugin-security, eslint-plugin-no-secrets), njsscan
- **Java**: SpotBugs with Find Security Bugs plugin, PMD
- **Output Formats**: SARIF, JSON, JUnit XML, Markdown
- **CI Platforms**: GitHub Actions, GitLab CI, Jenkins, Azure DevOps

## Usage

Provide the agent with the path to a source code repository. Optionally specify target languages, custom rule files, or a CI platform for pipeline integration. The agent will run the appropriate SAST tools and deliver a prioritized findings report.

**Prompt example:**

```
Run SAST on the Python application in /app using Semgrep and Bandit. Flag any SQL injection, hardcoded secrets, and insecure deserialization. Output results in SARIF format for GitHub Code Scanning.
```

## Examples

### Example 1: Semgrep Scan on a Python Flask Application

**Command:**

```bash
semgrep scan --config=p/owasp-top-ten --config=p/python --json --output=semgrep-results.json /app
```

**Findings (excerpt):**

```
┌─────────────────────────────────────────────────────────────────┐
│ python.flask.security.injection.sql-injection-with-format-string │
│ Severity: ERROR  │  CWE-89  │  OWASP A03:2021                  │
├─────────────────────────────────────────────────────────────────┤
│ /app/routes/users.py:42                                         │
│                                                                 │
│   40│   def search_users(name):                                 │
│   41│       query = f"SELECT * FROM users WHERE name = '{name}'"│
│   42│       result = db.execute(query)                          │
│                                                                 │
│ Fix: Use parameterized queries instead of string formatting.    │
├─────────────────────────────────────────────────────────────────┤
│ python.lang.security.audit.hardcoded-password                   │
│ Severity: WARNING  │  CWE-798  │  OWASP A07:2021               │
├─────────────────────────────────────────────────────────────────┤
│ /app/config.py:11                                               │
│                                                                 │
│   10│   class Config:                                           │
│   11│       DB_PASSWORD = "SuperSecret123!"                     │
│   12│       JWT_SECRET = "my-jwt-secret"                        │
│                                                                 │
│ Fix: Load secrets from environment variables or a secrets       │
│      manager, never hardcode them in source files.              │
└─────────────────────────────────────────────────────────────────┘
```

**Fixed code for the SQL injection finding:**

```python
# BEFORE — vulnerable to SQL injection
def search_users(name):
    query = f"SELECT * FROM users WHERE name = '{name}'"
    result = db.execute(query)
    return result

# AFTER — parameterized query
def search_users(name):
    query = "SELECT * FROM users WHERE name = :name"
    result = db.execute(text(query), {"name": name})
    return result
```

### Example 2: CodeQL Query for Insecure Deserialization in Java

**Custom CodeQL query (`insecure-deserialization.ql`):**

```ql
/**
 * @name Insecure deserialization of untrusted data
 * @description Deserializing data from an untrusted source without validation
 *              can lead to remote code execution.
 * @kind path-problem
 * @problem.severity error
 * @id java/insecure-deserialization
 * @tags security
 *       cwe-502
 *       owasp-a08
 */

import java
import semmle.code.java.dataflow.TaintTracking
import semmle.code.java.security.UnsafeDeserializationQuery

from UnsafeDeserializationConfig config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "Untrusted data from $@ is deserialized here without validation.", source.getNode(),
  "user-controlled input"
```

**Running the query:**

```bash
codeql database create java-db --language=java --source-root=/app
codeql database analyze java-db insecure-deserialization.ql --format=sarif-latest --output=codeql-results.sarif
```

**Sample finding:**

```
/app/src/main/java/com/example/api/ImportController.java:35
  ObjectInputStream ois = new ObjectInputStream(request.getInputStream());
  Object obj = ois.readObject();  // CWE-502: untrusted deserialization

Fix: Replace ObjectInputStream with a safe alternative like JSON deserialization
     with explicit type binding, or use an allowlist-based ObjectInputFilter.
```

## Best Practices

- **Shift left — scan on every pull request** — catching vulnerabilities during code review is 10-100x cheaper than finding them in production. Configure SAST as a required CI check on all protected branches.
- **Tune rules to reduce false positives** — start with a curated security rule set (e.g., Semgrep `p/owasp-top-ten`) rather than enabling all rules. Add suppressions for confirmed false positives with documented justification.
- **Layer multiple tools** — no single SAST tool catches everything. Combine pattern-based tools (Semgrep) with semantic analysis tools (CodeQL) for broader coverage. Each tool has different strengths.
- **Create custom rules for your codebase** — write project-specific Semgrep or CodeQL rules to enforce internal security patterns, such as ensuring all database queries go through a sanitizing wrapper function.
- **Use SARIF for unified reporting** — the Static Analysis Results Interchange Format is supported by GitHub, GitLab, Azure DevOps, and SonarQube, enabling a single dashboard for all SAST findings regardless of the tool that produced them.

## Safety Boundaries

- Work only on systems the user owns or is explicitly authorized to assess, and record the approved scope before testing.
- Start with passive or read-only inspection. Obtain explicit approval before active scanning, exploitation, load generation, or disruptive remediation.
- Never expose secrets, extract unrelated data, weaken production controls, or expand beyond the approved targets.
- Preserve evidence, minimize impact, stop on instability, and provide rollback or containment steps for every material change.

## Edge Cases

- **Generated or vendored code** — SAST tools will flag issues in auto-generated protobuf stubs, vendored dependencies, or migration files. Exclude these paths from scanning using `.semgrepignore` or CodeQL path filters to avoid noise.
- **Template languages and DSLs** — Jinja2 templates, ERB, JSX, and other templating languages may not be fully parsed by all SAST tools. Use tool-specific plugins or supplementary scanners that understand the template syntax.
- **False positives in test code** — test files often contain intentionally insecure patterns (e.g., hardcoded test credentials, raw SQL for test setup). Configure separate rule sets or severity thresholds for test directories.
- **Large monorepos with slow scan times** — full CodeQL analysis on a million-line monorepo can take over an hour. Use incremental analysis, scan only changed files on PRs, and run full scans on a nightly schedule.
- **Secrets in historical commits** — SAST tools scan the current working tree, not Git history. Pair SAST with secret scanning tools like Gitleaks or TruffleHog to detect credentials committed in past revisions and still present in the Git log.
