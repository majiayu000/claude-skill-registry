---
name: setup-cost-optimization
description: "Step-by-step guide for implementing cost optimization strategies for serverless architectures including compute right-sizing, data transfer optimization, storage policies, and cost visibility."
tools: Read, Grep, Glob, Write, Edit, Bash
context: cost-optimization, serverless, right-sizing, storage-policies, cost-allocation, anomaly-detection
---

# Skill: Setup Cost Optimization

This skill teaches you how to implement comprehensive cost optimization for serverless architectures following  patterns. You'll learn to audit costs, right-size compute functions, minimize data transfer, configure storage policies, and set up cost visibility with anomaly detection.

Cost optimization is not a one-time exercise. It's a continuous practice that must be built into your architecture from day one. Serverless "pay-per-use" pricing makes cost directly tied to code efficiency—inefficient code directly translates to higher bills.

Without proper cost governance, serverless costs can spiral quickly. A single misconfigured function with excessive memory or a database table without TTL can silently drain your budget.

## Prerequisites

- Cloud CLI configured with appropriate credentials
- Understanding of serverless compute, NoSQL databases, and object storage
- Existing microservices following  patterns
- Cost Explorer and monitoring service access
- IAM permissions for cost management APIs

## Overview

In this skill, you will:
1. Audit current costs to establish baselines
2. Right-size compute memory using power tuning
3. Optimize data transfer patterns
4. Configure storage policies (database TTL, object storage lifecycle)
5. Implement comprehensive cost tagging
6. Create cost dashboards and reports
7. Set up anomaly detection and alerts

## Step 1: Audit Current Costs

Before optimizing, you need visibility into current spending. This establishes baselines and identifies high-impact optimization targets.

### Cost Analyzer

```pseudocode
TYPE ServiceCost
    serviceName: String
    cost: Float64
    currency: String
    period: String
END TYPE

TYPE CostAnomaly
    resourceId: String
    expectedCost: Float64
    actualCost: Float64
    percentChange: Float64
    detectedAt: DateTime
END TYPE

INTERFACE CostExplorerClient
    METHOD GetCostAndUsage(ctx: Context, input: CostUsageInput) RETURNS Result<CostUsageOutput, Error>
END INTERFACE

TYPE CostAnalyzer
    client: CostExplorerClient

CONSTRUCTOR NewCostAnalyzer(config: CloudConfig) RETURNS CostAnalyzer
    RETURN CostAnalyzer{
        client: NewCostExplorerClient(config)
    }
END CONSTRUCTOR

METHOD CostAnalyzer.GetServiceCosts(ctx: Context, startDate: DateTime, endDate: DateTime) RETURNS Result<List<ServiceCost>, Error>
    input = CostUsageInput{
        timePeriod: DateInterval{
            start: startDate.Format("2006-01-02"),
            end: endDate.Format("2006-01-02")
        },
        granularity: "MONTHLY",
        metrics: ["BlendedCost"],
        groupBy: [GroupDefinition{type: "DIMENSION", key: "SERVICE"}]
    }

    result = this.client.GetCostAndUsage(ctx, input)
    IF result.IsError() THEN
        RETURN Error("failed to get cost data: " + result.Error().Message())
    END IF

    costs = NewList()
    FOR EACH group IN result.Value().ResultsByTime DO
        FOR EACH g IN group.Groups DO
            amount = ParseFloat(g.Metrics["BlendedCost"].Amount)
            currency = g.Metrics["BlendedCost"].Unit
            costs.Add(ServiceCost{
                serviceName: g.Keys[0],
                cost: amount,
                currency: currency,
                period: group.TimePeriod.Start
            })
        END FOR
    END FOR

    RETURN Ok(costs)
END METHOD

METHOD CostAnalyzer.GetComputeCosts(ctx: Context, startDate: DateTime, endDate: DateTime) RETURNS Result<List<ServiceCost>, Error>
    input = CostUsageInput{
        timePeriod: DateInterval{
            start: startDate.Format("2006-01-02"),
            end: endDate.Format("2006-01-02")
        },
        granularity: "DAILY",
        metrics: ["BlendedCost", "UsageQuantity"],
        filter: Expression{
            dimensions: DimensionValues{
                key: "SERVICE",
                values: ["Serverless Compute"]
            }
        },
        groupBy: [GroupDefinition{type: "TAG", key: "function-name"}]
    }

    result = this.client.GetCostAndUsage(ctx, input)
    IF result.IsError() THEN
        RETURN Error("failed to get compute cost data: " + result.Error().Message())
    END IF

    costs = NewList()
    FOR EACH group IN result.Value().ResultsByTime DO
        FOR EACH g IN group.Groups DO
            amount = ParseFloat(g.Metrics["BlendedCost"].Amount)
            costs.Add(ServiceCost{
                serviceName: g.Keys[0],
                cost: amount,
                currency: "USD",
                period: group.TimePeriod.Start
            })
        END FOR
    END FOR

    RETURN Ok(costs)
END METHOD

METHOD CostAnalyzer.DetectAnomalies(ctx: Context, threshold: Float64) RETURNS Result<List<CostAnomaly>, Error>
    // Get last 7 days vs previous 7 days
    now = CurrentTimeUTC()
    currentEnd = now
    currentStart = now.AddDays(-7)
    previousEnd = currentStart
    previousStart = previousEnd.AddDays(-7)

    currentResult = this.GetServiceCosts(ctx, currentStart, currentEnd)
    IF currentResult.IsError() THEN
        RETURN currentResult.Error()
    END IF

    previousResult = this.GetServiceCosts(ctx, previousStart, previousEnd)
    IF previousResult.IsError() THEN
        RETURN previousResult.Error()
    END IF

    // Build lookup for previous period
    prevCosts = NewMap()
    FOR EACH c IN previousResult.Value() DO
        prevCosts[c.serviceName] = c.cost
    END FOR

    anomalies = NewList()
    FOR EACH c IN currentResult.Value() DO
        prev = prevCosts[c.serviceName]
        IF prev > 0 THEN
            change = ((c.cost - prev) / prev) * 100
            IF change > threshold THEN
                anomalies.Add(CostAnomaly{
                    resourceId: c.serviceName,
                    expectedCost: prev,
                    actualCost: c.cost,
                    percentChange: change,
                    detectedAt: now
                })
            END IF
        END IF
    END FOR

    RETURN Ok(anomalies)
END METHOD
```

Run an initial cost audit to establish baselines. Identify the top 5 cost drivers before optimizing.

## Step 2: Right-Size Compute Memory

Serverless compute pricing is based on memory x duration. More memory means faster execution but higher per-ms cost. Finding the optimal balance is critical.

### Compute Optimizer

```pseudocode
TYPE MemoryRecommendation
    functionName: String
    currentMemory: Int32
    recommendedMemory: Int32
    currentCostPerReq: Float64
    optimalCostPerReq: Float64
    savingsPercent: Float64
    reason: String
END TYPE

INTERFACE ComputeClient
    METHOD GetFunction(ctx: Context, functionName: String) RETURNS Result<FunctionConfig, Error>
    METHOD ListFunctions(ctx: Context, marker: String) RETURNS Result<FunctionListOutput, Error>
END INTERFACE

INTERFACE MetricsClient
    METHOD GetMetricStatistics(ctx: Context, input: MetricStatisticsInput) RETURNS Result<MetricStatisticsOutput, Error>
END INTERFACE

TYPE ComputeOptimizer
    computeClient: ComputeClient
    metricsClient: MetricsClient

CONSTRUCTOR NewComputeOptimizer(config: CloudConfig) RETURNS ComputeOptimizer
    RETURN ComputeOptimizer{
        computeClient: NewComputeClient(config),
        metricsClient: NewMetricsClient(config)
    }
END CONSTRUCTOR

METHOD ComputeOptimizer.AnalyzeFunction(ctx: Context, functionName: String) RETURNS Result<MemoryRecommendation, Error>
    // Get current configuration
    configResult = this.computeClient.GetFunction(ctx, functionName)
    IF configResult.IsError() THEN
        RETURN Error("failed to get function config: " + configResult.Error().Message())
    END IF

    currentMemory = configResult.Value().MemorySize

    // Get memory and duration metrics
    avgDurationResult = this.getAverageDuration(ctx, functionName)
    IF avgDurationResult.IsError() THEN
        RETURN avgDurationResult.Error()
    END IF
    avgDuration = avgDurationResult.Value()

    maxMemoryResult = this.getMaxMemoryUsed(ctx, functionName)
    IF maxMemoryResult.IsError() THEN
        RETURN maxMemoryResult.Error()
    END IF
    maxMemoryUsed = maxMemoryResult.Value()

    rec = MemoryRecommendation{
        functionName: functionName,
        currentMemory: currentMemory
    }

    // Calculate memory utilization
    memoryUtilization = Float64(maxMemoryUsed) / Float64(currentMemory) * 100

    // Recommendation logic
    IF memoryUtilization < 50 THEN
        // Over-provisioned: recommend 1.5x max usage
        rec.recommendedMemory = Int32(Ceil(Float64(maxMemoryUsed) * 1.5 / 64) * 64)
        IF rec.recommendedMemory < 128 THEN
            rec.recommendedMemory = 128
        END IF
        rec.reason = Format("Memory utilization only %.1f%%, function is over-provisioned", memoryUtilization)
    ELSE IF memoryUtilization > 85 THEN
        // Near limit: recommend more memory for safety
        rec.recommendedMemory = Int32(Ceil(Float64(currentMemory) * 1.5 / 64) * 64)
        rec.reason = Format("Memory utilization %.1f%%, increase for headroom", memoryUtilization)
    ELSE
        rec.recommendedMemory = currentMemory
        rec.reason = Format("Memory utilization %.1f%%, current setting is optimal", memoryUtilization)
    END IF

    // Calculate cost impact
    // Typical pricing: ~$0.0000166667 per GB-second
    pricePerGBSecond = 0.0000166667
    currentGBSeconds = Float64(currentMemory) / 1024 * avgDuration / 1000
    optimalGBSeconds = Float64(rec.recommendedMemory) / 1024 * avgDuration / 1000

    rec.currentCostPerReq = currentGBSeconds * pricePerGBSecond
    rec.optimalCostPerReq = optimalGBSeconds * pricePerGBSecond

    IF rec.currentCostPerReq > 0 THEN
        rec.savingsPercent = (rec.currentCostPerReq - rec.optimalCostPerReq) / rec.currentCostPerReq * 100
    END IF

    RETURN Ok(rec)
END METHOD

METHOD ComputeOptimizer.getAverageDuration(ctx: Context, functionName: String) RETURNS Result<Float64, Error>
    endTime = CurrentTimeUTC()
    startTime = endTime.AddDays(-7)

    result = this.metricsClient.GetMetricStatistics(ctx, MetricStatisticsInput{
        namespace: "Serverless/Compute",
        metricName: "Duration",
        dimensions: [Dimension{name: "FunctionName", value: functionName}],
        startTime: startTime,
        endTime: endTime,
        period: 86400,  // 1 day
        statistics: ["Average"]
    })

    IF result.IsError() THEN
        RETURN result.Error()
    END IF

    IF result.Value().Datapoints.IsEmpty() THEN
        RETURN Error("no duration data available")
    END IF

    total = 0.0
    FOR EACH dp IN result.Value().Datapoints DO
        total = total + dp.Average
    END FOR

    RETURN Ok(total / Float64(result.Value().Datapoints.Length()))
END METHOD

METHOD ComputeOptimizer.getMaxMemoryUsed(ctx: Context, functionName: String) RETURNS Result<Int32, Error>
    endTime = CurrentTimeUTC()
    startTime = endTime.AddDays(-7)

    result = this.metricsClient.GetMetricStatistics(ctx, MetricStatisticsInput{
        namespace: "Serverless/Compute",
        metricName: "MaxMemoryUsed",
        dimensions: [Dimension{name: "FunctionName", value: functionName}],
        startTime: startTime,
        endTime: endTime,
        period: 86400,
        statistics: ["Maximum"]
    })

    IF result.IsError() THEN
        RETURN result.Error()
    END IF

    maxMem = 0.0
    FOR EACH dp IN result.Value().Datapoints DO
        IF dp.Maximum > maxMem THEN
            maxMem = dp.Maximum
        END IF
    END FOR

    RETURN Ok(Int32(maxMem))
END METHOD

METHOD ComputeOptimizer.AnalyzeAllFunctions(ctx: Context) RETURNS Result<List<MemoryRecommendation>, Error>
    recommendations = NewList()
    nextMarker = ""

    LOOP
        result = this.computeClient.ListFunctions(ctx, nextMarker)
        IF result.IsError() THEN
            RETURN result.Error()
        END IF

        FOR EACH fn IN result.Value().Functions DO
            recResult = this.AnalyzeFunction(ctx, fn.FunctionName)
            IF recResult.IsError() THEN
                CONTINUE  // Skip functions we can't analyze
            END IF
            IF recResult.Value().savingsPercent > 10 THEN  // Only include significant savings
                recommendations.Add(recResult.Value())
            END IF
        END FOR

        IF result.Value().NextMarker IS NULL THEN
            BREAK
        END IF
        nextMarker = result.Value().NextMarker
    END LOOP

    RETURN Ok(recommendations)
END METHOD
```

Run power tuning on your highest-invocation functions first. A 20% reduction on a function invoked 1M times/month saves more than 50% on a rarely-used function.

## Step 3: Optimize Data Transfer

Data transfer costs accumulate silently. Cross-zone traffic, NAT Gateway usage, and public internet egress all add up.

### Data Transfer Optimizer

```pseudocode
TYPE VPCEndpointRecommendation
    serviceName: String
    endpointType: String
    estimatedSavings: Float64
    currentNATCost: Float64
    endpointCost: Float64
    reason: String
END TYPE

TYPE CrossZoneTrafficReport
    sourceZone: String
    destinationZone: String
    bytesTransferred: Int64
    estimatedCost: Float64
    recommendation: String
END TYPE

INTERFACE NetworkClient
    METHOD DescribeVpcEndpoints(ctx: Context, vpcId: String) RETURNS Result<VpcEndpointsOutput, Error>
END INTERFACE

TYPE DataTransferOptimizer
    networkClient: NetworkClient

CONSTRUCTOR NewDataTransferOptimizer(config: CloudConfig) RETURNS DataTransferOptimizer
    RETURN DataTransferOptimizer{
        networkClient: NewNetworkClient(config)
    }
END CONSTRUCTOR

METHOD DataTransferOptimizer.AnalyzeVPCEndpoints(ctx: Context, vpcId: String) RETURNS Result<List<VPCEndpointRecommendation>, Error>
    // Check existing endpoints
    existingResult = this.networkClient.DescribeVpcEndpoints(ctx, vpcId)
    IF existingResult.IsError() THEN
        RETURN Error("failed to describe VPC endpoints: " + existingResult.Error().Message())
    END IF

    existingServices = NewMap()
    FOR EACH ep IN existingResult.Value().VpcEndpoints DO
        existingServices[ep.ServiceName] = TRUE
    END FOR

    // Recommended services for serverless architectures
    recommendedServices = [
        {service: "nosql-database", endpointType: "Gateway", description: "Free gateway endpoint for NoSQL database"},
        {service: "object-storage", endpointType: "Gateway", description: "Free gateway endpoint for object storage"},
        {service: "message-queue", endpointType: "Interface", description: "Interface endpoint for message queue"},
        {service: "notification-service", endpointType: "Interface", description: "Interface endpoint for notifications"},
        {service: "secrets-manager", endpointType: "Interface", description: "Interface endpoint for secrets manager"},
        {service: "config-store", endpointType: "Interface", description: "Interface endpoint for config store"}
    ]

    recommendations = NewList()
    FOR EACH svc IN recommendedServices DO
        IF NOT existingServices[svc.service] THEN
            rec = VPCEndpointRecommendation{
                serviceName: svc.service,
                endpointType: svc.endpointType,
                reason: svc.description
            }

            // Gateway endpoints are free; interface endpoints have hourly cost
            IF svc.endpointType == "Gateway" THEN
                rec.endpointCost = 0
                rec.estimatedSavings = 50  // Estimate based on typical NAT usage
            ELSE
                rec.endpointCost = 7.20 * 24 * 30 / 1000  // ~$7.20/month per zone
                rec.estimatedSavings = 20
            END IF

            recommendations.Add(rec)
        END IF
    END FOR

    RETURN Ok(recommendations)
END METHOD

METHOD DataTransferOptimizer.AnalyzeCrossZoneTraffic(ctx: Context) RETURNS Result<List<CrossZoneTrafficReport>, Error>
    // This would typically query VPC Flow Logs or metrics
    // For demonstration, returning guidance
    RETURN Ok([
        CrossZoneTrafficReport{recommendation: "Deploy functions in single zone when possible"},
        CrossZoneTrafficReport{recommendation: "Use database global tables only when needed"},
        CrossZoneTrafficReport{recommendation: "Co-locate services that communicate frequently"}
    ])
END METHOD
```

Gateway endpoints for object storage and NoSQL databases are typically free. Always deploy them. Interface endpoints cost ~$7/month per zone but eliminate NAT Gateway data processing charges.

## Step 4: Configure Storage Policies

Storage costs grow silently over time. Without lifecycle policies and TTL, old data accumulates indefinitely.

### Database TTL Configuration

```pseudocode
TYPE TTLRecommendation
    tableName: String
    hasTTL: Boolean
    ttlAttribute: String
    itemCount: Int64
    tableSizeBytes: Int64
    recommendation: String
END TYPE

INTERFACE DatabaseClient
    METHOD ListTables(ctx: Context) RETURNS Result<TableListOutput, Error>
    METHOD DescribeTable(ctx: Context, tableName: String) RETURNS Result<TableDescription, Error>
    METHOD DescribeTimeToLive(ctx: Context, tableName: String) RETURNS Result<TTLDescription, Error>
    METHOD UpdateTimeToLive(ctx: Context, tableName: String, attributeName: String, enabled: Boolean) RETURNS Result<Void, Error>
END INTERFACE

TYPE DatabaseOptimizer
    client: DatabaseClient

CONSTRUCTOR NewDatabaseOptimizer(config: CloudConfig) RETURNS DatabaseOptimizer
    RETURN DatabaseOptimizer{
        client: NewDatabaseClient(config)
    }
END CONSTRUCTOR

METHOD DatabaseOptimizer.AnalyzeTTL(ctx: Context) RETURNS Result<List<TTLRecommendation>, Error>
    recommendations = NewList()

    tablesResult = this.client.ListTables(ctx)
    IF tablesResult.IsError() THEN
        RETURN Error("failed to list tables: " + tablesResult.Error().Message())
    END IF

    FOR EACH tableName IN tablesResult.Value().TableNames DO
        // Get table description
        descResult = this.client.DescribeTable(ctx, tableName)
        IF descResult.IsError() THEN
            CONTINUE
        END IF

        // Check TTL status
        ttlResult = this.client.DescribeTimeToLive(ctx, tableName)
        IF ttlResult.IsError() THEN
            CONTINUE
        END IF

        rec = TTLRecommendation{
            tableName: tableName,
            itemCount: descResult.Value().ItemCount,
            tableSizeBytes: descResult.Value().TableSizeBytes
        }

        IF ttlResult.Value().Status == "ENABLED" THEN
            rec.hasTTL = TRUE
            rec.ttlAttribute = ttlResult.Value().AttributeName
            rec.recommendation = "TTL is configured correctly"
        ELSE
            rec.hasTTL = FALSE
            rec.recommendation = "Consider enabling TTL to automatically delete old items"
        END IF

        recommendations.Add(rec)
    END FOR

    RETURN Ok(recommendations)
END METHOD

METHOD DatabaseOptimizer.EnableTTL(ctx: Context, tableName: String, attributeName: String) RETURNS Result<Void, Error>
    result = this.client.UpdateTimeToLive(ctx, tableName, attributeName, TRUE)
    IF result.IsError() THEN
        RETURN Error("failed to enable TTL: " + result.Error().Message())
    END IF
    RETURN Ok(Void)
END METHOD
```

### Object Storage Lifecycle Policies

```pseudocode
TYPE LifecycleRecommendation
    bucketName: String
    hasLifecycleRules: Boolean
    ruleCount: Int
    recommendation: String
END TYPE

TYPE LifecycleRule
    id: String
    status: String
    prefix: String
    transitions: List<Transition>
    expiration: Expiration (optional)
END TYPE

TYPE Transition
    days: Int32
    storageClass: String
END TYPE

INTERFACE ObjectStorageClient
    METHOD ListBuckets(ctx: Context) RETURNS Result<BucketListOutput, Error>
    METHOD GetBucketLifecycleConfiguration(ctx: Context, bucketName: String) RETURNS Result<LifecycleConfiguration, Error>
    METHOD PutBucketLifecycleConfiguration(ctx: Context, bucketName: String, rules: List<LifecycleRule>) RETURNS Result<Void, Error>
END INTERFACE

TYPE ObjectStorageOptimizer
    client: ObjectStorageClient

CONSTRUCTOR NewObjectStorageOptimizer(config: CloudConfig) RETURNS ObjectStorageOptimizer
    RETURN ObjectStorageOptimizer{
        client: NewObjectStorageClient(config)
    }
END CONSTRUCTOR

METHOD ObjectStorageOptimizer.AnalyzeLifecycles(ctx: Context) RETURNS Result<List<LifecycleRecommendation>, Error>
    bucketsResult = this.client.ListBuckets(ctx)
    IF bucketsResult.IsError() THEN
        RETURN Error("failed to list buckets: " + bucketsResult.Error().Message())
    END IF

    recommendations = NewList()
    FOR EACH bucket IN bucketsResult.Value().Buckets DO
        rec = LifecycleRecommendation{
            bucketName: bucket.Name
        }

        lifecycleResult = this.client.GetBucketLifecycleConfiguration(ctx, bucket.Name)
        IF lifecycleResult.IsError() THEN
            rec.hasLifecycleRules = FALSE
            rec.recommendation = "No lifecycle rules configured - consider adding rules for cost optimization"
        ELSE
            rec.hasLifecycleRules = TRUE
            rec.ruleCount = lifecycleResult.Value().Rules.Length()
            rec.recommendation = Format("%d lifecycle rules configured", rec.ruleCount)
        END IF

        recommendations.Add(rec)
    END FOR

    RETURN Ok(recommendations)
END METHOD

METHOD ObjectStorageOptimizer.CreateStandardLifecycleRules(ctx: Context, bucketName: String) RETURNS Result<Void, Error>
    rules = [
        LifecycleRule{
            id: "transition-to-ia-30-days",
            status: "Enabled",
            prefix: "",
            transitions: [
                Transition{days: 30, storageClass: "STANDARD_IA"}
            ]
        },
        LifecycleRule{
            id: "transition-to-archive-90-days",
            status: "Enabled",
            prefix: "archive/",
            transitions: [
                Transition{days: 90, storageClass: "ARCHIVE"}
            ]
        },
        LifecycleRule{
            id: "delete-old-versions-30-days",
            status: "Enabled",
            prefix: "",
            noncurrentVersionExpiration: NoncurrentVersionExpiration{noncurrentDays: 30}
        }
    ]

    result = this.client.PutBucketLifecycleConfiguration(ctx, bucketName, rules)
    IF result.IsError() THEN
        RETURN Error("failed to create lifecycle rules: " + result.Error().Message())
    END IF

    RETURN Ok(Void)
END METHOD
```

Enable TTL on all database tables with temporal data. Transition objects to infrequent access after 30 days and archive after 90 days for archival data.

## Step 5: Implement Cost Tagging

Tags enable cost allocation and accountability. Without tags, you cannot attribute costs to teams or services.

### Tagging Standards

```pseudocode
TYPE StandardTags
    service: String      // e.g., "facilitysvc"
    environment: String  // e.g., "production", "staging"
    team: String         // e.g., "platform", "billing"
    costCenter: String   // e.g., "CC-1234"
    project: String      // e.g., "-core"
END TYPE

FUNCTION RequiredTags() RETURNS List<String>
    RETURN ["service", "environment", "team", "cost_center", "project"]
END FUNCTION

FUNCTION ValidateResourceTags(tags: Map<String, String>) RETURNS List<String>
    missing = NewList()
    FOR EACH required IN RequiredTags() DO
        IF NOT tags.ContainsKey(required) THEN
            missing.Add(required)
        END IF
    END FOR
    RETURN missing
END FUNCTION

FUNCTION ApplyStandardTags(existingTags: Map<String, String>, standard: StandardTags) RETURNS Map<String, String>
    IF existingTags IS NULL THEN
        existingTags = NewMap()
    END IF
    existingTags["service"] = standard.service
    existingTags["environment"] = standard.environment
    existingTags["team"] = standard.team
    existingTags["cost_center"] = standard.costCenter
    existingTags["project"] = standard.project
    RETURN existingTags
END FUNCTION

TYPE TagComplianceReport
    totalResources: Int
    compliantResources: Int
    nonCompliantResources: List<NonCompliantResource>
END TYPE

TYPE NonCompliantResource
    resourceId: String
    resourceType: String
    missingTags: List<String>
END TYPE

TYPE TagComplianceChecker
    resourceClient: ResourceClient

METHOD TagComplianceChecker.CheckCompliance(ctx: Context) RETURNS Result<TagComplianceReport, Error>
    report = TagComplianceReport{
        nonCompliantResources: NewList()
    }

    resourcesResult = this.resourceClient.ListAllResources(ctx)
    IF resourcesResult.IsError() THEN
        RETURN resourcesResult.Error()
    END IF

    FOR EACH resource IN resourcesResult.Value() DO
        report.totalResources = report.totalResources + 1
        missingTags = ValidateResourceTags(resource.Tags)

        IF missingTags.IsEmpty() THEN
            report.compliantResources = report.compliantResources + 1
        ELSE
            report.nonCompliantResources.Add(NonCompliantResource{
                resourceId: resource.Id,
                resourceType: resource.Type,
                missingTags: missingTags
            })
        END IF
    END FOR

    RETURN Ok(report)
END METHOD
```

Activate cost allocation tags in the Billing console. Run a weekly report to identify untagged resources.

## Step 6: Create Cost Dashboards

Visibility drives accountability. Create dashboards that show cost trends and anomalies.

### Cost Dashboard Builder

```pseudocode
TYPE DashboardWidget
    type: String
    x: Int
    y: Int
    width: Int
    height: Int
    properties: Map<String, Any>
END TYPE

INTERFACE DashboardClient
    METHOD PutDashboard(ctx: Context, name: String, body: String) RETURNS Result<Void, Error>
END INTERFACE

TYPE CostDashboardBuilder
    client: DashboardClient

CONSTRUCTOR NewCostDashboardBuilder(config: CloudConfig) RETURNS CostDashboardBuilder
    RETURN CostDashboardBuilder{
        client: NewDashboardClient(config)
    }
END CONSTRUCTOR

METHOD CostDashboardBuilder.CreateServiceCostDashboard(ctx: Context, serviceName: String) RETURNS Result<Void, Error>
    widgets = [
        DashboardWidget{
            type: "text",
            x: 0, y: 0, width: 24, height: 1,
            properties: {"markdown": Format("# %s Cost Dashboard", serviceName)}
        },
        DashboardWidget{
            type: "metric",
            x: 0, y: 1, width: 12, height: 6,
            properties: {
                "title": "Function Invocations",
                "view": "timeSeries",
                "stacked": FALSE,
                "metrics": [
                    ["Serverless/Compute", "Invocations", "FunctionName", serviceName + "-api"]
                ],
                "period": 3600
            }
        },
        DashboardWidget{
            type: "metric",
            x: 12, y: 1, width: 12, height: 6,
            properties: {
                "title": "Function Duration (Cost Driver)",
                "view": "timeSeries",
                "metrics": [
                    ["Serverless/Compute", "Duration", "FunctionName", serviceName + "-api", {"stat": "p50"}],
                    ["...", {"stat": "p99"}]
                ],
                "period": 3600
            }
        },
        DashboardWidget{
            type: "metric",
            x: 0, y: 7, width: 12, height: 6,
            properties: {
                "title": "Database Consumed Capacity",
                "view": "timeSeries",
                "metrics": [
                    ["NoSQL/Database", "ConsumedReadCapacityUnits", "TableName", serviceName + "-table"],
                    ["NoSQL/Database", "ConsumedWriteCapacityUnits", "TableName", serviceName + "-table"]
                ],
                "period": 3600
            }
        }
    ]

    body = {"widgets": widgets}
    bodyJSON = JsonSerialize(body)

    result = this.client.PutDashboard(ctx, Format("%s-cost-dashboard", serviceName), bodyJSON)
    RETURN result
END METHOD
```

Create dashboards for each service showing invocations, duration, and consumed capacity—the primary cost drivers.

## Step 7: Implement Anomaly Alerts

Detect cost spikes before they become expensive surprises.

### Cost Anomaly Alerting

```pseudocode
TYPE CostAlert
    alarmName: String
    description: String
    metricName: String
    namespace: String
    dimensions: List<Dimension>
    period: Int32
    evaluationPeriods: Int32
    threshold: Float64
    comparisonOperator: String
    alarmActions: List<String>
END TYPE

INTERFACE AlertClient
    METHOD PutMetricAlarm(ctx: Context, input: MetricAlarmInput) RETURNS Result<Void, Error>
END INTERFACE

TYPE CostAlertManager
    client: AlertClient

CONSTRUCTOR NewCostAlertManager(config: CloudConfig) RETURNS CostAlertManager
    RETURN CostAlertManager{
        client: NewAlertClient(config)
    }
END CONSTRUCTOR

METHOD CostAlertManager.CreateComputeCostAlert(ctx: Context, functionName: String, notificationArn: String) RETURNS Result<Void, Error>
    // Alert if invocations spike 200% above normal
    result = this.client.PutMetricAlarm(ctx, MetricAlarmInput{
        alarmName: Format("%s-invocation-spike", functionName),
        alarmDescription: "Compute invocations significantly above normal - potential cost impact",
        metricName: "Invocations",
        namespace: "Serverless/Compute",
        statistic: "Sum",
        dimensions: [Dimension{name: "FunctionName", value: functionName}],
        period: 3600,  // 1 hour
        evaluationPeriods: 1,
        threshold: 10000,  // Adjust based on baseline
        comparisonOperator: "GreaterThanThreshold",
        alarmActions: [notificationArn],
        treatMissingData: "notBreaching"
    })
    RETURN result
END METHOD

METHOD CostAlertManager.CreateDatabaseCostAlert(ctx: Context, tableName: String, notificationArn: String) RETURNS Result<Void, Error>
    result = this.client.PutMetricAlarm(ctx, MetricAlarmInput{
        alarmName: Format("%s-consumed-capacity-spike", tableName),
        alarmDescription: "Database consumed capacity above threshold - potential cost impact",
        metricName: "ConsumedReadCapacityUnits",
        namespace: "NoSQL/Database",
        statistic: "Sum",
        dimensions: [Dimension{name: "TableName", value: tableName}],
        period: 300,  // 5 minutes
        evaluationPeriods: 3,
        threshold: 1000,  // Adjust based on baseline
        comparisonOperator: "GreaterThanThreshold",
        alarmActions: [notificationArn],
        treatMissingData: "notBreaching"
    })
    RETURN result
END METHOD

METHOD CostAlertManager.CreateBudgetAlert(ctx: Context, budgetName: String, monthlyLimit: Float64, notificationArn: String) RETURNS Result<Void, Error>
    // Create alerts at 50%, 80%, and 100% of budget
    thresholds = [50.0, 80.0, 100.0]

    FOR EACH threshold IN thresholds DO
        result = this.client.PutBudgetAlert(ctx, BudgetAlertInput{
            budgetName: budgetName,
            limit: monthlyLimit,
            thresholdPercent: threshold,
            notificationArn: notificationArn
        })
        IF result.IsError() THEN
            RETURN result.Error()
        END IF
    END FOR

    RETURN Ok(Void)
END METHOD
```

Set alerts at 150% and 200% of baseline costs. Investigate any spike immediately.

## Verification Checklist

After setting up cost optimization:

- [ ] Cost Explorer shows costs grouped by service tags
- [ ] All serverless functions analyzed for memory right-sizing
- [ ] VPC endpoints deployed for object storage and NoSQL database (free Gateway endpoints)
- [ ] Database tables have TTL enabled for temporal data
- [ ] Object storage buckets have lifecycle policies for automatic tiering
- [ ] All resources tagged with service, environment, team, cost_center
- [ ] Cost dashboards exist for each major service
- [ ] Anomaly alerts configured at 150% and 200% of baseline
- [ ] Weekly cost review meetings scheduled
- [ ] Untagged resource report runs daily
- [ ] Monthly cost optimization review documented
- [ ] Budget alerts set at 50%, 80%, and 100% thresholds
