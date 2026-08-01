# SLB Pattern Matching — Reference

## Table of Contents
- [Risk Tiers](#risk-tiers)
- [Default Patterns](#default-patterns)
- [Classification Algorithm](#classification-algorithm)
- [Request Lifecycle](#request-lifecycle)

---

## Risk Tiers

| Tier | Approvals | Auto-approve | Description |
|------|-----------|--------------|-------------|
| **CRITICAL** | 2+ | Never | Most dangerous, can destroy system/data |
| **DANGEROUS** | 1 | Never | Significant risk, needs review |
| **CAUTION** | 0 | After 30s | Minor risk, auto-approved with delay |
| **SAFE** | 0 | Immediately | Low risk, skip review |

---

## Default Patterns

### CRITICAL (2+ approvals)

- `rm -rf /...`
- `DROP DATABASE/SCHEMA`
- `TRUNCATE TABLE`
- `terraform destroy`
- `kubectl delete node/namespace/pv/pvc`
- `git push --force`
- `aws terminate-instances`
- `dd ... of=/dev/`

### DANGEROUS (1 approval)

- `rm -rf`
- `git reset --hard`
- `git clean -fd`
- `kubectl delete`
- `terraform destroy -target`
- `DROP TABLE`
- `chmod -R`
- `chown -R`

### CAUTION (auto-approved after 30s)

- `rm <file>`
- `git stash drop`
- `git branch -d`
- `npm/pip uninstall`

### SAFE (skip review)

- `rm *.log`
- `rm *.tmp`
- `git stash`
- `kubectl delete pod`
- `npm cache clean`

---

## Classification Algorithm

### 1. Normalization

Commands are parsed with shell-aware tokenization:
- Strips wrapper prefixes: `sudo`, `doas`, `env`, `time`, `nohup`
- Extracts inner commands from `bash -c 'command'`
- Resolves paths: `./foo` → `/absolute/path/foo`

### 2. Compound Command Handling

Commands with `;`, `&&`, `||`, `|` are split and each segment classified. **Highest risk segment wins**:

```
echo "done" && rm -rf /etc    →  CRITICAL (rm -rf /etc wins)
ls && git status              →  SAFE (no dangerous patterns)
```

### 3. Shell-Aware Splitting

Separators inside quotes preserved:

```
psql -c "DELETE FROM users; DROP TABLE x;"  →  Single segment (SQL)
echo "foo" && rm -rf /tmp                   →  Two segments
```

### 4. Pattern Precedence

SAFE → CRITICAL → DANGEROUS → CAUTION (first match wins)

### 5. Fail-Safe Parse Handling

If parsing fails, tier is **upgraded by one level**:
- SAFE → CAUTION
- CAUTION → DANGEROUS
- DANGEROUS → CRITICAL

---

## Request Lifecycle

### State Machine

```
                    ┌─────────────┐
                    │   PENDING   │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐───────────────┐
           ▼               ▼               ▼               ▼
     ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
     │ APPROVED │    │ REJECTED │    │ CANCELLED│    │ TIMEOUT  │
     └────┬─────┘    └──────────┘    └──────────┘    └────┬─────┘
          │              (terminal)      (terminal)       │
          ▼                                               ▼
     ┌──────────┐                                   ┌──────────┐
     │EXECUTING │                                   │ESCALATED │
     └────┬─────┘                                   └──────────┘
          │
   ┌──────┴──────┬──────────┐
   ▼             ▼          ▼
┌────────┐  ┌─────────┐  ┌────────┐
│EXECUTED│  │EXEC_FAIL│  │TIMED_OUT│
└────────┘  └─────────┘  └────────┘
(terminal)   (terminal)   (terminal)
```

### Approval TTL

- **Standard requests**: 30 minutes (configurable)
- **CRITICAL requests**: 10 minutes (stricter)

If approval expires before execution, re-approval required.
