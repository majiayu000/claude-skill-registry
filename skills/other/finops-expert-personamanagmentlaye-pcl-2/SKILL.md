---
name: finops-expert
version: 1.0.0
description: Expert-level cloud financial operations, cost optimization, and cloud economics
category: professional
tags: [finops, cloud-cost, optimization, cloud-economics, aws-cost]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(*)
---

# FinOps Expert

Expert guidance for cloud financial operations, cost optimization, resource management, and cloud economics.

## Core Concepts

### FinOps Fundamentals
- Cloud cost visibility
- Usage optimization
- Rate optimization
- Architecture optimization
- Cloud unit economics
- Showback and chargeback

### Cost Management
- Reserved Instances (RIs)
- Savings Plans
- Spot instances
- Right-sizing resources
- Idle resource cleanup
- Storage lifecycle policies

### FinOps Practices
- Tagging strategies
- Budgets and alerts
- Cost allocation
- Forecasting and planning
- Cross-team collaboration
- Continuous optimization

## AWS Cost Analysis

```python
import boto3
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd

class AWSCostAnalyzer:
    """Analyze AWS costs using Cost Explorer API"""

    def __init__(self):
        self.ce_client = boto3.client('ce')

    def get_cost_and_usage(self, start_date: str, end_date: str,
                          granularity: str = 'DAILY',
                          metrics: List[str] = None) -> Dict:
        """Get cost and usage data"""
        if metrics is None:
            metrics = ['UnblendedCost', 'UsageQuantity']

        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity=granularity,
            Metrics=metrics,
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )

        return response['ResultsByTime']

    def get_top_services_by_cost(self, days: int = 30, top_n: int = 10) -> pd.DataFrame:
        """Get top services by cost"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        results = self.get_cost_and_usage(start_date, end_date, 'MONTHLY')

        service_costs = {}
        for result in results:
            for group in result['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['UnblendedCost']['Amount'])

                if service in service_costs:
                    service_costs[service] += cost
                else:
                    service_costs[service] = cost

        df = pd.DataFrame(list(service_costs.items()),
                         columns=['Service', 'Cost'])
        return df.nlargest(top_n, 'Cost')

    def get_cost_forecast(self, days_ahead: int = 30) -> Dict:
        """Get cost forecast"""
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

        response = self.ce_client.get_cost_forecast(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Metric='UNBLENDED_COST',
            Granularity='MONTHLY'
        )

        return {
            'forecasted_cost': float(response['Total']['Amount']),
            'mean_value': float(response['ForecastResultsByTime'][0]['MeanValue'])
        }

    def get_rightsizing_recommendations(self) -> List[Dict]:
        """Get EC2 rightsizing recommendations"""
        response = self.ce_client.get_rightsizing_recommendation(
            Service='AmazonEC2'
        )

        recommendations = []
        for rec in response['RightsizingRecommendations']:
            recommendations.append({
                'instance_id': rec['CurrentInstance']['ResourceId'],
                'current_type': rec['CurrentInstance']['InstanceType'],
                'recommended_type': rec['ModifyRecommendationDetail']['TargetInstances'][0]['InstanceType']
                    if rec.get('ModifyRecommendationDetail') else None,
                'estimated_savings': float(rec['EstimatedMonthlySavings']['Value'])
                    if rec.get('EstimatedMonthlySavings') else 0
            })

        return recommendations

class CostOptimizer:
    """Optimize cloud costs"""

    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.rds_client = boto3.client('rds')
        self.s3_client = boto3.client('s3')

    def find_idle_resources(self) -> Dict[str, List]:
        """Find idle/unused resources"""
        idle_resources = {
            'ec2_instances': [],
            'ebs_volumes': [],
            'elastic_ips': [],
            'load_balancers': []
        }

        # Idle EC2 instances (stopped for > 7 days)
        instances = self.ec2_client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
        )

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                idle_resources['ec2_instances'].append({
                    'id': instance['InstanceId'],
                    'type': instance['InstanceType'],
                    'state': instance['State']['Name']
                })

        # Unattached EBS volumes
        volumes = self.ec2_client.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )

        for volume in volumes['Volumes']:
            idle_resources['ebs_volumes'].append({
                'id': volume['VolumeId'],
                'size': volume['Size'],
                'type': volume['VolumeType']
            })

        # Unattached Elastic IPs
        addresses = self.ec2_client.describe_addresses()

        for address in addresses['Addresses']:
            if 'InstanceId' not in address:
                idle_resources['elastic_ips'].append({
                    'allocation_id': address['AllocationId'],
                    'public_ip': address['PublicIp']
                })

        return idle_resources

    def calculate_reserved_instance_savings(self,
                                           instance_type: str,
                                           count: int,
                                           term: int = 1) -> Dict:
        """Calculate RI savings"""
        # Simplified calculation (would use actual pricing API)
        on_demand_hourly = self._get_on_demand_price(instance_type)
        ri_hourly = on_demand_hourly * 0.65  # ~35% discount

        hours_per_year = 24 * 365
        annual_on_demand = on_demand_hourly * hours_per_year * count
        annual_ri = ri_hourly * hours_per_year * count

        return {
            'instance_type': instance_type,
            'count': count,
            'annual_on_demand_cost': annual_on_demand,
            'annual_ri_cost': annual_ri,
            'annual_savings': annual_on_demand - annual_ri,
            'savings_percentage': ((annual_on_demand - annual_ri) / annual_on_demand) * 100
        }

    def _get_on_demand_price(self, instance_type: str) -> float:
        """Get on-demand hourly price (simplified)"""
        # In production, use AWS Pricing API
        prices = {
            't3.micro': 0.0104,
            't3.small': 0.0208,
            't3.medium': 0.0416,
            'm5.large': 0.096,
            'm5.xlarge': 0.192
        }
        return prices.get(instance_type, 0.10)
```

## Cost Allocation and Tagging

```python
class CostAllocation:
    """Manage cost allocation with tags"""

    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.ce_client = boto3.client('ce')

    def define_tagging_strategy(self) -> Dict[str, List[str]]:
        """Define mandatory tags"""
        return {
            'environment': ['prod', 'staging', 'dev'],
            'team': ['engineering', 'data', 'product'],
            'cost_center': ['CC001', 'CC002', 'CC003'],
            'project': ['project-a', 'project-b'],
            'owner': ['email addresses']
        }

    def audit_resource_tags(self, resource_type: str = 'instance') -> List[Dict]:
        """Audit resources for missing tags"""
        mandatory_tags = ['environment', 'team', 'cost_center']
        untagged_resources = []

        if resource_type == 'instance':
            instances = self.ec2_client.describe_instances()

            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    tags = {tag['Key']: tag['Value']
                           for tag in instance.get('Tags', [])}

                    missing_tags = [tag for tag in mandatory_tags
                                  if tag not in tags]

                    if missing_tags:
                        untagged_resources.append({
                            'resource_id': instance['InstanceId'],
                            'missing_tags': missing_tags
                        })

        return untagged_resources

    def get_cost_by_tag(self, tag_key: str, start_date: str,
                       end_date: str) -> pd.DataFrame:
        """Get costs grouped by tag"""
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'TAG', 'Key': tag_key}
            ]
        )

        costs = []
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                costs.append({
                    'tag_value': group['Keys'][0].split('$')[1]
                        if '$' in group['Keys'][0] else 'Untagged',
                    'cost': float(group['Metrics']['UnblendedCost']['Amount'])
                })

        return pd.DataFrame(costs)
```

## Budget Management

```python
class BudgetManager:
    """Manage AWS budgets and alerts"""

    def __init__(self):
        self.budgets_client = boto3.client('budgets')
        self.account_id = boto3.client('sts').get_caller_identity()['Account']

    def create_monthly_budget(self, name: str, amount: float,
                             email: str) -> Dict:
        """Create monthly cost budget with alerts"""
        budget = {
            'BudgetName': name,
            'BudgetLimit': {
                'Amount': str(amount),
                'Unit': 'USD'
            },
            'TimeUnit': 'MONTHLY',
            'BudgetType': 'COST'
        }

        # Alert at 80% and 100%
        notifications = [
            {
                'Notification': {
                    'NotificationType': 'ACTUAL',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': 80,
                    'ThresholdType': 'PERCENTAGE'
                },
                'Subscribers': [{
                    'SubscriptionType': 'EMAIL',
                    'Address': email
                }]
            },
            {
                'Notification': {
                    'NotificationType': 'ACTUAL',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': 100,
                    'ThresholdType': 'PERCENTAGE'
                },
                'Subscribers': [{
                    'SubscriptionType': 'EMAIL',
                    'Address': email
                }]
            }
        ]

        response = self.budgets_client.create_budget(
            AccountId=self.account_id,
            Budget=budget,
            NotificationsWithSubscribers=notifications
        )

        return response
```

## Best Practices

### Cost Visibility
- Implement comprehensive tagging
- Enable Cost Explorer
- Set up cost allocation tags
- Create custom cost reports
- Use dashboards for visualization
- Monitor costs daily

### Optimization
- Right-size resources regularly
- Use Reserved Instances/Savings Plans
- Leverage Spot instances for flexible workloads
- Implement auto-scaling
- Clean up idle resources
- Use storage lifecycle policies

### Governance
- Set budgets and alerts
- Implement approval workflows
- Regular cost reviews
- Cross-team accountability
- Document cost optimization wins
- Automate cost controls

## Anti-Patterns

❌ No tagging strategy
❌ Ignoring rightsizing recommendations
❌ Not using Reserved Instances
❌ No budget alerts
❌ Keeping idle resources
❌ Manual cost tracking
❌ Siloed cost responsibility

## Resources

- AWS Cost Explorer: https://aws.amazon.com/aws-cost-management/aws-cost-explorer/
- FinOps Foundation: https://www.finops.org/
- AWS Well-Architected Cost Optimization: https://wa.aws.amazon.com/wat.pillar.costOptimization.en.html
- Boto3 Cost Explorer: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html
