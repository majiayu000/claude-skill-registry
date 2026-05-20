---
name: af-gidev-server
description: |
  Use when working with GiDev server operations - worktrees, tmux sessions, Caddy routing,
  port allocation, start-work/stop-work scripts, or server-specific tooling. For AWS credentials
  and DNS operations, use `af-environment-infrastructure` instead.

title: GiDev Server Operations
created: 2025-12-11
updated: 2026-01-03
last_checked: 2026-01-03
tags: [skill, expertise, gidev, server, worktrees, caddy]
parent: ../README.md
---

# GiDev Server Operations

Directive knowledge for GiDev server-specific operations: worktrees, tmux, Caddy routing, and dev tooling.

## When to Use This Skill

Load this skill when you need to:
- Create or manage git worktrees
- Work with tmux sessions
- Configure Caddy routing for dev URLs
- Use start-work/stop-work scripts
- Understand port allocation
- Query the project registry

**For AWS/DNS/credentials:** Use `af-environment-infrastructure` instead.

## Skills Referenced

- **`af-environment-infrastructure`** - For AWS credentials, DNS, Doppler patterns

---

## Quick Reference

### Key Locations

| Component | Location |
|-----------|----------|
| Project registry | `project-registry` CLI |
| Bare repos | `/srv/repos/` |
| Worktrees | `/srv/worktrees/{project}/{issue}` |
| Server docs | `/srv/docs/` |
| Caddy configs | `/etc/caddy/sites-enabled/` |

### Port Allocation Formula

```bash
ISSUE_NUM="${ISSUE_KEY##*-}"           # Extract number from JCN-123
MAIN_PORT=$((PORT_BASE + ISSUE_NUM))   # Main app
STORYBOOK_PORT=$((PORT_BASE + 3000 + ISSUE_NUM))  # Storybook
TEST_REPORT_PORT=$((PORT_BASE + 6000 + ISSUE_NUM)) # Test reports
```

### Project Port Bases

| Project | Port Base | Example (issue 4) |
|---------|-----------|-------------------|
| indigo | 3000 | 3004, 6004, 9004 |
| juncan | 23000 | 23004, 26004, 29004 |
| andon | 13000 | 13004, 16004, 19004 |

---

## Rules

### Worktree Rules (MUST)

1. **MUST use start-work to create worktrees.** Never manually create worktrees - the script handles port allocation, Caddy config, and tmux.

2. **MUST use stop-work to clean up.** It removes Caddy configs, kills processes, and deletes the worktree properly.

3. **MUST NOT switch branches in a worktree.** Each worktree is dedicated to one issue. Ask user permission before any `git checkout` or `git switch`.

### Caddy Rules (MUST)

4. **MUST use http:// prefix in Caddy configs.** Traffic comes through Cloudflare Tunnel which handles HTTPS:
   ```caddy
   http://jcn-4.gaininsight.co.uk {
       reverse_proxy localhost:23004
   }
   ```

5. **MUST reload Caddy after config changes:**
   ```bash
   sudo caddy reload --config /etc/caddy/Caddyfile
   ```

### Permission Rules (SHOULD)

6. **SHOULD run fix-permissions if encountering permission errors.** Worktrees need correct ownership for shared access.

7. **SHOULD use project-registry to check project config** before making assumptions.

---

## Workflows

### Workflow: Start Work on an Issue

**When:** Beginning work on a Linear issue

**Command:**
```bash
start-work {project} {ISSUE-KEY}
# Example: start-work juncan JCN-4
```

**What happens:**
1. Creates worktree at `/srv/worktrees/{project}/{ISSUE-KEY}`
2. Allocates ports based on issue number
3. Creates Caddy configs for main app, storybook, test reports
4. Creates tmux session named `{ISSUE-KEY}`
5. Generates `PORT_INFO.md` with allocated ports
6. Runs `.start-work-hooks` if present

**After starting:**
```bash
tmux attach -t JCN-4   # Attach to session
cat PORT_INFO.md       # See allocated ports
```

### Workflow: Stop Work on an Issue

**When:** Finished with an issue or need to clean up

**Command:**
```bash
stop-work {ISSUE-KEY}
# Example: stop-work JCN-4
```

**What happens:**
1. Runs `.stop-work-hooks` if present (cleanup, sandbox deletion)
2. Kills tmux session
3. Removes Caddy configs
4. Deletes worktree

### Workflow: Fix Permission Issues

**When:** Encountering "permission denied" errors in worktrees

**Command:**
```bash
fix-permissions
# Or for specific worktree:
fix-permissions /srv/worktrees/juncan/JCN-4
```

### Workflow: Query Project Configuration

**When:** Need to know project settings

**Commands:**
```bash
project-registry list              # List all projects
project-registry juncan            # Show project config
project-registry juncan aws        # Show AWS accounts
project-registry accounts          # List all AWS accounts
project-registry validate          # Validate registry file
```

---

## Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| "permission denied" | Wrong file ownership | Run `fix-permissions` |
| URL not accessible | Caddy not reloaded | `sudo caddy reload --config /etc/caddy/Caddyfile` |
| Port already in use | Another worktree using same issue number | Check with `ss -tulpn \| grep {port}` |
| Caddy HTTPS errors | Using `https://` prefix | Change to `http://` (Cloudflare handles TLS) |
| Worktree exists | Previous work not cleaned up | Run `stop-work {ISSUE-KEY}` first |

---

## Essential Reading

| Document | Purpose |
|----------|---------|
| `/srv/docs/CLAUDE.md` | Main AI agent context for GiDev |
| `/srv/docs/DEV_SERVER_ROUTING_CADDY.md` | Port allocation and Caddy details |
| `/srv/docs/DEVELOPER_ONBOARDING.md` | Full developer setup guide |
| `/srv/docs/PERMISSIONS.md` | Permission troubleshooting |

---

**Remember:**
1. Use start-work/stop-work, not manual worktree commands
2. Caddy configs use `http://` (Cloudflare handles HTTPS)
3. Don't switch branches in worktrees without permission
4. Run fix-permissions for ownership issues
