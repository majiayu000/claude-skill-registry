---
name: aws-diagram
description: Generate AWS architecture diagrams from infrastructure JSON. Use when user asks to "generate diagram", "create AWS diagram", "visualize infrastructure", or "draw architecture".
---

# AWS Diagram Generator

Generate architecture diagrams from `aws_infrastructure.json` using the Python `diagrams` library.

## Before Starting

1. Check that `aws_infrastructure.json` exists in the current directory
2. Ask user which diagram type they want:
   - **architecture** - Overall infrastructure overview
   - **security** - Security controls and traffic flow
   - **network** - Network topology and connectivity
   - **data-flow** - Data flow between components
   - **all** - Generate all types

3. Ask for output format: **png** (default), **svg**, or **pdf**

## Process

1. Read `aws_infrastructure.json`
2. Generate Python code using the `diagrams` library
3. Write the code to a temporary file
4. Execute it with `python <file>.py`
5. Report the generated files to the user

## Diagrams Library Reference

### Basic Structure
```python
from diagrams import Diagram, Cluster, Edge

with Diagram("Title", filename="output_name", outformat="png", show=False):
    # Create nodes and connections
```

### AWS Icons (import from diagrams.aws.*)

**Compute:**
```python
from diagrams.aws.compute import ECS, Lambda, Fargate, EC2, EKS, Batch, ECR
```

**Database:**
```python
from diagrams.aws.database import RDS, Aurora, ElastiCache, Dynamodb, DocumentDB, Neptune, Redshift
```
Note: Use `Dynamodb` (not DynamoDB)

**Network:**
```python
from diagrams.aws.network import ALB, NLB, CloudFront, Route53, VPC, InternetGateway, NATGateway, TransitGateway, Endpoint, APIGateway
```

**Storage:**
```python
from diagrams.aws.storage import S3, EFS
```

**Security:**
```python
from diagrams.aws.security import WAF, Shield, ACM, Cognito, SecretsManager, KMS, IAM
```

**Integration:**
```python
from diagrams.aws.integration import SQS, SNS, Eventbridge, StepFunctions
```
Note: Use `Eventbridge` (not EventBridge)

**Analytics:**
```python
from diagrams.aws.analytics import Kinesis, Athena, Glue, EMR, Quicksight
```

**Management:**
```python
from diagrams.aws.management import Cloudwatch, CloudwatchAlarm, Cloudtrail
```

**General (for unknown services):**
```python
from diagrams.aws.general import General
```

**External/Users:**
```python
from diagrams.onprem.network import Internet
from diagrams.onprem.client import Users
```

### Connections
```python
# Left to right flow
node1 >> node2
node1 >> Edge(label="HTTPS") >> node2

# Multiple targets
node1 >> [node2, node3]
```

### Clusters (for grouping)
```python
with Cluster("VPC"):
    with Cluster("Public Subnet"):
        alb = ALB("Load Balancer")
    with Cluster("Private Subnet"):
        app = Fargate("App")
```

## Diagram Types

### Architecture Diagram
Show overall infrastructure:
- Internet/Users connecting to load balancers
- Load balancers to compute (ECS, Lambda, EC2)
- Compute to databases (RDS, DynamoDB, ElastiCache)
- Storage services (S3)
- Group by VPC and subnet types

### Security Diagram
Show security controls:
- WAF protecting load balancers
- Cognito for authentication
- ACM certificates
- Security boundaries (VPC, subnets)
- Traffic flow from external to internal
- KMS, Secrets Manager

### Network Diagram
Show network topology:
- VPC with CIDR
- Subnets grouped by availability zone
- Internet Gateway and NAT Gateways
- Transit Gateway connections
- VPC Endpoints

### Data Flow Diagram
Show data movement:
- How data enters (API, events)
- Processing pipeline (compute services)
- Data storage destinations
- Caching layers
- Event flows (SQS, SNS, EventBridge)

## Output Files

Use these filenames:
- `aws_architecture.png`
- `aws_security.png`
- `aws_network.png`
- `aws_data_flow.png`

## Guidelines

1. Set `show=False` in Diagram constructor
2. Create meaningful labels from the JSON data
3. Draw connections based on logical relationships
4. Use Clusters to group related resources
5. Limit displayed items to 3-5 per category for readability
6. For services not in the library, use `General`
7. Always use the exact import names (case-sensitive)

## Example Generated Code

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import Fargate
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ALB, InternetGateway
from diagrams.aws.storage import S3
from diagrams.onprem.network import Internet

with Diagram("AWS Architecture - MyProject (PROD)", filename="aws_architecture", outformat="png", show=False):
    internet = Internet("Users")

    with Cluster("VPC: 10.0.0.0/16"):
        igw = InternetGateway("IGW")

        with Cluster("Public Subnet"):
            alb = ALB("Public ALB")

        with Cluster("Private Subnet"):
            with Cluster("ECS Cluster"):
                svc1 = Fargate("api")
                svc2 = Fargate("worker")

            db = RDS("Aurora")
            cache = ElastiCache("Redis")

    s3 = S3("Assets")

    internet >> igw >> alb >> [svc1, svc2]
    svc1 >> [db, cache, s3]
    svc2 >> [db, s3]
```

## After Generation

Tell the user:
1. Which diagram files were created
2. They can open PNG/SVG directly or import into documentation
