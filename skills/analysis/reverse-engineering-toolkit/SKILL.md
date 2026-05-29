---
name: reverse-engineering-toolkit
description: Understand undocumented systems through static/dynamic analysis, dependency mapping, and pattern recognition
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, WebFetch]
---

# Reverse Engineering Toolkit

## Purpose

This skill enables you to understand systems without documentation by analyzing code structure, runtime behavior, dependencies, and design patterns. Use this when facing:

- Undocumented legacy codebases requiring modernization
- Third-party APIs with incomplete specifications
- Lost or outdated design documentation
- Security audits of closed-source systems
- Onboarding to unfamiliar codebases

## When to Use This Skill

**Use reverse engineering when**:
- Documentation is missing, outdated, or incomplete
- System behavior needs to be understood through observation
- Dependencies and coupling need to be visualized
- Design patterns need to be identified and cataloged
- API contracts need to be inferred from implementation
- Legacy code requires understanding before refactoring

**Do NOT use when**:
- Good documentation already exists (read it instead!)
- Source code is unavailable (different techniques needed)
- Simple codebase can be understood by reading
- Time constraints don't allow deep analysis

## Quick Start: 4-Step Process

### 1. Discover
Identify what exists in the system:
```bash
# Find all source files
find . -type f -name "*.py" -o -name "*.js" -o -name "*.java"

# Count lines of code
cloc .

# Identify entry points
grep -r "main\|app\|server" --include="*.py"
```

### 2. Map
Build a structural understanding:
```python
# Extract imports and dependencies
import ast
with open('module.py') as f:
    tree = ast.parse(f.read())
    imports = [node for node in ast.walk(tree) if isinstance(node, ast.Import)]
```

### 3. Analyze
Understand behavior and patterns:
```bash
# Trace execution
strace -o trace.log ./program

# Analyze function calls
python -m pycallgraph graphviz -- ./script.py
```

### 4. Document
Capture findings:
- Dependency graphs (Mermaid diagrams)
- Design pattern catalog
- API documentation
- Architecture diagrams

## Core Patterns Overview

### Pattern 1: Static Code Analysis
**Purpose**: Understand code structure without execution
**Tools**: tree-sitter, AST parsers, ctags, grep
**Output**: Symbol tables, call graphs, class hierarchies
**See**: PATTERNS.md → Static Code Analysis

### Pattern 2: Dynamic Analysis & Tracing
**Purpose**: Observe runtime behavior and data flow
**Tools**: strace, ltrace, debuggers, profilers
**Output**: Execution traces, memory snapshots, performance profiles
**See**: PATTERNS.md → Dynamic Analysis & Tracing

### Pattern 3: Dependency Graph Extraction
**Purpose**: Map relationships between modules, files, functions
**Tools**: import analyzers, call graph generators, visualization tools
**Output**: Dependency graphs, coupling metrics, circular dependency detection
**See**: PATTERNS.md → Dependency Graph Extraction

### Pattern 4: Design Pattern Recognition
**Purpose**: Identify architectural and code patterns
**Tools**: Pattern matching algorithms, structural analysis
**Output**: Pattern catalog (Singleton, Factory, Observer, etc.)
**See**: PATTERNS.md → Design Pattern Recognition

### Pattern 5: Documentation Generation
**Purpose**: Auto-generate documentation from code analysis
**Tools**: Sphinx, JSDoc, Doxygen, custom generators
**Output**: API docs, architecture diagrams, onboarding guides
**See**: PATTERNS.md → Documentation Generation

## Detailed Resources

- **KNOWLEDGE.md**: Theory, concepts, tools comparison, academic references
- **PATTERNS.md**: Implementation details for all 5 patterns with architecture considerations
- **EXAMPLES.md**: Working code examples for each pattern with real-world use cases
- **GOTCHAS.md**: Common pitfalls, debugging strategies, language-specific challenges
- **REFERENCE.md**: Tool command references, APIs, configuration options

## Top 3 Gotchas

### 1. Obfuscated or Minified Code
**Problem**: Code intentionally made hard to understand
**Solution**: Use deobfuscation tools, focus on runtime behavior instead
**See**: GOTCHAS.md → Obfuscated Code Challenges

### 2. Large Codebase Performance
**Problem**: Analysis tools timeout or consume excessive memory
**Solution**: Incremental analysis, sampling, focus on critical paths
**See**: GOTCHAS.md → Large Codebase Performance Issues

### 3. Dynamic Language Challenges
**Problem**: Type information and call targets unknown until runtime
**Solution**: Combine static analysis with runtime instrumentation
**See**: GOTCHAS.md → Dynamic Language Challenges

## Quick Reference Card

### Analysis Approach Selection

| Situation | Approach | Primary Tools |
|-----------|----------|--------------|
| Need overview | Static analysis | tree-sitter, grep, cloc |
| Understand behavior | Dynamic tracing | strace, debugger |
| Map dependencies | Graph extraction | import analyzers, graphviz |
| Find patterns | Pattern recognition | AST matching, structural analysis |
| Create docs | Auto-documentation | Sphinx, Doxygen, custom scripts |

### Common Commands

```bash
# Quick structure overview
tree -L 3 -I 'node_modules|*.pyc'

# Find entry points
grep -r "if __name__" --include="*.py"
grep -r "function main" --include="*.js"

# Extract function definitions
ctags -R --fields=+n --languages=python .

# Generate call graph
python -m pycallgraph graphviz -- script.py

# Trace system calls
strace -f -e trace=file ./program 2>&1 | grep open

# Dependency analysis (Python)
pydeps module.py --show-deps

# Find design patterns
grep -r "class.*Singleton\|getInstance\|factory" --include="*.py"
```

### Analysis Workflow

```
1. Reconnaissance
   ├─ Identify languages, frameworks, build system
   ├─ Locate entry points (main, server, app)
   └─ Estimate codebase size and complexity

2. Static Analysis
   ├─ Parse AST for all modules
   ├─ Extract symbols (classes, functions, variables)
   ├─ Build call graph and class hierarchy
   └─ Identify imports and dependencies

3. Dynamic Analysis
   ├─ Run with instrumentation
   ├─ Trace execution paths
   ├─ Monitor system calls and network traffic
   └─ Profile performance hotspots

4. Pattern Analysis
   ├─ Identify structural patterns (classes, inheritance)
   ├─ Detect design patterns (Singleton, Factory, etc.)
   ├─ Find architectural patterns (MVC, microservices)
   └─ Catalog anti-patterns and code smells

5. Documentation
   ├─ Generate dependency graphs
   ├─ Create architecture diagrams
   ├─ Write API documentation
   └─ Build onboarding guide
```

### Tool Selection Matrix

| Language | Static Analysis | Dynamic Analysis | Dependency Graph |
|----------|----------------|------------------|------------------|
| Python | ast, tree-sitter | pdb, py-spy | pydeps, pipdeptree |
| JavaScript | esprima, acorn | Chrome DevTools | madge, dependency-cruiser |
| Java | JavaParser, ANTLR | jdb, VisualVM | jdeps, gradle dependencies |
| C/C++ | libclang, cppcheck | gdb, valgrind | cinclude2dot, graphviz |
| Go | go/ast, go/parser | delve, pprof | go mod graph |
| Rust | syn, rust-analyzer | lldb, cargo-flamegraph | cargo tree |

## Integration with Agents

### Primary Agent: code-archaeologist
This skill is designed for use by the `code-archaeologist` agent, which specializes in understanding legacy and undocumented systems.

**Agent delegates to this skill for**:
- Code structure analysis
- Dependency mapping
- Pattern recognition
- Documentation generation

**Agent retains responsibility for**:
- User interaction and requirements gathering
- High-level strategy and planning
- Results presentation and visualization
- Integration with other analysis workflows

### Other Compatible Agents
- `security-auditor`: Security-focused reverse engineering
- `integration-engineer`: API behavior analysis
- `api-consumer-advocate`: Protocol reverse engineering
- `refactoring-lead`: Understanding before refactoring

## Success Criteria

You've successfully applied this skill when you can:
- [ ] Explain what the system does without original documentation
- [ ] Generate accurate dependency graphs
- [ ] Identify and catalog design patterns used
- [ ] Create functional documentation for onboarding
- [ ] Map data flow through the system
- [ ] Identify architectural boundaries and modules

## Related Skills

- **codebase-onboarding-analyzer**: Uses reverse engineering for rapid codebase understanding
- **architecture-evaluation-framework**: Analyzes system architecture (reverse engineering identifies it)
- **gap-analysis-framework**: Identifies what's missing (reverse engineering shows what exists)
- **security-scanning-suite**: Security-focused analysis (uses reverse engineering techniques)

## References

### Books
- "Reversing: Secrets of Reverse Engineering" by Eldad Eilam
- "The IDA Pro Book" by Chris Eagle
- "Practical Binary Analysis" by Dennis Andriesse

### Tools Documentation
- tree-sitter: https://tree-sitter.github.io/tree-sitter/
- Ghidra: https://ghidra-sre.org/
- radare2: https://rada.re/n/
- Binary Ninja: https://binary.ninja/

### Academic Papers
- "Program Comprehension: A Survey" by von Mayrhauser & Vans
- "Design Pattern Detection Using Similarity Scoring" by Tsantalis et al.
- "Static Analysis: A Survey" by Bessey et al.

## Quick Decision Tree

```
Need to understand undocumented system?
│
├─ Have source code?
│  ├─ Yes → Start with Static Analysis (Pattern 1)
│  │         Then Dynamic Analysis (Pattern 2) if needed
│  │
│  └─ No → Use Dynamic Analysis only (Pattern 2)
│           Focus on behavior observation
│
├─ Need to see relationships?
│  └─ Use Dependency Graph Extraction (Pattern 3)
│
├─ Want to identify patterns?
│  └─ Use Design Pattern Recognition (Pattern 4)
│
└─ Need to create documentation?
   └─ Use Documentation Generation (Pattern 5)
```

## Next Steps

1. Read KNOWLEDGE.md for theoretical foundation
2. Study PATTERNS.md for implementation approaches
3. Try EXAMPLES.md for hands-on practice
4. Consult GOTCHAS.md when stuck
5. Reference REFERENCE.md for tool details

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-10-27
**Maintainer**: Issue #60 Implementation Team
