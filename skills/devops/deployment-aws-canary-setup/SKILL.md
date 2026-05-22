---
name: deployment-aws-canary-setup
description: "Step-by-step guide for setting up AWS Lambda canary deployments with CDK, CloudWatch alarms, and automated rollback."
---

# Skill: AWS Canary Deployment Setup

This skill teaches you how to set up progressive canary deployments for AWS Lambda using CDK TypeScript. You'll configure Lambda versions and aliases, CloudWatch alarms for automated rollback, and CodeDeploy deployment groups for traffic shifting.

Canary deployments reduce deployment risk by routing a small percentage of traffic to new code first. If the new version performs well (low errors, acceptable latency), traffic gradually shifts until 100% reaches the new version. If metrics fail, traffic automatically rolls back to the stable version.

This approach is essential for production workloads where zero-downtime deployments and automatic failure recovery are critical requirements.

## Prerequisites

- AWS CDK v2 installed (`npm install -g aws-cdk`)
- TypeScript project with CDK configured
- Lambda function deployed with proper IAM roles
- CloudWatch configured for Lambda metrics
- Understanding of Lambda versions and aliases

## Overview

In this skill, you will:
1. Create Lambda function with versioning and alias
2. Configure CloudWatch alarms for error rate and latency
3. Set up CodeDeploy deployment group with canary config
4. Create CDK stack with all deployment infrastructure
5. Implement rollback procedures
6. Add monitoring dashboard for canary metrics

## Step 1: Create Lambda with Versioning and Alias

Lambda versions are immutable snapshots of your function code and configuration. Aliases are mutable pointers that can route traffic between versions.

### CDK Lambda Construct with Versioning

```typescript
// lib/constructs/versioned-lambda.ts
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as codedeploy from 'aws-cdk-lib/aws-codedeploy';
import { Construct } from 'constructs';

export interface VersionedLambdaProps {
  functionName: string;
  description: string;
  codePath: string;
  handler: string;
  runtime: lambda.Runtime;
  memorySize?: number;
  timeout?: cdk.Duration;
  environment?: { [key: string]: string };
  reservedConcurrentExecutions?: number;
}

export class VersionedLambda extends Construct {
  public readonly function: lambda.Function;
  public readonly alias: lambda.Alias;
  public readonly currentVersion: lambda.Version;

  constructor(scope: Construct, id: string, props: VersionedLambdaProps) {
    super(scope, id);

    // Create Lambda function with tracing enabled
    this.function = new lambda.Function(this, 'Function', {
      functionName: props.functionName,
      description: props.description,
      runtime: props.runtime,
      handler: props.handler,
      code: lambda.Code.fromAsset(props.codePath),
      memorySize: props.memorySize ?? 256,
      timeout: props.timeout ?? cdk.Duration.seconds(30),
      environment: props.environment,
      tracing: lambda.Tracing.ACTIVE,
      reservedConcurrentExecutions: props.reservedConcurrentExecutions,
      // Enable versioning by setting currentVersionOptions
      currentVersionOptions: {
        removalPolicy: cdk.RemovalPolicy.RETAIN,
        description: `Version deployed at ${new Date().toISOString()}`,
      },
    });

    // Get the current version (creates new version on each deployment)
    this.currentVersion = this.function.currentVersion;

    // Create alias pointing to current version
    // The alias is what API Gateway or other services invoke
    this.alias = new lambda.Alias(this, 'LiveAlias', {
      aliasName: 'live',
      version: this.currentVersion,
      description: 'Production traffic alias',
    });
  }
}
```

The key concepts here:
- **Versions**: Each deployment creates an immutable version snapshot
- **Alias**: The "live" alias is what clients invoke, not a specific version
- **Traffic routing**: The alias can split traffic between two versions

### Using the Construct

```typescript
// lib/stacks/api-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import { VersionedLambda } from '../constructs/versioned-lambda';

export class ApiStack extends cdk.Stack {
  public readonly apiHandler: VersionedLambda;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const stage = this.node.tryGetContext('stage') || 'dev';

    this.apiHandler = new VersionedLambda(this, 'ApiHandler', {
      functionName: `my-service-api-${stage}`,
      description: 'API handler for my-service',
      codePath: '../dist/api',
      handler: 'bootstrap',
      runtime: lambda.Runtime.PROVIDED_AL2023,
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
      environment: {
        STAGE: stage,
        LOG_LEVEL: stage === 'prod' ? 'INFO' : 'DEBUG',
      },
    });

    // Export alias ARN for API Gateway integration
    new cdk.CfnOutput(this, 'ApiAliasArn', {
      value: this.apiHandler.alias.functionArn,
      description: 'Lambda alias ARN for API Gateway',
    });
  }
}
```

## Step 2: Configure CloudWatch Alarms

CloudWatch alarms monitor your Lambda's health during deployment. If metrics breach thresholds, CodeDeploy triggers automatic rollback.

### Alarm Configuration Construct

```typescript
// lib/constructs/deployment-alarms.ts
import * as cdk from 'aws-cdk-lib';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export interface DeploymentAlarmsProps {
  lambdaFunction: lambda.Function;
  alias: lambda.Alias;
  alarmNamePrefix: string;
  // Thresholds
  errorRateThreshold?: number;      // Default: 1%
  latencyP99Threshold?: number;     // Default: 5000ms
  throttleThreshold?: number;       // Default: 10 per minute
  evaluationPeriods?: number;       // Default: 2
}

export class DeploymentAlarms extends Construct {
  public readonly errorAlarm: cloudwatch.Alarm;
  public readonly latencyAlarm: cloudwatch.Alarm;
  public readonly throttleAlarm: cloudwatch.Alarm;
  public readonly allAlarms: cloudwatch.Alarm[];

  constructor(scope: Construct, id: string, props: DeploymentAlarmsProps) {
    super(scope, id);

    const evaluationPeriods = props.evaluationPeriods ?? 2;

    // Error rate alarm - triggers rollback if errors exceed threshold
    this.errorAlarm = new cloudwatch.Alarm(this, 'ErrorAlarm', {
      alarmName: `${props.alarmNamePrefix}-errors`,
      alarmDescription: 'Lambda error rate exceeded threshold during deployment',
      metric: props.alias.metricErrors({
        period: cdk.Duration.minutes(1),
        statistic: 'Sum',
      }),
      threshold: props.errorRateThreshold ?? 10,
      evaluationPeriods: evaluationPeriods,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });

    // P99 latency alarm - triggers rollback if latency too high
    this.latencyAlarm = new cloudwatch.Alarm(this, 'LatencyAlarm', {
      alarmName: `${props.alarmNamePrefix}-latency-p99`,
      alarmDescription: 'Lambda P99 latency exceeded threshold during deployment',
      metric: props.alias.metricDuration({
        period: cdk.Duration.minutes(1),
        statistic: 'p99',
      }),
      threshold: props.latencyP99Threshold ?? 5000,
      evaluationPeriods: evaluationPeriods,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });

    // Throttle alarm - indicates capacity issues
    this.throttleAlarm = new cloudwatch.Alarm(this, 'ThrottleAlarm', {
      alarmName: `${props.alarmNamePrefix}-throttles`,
      alarmDescription: 'Lambda throttling detected during deployment',
      metric: props.alias.metricThrottles({
        period: cdk.Duration.minutes(1),
        statistic: 'Sum',
      }),
      threshold: props.throttleThreshold ?? 10,
      evaluationPeriods: evaluationPeriods,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });

    this.allAlarms = [this.errorAlarm, this.latencyAlarm, this.throttleAlarm];
  }
}
```

These alarms monitor the alias (which receives production traffic), not the function directly. This ensures we're measuring the actual user experience during canary deployment.

## Step 3: Configure CodeDeploy Deployment Group

CodeDeploy manages the traffic shifting between Lambda versions. It supports multiple deployment strategies.

### Deployment Configuration Options

```typescript
// lib/constructs/canary-deployment.ts
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as codedeploy from 'aws-cdk-lib/aws-codedeploy';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import { Construct } from 'constructs';

// Available deployment configurations
export enum CanaryDeploymentConfig {
  // Canary: Deploy to small percentage, wait, then 100%
  CANARY_10_PERCENT_5_MINUTES = 'CANARY_10PERCENT_5MINUTES',
  CANARY_10_PERCENT_10_MINUTES = 'CANARY_10PERCENT_10MINUTES',
  CANARY_10_PERCENT_15_MINUTES = 'CANARY_10PERCENT_15MINUTES',
  
  // Linear: Gradually increase traffic at fixed intervals
  LINEAR_10_PERCENT_EVERY_1_MINUTE = 'LINEAR_10PERCENT_EVERY_1MINUTE',
  LINEAR_10_PERCENT_EVERY_2_MINUTES = 'LINEAR_10PERCENT_EVERY_2MINUTES',
  LINEAR_10_PERCENT_EVERY_3_MINUTES = 'LINEAR_10PERCENT_EVERY_3MINUTES',
  LINEAR_10_PERCENT_EVERY_10_MINUTES = 'LINEAR_10PERCENT_EVERY_10MINUTES',
  
  // All at once (not recommended for production)
  ALL_AT_ONCE = 'ALL_AT_ONCE',
}

export interface CanaryDeploymentProps {
  alias: lambda.Alias;
  deploymentConfig: CanaryDeploymentConfig;
  alarms: cloudwatch.Alarm[];
  applicationName?: string;
  deploymentGroupName?: string;
}

export class CanaryDeployment extends Construct {
  public readonly application: codedeploy.LambdaApplication;
  public readonly deploymentGroup: codedeploy.LambdaDeploymentGroup;

  constructor(scope: Construct, id: string, props: CanaryDeploymentProps) {
    super(scope, id);

    // Create CodeDeploy application
    this.application = new codedeploy.LambdaApplication(this, 'Application', {
      applicationName: props.applicationName,
    });

    // Map deployment config enum to CDK deployment config
    const deploymentConfig = this.getDeploymentConfig(props.deploymentConfig);

    // Create deployment group with automatic rollback
    this.deploymentGroup = new codedeploy.LambdaDeploymentGroup(this, 'DeploymentGroup', {
      application: this.application,
      deploymentGroupName: props.deploymentGroupName,
      alias: props.alias,
      deploymentConfig: deploymentConfig,
      
      // Attach alarms for automatic rollback
      alarms: props.alarms,
      
      // Auto-rollback on deployment failure or alarm breach
      autoRollback: {
        failedDeployment: true,
        stoppedDeployment: true,
        deploymentInAlarm: true,
      },
    });
  }

  private getDeploymentConfig(
    config: CanaryDeploymentConfig
  ): codedeploy.ILambdaDeploymentConfig {
    switch (config) {
      case CanaryDeploymentConfig.CANARY_10_PERCENT_5_MINUTES:
        return codedeploy.LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES;
      case CanaryDeploymentConfig.CANARY_10_PERCENT_10_MINUTES:
        return codedeploy.LambdaDeploymentConfig.CANARY_10PERCENT_10MINUTES;
      case CanaryDeploymentConfig.CANARY_10_PERCENT_15_MINUTES:
        return codedeploy.LambdaDeploymentConfig.CANARY_10PERCENT_15MINUTES;
      case CanaryDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE:
        return codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE;
      case CanaryDeploymentConfig.LINEAR_10_PERCENT_EVERY_2_MINUTES:
        return codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_2MINUTES;
      case CanaryDeploymentConfig.LINEAR_10_PERCENT_EVERY_3_MINUTES:
        return codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_3MINUTES;
      case CanaryDeploymentConfig.LINEAR_10_PERCENT_EVERY_10_MINUTES:
        return codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_10MINUTES;
      case CanaryDeploymentConfig.ALL_AT_ONCE:
        return codedeploy.LambdaDeploymentConfig.ALL_AT_ONCE;
      default:
        return codedeploy.LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES;
    }
  }
}
```

### Deployment Config Comparison

| Config | Traffic Shift | Total Time | Use Case |
|--------|---------------|------------|----------|
| CANARY_10PERCENT_5MINUTES | 10% → 100% | 5 min | Quick validation |
| CANARY_10PERCENT_10MINUTES | 10% → 100% | 10 min | Standard production |
| LINEAR_10PERCENT_EVERY_1MINUTE | 10% increments | 10 min | Gradual rollout |
| LINEAR_10PERCENT_EVERY_10MINUTES | 10% increments | 100 min | High-risk changes |

## Step 4: Complete CDK Stack

Combine all components into a production-ready deployment stack.

```typescript
// lib/stacks/canary-deployment-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as codedeploy from 'aws-cdk-lib/aws-codedeploy';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import { Construct } from 'constructs';
import { VersionedLambda } from '../constructs/versioned-lambda';
import { DeploymentAlarms } from '../constructs/deployment-alarms';
import { CanaryDeployment, CanaryDeploymentConfig } from '../constructs/canary-deployment';

export interface CanaryDeploymentStackProps extends cdk.StackProps {
  stage: string;
  serviceName: string;
  codePath: string;
  deploymentConfig?: CanaryDeploymentConfig;
  errorRateThreshold?: number;
  latencyP99Threshold?: number;
}

export class CanaryDeploymentStack extends cdk.Stack {
  public readonly lambdaFunction: lambda.Function;
  public readonly alias: lambda.Alias;
  public readonly deploymentGroup: codedeploy.LambdaDeploymentGroup;

  constructor(scope: Construct, id: string, props: CanaryDeploymentStackProps) {
    super(scope, id, props);

    const alarmPrefix = `${props.serviceName}-${props.stage}`;

    // Create versioned Lambda
    const versionedLambda = new VersionedLambda(this, 'ApiHandler', {
      functionName: `${props.serviceName}-api-${props.stage}`,
      description: `${props.serviceName} API handler`,
      codePath: props.codePath,
      handler: 'bootstrap',
      runtime: lambda.Runtime.PROVIDED_AL2023,
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
      environment: {
        STAGE: props.stage,
        SERVICE_NAME: props.serviceName,
      },
    });

    this.lambdaFunction = versionedLambda.function;
    this.alias = versionedLambda.alias;

    // Create deployment alarms
    const alarms = new DeploymentAlarms(this, 'Alarms', {
      lambdaFunction: this.lambdaFunction,
      alias: this.alias,
      alarmNamePrefix: alarmPrefix,
      errorRateThreshold: props.errorRateThreshold,
      latencyP99Threshold: props.latencyP99Threshold,
    });

    // Determine deployment config based on stage
    const deploymentConfig = props.deploymentConfig ?? 
      (props.stage === 'prod' 
        ? CanaryDeploymentConfig.CANARY_10_PERCENT_10_MINUTES
        : CanaryDeploymentConfig.ALL_AT_ONCE);

    // Create canary deployment group
    const canaryDeployment = new CanaryDeployment(this, 'CanaryDeploy', {
      alias: this.alias,
      deploymentConfig: deploymentConfig,
      alarms: alarms.allAlarms,
      applicationName: `${props.serviceName}-${props.stage}`,
      deploymentGroupName: `${props.serviceName}-${props.stage}-dg`,
    });

    this.deploymentGroup = canaryDeployment.deploymentGroup;

    // Outputs
    new cdk.CfnOutput(this, 'FunctionName', {
      value: this.lambdaFunction.functionName,
    });

    new cdk.CfnOutput(this, 'AliasArn', {
      value: this.alias.functionArn,
    });

    new cdk.CfnOutput(this, 'CurrentVersion', {
      value: versionedLambda.currentVersion.version,
    });

    new cdk.CfnOutput(this, 'DeploymentGroupName', {
      value: this.deploymentGroup.deploymentGroupName,
    });
  }
}
```

### CDK App Entry Point

```typescript
// bin/app.ts
#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CanaryDeploymentStack } from '../lib/stacks/canary-deployment-stack';
import { CanaryDeploymentConfig } from '../lib/constructs/canary-deployment';

const app = new cdk.App();

const stage = app.node.tryGetContext('stage') || 'dev';
const serviceName = 'my-service';

new CanaryDeploymentStack(app, `${serviceName}-${stage}`, {
  stage: stage,
  serviceName: serviceName,
  codePath: '../dist/api',
  deploymentConfig: stage === 'prod' 
    ? CanaryDeploymentConfig.CANARY_10_PERCENT_10_MINUTES
    : CanaryDeploymentConfig.ALL_AT_ONCE,
  errorRateThreshold: 10,
  latencyP99Threshold: 5000,
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || 'eu-west-1',
  },
});
```

## Step 5: Test Rollback Scenarios

Implement scripts and procedures for testing rollback behavior.

### Metrics Check Script

```bash
#!/bin/bash
# scripts/check-metrics.sh
# Validates Lambda metrics for canary deployment health

set -euo pipefail

SERVICE=$1
STAGE=$2
FUNCTION_NAME="${SERVICE}-api-${STAGE}"
ALIAS_NAME="live"

echo "Checking metrics for ${FUNCTION_NAME}:${ALIAS_NAME}..."

# Time range: last 5 minutes
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_TIME=$(date -u -v-5M +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || \
             date -u -d "5 minutes ago" +"%Y-%m-%dT%H:%M:%SZ")

# Get error count
ERRORS=$(aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=$FUNCTION_NAME Name=Resource,Value="${FUNCTION_NAME}:${ALIAS_NAME}" \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --period 300 \
  --statistics Sum \
  --query 'Datapoints[0].Sum' \
  --output text 2>/dev/null || echo "0")

# Get invocation count  
INVOCATIONS=$(aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=$FUNCTION_NAME Name=Resource,Value="${FUNCTION_NAME}:${ALIAS_NAME}" \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --period 300 \
  --statistics Sum \
  --query 'Datapoints[0].Sum' \
  --output text 2>/dev/null || echo "1")

# Get P99 duration
DURATION_P99=$(aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=$FUNCTION_NAME Name=Resource,Value="${FUNCTION_NAME}:${ALIAS_NAME}" \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --period 300 \
  --extended-statistics p99 \
  --query 'Datapoints[0].ExtendedStatistics.p99' \
  --output text 2>/dev/null || echo "0")

# Handle None values
ERRORS=${ERRORS//None/0}
INVOCATIONS=${INVOCATIONS//None/1}
DURATION_P99=${DURATION_P99//None/0}

# Calculate error rate
if [[ "$INVOCATIONS" != "0" ]]; then
  ERROR_RATE=$(echo "scale=4; $ERRORS / $INVOCATIONS" | bc)
else
  ERROR_RATE="0"
fi

echo "=========================================="
echo "Errors:       $ERRORS"
echo "Invocations:  $INVOCATIONS"
echo "Error Rate:   $ERROR_RATE"
echo "P99 Duration: ${DURATION_P99}ms"
echo "=========================================="

# Validate against thresholds
FAILED=0

if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
  echo "❌ FAIL: Error rate $ERROR_RATE > 1%"
  FAILED=1
fi

if (( $(echo "$DURATION_P99 > 5000" | bc -l) )); then
  echo "❌ FAIL: P99 latency ${DURATION_P99}ms > 5000ms"
  FAILED=1
fi

if [[ $FAILED -eq 1 ]]; then
  echo ""
  echo "Metrics validation FAILED - rollback recommended"
  exit 1
fi

echo "✅ PASS: All metrics within thresholds"
exit 0
```

### Manual Rollback Commands

```bash
#!/bin/bash
# scripts/rollback.sh
# Manually rollback to previous Lambda version

set -euo pipefail

SERVICE=$1
STAGE=$2
FUNCTION_NAME="${SERVICE}-api-${STAGE}"
ALIAS_NAME="live"

echo "Rolling back ${FUNCTION_NAME}..."

# Get previous version (second to last)
PREVIOUS_VERSION=$(aws lambda list-versions-by-function \
  --function-name "$FUNCTION_NAME" \
  --query 'Versions[-2].Version' \
  --output text)

if [[ "$PREVIOUS_VERSION" == "None" || "$PREVIOUS_VERSION" == "\$LATEST" ]]; then
  echo "Error: No previous version found to rollback to"
  exit 1
fi

echo "Rolling back to version: $PREVIOUS_VERSION"

# Update alias to point to previous version (100% traffic)
aws lambda update-alias \
  --function-name "$FUNCTION_NAME" \
  --name "$ALIAS_NAME" \
  --function-version "$PREVIOUS_VERSION" \
  --routing-config 'AdditionalVersionWeights={}'

echo "✅ Rollback complete. Alias now points to version $PREVIOUS_VERSION"

# Verify
CURRENT=$(aws lambda get-alias \
  --function-name "$FUNCTION_NAME" \
  --name "$ALIAS_NAME" \
  --query 'FunctionVersion' \
  --output text)

echo "Current alias version: $CURRENT"
```

### Stop In-Progress Deployment

```bash
#!/bin/bash
# scripts/stop-deployment.sh
# Stop an in-progress CodeDeploy deployment

set -euo pipefail

SERVICE=$1
STAGE=$2
APPLICATION_NAME="${SERVICE}-${STAGE}"
DEPLOYMENT_GROUP="${SERVICE}-${STAGE}-dg"

# Get current deployment ID
DEPLOYMENT_ID=$(aws deploy list-deployments \
  --application-name "$APPLICATION_NAME" \
  --deployment-group-name "$DEPLOYMENT_GROUP" \
  --include-only-statuses "InProgress" \
  --query 'deployments[0]' \
  --output text)

if [[ "$DEPLOYMENT_ID" == "None" ]]; then
  echo "No in-progress deployment found"
  exit 0
fi

echo "Stopping deployment: $DEPLOYMENT_ID"

aws deploy stop-deployment \
  --deployment-id "$DEPLOYMENT_ID" \
  --auto-rollback-enabled

echo "✅ Deployment stopped and rollback initiated"
```

## Step 6: Monitor Canary Metrics

Create a CloudWatch dashboard for monitoring canary deployments in real-time.

```typescript
// lib/constructs/canary-dashboard.ts
import * as cdk from 'aws-cdk-lib';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export interface CanaryDashboardProps {
  dashboardName: string;
  lambdaFunction: lambda.Function;
  alias: lambda.Alias;
}

export class CanaryDashboard extends Construct {
  public readonly dashboard: cloudwatch.Dashboard;

  constructor(scope: Construct, id: string, props: CanaryDashboardProps) {
    super(scope, id);

    this.dashboard = new cloudwatch.Dashboard(this, 'Dashboard', {
      dashboardName: props.dashboardName,
    });

    // Error rate widget
    this.dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'Error Rate',
        left: [
          props.alias.metricErrors({
            period: cdk.Duration.minutes(1),
            statistic: 'Sum',
            label: 'Errors',
          }),
        ],
        right: [
          props.alias.metricInvocations({
            period: cdk.Duration.minutes(1),
            statistic: 'Sum',
            label: 'Invocations',
          }),
        ],
        width: 12,
      }),
      new cloudwatch.GraphWidget({
        title: 'Latency (P50, P90, P99)',
        left: [
          props.alias.metricDuration({
            period: cdk.Duration.minutes(1),
            statistic: 'p50',
            label: 'P50',
          }),
          props.alias.metricDuration({
            period: cdk.Duration.minutes(1),
            statistic: 'p90',
            label: 'P90',
          }),
          props.alias.metricDuration({
            period: cdk.Duration.minutes(1),
            statistic: 'p99',
            label: 'P99',
          }),
        ],
        width: 12,
      })
    );

    // Throttles and concurrent executions
    this.dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'Throttles',
        left: [
          props.alias.metricThrottles({
            period: cdk.Duration.minutes(1),
            statistic: 'Sum',
          }),
        ],
        width: 8,
      }),
      new cloudwatch.GraphWidget({
        title: 'Concurrent Executions',
        left: [
          props.lambdaFunction.metric('ConcurrentExecutions', {
            period: cdk.Duration.minutes(1),
            statistic: 'Maximum',
          }),
        ],
        width: 8,
      }),
      new cloudwatch.SingleValueWidget({
        title: 'Current Error Rate',
        metrics: [
          props.alias.metricErrors({
            period: cdk.Duration.minutes(5),
            statistic: 'Sum',
          }),
        ],
        width: 8,
      })
    );
  }
}
```

## Makefile Targets

Add deployment targets to your Makefile for easy canary operations.

```makefile
# Makefile for canary deployment operations

SERVICE_NAME := my-service
STAGE ?= dev
CDK_DIR := deploy/cdk
VERSION ?= $(shell git describe --tags --always)

.PHONY: deploy deploy-canary promote rollback check-metrics stop-deployment

# Standard deployment (uses stage-appropriate config)
deploy: build
	@echo "Deploying $(SERVICE_NAME) to $(STAGE)..."
	cd $(CDK_DIR) && cdk deploy --context stage=$(STAGE) --require-approval never

# Deploy with specific canary weight (0.1 = 10%, 0.5 = 50%)
deploy-canary: build
ifndef WEIGHT
	$(error WEIGHT is required, e.g., make deploy-canary WEIGHT=0.1)
endif
	@echo "Deploying canary at $(WEIGHT) weight..."
	cd $(CDK_DIR) && CANARY_WEIGHT=$(WEIGHT) cdk deploy --context stage=$(STAGE)

# Promote canary to 100%
promote:
	@echo "Promoting $(SERVICE_NAME) to 100% in $(STAGE)..."
	./scripts/promote.sh $(SERVICE_NAME) $(STAGE)

# Rollback to previous version
rollback:
	@echo "Rolling back $(SERVICE_NAME) in $(STAGE)..."
	./scripts/rollback.sh $(SERVICE_NAME) $(STAGE)

# Check deployment metrics
check-metrics:
	@./scripts/check-metrics.sh $(SERVICE_NAME) $(STAGE)

# Stop in-progress deployment
stop-deployment:
	@./scripts/stop-deployment.sh $(SERVICE_NAME) $(STAGE)

# Build Lambda binary
build:
	GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build -o bootstrap ./cmd/api
	zip -j dist/api.zip bootstrap
	rm bootstrap
```

## Verification Checklist

After setting up canary deployments, verify:

- [ ] Lambda function publishes new version on each deployment
- [ ] Alias "live" exists and points to current version
- [ ] CloudWatch alarms configured for errors, latency, and throttles
- [ ] CodeDeploy deployment group created with correct config
- [ ] Alarms attached to deployment group for auto-rollback
- [ ] autoRollback enabled for failedDeployment and deploymentInAlarm
- [ ] Metrics check script validates error rate < 1%
- [ ] Metrics check script validates P99 latency < 5000ms
- [ ] Manual rollback script updates alias to previous version
- [ ] Stop deployment script halts in-progress deployments
- [ ] Dashboard shows real-time canary metrics
- [ ] Makefile has deploy, rollback, and check-metrics targets
- [ ] Different deployment configs used per environment (ALL_AT_ONCE for dev, CANARY for prod)
