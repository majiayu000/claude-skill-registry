---
name: flow-trace
description: Trace data flow across files from source to sink. Use for cross-file taint analysis, understanding how user input reaches dangerous sinks, and documenting vulnerability paths.
---

# Flow Trace Skill

## Purpose

Trace data flow from source (user input) to sink (dangerous function) across multiple files. Outputs structured flow_edges for visualization and documentation.

## When to Use

- After finding a potential vulnerability, trace the full path
- Understanding how user input reaches a dangerous sink
- Documenting the attack path for a finding
- Verifying if a source can actually reach a sink

## Input Requirements

Provide either:
1. **Starting point**: Source file and function/variable
2. **Ending point**: Sink file and function
3. **Both**: For verifying connectivity

## Output Format

Output flow edges in this structure:

```yaml
flow_edges:
  - from_file: "src/routes/api.rs"
    from_line: 45
    from_symbol: "request.params['id']"
    to_file: "src/routes/api.rs"
    to_line: 48
    to_symbol: "get_user(id)"
    kind: taint
    notes: "User input passed to function"

  - from_file: "src/routes/api.rs"
    from_line: 48
    from_symbol: "get_user(id)"
    to_file: "src/db/users.rs"
    to_line: 23
    to_symbol: "User::find(id)"
    kind: dataflow
    notes: "Function call crosses file boundary"

  - from_file: "src/db/users.rs"
    from_line: 23
    from_symbol: "User::find(id)"
    to_file: "src/db/users.rs"
    to_line: 25
    to_symbol: "db.query(format!(...))"
    kind: taint
    notes: "SINK: Unsanitized input in SQL query"
```

## Flow Edge Types

| Kind | Description |
|------|-------------|
| `taint` | User-controlled data propagation |
| `dataflow` | General data flow (assignments, returns) |
| `authz` | Authorization/permission check flow |
| `controlflow` | Conditional branches affecting security |

## Tracing Process

### 1. Identify Source
```
Common sources:
- HTTP request parameters, body, headers
- File uploads (filename, content)
- Database values (stored attacks)
- Environment variables
- WebSocket messages
- Command line arguments
```

### 2. Follow Transformations
```
Track through:
- Variable assignments: let x = source
- Function parameters: foo(source)
- Return values: return process(source)
- Object properties: obj.field = source
- Array operations: arr.push(source)
```

### 3. Cross File Boundaries
```
Look for:
- Function calls to other modules
- Imports/requires
- Class inheritance
- Trait implementations
- Interface method calls
```

### 4. Identify Sinks
```
Dangerous sinks by type:
- SQL: db.query(), db.execute(), raw SQL
- Command: system(), exec(), spawn()
- XSS: innerHTML, document.write()
- File: open(), readFile(), writeFile()
- SSRF: http.get(url), fetch(url)
```

## Example Trace

### Starting Point
```
File: src/api/users.rs:15
Symbol: request.query("id")
```

### Trace Output
```yaml
flow_edges:
  - from_file: "src/api/users.rs"
    from_line: 15
    from_symbol: "request.query('id')"
    to_file: "src/api/users.rs"
    to_line: 16
    to_symbol: "id"
    kind: taint
    notes: "Query param extracted"

  - from_file: "src/api/users.rs"
    from_line: 16
    from_symbol: "id"
    to_file: "src/api/users.rs"
    to_line: 18
    to_symbol: "UserService::get(id)"
    kind: dataflow
    notes: "Passed to service layer"

  - from_file: "src/api/users.rs"
    from_line: 18
    from_symbol: "UserService::get(id)"
    to_file: "src/services/user.rs"
    to_line: 42
    to_symbol: "UserRepository::find(id)"
    kind: dataflow
    notes: "Service delegates to repository"

  - from_file: "src/services/user.rs"
    from_line: 42
    from_symbol: "UserRepository::find(id)"
    to_file: "src/db/repository.rs"
    to_line: 78
    to_symbol: "db.execute(query)"
    kind: taint
    notes: "SINK: SQL execution"

summary: "User input from query param flows through 4 hops to SQL sink"
sink_type: "SQL Injection"
sanitization_found: false
```

## Summary Format

After tracing, provide:
```
summary: "<source> -> ... (<N> hops) -> <sink>"
sink_type: "SQL Injection|Command Injection|XSS|Path Traversal|SSRF|..."
sanitization_found: true|false
sanitization_notes: "Input validated at step 2 with regex"
```

## Tips for Effective Tracing

1. **Start broad, narrow down**: First identify all call sites, then trace specific paths
2. **Watch for sanitization**: Note if/where input is validated or escaped
3. **Track transformations**: URL decode, base64, JSON parse can bypass filters
4. **Check error paths**: Error handlers often have different (weaker) validation
5. **Follow async flows**: Callbacks, promises, async/await can obscure data flow

## KYCo Integration

After tracing a vulnerability path, register the finding and flow edges:

### 1. Check Active Project
```bash
kyco project list
```

### 2. Create Finding with Taint Path
```bash
kyco finding create \
  --title "SQL Injection via user ID parameter" \
  --project PROJECT_ID \
  --severity high \
  --cwe CWE-89 \
  --attack-scenario "User input flows from request.params['id'] through 4 hops to db.query() without sanitization"
```

### 3. Import SARIF/Semgrep Results (if available)
```bash
# Import from security scanner output
kyco finding import semgrep-results.json --project PROJECT_ID

# Auto-detect format
kyco finding import scan-results.sarif --project PROJECT_ID
```

### 4. View Flow in Kanban
The KYCo GUI Kanban board visualizes flow traces. Open with:
```bash
kyco gui
```
Then click on a finding to see the SOURCE → intermediate → SINK flow graph.
