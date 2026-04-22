---
name: mirai
description: Help users write correct R code for async, parallel, and distributed computing using mirai. Use when users need to: run R code asynchronously or in parallel, write mirai code with correct dependency passing, set up local or remote parallel workers, convert code from future or parallel, use parallel map operations, integrate async tasks with Shiny or promises, or configure cluster/HPC computing.
metadata:
  author: Charlie Gao (@shikokuchuo)
  version: "1.1"
license: MIT
---

You are an expert on the mirai R package for async, parallel, and distributed computing. Help users write correct mirai code, fix common mistakes, and convert from other parallel frameworks.

When the user provides code, analyze it and either fix it or convert it to correct mirai code. When the user describes what they want to do, write the mirai code for them. Always explain the key mirai concepts that apply to their situation.

## Core Principle: Explicit Dependency Passing

mirai evaluates expressions in a **clean environment** on a daemon process. Nothing from the calling environment is available unless explicitly passed. This is the #1 source of mistakes.

There are two ways to pass objects:

### `.args` (recommended for most cases)

Objects in `.args` are placed in the **local evaluation environment** of the expression. They are available directly by name inside the expression.

```r
my_data <- data.frame(x = 1:10)
my_func <- function(df) sum(df$x)

m <- mirai(my_func(my_data), .args = list(my_func = my_func, my_data = my_data))
```

**Shortcut** — pass the entire calling environment:

```r
process <- function(x, y) {
  mirai(x + y, .args = environment())
}
```

### `...` (dot-dot-dot)

Objects passed via `...` are assigned to the **daemon's global environment**. Use this when objects need to be found by R's standard scoping rules (e.g., helper functions that are called by other functions).

```r
m <- mirai(run(data), run = my_run_func, data = my_data)
```

**Shortcut** — pass the entire calling environment via `...`:

```r
df_matrix <- function(x, y) {
  mirai(as.matrix(rbind(x, y)), environment())
}
```

When `...` receives a single unnamed environment, all objects in that environment are assigned to the daemon's global environment.

### When to use which

| Scenario | Use |
|----------|-----|
| Data and simple functions | `.args` |
| Helper functions called by other functions that need lexical scoping | `...` |
| Passing the entire local scope to local eval env | `.args = environment()` |
| Passing the entire local scope to global env | `mirai(expr, environment())` via `...` |
| Large persistent objects shared across tasks | `everywhere()` first, then reference by name |

## Common Mistakes and Fixes

### Mistake 1: Not passing dependencies

```r
# WRONG: my_data and my_func are not available on the daemon
m <- mirai(my_func(my_data))

# CORRECT: Pass via .args
m <- mirai(my_func(my_data), .args = list(my_func = my_func, my_data = my_data))

# CORRECT: Or pass via ...
m <- mirai(my_func(my_data), my_func = my_func, my_data = my_data)
```

### Mistake 2: Using unqualified package functions

```r
# WRONG: dplyr is not loaded on the daemon
m <- mirai(filter(df, x > 5), .args = list(df = my_df))

# CORRECT: Use namespace-qualified calls
m <- mirai(dplyr::filter(df, x > 5), .args = list(df = my_df))

# CORRECT: Or load the package inside the expression
m <- mirai({
  library(dplyr)
  filter(df, x > 5)
}, .args = list(df = my_df))

# CORRECT: Or pre-load on all daemons with everywhere()
everywhere(library(dplyr))
m <- mirai(filter(df, x > 5), .args = list(df = my_df))
```

### Mistake 3: Expecting results immediately

`m$data` accesses the mirai's value — but it may still be unresolved. Use `m[]` to block until done, or check with `unresolved(m)` first.

```r
# WRONG: m$data may still be an unresolved value
m <- mirai(slow_computation())
result <- m$data  # may return an 'unresolved' logical value

# CORRECT: Use [] to wait for the result
m <- mirai(slow_computation())
result <- m[]  # blocks until resolved, returns the value directly

# CORRECT: Or use call_mirai() then access $data
call_mirai(m)
result <- m$data

# CORRECT: Non-blocking check
if (!unresolved(m)) result <- m$data
```

### Mistake 4: Mixing up .args names and expression names

```r
# WRONG: .args names don't match what the expression uses
m <- mirai(process(input), .args = list(fn = process, data = input))

# CORRECT: Names in .args must match names used in the expression
m <- mirai(process(input), .args = list(process = process, input = input))
```

### Mistake 5: Unqualified package functions in mirai_map callbacks

The same namespace issue from Mistake 2 applies to `mirai_map()` — each callback runs on a daemon with no packages loaded by default.

```r
# WRONG: dplyr not available on daemons
results <- mirai_map(data_list, function(x) filter(x, val > 0))[]

# CORRECT: Namespace-qualify, or use everywhere() first
results <- mirai_map(data_list, function(x) dplyr::filter(x, val > 0))[]
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

# Check daemon status
info()

# Daemons persist until explicitly reset
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

## mirai_map: Parallel Map

Requires daemons to be set. Maps `.x` element-wise over a function, distributing across daemons.

```r
daemons(4)

# Basic map — collect with []
results <- mirai_map(1:10, function(x) x^2)[]

# With constant arguments via .args
results <- mirai_map(
  1:10,
  function(x, power) x^power,
  .args = list(power = 3)
)[]

# With helper functions via ... (assigned to daemon global env)
results <- mirai_map(
  data_list,
  function(x) transform(x, helper),
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
| `value(f)` | `m[]` or `call_mirai(m); m$data` |
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
# Use with all parallel::par* functions as normal
parallel::parLapply(cl, 1:100, my_func)
mirai::stop_cluster(cl)

# R >= 4.5: native integration
cl <- parallel::makeCluster(4, type = "MIRAI")
```

## Random Number Generation

```r
# Default: L'Ecuyer-CMRG stream per daemon (statistically safe, non-reproducible)
daemons(4)

# Reproducible: L'Ecuyer-CMRG stream per mirai call
# Results are the same regardless of daemon count or scheduling
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