# Pattern Scoring Rules

4-score model for evaluating architectural pattern implementations.

## Score Categories

| Score | Focus | Question Answered |
|-------|-------|-------------------|
| Compliance | Standards | "Does it follow industry standards?" |
| Completeness | Coverage | "Are all required parts implemented?" |
| Quality | Code | "Is the implementation well-written?" |
| Implementation | Reality | "Does it actually work in production?" |

## Compliance Score (0-100)

Measures adherence to industry standards and project conventions.

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Follows industry standard | +35 | Grep for pattern-specific structures (see pattern_library.md Detection Keywords) |
| Consistent naming conventions | +20 | `Grep("class.*{Pattern}(Service\|Handler\|Worker\|Processor)")` + file names match (`*_processor.py`, `*Handler.ts`) |
| Follows tech stack conventions | +20 | `Grep("{standard_lib}")` — e.g., Bull/BullMQ for Node.js jobs, Celery for Python |
| No anti-patterns detected | +25 | All anti-pattern checks below return 0 matches |

**Anti-pattern detection:**

| Anti-pattern | Detection Grep | Threshold |
|--------------|----------------|-----------|
| God class | File length >500 lines containing pattern keywords | Any match = -5 |
| Circular deps | `Grep("import.*{moduleA}")` in moduleB AND `Grep("import.*{moduleB}")` in moduleA | Any match = -10 |
| Mixed concerns | `Grep("httpx\|requests\|fetch")` in job/worker files | Any match = -5 |
| Hardcoded config | `Grep("localhost\|:5432\|:6379\|password.*=.*['\"]")` in pattern files | Any match = -5 |

## Completeness Score (0-100)

Measures whether all necessary components are present.

| Criterion | Points | Detection |
|-----------|--------|-----------|
| All required components present | +45 | Per-pattern component table below (each component has Grep) |
| Error handling implemented | +20 | `Grep("try\|catch\|except\|Error\|Exception\|\.catch\\(")` + `Grep("retry\|backoff\|dlq\|dead.?letter")` |
| Logging/observability | +20 | `Grep("logger\|logging\|log\\.\|structlog\|winston")` + `Grep("metrics\|prometheus\|statsd\|trace\|opentelemetry")` |
| Tests exist | +15 | `Glob("**/test*{pattern}*")` OR `Glob("**/*{pattern}*.test.*")` OR `Glob("**/*{pattern}*.spec.*")` |

**Required components by pattern (with detection):**

| Pattern | Component | Detection Grep | Weight |
|---------|-----------|----------------|--------|
| Job Processing | Queue | `Queue\|createQueue\|add_task\|enqueue` | 10 |
| Job Processing | Worker | `Worker\|process\|consume\|on_message` | 10 |
| Job Processing | DLQ | `dlq\|dead.?letter\|failed.?queue\|on_failed` | 10 |
| Job Processing | Retry config | `retry\|attempts\|backoff\|maxRetries` | 10 |
| Event-Driven | Publisher | `publish\|emit\|dispatch\|produce` | 10 |
| Event-Driven | Subscriber | `subscribe\|on\\(\|listen\|consume\|handler` | 10 |
| Event-Driven | Event schema | `EventSchema\|event_type\|EventType\|schema.*event` | 10 |
| Event-Driven | Event versioning | `version\|schema_version\|v[0-9]` in event files | 10 |
| Caching | Cache client | `Cache\|Redis\|createClient\|cache_client` | 10 |
| Caching | Invalidation | `invalidate\|evict\|delete.*cache\|bust.*cache` | 15 |
| Caching | TTL config | `ttl\|expire\|maxAge\|time.?to.?live` | 15 |
| Resilience | Circuit breaker | `CircuitBreaker\|circuit.?breaker\|breaker` | 10 |
| Resilience | Timeout | `timeout\|Timeout\|deadline\|time_limit` | 10 |
| Resilience | Fallback | `fallback\|Fallback\|default.*response\|graceful` | 10 |
| Resilience | Retry | `retry\|Retry\|with_retries\|retryWhen` | 10 |
| Repository | Interface | `interface.*Repository\|Protocol.*Repository\|ABC.*Repository` | 15 |
| Repository | Implementation | `class.*Repository.*implements\|class.*Repository\\(` | 15 |
| Repository | Unit of Work | `UnitOfWork\|unit.?of.?work\|commit\|transaction` | 10 |
| Singleton | Instance control | `_instance\|__new__\|getInstance\|SingletonMeta` | 15 |
| Singleton | Thread safety | `Lock\|threading\|synchronized\|Mutex` | 15 |
| Singleton | Lazy init | `if.*_instance.*None\|if.*instance.*null\|lazy` | 10 |
| Factory | Creator method | `create\|create_.*instance\|factory_method\|build` | 10 |
| Factory | Product interface | `Protocol\|ABC\|interface\|abstract.*class` | 15 |
| Factory | Registration | `register\|_creators\|_factory_map\|factory_registry` | 15 |
| Builder | Build method | `\.build()\|build_result\|construct\|to_.*()` | 10 |
| Builder | Setter chain | `return.*self\|return.*this\|with_\|set_` | 15 |
| Builder | Validation | `validate\|assert\|raise\|throw` in build | 15 |
| Adapter | Port/interface | `Protocol\|ABC\|Port\|interface.*Adapter` | 15 |
| Adapter | Implementation | `class.*Adapter.*:\|implements.*Port\|Adapter.*Protocol` | 15 |
| Adapter | Error translation | `except.*:.*raise\|catch.*throw\|map.*error` | 10 |
| Pipeline | Stage interface | `Protocol\|ABC\|Stage\|PipelineStep\|BaseStep` | 10 |
| Pipeline | Composition | `add_stage\|pipe\|compose\|chain\|>>` | 15 |
| Pipeline | Context | `context\|PipelineContext\|state\|pipe_data` | 15 |
| Strategy | Interface | `Protocol\|ABC\|interface.*Strategy\|abstract.*Strategy` | 15 |
| Strategy | Selection | `select.*strategy\|get_strategy\|strategy_map\|match` | 15 |
| Strategy | Implementation | `class.*Strategy.*:\|class.*Handler.*:` (2+ concrete) | 10 |
| Template Method | Abstract steps | `@abstractmethod\|abstract.*def\|pure.*virtual` | 15 |
| Template Method | Template method | `def.*process\|def.*execute\|def.*run` calling abstract steps | 15 |
| Template Method | Hook methods | `def.*hook\|on_before\|on_after\|pre_.*\|post_.*` | 10 |
| Registry | Registry storage | `_registry\|_handlers\|_map\|registry_dict` | 15 |
| Registry | Register method | `def.*register\|register(` | 15 |
| Registry | Lookup method | `def.*get\|get_handler\|resolve\|lookup` | 10 |
| Orchestrator | Step execution | `execute.*step\|run.*step\|step.*execute` | 10 |
| Orchestrator | State tracking | `workflow.*state\|execution.*log\|step.*status` | 10 |
| Orchestrator | Error recovery | `retry.*step\|compensate\|rollback\|on_error` | 10 |
| Orchestrator | Step definition | `add_step\|define.*step\|Step\|WorkflowStep` | 10 |
| Service Layer | Service class | `class.*Service.*:\|ServiceLayer\|ApplicationService` | 10 |
| Service Layer | DI constructor | `__init__.*repository\|@inject\|Depends(` | 10 |
| Service Layer | Transaction | `transaction\|commit\|UnitOfWork\|@Transactional` | 10 |
| Service Layer | DTO usage | `Schema\|DTO\|Input\|Output\|Request.*Model` | 10 |
| Dependency Injection | Container | `Container\|Injector\|Module\|Provider` | 10 |
| Dependency Injection | Binding | `bind\|provide\|register\|to_class\|to_value` | 10 |
| Dependency Injection | Injection point | `@inject\|Depends(\|@Inject\|constructor.*inject` | 10 |
| Dependency Injection | Scope | `Scope\|Singleton\|Transient\|Scoped\|Request.*scope` | 10 |
| CQRS | Command handler | `CommandHandler\|handle_command\|command.*handler` | 10 |
| CQRS | Query handler | `QueryHandler\|handle_query\|query.*handler` | 10 |
| CQRS | Read model | `ReadModel\|read_model\|Projection\|materialized` | 10 |
| CQRS | Write model | `WriteModel\|write_model\|Aggregate\|command.*model` | 10 |
| Event Sourcing | Event store | `EventStore\|event_store\|append_events\|get_events` | 10 |
| Event Sourcing | Aggregate root | `AggregateRoot\|aggregate_root\|apply_event` | 10 |
| Event Sourcing | Event schema | `DomainEvent\|event_type\|event.*schema\|EventBase` | 10 |
| Event Sourcing | Snapshot | `snapshot\|Snapshot\|create_snapshot\|load_snapshot` | 10 |
| Saga | Step definition | `SagaStep\|step.*define\|saga.*step\|add_step` | 10 |
| Saga | Compensation | `compensate\|rollback\|undo\|revert.*step` | 15 |
| Saga | State tracking | `saga.*state\|step.*status\|saga.*log` | 15 |
| API Gateway | Routing | `route\|proxy\|forward\|upstream\|gateway.*route` | 10 |
| API Gateway | Rate limiting | `rate.?limit\|throttle\|RateLimit` | 10 |
| API Gateway | Authentication | `auth\|token.*verify\|jwt.*verify\|middleware.*auth` | 10 |
| API Gateway | Error handling | `error.*handler\|global.*error\|exception.*filter` | 10 |
| Message Queue | Producer | `produce\|publish\|send_message\|enqueue` | 10 |
| Message Queue | Consumer | `consume\|subscribe\|on_message\|handle_message` | 10 |
| Message Queue | DLQ | `dlq\|dead.?letter\|rejected\|nack` | 10 |
| Message Queue | Ack/Nack | `ack\|acknowledge\|nack\|reject\|basic_ack` | 10 |
| HTTP Client | Client class | `HttpClient\|ApiClient\|RestClient\|AsyncClient` | 10 |
| HTTP Client | Timeout config | `timeout\|Timeout\|connect_timeout\|read_timeout` | 10 |
| HTTP Client | Error handling | `raise_for_status\|status_code\|HTTPError\|check.*response` | 10 |
| HTTP Client | Retry/pool | `retry\|pool\|max_connections\|limits\|Retry` | 10 |
| Rate Limiting | Limiter setup | `RateLimit\|Limiter\|rate_limit\|@rate_limit` | 10 |
| Rate Limiting | Storage backend | `Redis\|Memcached\|in_memory\|rate_limit.*store` | 10 |
| Rate Limiting | Response handling | `429\|TooManyRequests\|rate.*exceeded\|Retry-After` | 10 |
| Rate Limiting | Per-route config | `limit.*route\|per_endpoint\|route.*limit` | 10 |
| Parameter Object | Typed fields | `@dataclass\|BaseModel\|NamedTuple\|TypedDict` | 15 |
| Parameter Object | Immutability | `frozen=True\|readonly\|Readonly\|immutable` | 15 |
| Parameter Object | Validation | `validator\|__post_init__\|validate\|field_validator` | 10 |
| Fail-Fast Validation | Schema definition | `BaseModel\|Schema\|@dataclass\|validate.*schema` | 10 |
| Fail-Fast Validation | Validation at entry | `@validator\|field_validator\|@validate\|ValidationError` | 15 |
| Fail-Fast Validation | Error response | `ValidationError\|422\|validation.*error\|errors()` | 15 |
| Client Notification | Send mechanism | `notify\|send.*webhook\|callback\|push.*notification` | 10 |
| Client Notification | Retry | `retry\|backoff\|max_attempts\|retry.*notify` | 10 |
| Client Notification | Security | `hmac\|signature\|secret\|sign.*payload\|webhook.*secret` | 10 |
| Client Notification | Delivery tracking | `delivered\|acknowledged\|delivery.*log\|callback.*status` | 10 |

## Quality Score (0-100)

Measures code quality and maintainability.

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Code readable (short methods) | +25 | Average method length <30 lines; `Grep("def \|function \|=>")` count vs file length |
| Maintainable (low complexity) | +25 | No deep nesting: `Grep("if.*if.*if\|for.*for.*for")` returns 0 matches |
| No code smells | +20 | All smell checks below return 0 matches |
| Follows SOLID | +15 | `Grep("interface\|abstract\|Protocol\|ABC\|@inject\|Depends\\(")` present |
| Performance optimized | +15 | `Grep("async\|await\|Promise\|cache\|memoize\|lru_cache")` present |

**Code smell detection:**

| Smell | Detection Grep | Threshold |
|-------|----------------|-----------|
| Magic numbers | `Grep("[^0-9][0-9]{2,}[^0-9]")` outside config/const files | >3 = -5 |
| Long params | `Grep("def.*,.*,.*,.*,.*,")` (5+ comma-separated) | Any = -3 per |
| Deep nesting | `Grep("^\\s{16,}(if\|for\|while)")` (4+ indent levels) | Any = -5 per |
| Large files | Pattern files >300 lines | Any = -5 per |

## Implementation Score (0-100)

Measures whether the pattern actually works in production.

| Criterion | Points | Detection |
|-----------|--------|-----------|
| Code exists and compiles | +30 | `Bash("npm run build")` or `Bash("python -m py_compile {file}")` — no errors |
| Used in production paths | +25 | `Grep("from.*{module}\|import.*{module}\|require.*{module}")` outside test files, >0 matches |
| No dead/unused implementations | +15 | `Grep("export\|__all__")` in pattern files → verify each export imported elsewhere |
| Integrated with other patterns | +15 | `Grep("@inject\|Depends\\(\|container\|config\|settings\|env")` in pattern files |
| Monitored/observable | +15 | `Grep("health.?check\|readiness\|liveness\|/health\|metrics\|prometheus")` in pattern files |

## Thresholds and Actions

| Score Range | Status | Action |
|-------------|--------|--------|
| ≥80% | ✅ Good | No action needed |
| 70-79% | ⚠️ Warning | Create improvement task (LOW priority) |
| 60-69% | ❌ Below threshold | Create refactor Story (MEDIUM priority) |
| <60% | 🚨 Critical | Create refactor Story (HIGH priority) |

## Effort Estimation

| Issue Type | Typical Effort |
|------------|----------------|
| Add error handling | 4h |
| Add tests | 4-8h |
| Refactor for SOLID | 1-2d |
| Add DLQ/retry logic | 4-8h |
| Major architectural change | 3-5d |

## Trend Calculation

Compare current audit with previous:

```
trend = "improving" if avg_score > prev_avg_score + 5%
trend = "declining" if avg_score < prev_avg_score - 5%
trend = "stable" otherwise
```

## Architecture Health Score

Weighted average of all patterns:

```
health_score = (
  sum(pattern.compliance * 0.25 +
      pattern.completeness * 0.25 +
      pattern.quality * 0.25 +
      pattern.implementation * 0.25)
) / pattern_count
```

## Layer Compliance Scoring

Layer violations detected by ln-642 affect **Compliance** and **Quality** scores.

### Deductions from Compliance Score

| Violation | Deduction | Rationale |
|-----------|-----------|-----------|
| I/O code in domain layer | -15 points | Violates architecture principles |
| I/O code in services layer | -10 points | Should use abstractions |
| Direct framework import in domain | -10 points | Domain should be framework-agnostic |

### Deductions from Quality Score

| Issue | Deduction | Rationale |
|-------|-----------|-----------|
| HTTP call without abstraction | -10 points | Missing client layer |
| Error handling in >2 files | -5 per extra file | Duplication, should centralize |
| Pattern coverage <80% | -10 points | Inconsistent architecture |
| Functions with cascade depth >= 3 | -5 per function | Deep cascade chain (source: ln-624 Rule 10) |
| Read-named functions with hidden writes | -5 per function | Architecturally dishonest interface (source: ln-643 Rule 6) |
| Service chain depth >= 3 levels | -10 per chain | Deep orchestration (source: ln-642 Phase 3.3) |

### Layer Violation Thresholds

| Violations Count | Impact |
|------------------|--------|
| 0 | Full score maintained |
| 1-3 | Warning, create improvement tasks |
| 4-10 | Below threshold, create refactor Story |
| >10 | Critical, prioritize architectural cleanup |

## Score Conversion

For cross-audit reporting between ln-620 (X/10) and ln-640 (0-100%):

| 4-Score Average | Equivalent X/10 | Status |
|-----------------|-----------------|--------|
| 90-100% | 9-10 | ✅ Healthy |
| 70-89% | 7-8 | ⚠️ Warning |
| 50-69% | 5-6 | ❌ Below threshold |
| <50% | <5 | 🚨 Critical |

**Formula:** `x_10 = round(percent / 10)`

## Generic Scoring (Adaptive Discovery Patterns)

For patterns discovered via Phase 1b heuristics that have no predefined components above, use these universal criteria:

| Score | Generic Criterion | Points | Detection |
|-------|------------------|--------|-----------|
| Compliance | Consistent naming | +45 | Class/file names contain pattern name |
| Compliance | No anti-patterns | +55 | Same anti-pattern table as above |
| Completeness | Core implementation exists | +35 | Files with pattern evidence (from discovery) |
| Completeness | Error handling | +35 | `Grep("try\|catch\|except\|Error")` in pattern files |
| Completeness | Tests exist | +30 | `Glob("**/test*{pattern}*")` |
| Quality | Short methods (<30 lines) | +25 | Same detection as Quality section |
| Quality | No code smells | +25 | Same smell table as above |
| Quality | Follows SOLID | +25 | Interfaces/abstractions present |
| Quality | Low complexity | +25 | No deep nesting |
| Implementation | Used in production paths | +35 | Imported outside test files |
| Implementation | Integrated with DI/config | +35 | `@inject\|Depends\|config\|settings` |
| Implementation | Monitored | +30 | `logger\|metrics\|health` in pattern files |

---
**Version:** 2.0.0
