---
name: aws-cloudformation-cloudwatch
description: AWS CloudFormation patterns for CloudWatch monitoring, metrics, alarms, dashboards, logs, and observability. Use when creating CloudWatch metrics, alarms, dashboards, log groups, log subscriptions, anomaly detection, synthesized canaries, Application Signals, and implementing template structure with Parameters, Outputs, Mappings, Conditions, cross-stack references, and CloudWatch best practices for monitoring production infrastructure.
category: aws
tags: [aws, cloudformation, cloudwatch, monitoring, observability, metrics, alarms, logs, dashboards, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation CloudWatch Monitoring

## Overview

Create production-ready monitoring and observability infrastructure using AWS CloudFormation templates. This skill covers CloudWatch metrics, alarms, dashboards, log groups, log insights, anomaly detection, synthesized canaries, Application Signals, and best practices for parameters, outputs, and cross-stack references.

## When to Use

Use this skill when:
- Creating custom CloudWatch metrics
- Configuring CloudWatch alarms for thresholds and anomaly detection
- Creating CloudWatch dashboards for multi-region visualization
- Implementing log groups with retention and encryption
- Configuring log subscriptions and cross-account log aggregation
- Implementing synthesized canaries for synthetic monitoring
- Enabling Application Signals for application performance monitoring
- Organizing templates with Parameters, Outputs, Mappings, Conditions
- Implementing cross-stack references with export/import
- Using Transform for macros and reuse

## CloudFormation Template Structure

### Base Template with Standard Format

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch monitoring and observability stack

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Monitoring Configuration
        Parameters:
          - Environment
          - LogRetentionDays
          - EnableAnomalyDetection
      - Label:
          default: Alarm Thresholds
        Parameters:
          - ErrorRateThreshold
          - LatencyThreshold
          - CpuUtilizationThreshold

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production
    Description: Deployment environment

  LogRetentionDays:
    Type: Number
    Default: 30
    AllowedValues:
      - 1
      - 3
      - 5
      - 7
      - 14
      - 30
      - 60
      - 90
      - 120
      - 150
      - 180
      - 365
      - 400
      - 545
      - 731
      - 1095
      - 1827
      - 2190
      - 2555
      - 2922
      - 3285
      - 3650
    Description: Number of days to retain log events

  EnableAnomalyDetection:
    Type: String
    Default: false
    AllowedValues:
      - true
      - false
    Description: Enable CloudWatch anomaly detection

  ErrorRateThreshold:
    Type: Number
    Default: 5
    Description: Error rate threshold for alarms (percentage)

  LatencyThreshold:
    Type: Number
    Default: 1000
    Description: Latency threshold in milliseconds

  CpuUtilizationThreshold:
    Type: Number
    Default: 80
    Description: CPU utilization threshold (percentage)

Mappings:
  EnvironmentConfig:
    dev:
      LogRetentionDays: 7
      ErrorRateThreshold: 10
      LatencyThreshold: 2000
      CpuUtilizationThreshold: 90
    staging:
      LogRetentionDays: 14
      ErrorRateThreshold: 5
      LatencyThreshold: 1500
      CpuUtilizationThreshold: 85
    production:
      LogRetentionDays: 30
      ErrorRateThreshold: 1
      LatencyThreshold: 500
      CpuUtilizationThreshold: 80

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  IsStaging: !Equals [!Ref Environment, staging]
  EnableAnomaly: !Equals [!Ref EnableAnomalyDetection, true]

Transform:
  - AWS::Serverless-2016-10-31

Resources:
  # Log Group per applicazione
  ApplicationLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/applications/${Environment}/application"
      RetentionInDays: !Ref LogRetentionDays
      KmsKeyId: !Ref LogKmsKey
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName

Outputs:
  LogGroupName:
    Description: Name of the application log group
    Value: !Ref ApplicationLogGroup
    Export:
      Name: !Sub "${AWS::StackName}-LogGroupName"
```

## Parameters Best Practices

### AWS-Specific Parameter Types

```yaml
Parameters:
  # AWS-specific types for validation
  CloudWatchNamespace:
    Type: AWS::CloudWatch::Namespace
    Description: CloudWatch metric namespace

  AlarmActionArn:
    Type: AWS::SNS::Topic::Arn
    Description: SNS topic ARN for alarm actions

  LogKmsKeyArn:
    Type: AWS::KMS::Key::Arn
    Description: KMS key ARN for log encryption

  DashboardArn:
    Type: AWS::CloudWatch::Dashboard::Arn
    Description: Existing dashboard ARN to import

  AnomalyDetectorArn:
    Type: AWS::CloudWatch::AnomalyDetector::Arn
    Description: Existing anomaly detector ARN
```

### Parameter Constraints

```yaml
Parameters:
  MetricName:
    Type: String
    Description: CloudWatch metric name
    ConstraintDescription: Must be 1-256 characters, alphanumeric, underscore, period, dash
    MinLength: 1
    MaxLength: 256
    AllowedPattern: "[a-zA-Z0-9._-]+"

  ThresholdValue:
    Type: Number
    Description: Alarm threshold value
    MinValue: 0
    MaxValue: 1000000000

  EvaluationPeriods:
    Type: Number
    Description: Number of evaluation periods
    Default: 5
    MinValue: 1
    MaxValue: 100
    ConstraintDescription: Must be between 1 and 100

  DatapointsToAlarm:
    Type: Number
    Description: Datapoints that must breach to trigger alarm
    Default: 5
    MinValue: 1
    MaxValue: 10

  Period:
    Type: Number
    Description: Metric period in seconds
    Default: 300
    AllowedValues:
      - 10
      - 30
      - 60
      - 300
      - 900
      - 3600
      - 21600
      - 86400

  ComparisonOperator:
    Type: String
    Description: Alarm comparison operator
    Default: GreaterThanThreshold
    AllowedValues:
      - GreaterThanThreshold
      - GreaterThanOrEqualToThreshold
      - LessThanThreshold
      - LessThanOrEqualToThreshold
      - GreaterThanUpperBound
      - LessThanLowerBound
```

### SSM Parameter References

```yaml
Parameters:
  AlarmTopicArn:
    Type: AWS::SSM::Parameter::Value<AWS::SNS::Topic::Arn>
    Default: /monitoring/alarms/topic-arn
    Description: SNS topic ARN from SSM Parameter Store

  DashboardConfig:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /monitoring/dashboards/config
    Description: Dashboard configuration from SSM
```

## Outputs and Cross-Stack References

### Export/Import Patterns

```yaml
# Stack A - Monitoring Stack
AWSTemplateFormatVersion: 2010-09-09
Description: Central monitoring infrastructure stack

Resources:
  AlarmTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${AWS::StackName}-alarms"
      DisplayName: !Sub "${AWS::StackName} Alarm Notifications"

  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/monitoring/${AWS::StackName}"
      RetentionInDays: 30

Outputs:
  AlarmTopicArn:
    Description: ARN of the alarm SNS topic
    Value: !Ref AlarmTopic
    Export:
      Name: !Sub "${AWS::StackName}-AlarmTopicArn"

  LogGroupName:
    Description: Name of the log group
    Value: !Ref LogGroup
    Export:
      Name: !Sub "${AWS::StackName}-LogGroupName"

  LogGroupArn:
    Description: ARN of the log group
    Value: !GetAtt LogGroup.Arn
    Export:
      Name: !Sub "${AWS::StackName}-LogGroupArn"
```

```yaml
# Stack B - Application Stack (imports from Monitoring Stack)
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack with monitoring integration

Parameters:
  MonitoringStackName:
    Type: String
    Description: Name of the monitoring stack

Resources:
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-processor"
      Runtime: python3.11
      Handler: app.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/function.zip
      Role: !GetAtt LambdaExecutionRole.Arn

  ErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-errors"
      AlarmDescription: Alert on Lambda errors
      MetricName: Errors
      Namespace: AWS/Lambda
      Dimensions:
        - Name: FunctionName
          Value: !Ref LambdaFunction
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 5
      Threshold: 1
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !ImportValue
          !Sub "${MonitoringStackName}-AlarmTopicArn"

  HighLatencyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-latency"
      AlarmDescription: Alert on high latency
      MetricName: Duration
      Namespace: AWS/Lambda
      Dimensions:
        - Name: FunctionName
          Value: !Ref LambdaFunction
      Statistic: P99
      Period: 60
      EvaluationPeriods: 3
      Threshold: 5000
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !ImportValue
          !Sub "${MonitoringStackName}-AlarmTopicArn"
```

### Nested Stacks for Modularity

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Main stack with nested monitoring stacks

Resources:
  # Nested stack for alarms
  AlarmsStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/monitoring/alarms.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        AlarmTopicArn: !Ref AlarmTopicArn

  # Nested stack for dashboards
  DashboardsStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/monitoring/dashboards.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        LogGroupNames: !Join [",", [!GetAtt AlarmsStack.Outputs.LogGroupName]]

  # Nested stack for log insights
  LogInsightsStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/monitoring/log-insights.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
```

## CloudWatch Metrics and Alarms

### Base Metric Alarm

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch metric alarms

Resources:
  # Error rate alarm
  ErrorRateAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-error-rate"
      AlarmDescription: Alert when error rate exceeds threshold
      MetricName: ErrorRate
      Namespace: !Ref CustomNamespace
      Dimensions:
        - Name: Service
          Value: !Ref ServiceName
        - Name: Environment
          Value: !Ref Environment
      Statistic: Average
      Period: 60
      EvaluationPeriods: 5
      DatapointsToAlarm: 3
      Threshold: !Ref ErrorRateThreshold
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref AlarmTopic
      InsufficientDataActions:
        - !Ref AlarmTopic
      OKActions:
        - !Ref AlarmTopic
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Severity
          Value: high

  # P99 latency alarm
  LatencyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-p99-latency"
      AlarmDescription: Alert when P99 latency exceeds threshold
      MetricName: Latency
      Namespace: !Ref CustomNamespace
      Dimensions:
        - Name: Service
          Value: !Ref ServiceName
      Statistic: p99
      ExtendedStatistic: "p99"
      Period: 60
      EvaluationPeriods: 3
      Threshold: !Ref LatencyThreshold
      ComparisonOperator: GreaterThanThreshold
      TreatMissingData: notBreaching
      AlarmActions:
        - !Ref AlarmTopic

  # 4xx errors alarm
  ClientErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-4xx-errors"
      AlarmDescription: Alert on high 4xx error rate
      MetricName: 4XXError
      Namespace: AWS/ApiGateway
      Dimensions:
        - Name: ApiName
          Value: !Ref ApiName
        - Name: Stage
          Value: !Ref StageName
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 100
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref AlarmTopic

  # 5xx errors alarm
  ServerErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-5xx-errors"
      AlarmDescription: Alert on high 5xx error rate
      MetricName: 5XXError
      Namespace: AWS/ApiGateway
      Dimensions:
        - Name: ApiName
          Value: !Ref ApiName
        - Name: Stage
          Value: !Ref StageName
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 2
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold
      ComparisonOperator: GreaterThanOrEqualToThreshold
      AlarmActions:
        - !Ref AlarmTopic
```

### Composite Alarm

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch composite alarms

Resources:
  # Base alarm for Lambda errors
  LambdaErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-lambda-errors"
      MetricName: Errors
      Namespace: AWS/Lambda
      Dimensions:
        - Name: FunctionName
          Value: !Ref LambdaFunction
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 5
      Threshold: 5
      ComparisonOperator: GreaterThanThreshold

  # Base alarm for Lambda throttles
  LambdaThrottleAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-lambda-throttles"
      MetricName: Throttles
      Namespace: AWS/Lambda
      Dimensions:
        - Name: FunctionName
          Value: !Ref LambdaFunction
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 5
      Threshold: 3
      ComparisonOperator: GreaterThanThreshold

  # Composite alarm combining both
  LambdaHealthCompositeAlarm:
    Type: AWS::CloudWatch::CompositeAlarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-lambda-health"
      AlarmDescription: Composite alarm for Lambda function health
      AlarmRule: !Or
        - !Ref LambdaErrorAlarm
        - !Ref LambdaThrottleAlarm
      ActionsEnabled: true
      AlarmActions:
        - !Ref AlarmTopic
      Tags:
        - Key: Service
          Value: lambda
        - Key: Tier
          Value: application
```

### Anomaly Detection Alarm

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch anomaly detection

Resources:
  # Anomaly detector for metric
  RequestRateAnomalyDetector:
    Type: AWS::CloudWatch::AnomalyDetector
    Properties:
      MetricName: RequestCount
      Namespace: !Ref CustomNamespace
      Dimensions:
        - Name: Service
          Value: !Ref ServiceName
        - Name: Environment
          Value: !Ref Environment
      Statistic: Sum
      Configuration:
        ExcludedTimeRanges:
          - StartTime: "2023-12-25T00:00:00"
            EndTime: "2023-12-26T00:00:00"
        MetricTimeZone: UTC

  # Alarm based on anomaly detection
  AnomalyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-anomaly-detection"
      AlarmDescription: Alert on anomalous metric behavior
      MetricName: RequestCount
      Namespace: !Ref CustomNamespace
      Dimensions:
        - Name: Service
          Value: !Ref ServiceName
      AnomalyDetectorConfiguration:
        ExcludeTimeRange:
          StartTime: "2023-12-25T00:00:00"
          EndTime: "2023-12-26T00:00:00"
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 2
      ComparisonOperator: GreaterThanUpperThreshold
      AlarmActions:
        - !Ref AlarmTopic

  # Alarm for low anomalous value
  LowTrafficAnomalyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-low-traffic"
      AlarmDescription: Alert on unusually low traffic
      MetricName: RequestCount
      Namespace: !Ref CustomNamespace
      Dimensions:
        - Name: Service
          Value: !Ref ServiceName
      AnomalyDetectorConfiguration:
        Bound: Lower
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 3
      Threshold: 0.5
      ComparisonOperator: LessThanLowerThreshold
      AlarmActions:
        - !Ref AlarmTopic
```

## CloudWatch Dashboards

### Dashboard Base

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch dashboard

Resources:
  # Main dashboard
  MainDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: !Sub "${AWS::StackName}-main"
      DashboardBody: !Sub |
        {
          "widgets": [
            {
              "type": "metric",
              "x": 0,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "title": "API Gateway Requests",
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "metrics": [
                  ["AWS/ApiGateway", "Count", "ApiName", "${ApiName}", "Stage", "${StageName}"],
                  [".", "4XXError", ".", ".", ".", "."],
                  [".", "5XXError", ".", ".", ".", "."]
                ],
                "period": 300,
                "stat": "Sum"
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "title": "API Gateway Latency",
                "view": "timeSeries",
                "region": "${AWS::Region}",
                "metrics": [
                  ["AWS/ApiGateway", "Latency", "ApiName", "${ApiName}", "Stage", "${StageName}", {"stat": "p99"}],
                  [".", ".", ".", ".", ".", ".", {"stat": "Average"}]
                ],
                "period": 300
              }
            },
            {
              "type": "metric",
              "x": 0,
              "y": 6,
              "width": 12,
              "height": 6,
              "properties": {
                "title": "Lambda Invocations",
                "view": "timeSeries",
                "region": "${AWS::Region}",
                "metrics": [
                  ["AWS/Lambda", "Invocations", "FunctionName", "${LambdaFunction}"],
                  [".", "Errors", ".", "."],
                  [".", "Throttles", ".", "."]
                ],
                "period": 60,
                "stat": "Sum"
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 6,
              "width": 12,
              "height": 6,
              "properties": {
                "title": "Lambda Duration",
                "view": "timeSeries",
                "region": "${AWS::Region}",
                "metrics": [
                  ["AWS/Lambda", "Duration", "FunctionName", "${LambdaFunction}", {"stat": "p99"}],
                  [".", ".", ".", ".", {"stat": "Average"}],
                  [".", ".", ".", ".", {"stat": "Maximum"}]
                ],
                "period": 60
              }
            },
            {
              "type": "log",
              "x": 0,
              "y": 12,
              "width": 24,
              "height": 6,
              "properties": {
                "title": "Application Logs",
                "view": "table",
                "region": "${AWS::Region}",
                "logGroupName": "${ApplicationLogGroup}",
                "timeRange": {
                  "type": "relative",
                  "from": 3600
                },
                "filterPattern": "ERROR | WARN"
              }
            }
          ]
        }

  # Dashboard for specific service
  ServiceDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: !Sub "${AWS::StackName}-${ServiceName}"
      DashboardBody: !Sub |
        {
          "start": "-PT6H",
          "widgets": [
            {
              "type": "text",
              "x": 0,
              "y": 0,
              "width": 24,
              "height": 1,
              "properties": {
                "markdown": "# ${ServiceName} - ${Environment} Dashboard"
              }
            },
            {
              "type": "metric",
              "x": 0,
              "y": 1,
              "width": 8,
              "height": 6,
              "properties": {
                "title": "Request Rate",
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "metrics": [
                  ["${CustomNamespace}", "RequestCount", "Service", "${ServiceName}", "Environment", "${Environment}"]
                ],
                "period": 60,
                "stat": "Sum"
              }
            },
            {
              "type": "metric",
              "x": 8,
              "y": 1,
              "width": 8,
              "height": 6,
              "properties": {
                "title": "Error Rate %",
                "view": "timeSeries",
                "region": "${AWS::Region}",
                "metrics": [
                  ["${CustomNamespace}", "ErrorCount", "Service", "${ServiceName}"],
                  [".", "RequestCount", ".", "."],
                  [".", "SuccessCount", ".", "."]
                ],
                "period": 60,
                "stat": "Average"
              }
            },
            {
              "type": "metric",
              "x": 16,
              "y": 1,
              "width": 8,
              "height": 6,
              "properties": {
                "title": "P99 Latency",
                "view": "timeSeries",
                "region": "${AWS::Region}",
                "metrics": [
                  ["${CustomNamespace}", "Latency", "Service", "${ServiceName}"]
                ],
                "period": 60,
                "stat": "p99"
              }
            }
          ]
        }
```

## CloudWatch Logs

### Log Group Configurations

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch log groups configuration

Parameters:
  LogRetentionDays:
    Type: Number
    Default: 30
    AllowedValues:
      - 1
      - 3
      - 5
      - 7
      - 14
      - 30
      - 60
      - 90
      - 120
      - 150
      - 180
      - 365
      - 400
      - 545
      - 731
      - 1095
      - 1827
      - 2190
      - 2555
      - 2922
      - 3285
      - 3650

Resources:
  # Application log group
  ApplicationLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/applications/${Environment}/${ApplicationName}"
      RetentionInDays: !Ref LogRetentionDays
      KmsKeyId: !Ref LogKmsKeyArn
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName
        - Key: Service
          Value: !Ref ServiceName

  # Lambda log group
  LambdaLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/lambda/${LambdaFunctionName}"
      RetentionInDays: !Ref LogRetentionDays
      KmsKeyId: !Ref LogKmsKeyArn

  # Subscription filter for Log Insights
  LogSubscriptionFilter:
    Type: AWS::Logs::SubscriptionFilter
    Properties:
      DestinationArn: !GetAtt LogDestination.Arn
      FilterPattern: '[timestamp=*Z, request_id, level, message]'
      LogGroupName: !Ref ApplicationLogGroup
      RoleArn: !GetAtt LogSubscriptionRole.Arn

  # Metric filter for errors
  ErrorMetricFilter:
    Type: AWS::Logs::MetricFilter
    Properties:
      FilterPattern: '[level="ERROR", msg]'
      LogGroupName: !Ref ApplicationLogGroup
      MetricTransformations:
        - MetricValue: "1"
          MetricNamespace: !Sub "${AWS::StackName}/Application"
          MetricName: ErrorCount
        - MetricValue: "$level"
          MetricNamespace: !Sub "${AWS::StackName}/Application"
          MetricName: LogLevel

  # Metric filter for warnings
  WarningMetricFilter:
    Type: AWS::Logs::MetricFilter
    Properties:
      FilterPattern: '[level="WARN", msg]'
      LogGroupName: !Ref ApplicationLogGroup
      MetricTransformations:
        - MetricValue: "1"
          MetricNamespace: !Sub "${AWS::StackName}/Application"
          MetricName: WarningCount

  # Log group with custom retention
  AuditLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/audit/${Environment}/${ApplicationName}"
      RetentionInDays: 365
      KmsKeyId: !Ref LogKmsKeyArn
```

### Log Insights Query

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch Logs Insights queries

Resources:
  # Query definition for recent errors
  RecentErrorsQuery:
    Type: AWS::Logs::QueryDefinition
    Properties:
      Name: !Sub "${AWS::StackName}-recent-errors"
      QueryString: |
        fields @timestamp, @message
        | sort @timestamp desc
        | limit 100
        | filter @message like /ERROR/
        | display @timestamp, @message, @logStream

  # Query for performance analysis
  PerformanceQuery:
    Type: AWS::Logs::QueryDefinition
    Properties:
      Name: !Sub "${AWS::StackName}-performance"
      QueryString: |
        fields @timestamp, @message, @duration
        | filter @duration > 1000
        | sort @duration desc
        | limit 50
        | display @timestamp, @duration, @message
```

## Synthesized Canaries

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch Synthesized Canaries

Parameters:
  CanarySchedule:
    Type: String
    Default: rate(5 minutes)
    Description: Schedule expression for canary

Resources:
  # Canary for API endpoint
  ApiCanary:
    Type: AWS::Synthetics::Canary
    Properties:
      Name: !Sub "${AWS::StackName}-api-check"
      ArtifactS3Location: !Sub "s3://${ArtifactBucket}/canary/${AWS::StackName}"
      Code:
        S3Bucket: !Ref CanariesCodeBucket
        S3Key: canary/api-check.zip
        Handler: apiCheck.handler
      ExecutionRoleArn: !GetAtt CanaryRole.Arn
      RuntimeVersion: syn-python-selenium-1.1
      Schedule:
        Expression: !Ref CanarySchedule
        DurationInSeconds: 120
      SuccessRetentionPeriodInDays: 31
      FailureRetentionPeriodInDays: 31
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Service
          Value: api

  # Alarm for canary failure
  CanaryFailureAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-canary-failed"
      AlarmDescription: Alert when synthesized canary fails
      MetricName: Failed
      Namespace: AWS/Synthetics
      Dimensions:
        - Name: CanaryName
          Value: !Ref ApiCanary
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 2
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      AlarmActions:
        - !Ref AlarmTopic

  # Alarm for canary latency
  CanaryLatencyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-canary-slow"
      AlarmDescription: Alert when canary latency is high
      MetricName: Duration
      Namespace: AWS/Synthetics
      Dimensions:
        - Name: CanaryName
          Value: !Ref ApiCanary
      Statistic: p99
      Period: 300
      EvaluationPeriods: 3
      Threshold: 5000
      ComparisonOperator: GreaterThanThreshold

  CanaryRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-canary-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: synthetics.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: SyntheticsLeastPrivilege
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - synthetics:DescribeCanaries
                  - synthetics:DescribeCanaryRuns
                  - synthetics:GetCanary
                  - synthetics:ListTagsForResource
                Resource: "*"
              - Effect: Allow
                Action:
                  - synthetics:StartCanary
                  - synthetics:StopCanary
                Resource: !Ref ApiCanary
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                  - logs:DescribeLogStreams
                Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/cw-syn-canary-*"
              - Effect: Allow
                Action:
                  - s3:PutObject
                  - s3:GetObject
                Resource: !Sub "s3://${ArtifactBucket}/canary/${AWS::StackName}/*"
              - Effect: Allow
                Action:
                  - kms:Decrypt
                Resource: !Ref KmsKeyArn
                Condition:
                  StringEquals:
                    kms:ViaService: !Sub "s3.${AWS::Region}.amazonaws.com"
```

## CloudWatch Application Signals

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch Application Signals for APM

Resources:
  # Service level indicator for availability
  AvailabilitySLI:
    Type: AWS::CloudWatch::ServiceLevelObjective
    Properties:
      Name: !Sub "${AWS::StackName}-availability"
      Description: Service level objective for availability
      Monitor:
        MonitorName: !Sub "${AWS::StackName}-monitor"
        MonitorType: AWS_SERVICE_LEVEL_INDICATOR
        ResourceGroup: !Ref ResourceGroup
      SliMetric:
        MetricName: Availability
        Namespace: !Sub "${AWS::StackName}/Application"
        Dimensions:
          - Name: Service
            Value: !Ref ServiceName
      Target:
        ComparisonOperator: GREATER_THAN_OR_EQUAL
        Threshold: 99.9
        Period:
          RollingInterval:
            Count: 1
            TimeUnit: HOUR
      Goal:
        TargetLevel: 99.9

  # Service level indicator for latency
  LatencySLI:
    Type: AWS::CloudWatch::ServiceLevelIndicator
    Properties:
      Name: !Sub "${AWS::StackName}-latency-sli"
      Monitor:
        MonitorName: !Sub "${AWS::StackName}-monitor"
      Metric:
        MetricName: Latency
        Namespace: !Sub "${AWS::StackName}/Application"
        Dimensions:
          - Name: Service
            Value: !Ref ServiceName
      OperationName: GetItem
      AccountId: !Ref AWS::AccountId

  # Monitor for application performance
  ApplicationMonitor:
    Type: AWS::CloudWatch::ApplicationMonitor
    Properties:
      MonitorName: !Sub "${AWS::StackName}-app-monitor"
      MonitorType: CW_MONITOR
      Telemetry:
        - Type: APM
          Config:
            Eps: 100
```

## Conditions and Transform

### Conditions for Environment-Specific Resources

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch with conditional resources

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production
    Description: Deployment environment

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  IsStaging: !Equals [!Ref Environment, staging]
  CreateAnomalyDetection: !Or [!Equals [!Ref Environment, staging], !Equals [!Ref Environment, production]]
  CreateSLI: !Equals [!Ref Environment, production]

Resources:
  # Base alarm for all environments
  BaseAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-errors"
      MetricName: Errors
      Namespace: !Ref CustomNamespace
      Dimensions:
        - Name: Service
          Value: !Ref ServiceName
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 5
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold

  # Alarm with different thresholds for production
  ProductionAlarm:
    Type: AWS::CloudWatch::Alarm
    Condition: IsProduction
    Properties:
      AlarmName: !Sub "${AWS::StackName}-errors-production"
      MetricName: Errors
      Namespace: !Ref CustomNamespace
      Dimensions:
        - Name: Service
          Value: !Ref ServiceName
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 3
      Threshold: 1
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref ProductionAlarmTopic

  # Anomaly detector only for staging and production
  AnomalyDetector:
    Type: AWS::CloudWatch::AnomalyDetector
    Condition: CreateAnomalyDetection
    Properties:
      MetricName: RequestCount
      Namespace: !Ref CustomNamespace
      Dimensions:
        - Name: Service
          Value: !Ref ServiceName
      Statistic: Sum

  # SLI only for production
  ServiceLevelIndicator:
    Type: AWS::CloudWatch::ServiceLevelIndicator
    Condition: CreateSLI
    Properties:
      Name: !Sub "${AWS::StackName}-sli"
      Monitor:
        MonitorName: !Sub "${AWS::StackName}-monitor"
      Metric:
        MetricName: Availability
        Namespace: !Sub "${AWS::StackName}/Application"
```

### Transform for Code Reuse

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31

Description: Using SAM Transform for CloudWatch resources

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11
    Environment:
      Variables:
        LOG_LEVEL: INFO
    LoggingConfiguration:
      LogGroup:
        Name: !Sub "/aws/lambda/${FunctionName}"
        RetentionInDays: 30

Resources:
  # Lambda function with automatic logging
  MonitoredFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-monitored"
      Handler: app.handler
      CodeUri: functions/monitored/
      Policies:
        - PolicyName: LogsLeastPrivilege
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                  - logs:DescribeLogStreams
                  - logs:GetLogEvents
                  - logs:FilterLogEvents
                Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/${AWS::StackName}-*"
              - Effect: Allow
                Action:
                  - logs:DescribeLogGroups
                Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:*"
      Events:
        Api:
          Type: Api
          Properties:
            Path: /health
            Method: get
```

## Best Practices

### Security

- Encrypt log groups with KMS keys
- Use resource-based policies for log access
- Implement cross-account log aggregation with proper IAM
- Configure log retention appropriate for compliance
- Use VPC endpoints for CloudWatch to isolate traffic
- Implement least privilege for IAM roles

### Performance

- Use appropriate metric periods (60s for alarms, 300s for dashboards)
- Implement composite alarms to reduce alarm fatigue
- Use anomaly detection for non-linear patterns
- Configure dashboards with efficient widgets
- Limit retention period for log groups

### Monitoring

- Implement SLI/SLO for service health
- Use multi-region dashboards for global applications
- Configure alarms with proper evaluation periods
- Implement canaries for synthetic monitoring
- Use Application Signals for APM

### Deployment

- Use change sets before deployment
- Test templates with cfn-lint
- Organize stacks by ownership (network, app, data)
- Use nested stacks for modularity
- Implement stack policies for protection

## CloudFormation Best Practices

### Stack Policies

Stack policies protect critical resources from unintentional updates. Use them to prevent modifications to production resources.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CloudWatch stack with protection policies

Resources:
  CriticalAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-critical"
      MetricName: Errors
      Namespace: AWS/Lambda
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 5
      Threshold: 1
      ComparisonOperator: GreaterThanThreshold

Metadata:
  AWS::CloudFormation::StackPolicy:
    Statement:
      - Effect: Deny
        Principal: "*"
        Action:
          - Update:Delete
          - Update:Modify
        Resource: "*"
      - Effect: Allow
        Principal: "*"
        Action:
          - Update:Modify
        Resource: "*"
        Condition:
          StringEquals:
            aws:RequestedOperation:
              - Describe*
              - List*
```

### Termination Protection

Enable termination protection to prevent accidental stack deletion, especially for production monitoring stacks.

**Via Console:**
1. Select the stack
2. Go to Stack actions > Change termination protection
3. Enable termination protection

**Via CLI:**
```bash
aws cloudformation update-termination-protection \
  --stack-name my-monitoring-stack \
  --enable-termination-protection
```

**Via CloudFormation (Stack Set):**
```yaml
Resources:
  MonitoringStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub "https://${BucketName}.s3.amazonaws.com/monitoring.yaml"
      TerminationProtection: true
```

### Drift Detection

Detect when actual infrastructure differs from the CloudFormation template.

**Detect drift on a single stack:**
```bash
aws cloudformation detect-drift \
  --stack-name my-monitoring-stack
```

**Get drift detection status:**
```bash
aws cloudFormation describe-stack-drift-detection-process-status \
  --stack-drift-detection-id <detection-id>
```

**Get resources that have drifted:**
```bash
aws cloudformation list-stack-resources \
  --stack-name my-monitoring-stack \
  --query "StackResourceSummaries[?StackResourceDriftStatus!='IN_SYNC']"
```

**Automation with Lambda:**
```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Automated drift detection scheduler

Resources:
  DriftDetectionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: CloudWatchDrift
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - cloudformation:DetectStackDrift
                  - cloudformation:DescribeStacks
                  - cloudformation:ListStackResources
                Resource: "*"
              - Effect: Allow
                Action:
                  - sns:Publish
                Resource: !Ref AlertTopic

  DriftDetectionFunction:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: python3.11
      Handler: drift_detector.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: functions/drift-detector.zip
      Role: !GetAtt DriftDetectionRole.Arn
      Environment:
        Variables:
          SNS_TOPIC_ARN: !Ref AlertTopic

  DriftDetectionRule:
    Type: AWS::Events::Rule
    Properties:
      ScheduleExpression: "rate(1 day)"
      Targets:
        - Id: DriftDetection
          Arn: !GetAtt DriftDetectionFunction.Arn

  AlertTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${AWS::StackName}-drift-alerts"
```

### Change Sets

Use change sets to preview and review changes before applying them.

**Create change set:**
```bash
aws cloudformation create-change-set \
  --stack-name my-monitoring-stack \
  --template-body file://updated-template.yaml \
  --change-set-name my-changeset \
  --capabilities CAPABILITY_IAM
```

**List change sets:**
```bash
aws cloudformation list-change-sets \
  --stack-name my-monitoring-stack
```

**Describe change set:**
```bash
aws cloudformation describe-change-set \
  --stack-name my-monitoring-stack \
  --change-set-name my-changeset
```

**Execute change set:**
```bash
aws cloudformation execute-change-set \
  --stack-name my-monitoring-stack \
  --change-set-name my-changeset
```

**Pipeline integration:**
```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: CI/CD pipeline for CloudWatch stacks

Resources:
  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      Name: !Sub "${AWS::StackName}-pipeline"
      RoleArn: !GetAtt PipelineRole.Arn
      Stages:
        - Name: Source
          Actions:
            - Name: SourceAction
              ActionTypeId:
                Category: Source
                Owner: AWS
                Provider: CodeCommit
                Version: "1"
              Configuration:
                RepositoryName: !Ref RepositoryName
                BranchName: main
              OutputArtifacts:
                - Name: SourceOutput
        - Name: Validate
          Actions:
            - Name: ValidateTemplate
              ActionTypeId:
                Category: Test
                Owner: AWS
                Provider: CloudFormation
                Version: "1"
              Configuration:
                ActionMode: VALIDATE_ONLY
                TemplatePath: SourceOutput::template.yaml
              InputArtifacts:
                - Name: SourceOutput
        - Name: Review
          Actions:
            - Name: CreateChangeSet
              ActionTypeId:
                Category: Deploy
                Owner: AWS
                Provider: CloudFormation
                Version: "1"
              Configuration:
                ActionMode: CHANGE_SET_REPLACE
                StackName: !Ref StackName
                ChangeSetName: !Sub "${StackName}-changeset"
                TemplatePath: SourceOutput::template.yaml
                Capabilities: CAPABILITY_IAM,CAPABILITY_NAMED_IAM
              InputArtifacts:
                - Name: SourceOutput
            - Name: Approval
              ActionTypeId:
                Category: Approval
                Owner: AWS
                Provider: Manual
                Version: "1"
              Configuration:
                CustomData: Review changes before deployment
        - Name: Deploy
          Actions:
            - Name: ExecuteChangeSet
              ActionTypeId:
                Category: Deploy
                Owner: AWS
                Provider: CloudFormation
                Version: "1"
              Configuration:
                ActionMode: CHANGE_SET_EXECUTE
                StackName: !Ref StackName
                ChangeSetName: !Sub "${StackName}-changeset"

  PipelineRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: codepipeline.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: PipelinePolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - codecommit:Get*
                  - codecommit:List*
                  - codecommit:BatchGet*
                Resource: "*"
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                Resource: !Sub "arn:aws:s3:::${ArtifactBucket}/*"
              - Effect: Allow
                Action:
                  - cloudformation:*
                  - iam:PassRole
                Resource: "*"
              - Effect: Allow
                Action:
                  - sns:Publish
                Resource: !Ref ApprovalTopic

  ApprovalTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${AWS::StackName}-approval"
```

## Related Resources

- [CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [CloudWatch Best Practices](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_best_practices.html)
- [Service Level Indicators](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ServiceLevelIndicators.html)
- [CloudFormation Drift Detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)
- [CloudFormation Change Sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)

## Additional Files

For complete details on resources and their properties, consult:
- [REFERENCE.md](reference.md) - Detailed reference guide for all CloudFormation resources
- [EXAMPLES.md](examples.md) - Complete production-ready examples
