---
name: cloudwatch-alarm-creator
description: Эксперт по CloudWatch алармам. Используй для настройки мониторинга AWS, метрик, порогов и уведомлений.
---

# CloudWatch Alarm Creator

Эксперт по мониторингу AWS CloudWatch и настройке алармов.

## Основные принципы

- **Выбор порогов**: Основывайте на исторических данных и бизнес-требованиях
- **Статистические методы**: Выбирайте подходящую статистику (Average, Sum, Maximum) по характеристикам метрик
- **Периоды оценки**: Баланс между отзывчивостью и подавлением шума
- **Actionable алерты**: Каждый аларм должен иметь понятный путь устранения
- **Оптимизация стоимости**: Эффективные стратегии для минимизации расходов

## EC2 Alarm

```json
{
  "AlarmName": "HighCPUUtilization",
  "MetricName": "CPUUtilization",
  "Namespace": "AWS/EC2",
  "Statistic": "Average",
  "Period": 300,
  "EvaluationPeriods": 2,
  "Threshold": 80,
  "ComparisonOperator": "GreaterThanThreshold",
  "Dimensions": [
    {
      "Name": "InstanceId",
      "Value": "i-1234567890abcdef0"
    }
  ],
  "AlarmActions": ["arn:aws:sns:region:account:topic"],
  "TreatMissingData": "notBreaching"
}
```

## ALB Alarm

```json
{
  "AlarmName": "HighTargetResponseTime",
  "MetricName": "TargetResponseTime",
  "Namespace": "AWS/ApplicationELB",
  "Statistic": "Average",
  "Period": 60,
  "EvaluationPeriods": 3,
  "DatapointsToAlarm": 2,
  "Threshold": 1.0,
  "ComparisonOperator": "GreaterThanThreshold",
  "Dimensions": [
    {
      "Name": "LoadBalancer",
      "Value": "app/my-alb/1234567890"
    }
  ],
  "TreatMissingData": "ignore"
}
```

## RDS Alarm

```json
{
  "AlarmName": "HighDatabaseConnections",
  "MetricName": "DatabaseConnections",
  "Namespace": "AWS/RDS",
  "Statistic": "Average",
  "Period": 300,
  "EvaluationPeriods": 2,
  "Threshold": 100,
  "ComparisonOperator": "GreaterThanThreshold",
  "Dimensions": [
    {
      "Name": "DBInstanceIdentifier",
      "Value": "my-database"
    }
  ]
}
```

## Terraform Configuration

```hcl
resource "aws_cloudwatch_metric_alarm" "ec2_cpu_high" {
  alarm_name          = "ec2-cpu-high-${var.instance_id}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "CPU utilization exceeds 80%"

  dimensions = {
    InstanceId = var.instance_id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_cloudwatch_metric_alarm" "custom_metric" {
  alarm_name          = "custom-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  threshold           = 5
  alarm_description   = "Error rate exceeds 5%"

  metric_query {
    id          = "error_rate"
    expression  = "errors/requests*100"
    label       = "Error Rate"
    return_data = true
  }

  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "MyApp"
      period      = 60
      stat        = "Sum"
    }
  }

  metric_query {
    id = "requests"
    metric {
      metric_name = "Requests"
      namespace   = "MyApp"
      period      = 60
      stat        = "Sum"
    }
  }
}
```

## Composite Alarm

```json
{
  "AlarmName": "CompositeSystemHealth",
  "AlarmRule": "ALARM(HighCPU) AND (ALARM(HighMemory) OR ALARM(HighDisk))",
  "AlarmActions": ["arn:aws:sns:region:account:critical-alerts"],
  "AlarmDescription": "System health degraded - multiple metrics breaching"
}
```

## Anomaly Detection

```json
{
  "AlarmName": "AnomalyDetectionCPU",
  "MetricName": "CPUUtilization",
  "Namespace": "AWS/EC2",
  "ThresholdMetricId": "ad1",
  "ComparisonOperator": "GreaterThanUpperThreshold",
  "EvaluationPeriods": 2,
  "Metrics": [
    {
      "Id": "m1",
      "MetricStat": {
        "Metric": {
          "Namespace": "AWS/EC2",
          "MetricName": "CPUUtilization",
          "Dimensions": [{"Name": "InstanceId", "Value": "i-123"}]
        },
        "Period": 300,
        "Stat": "Average"
      }
    },
    {
      "Id": "ad1",
      "Expression": "ANOMALY_DETECTION_BAND(m1, 2)"
    }
  ]
}
```

## SNS Integration

```hcl
resource "aws_sns_topic" "alerts" {
  name = "cloudwatch-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "ops-team@example.com"
}

resource "aws_sns_topic_subscription" "lambda" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.alert_handler.arn
}
```

## TreatMissingData Options

| Значение | Описание | Использование |
|----------|----------|---------------|
| `notBreaching` | Missing = OK | Стандартные метрики |
| `breaching` | Missing = ALARM | Heartbeat мониторинг |
| `ignore` | Сохранять текущее | ALB метрики |
| `missing` | Missing = INSUFFICIENT | По умолчанию |

## Рекомендации по порогам

```yaml
EC2:
  CPUUtilization:
    warning: 70%
    critical: 85%
    period: 300s

  StatusCheckFailed:
    threshold: 1
    period: 60s

ALB:
  TargetResponseTime:
    p95_warning: 500ms
    p99_critical: 1000ms

  HTTPCode_ELB_5XX:
    threshold: 10
    period: 60s

RDS:
  CPUUtilization:
    warning: 70%
    critical: 85%

  FreeableMemory:
    critical: 256MB

  DiskQueueDepth:
    warning: 5
    critical: 10
```

## Стоимость оптимизации

- Консолидируйте алармы через composite alarms
- Используйте более длинные периоды где возможно
- Удаляйте неиспользуемые алармы регулярно
- Группируйте ресурсы через теги

## Тестирование алармов

```bash
# Переключить состояние для тестирования уведомлений
aws cloudwatch set-alarm-state \
  --alarm-name "HighCPUUtilization" \
  --state-value ALARM \
  --state-reason "Testing notifications"
```

## Лучшие практики

1. **2 из 3 datapoints** — фильтрация временных спайков
2. **Percentile-based thresholds** — для latency метрик (P95, P99)
3. **Multi-level alerts** — Warning и Critical уровни
4. **Документируйте runbooks** — для каждого типа аларма
5. **Регулярный аудит** — пересматривайте эффективность порогов
