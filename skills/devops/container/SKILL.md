---
name: container
description: Container engine abstraction, Docker/Podman patterns, path handling, Linux-only policy
disable-model-invocation: false
---

# Container Engine Skill

This skill covers the container runtime implementation in Invowk, including the engine abstraction layer, Docker/Podman support, and sandbox-aware execution.

Use this skill when working on:
- `internal/container/` - Container engine abstraction
- `internal/runtime/container.go` - Container runtime implementation
- `internal/provision/` - Container provisioning logic
- Container-related tests

---

## Linux-Only Container Support

**CRITICAL: The container runtime ONLY supports Linux containers.**

| Supported | NOT Supported |
|-----------|---------------|
| Debian-based images (`debian:stable-slim`) | Alpine-based images (`alpine:*`) |
| Standard Linux containers | Windows container images |

**Why no Alpine:** musl-based environments have many subtle gotchas; we prioritize reliability over image size.

**Why no Windows containers:** They're rarely used and would introduce too much extra complexity to Invowk's auto-provisioning logic.

**In tests, docs, and examples:** Always use `debian:stable-slim` as the reference image.

---

## Engine Interface

The `Engine` interface (`engine.go`) defines the unified contract for all container operations:

```go
type Engine interface {
    // Core operations
    Build(ctx context.Context, opts BuildOptions) (*BuildResult, error)
    Run(ctx context.Context, opts RunOptions) (*RunResult, error)
    Remove(ctx context.Context, containerID string) error
    ImageExists(ctx context.Context, image string) (bool, error)
    RemoveImage(ctx context.Context, image string) error

    // Metadata
    Name() string
    Version(ctx context.Context) (string, error)
    Available() bool

    // Interactive mode support
    BuildRunArgs(opts RunOptions) []string
    BinaryPath() string
}
```

**Key Pattern:** The interface doesn't expose vendor-specific methods. Methods like `Exec()` and `InspectImage()` exist only on concrete types.

---

## BaseCLIEngine Embedding Pattern

Both Docker and Podman engines embed `BaseCLIEngine` (`engine_base.go`) for shared CLI command construction:

```go
type BaseCLIEngine struct {
    binaryPath         string
    execCommand        ExecCommandFunc       // For mocking in tests
    volumeFormatter    VolumeFormatFunc      // SELinux label injection
    runArgsTransformer RunArgsTransformer    // Podman --userns=keep-id
}
```

### Responsibilities

| Method | Purpose |
|--------|---------|
| `BuildArgs()`, `RunArgs()` | Construct CLI arguments |
| `RunCommand()`, `RunCommandCombined()` | Execute commands |
| `FormatVolumeMount()`, `ParseVolumeMount()` | Volume mount handling |
| `ResolveDockerfilePath()` | Path resolution with traversal protection |

### Functional Options

```go
// For testing - inject mock command executor
eng := NewDockerEngine(WithExecCommand(mockExec))

// For Podman - SELinux label injection
eng := NewPodmanEngine(WithVolumeFormatter(selinuxFormatter))

// For Podman - rootless mode
eng := NewPodmanEngine(WithRunArgsTransformer(usernsKeepID))
```

---

## Docker vs Podman Implementation

### Docker (`docker.go`)

Minimal implementation—mostly delegates to `BaseCLIEngine`:

```go
type DockerEngine struct {
    *BaseCLIEngine
}

func NewDockerEngine(opts ...Option) (*DockerEngine, error) {
    path, err := exec.LookPath("docker")
    if err != nil {
        return nil, err
    }
    return &DockerEngine{BaseCLIEngine: newBase(path, opts...)}, nil
}
```

### Podman (`podman.go`)

More complex due to Linux-specific features:

**Binary Discovery:**
```go
// Tries podman first, then podman-remote (for immutable distros like Silverblue)
path, err := exec.LookPath("podman")
if err != nil {
    path, err = exec.LookPath("podman-remote")
}
```

**Automatic Enhancements:**

1. **SELinux Volume Labels**: Automatically adds `:z` labels to volumes on SELinux systems
   ```go
   // Checks /sys/fs/selinux existence (more reliable than checking enforce status)
   func isSELinuxPresent() bool {
       _, err := os.Stat("/sys/fs/selinux")
       return err == nil
   }
   ```

2. **Rootless Compatibility**: Injects `--userns=keep-id` to preserve host UID/GID
   ```go
   // Only transforms 'run' commands, inserted before image name
   func makeUsernsKeepIDAdder() RunArgsTransformer { ... }
   ```

---

## Path Handling (Host vs Container)

**CRITICAL:** Container paths always use forward slashes (`/`), regardless of host platform.

### Two Path Domains

| Domain | Separator | Example |
|--------|-----------|---------|
| Host paths | Platform-native (`\` on Windows) | `C:\app\config.json` |
| Container paths | Always `/` | `/workspace/script.sh` |

### Conversion Pattern

```go
// Converting host path to container path
containerPath := "/workspace/" + filepath.ToSlash(relPath)

// WRONG: filepath.Join uses backslashes on Windows
containerPath := filepath.Join("/workspace", relPath)  // Broken on Windows!
```

### Path Security

`ResolveDockerfilePath()` includes path traversal detection to prevent `../..` escapes.

See `.claude/rules/windows.md` for comprehensive path handling guidance.

---

## SandboxAwareEngine Wrapper

The `SandboxAwareEngine` (`sandbox_engine.go`) is a decorator for Flatpak/Snap execution:

**Problem:** Container engines run on the host, not inside the sandbox. Paths don't match.

**Solution:** Execute commands via `flatpak-spawn --host` or `snap run --shell`.

```go
type SandboxAwareEngine struct {
    wrapped     Engine
    sandboxType platform.SandboxType
}

// Factory function wraps engine if sandbox detected
func NewEngine(preferredType EngineType) (Engine, error) {
    engine := createEngine(preferredType)
    return NewSandboxAwareEngine(engine), nil  // Auto-wraps if needed
}
```

---

## Engine Factory Functions

### Preference with Fallback

```go
// Tries preferred engine first, falls back to alternative
engine, err := container.NewEngine(container.Podman)  // or container.Docker
```

### Auto-Detection

```go
// Tries Podman first (better for rootless), then Docker
engine, err := container.AutoDetectEngine()
```

Both return wrapped `SandboxAwareEngine`.

---

## Exit Code Handling

Container engines distinguish between process exit codes and errors:

```go
result := &RunResult{}
if err != nil {
    var exitErr *exec.ExitError
    if errors.As(err, &exitErr) {
        result.ExitCode = exitErr.ExitCode()  // Process exited non-zero
    } else {
        result.ExitCode = 1
        result.Error = err  // Actual error (network, etc.)
    }
}
```

---

## Testing Patterns

### Unit Tests with Mocked Commands

```go
func TestDockerBuild(t *testing.T) {
    var capturedArgs []string
    mockExec := func(name string, args ...string) *exec.Cmd {
        capturedArgs = args
        return exec.Command("echo", "ok")
    }

    eng, _ := NewDockerEngine(WithExecCommand(mockExec))
    eng.Build(ctx, opts)

    // Verify expected arguments
    assert.Contains(t, capturedArgs, "--no-cache")
}
```

### Integration Tests

```go
func TestDockerBuild_Integration(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }
    // Test with real container engine
}
```

### testscript HOME Fix

Container tests using testscript need `HOME` set to a writable directory:

```go
Setup: func(env *testscript.Env) error {
    // Docker/Podman CLI requires valid HOME for config storage
    env.Setenv("HOME", env.WorkDir)
    return nil
},
```

### Container Test Timeout Strategy

Multi-layer timeout strategy prevents indefinite hangs:

1. **Per-test deadline** (3 minutes): `testscript.Params{Deadline: deadline}`
2. **Cleanup via `env.Defer()`**: Removes orphaned containers
3. **CI explicit timeout** (15 minutes): Safety net for catastrophic failures

---

## File Organization

| File | Purpose |
|------|---------|
| `engine.go` | Interface, factories, engine types |
| `engine_base.go` | Shared CLI implementation |
| `docker.go` | Docker concrete implementation |
| `podman.go` | Podman + SELinux/rootless logic |
| `sandbox_engine.go` | Flatpak/Snap wrapper decorator |
| `doc.go` | Package documentation |

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Using `filepath.Join()` for container paths | Backslashes on Windows | Use string concat with `/` or `filepath.ToSlash()` |
| Forgetting `HOME` in testscript | "mkdir /no-home: permission denied" | Set `HOME` to `env.WorkDir` in Setup |
| Testing with Alpine images | Unexpected musl behavior | Always use `debian:stable-slim` |
| Missing SELinux labels | Permission denied in Podman | Use Podman's auto-labeling or explicit `:z` |
| Container tests hanging | CI timeout | Use per-test deadline + cleanup in `env.Defer()` |
