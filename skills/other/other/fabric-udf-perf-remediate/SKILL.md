---
name: fabric-udf-perf-remediate
description: Diagnose and resolve performance issues with Microsoft Fabric User Data Functions. Use when functions are slow, timing out, returning errors, consuming excessive capacity units, or exhibiting cold start latency. Covers execution timeouts, response size limits, connection bottlenecks, logging analysis, capacity metrics monitoring, invocation diagnostics, Python optimization, and UDF service limit remediate.
license: Complete terms in LICENSE.txt
---
# Microsoft Fabric User Data Functions Performance remediate

Systematic guide for diagnosing and resolving performance issues with Fabric User Data Functions (UDFs). Covers cold starts, execution timeouts, capacity consumption, connection bottlenecks, and Python code optimization.

## When to Use This Skill

- Function invocations are slow or intermittently timing out
- Capacity metrics show unexpected CU consumption from UDF operations
- Functions fail with timeout, response size, or connection errors
- Cold start latency is impacting downstream consumers (Pipelines, Notebooks, Power BI)
- Historical logs show increasing duration trends
- Need to optimize UDF code for better performance within service limits

## Prerequisites

- Access to the Fabric portal with permissions on the User Data Functions item
- Microsoft Fabric Capacity Metrics app installed (for CU analysis)
- Python 3.11+ locally (for code profiling outside Fabric)
- PowerShell 7+ (for running diagnostic scripts)

## Service Limits Quick Reference

| Limit                 | Value       | Impact                           |
| --------------------- | ----------- | -------------------------------- |
| Request payload       | 4 MB        | All input parameters combined    |
| Execution timeout     | 240 seconds | Maximum function runtime         |
| Response size         | 30 MB       | Maximum return value size        |
| Log retention         | 30 days     | Historical invocation log window |
| Private library max   | 28.6 MB     | Per `.whl` file upload         |
| Test session timeout  | 15 minutes  | Idle timeout in Develop mode     |
| Daily log ingestion   | 250 MB      | Logs may be sampled beyond this  |
| Python version (Run)  | 3.11        | Published functions runtime      |
| Python version (Test) | 3.12        | Develop mode test runtime        |

## Step-by-Step remediate Workflow

### Step 1: Identify the Symptom

Determine which category your issue falls into:

| Symptom                                | Likely Root Cause                         | Go To  |
| -------------------------------------- | ----------------------------------------- | ------ |
| First invocation slow, subsequent fast | Cold start / initialization               | Step 2 |
| All invocations consistently slow      | Code inefficiency or data volume          | Step 3 |
| Intermittent timeouts                  | Connection issues or capacity throttling  | Step 4 |
| Response too large error               | Unbounded query results                   | Step 5 |
| High CU consumption in Metrics app     | Excessive execution frequency or duration | Step 6 |
| Function fails with import errors      | Library loading overhead                  | Step 7 |

### Step 2: Diagnose Cold Start Latency

Fabric User Data Functions run in a serverless environment. The first invocation after a period of inactivity incurs initialization overhead.

**Check historical logs for the pattern:**

1. Switch to **Run only mode** in the Functions portal
2. Open **View historical log** for the target function
3. Compare Duration(ms) of the first invocation vs. subsequent ones
4. A 3-10x difference confirms cold start behavior

**Mitigations:**

- Implement a health-check or warm-up invocation on a schedule via Pipeline
- Minimize top-level imports; use lazy imports for heavy libraries
- Reduce private library count and size (each `.whl` adds init time)
- Keep PyPI dependency list minimal in `definition.json`

### Step 3: Profile Slow Function Code

For consistently slow functions, instrument your code with timing:

```python
import logging
import time

@udf.function()
def my_function(param: str) -> str:
    start = time.perf_counter()

    # Phase 1: Data retrieval
    t1 = time.perf_counter()
    data = fetch_data(param)
    logging.info(f"Data retrieval: {time.perf_counter() - t1:.3f}s")

    # Phase 2: Processing
    t2 = time.perf_counter()
    result = process(data)
    logging.info(f"Processing: {time.perf_counter() - t2:.3f}s")

    logging.info(f"Total execution: {time.perf_counter() - start:.3f}s")
    return result
```

Review logs in the **Invocation details** pane to identify the slowest phase.

**Common bottlenecks and fixes:**

- **Data source queries**: Add WHERE clauses, limit columns, use parameterized queries
- **DataFrame operations**: Filter early, avoid iterrows(), use vectorized operations
- **Serialization**: Return only required fields, use compact formats
- **External API calls**: Add timeouts, implement retry with backoff

See [performance-optimization.md](./references/performance-optimization.md) for detailed code patterns.

### Step 4: Investigate Connection and Timeout Issues

**Connection errors to Fabric data sources:**

1. Verify connections in **Manage connections** panel
2. Confirm credentials are valid and not expired
3. Check that connected data source artifacts still exist
4. Test the data source independently (run a query directly in the Warehouse/Lakehouse)

**Capacity throttling indicators:**

1. Open the **Microsoft Fabric Capacity Metrics** app
2. Navigate to the **Compute** page
3. Filter to the workspace containing your UDF
4. Check if CU utilization exceeds 100% during the failure window
5. Look for HTTP 430 errors in logs: `TooManyRequestsForCapacity`

**Timeout approaching 240s:**

- Break large operations into smaller chunks
- Implement pagination in data retrieval
- Consider moving heavy processing to a Notebook and using the UDF as a thin API layer
- Use `logging.warning()` to flag operations exceeding thresholds

### Step 5: Resolve Response Size Issues

The 30 MB response limit triggers when functions return large datasets unbounded.

**Diagnostic approach:**

```python
import sys
import json
import logging

@udf.function()
def my_query_function() -> list:
    results = execute_query()
    size_bytes = sys.getsizeof(json.dumps(results))
    logging.info(f"Response size estimate: {size_bytes / (1024*1024):.2f} MB")

    if size_bytes > 25_000_000:  # 25 MB warning threshold
        logging.warning("Response approaching 30 MB limit")

    return results
```

**Mitigations:**

- Add TOP/LIMIT clauses to queries
- Implement pagination with offset parameters
- Return summary/aggregated data instead of raw rows
- Compress or filter response fields

### Step 6: Analyze Capacity Consumption

UDF operations reported in the Fabric Capacity Metrics app:

| Operation                                | Type        | Trigger                                                  |
| ---------------------------------------- | ----------- | -------------------------------------------------------- |
| User Data Functions Execution            | Interactive | Function invoked by portal, Fabric item, or external app |
| User Data Functions Portal Test          | Interactive | Testing in Develop mode (minimum 15-min session)         |
| User Data Functions Static Storage       | Background  | Metadata stored in OneLake (always-on cost)              |
| User Data Functions Static Storage Read  | Background  | Metadata read after inactivity period                    |
| User Data Functions Static Storage Write | Background  | Every publish operation                                  |

**Cost reduction strategies:**

- Reduce invocation frequency from calling items (Pipelines, Notebooks)
- Cache results in the caller when data doesn't change frequently
- Optimize function duration (execution time directly impacts CU consumption)
- Consolidate multiple small functions into fewer, more efficient ones
- Avoid unnecessary publishes (each triggers storage write operations)

Run the [capacity-analysis.ps1](./scripts/capacity-analysis.ps1) script to generate a capacity usage summary.

### Step 7: Resolve Library Loading Issues

Heavy or numerous libraries increase initialization time and can cause import errors.

**Best practices:**

- Use only libraries you actually need in `definition.json`
- Pin specific versions to avoid unexpected updates
- Prefer lightweight alternatives (e.g., `httpx` over `requests` if async needed)
- Custom `.whl` files must be under 28.6 MB each
- Use lazy imports for rarely-used heavy libraries

```python
# Instead of top-level import
# import heavy_library

@udf.function()
def my_function() -> str:
    import heavy_library  # Lazy import - only loads when function is called
    return heavy_library.process()
```

## Logging Best Practices for Performance Monitoring

Use structured logging to make performance data queryable in historical logs:

```python
import logging

# Log at key decision points
logging.info(f"PERF|function_name|phase|{duration_ms}ms|{record_count} rows")

# Use appropriate levels
logging.warning(f"PERF|slow_query|{duration_ms}ms exceeds 5000ms threshold")
logging.error(f"PERF|timeout_risk|{duration_ms}ms approaching 240s limit")
```

See the [logging template](./templates/perf_logging.py) for a reusable instrumented function pattern.

## remediate Decision Tree

```
Function is slow or failing
├── First call only? → Cold start (Step 2)
├── All calls slow?
│   ├── Data source query slow? → Optimize query (Step 3)
│   ├── Processing slow? → Profile code (Step 3)
│   └── Response too large? → Add pagination (Step 5)
├── Intermittent failures?
│   ├── HTTP 430 errors? → Capacity throttling (Step 4)
│   ├── Connection timeout? → Data source issues (Step 4)
│   └── Import errors? → Library problems (Step 7)
└── High CU bill?
    └── Analyze metrics app (Step 6)
```

## Regional Limitations

User Data Functions are not available in all Fabric regions. The Test capability in Develop mode is additionally unavailable in Brazil South, Israel Central, and Mexico Central. If your tenant region is unsupported, create a Capacity in a supported region.

Check current region availability at [Fabric region availability](https://learn.microsoft.com/en-us/fabric/admin/region-availability).

## References

- [Performance Optimization Patterns](./references/performance-optimization.md) - Detailed code optimization techniques
- [Capacity Analysis Script](./scripts/capacity-analysis.ps1) - PowerShell script to summarize UDF capacity usage
- [Diagnostic Checklist Script](./scripts/diagnostic-checklist.ps1) - Interactive remediate walkthrough
- [Performance Logging Template](./templates/perf_logging.py) - Instrumented function boilerplate
- [Microsoft Docs: View Function Logs](https://learn.microsoft.com/en-us/fabric/data-engineering/user-data-functions/view-function-logs)
- [Microsoft Docs: Service Limits](https://learn.microsoft.com/en-us/fabric/data-engineering/user-data-functions/user-data-functions-service-limits)
- [Microsoft Docs: Fabric Operations](https://learn.microsoft.com/en-us/fabric/enterprise/fabric-operations)
- [Microsoft Docs: Capacity Metrics App](https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app)
