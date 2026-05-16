---
name: mirai
description: Help users write correct R code for async, parallel, and distributed computing using mirai. Use when users need to run R code asynchronously or in parallel, write mirai code with correct dependency passing, set up parallel workers, convert from future or parallel, use mirai_map, integrate with Shiny or promises, or configure cluster/HPC computing.
metadata:
  author: Charlie Gao (@shikokuchuo)
  version: "1.2"
license: MIT
---

mirai is a minimalist R framework for async, parallel, and distributed evaluation, built on nanonext.

## Core Principle: Explicit Dependency Passing

mirai evaluates expressions in a **clean environment** on a daemon process. Nothing from the calling environment is available unless passed explicitly — this is the #1 source of mistakes.

```r
# WRONG: my_data and my_func are not available on the daemon
m <- mirai(my_func(my_data))
```

There are two ways to pass objects, and the names used **must match** the names referenced in the expression.

### `.args` (recommended)

Objects in `.args` populate the expression's **local evaluation environment** — available directly by name inside the expression.

```r
m <- mirai(my_func(my_data), .args = list(my_func = my_func, my_data = my_data))
```

### `...` (dot-dot-dot)

Objects passed via `...` are assigned to the **daemon's global environment**. Use this when objects need to be found by R's standard scoping rules (e.g., helper functions called by other functions).

```r
m <- mirai(my_func(my_data), my_func = my_func, my_data = my_data)
```

### Shortcut: pass the whole calling environment

```r
# .args form — populates local eval env
process <- function(x, y) mirai(x + y, .args = environment())

# ... form — single unnamed environment, populates daemon global env
df_matrix <- function(x, y) mirai(as.matrix(rbind(x, y)), environment())
```

### When to use which

| Scenario | Use |
|----------|-----|
| Data and simple functions | `.args` |
| Helper functions called by other functions that need lexical scoping | `...` |
| Pass entire local scope to local eval env | `.args = environment()` |
| Pass entire local scope to daemon global env | `mirai(expr, environment())` |
| Large objects shared across many tasks | `everywhere()` first, then reference by name |

## Common Mistakes

### Unqualified package functions

Daemons start with no user packages loaded. Same applies inside `mirai_map()` callbacks.

```r
# WRONG: dplyr is not loaded on the daemon
m <- mirai(filter(df, x > 5), .args = list(df = my_df))

# CORRECT: namespace-qualify
m <- mirai(dplyr::filter(df, x > 5), .args = list(df = my_df))

# CORRECT: load inside the expression
m <- mirai({
  library(dplyr)
  filter(df, x > 5)
}, .args = list(df = my_df))

# CORRECT: pre-load on all daemons
everywhere(library(dplyr))
m <- mirai(filter(df, x > 5), .args = list(df = my_df))
```

### Expecting results immediately

`m$data` accesses the value but may still be unresolved. Use `m[]` (or `collect_mirai(m)`) to block until done; use `unresolved(m)` for a non-blocking check.

```r
m <- mirai(slow_computation())
result <- m[]                          # blocks until resolved
if (!unresolved(m)) result <- m$data   # non-blocking
```

## Setting Up Daemons

### No daemons required

`mirai()` works without calling `daemons()` first — it launches a transient background process per call. Setting up daemons is only needed for persistent pools of workers.

### Local daemons

```r
# Start 4 local daemon processes (with dispatcher, the default)
daemons(4)

# Direct connection (no dispatcher) — lower overhead, round-robin scheduling
daemons(4, dispatcher = FALSE)

# Concise programmatic statistics (vs. the richer status())
info()

# Reset (daemons otherwise persist for the session)
daemons(0)
```

### Scoped daemons (auto-cleanup)

`with(daemons(...), {...})` **creates** daemons and automatically cleans them up when the block exits.

```r
with(daemons(4), {
  m <- mirai(expensive_task())
  m[]
})
```

### Scoped compute profile switching

`local_daemons()` and `with_daemons()` **switch** the active compute profile to one that already exists — they do not create daemons.

```r
daemons(4, .compute = "workers")

# Switch active profile for the duration of the calling function
my_func <- function() {
  local_daemons("workers")
  mirai(task())[]  # uses "workers" profile
}

# Switch active profile for a block
with_daemons("workers", {
  m <- mirai(task())
  m[]
})
```

### Compute profiles (multiple independent pools)

```r
daemons(4, .compute = "cpu")
daemons(2, .compute = "gpu")

m1 <- mirai(cpu_work(), .compute = "cpu")
m2 <- mirai(gpu_work(), .compute = "gpu")
```

## Memory Backpressure (`memory` + `try_mirai()`)

For high-throughput producers (Shiny, promises, ingest pipelines), use the `memory` argument to `daemons()` to cap the queued task payload at dispatcher (MB, metric). Pair it with `try_mirai()` so the host R thread never blocks on submission.

```r
# 100 MB queue cap. mirai() blocks on submission once the queue is full.
daemons(4, memory = 100)

# try_mirai() returns NULL (invisibly) instead of blocking when the cap is hit.
m <- try_mirai(work(x), .args = list(x = x))
if (is.null(m)) {
  # backpressure: drop, retry later, or signal upstream
} else {
  # m is a regular mirai
}

# Inspect current and peak queue usage
status()$memory
```

`memory` requires dispatcher. Without dispatcher (or with `memory = NULL`), `try_mirai()` always returns a mirai.

## mirai_map: Parallel Map

Requires daemons to be set. Maps `.x` element-wise over a function, distributing across daemons. Namespace-qualify any package functions used inside the callback (see Mistake 2).

```r
daemons(4)

# Basic map — collect with []
results <- mirai_map(1:10, function(x) x^2)[]

# Constants via .args, helpers via ... (same passing rules as mirai())
results <- mirai_map(
  data_list,
  function(x, power) helper(x, power),
  .args = list(power = 3),
  helper = my_helper_func
)[]

# Flatten results to a vector
results <- mirai_map(1:10, sqrt)[.flat]

# Progress bar (requires cli package)
results <- mirai_map(1:100, slow_task)[.progress]

# Early stopping on error
results <- mirai_map(1:100, risky_task)[.stop]

# Combine options
results <- mirai_map(1:100, task)[.stop, .progress]
```

### Mapping over multiple arguments (data frame rows)

```r
# Each row becomes arguments to the function
params <- data.frame(mean = 1:5, sd = c(0.1, 0.5, 1, 2, 5))
results <- mirai_map(params, function(mean, sd) rnorm(100, mean, sd))[]
```

### Process as completed (`race_mirai`)

`race_mirai()` returns the integer index of the first resolved mirai in a list (or `0L` if empty). Useful when you want to handle results in completion order rather than submission order.

```r
remaining <- mirai_map(jobs, run)
while (length(remaining) > 0) {
  idx <- race_mirai(remaining)
  process(remaining[[idx]]$data)
  remaining <- remaining[-idx]
}
```

## everywhere: Pre-load State on All Daemons

```r
daemons(4)

# Load packages on all daemons
everywhere(library(DBI))

# Set up persistent connections
everywhere(con <<- dbConnect(RSQLite::SQLite(), db_path), db_path = tempfile())

# Export objects to daemon global environment via ...
# The empty {} expression is intentional — the point is to export objects via ...
everywhere({}, api_key = my_key, config = my_config)

# .min = N forces a synchronization point: the call must complete on at least
# N daemons before subsequent mirai evaluations proceed. Useful when launching
# remote daemons that connect over time.
everywhere(library(arrow), .min = 4)
```

## Error Handling

```r
m <- mirai(stop("something went wrong"))
m[]

is_mirai_error(m$data)       # TRUE for execution errors
is_mirai_interrupt(m$data)   # TRUE for cancelled tasks
is_error_value(m$data)       # TRUE for any error/interrupt/timeout

m$data$message               # Error message
m$data$stack.trace           # Full stack trace
m$data$condition.class       # Original error classes

# Timeouts (requires dispatcher)
m <- mirai(Sys.sleep(60), .timeout = 5000)  # 5-second timeout

# Cancellation (requires dispatcher)
m <- mirai(long_running_task())
stop_mirai(m)
```

## Shiny / Promises Integration

### ExtendedTask pattern

```r
library(shiny)
library(bslib)
library(mirai)

daemons(4)
onStop(function() daemons(0))

ui <- page_fluid(
  input_task_button("run", "Run Analysis"),
  plotOutput("result")
)

server <- function(input, output, session) {
  task <- ExtendedTask$new(
    function(n) mirai(rnorm(n), .args = list(n = n))
  ) |> bind_task_button("run")

  observeEvent(input$run, task$invoke(input$n))
  output$result <- renderPlot(hist(task$result()))
}
```

For high-traffic apps, set `daemons(4, memory = ...)` and submit with `try_mirai()` to apply backpressure without stalling the Shiny event loop.

### Promise piping

```r
library(promises)
mirai({Sys.sleep(1); "done"}) %...>% cat()
```

## Remote / Distributed Computing

### SSH (direct connection)

```r
daemons(
  url = host_url(tls = TRUE),
  remote = ssh_config(c("ssh://user@node1", "ssh://user@node2"))
)
```

### SSH (tunnelled, for firewalled environments)

```r
daemons(
  n = 4,
  url = local_url(tcp = TRUE),
  remote = ssh_config("ssh://user@node1", tunnel = TRUE)
)
```

### HPC cluster (Slurm/SGE/PBS/LSF)

```r
daemons(
  n = 1,
  url = host_url(),
  remote = cluster_config(
    command = "sbatch",
    options = "#SBATCH --job-name=mirai\n#SBATCH --mem=8G\n#SBATCH --array=1-50",
    rscript = file.path(R.home("bin"), "Rscript")
  )
)
```

### HTTP launcher (e.g., Posit Workbench)

```r
daemons(n = 2, url = host_url(), remote = http_config())
```

## Converting from future

| future | mirai |
|--------|-------|
| Auto-detects globals | Must pass all dependencies explicitly |
| `future({expr})` | `mirai({expr}, .args = list(...))` |
| `value(f)` | `m[]` or `collect_mirai(m)` |
| `plan(multisession, workers = 4)` | `daemons(4)` |
| `plan(sequential)` / reset | `daemons(0)` |
| `future_lapply(X, FUN)` | `mirai_map(X, FUN)[]` |
| `future_map(X, FUN)` (furrr) | `mirai_map(X, FUN)[]` |
| `future_promise(expr)` | `mirai(expr, ...)` (auto-converts to promise) |

The key conversion step: identify all objects the expression uses from the calling environment and pass them explicitly via `.args` or `...`.

## Converting from parallel

| parallel | mirai |
|----------|-------|
| `makeCluster(4)` | `daemons(4)` or `make_cluster(4)` |
| `clusterExport(cl, "x")` | Pass via `.args` / `...`, or use `everywhere()` |
| `clusterEvalQ(cl, library(pkg))` | `everywhere(library(pkg))` |
| `parLapply(cl, X, FUN)` | `mirai_map(X, FUN)[]` |
| `parSapply(cl, X, FUN)` | `mirai_map(X, FUN)[.flat]` |
| `mclapply(X, FUN, mc.cores = 4)` | `daemons(4); mirai_map(X, FUN)[]` |
| `stopCluster(cl)` | `daemons(0)` |

### Drop-in replacement via make_cluster

For code that already uses the parallel package extensively, `make_cluster()` provides a drop-in backend:

```r
cl <- mirai::make_cluster(4)
parallel::parLapply(cl, 1:100, my_func)
mirai::stop_cluster(cl)

# R >= 4.5: native integration
cl <- parallel::makeCluster(4, type = "MIRAI")
```

## Random Number Generation

```r
# Default: L'Ecuyer-CMRG stream per daemon (statistically safe, non-reproducible)
daemons(4)

# Reproducible: L'Ecuyer-CMRG stream per mirai call.
# Results are the same regardless of daemon count or scheduling.
daemons(4, seed = 42)
```

## Debugging

```r
# Synchronous mode — runs in the host process, supports browser()
daemons(sync = TRUE)
m <- mirai({
  browser()
  result <- tricky_function(x)
  result
}, .args = list(tricky_function = tricky_function, x = my_x))
daemons(0)

# Capture daemon stdout/stderr
daemons(4, output = TRUE)
```

## Advanced Pattern: Nested Parallelism

Inside daemon callbacks (e.g., `mirai_map`), use `local_url()` + `launch_local()` instead of `daemons(n)` to avoid conflicting with the outer daemon pool.

```r
mirai_map(1:10, function(x) {
  daemons(url = local_url())
  launch_local(2)
  result <- mirai_map(1:5, function(y, x) x * y, .args = list(x = x))[]
  daemons(0)
  result
})[]
```
