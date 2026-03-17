---
name: devops-expert
version: 1.0.0
description: Expert-level DevOps practices, culture, automation, and continuous delivery
category: devops
tags: [devops, ci-cd, automation, infrastructure, culture]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(*)
---

# DevOps Expert

Expert guidance for DevOps practices, culture, CI/CD pipelines, infrastructure automation, and operational excellence.

## Core Concepts

### DevOps Culture
- Collaboration and communication
- Shared responsibility
- Continuous improvement
- Breaking down silos
- Blameless culture
- Measuring everything

### Automation
- Infrastructure as Code (IaC)
- Configuration management
- Deployment automation
- Testing automation
- Monitoring automation
- Self-service platforms

### CI/CD
- Continuous Integration
- Continuous Delivery
- Continuous Deployment
- Pipeline as Code
- Artifact management
- Release strategies

## CI/CD Pipeline

```yaml
# GitHub Actions Example
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Run security scan
        run: npm audit

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=staging

      - name: Wait for rollout
        run: kubectl rollout status deployment/myapp -n staging

      - name: Run smoke tests
        run: npm run test:smoke

  deploy-production:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=production

      - name: Wait for rollout
        run: kubectl rollout status deployment/myapp -n production
```

## Infrastructure as Code

```python
# Pulumi Infrastructure as Code
import pulumi
import pulumi_aws as aws

# VPC
vpc = aws.ec2.Vpc("main-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "main-vpc"})

# Subnets
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
    map_public_ip_on_launch=True,
    tags={"Name": "public-subnet"})

private_subnet = aws.ec2.Subnet("private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="us-east-1b",
    tags={"Name": "private-subnet"})

# Internet Gateway
igw = aws.ec2.InternetGateway("igw",
    vpc_id=vpc.id,
    tags={"Name": "main-igw"})

# Route Table
route_table = aws.ec2.RouteTable("public-rt",
    vpc_id=vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            gateway_id=igw.id,
        )
    ],
    tags={"Name": "public-rt"})

# Security Group
security_group = aws.ec2.SecurityGroup("web-sg",
    vpc_id=vpc.id,
    description="Allow HTTP and HTTPS traffic",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=443,
            to_port=443,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )
    ])

# EKS Cluster
cluster = aws.eks.Cluster("app-cluster",
    role_arn=cluster_role.arn,
    vpc_config=aws.eks.ClusterVpcConfigArgs(
        subnet_ids=[public_subnet.id, private_subnet.id],
        security_group_ids=[security_group.id],
    ))

# Export outputs
pulumi.export("vpc_id", vpc.id)
pulumi.export("cluster_name", cluster.name)
pulumi.export("cluster_endpoint", cluster.endpoint)
```

## Deployment Strategies

```python
from typing import List, Dict
import time

class DeploymentStrategy:
    """Implement various deployment strategies"""

    def __init__(self, service_name: str):
        self.service_name = service_name

    def blue_green_deployment(self, blue_version: str, green_version: str):
        """Blue-Green deployment"""
        # Deploy green environment
        self.deploy_environment("green", green_version)

        # Run tests on green
        if self.run_tests("green"):
            # Switch traffic to green
            self.switch_traffic("green")

            # Keep blue for rollback
            print(f"Deployment successful. Blue ({blue_version}) kept for rollback.")
        else:
            # Rollback - keep blue active
            print("Tests failed on green. Keeping blue active.")

    def canary_deployment(self, current_version: str, new_version: str,
                         canary_percentage: int = 10):
        """Canary deployment"""
        # Deploy canary with small percentage
        self.deploy_canary(new_version, canary_percentage)

        # Monitor metrics
        metrics = self.monitor_canary_metrics(duration_minutes=10)

        if metrics['error_rate'] < 0.1 and metrics['latency_p95'] < 500:
            # Gradually increase canary traffic
            for percentage in [25, 50, 75, 100]:
                self.update_canary_traffic(percentage)
                time.sleep(300)  # 5 minutes between increases

                if not self.check_health():
                    self.rollback(current_version)
                    return False

            print(f"Canary deployment successful: {new_version}")
            return True
        else:
            self.rollback(current_version)
            print("Canary deployment failed - rolled back")
            return False

    def rolling_deployment(self, version: str, batch_size: int = 1):
        """Rolling deployment"""
        instances = self.get_instances()

        for i in range(0, len(instances), batch_size):
            batch = instances[i:i + batch_size]

            # Update batch
            for instance in batch:
                self.update_instance(instance, version)
                self.wait_for_healthy(instance)

            # Verify batch health
            if not self.check_health():
                print(f"Rolling deployment failed at batch {i//batch_size + 1}")
                return False

        print(f"Rolling deployment successful: {version}")
        return True

    def feature_flag_deployment(self, feature_name: str, enabled: bool,
                               rollout_percentage: int = 100):
        """Feature flag based deployment"""
        return {
            'feature': feature_name,
            'enabled': enabled,
            'rollout_percentage': rollout_percentage,
            'targeting': {
                'user_segments': ['beta_users'] if rollout_percentage < 100 else ['all']
            }
        }
```

## Configuration Management

```python
from typing import Dict, Any
import yaml
import json

class ConfigurationManager:
    """Manage application configuration"""

    def __init__(self, environment: str):
        self.environment = environment
        self.config = {}

    def load_config(self, config_file: str):
        """Load configuration from file"""
        with open(config_file, 'r') as f:
            if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                self.config = yaml.safe_load(f)
            elif config_file.endswith('.json'):
                self.config = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def merge_environment_config(self, env_config: Dict):
        """Merge environment-specific configuration"""
        self.config = self._deep_merge(self.config, env_config)

    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def validate_required_keys(self, required_keys: List[str]) -> List[str]:
        """Validate that required configuration keys exist"""
        missing = []

        for key in required_keys:
            if self.get(key) is None:
                missing.append(key)

        return missing
```

## Monitoring and Observability

```python
import logging
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

class ObservabilityStack:
    """Implement observability best practices"""

    def __init__(self):
        self.logger = self._setup_logging()
        self.stats = stats_module.stats
        self.view_manager = self.stats.view_manager

    def _setup_logging(self) -> logging.Logger:
        """Setup structured logging"""
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", '
            '"service": "%(name)s", "message": "%(message)s"}'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def log_with_context(self, level: str, message: str, **context):
        """Log with additional context"""
        log_func = getattr(self.logger, level)
        log_func(message, extra=context)

    def track_custom_metric(self, metric_name: str, value: float,
                           tags: Dict[str, str]):
        """Track custom application metric"""
        # Implementation would send to metrics backend
        pass

    def create_distributed_trace(self, operation_name: str):
        """Create distributed trace span"""
        # Implementation would use OpenTelemetry or similar
        pass
```

## Best Practices

### Culture & Process
- Foster collaboration between Dev and Ops
- Automate everything possible
- Measure and monitor continuously
- Practice blameless post-mortems
- Share knowledge and documentation
- Encourage experimentation
- Celebrate successes and learn from failures

### CI/CD
- Keep builds fast (<10 minutes)
- Run tests in parallel
- Use pipeline as code
- Implement automated rollbacks
- Require code review before merge
- Use trunk-based development
- Deploy small, frequent changes

### Infrastructure
- Use Infrastructure as Code
- Version everything (code, config, infrastructure)
- Implement disaster recovery
- Practice chaos engineering
- Use immutable infrastructure
- Automate security scanning
- Monitor cloud costs

## Anti-Patterns

❌ Manual deployments
❌ Configuration drift
❌ No automated testing
❌ Long-lived feature branches
❌ Blame culture
❌ Siloed teams
❌ Ignoring technical debt

## Resources

- The Phoenix Project: https://itrevolution.com/the-phoenix-project/
- DevOps Handbook: https://itrevolution.com/the-devops-handbook/
- State of DevOps Report: https://www.devops-research.com/research.html
- GitLab CI/CD: https://docs.gitlab.com/ee/ci/
- GitHub Actions: https://docs.github.com/en/actions
