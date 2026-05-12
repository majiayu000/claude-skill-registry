# Architectural Pattern Library

Detection patterns, best practices, and discovery heuristics for ln-640/ln-641.

Patterns below are a **baseline seed** — ln-640 Phase 1b uses Discovery Heuristics to find additional project-specific patterns beyond this table.

## Pattern Detection (Grep)

| Group | Pattern | Detection Keywords | File Types |
|-------|---------|-------------------|------------|
| Creational | Singleton | `_instance\|__new__\|@singleton\|SingletonMeta\|getInstance` | *.py, *.ts, *.js, *.java, *.cs |
| Creational | Factory | `Factory\|create_.*instance\|FactoryMethod\|AbstractFactory\|factory_method` | *.py, *.ts, *.js, *.java, *.cs |
| Creational | Builder | `Builder\|\.build()\|with_.*return.*self\|\.set_.*\.set_` | *.py, *.ts, *.js, *.java, *.cs |
| Structural | Adapter | `Adapter\|adapt(\|Protocol.*class.*ABC\|implements.*Port` | *.py, *.ts, *.js, *.java, *.cs |
| Structural | Pipeline | `Pipeline\|Stage\|PipelineStep\|add_stage\|compose_stages\|pipe_chain` | *.py, *.ts, *.js, *.go |
| Behavioral | Strategy | `Strategy\|StrategyPattern\|set_strategy\|execute_strategy\|HandlerRegistry` | *.py, *.ts, *.js, *.java, *.cs |
| Behavioral | Template Method | `@abstractmethod.*def\|class.*ABC.*:.*def\|template_method\|TemplateMethod` | *.py, *.ts, *.js, *.java |
| Behavioral | Registry | `_registry\|register(\|get_handler\|_handlers\[\|HandlerRegistry` | *.py, *.ts, *.js |
| Behavioral | Orchestrator | `Orchestrator\|orchestrate\|WorkflowEngine\|step.*execute` | *.py, *.ts, *.js |
| Architecture | Service Layer | `class.*Service.*:\|ServiceLayer\|ApplicationService\|@Service` | *.py, *.ts, *.js, *.java, *.cs |
| Architecture | Dependency Injection | `Depends(\|@inject\|container\|Provider\|bind\|Injector` | *.py, *.ts, *.js, *.java, *.cs |
| Architecture | Repository | `Repository\|findBy\|findOne\|save\|delete\|@Repository` | *.ts, *.js, *.py, *.java |
| Architecture | CQRS | `Command\|Query\|ReadModel\|WriteModel\|CommandHandler` | *.ts, *.js, *.cs |
| Architecture | Event Sourcing | `EventStore\|Aggregate\|AggregateRoot\|DomainEvent` | *.ts, *.js, *.cs |
| Infrastructure | Job Processing | `Queue\|Worker\|Job\|Bull\|BullMQ\|Celery\|Sidekiq` | *.ts, *.js, *.py, *.rb |
| Infrastructure | Event-Driven | `EventEmitter\|publish\|subscribe\|emit\|on(\s*['"]` | *.ts, *.js, *.py |
| Infrastructure | Caching | `Cache\|Redis\|Memcached\|TTL\|invalidate\|@Cacheable` | *.ts, *.js, *.py, *.java |
| Infrastructure | Resilience | `CircuitBreaker\|Retry\|Timeout\|Fallback\|Bulkhead` | *.ts, *.js, *.py |
| Infrastructure | Message Queue | `RabbitMQ\|Kafka\|SQS\|AMQP\|MessageBroker` | *.ts, *.js, *.py |
| Infrastructure | HTTP Client | `httpx.AsyncClient\|aiohttp.ClientSession\|HttpClient\|RestClient\|ApiClient` | *.py, *.ts, *.js, *.java |
| Infrastructure | API Gateway | `Gateway\|Proxy\|RateLimit\|ApiGateway` | *.ts, *.js, *.py |
| Infrastructure | Rate Limiting | `RateLimit\|rate_limit\|slowapi\|throttle\|@rate_limit\|Throttle` | *.py, *.ts, *.js, *.java |
| Communication | Saga | `Saga\|SagaStep\|Compensate\|compensat` | *.ts, *.js, *.py |
| Communication | Client Notification | `notify\|callback_url\|webhook\|SSE\|EventSource\|WebSocket.*send` | *.py, *.ts, *.js |
| Data | Parameter Object | `@dataclass.*frozen\|NamedTuple\|TypedDict\|ValueObject\|@value_object` | *.py, *.ts, *.js, *.java, *.cs |
| Data | Fail-Fast Validation | `ValidationError\|@validator\|@validate\|pydantic.BaseModel\|field_validator` | *.py, *.ts, *.js |
| Architecture | Flat Orchestration | `Orchestrator\|Coordinator\|Workflow\|UseCase\|CommandHandler` | *.py, *.ts, *.js, *.java, *.cs |

---

## Key Best Practices by Pattern

### Singleton

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Thread safety | `Lock\|threading.Lock\|synchronized\|Mutex\|lock` | HIGH |
| Lazy initialization | `if.*_instance.*None\|if.*instance.*null\|lazy` | MEDIUM |
| Testing support (reset) | `reset\|_instance.*=.*None\|clear_instance\|@pytest.fixture` | MEDIUM |
| No global mutable state | Instance fields are configuration/clients only | LOW |

### Factory

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Interface/protocol for products | `Protocol\|ABC\|interface\|abstract.*class` used by factory | HIGH |
| Registration mechanism | `register\|_creators\|_factory_map\|factory_registry` | MEDIUM |
| Configuration-driven | `config\|settings\|env` in factory create | MEDIUM |
| Error on unknown type | `raise.*Unknown\|throw.*not.*supported\|ValueError\|KeyError` in factory | MEDIUM |

### Builder

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Fluent interface | `return.*self\|return.*this` in setter methods | MEDIUM |
| Validation on build | `validate\|assert\|raise\|throw` in build() method | HIGH |
| Immutable result | `frozen\|readonly\|immutable\|@dataclass.*frozen` on built object | MEDIUM |
| Default values | `default\|Optional\|=.*None\|=.*null` in builder fields | LOW |

### Adapter

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Port/interface definition | `Protocol\|ABC\|interface\|Port\|abstract.*class` | HIGH |
| Single responsibility | Adapter file <100 lines, 1 class per file | MEDIUM |
| Error translation | `except.*:.*raise\|catch.*throw\|map.*error\|translate.*exception` | MEDIUM |
| Dependency inversion | `@inject\|Depends\|constructor.*interface\|bind.*to` | HIGH |

### Pipeline

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Stage interface | `Protocol\|ABC\|interface\|Stage\|PipelineStep` | HIGH |
| Error handling per stage | `try.*stage\|catch.*step\|on_stage_error\|stage.*error` | HIGH |
| Stage composition | `add_stage\|pipe\|compose\|>>.*stage\|chain` | MEDIUM |
| Context/state passing | `context\|PipelineContext\|state\|pipe_data` | MEDIUM |

### Strategy

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Strategy interface | `Protocol\|ABC\|interface\|abstract.*Strategy` | HIGH |
| Runtime selection | `select.*strategy\|get_strategy\|strategy_map\|match.*strategy` | MEDIUM |
| Default strategy | `default.*strategy\|fallback.*strategy\|else.*strategy` | LOW |
| Open/closed principle | Registration/config-based, no `if/elif/switch` chains >3 | MEDIUM |

### Template Method

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Abstract steps | `@abstractmethod\|abstract.*def\|pure.*virtual` | HIGH |
| Hook methods | `def.*hook\|on_before\|on_after\|pre_.*\|post_.*` (overridable, non-abstract) | MEDIUM |
| Final template method | Template method itself not overridable | LOW |
| Documentation | Docstring on template method explaining step order | MEDIUM |

### Registry

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Type-safe registration | `register.*type\|register.*class\|registry\[.*\].*=` | MEDIUM |
| Duplicate detection | `already.*registered\|duplicate.*key\|KeyError\|raise.*exists` | MEDIUM |
| Lazy loading | `lazy\|load_on_demand\|import_module\|__import__` in registry | LOW |
| Auto-discovery | `__subclasses__\|entry_points\|scan.*module\|discover` | LOW |

### Orchestrator

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Step tracking | `step.*status\|workflow.*state\|execution.*log` | HIGH |
| Error recovery | `retry.*step\|compensate\|rollback\|on_error` | HIGH |
| Timeout per step | `timeout\|deadline\|step.*timeout` | MEDIUM |
| Parallel execution | `gather\|Promise.all\|parallel\|concurrent\|asyncio.gather` | LOW |

#### Flat Orchestration (AI-Ready variant)

> "Flat Orchestration" = sequential step orchestration at single level. NOT the "cascading pipe" anti-pattern.

| Best Practice | Detection | Severity |
|---------------|-----------|----------|
| No service→service→service chains (3+ levels) | Service importing 3+ other services | HIGH |
| Each step is a sink (side-effect depth <= 1) | Side-effect markers in called functions (per `references/ai_ready_architecture.md`) | MEDIUM |

### Service Layer

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Single responsibility | Service class <300 lines, methods <30 lines | MEDIUM |
| Dependency injection | `@inject\|Depends\|constructor.*inject\|__init__.*repository` | HIGH |
| Transaction management | `transaction\|commit\|UnitOfWork\|@Transactional` | HIGH |
| DTO at boundaries | `Schema\|DTO\|DataTransfer\|Input\|Output` in method signatures | MEDIUM |
| No direct I/O | No `httpx\|requests\|open(` directly in service files | HIGH |

### Dependency Injection

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Container/provider setup | `Container\|Provider\|Module\|bind\|register` | HIGH |
| Interface binding | `bind.*to\|provide.*interface\|Protocol.*Depends` | HIGH |
| Scope management | `Scope\|Singleton\|Transient\|Request.*scope\|Scoped` | MEDIUM |
| No service locator | Should NOT see `container.get\|resolve(` outside composition root | MEDIUM |

### Job Processing

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Dead Letter Queue (DLQ) | `dlq\|dead.?letter\|failed.?queue\|on_failed\|failedJobsQueue` | HIGH |
| Exponential backoff | `backoff\|exponential\|backoffDelay\|retry_backoff` | HIGH |
| Idempotency keys | `idempoten\|dedup\|job.?id.*unique\|unique.?job` | MEDIUM |
| Job prioritization | `priority\|PRIORITY\|prioritize\|urgent` in queue config | LOW |
| Graceful shutdown | `SIGTERM\|SIGINT\|graceful.*shut\|beforeExit\|shutdown.*handler` | HIGH |
| Concurrency control | `concurrency\|maxWorkers\|worker.?limit\|limiter\|rate.?limit` | MEDIUM |
| Job timeout | `timeout\|jobTimeout\|time_limit\|TTL` in worker config | MEDIUM |
| Progress tracking | `progress\|onProgress\|job.?status\|update_state` | LOW |

### Event-Driven

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Event schema versioning | `version\|schema_version\|v[0-9].*event\|EventV[0-9]` | HIGH |
| Dead letter queue | `dlq\|dead.?letter\|unprocessed\|failed.?event` | HIGH |
| Correlation IDs | `correlation.?id\|trace.?id\|request.?id\|x-correlation` | MEDIUM |
| Idempotent handlers | `idempoten\|already.?processed\|dedup\|event.?id.*check` | HIGH |
| Ordering guarantees | `partition.?key\|ordering\|sequence\|ordered` | LOW |
| Schema validation | `schema.*valid\|validate.*event\|EventSchema\|zod\|pydantic` | MEDIUM |
| Replay capability | `replay\|reprocess\|re.?emit\|event.?store\|EventStore` | LOW |

### Caching

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Invalidation strategy | `invalidate\|evict\|delete.*cache\|bust.*cache\|on_update.*cache` | HIGH |
| Cache-aside pattern | `get.*cache.*miss.*fetch\|cache.?aside\|read.?through` | MEDIUM |
| Key naming conventions | `cache.?key\|key.?prefix\|namespace.*cache\|key.*template` | LOW |
| Stampede prevention | `lock\|mutex\|singleflight\|debounce.*cache\|cache.?lock` | MEDIUM |
| Distributed consistency | `pub.?sub.*invalidat\|broadcast.*cache\|cluster.*cache` | LOW |
| Fallback on miss | `fallback\|miss.*fetch\|cache.*miss.*return` | MEDIUM |
| Cache warming | `warm\|preload\|prefetch\|prime.*cache\|startup.*cache` | LOW |

### Resilience

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Circuit breaker states | `CircuitBreaker\|circuit.?breaker\|OPEN\|HALF_OPEN\|CLOSED` in resilience code | HIGH |
| Bulkhead isolation | `Bulkhead\|bulkhead\|semaphore\|concurrent.?limit\|isolation` | MEDIUM |
| Timeout per dependency | `timeout\|Timeout\|deadline\|time_limit` per external call | HIGH |
| Fallback responses | `fallback\|Fallback\|default.*response\|graceful.*degrade` | HIGH |
| Retry with jitter | `jitter\|random.*delay\|backoff.*jitter\|retry.*random` | MEDIUM |
| Health checks | `health.?check\|readiness\|liveness\|ping\|/health` | MEDIUM |
| Graceful degradation | `degrade\|feature.?flag\|circuit.*open.*return\|fallback.*default` | LOW |

### CQRS

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Command/Query separation | `Command\|Query\|CommandHandler\|QueryHandler` in separate dirs | HIGH |
| Eventually consistent reads | `eventual\|async.*project\|read.?model.*update` | MEDIUM |
| Projection updates | `Projection\|project\|materialize\|ReadModel.*update` | MEDIUM |
| Event-driven updates | `on.*Event\|EventHandler\|subscribe.*update` for projections | MEDIUM |
| Read model rebuild | `rebuild\|reproject\|replay.*read.?model\|migrate.*projection` | LOW |
| Separate data stores | `readDb\|writeDb\|read.*connection\|write.*connection` | LOW |

### Repository

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Unit of Work | `UnitOfWork\|unit.?of.?work\|commit\|SaveChanges\|flush` | HIGH |
| Specification pattern | `Specification\|specification\|criteria\|Criteria\|filter.*query` | LOW |
| Transaction management | `transaction\|Transaction\|begin\|commit\|rollback\|@Transactional` | HIGH |
| Pagination support | `paginate\|Pagination\|skip.*take\|offset.*limit\|cursor` | MEDIUM |
| Soft delete | `soft.?delete\|is_deleted\|deleted_at\|IsDeleted\|paranoid` | LOW |
| Audit logging | `audit\|created_at\|updated_at\|modified_by\|@Audit` | MEDIUM |

### Saga

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Compensation logic | `compensate\|rollback\|undo\|revert.*step` | HIGH |
| Step tracking | `step.*status\|saga.*state\|step.*complete` | HIGH |
| Timeout per step | `timeout\|step.*timeout\|deadline` in saga | MEDIUM |
| Idempotent steps | `idempoten\|already.*executed\|step.*id.*check` | MEDIUM |
| Failure isolation | `try.*step\|catch.*step\|on_step_failure` | HIGH |
| Distributed tracing | `correlation.?id\|trace.?id\|saga.?id` | LOW |

### API Gateway

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Rate limiting | `rate.?limit\|throttle\|RateLimit` | HIGH |
| Authentication | `auth\|token\|jwt\|Bearer\|middleware.*auth` | HIGH |
| Request validation | `validate\|schema\|Joi\|Zod\|pydantic` at gateway | MEDIUM |
| Circuit breaker for backends | `circuit.?breaker\|fallback\|retry` in gateway | MEDIUM |
| Request/response logging | `log.*request\|log.*response\|access.?log` | LOW |
| CORS configuration | `cors\|CORS\|Access-Control` | MEDIUM |

### Event Sourcing

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Event immutability | `frozen\|immutable\|readonly\|@dataclass.*frozen` on events | HIGH |
| Snapshot support | `snapshot\|Snapshot\|create_snapshot\|load_snapshot` | MEDIUM |
| Event versioning | `version\|event_version\|schema_version\|EventV[0-9]` | HIGH |
| Aggregate root | `AggregateRoot\|aggregate_root\|apply_event\|load_events` | HIGH |
| Projection rebuild | `rebuild\|reproject\|replay.*projection` | MEDIUM |
| Event store interface | `EventStore\|event_store\|append_events\|get_events` | HIGH |

### Message Queue

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Dead letter queue | `dlq\|dead.?letter\|rejected\|nack` | HIGH |
| Message acknowledgment | `ack\|acknowledge\|basic_ack\|commit_offsets` | HIGH |
| Serialization format | `serialize\|deserialize\|json\|avro\|protobuf` in queue | MEDIUM |
| Connection retry | `reconnect\|retry.*connect\|connection.*retry` | HIGH |
| Consumer groups | `consumer.?group\|group.?id\|ConsumerGroup` | MEDIUM |
| Message ordering | `partition\|ordering\|sequence\|fifo` | LOW |

### HTTP Client

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Connection pooling | `pool\|max_connections\|limits\|pool_connections` | HIGH |
| Timeout configuration | `timeout\|Timeout\|connect_timeout\|read_timeout` | HIGH |
| Retry logic | `retry\|Retry\|backoff\|retry_transport\|max_retries` | MEDIUM |
| Base URL configuration | `base_url\|BASE_URL\|api_url` from config/env | MEDIUM |
| Response error handling | `raise_for_status\|status_code.*!=\|check.*response` | HIGH |

### Rate Limiting

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Per-endpoint limits | `limit.*route\|@rate_limit\|@throttle\|per_endpoint` | MEDIUM |
| Backend storage | `Redis\|Memcached\|in_memory.*limit\|rate_limit.*store` | MEDIUM |
| Response headers | `X-RateLimit\|Retry-After\|rate.*header` | LOW |
| Graceful rejection | `429\|TooManyRequests\|rate.*exceeded\|throttled` | HIGH |

### Client Notification

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Retry on failure | `retry\|backoff\|max_attempts` for webhook/notification | HIGH |
| Delivery confirmation | `delivered\|acknowledged\|callback.*status\|delivery.*log` | MEDIUM |
| Authentication/signing | `hmac\|signature\|secret\|sign.*payload\|webhook.*secret` | HIGH |
| Rate limiting outgoing | `rate.?limit.*notify\|throttle.*callback\|batch.*notify` | LOW |

### Parameter Object

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Immutability | `frozen=True\|readonly\|Readonly\|immutable\|const` | HIGH |
| Validation | `validator\|@validate\|__post_init__\|validate` in dataclass | MEDIUM |
| Type safety | Typed fields (not `dict` or `Any`) | MEDIUM |
| Documentation | Docstring or comment on fields purpose | LOW |

### Fail-Fast Validation

| Best Practice | Detection Grep | Severity if Missing |
|---------------|----------------|---------------------|
| Validation at boundaries | `@validator\|field_validator\|@validate\|ValidationError` in API/service entry | HIGH |
| Custom error messages | `msg=\|message=\|detail=\|description=` in validator | MEDIUM |
| Schema reuse | Same schema used in API + service (not duplicated) | MEDIUM |
| Validation aggregation | `ValidationError.*errors\|collect.*errors\|all_errors` (report all, not fail on first) | LOW |

---

## Discovery Heuristics

Used by ln-640 Phase 1b to discover patterns NOT in the baseline table above.

### Structural Heuristics

| Heuristic | Detection | Inferred Pattern |
|-----------|-----------|-----------------|
| Class naming conventions | `Grep("class\s+\w*(Factory\|Builder\|Strategy\|Adapter\|Observer\|Decorator\|Proxy\|Mediator\|Command\|Visitor\|State\|Chain\|Facade)")` | GoF pattern matching class name suffix |
| Abstract hierarchy | Find ABC/abstract classes with 2+ concrete implementations in same directory | Template Method or Strategy |
| Fluent interface | `return self\|return this` chains in non-test code (3+ methods in same class) | Builder |
| Registration dict | `_registry\|_handlers\|_map\s*[=:]\s*\{` with `register(` method in same file | Registry |
| Middleware chain | `app.use(\|add_middleware(\|@app.middleware` | Chain of Responsibility |
| Event listeners | `@on_event\|addEventListener\|@receiver\|signal\|on_.*_event` | Observer |
| Decorator wrappers | `@wraps\|functools.wraps\|__wrapped__` in non-framework code | Decorator pattern |
| State machine | `state\|transition\|current_state\|StateMachine\|FSM` | State pattern |
| Pub/Sub | `subscriber\|publisher\|topic\|channel\|broadcast` outside message queue context | Observer / Mediator |

### Document-Based Heuristics

| Source | Detection | Inferred Pattern |
|--------|-----------|-----------------|
| ADR/Guide names | Scan `docs/reference/adrs/*.md`, `docs/reference/guides/*.md` filenames and H1 headers for pattern names not in library | Named patterns from project docs |
| Architecture.md | Grep for pattern terminology in project architecture docs | Architecture-level patterns |
| Code comments | `Grep("pattern:\|@pattern\|design pattern\|implements.*pattern")` | Developer-annotated patterns |
| README/docs | Grep for "pattern" + GoF names in project documentation | Documented but uncataloged patterns |

### Discovery Output

Each discovered pattern gets:
- `name`: inferred pattern name
- `evidence`: file paths + grep matches
- `confidence`: HIGH (naming + structure match) / MEDIUM (naming only) / LOW (structural heuristic only)
- `status`: "Discovered" in catalog (distinct from baseline "Undocumented")

---

## Pattern Recommendations

Used by ln-640 Phase 1c to suggest patterns that COULD improve architecture.

| Condition | Detection | Recommendation |
|-----------|-----------|---------------|
| External API calls without retry/timeout | `httpx\|requests\|fetch` found but no `retry\|CircuitBreaker\|timeout` nearby | Resilience (Circuit Breaker + Retry) |
| 3+ services with similar constructor params | `__init__\|constructor` with 4+ identical param names across services | Dependency Injection container |
| 5+ constructor params in any class | `def __init__.*,.*,.*,.*,.*,` | Builder or Parameter Object |
| Copy-paste validation across endpoints | Same `@validator\|Joi.object\|Zod.object` in 3+ files | Fail-Fast Validation with shared schemas |
| Multiple if/elif chains selecting handler | `if.*elif.*elif` or `switch.*case.*case.*case` (3+ branches) | Strategy + Registry |
| Direct DB access from API layer | `session\|query\|find\|select` in `**/api/**` or `**/controllers/**` | Repository pattern |
| No DLQ for job/queue processing | Job Processing detected but no `dlq\|dead.?letter` | Dead Letter Queue + Retry |
| No error centralization | `try.*except\|try.*catch` in 5+ files with same exception types | Error Handler / Middleware pattern |

---

## MCP Ref Search Queries

Use these queries with `ref_search_documentation`:

| Pattern | Search Query |
|---------|-------------|
| Singleton | "singleton pattern {tech_stack} thread safety testing" |
| Factory | "factory pattern {tech_stack} abstract factory registration" |
| Builder | "builder pattern {tech_stack} fluent interface validation" |
| Adapter | "adapter pattern {tech_stack} port interface dependency inversion" |
| Pipeline | "pipeline pattern {tech_stack} stage composition middleware" |
| Strategy | "strategy pattern {tech_stack} runtime selection handler" |
| Service Layer | "service layer pattern {tech_stack} transaction management" |
| Dependency Injection | "dependency injection {tech_stack} container provider binding" |
| Repository | "repository pattern {tech_stack} unit of work" |
| CQRS | "cqrs pattern {tech_stack} command query separation" |
| Job Processing | "job queue best practices {tech_stack} dead letter retry" |
| Event-Driven | "event driven architecture patterns {tech_stack} event sourcing" |
| Caching | "caching strategies {tech_stack} cache invalidation redis" |
| Resilience | "circuit breaker pattern {tech_stack} retry timeout" |
| Saga | "saga pattern {tech_stack} orchestration compensation" |
| API Gateway | "api gateway pattern {tech_stack} rate limiting authentication" |
| Event Sourcing | "event sourcing pattern {tech_stack} aggregate event store" |
| Message Queue | "message queue best practices {tech_stack} dead letter consumer" |
| HTTP Client | "http client best practices {tech_stack} connection pooling retry" |
| Rate Limiting | "rate limiting api {tech_stack} throttling strategies" |

## Context7 Libraries

| Pattern | Library to Query |
|---------|-----------------|
| Job Processing (Node.js) | bull, bullmq |
| Job Processing (Python) | celery |
| Event-Driven (Node.js) | eventemitter2, rxjs |
| Caching (Node.js) | ioredis, node-cache |
| Resilience (Node.js) | cockatiel, opossum |
| CQRS (.NET) | mediatr |
| Dependency Injection (Python) | dependency-injector |
| Dependency Injection (Node.js) | tsyringe, inversify |
| Dependency Injection (.NET) | microsoft.extensions.dependencyinjection |
| HTTP Client (Python) | httpx |
| HTTP Client (Node.js) | axios, got |
| Rate Limiting (Python) | slowapi |
| Rate Limiting (Node.js) | express-rate-limit |
| Message Queue (Node.js) | amqplib |
| Message Queue (Python) | pika, aiokafka |
| Pipeline (Python) | luigi, prefect |
| Saga (Node.js) | saga-orchestrator |
| Validation (Python) | pydantic |
| Validation (Node.js) | zod, joi |

---
**Version:** 2.0.0
