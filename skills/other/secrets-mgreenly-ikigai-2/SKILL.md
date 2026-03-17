---
name: security/secrets
description: Secrets Management security skill
---

# Secrets Management

API keys and credentials require careful handling throughout their lifecycle.

## ikigai Application

**API keys (OpenAI, Anthropic, etc.):**
- Store in config file with `0600` permissions
- Load once at startup, hold in memory
- Never log, never include in error messages
- Never embed in source code or commits

**Memory handling:**
- Scrub secrets from memory when done: `explicit_bzero(key, len)`
- Avoid `strdup()` for secrets (can't track copies)
- Keep secret lifetime short and scoped

**Config file security:**
```c
// Check permissions before reading
struct stat st;
if (stat(path, &st) == 0 && (st.st_mode & 077) != 0) {
    return ERR(ctx, SECURITY, "Config file permissions too open");
}
```

**Never expose:**
- In logs or debug output
- In error messages shown to user
- In core dumps (`prctl(PR_SET_DUMPABLE, 0)`)
- Via environment to child processes

**Review red flags:** Secrets in `printf`/logging, `strdup` on credentials, missing permission checks.
