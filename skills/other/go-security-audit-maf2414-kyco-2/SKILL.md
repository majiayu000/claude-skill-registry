---
name: go-security-audit
description: Security audit for Go backend code and SDKs. Covers Go-specific vulnerabilities, common security pitfalls, and best practices. Use when auditing Go codebases.
---

# Go Security Audit

## Purpose

Comprehensive security audit for Go codebases covering Go-specific vulnerabilities, common pitfalls, and security best practices.

## Focus Areas

- **SQL Injection**: String formatting in database queries
- **Command Injection**: os/exec with user input
- **Path Traversal**: File operations with user paths
- **Race Conditions**: Concurrent access without synchronization
- **Error Handling**: Ignored errors, panic recovery
- **Crypto Issues**: Weak random, improper key handling

## Go-Specific Vulnerabilities

### SQL Injection
```go
// VULNERABLE - string formatting
query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", userInput)
db.Query(query)

// SECURE - parameterized query
db.Query("SELECT * FROM users WHERE id = ?", userInput)
// Or with sqlx:
db.Get(&user, "SELECT * FROM users WHERE id = $1", userInput)
```

### Command Injection
```go
// VULNERABLE - shell expansion
cmd := exec.Command("sh", "-c", "ls " + userInput)

// SECURE - no shell, array arguments
cmd := exec.Command("ls", userInput)  // userInput as single arg
```

### Path Traversal
```go
// VULNERABLE - user controls path
path := filepath.Join("/uploads", userInput)
// userInput = "../../../etc/passwd"

// SECURE - validate path stays in directory
path := filepath.Join("/uploads", filepath.Base(userInput))
// Or check after resolution:
absPath, _ := filepath.Abs(path)
if !strings.HasPrefix(absPath, "/uploads/") {
    return ErrInvalidPath
}
```

### Race Conditions
```go
// VULNERABLE - race on shared state
var balance int64
func withdraw(amount int64) bool {
    if balance >= amount {  // TOCTOU race
        balance -= amount
        return true
    }
    return false
}

// SECURE - use mutex or atomic
var mu sync.Mutex
func withdraw(amount int64) bool {
    mu.Lock()
    defer mu.Unlock()
    if balance >= amount {
        balance -= amount
        return true
    }
    return false
}
```

### Error Handling
```go
// VULNERABLE - ignored error
data, _ := ioutil.ReadFile(path)  // Error ignored!

// VULNERABLE - panic in HTTP handler (DoS)
func handler(w http.ResponseWriter, r *http.Request) {
    panic("oops")  // Kills entire server
}

// SECURE - handle errors
data, err := ioutil.ReadFile(path)
if err != nil {
    return fmt.Errorf("read config: %w", err)
}
```

### Weak Random
```go
// VULNERABLE - math/rand is predictable
import "math/rand"
token := rand.Int63()

// SECURE - crypto/rand for security
import "crypto/rand"
var token [32]byte
rand.Read(token[:])
```

## Output Format

```yaml
findings:
  - title: "SQL Injection via fmt.Sprintf"
    severity: critical
    attack_scenario: "Attacker injects SQL through userInput parameter"
    preconditions: "None"
    reachability: public
    impact: "Database compromise"
    confidence: high
    cwe_id: "CWE-89"
    affected_assets:
      - "pkg/db/users.go:45"
    taint_path: "r.URL.Query().Get('id') -> fmt.Sprintf() -> db.Query()"
```

## Dangerous Functions to Audit

### Database
```
db.Query(fmt.Sprintf(...))
db.Exec(string + variable)
db.Raw(userInput)
```

### OS/Exec
```
exec.Command("sh", "-c", ...)
exec.Command(userInput, ...)
os.StartProcess with user args
```

### File Operations
```
os.Open(userPath)
ioutil.ReadFile(userPath)
http.ServeFile without path validation
```

### Crypto
```
math/rand for tokens
md5.Sum for passwords
des.NewCipher (weak)
cipher.NewCBCDecrypter without MAC
```

### HTTP
```
http.Get(userURL) // SSRF
http.ListenAndServe with no TLS
ResponseWriter.Write without Content-Type
```

## Severity Guidelines

| Issue | Severity |
|-------|----------|
| SQL Injection | Critical |
| Command Injection | Critical |
| Path Traversal (read) | High |
| Path Traversal (write) | Critical |
| Race condition (security) | High |
| Weak crypto (passwords) | High |
| SSRF | High |
| Ignored security error | Medium |
| math/rand for tokens | High |
| Panic in HTTP handler | Medium |

## Go Security Tools

```bash
# Static analysis
gosec ./...
staticcheck ./...
go vet ./...

# Race detection
go test -race ./...

# Dependency vulnerabilities
govulncheck ./...
```

## KYCo Integration

Register findings and import scanner results using kyco CLI:

### 1. Check/Select Active Project
```bash
kyco project list
kyco project select PROJECT_ID
```

### 2. Import gosec/semgrep Results
```bash
# Generate SARIF from gosec
gosec -fmt sarif -out gosec-results.sarif ./...

# Import into KYCo
kyco finding import gosec-results.sarif --project PROJECT_ID

# Or import semgrep results
semgrep --config auto --sarif -o semgrep.sarif .
kyco finding import semgrep.sarif --project PROJECT_ID
```

### 3. Register Manual Findings
```bash
kyco finding create \
  --title "SQL Injection via fmt.Sprintf" \
  --project PROJECT_ID \
  --severity critical \
  --cwe CWE-89 \
  --attack-scenario "Attacker injects SQL through userInput parameter" \
  --assets "pkg/db/users.go:45"
```

### 4. View Findings
```bash
kyco finding list --project PROJECT_ID
kyco gui  # Opens Kanban board
```
