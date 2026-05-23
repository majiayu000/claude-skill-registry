---
name: cloud-diagram
description: >
  Generate professional cloud architecture diagrams as PNG images using Python code.
  Use this skill whenever the user asks to create, draw, visualize, or diagram any cloud
  architecture, infrastructure, network topology, landing zone, hub-spoke design,
  multi-tier application layout, or deployment pipeline. Trigger on any of these clouds
  or platforms: Azure (VNet, App Service, AKS, SQL, Cosmos DB, Functions, etc.),
  AWS (EC2, ECS, EKS, Lambda, RDS, S3, CloudFront, ALB, DynamoDB, SQS, SNS, etc.),
  GCP / Google Cloud (GKE, Cloud Run, Cloud SQL, BigQuery, Pub/Sub, Cloud Functions, etc.),
  Kubernetes / K8s (Pods, Deployments, Services, Ingress, StatefulSets, etc.),
  on-premises / self-hosted (Nginx, Docker, PostgreSQL, Redis, Kafka, Elasticsearch, etc.),
  or multi-cloud / hybrid designs combining any of the above. Also covers: Alibaba Cloud,
  DigitalOcean, Oracle Cloud (OCI), IBM Cloud, Firebase, Elastic, OpenStack, and generic
  architecture nodes. Supports 2000+ node types across 16 providers.
version: 1.1.0
author: CyberSorted
tags: [diagram, architecture, cloud, infrastructure, visualization, azure, aws, gcp, kubernetes, k8s, onprem, multi-cloud]
license: MIT
---

# Cloud Architecture Diagram Generator

Generate professional cloud architecture diagrams using the Python `diagrams` library
(mingrammer/diagrams) with Graphviz rendering. Outputs PNG images with official icons
for Azure, AWS, GCP, Kubernetes, on-premises, and 10+ other providers.

## Prerequisites

The script needs two dependencies. Install them at runtime if missing:

```bash
pip install diagrams --break-system-packages -q
apt-get install -y graphviz -q 2>/dev/null || true
```

## Workflow

### Step 1: Understand the Architecture

Before writing any code, clarify what the user wants:

- **Which cloud provider(s)?** Azure, AWS, GCP, Kubernetes, on-prem, or a multi-cloud mix
- **What type of diagram?** Architecture overview, network topology, landing zone, data flow, CI/CD pipeline
- **Which services?** Map user descriptions to specific node classes for the chosen provider
- **How complex?** Simple (3-5 nodes), medium (6-15 nodes), complex (15+ nodes with multiple clusters)
- **Layout direction?** Left-to-right (`LR`) for wide diagrams, top-to-bottom (`TB`) for tall ones

If the user is vague (e.g., "draw me a web app architecture"), make reasonable assumptions
and generate a solid default -- don't over-ask. You can always iterate.

### Step 2: Map Services to Node Classes

Consult `references/<provider>-nodes.md` for the full node list per provider. Below are the most common mappings.

#### Azure (`from diagrams.azure.<module> import <Class>`)

**Compute:** `AppServices`, `FunctionApps`, `KubernetesServices` (alias `AKS`), `VM`, `VMScaleSet` (alias `VMSS`), `ContainerInstances`, `ContainerApps`, `BatchAccounts`

**Networking:** `VirtualNetworks`, `ApplicationGateway`, `LoadBalancers`, `Firewall`, `FrontDoors`, `CDNProfiles`, `DNSZones`, `ExpressrouteCircuits`, `VirtualNetworkGateways`, `TrafficManagerProfiles`, `Subnets`, `PrivateEndpoint`, `PublicIpAddresses`

**Database:** `SQLDatabases`, `CosmosDb`, `CacheForRedis`, `DatabaseForPostgresqlServers`, `DatabaseForMysqlServers`

**Storage:** `BlobStorage`, `StorageAccounts`, `DataLakeStorage`, `QueueStorage`, `FileStorage`

**Security:** `KeyVaults`, `Sentinel`, `SecurityCenter`

**Identity:** `ActiveDirectory`, `ManagedIdentities`, `ConditionalAccess`

**Integration:** `ServiceBus`, `EventGridTopics`, `LogicApps`, `APIManagement`

**DevOps/Monitoring:** `ApplicationInsights`, `Pipelines`, `Repos`, `AzureDevops`

**AI/ML:** `CognitiveServices`, `MachineLearning`, `AzureOpenai`

#### AWS (`from diagrams.aws.<module> import <Class>`)

**Compute:** `EC2`, `ECS`, `EKS`, `Lambda`, `Fargate`, `Batch`, `ElasticBeanstalk`

**Networking:** `ELB`, `ALB`, `NLB`, `CloudFront`, `Route53`, `VPC`, `APIGateway`, `DirectConnect`

**Database:** `RDS`, `Aurora`, `DynamoDB`, `ElastiCache`, `Redshift`, `Neptune`, `DocumentDB`

**Storage:** `S3`, `EFS`, `EBS`, `FSx`, `Glacier`

**Security:** `WAF`, `Shield`, `IAMRole`, `IAM`, `KMS`, `SecretsManager`, `Cognito`

**Integration:** `SQS`, `SNS`, `Kinesis`, `StepFunctions`, `EventBridge`

**Management:** `Cloudwatch`, `Cloudtrail`, `Config`, `SystemsManager`

#### GCP (`from diagrams.gcp.<module> import <Class>`)

**Compute:** `Run`, `Functions`, `GKE`, `ComputeEngine`, `AppEngine`

**Networking:** `CDN`, `DNS`, `LoadBalancing`, `Armor`, `VPC`

**Database:** `SQL`, `Spanner`, `Bigtable`, `Firestore`, `Memorystore`

**Storage:** `GCS`, `Filestore`, `PersistentDisk`

**Analytics:** `BigQuery`, `Dataflow`, `Dataproc`, `PubSub`, `Composer`

#### Kubernetes (`from diagrams.k8s.<module> import <Class>`)

**Compute:** `Pod`, `Deployment`, `ReplicaSet`, `StatefulSet`, `DaemonSet`, `Job`, `CronJob`

**Networking:** `Ingress`, `Service`, `NetworkPolicy`

**Storage:** `PV`, `PVC`, `StorageClass`

**Other:** `HPA`, `Namespace`, `ConfigMap`, `Secret`, `ServiceAccount`

#### On-Premises / Open Source (`from diagrams.onprem.<module> import <Class>`)

**Compute:** `Docker`, `Nomad`

**Database:** `PostgreSQL`, `MySQL`, `MongoDB`, `Redis`, `Cassandra`, `ClickHouse`, `Elasticsearch`

**Network:** `Nginx`, `HAProxy`, `Traefik`, `Envoy`, `Istio`, `Kong`

**Queue:** `Kafka`, `RabbitMQ`, `Celery`

**Monitoring:** `Grafana`, `Prometheus`, `Datadog`, `Splunk`

**CI/CD:** `Jenkins`, `GitlabCI`, `GithubActions`, `ArgoCD`

### Step 3: Write the Diagram Code

Use this pattern:

```python
from diagrams import Diagram, Cluster, Edge
# Import from any provider:
from diagrams.azure.<module> import <NodeClass>
from diagrams.aws.<module> import <NodeClass>
from diagrams.gcp.<module> import <NodeClass>
from diagrams.k8s.<module> import <NodeClass>
from diagrams.onprem.<module> import <NodeClass>

with Diagram("<Title>", show=False, filename="<output_name>", outformat="png", direction="LR"):
    # Optional: group related resources in Clusters
    with Cluster("Resource Group / VPC / Region"):
        node1 = NodeClass("Label")
        node2 = NodeClass("Label")

    # Connect with >> (data flow direction)
    node1 >> node2

    # Fan out to multiple targets
    node1 >> [node2, node3]

    # Custom edge labels and styles
    node1 >> Edge(label="HTTPS", color="blue") >> node2
```

**Multi-provider example** (mix providers freely in one diagram):

```python
from diagrams.aws.network import CloudFront
from diagrams.azure.compute import AppServices
from diagrams.gcp.database import Spanner
from diagrams.onprem.monitoring import Grafana

# All of these can coexist in a single Diagram context
```

**Key patterns:**

- **Clusters** = Resource Groups, VPCs, VNets, Subnets, Regions, Namespaces, or any logical grouping
- **Nested Clusters** = VNet containing Subnets, Region containing Resource Groups
- **Edge direction** = `>>` flows left-to-right or top-to-bottom depending on `direction`
- **Edge labels** = Use `Edge(label="protocol/description")` for clarity
- **Lists** = `source >> [target1, target2]` fans out connections
- **Bidirectional** = Use `node1 >> node2` and `node2 >> node1` separately, or `node1 - node2` for undirected

**Direction guidelines:**
- `LR` (left-to-right): Best for data flow, request paths, pipelines
- `TB` (top-to-bottom): Best for hierarchical designs, landing zones, network topology
- `RL` or `BT`: Rarely used but available

**Diagram() parameters:**
- `show=False` -- Always set this (don't open a viewer)
- `filename` -- Output path without extension
- `outformat` -- Use `"png"` (default) or `"svg"`
- `direction` -- `"LR"`, `"TB"`, `"RL"`, `"BT"`
- `graph_attr` -- Dict of Graphviz attributes for fine-tuning (e.g., `{"fontsize": "20", "bgcolor": "white", "pad": "0.5"}`)

### Step 4: Generate and Present

1. Write the Python script to a temp file
2. Run it: `python3 /tmp/cloud_diagram.py`
3. The output PNG will be at the `filename` path
4. Present the image to the user

### Step 5: Iterate

If the user wants changes:
- Add/remove services
- Change layout or grouping
- Adjust labels or edge descriptions
- Change output format
- Switch or add cloud providers

Modify the script and regenerate. Each run is fast (~2-5 seconds).

## Common Architecture Patterns

### Azure: Hub-Spoke Network

```
Hub VNet: Firewall, VPN Gateway, Bastion
  +-- Spoke 1: Web tier (App Gateway -> App Services)
  +-- Spoke 2: Data tier (SQL, Cosmos DB)
  +-- Spoke 3: AKS workloads
```

### Azure: 3-Tier Web Application

```
Users -> Front Door/CDN -> App Gateway -> App Services/AKS -> SQL/Cosmos DB
                                                            -> Redis Cache
                                                            -> Blob Storage
```

### Azure: Serverless Event-Driven

```
Event Source -> Event Grid/Service Bus -> Function Apps -> Cosmos DB
                                                        -> Blob Storage
                                      -> Logic Apps -> External APIs
```

### AWS: 3-Tier Web Application

```
Route 53 -> CloudFront -> WAF -> ALB -> ECS/EC2 -> RDS (Multi-AZ)
                                                 -> ElastiCache
                                                 -> S3
```

### AWS: Serverless

```
API Gateway -> Lambda -> DynamoDB
                      -> S3
            -> Step Functions -> Lambda -> SQS -> Lambda
EventBridge -> Lambda -> SNS -> Subscribers
```

### AWS: Data Lake

```
S3 (raw) -> Glue ETL -> S3 (curated) -> Athena -> QuickSight
                                       -> Redshift Spectrum
Kinesis Data Streams -> Kinesis Firehose -> S3
```

### GCP: Web Application

```
Cloud DNS -> Cloud CDN -> Cloud Load Balancing -> Cloud Run / GKE
                                               -> Cloud SQL / Spanner
                                               -> Memorystore
Cloud Armor (WAF) -|
```

### GCP: Data Analytics

```
Pub/Sub -> Dataflow -> BigQuery -> Looker
                    -> Cloud Storage
Cloud Composer (orchestration)
```

### Kubernetes: Microservices

```
Ingress -> Service A -> Pod (Deployment) -> PVC -> PV
        -> Service B -> Pod (StatefulSet) -> ConfigMap, Secret
HPA auto-scales Deployments
NetworkPolicy controls east-west traffic
```

### Multi-Cloud: Active-Active

```
Global LB
  +-- AWS (us-east-1): CloudFront -> ECS -> RDS
  +-- Azure (East US): Front Door -> App Service -> Cosmos DB
  +-- GCP (us-central1): CDN -> Cloud Run -> Spanner
Cross-region replication between databases
```

### Hybrid: On-Prem + Cloud

```
On-Prem: Nginx -> Docker containers -> PostgreSQL
  |-- VPN / ExpressRoute / Interconnect --|
Cloud: API Gateway -> Kubernetes -> Managed DB
Monitoring: Prometheus + Grafana (on-prem) collecting from both
```

## Using Custom Icons

For services not in the `diagrams` library, use `Custom` nodes:

```python
from diagrams.custom import Custom
from urllib.request import urlretrieve

icon_url = "https://example.com/my-service-icon.png"
icon_file = "custom_icon.png"
urlretrieve(icon_url, icon_file)

custom_node = Custom("My Service", icon_file)
```

## Edge Styling Reference

```python
Edge(label="HTTPS", color="blue", style="bold")
Edge(label="async", color="orange", style="dashed")
Edge(label="private link", color="darkgreen", style="dotted")
Edge(color="firebrick", style="bold")   # Error/alert path
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: diagrams` | `pip install diagrams --break-system-packages` |
| `ExecutableNotFound: dot` | `apt-get install -y graphviz` |
| Nodes overlapping | Add `graph_attr={"nodesep": "1.0", "ranksep": "1.5"}` |
| Diagram too wide/tall | Switch `direction` between `LR` and `TB` |
| Import error for a node | Check `references/<provider>-nodes.md` for the exact class name and module |
| Unknown provider module | Run `python scripts/generate_node_refs.py --provider <name> --output-dir references/` |
