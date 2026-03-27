---
name: phx:examples
description: Practical examples and walkthroughs for Elixir/Phoenix patterns, including plugin workflow demonstrations. Use whenever the user asks "how do I...", "show me an example of...", "what does X look like", or needs to see a working implementation pattern for Phoenix, LiveView, Ecto, or OTP features. Also triggers when the user asks about plugin commands or wants to see what a workflow produces.
effort: low
---

# Examples & Walkthroughs

## Official Phoenix Guides (Reference)

For standard implementation patterns, always check official guides first:

| Topic | Guide |
|-------|-------|
| Contexts | [hexdocs.pm/phoenix/contexts](https://hexdocs.pm/phoenix/contexts.html) |
| Ecto Basics | [hexdocs.pm/phoenix/ecto](https://hexdocs.pm/phoenix/ecto.html) |
| LiveView | [hexdocs.pm/phoenix_live_view](https://hexdocs.pm/phoenix_live_view/welcome.html) |
| Authentication | [mix phx.gen.auth](https://hexdocs.pm/phoenix/mix_phx_gen_auth.html) |
| Channels | [hexdocs.pm/phoenix/channels](https://hexdocs.pm/phoenix/channels.html) |
| Testing | [hexdocs.pm/phoenix/testing](https://hexdocs.pm/phoenix/testing.html) |
| Deployment | [hexdocs.pm/phoenix/deployment](https://hexdocs.pm/phoenix/deployment.html) |

## Plugin-Specific Patterns

Patterns NOT in official guides (unique to this plugin):

### Tidewave Integration Workflow

```bash
# 1. Check if Tidewave is running
/mcp

# 2. If connected, debug with runtime tools
# Get exact docs for YOUR dependency versions
mcp__tidewave__get_docs "Ecto.Query"

# Execute code in running app
mcp__tidewave__project_eval "MyApp.Accounts.list_users() |> length()"

# Query database directly
mcp__tidewave__execute_sql_query "SELECT count(*) FROM users"
```

### Multi-Agent Review Workflow

```bash
# 1. Plan feature with specialist agents
/phx:plan Add user avatars with S3 upload

# 2. After implementation, review with multiple perspectives
/phx:review lib/my_app/accounts.ex  # Elixir idioms
# Security analyzer runs automatically on auth code

# 3. Before deployment
# Deployment validator checks production readiness
```

### Iron Laws Enforcement

This plugin enforces non-negotiable rules across all agents:

**Elixir Idioms:**

- NO process without runtime reason
- Messages are copied (keep small)
- Changesets for external data

**LiveView:**

- NEVER query DB in mount
- ALWAYS use streams for lists
- RE-AUTHORIZE in every handle_event

**Oban:**

- Jobs MUST be idempotent
- ALWAYS handle {:error, _} returns
- Use unique keys for deduplication

**Security:**

- Validate at boundaries
- Never interpolate user input in queries
- Authorize everywhere (not just mount)

## Example Workflows

### Bug Investigation

```bash
# 1. Start with obvious checks
/phx:investigate Login failing after password reset

# 2. Agent checks Ralph Wiggum list:
#    - File saved? Compiled? Migrated?
#    - Atom vs string keys?
#    - Data preloaded?

# 3. If complex, escalate to Ralph Wiggum Loop (if installed)
/ralph-loop:ralph-loop "Fix login tests. Output <promise>DONE</promise> when green."
```

### Feature Planning

```bash
# 1. Research phase
/phx:research Oban unique jobs best practices

# 2. Plan with context analysis
/phx:plan Add daily digest email job

# 3. Agents coordinate:
#    - hex-library-researcher evaluates deps
#    - oban-specialist designs worker
#    - ecto-schema-designer plans data model
```

### Security Audit

```bash
# 1. Run security analyzer on auth code
/phx:review lib/my_app_web/controllers/session_controller.ex

# 2. Check for common vulnerabilities:
#    - SQL injection (parameterized queries?)
#    - XSS (proper escaping?)
#    - CSRF (tokens present?)
#    - Authorization (re-checked in events?)
```

## When to Use Official Docs vs Plugin

| Situation | Use |
|-----------|-----|
| "How do I create a context?" | Official Phoenix guides |
| "Is my context design idiomatic?" | Plugin's `/phx:review` |
| "How do I add LiveView?" | Official LiveView guides |
| "Does my LiveView have memory issues?" | Plugin's Iron Laws |
| "How do I deploy to Fly.io?" | Official deployment guide |
| "Is my release config production-ready?" | Plugin's deployment-validator |
