---
name: codeql-expert
version: 1.0.0
description: Expert-level CodeQL for static analysis, vulnerability detection, and security code scanning
category: security
tags: [codeql, static-analysis, sast, vulnerability-detection, github-security]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(codeql:*, gh:*)
---

# CodeQL Expert

Expert guidance for CodeQL static analysis, custom query development, vulnerability detection, and integration with CI/CD pipelines.

## Core Concepts

### CodeQL Overview
- Semantic code analysis engine
- Treats code as data (queryable database)
- Supports C/C++, C#, Go, Java, JavaScript/TypeScript, Python, Ruby
- Powers GitHub Code Scanning
- Custom query development with QL language

### CodeQL Workflow
1. Extract code to database
2. Write QL queries
3. Run analysis
4. Review results
5. Fix vulnerabilities
6. Integrate into CI/CD

### Query Types
- Security queries (vulnerabilities)
- Code quality queries (bugs, code smells)
- Compliance queries (coding standards)
- Custom queries (org-specific patterns)

## Installation & Setup

```bash
# Download CodeQL CLI
wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip
unzip codeql-linux64.zip
export PATH="$PATH:/path/to/codeql"

# Clone CodeQL queries
git clone https://github.com/github/codeql.git codeql-repo

# Verify
codeql --version
```

### Create Database

```bash
# JavaScript/TypeScript
codeql database create my-js-db --language=javascript

# Java (requires build)
codeql database create my-java-db \
  --language=java \
  --command="mvn clean package"

# Python
codeql database create my-python-db --language=python

# Multiple languages
codeql database create my-db --db-cluster --language=javascript,python
```

## Writing CodeQL Queries

### Basic Query Structure

```ql
/**
 * @name SQL Injection
 * @description Detects SQL injection vulnerabilities
 * @kind path-problem
 * @problem.severity error
 * @security-severity 9.8
 * @precision high
 * @id js/sql-injection
 * @tags security external/cwe/cwe-089
 */

import javascript
import semmle.javascript.security.dataflow.SqlInjectionQuery
import DataFlow::PathGraph

from Configuration cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "SQL query depends on $@.", source.getNode(), "user input"
```

### Find XSS Vulnerabilities

```ql
/**
 * @name Cross-site scripting
 * @kind path-problem
 */

import javascript
import semmle.javascript.security.dataflow.DomBasedXssQuery
import DataFlow::PathGraph

from Configuration cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "XSS vulnerability due to $@.", source.getNode(), "user input"
```

### Find Hardcoded Credentials

```ql
/**
 * @name Hardcoded credentials
 * @kind problem
 */

import javascript

from StringLiteral str, Variable v
where
  v.getAnAssignedExpr() = str and
  (
    v.getName().toLowerCase().matches("%password%") or
    v.getName().toLowerCase().matches("%apikey%") or
    v.getName().toLowerCase().matches("%secret%")
  ) and
  str.getValue().length() > 8 and
  not str.getValue().matches("TODO%")
select str, "Hardcoded credential: " + v.getName()
```

### Custom Taint Tracking

```ql
/**
 * @name Custom taint tracking
 */

import javascript
import semmle.javascript.dataflow.DataFlow

class CustomTaintTracking extends TaintTracking::Configuration {
  CustomTaintTracking() { this = "CustomTaintTracking" }

  override predicate isSource(DataFlow::Node source) {
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    exists(CallExpr call |
      call.getCalleeName() in ["exec", "eval", "system"]
    |
      sink.asExpr() = call.getAnArgument()
    )
  }

  override predicate isSanitizer(DataFlow::Node node) {
    node = DataFlow::BarrierGuard<StringOps::Validation>::getABarrierNode()
  }
}

from CustomTaintTracking cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "Dangerous operation with $@.", source.getNode(), "user input"
```

## Running CodeQL

```bash
# Analyze database
codeql database analyze my-db \
  --format=sarif-latest \
  --output=results.sarif \
  codeql/javascript-queries:codeql-suites/javascript-security-extended.qls

# Run custom query
codeql query run my-query.ql --database=my-db --output=results.bqrs

# Convert to CSV
codeql bqrs decode results.bqrs --format=csv --output=results.csv
```

### GitHub Actions Integration

```yaml
name: CodeQL Analysis

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write

    strategy:
      matrix:
        language: ['javascript', 'python']

    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: ${{ matrix.language }}
          queries: +security-extended

      - name: Autobuild
        uses: github/codeql-action/autobuild@v2

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
```

## Best Practices

- Start with built-in queries
- Test on small codebases first
- Optimize for performance
- Add clear documentation
- Tune to reduce false positives
- Integrate into CI/CD early

## Resources

- CodeQL Docs: https://codeql.github.com/docs/
- Queries: https://github.com/github/codeql
- Code Scanning: https://docs.github.com/en/code-security/code-scanning
