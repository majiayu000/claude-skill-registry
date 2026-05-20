---
name: mcp-cloudflare
description: "Manage Workers/KV/R2/D1/Hyperdrive via Cloudflare MCP, perform observability/build troubleshooting/audit/container sandbox operations. Triggers: worker/KV/R2/D1/logs/build/deploy/screenshot/audit/sandbox. Three permission tiers: Diagnose (read-only), Change (write requires confirmation), Super Admin (isolated environment). Write operations must follow read-first, user confirmation, post-execution verification."
disable-model-invocation: true
---

# Cloudflare MCP Skill

Interact with Cloudflare services via MCP: Workers, KV, R2, D1, Hyperdrive, Observability, Builds, Audit, Container Sandbox.

## File-based Pipeline (Pass Paths Only)

When integrating troubleshooting/changes into multi-step workflows, persist all evidence and artifacts to disk, passing only paths between agents/sub-agents.

Recommended directory structure (within project): `runs/<workflow>/active/<run_id>/`

- Input: `01-input/goal.md` (symptoms/objectives), `01-input/context.json` (account/worker/resource/time_range, etc.)
- Evidence: `02-analysis/observability.md`, `02-analysis/audit.md`, `02-analysis/screenshots/`
- Plan: `03-plans/change-plan.md` (write operation plan; must write here and await confirmation first)
- Output: `05-final/report.md` (conclusion + evidence chain + tool call summary + next steps)
- Logs: `logs/events.jsonl` (summary of each tool call)

## Permission Tiers (Core Principles)

| Tier | Purpose | Tool Scope | Risk Control |
|------|---------|------------|--------------|
| **Diagnose** | Read-only/query/troubleshoot | Observability, Builds, Browser, Audit | Default entry point, no write operations |
| **Change** | Create/modify/delete resources | Workers Bindings (KV/R2/D1) | Requires user confirmation, post-execution verification |
| **Super Admin** | Highest privileges | All + Container Sandbox | Only in isolated environments/test accounts |

## Tool Reference

### Diagnose Tier (Read-only)

**Observability**
| Tool | Purpose |
|------|---------|
| `query_worker_observability` | Query logs/metrics (events, CPU, error rate) |
| `observability_keys` | Discover available fields |
| `observability_values` | Explore field values |

**Builds**
| Tool | Purpose |
|------|---------|
| `workers_builds_list_builds` | List build history |
| `workers_builds_get_build` | Get build details |
| `workers_builds_get_build_logs` | Get build logs |

**Browser Rendering (Page Capture)**
| Tool | Purpose |
|------|---------|
| `get_url_html_content` | Fetch page HTML |
| `get_url_markdown` | Convert to Markdown |
| `get_url_screenshot` | Take page screenshot |

**Audit Logs**
| Tool | Purpose |
|------|---------|
| `auditlogs_by_account_id` | Pull change history by time range |

### Change Tier (Write Operations)

**Account**
| Tool | Purpose |
|------|---------|
| `accounts_list` | List accounts |
| `set_active_account` | Set active account |

**Builds (Settings)**
| Tool | Purpose |
|------|---------|
| `workers_builds_set_active_worker` | ⚠️ Set active worker (requires confirmation) |

**KV**
| Tool | Purpose |
|------|---------|
| `kv_namespaces_list` | List namespaces |
| `kv_namespace_get` | Get details |
| `kv_namespace_create` | Create (⚠️ requires confirmation) |
| `kv_namespace_update` | Update (⚠️ requires confirmation) |
| `kv_namespace_delete` | Delete (⚠️ requires confirmation) |

**R2**
| Tool | Purpose |
|------|---------|
| `r2_buckets_list` | List buckets |
| `r2_bucket_get` | Get details |
| `r2_bucket_create` | Create (⚠️ requires confirmation) |
| `r2_bucket_delete` | Delete (⚠️ requires confirmation) |

**D1**
| Tool | Purpose |
|------|---------|
| `d1_databases_list` | List databases |
| `d1_database_get` | Get details |
| `d1_database_query` | Execute SQL |
| `d1_database_create` | Create (⚠️ requires confirmation) |
| `d1_database_delete` | Delete (⚠️ requires confirmation) |

**Hyperdrive**
| Tool | Purpose |
|------|---------|
| `hyperdrive_configs_list` | List configs |
| `hyperdrive_config_get` | Get details |
| `hyperdrive_config_create` | Create (⚠️ requires confirmation) |
| `hyperdrive_config_edit` | Edit (⚠️ requires confirmation) |
| `hyperdrive_config_delete` | Delete (⚠️ requires confirmation) |

**Workers**
| Tool | Purpose |
|------|---------|
| `workers_list` | List workers |
| `workers_get_worker` | Get worker details |
| `workers_get_worker_code` | Get source code |

### Super Admin Tier (Container Sandbox)

| Tool | Purpose |
|------|---------|
| `container_initialize` | Initialize container (~10 min lifecycle) |
| `container_exec` | Execute command |
| `container_file_write` | Write file |
| `container_file_read` | Read file |
| `container_files_list` | List files |
| `container_file_delete` | Delete file |

**Container Notes**: No persistent state, short lifespan, only for temporary tasks (running tests/reproducing issues/parsing data).

## Security Rules (Must Follow)

### Read Operations
1. **Define scope first**: account / worker / resource ID
2. **No account? Run `accounts_list` first**
3. Conclusions must have evidence chain: logs/screenshots/audit records

### Write Operations (Three-step Flow)
```
1. Plan: Read current state first (list/get)
2. Confirm: Output precise change (name/ID/impact scope), await user confirmation
3. Execute: create/delete/update
4. Verify: audit logs + observability confirm no new errors
```

### Prohibited Actions
- ❌ Execute create/delete/update without confirmation
- ❌ Delete production resources (unless user explicitly says "delete production xxx")
- ❌ Use Super Admin privileges in non-isolated environments
- ❌ Use container sandbox as persistent environment

## Operation Workflows

### Troubleshooting Flow (Typical)
```
1. Clarify symptoms → worker name/time range/error type
2. query_worker_observability to pull logs/metrics
3. If build-related → workers_builds_get_build_logs
4. If page-related → get_url_screenshot to reproduce
5. Trace changes → auditlogs_by_account_id
6. Summarize: root cause + evidence + fix recommendations
```

### Resource Management Flow
```
1. accounts_list → set_active_account
2. List resources (kv_namespaces_list / r2_buckets_list / d1_databases_list)
3. Plan changes → present to user
4. Execute after confirmation
5. Verify: audit logs + observability shows no errors
```

## Output Format

- **Language**: English
- **Structure**: Conclusion → Key data/evidence → Tool call summary → Next steps
- **Write operations**: Must clearly list operations to be executed and impact scope

Example output:
```
✅ Investigation complete: worker `api-gateway` experienced 5xx spike between 18:00-18:30

Root cause: New code deployed threw TypeError when processing /v2/users
Evidence:
- Logs: 18:02 first occurrence of "Cannot read property 'id' of undefined"
- Audit: 18:00 user dev@example.com deployed new version
- Metrics: error_rate jumped from 0.1% to 12%

Recommendation: Roll back to previous version, or fix /v2/users handler
```

## Error Handling

| Situation | Action |
|-----------|--------|
| Account not set | Run `accounts_list` → `set_active_account` first |
| Resource doesn't exist | Verify ID/name is correct, list available resources |
| Insufficient permissions | Explain required permissions, suggest checking API token scope |
| Observability query too long | Split into smaller time ranges, ask more specific questions |

## Scenario Examples

See [scenarios.md](scenarios.md) for 20 real-world development scenarios.
