<!-- SOURCE-OF-TRUTH: plugins/codebase-audit-suite/shared/references/layer_rules.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Layer Boundary Rules

Layer violation detection and cross-layer consistency rules for ln-642.

## Auto-Discovery from docs/architecture.md

Read Section 4.2 (Top-Level Decomposition) and Section 5.3 (Infrastructure Layer Components) to determine project's layer structure and allowed dependencies.

## Common Architecture Presets (fallback if no architecture.md)

| Architecture | Layers | Dependency Direction |
|--------------|--------|---------------------|
| Layered (n-tier) | Presentation > Business > Data | top-down only |
| Hexagonal | Ports <> Adapters < Domain | adapters depend on ports |
| Clean | Controllers > UseCases > Entities | outside-in |
| Vertical Slices | Feature modules | no cross-slice deps |
| MVC | View > Controller > Model | no Model>View |

## I/O Pattern Boundary Rules

Regardless of architecture, these patterns should be isolated in infrastructure/adapters:

| Pattern | Forbidden In | Detection Grep | Allowed In |
|---------|--------------|----------------|------------|
| HTTP Client | domain/, services/, api/ | `httpx\\.\|aiohttp\\.\|requests\\.(get\|post)` | infrastructure/http/, clients/ |
| DB Session | domain/, services/, api/ | `session\\.(execute\|query\|add\|commit)` | infrastructure/persistence/, repositories/ |
| Raw SQL | domain/, services/ | `SELECT\\s.*FROM\|INSERT\\s+INTO` | infrastructure/persistence/ |
| File I/O | domain/ | `open\\(\|Path\\(.*\\)\\.(read\|write)` | infrastructure/storage/ |
| Env Access | domain/ | `os\\.(environ\|getenv)` | core/config/, settings/ |
| Framework | domain/ | `from\\s+(fastapi\|flask\|django)` | api/, infrastructure/ |

## Coverage Checks

| Check | Grep Pattern | Threshold |
|-------|--------------|-----------|
| HTTP Abstraction | `client\\.(get\|post\|put\|delete)` vs direct calls | 90% |
| Error Centralization | `except\\s+(httpx\|aiohttp\|requests)\\.` in <=2 files | Yes |

## Cross-Layer Consistency Checks

### Transaction Boundary Rules

| Owner Layer | commit() Allowed In | commit() Forbidden In |
|-------------|---------------------|----------------------|
| Service-owned UoW | services/ | repositories/, api/ |
| Endpoint-owned UoW | api/ | repositories/, services/ |
| Repository-owned UoW | repositories/ | services/, api/ |

**Detection:**
```
repo_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/repositories/**")
service_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/services/**")
api_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/api/**")
```

**Safe Patterns (not violations):**
- `# best-effort telemetry` comment in context
- `_callbacks.py` files (progress notifiers)
- `# UoW boundary` explicit marker

### Session Ownership Rules

| Pattern | Detection | Severity |
|---------|-----------|----------|
| DI + Local mix | `Depends(get_session)` in API AND `AsyncSessionLocal()` in service/repo | HIGH |
| Service local session | `AsyncSessionLocal()` in service calling DI-based repo | MEDIUM |

### Async Consistency Rules

| Blocking Pattern | Detection in `async def` | Safe Alternative |
|------------------|-------------------------|------------------|
| File read | `\\.read_bytes\\(\\)\|\\.read_text\\(\\)` | `asyncio.to_thread()` |
| File write | `\\.write_bytes\\(\\)\|\\.write_text\\(\\)` | `asyncio.to_thread()` |
| open() | `(?<!aiofiles\\.)open\\(` | `aiofiles.open()` |
| time.sleep | `time\\.sleep\\(` | `asyncio.sleep()` |
| requests | `requests\\.(get\|post)` | `httpx.AsyncClient` |

### Fire-and-Forget Rules

| Pattern | Detection | Severity |
|---------|-----------|----------|
| Task without handler | `create_task\\(` without `.add_done_callback(` | MEDIUM |
| Task in loop | `for.*create_task\\(` without error collection | HIGH |

**Safe Patterns:**
- `# fire-and-forget` comment documenting intent
- Task assigned to variable with later `await`
- Explicit `.add_done_callback(handle_exception)`

---
**Version:** 2.0.0
