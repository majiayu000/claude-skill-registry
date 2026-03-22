---
name: sindoq
description: Execute code in sandboxed environments using Docker, Podman, Wasmer, gVisor, Firecracker, Kubernetes, or cloud providers. Use when the user needs to safely run untrusted code, build AI code execution pipelines, or set up isolated sandbox environments.
---

# sindoq - AI Sandbox

sindoq (means "box" in Kurdish) is a Go SDK for sandboxed code execution. One API, any provider.

## Installation

```bash
go get github.com/happyhackingspace/sindoq
```

## Quick Start

### One-liner Execution

```go
result, err := sindoq.Execute(ctx, `print("Hello, World!")`)
fmt.Println(result.Stdout) // Hello, World!
```

### With Specific Provider

```go
sb, err := sindoq.Create(ctx, sindoq.WithProvider("docker"))
if err != nil {
    log.Fatal(err)
}
defer sb.Stop(ctx)

result, err := sb.Execute(ctx, `console.log("Hello")`, sindoq.WithLanguage("JavaScript"))
fmt.Println(result.Stdout)
```

### Streaming Output

```go
sb, err := sindoq.Create(ctx, sindoq.WithProvider("docker"))
defer sb.Stop(ctx)

err = sb.ExecuteStream(ctx, code, func(e *executor.StreamEvent) error {
    if e.Type == executor.StreamStdout {
        fmt.Print(e.Data)
    }
    return nil
})
```

### Async Execution

```go
results, err := sb.ExecuteAsync(ctx, code)
// Do other work...
result := <-results
fmt.Println(result.Stdout)
```

## Providers

| Provider | Type | Use Case |
|----------|------|----------|
| `docker` | Local | Development, CI/CD |
| `podman` | Local | Rootless containers |
| `wasmer` | Local | Cross-platform WASM sandbox (Linux, macOS, Windows) |
| `nsjail` | Local | Ultra-fast process isolation (~5ms, Linux only) |
| `gvisor` | Local | Strong isolation, syscall filtering (Linux only) |
| `firecracker` | Local | Maximum isolation (microVMs, Linux only) |
| `landlock` | Local | Kernel-level sandboxing via Landlock LSM (Linux 5.13+) |
| `seatbelt` | Local | Kernel-level sandboxing via sandbox-exec (macOS) |
| `kubernetes` | Cloud | Scalable workloads |
| `vercel` | Cloud | Serverless execution |
| `e2b` | Cloud | AI code interpreter |

## Provider Configuration

```go
// Docker
sb, _ := sindoq.Create(ctx, sindoq.WithDockerConfig(sindoq.DockerConfig{
    Host: "unix:///var/run/docker.sock",
}))

// Vercel
sb, _ := sindoq.Create(ctx, sindoq.WithVercelConfig(sindoq.VercelConfig{
    Token: os.Getenv("VERCEL_TOKEN"),
}))

// E2B
sb, _ := sindoq.Create(ctx, sindoq.WithE2BConfig(sindoq.E2BConfig{
    APIKey: os.Getenv("E2B_API_KEY"),
}))

// Wasmer (cross-platform)
sb, _ := sindoq.Create(ctx, sindoq.WithWasmerConfig(sindoq.WasmerConfig{
    WasmerPath: "wasmer",
    TimeLimit:  30,
}))

// Seatbelt (macOS)
sb, _ := sindoq.Create(ctx, sindoq.WithSeatbeltConfig(sindoq.SeatbeltConfig{
    EnableNetwork: false,
}))
```

## Features

- **Multi-provider support**: Docker, Podman, Wasmer, nsjail, gVisor, Firecracker, Landlock, Seatbelt, Kubernetes, Vercel, E2B
- **Auto language detection**: Automatically detects programming language from code
- **Streaming output**: Real-time stdout/stderr streaming
- **Async execution**: Non-blocking execution with channels
- **Resource limits**: Control CPU, memory, and execution time
- **File system access**: Read/write files in sandbox environments

## References

- Repository: https://github.com/HappyHackingSpace/sindoq
