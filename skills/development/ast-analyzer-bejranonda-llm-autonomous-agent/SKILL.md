---
name: ast-analyzer
description: Deep Abstract Syntax Tree analysis for understanding code structure, dependencies, impact analysis, and pattern detection at the structural level across multiple programming languages
version: 1.0.0
---

## AST Analyzer Skill

Provides comprehensive Abstract Syntax Tree (AST) analysis capabilities for understanding code at a structural level, identifying patterns, dependencies, and potential issues that simple text analysis would miss.

## Core Philosophy

**Beyond Text Analysis**: While traditional code analysis works with text patterns, AST analysis understands the actual structure and semantics of code, enabling:
- Precise refactoring without breaking logic
- Accurate dependency tracking
- Reliable impact analysis
- Language-aware pattern detection

## Core Capabilities

### 1. AST Parsing

**Multi-Language Support**:
```python
# Python example using ast module
import ast

def parse_python_code(source_code):
    tree = ast.parse(source_code)

    # Extract all function definitions
    functions = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]

    # Extract all class definitions
    classes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    ]

    return {
        "functions": len(functions),
        "classes": len(classes),
        "function_details": [
            {
                "name": f.name,
                "args": [arg.arg for arg in f.args.args],
                "line": f.lineno,
                "decorators": [d.id for d in f.decorator_list if isinstance(d, ast.Name)]
            }
            for f in functions
        ]
    }
```

**JavaScript/TypeScript Support**:
```javascript
// Using babel or acorn parser
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;

function parseJavaScriptCode(sourceCode) {
    const ast = parser.parse(sourceCode, {
        sourceType: 'module',
        plugins: ['jsx', 'typescript']
    });

    const analysis = {
        functions: [],
        classes: [],
        imports: [],
        exports: []
    };

    traverse(ast, {
        FunctionDeclaration(path) {
            analysis.functions.push({
                name: path.node.id.name,
                params: path.node.params.map(p => p.name),
                async: path.node.async
            });
        },
        ClassDeclaration(path) {
            analysis.classes.push({
                name: path.node.id.name,
                methods: path.node.body.body.filter(
                    m => m.type === 'ClassMethod'
                )
            });
        }
    });

    return analysis;
}
```

### 2. Function and Class Hierarchy Analysis

**Hierarchy Extraction**:
```python
def analyze_class_hierarchy(ast_tree):
    """Extract complete class inheritance hierarchy."""
    hierarchy = {}

    for node in ast.walk(ast_tree):
        if isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "bases": [
                    base.id if isinstance(base, ast.Name) else str(base)
                    for base in node.bases
                ],
                "methods": [
                    m.name for m in node.body
                    if isinstance(m, ast.FunctionDef)
                ],
                "decorators": [
                    d.id for d in node.decorator_list
                    if isinstance(d, ast.Name)
                ],
                "line": node.lineno
            }
            hierarchy[node.name] = class_info

    # Build inheritance tree
    for class_name, info in hierarchy.items():
        info["children"] = [
            name for name, data in hierarchy.items()
            if class_name in data["bases"]
        ]

    return hierarchy
```

**Method Call Graph**:
```python
def build_call_graph(ast_tree):
    """Build function call graph showing dependencies."""
    call_graph = {}

    for node in ast.walk(ast_tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            calls = []

            # Find all function calls within this function
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        calls.append(child.func.id)
                    elif isinstance(child.func, ast.Attribute):
                        calls.append(f"{child.func.value.id}.{child.func.attr}")

            call_graph[function_name] = {
                "calls": list(set(calls)),
                "complexity": calculate_complexity(node)
            }

    return call_graph
```

### 3. Variable Scope and Lifetime Tracking

**Scope Analysis**:
```python
def analyze_variable_scope(ast_tree):
    """Track variable definitions, assignments, and usage scope."""
    scopes = []

    class ScopeAnalyzer(ast.NodeVisitor):
        def __init__(self):
            self.current_scope = None
            self.scopes = {}

        def visit_FunctionDef(self, node):
            # Enter new scope
            scope_name = f"{self.current_scope}.{node.name}" if self.current_scope else node.name
            self.scopes[scope_name] = {
                "type": "function",
                "variables": {},
                "params": [arg.arg for arg in node.args.args],
                "line": node.lineno
            }

            old_scope = self.current_scope
            self.current_scope = scope_name

            # Analyze variable assignments in this scope
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name):
                            self.scopes[scope_name]["variables"][target.id] = {
                                "first_assignment": child.lineno,
                                "type": "local"
                            }

            self.current_scope = old_scope

        def visit_ClassDef(self, node):
            # Similar scope tracking for classes
            scope_name = f"{self.current_scope}.{node.name}" if self.current_scope else node.name
            self.scopes[scope_name] = {
                "type": "class",
                "variables": {},
                "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                "line": node.lineno
            }

    analyzer = ScopeAnalyzer()
    analyzer.visit(ast_tree)
    return analyzer.scopes
```

### 4. Code Pattern and Anti-Pattern Detection

**Common Patterns**:
```python
def detect_patterns(ast_tree):
    """Detect common code patterns and anti-patterns."""
    patterns_found = {
        "design_patterns": [],
        "anti_patterns": [],
        "code_smells": []
    }

    # Singleton pattern detection
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.ClassDef):
            # Check for singleton indicators
            has_instance_attr = any(
                isinstance(n, ast.Assign) and
                any(isinstance(t, ast.Name) and t.id == '_instance' for t in n.targets)
                for n in node.body
            )

            has_new_method = any(
                isinstance(n, ast.FunctionDef) and n.name == '__new__'
                for n in node.body
            )

            if has_instance_attr and has_new_method:
                patterns_found["design_patterns"].append({
                    "pattern": "Singleton",
                    "class": node.name,
                    "line": node.lineno
                })

    # Anti-pattern: God class (too many methods)
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.ClassDef):
            method_count = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))

            if method_count > 20:
                patterns_found["anti_patterns"].append({
                    "pattern": "God Class",
                    "class": node.name,
                    "method_count": method_count,
                    "line": node.lineno,
                    "severity": "high"
                })

    # Code smell: Long function
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.FunctionDef):
            # Count lines in function
            if hasattr(node, 'end_lineno'):
                line_count = node.end_lineno - node.lineno

                if line_count > 50:
                    patterns_found["code_smells"].append({
                        "smell": "Long Function",
                        "function": node.name,
                        "lines": line_count,
                        "line": node.lineno,
                        "recommendation": "Consider breaking into smaller functions"
                    })

    # Code smell: Nested loops
    for node in ast.walk(ast_tree):
        if isinstance(node, (ast.For, ast.While)):
            nested_loops = [
                child for child in ast.walk(node)
                if isinstance(child, (ast.For, ast.While)) and child != node
            ]

            if len(nested_loops) >= 2:
                patterns_found["code_smells"].append({
                    "smell": "Deep Nesting",
                    "nesting_level": len(nested_loops) + 1,
                    "line": node.lineno,
                    "recommendation": "Consider extracting inner loops or using different algorithm"
                })

    return patterns_found
```

### 5. Dependency Mapping

**Import Analysis**:
```python
def analyze_dependencies(ast_tree, file_path):
    """Build complete dependency map."""
    dependencies = {
        "imports": [],
        "from_imports": [],
        "internal_deps": [],
        "external_deps": [],
        "unused_imports": []
    }

    # Track all imports
    imported_names = set()

    for node in ast.walk(ast_tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_name = alias.asname if alias.asname else alias.name
                imported_names.add(import_name)
                dependencies["imports"].append({
                    "module": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno
                })

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                import_name = alias.asname if alias.asname else alias.name
                imported_names.add(import_name)
                dependencies["from_imports"].append({
                    "module": module,
                    "name": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno
                })

    # Classify as internal or external
    for imp in dependencies["imports"] + dependencies["from_imports"]:
        module = imp.get("module", "")
        if module.startswith(".") or "/" in file_path and module.startswith(file_path.split("/")[0]):
            dependencies["internal_deps"].append(imp)
        else:
            dependencies["external_deps"].append(imp)

    # Find unused imports
    used_names = set()
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                used_names.add(node.value.id)

    dependencies["unused_imports"] = [
        name for name in imported_names
        if name not in used_names
    ]

    return dependencies
```

**Circular Dependency Detection**:
```python
def detect_circular_dependencies(project_files):
    """Detect circular import chains across project."""
    dependency_graph = {}

    # Build dependency graph
    for file_path, ast_tree in project_files.items():
        deps = analyze_dependencies(ast_tree, file_path)
        dependency_graph[file_path] = [
            imp["module"] for imp in deps["internal_deps"]
        ]

    # Find cycles using DFS
    def find_cycles(node, visited, rec_stack, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        cycles = []

        for neighbor in dependency_graph.get(node, []):
            if neighbor not in visited:
                cycles.extend(find_cycles(neighbor, visited, rec_stack, path[:]))
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])

        rec_stack.remove(node)
        return cycles

    all_cycles = []
    visited = set()

    for file_path in dependency_graph:
        if file_path not in visited:
            cycles = find_cycles(file_path, visited, set(), [])
            all_cycles.extend(cycles)

    return {
        "circular_dependencies": all_cycles,
        "count": len(all_cycles),
        "severity": "high" if len(all_cycles) > 0 else "none"
    }
```

### 6. Impact Analysis

**Change Impact Calculator**:
```python
def calculate_change_impact(ast_tree, changed_entity, change_type):
    """
    Calculate downstream impact of a code change.

    Args:
        ast_tree: AST of the codebase
        changed_entity: Function/class name that changed
        change_type: 'signature_change', 'deletion', 'rename'
    """
    call_graph = build_call_graph(ast_tree)

    impact = {
        "direct_callers": [],
        "indirect_callers": [],
        "affected_tests": [],
        "risk_score": 0,
        "breaking_change": False
    }

    # Find direct callers
    for func_name, data in call_graph.items():
        if changed_entity in data["calls"]:
            impact["direct_callers"].append({
                "function": func_name,
                "complexity": data["complexity"]
            })

    # Find indirect callers (BFS through call graph)
    visited = set()
    queue = impact["direct_callers"][:]

    while queue:
        caller = queue.pop(0)
        func_name = caller["function"]

        if func_name in visited:
            continue

        visited.add(func_name)

        # Find callers of this function
        for next_func, data in call_graph.items():
            if func_name in data["calls"] and next_func not in visited:
                impact["indirect_callers"].append({
                    "function": next_func,
                    "complexity": data["complexity"]
                })
                queue.append({"function": next_func, "complexity": data["complexity"]})

    # Identify affected test files
    impact["affected_tests"] = [
        func for func in impact["direct_callers"] + impact["indirect_callers"]
        if func["function"].startswith("test_") or "_test" in func["function"]
    ]

    # Calculate risk score
    direct_count = len(impact["direct_callers"])
    indirect_count = len(impact["indirect_callers"])
    avg_complexity = sum(c["complexity"] for c in impact["direct_callers"]) / max(direct_count, 1)

    impact["risk_score"] = min(100, (
        direct_count * 10 +
        indirect_count * 2 +
        avg_complexity * 5
    ))

    # Determine if breaking change
    impact["breaking_change"] = (
        change_type in ["signature_change", "deletion"] and
        direct_count > 0
    )

    return impact
```

### 7. Coupling and Cohesion Analysis

**Coupling Metrics**:
```python
def analyze_coupling(ast_tree):
    """Measure coupling between modules/classes."""
    coupling_metrics = {
        "afferent_coupling": {},  # How many depend on this
        "efferent_coupling": {},  # How many this depends on
        "instability": {}          # Ratio of efferent to total
    }

    call_graph = build_call_graph(ast_tree)

    # Calculate afferent coupling (Ca)
    for func_name in call_graph:
        afferent_count = sum(
            1 for other_func, data in call_graph.items()
            if func_name in data["calls"]
        )
        coupling_metrics["afferent_coupling"][func_name] = afferent_count

    # Calculate efferent coupling (Ce)
    for func_name, data in call_graph.items():
        efferent_count = len(data["calls"])
        coupling_metrics["efferent_coupling"][func_name] = efferent_count

    # Calculate instability (Ce / (Ce + Ca))
    for func_name in call_graph:
        ce = coupling_metrics["efferent_coupling"].get(func_name, 0)
        ca = coupling_metrics["afferent_coupling"].get(func_name, 0)

        total = ce + ca
        coupling_metrics["instability"][func_name] = ce / max(total, 1)

    # Identify highly coupled functions
    highly_coupled = [
        {
            "function": func_name,
            "afferent": coupling_metrics["afferent_coupling"][func_name],
            "efferent": coupling_metrics["efferent_coupling"][func_name],
            "instability": coupling_metrics["instability"][func_name]
        }
        for func_name in call_graph
        if (coupling_metrics["afferent_coupling"][func_name] +
            coupling_metrics["efferent_coupling"][func_name]) > 10
    ]

    return {
        "metrics": coupling_metrics,
        "highly_coupled": highly_coupled,
        "average_instability": sum(coupling_metrics["instability"].values()) / len(coupling_metrics["instability"])
    }
```

## When to Apply This Skill

### Primary Use Cases

1. **Refactoring Analysis**
   - Understand code structure before refactoring
   - Calculate impact of proposed changes
   - Identify safe refactoring opportunities
   - Detect coupled code that needs attention

2. **Code Review**
   - Detect anti-patterns and code smells
   - Verify design pattern implementations
   - Check for circular dependencies
   - Assess code complexity

3. **Security Vulnerability Scanning**
   - Find code patterns associated with vulnerabilities
   - Track data flow for taint analysis
   - Identify unsafe function calls
   - Detect missing input validation

4. **Architecture Validation**
   - Verify intended architecture is implemented
   - Detect architectural violations
   - Measure coupling between components
   - Identify god classes and god functions

5. **Dependency Analysis**
   - Build comprehensive dependency graphs
   - Detect circular dependencies
   - Find unused imports
   - Classify internal vs external dependencies

6. **Test Suite Impact Analysis**
   - Identify which tests cover changed code
   - Calculate test coverage gaps
   - Prioritize test execution based on changes
   - Generate test suggestions for uncovered code

## Integration with Enhanced Learning

This skill integrates with the enhanced learning system to:

1. **Learn Refactoring Patterns**
   - Track which refactorings are successful
   - Identify patterns that lead to quality improvements
   - Build library of safe refactoring strategies

2. **Improve Impact Predictions**
   - Learn actual vs predicted impact
   - Refine risk scoring algorithms
   - Improve accuracy of breaking change detection

3. **Pattern Recognition Evolution**
   - Discover new patterns specific to project
   - Learn team-specific anti-patterns
   - Adapt pattern detection to codebase style

4. **Dependency Best Practices**
   - Learn optimal dependency structures
   - Identify problematic dependency patterns
   - Suggest improvements based on successful refactorings

## Output Format

### Comprehensive Analysis Report

```json
{
  "file": "path/to/file.py",
  "analysis_timestamp": "2025-10-23T15:30:00Z",
  "summary": {
    "functions": 25,
    "classes": 5,
    "total_lines": 850,
    "complexity_score": 68,
    "maintainability_index": 72
  },
  "hierarchy": {
    "classes": [...],
    "functions": [...],
    "call_graph": {...}
  },
  "dependencies": {
    "imports": [...],
    "internal_deps": [...],
    "external_deps": [...],
    "unused_imports": [...],
    "circular_dependencies": []
  },
  "patterns": {
    "design_patterns": [...],
    "anti_patterns": [...],
    "code_smells": [...]
  },
  "coupling": {
    "metrics": {...},
    "highly_coupled": [...],
    "recommendations": [...]
  },
  "impact_analysis": {
    "high_risk_changes": [...],
    "affected_components": [...]
  },
  "recommendations": [
    "Break down God class 'DataProcessor' (45 methods)",
    "Extract nested loops in 'process_data' function",
    "Remove unused import 'unused_module'",
    "Resolve circular dependency between module_a and module_b"
  ]
}
```

## Tools and Libraries

### Python
- **ast module**: Built-in Python AST parser
- **astroid**: Advanced AST manipulation
- **rope**: Refactoring library with AST support
- **radon**: Code metrics (complexity, maintainability)

### JavaScript/TypeScript
- **@babel/parser**: JavaScript parser
- **@babel/traverse**: AST traversal
- **typescript**: TypeScript compiler API
- **esprima**: ECMAScript parser

### Multi-Language
- **tree-sitter**: Universal parser for multiple languages
- **srcML**: Source code to XML for analysis
- **understand**: Commercial but powerful code analysis

## Best Practices

1. **Cache AST Parsing**: Parsing is expensive, cache results
2. **Incremental Analysis**: Only re-analyze changed files
3. **Language-Specific Handling**: Different languages need different approaches
4. **Combine with Static Analysis**: AST + linters = comprehensive view
5. **Visualize Complex Graphs**: Use graphviz for dependency visualization

## Performance Considerations

- **Large Files**: Consider streaming or chunked analysis
- **Deep Nesting**: Set recursion limits to prevent stack overflow
- **Memory Usage**: AST can be memory-intensive for large codebases
- **Parallel Processing**: Analyze files in parallel when possible

## Limitations

- **Dynamic Code**: Can't analyze dynamically generated code
- **External Dependencies**: Limited insight into third-party libraries
- **Runtime Behavior**: Static analysis only, no runtime information
- **Complex Metaprogramming**: Difficult to analyze decorators, metaclasses

This skill provides the foundation for deep code understanding that enables safe refactoring, accurate impact analysis, and intelligent code review recommendations.