---
name: jskim
description: Token-saving Java file reader. Use when working with Java files (.java) to reduce token usage. Auto-triggers when exploring, reading, or understanding Java classes, services, controllers, entities, or any .java files. Run jskim before using the Read tool on Java files to understand structure first, then Read only the lines you need.
argument-hint: [file-path or src-directory]
allowed-tools: Bash(jskim:*)
---

# jskim — Java Token Saver for Spring Boot

A CLI tool that summarizes Java files compactly, saving 70-80% of input tokens. Optimized for Spring Boot projects with Lombok, REST controllers, DI wiring, and configuration properties.

## Requirements

Python 3.10+ — install via pip:
```bash
pip install jskim
```

**Before first use**, verify jskim is installed by running `jskim --version`. If you get "command not found", tell the user:
> jskim is not installed. Install it with: `pip install jskim`

Do not attempt to run jskim commands until it is confirmed installed. Fall back to the `Read` tool if the user declines to install it.

## Usage

`jskim` auto-detects whether you're pointing at a file or directory, and whether you're asking for a summary or method extraction.

### Single file summary
Summarizes a Java file — collapses imports, fields, boilerplate (getters/setters/equals/hashCode), and shows method signatures with line ranges. Shows annotation parameters for key Spring annotations (`@GetMapping("/path")`, `@Value("${key}")`, `@ConfigurationProperties("prefix")`, etc.).

```bash
jskim <file.java>
jskim <file.java> --grep <pattern>       # filter methods by name/signature
jskim <file.java> --annotation <@Ann>    # filter methods by annotation
jskim A.java B.java C.java               # multiple files
```

**Filters** (useful for large files with many methods):
- `--grep billing` — show only methods whose signature contains "billing" (case-insensitive)
- `--annotation @Transactional` — show only methods with that annotation
- Filters apply to the method listing only. Header, fields, and inner types are always shown.
- Filters can be combined: `--grep create --annotation @PostMapping`

### Project map
Generates a compact map of all Java files in a directory — packages, classes, annotations, field/method counts, Lombok usage, enum constants.

```bash
jskim <src_dir>
jskim <src_dir> --deps                          # import-based dependencies
jskim <src_dir> --endpoints                     # REST endpoint map
jskim <src_dir> --beans                         # Spring bean DI graph + @Bean producers + config properties
jskim <src_dir> --package <prefix>               # filter by package
jskim <src_dir> --annotation <@Ann>              # filter by class annotation
jskim <src_dir> --extends <ClassName>            # filter by superclass
jskim <src_dir> --implements <Interface>        # filter by implemented interface
```

**Filters** (essential for large projects with hundreds of files):
- `--package com.stw.server.tripsheet` — only show classes in that package (prefix match)
- `--annotation @RestController` — only show classes with that annotation
- `--extends BaseService` — only show classes extending that superclass
- `--implements EventPublisher` — only show classes implementing that interface
- `--deps` — show which classes depend on which (uses imports, runs in seconds even on 2000+ files)
- `--endpoints` — list all REST endpoints: HTTP method, path, handler method, line number
- `--beans` — show Spring bean DI graph, `@Bean` factory method producers, and `@ConfigurationProperties` with field details
- Filters can be combined: `--package com.example --annotation @Service --deps --endpoints --beans`

### Diff mode
Summarizes only the Java files and methods changed in a git diff. Ideal for PR reviews — instead of reading full files, get structural context for just the changed parts.

```bash
jskim --diff HEAD~1                    # changes since last commit
jskim --diff main                      # changes vs main branch
jskim --diff main...feature-branch     # merge-base comparison
jskim src/ --diff HEAD~1               # scoped to directory
git diff main | jskim --diff -         # read diff from stdin
```

**Output markers**:
- `[NEW]` — file or method that was added
- `[MODIFIED]` — method whose body was changed
- `[DELETED]` — file or method that was removed
- `→` calls shown for new/modified methods (same format as file summary)
- Getters, setters, and boilerplate changes are suppressed (not interesting)
- Unchanged methods are counted but not listed

### Method extraction
Extracts method source code with context (fields, called methods, annotations, Javadoc).

```bash
jskim <file.java> --list                         # list all methods
jskim <file.java> <method_name>                   # extract one method
jskim <file.java> <method1> <method2> <method3>   # extract multiple
```

**Multiple methods** — pass all names in one call instead of running the script multiple times. This is useful when you need a method and the methods it calls:
- Deduplicates results automatically
- Reports any names that weren't found: `// not found: methodX`
- Shows "called methods in same class" across all extracted methods

## Reading the output

### File summary output format

```
// path/to/File.java
// com.example.billing | 12 imports: java.util(3), jakarta.persistence(2), ...
// lombok: @Data: getters, setters, toString, equals, hashCode
// @RestController @RequestMapping("/api/v1/billing")
// public class BillingController extends BaseController
//
// fields:
//   BillingRepository billingRepo (@Autowired)
//   BillingValidator validator
//   AuditLogger auditLogger
//   String tenantId
//
// getters: getName, getStatus              <- collapsed, names only
// setters: setName, setStatus              <- collapsed, names only
// boilerplate: toString, hashCode, equals  <- collapsed, names only
// methods:
//     L18-L21 (  4 lines): public BillingController(BillingService svc, BillingValidator v)
//     L45-L62 ( 18 lines): @PostMapping public Bill createBill(BillDTO dto)
//                → auditLogger.log, billingService.create, notifyStakeholders, validator.validate
//     L64-L80 ( 17 lines): @GetMapping("/{id}") public Bill getBill(Long id)
//                → billingService.findById
//     L82-L95 ( 14 lines): @PutMapping("/{id}") public Bill updateBill(Long id, BillDTO dto)
//                → auditLogger.log, billingService.findById, billingService.update, validator.validate
//
// inner types:
//   L90: public static enum Status
//
// other classes in file:
//   L100: class BillingHelper [2F, 3M]     <- 2F = 2 fields, 3M = 3 methods
//
// total: 120 lines
```

For enums:
```
// public enum BillStatus
//
// constants: DRAFT, PENDING, APPROVED, REJECTED
//
// fields:
//   String label
```

- `L45-L62` = line range in the file (use with `Read` offset/limit)
- `( 18 lines)` = method body length
- `→` = method calls — lists direct method invocations made by this method (sorted alphabetically)
  - **Noise is auto-filtered**: collection ops (`put`, `get`, `add`, `remove`, `stream`, `collect`), utility checks (`Objects.equals`, `StringUtils.isBlank`, `MapUtils.isEmpty`), logging (`log.info`, `logger.debug`), type conversions (`toString`, `valueOf`), and stream plumbing (`map`, `filter`, `forEach`) are excluded
  - Chained/fluent calls (streams, builders) are excluded — only the root call on a simple object is shown
  - Calls are capped at 10 per method; overflow shown as `... +N more`
  - Abstract methods and methods with no calls have no `→` line
- Spring annotation parameters are preserved: `@GetMapping("/{id}")`, `@Value("${config.key}")`
- getters/setters/boilerplate are collapsed to names only — no line ranges, no calls, not worth reading
- `NF` = N fields, `NM` = N methods (used for inner/extra types)
- Enum constants are listed inline
- Static initializer blocks shown with line ranges: `// static initializer (L10-L25, 16 lines)`

### Interpreting `→` method calls

The `→` line shows business-logic calls only — boilerplate noise (collection ops, logging, utility checks, stream plumbing, type conversions) is automatically filtered out. What remains is high-signal:

**Dependency calls (match a field in `fields:`):**
- `billingService.create` → field `BillingService billingService` exists → injected dependency call. **Follow this.**
- `validator.validate` → field `BillingValidator validator` exists → dependency call. **Follow this.**

**Same-class calls (no dot prefix):**
- `notifyStakeholders` → unqualified name → private/inherited method in the same class. Use `jskim File.java notifyStakeholders` to read it.

**Accessor calls on parameters/locals (do NOT match any field):**
- `dto.getName`, `order.getId` → getter calls on method parameters or local variables. Usually not worth tracing.

**Rule of thumb:** If the object name before the dot matches a field name in the `fields:` section, it's a dependency call worth following. If it doesn't match any field, it's likely an accessor on a parameter or local — lower priority for tracing.

### Project map output format

```
// Project Map: 42 files, 8500 lines
//
// com.example.billing (5 files, 600 lines)
//   class BillingService @Service [3F | 8M | 120L | lombok:Data]
//   class BillingRepository @Repository [0F | 5M | 45L]
//   class BillDTO @Data [7F | 0M | 30L | lombok:Data,Builder]
//   enum BillStatus { DRAFT, PENDING, APPROVED, REJECTED } [0F | 0M | 15L]
//   interface BillingPort [0F | 3M | 20L]
```

With `--endpoints`:
```
// === REST Endpoints ===
//   GET     /api/v1/billing         BillingController.list()      L45
//   POST    /api/v1/billing         BillingController.create()    L62
//   GET     /api/v1/billing/{id}    BillingController.get()       L70
//   PUT     /api/v1/billing/{id}    BillingController.update()    L80
//   DELETE  /api/v1/billing/{id}    BillingController.delete()    L90
```

With `--beans`:
```
// === Bean Dependencies ===
//   BillingService @Service <- BillingRepository, BillValidator, KafkaTemplate
//   BillingController @RestController <- BillingService, AuthService
//
// === Bean Producers (@Bean) ===
//   AppConfig @Configuration -> ObjectMapper, TaskScheduler, NotificationClient
//
// === Configuration Properties ===
//   billing.* (BillingProperties): BigDecimal taxRate, String currency, int maxRetries
```

With `--deps`:
```
// === Dependencies ===
//   BillingService -> BillingRepository, BillDTO, BillingPort
```

- `NF` = N fields, `NM` = N methods, `NL` = N lines in file
- `lombok:Data,Builder` = Lombok annotations present on the class
- `inner:Foo,Bar` = inner classes/enums inside this class
- Enum constants shown inline: `enum Status { ACTIVE, INACTIVE }`
- Dependencies (`--deps`) = import-based class references
- Endpoints (`--endpoints`) = all `@GetMapping`/`@PostMapping`/etc. with full paths
- Beans (`--beans`) = DI wiring, `@Bean` factory method producers, and `@ConfigurationProperties`

### Method extraction output format

**With `--list`:**
```
// public class BillingService extends BaseService
//
//     L45-L62 ( 18 lines): @PostMapping public Bill createBill(BillDTO dto)
//     L64-L80 ( 17 lines): public void processBill(Long id)
```

**With method names:**
```
// public class BillingService extends BaseService
// fields: BillingRepository billingRepo, String tenantId
//
// @PostMapping public Bill createBill(BillDTO dto) (L45-L62)
//
//   45 |     @PostMapping
//   46 |     public Bill createBill(BillDTO dto) {
//        ...full method source with line numbers...
//   62 |     }
//
// --- called methods in same class ---
//   L64-L80: public void processBill(Long id)
```

- Shows full method source with line numbers
- `fields:` lists class fields for context
- `called methods in same class` shows other methods referenced in the extracted method bodies
- `// not found: methodX` appears if a requested method name wasn't found

## Workflow

Follow this order to minimize tokens:

1. **Explore** -> `jskim src/` to understand project structure
2. **Narrow** -> `jskim src/ --package com.example.billing` to focus on relevant package
3. **Spring context** -> `jskim src/ --endpoints --beans` to see REST API + DI wiring
4. **Understand** -> `jskim File.java` to see class structure (fields, methods, line ranges, and method calls)
5. **Trace** -> Use `→` calls to follow execution: match `fieldName.method` against `fields:` to find the target class type, then skim that class to continue
6. **Filter** -> `jskim File.java --grep billing` if the class has many methods
7. **Focus** -> `jskim File.java methodA methodB` to read the methods you need
8. **Edit** -> Use `Read` with `offset`/`limit` on only the lines that matter, then `Edit` normally

### Tracing call flow across files (step-by-step example)

**Goal:** Understand what happens when `POST /api/v1/billing` is called.

```
Step 1: jskim BillingController.java
        → See: createBill() calls billingService.create, validator.validate
        → See fields: BillingService billingService, BillingValidator validator

Step 2: jskim BillingService.java
        → See: create() calls billingRepo.save, eventPublisher.publish, calculateTax
        → See fields: BillingRepository billingRepo, EventPublisher eventPublisher

Step 3: jskim BillingService.java calculateTax
        → Read the method source to understand the tax logic

Done — you traced Controller → Service → Repository in 3 tool calls,
reading ~50 lines of skim output instead of ~500 lines of raw Java.
```

### Finding callers (reverse lookup)

The `→` calls show what a method calls (downstream). To find what calls a method (upstream), combine `Grep` with `jskim`:

```
Goal: Who calls billingService.create()?

Step 1: Grep for "\.create(" across *.java files → find calling files
Step 2: jskim each calling file → see which methods contain the call and their full context
```

For finding all usages of a method within the same project:
- `jskim src/ --grep create` — scans all files but only shows methods matching "create"
- `Grep "create(" --glob "*.java"` — finds raw references, then skim the files to understand context

### When to use each tool

| Situation | Tool |
|---|---|
| PR review / what changed? (large diff, 1000+ lines) | `jskim --diff develop` to triage, then `git diff` for details |
| PR review / what changed? (small diff, < 1000 lines) | `git diff develop...HEAD` directly — skip jskim |
| New project, need orientation | `jskim src/` |
| Find all REST controllers | `jskim src/ --annotation @RestController` |
| See all API endpoints at a glance | `jskim src/ --endpoints` |
| See Spring bean DI wiring + producers | `jskim src/ --beans` |
| Find all classes extending BaseService | `jskim src/ --extends BaseService` |
| Find all implementations of an interface | `jskim src/ --implements EventPublisher` |
| Understand a class structure | `jskim File.java` |
| Trace call flow downstream | Skim the class → follow `→` field calls → skim the dependency class |
| Find callers (upstream) | `Grep "methodName("` across `*.java` → skim calling files |
| Assess impact of a change | Combine downstream (`→`) + upstream (`Grep`) to see full blast radius |
| Large class (500+ lines), looking for specific methods | `jskim File.java --grep keyword` |
| Need to read a method's source code | `jskim File.java methodName` |
| Need method + related methods together | `jskim File.java method1 method2 method3` |

### When to use `jskim --diff` vs `git diff`

`jskim --diff` gives **structural context** — which methods were added, modified, or deleted, with signatures and call graphs. `git diff` gives the **actual code changes**. They serve different purposes:

**Use `jskim --diff` when:**
- The diff is large (1000+ lines, 10+ files) and you need to triage what changed before diving in
- Changed files are large (300+ lines each) — skim tells you which methods were affected without reading entire files
- You need to understand the shape/scope of changes across many files before reviewing details
- You want to identify which modified methods call what, to assess blast radius

**Use `git diff` directly (skip `jskim --diff`) when:**
- The diff is small (< ~1000 lines total) — you can read the entire diff faster than running jskim and then reading the diff anyway
- All changed files are small (< 150 lines each) — the skim output is roughly the same size as the raw diff, so it saves nothing
- You've already read the full `git diff` — running jskim after is redundant
- You need to review actual code logic, not just structure — jskim shows signatures and call graphs, not the changed lines themselves. For bug hunting and code review, you still need the real diff

**Key insight:** `jskim --diff` is a **triage tool**, not a replacement for reading the diff. Use it first on large diffs to decide where to focus, then read the actual changes with `git diff` or `Read`. On small diffs, skip it entirely and go straight to `git diff`.

### When NOT to use jskim

- **Small files (<100 lines)** — just use `Read` directly, skim overhead isn't worth it
- **Small diffs (< ~1000 lines)** — `git diff` is faster and gives you more useful information than `jskim --diff`
- **You already have line numbers** — if `Grep` already told you the exact lines, use `Read` with offset/limit directly. Don't waste a tool call on jskim.
- **You already read the full diff** — don't run `jskim --diff` after reading `git diff`; the structural info is already in context
- **Generated code** — JOOQ output, Protobuf stubs, Swagger-generated clients. These are mechanical and don't benefit from summarization.
- **Non-Java files** — this tool only handles `.java` files
- **The user asked to read the full file** — respect the request, use `Read`

### Rules
- Run `jskim` before using the `Read` tool on a Java file when you don't already know where to look (no line numbers from grep, no prior context). Skip jskim if you already have the line range you need.
- Use the line ranges from skim output to `Read` with `offset` and `limit` — never read the whole file when you only need one method
- When exploring a new Java project, start with `jskim <src_dir>` to understand the structure
- For large projects (500+ files), use `--package` to scope project map output
- For large classes (300+ lines, many methods), use `--grep` or `--annotation` to filter output
- For editing: use the `Read` tool with offset/limit to get the exact lines, then `Edit` normally — skim is for understanding, not for editing
- When you need multiple related methods, extract them all in one `jskim File.java method1 method2` call
- When tracing call flow, check the `→` calls against the `fields:` section to identify dependency calls vs parameter accessor noise

## Fallback — if jskim crashes

If `jskim` fails (syntax error, unexpected Java construct, Python not found, etc.), **do not stop or ask the user to fix it**. Fall back to your native tools:

1. Use the `Read` tool to read the Java file directly
2. Produce a similar compact summary yourself — list the package, key annotations, fields (type + name), and method signatures with line ranges
3. Continue with the workflow as normal

The goal is always: understand the Java file's structure with minimal tokens. jskim is the fast path, but you can always do it yourself if it breaks.

## What $ARGUMENTS is for

If the user invokes `/jskim` with arguments:
- If argument is a `.java` file -> run `jskim $ARGUMENTS`
- If argument is a directory -> run `jskim $ARGUMENTS`
- If argument is `<file.java> <method>` -> run `jskim $ARGUMENTS`
- If no arguments -> explain the available tools
