---
name: setup-kpi-monitoring
description: "Step-by-step guide for implementing business-aligned KPI monitoring with actionable thresholds, ownership, and dashboards using cloud-agnostic patterns."
---

# Skill: Setup KPI Monitoring

This skill teaches you how to implement KPI (Key Performance Indicator) monitoring for your  services. You'll define business-aligned KPIs, implement collectors, create dashboards, set up alerting, and establish ownership for each metric.

KPIs bridge technical metrics and business outcomes. Observability tells you what broke; KPIs tell you if you're succeeding. Without KPIs, you have data but no insight.

## Prerequisites

- Grafana instance accessible (self-hosted or Grafana Cloud)
- Existing microservice with observability setup
- Prometheus or CloudWatch as metrics backend
- Understanding of your bounded context's business goals

## Overview

In this skill, you will:
1. Define a KPI catalog aligned to business goals
2. Implement KPI collectors in your services
3. Create Grafana dashboards for KPI visualization
4. Set up alerting with actionable thresholds
5. Assign ownership and response plans
6. Create KPI reporting for stakeholders

## Step 1: Define KPI Catalog

```pseudocode
TYPE Category
    RELIABILITY = "reliability"
    PERFORMANCE = "performance"
    BUSINESS = "business"
    OPERATIONAL = "operational"
END TYPE

TYPE IndicatorType
    LEADING = "leading"
    LAGGING = "lagging"
END TYPE

TYPE Threshold
    target: Float64
    warning: Float64
    critical: Float64
    comparison: String  // "gte" or "lte"
END TYPE

TYPE KPIDefinition
    id: String
    name: String
    description: String
    category: Category
    indicatorType: IndicatorType
    unit: String
    threshold: Threshold
    owner: String
    responsePlan: String
    boundedContext: String
    leadingIndicator: String (optional)
END TYPE

TYPE KPICatalog
    version: String
    updatedAt: DateTime
    definitions: List<KPIDefinition>

METHOD KPICatalog.GetByID(id: String) RETURNS (KPIDefinition, Boolean)
    FOR EACH def IN this.definitions DO
        IF def.id == id THEN
            RETURN (def, TRUE)
        END IF
    END FOR
    RETURN (KPIDefinition{}, FALSE)
END METHOD

METHOD KPICatalog.GetByCategory(category: Category) RETURNS List<KPIDefinition>
    result = NewList()
    FOR EACH def IN this.definitions DO
        IF def.category == category THEN
            result.Add(def)
        END IF
    END FOR
    RETURN result
END METHOD
```

## Step 2: Implement KPI Collectors

```pseudocode
TYPE KPIValue
    kpiId: String
    value: Float64
    timestamp: DateTime
    labels: Map<String, String>
    context: String

INTERFACE Collector
    METHOD Collect(ctx: Context) RETURNS Result<KPIValue, Error>
    METHOD KPIID() RETURNS String
    METHOD Interval() RETURNS Duration
END INTERFACE

INTERFACE Publisher
    METHOD Publish(ctx: Context, value: KPIValue) RETURNS Result<Void, Error>
    METHOD PublishBatch(ctx: Context, values: List<KPIValue>) RETURNS Result<Void, Error>
END INTERFACE

TYPE Registry
    collectors: Map<String, Collector>
    publisher: Publisher
    catalog: KPICatalog

METHOD Registry.Register(collector: Collector) RETURNS Result<Void, Error>
    kpiId = collector.KPIID()
    _, exists = this.catalog.GetByID(kpiId)
    IF NOT exists THEN
        RETURN Error("unknown KPI: " + kpiId)
    END IF
    this.collectors[kpiId] = collector
    RETURN Ok(Void)
END METHOD

METHOD Registry.CollectAll(ctx: Context) RETURNS Result<List<KPIValue>, Error>
    values = NewList()
    FOR EACH collector IN this.collectors.Values() DO
        result = collector.Collect(ctx)
        IF result.IsError() THEN
            CONTINUE
        END IF
        values.Add(result.Value())
    END FOR
    RETURN Ok(values)
END METHOD
```

## Step 3: Create Grafana Dashboards

```pseudocode
TYPE GrafanaDashboard
    title: String
    uid: String
    tags: List<String>
    panels: List<Panel>
    refresh: String
    time: TimeRange
END TYPE

TYPE Panel
    id: Int
    title: String
    type: String
    gridPos: GridPos
    targets: List<Target>
    thresholds: List<Threshold>
END TYPE

TYPE DashboardBuilder
    catalog: KPICatalog

METHOD DashboardBuilder.BuildOverviewDashboard() RETURNS GrafanaDashboard
    dashboard = GrafanaDashboard{
        title: "KPI Overview",
        uid: "kpi-overview",
        tags: ["kpi", "business"],
        refresh: "1m",
        panels: NewList()
    }

    FOR EACH category IN [Category.RELIABILITY, Category.PERFORMANCE, Category.BUSINESS, Category.OPERATIONAL] DO
        kpis = this.catalog.GetByCategory(category)
        FOR EACH def IN kpis DO
            panel = this.buildKPIPanel(def)
            dashboard.panels.Add(panel)
        END FOR
    END FOR

    RETURN dashboard
END METHOD
```

## Step 4: Set Up Alerting

```pseudocode
TYPE AlertSeverity
    WARNING = "warning"
    CRITICAL = "critical"
END TYPE

TYPE AlertConfig
    kpiId: String
    name: String
    severity: AlertSeverity
    threshold: Float64
    comparison: String
    evaluationPeriod: Duration
    notificationGroup: String
    runbook: String
    owner: String
END TYPE

TYPE AlertManager
    catalog: KPICatalog

METHOD AlertManager.GenerateAlerts() RETURNS List<AlertConfig>
    alerts = NewList()
    FOR EACH def IN this.catalog.definitions DO
        // Warning alert
        alerts.Add(AlertConfig{
            kpiId: def.id,
            name: def.name + " - Warning",
            severity: AlertSeverity.WARNING,
            threshold: def.threshold.warning,
            runbook: "https://runbooks.example.io/kpi/" + def.id,
            owner: def.owner
        })
        // Critical alert
        alerts.Add(AlertConfig{
            kpiId: def.id,
            name: def.name + " - Critical",
            severity: AlertSeverity.CRITICAL,
            threshold: def.threshold.critical,
            owner: def.owner
        })
    END FOR
    RETURN alerts
END METHOD
```

## Step 5: Assign Ownership

```pseudocode
TYPE Owner
    name: String
    slackChannel: String
    pagerDuty: String
    email: String
    kpis: List<String>
END TYPE

TYPE OwnershipRegistry
    owners: Map<String, Owner>

METHOD OwnershipRegistry.GetOwner(kpiId: String) RETURNS (Owner, Boolean)
    FOR EACH owner IN this.owners.Values() DO
        FOR EACH id IN owner.kpis DO
            IF id == kpiId THEN
                RETURN (owner, TRUE)
            END IF
        END FOR
    END FOR
    RETURN (Owner{}, FALSE)
END METHOD

METHOD OwnershipRegistry.ValidateOwnership(catalog: KPICatalog) RETURNS List<String>
    unowned = NewList()
    FOR EACH def IN catalog.definitions DO
        _, found = this.GetOwner(def.id)
        IF NOT found THEN
            unowned.Add(def.id)
        END IF
    END FOR
    RETURN unowned
END METHOD
```

## Step 6: Create KPI Reporting

```pseudocode
TYPE Report
    title: String
    period: String
    generatedAt: DateTime
    summary: Summary
    kpis: List<KPIStatus>
END TYPE

TYPE Summary
    totalKPIs: Int
    healthy: Int
    warning: Int
    critical: Int
    healthScore: Float64
END TYPE

TYPE KPIStatus
    definition: KPIDefinition
    current: Float64
    previous: Float64
    trend: String
    status: String
END TYPE

TYPE ReportGenerator
    catalog: KPICatalog
    metricsClient: MetricsClient

METHOD ReportGenerator.GenerateWeeklyReport(ctx: Context) RETURNS Result<Report, Error>
    now = CurrentTimeUTC()
    weekAgo = now.AddDays(-7)

    report = Report{
        title: "Weekly KPI Report",
        period: weekAgo.Format("2006-01-02") + " to " + now.Format("2006-01-02"),
        generatedAt: now
    }

    FOR EACH def IN this.catalog.definitions DO
        current = this.metricsClient.QueryKPIValue(ctx, def.id, now)
        previous = this.metricsClient.QueryKPIValue(ctx, def.id, weekAgo)
        status = this.evaluateStatus(def, current)
        report.kpis.Add(KPIStatus{definition: def, current: current, previous: previous, status: status})
    END FOR

    RETURN Ok(report)
END METHOD
```

## Verification Checklist

- [ ] KPI catalog documents all 5-10 critical KPIs
- [ ] Each KPI has business alignment (answers "are we delivering value?")
- [ ] Each KPI has a clear threshold (target, warning, critical)
- [ ] Each KPI has an owner with contact information
- [ ] Each KPI has a response plan documented
- [ ] Leading indicators are included
- [ ] Collectors are implemented for each KPI
- [ ] Grafana dashboard shows all KPIs with thresholds
- [ ] Warning and critical alerts are configured
- [ ] Alert notifications route to correct owners
- [ ] Runbooks exist for each KPI alert
- [ ] Weekly reports are automated
