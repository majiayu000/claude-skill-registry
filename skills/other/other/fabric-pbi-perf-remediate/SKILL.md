---
name: fabric-pbi-perf-remediate
description: Diagnose and resolve Power BI performance issues in Microsoft Fabric. Use when reports load slowly, DAX queries are inefficient, semantic models need optimization, DirectQuery is underperforming, capacity is throttled, visuals render slowly, or data refresh is slow. Covers Performance Analyzer, DAX Studio, Fabric Capacity Metrics app, VOrder, query folding, incremental refresh, storage modes, Best Practice Analyzer, and Spark resource profiles for Power BI workloads.
license: Complete terms in LICENSE.txt
---
# Power BI Performance remediate in Microsoft Fabric

Systematic toolkit for diagnosing, analyzing, and resolving Power BI performance bottlenecks across the Microsoft Fabric platform. Covers semantic model optimization, DAX tuning, capacity management, DirectQuery diagnostics, and report design best practices.

## When to Use This Skill

- Power BI reports are slow to load or interact with
- DAX queries take too long to execute
- Semantic model refresh is slow or timing out
- Fabric capacity is throttled or overutilized
- DirectQuery reports have high latency
- Visuals render slowly or time out
- Users report intermittent performance degradation
- Migrating to Fabric and need to optimize for the new platform
- Planning capacity sizing for Power BI workloads
- Conducting a performance audit or health check

## Prerequisites

| Tool                                    | Purpose                                   | Required     |
| --------------------------------------- | ----------------------------------------- | ------------ |
| Power BI Desktop                        | Performance Analyzer, DAX query view      | Yes          |
| DAX Studio                              | Advanced DAX profiling and server timers  | Recommended  |
| Fabric Capacity Metrics App             | Capacity utilization monitoring           | Yes (admins) |
| Tabular Editor / Best Practice Analyzer | Semantic model analysis                   | Recommended  |
| SQL Server Profiler                     | DirectQuery trace analysis                | Optional     |
| PowerShell 7+                           | Automation scripts included in this skill | Optional     |

## Step-by-Step Workflows

### Workflow 1: Initial Performance Triage

Determine where the bottleneck lives before diving deep.

1. **Reproduce the issue** in Power BI Desktop with Performance Analyzer enabled
   - View ribbon > Performance Analyzer > Start recording > Refresh visuals
2. **Categorize each visual** by its dominant cost:
   - DAX query duration > 500ms → Investigate semantic model / DAX
   - Visual display duration > 500ms → Investigate report design
   - Other duration > 500ms → Investigate data source / gateway
3. **Check capacity health** using the Fabric Capacity Metrics app
   - Look for overload (>100% utilization), throttling events, or queued operations
4. **Route to the appropriate deep-dive workflow below**

### Workflow 2: DAX Query Optimization

See [dax-optimization-patterns.md](./references/dax-optimization-patterns.md) for a comprehensive catalog of anti-patterns and fixes.

1. Capture slow DAX from Performance Analyzer (copy query from visual)
2. Open DAX query view in Power BI Desktop (or DAX Studio)
3. Run query with Server Timings enabled (DAX Studio: Server Timings tab)
4. Analyze the breakdown:
   - **Formula Engine (FE) time**: DAX calculation overhead
   - **Storage Engine (SE) time**: Data scan / retrieval overhead
   - **SE queries count**: High count indicates poor query plan
5. Apply optimization patterns from the reference guide
6. Re-test and compare timings

### Workflow 3: Semantic Model Optimization

See [capacity-optimization.md](./references/capacity-optimization.md) for Fabric-specific tuning.

1. Run Best Practice Analyzer (Tabular Editor or Fabric notebook)
2. Address findings by priority:
   - Remove unused columns and tables
   - Fix incorrect data types (text dates, high-precision decimals)
   - Replace calculated columns with calculated measures where possible
   - Reduce cardinality on high-cardinality columns
3. Evaluate storage mode (Import vs DirectQuery vs Composite)
4. Configure incremental refresh for large fact tables
5. Enable VOrder for read-heavy Power BI workloads in Fabric:
   ```
   spark.sql.parquet.vorder.default=true
   ```

   Or use the `readHeavyForPBI` resource profile at the environment level.

### Workflow 4: Report Design Optimization

1. Audit visual count per page (target: 8 or fewer interactive visuals)
2. Identify high-cardinality visuals (tables/matrices with thousands of rows)
3. Check for excessive cross-filtering between visuals
4. Evaluate filter context complexity (many slicers, complex RLS)
5. Consider:
   - Bookmarks + drill-through instead of dense pages
   - Pre-aggregated measures instead of visual-level calculations
   - Paginated reports for large tabular exports

### Workflow 5: DirectQuery Performance

See [directquery-tuning.md](./references/directquery-tuning.md) for detailed guidance.

1. Enable Performance Analyzer and identify slow DirectQuery visuals
2. Locate trace files for SQL analysis:
   - File > Options > Diagnostics > Open traces folder
   - Find `FlightRecorderCurrent.trc` in the active workspace
3. Open trace in SQL Server Profiler and filter by `DirectQuery Begin/End`
4. Analyze generated SQL for inefficient patterns
5. Optimize at the source (indexes, views, materialized tables)
6. Consider Composite model (Import aggregations + DirectQuery detail)

### Workflow 6: Capacity Monitoring and Sizing

See [capacity-optimization.md](./references/capacity-optimization.md) for detailed guidance.

1. Install and configure the Fabric Capacity Metrics app
2. Monitor key metrics:
   - Interactive vs background operation split
   - Throttling events and queue depth
   - Per-item compute consumption
3. Identify top consumers and optimize or reschedule them
4. Right-size capacity SKU based on measured utilization
5. Consider Autoscale Billing for Spark if bursty workloads exist

## Quick Reference: Common Fixes

| Symptom                          | Likely Cause                   | Quick Fix                                    |
| -------------------------------- | ------------------------------ | -------------------------------------------- |
| All visuals slow                 | Capacity overloaded            | Scale up SKU or reduce concurrency           |
| Single visual slow               | Inefficient DAX measure        | Profile in DAX Studio, rewrite measure       |
| Slow after slicer change         | High cardinality filter        | Reduce distinct values or use Top N          |
| Slow first load, fast after      | Cold cache                     | Enable query caching; check refresh schedule |
| Slow in Service, fast in Desktop | Gateway bottleneck or capacity | Check gateway logs and capacity metrics      |
| Refresh takes hours              | No incremental refresh         | Enable incremental refresh on fact tables    |
| DirectQuery timeouts             | Source query too slow          | Add indexes; consider Import aggregations    |
| Intermittent slowness            | Capacity throttling            | Review Capacity Metrics app for spikes       |

## Automation Scripts

Run the diagnostic PowerShell script to collect environment and configuration data:

```powershell
# Collect Power BI workspace and dataset metadata for analysis
./scripts/Invoke-PBIPerformanceAnalysis.ps1 -WorkspaceId "<workspace-guid>"
```

Analyze DAX query patterns from a semantic model:

```powershell
# Extract and evaluate DAX measures for common anti-patterns
./scripts/Get-DAXQueryMetrics.ps1 -DatasetId "<dataset-guid>" -WorkspaceId "<workspace-guid>"
```

## Performance Assessment Template

Use the [performance-report-template.md](./templates/performance-report-template.md) to document findings and recommendations from a performance audit.

## remediate

| Issue                                | Resolution                                                                               |
| ------------------------------------ | ---------------------------------------------------------------------------------------- |
| Performance Analyzer shows no data   | Ensure you clicked "Start recording" before refreshing                                   |
| DAX Studio cannot connect            | Check XMLA endpoint is enabled on capacity (requires P1/F64+)                            |
| Capacity Metrics app not available   | App requires admin role; install from AppSource                                          |
| VOrder not improving PBI performance | Verify `readHeavyForPBI` profile is active; check file format is Delta/Parquet         |
| Best Practice Analyzer missing rules | Update to latest Tabular Editor; import community rules from te2.wiki                    |
| Scripts fail to authenticate         | Run `Connect-PowerBIServiceAccount` first; ensure Power BI Management module installed |

## References

- [remediate Flowchart](./references/remediate-flowchart.md) - Decision tree for systematic diagnosis
- [DAX Optimization Patterns](./references/dax-optimization-patterns.md) - Anti-patterns and proven fixes
- [Capacity Optimization](./references/capacity-optimization.md) - Fabric capacity tuning for Power BI
- [DirectQuery Tuning](./references/directquery-tuning.md) - Source optimization and Composite models
- [Performance Report Template](./templates/performance-report-template.md) - Audit documentation template
- [Microsoft: Optimization guide for Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization)
- [Microsoft: Troubleshoot report performance](https://learn.microsoft.com/en-us/power-bi/guidance/report-performance-troubleshoot)
- [Microsoft: Monitor report performance](https://learn.microsoft.com/en-us/power-bi/guidance/monitor-report-performance)
- [Microsoft: Evaluate and optimize Fabric capacity](https://learn.microsoft.com/en-us/fabric/enterprise/optimize-capacity)
