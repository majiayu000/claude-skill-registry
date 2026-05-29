---
name: navigator
description: Working with the Navigator Go submodule for web server fixes and enhancements. Use when deployment plans require Navigator changes, config parsing issues arise, or new routing/proxy behavior is needed.
---

# Navigator Submodule Development

## Why Navigator is a Submodule

Navigator is included as a Git submodule because showcase routinely needs Navigator fixes to implement deployment plans. Changes are tested in showcase context before being pushed upstream.

**Location**: `navigator/` (Git submodule)
**Language**: Go
**Purpose**: Multi-tenant web server with framework independence

## Project Structure

```
navigator/
├── cmd/navigator/            # Production Navigator implementation
├── internal/                  # Modular packages
│   ├── config/               # Configuration loading and parsing
│   ├── server/               # HTTP handling, routing, static files
│   ├── auth/                 # Authentication (htpasswd)
│   ├── process/              # Web app lifecycle management
│   └── proxy/                # Reverse proxy and Fly-Replay
└── docs/                     # MkDocs documentation
```

## Critical Architecture: Configuration Flow

Understanding this flow is essential for fixing config-related bugs:

1. **YAML file** (user-facing config)
2. **YAMLConfig struct** in `types.go` (mirrors YAML structure with yaml tags)
3. **ConfigParser** in `parser.go` (converts YAML to internal format)
4. **Config struct** in `types.go` (optimized internal representation)

**Common Bug Pattern**: When adding config fields, developers often:
- ✅ Add field to `Config` struct (internal)
- ❌ FORGET to add field to `YAMLConfig` struct
- ❌ FORGET to add parsing logic in `parser.go`
- Result: YAML config is valid but silently ignored!

## Request Flow in Handler (Order Matters!)

```go
// From internal/server/handler.go ServeHTTP()
1. Health checks      // BEFORE everything (bypasses auth)
2. Authentication     // EARLY check (before routing)
3. Rewrites/redirects
4. CGI scripts
5. Reverse proxies
6. Static files
7. Maintenance mode
8. Web app proxy      // Tenant routing
```

**Security Critical**: Health checks MUST come before auth. Auth MUST come before tenant routing.

## Common Development Tasks

### Adding a New Config Option

**Example: Health Check Config (Recent Fix)**

**Step 1**: Add to YAMLConfig in `internal/config/types.go`:
```go
type YAMLConfig struct {
    Server struct {
        // ... other fields
        HealthCheck HealthCheckConfig `yaml:"health_check"` // ← Must have yaml tag
    } `yaml:"server"`
}
```

**Step 2**: Add to internal Config (if different structure needed):
```go
type Config struct {
    Server struct {
        // ... other fields
        HealthCheck HealthCheckConfig
    }
}
```

**Step 3**: Add parsing logic in `internal/config/parser.go`:
```go
func (p *ConfigParser) parseServerConfig() {
    // ... other parsing
    p.config.Server.HealthCheck = p.yamlConfig.Server.HealthCheck // ← CRITICAL
}
```

**Step 4**: Add tests in `internal/config/parser_test.go`:
```go
func TestConfigParser_ParseHealthCheck(t *testing.T) {
    yamlConfig := YAMLConfig{}
    yamlConfig.Server.HealthCheck = HealthCheckConfig{
        Path: "/up",
        Response: &HealthCheckResponse{Status: 200, Body: "OK"},
    }

    parser := NewConfigParser(&yamlConfig)
    config, err := parser.Parse()

    if config.Server.HealthCheck.Path != "/up" {
        t.Errorf("HealthCheck not parsed correctly")
    }
}
```

**Step 5**: Add integration tests in `internal/server/handler_test.go` (or appropriate file).

### Adding Handler Behavior

**Example: Health Check Handler (Recent Fix)**

```go
// Add early in ServeHTTP - order matters!
func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    // Health checks BEFORE authentication
    if h.config.Server.HealthCheck.Path != "" && r.URL.Path == h.config.Server.HealthCheck.Path {
        h.handleHealthCheck(recorder, r)
        return  // Stop processing
    }

    // Authentication check comes next
    // ... rest of handler
}
```

**Integration Test (Security Critical)**:
```go
func TestHandler_ServeHTTP_HealthCheckBeforeAuth(t *testing.T) {
    cfg := &config.Config{}
    cfg.Server.HealthCheck = config.HealthCheckConfig{
        Path: "/up",
        Response: &config.HealthCheckResponse{Status: 200, Body: "OK"},
    }
    cfg.Auth.Enabled = true  // Enable auth

    basicAuth := &auth.BasicAuth{}
    handler := CreateTestHandler(cfg, nil, basicAuth, nil)

    req := httptest.NewRequest("GET", "/up", nil)
    // NO auth credentials provided
    recorder := httptest.NewRecorder()
    handler.ServeHTTP(recorder, req)

    // MUST succeed without auth - critical security requirement
    if recorder.Code != 200 {
        t.Errorf("Health check should bypass auth")
    }
}
```

## Testing Requirements

### Test Checklist
- [ ] **Config parser tests** (`internal/config/parser_test.go`)
  - YAML unmarshaling works
  - Parsing logic copies fields correctly
  - Default values applied
  - Edge cases (empty, nil)

- [ ] **Integration tests** (appropriate `*_test.go`)
  - Full request/response through `ServeHTTP`
  - Security implications (especially auth bypass scenarios)
  - Edge cases and error conditions

### Running Tests

```bash
# All tests
go test ./...

# Specific package
go test -v ./internal/config/
go test -v ./internal/server/

# With coverage
go test -cover ./...

# Pre-commit validation (CI requirements)
gofmt -s -l . && \
golangci-lint run && \
go vet ./... && \
go test -race -cover -timeout=3m ./... && \
go build ./cmd/navigator-refactored && \
echo "✓ All CI checks passed!"
```

## Recent Fixes (Nov 2024)

### Fix 1: CGI reload_config Not Parsed
**Problem**: `reload_config` field in CGI scripts ignored
**Cause**: Field missing from `YAMLConfig.Server.CGIScripts`
**Fix**: Added field to `CGIScriptConfig` struct
**Lesson**: Always check YAMLConfig has all fields with yaml tags

### Fix 2: Health Checks Not Working
**Problem**: `/up` returned 401 (auth) or started index tenant unnecessarily
**Cause**:
- `YAMLConfig.Server` missing `HealthCheck` field
- `parseServerConfig()` not copying health check config

**Fix**:
```go
// types.go - Added to YAMLConfig.Server
HealthCheck HealthCheckConfig `yaml:"health_check"`

// parser.go - Added to parseServerConfig()
p.config.Server.HealthCheck = p.yamlConfig.Server.HealthCheck
```

**Test Coverage**: 270 lines added
- Parser tests: YAML → Config transformation
- Handler tests: before auth, different paths, custom headers
- Security test: health checks bypass authentication

## Common Bug Patterns

### Pattern 1: Config Parser Forgot to Copy Field
```go
// ❌ BUG: Field exists in YAMLConfig but not copied
type YAMLConfig struct {
    Server struct {
        HealthCheck HealthCheckConfig `yaml:"health_check"`
    }
}

func (p *ConfigParser) parseServerConfig() {
    // ... other fields copied
    // ❌ FORGOT: p.config.Server.HealthCheck = p.yamlConfig.Server.HealthCheck
}

// ✅ FIX: Add the copy statement
p.config.Server.HealthCheck = p.yamlConfig.Server.HealthCheck
```

**How to catch**: Write parser tests that verify field is copied.

### Pattern 2: Missing yaml Tag
```go
// ❌ BUG: No yaml tag, field won't unmarshal
type ServerConfig struct {
    Listen string  // Won't unmarshal from YAML
}

// ✅ FIX: Add yaml tag
type ServerConfig struct {
    Listen string `yaml:"listen"`
}
```

### Pattern 3: Wrong Handler Order
```go
// ❌ BUG: Auth check after tenant routing (can be bypassed!)
func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    h.handleWebAppProxy(w, r)  // Routes first
    if !h.auth.CheckAuth(r) {  // Auth never runs!
        return
    }
}

// ✅ FIX: Correct order
func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    // 1. Health checks (before everything)
    if h.config.Server.HealthCheck.Path != "" { /* ... */ }

    // 2. Authentication (EARLY)
    isPublic := auth.ShouldExcludeFromAuth(r.URL.Path, h.config)
    needsAuth := h.auth.IsEnabled() && !isPublic
    if needsAuth && !h.auth.CheckAuth(r) {
        h.auth.RequireAuth(recorder)
        return
    }

    // 3. Then routing
    h.handleWebAppProxy(w, r)
}
```

**How to catch**: Write integration tests that verify security (auth bypass scenarios).

## Deployment Workflow

1. **Rebase submodule on main before making changes**:
```bash
cd navigator

# Fetch latest from remote
git fetch origin

# Rebase on main (creates a clean linear history)
git rebase origin/main

# If conflicts, resolve them and continue
# git rebase --continue
```

2. **Work in Navigator submodule**:
```bash
# Make changes, run tests
go test ./...
golangci-lint run
git add -A
git commit -m "Fix: health check parsing"
```

3. **Test in showcase context**:
```bash
cd ..  # Back to showcase root
# Test Navigator fix with showcase deployment
```

4. **Push to both repos**:
```bash
# Push Navigator changes
cd navigator
git push origin HEAD:refs/heads/main

# Update submodule reference in showcase
cd ..
git add navigator
git commit -m "Update navigator: fix health check parsing"
git push
```

**Note**: If submodule is in detached HEAD state (common after `git submodule update`), the rebase step ensures you're building on the latest main branch before making changes.

## Quick Reference Commands

```bash
# Build Navigator
cd navigator
go build -o bin/navigator cmd/navigator

# Or use make
make build

# Run with config
./bin/navigator config/navigator.yml

# Reload config (SIGHUP)
kill -HUP $(cat /tmp/navigator.pid)

# Debug config loading
LOG_LEVEL=debug ./bin/navigator config/navigator.yml
```

## When to Fix Navigator

You need Navigator changes when:
- ✅ Deployment plan requires new config options
- ✅ New routing/proxy behavior needed
- ✅ Authentication/security enhancements required
- ✅ Config not being parsed correctly (check YAMLConfig + parser)
- ✅ Request flow order needs adjustment

**Pattern**: Fix Navigator first, test in showcase, then continue deployment plan.

## Essential Files

- **`navigator/CLAUDE.md`** - Comprehensive development guide (read first!)
- **`internal/config/types.go`** - All config structures (YAMLConfig + Config)
- **`internal/config/parser.go`** - YAML → Config conversion
- **`internal/server/handler.go`** - Main HTTP request routing

## Getting Help

1. Read `navigator/CLAUDE.md` for comprehensive guide
2. Check `navigator/docs/` for user documentation
3. Search tests for similar patterns
4. Review Git history for "Fix:" commits
5. Run with `LOG_LEVEL=debug` to see what's happening
