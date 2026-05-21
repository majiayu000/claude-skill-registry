# Bottleneck Classification Taxonomy

<!-- SCOPE: Detailed classification of performance bottleneck types with code-level indicators per language/framework. -->
<!-- DO NOT add here: profiling workflow -> ln-811 SKILL.md; optimization strategies -> ln-812 SKILL.md -->

Systematic taxonomy for classifying bottlenecks discovered during request path tracing.

---

## Classification Types

### CPU-Bound

**Definition:** Processing time dominated by computation, not waiting for external resources.

| Indicator | Language Examples |
|-----------|-----------------|
| Tight loops without I/O | `for`, `while`, list comprehensions, `Array.map` |
| Sorting / searching | `sorted()`, `Array.sort()`, `Collections.sort()` |
| Regex compilation/matching | `re.compile()`, `new RegExp()`, `Regex.Match()` |
| Cryptographic operations | `hashlib`, `bcrypt`, `crypto.createHash()` |
| Serialization / deserialization | `JSON.parse/stringify`, `pickle`, `Marshal` |
| String processing | Template rendering, XML/HTML parsing |
| Image / media processing | PIL, sharp, ImageMagick calls |

**Typical latency:** < 10ms per operation (unless algorithmic complexity issue).

### I/O-DB (Database)

| Indicator | Language Examples |
|-----------|-----------------|
| ORM queries | `session.query()`, `Model.objects.filter()`, `db.Where()` |
| Raw SQL | `cursor.execute()`, `pool.query()`, `Dapper.Query()` |
| Transaction blocks | `BEGIN/COMMIT`, `session.begin()`, `TransactionScope` |
| Migration / schema ops | `ALTER TABLE`, `CREATE INDEX` |

**Patterns to flag:**
- N+1: Query inside loop iterating over parent results
- Missing index: Full table scan on large table
- Over-fetching: `SELECT *` when few columns needed
- Unbounded: No `LIMIT` / `.Take()` on user-facing query

**Typical latency:** 1-10ms (indexed), 10-1000ms (scan), 1-50ms (N+1 per iteration).

### I/O-Network (HTTP/gRPC)

| Indicator | Language Examples |
|-----------|-----------------|
| HTTP client calls | `requests.get/post()`, `httpx.get()`, `fetch()`, `axios.*`, `HttpClient.*` |
| gRPC stubs | `stub.Method()`, `client.Call()` |
| WebSocket send | `ws.send()`, `socket.emit()` |
| SMTP | `smtplib.send_message()`, `nodemailer.sendMail()` |
| Message queues | `channel.basic_publish()`, `producer.send()` |

**Patterns to flag:**
- Sequential calls in loop (N+1 HTTP)
- Missing batch API usage (batch endpoint exists but not used)
- No connection pooling
- No timeout configuration

**Typical latency:** 1-50ms (internal/localhost), 100-700ms (external API), 1-10s (slow external).

### I/O-File

| Indicator | Language Examples |
|-----------|-----------------|
| File read/write | `open()`, `fs.readFile()`, `File.ReadAllText()` |
| File streams | `io.BufferedReader`, `fs.createReadStream()` |
| Temp file creation | `tempfile.*`, `os.tmpdir()` |
| Directory listing | `os.listdir()`, `fs.readdir()`, `glob()` |

**Typical latency:** 1-10ms (small file), 10-100ms (large file), 100ms+ (many files).

### Architecture

**Definition:** Bottleneck caused by code structure, not individual operation speed.

| Pattern | Description | How to Detect |
|---------|-------------|---------------|
| N+1 I/O | Loop containing any I/O call (DB, HTTP, file) | Loop body contains I/O indicator from other categories |
| Sequential-when-parallel | Independent I/O calls executed sequentially | Multiple I/O calls with no data dependency between them |
| Missing cache | Same expensive operation called repeatedly with same input | Identical function call in multiple code paths |
| Missing batch | API supports batch but called per-item | Batch method exists on client but loop calls single-item method |
| Redundant computation | Same computation performed multiple times | Same function called with same args in different places |

### External

**Definition:** Latency determined by third-party service, not under our control.

| Indicator | How to Confirm |
|-----------|---------------|
| Third-party API call | Domain is not internal (no localhost, no internal DNS) |
| No batch alternative | Service API docs show no batch endpoint |
| No caching possible | Results are non-deterministic or time-sensitive |
| SLA-bound | Service has known latency SLA (e.g., "p99 < 2s") |

**"Wrong tool" signal:** If 90%+ of total time is External with no optimization path.

---

## Classification Decision Tree

```
Is the slow step doing I/O?
├── NO → CPU-bound
└── YES → What kind of I/O?
    ├── Database → I/O-DB
    ├── HTTP/gRPC/messaging → I/O-Network
    ├── File system → I/O-File
    └── Any I/O inside a loop?
        ├── YES → Architecture (N+1 pattern)
        └── NO → Is it external (third-party)?
            ├── YES → External
            └── NO → Check for missing batch/cache/parallelism
                ├── Found → Architecture
                └── Not found → I/O-{subtype}
```

---

## Multi-Bottleneck Prioritization

When multiple bottlenecks exist, prioritize by time share:

| Time Share | Priority |
|------------|----------|
| > 50% | PRIMARY — optimize first |
| 20-50% | SECONDARY — optimize after primary |
| < 20% | TERTIARY — defer unless easy win |

**Pareto rule:** Typically 80% of latency comes from 20% of steps. Focus on top 1-3 bottlenecks.

---

**Version:** 1.0.0
**Last Updated:** 2026-03-14
