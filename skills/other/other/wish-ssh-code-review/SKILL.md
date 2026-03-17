---
name: wish-ssh-code-review
description: Reviews Wish SSH server code for proper middleware, session handling, and security patterns. Use when reviewing SSH server code using charmbracelet/wish.
---

# Wish SSH Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Server setup, middleware | [references/server.md](references/server.md) |
| Session handling, security | [references/sessions.md](references/sessions.md) |

## Review Checklist

- [ ] Host keys are loaded from file or generated securely
- [ ] Middleware order is correct (logging first, auth early)
- [ ] Session context is used for per-connection state
- [ ] Graceful shutdown handles active sessions
- [ ] PTY requests are handled for terminal apps
- [ ] Connection limits prevent resource exhaustion
- [ ] Timeout middleware prevents hung connections
- [ ] BubbleTea middleware correctly configured

## Critical Patterns

### Server Setup

```go
// GOOD - complete server setup
s, err := wish.NewServer(
    wish.WithAddress(fmt.Sprintf("%s:%d", host, port)),
    wish.WithHostKeyPath(".ssh/id_ed25519"),
    wish.WithMiddleware(
        logging.Middleware(),       // first: log all connections
        activeterm.Middleware(),    // handle terminal sizing
        bubbletea.Middleware(teaHandler),
    ),
)
if err != nil {
    return fmt.Errorf("creating server: %w", err)
}
```

### Graceful Shutdown

```go
// BAD - abrupt shutdown
log.Fatal(s.ListenAndServe())

// GOOD - graceful shutdown
done := make(chan os.Signal, 1)
signal.Notify(done, os.Interrupt, syscall.SIGTERM)

go func() {
    if err := s.ListenAndServe(); err != nil && !errors.Is(err, ssh.ErrServerClosed) {
        log.Error("server error", "error", err)
    }
}()

<-done
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
if err := s.Shutdown(ctx); err != nil {
    log.Error("shutdown error", "error", err)
}
```

### BubbleTea Handler

```go
func teaHandler(s ssh.Session) (tea.Model, []tea.ProgramOption) {
    pty, _, _ := s.Pty()

    model := NewModel(pty.Window.Width, pty.Window.Height)

    return model, []tea.ProgramOption{
        tea.WithAltScreen(),
        tea.WithMouseCellMotion(),
    }
}
```

## When to Load References

- Reviewing server initialization → server.md
- Reviewing authentication, session state → sessions.md

## Review Questions

1. Are host keys handled securely?
2. Is middleware order correct?
3. Is graceful shutdown implemented?
4. Are PTY window sizes passed to the TUI?
5. Are connection timeouts configured?
