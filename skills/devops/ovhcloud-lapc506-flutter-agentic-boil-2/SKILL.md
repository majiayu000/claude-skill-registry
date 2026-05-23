# ☁️ Skill: OVHCloud Backend Deployment

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-ovhcloud` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `ovh`, `ovhcloud`, `kubernetes`, `object-storage` |

## 🔑 Keywords

- `ovh`, `ovhcloud`, `managed-kubernetes`, `object-storage`, `@skill:ovhcloud`

## 📖 Descripción

OVHCloud ofrece servicios cloud europeos para backends Flutter: Managed Kubernetes, Object Storage, Databases, y más con precios competitivos.

## 💻 Servicios Principales

### 1. Managed Kubernetes

```bash
# Install OVH CLI
pip3 install python-ovh

# Create cluster via API
curl -X POST https://api.ovh.com/v1/cloud/project/{serviceName}/kube \
  -H "Content-Type: application/json" \
  -d '{
    "name": "myapp-prod",
    "region": "GRA7",
    "version": "1.28",
    "privateNetworkId": null,
    "nodepool": {
      "name": "default-pool",
      "flavorName": "b2-7",
      "desiredNodes": 3,
      "minNodes": 2,
      "maxNodes": 10,
      "autoscale": true
    }
  }'

# Get kubeconfig
ovh-cli kube kubeconfig --name myapp-prod > kubeconfig.yaml
export KUBECONFIG=kubeconfig.yaml
```

### 2. Object Storage (S3 Compatible)

```python
import boto3

# Configure S3 client for OVH
s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    endpoint_url='https://s3.gra.io.cloud.ovh.net',
    region_name='gra'
)

# Create bucket
s3_client.create_bucket(Bucket='myapp-storage-prod')

# Upload file
s3_client.upload_file('local-file.txt', 'myapp-storage-prod', 'remote-file.txt')

# Set CORS
cors_configuration = {
    'CORSRules': [{
        'AllowedHeaders': ['*'],
        'AllowedMethods': ['GET', 'PUT', 'POST'],
        'AllowedOrigins': ['*'],
        'ExposeHeaders': []
    }]
}

s3_client.put_bucket_cors(
    Bucket='myapp-storage-prod',
    CORSConfiguration=cors_configuration
)
```

### 3. Managed Databases

```bash
# Create PostgreSQL instance via OVH Manager or API
curl -X POST https://api.ovh.com/v1/cloud/project/{serviceName}/database/postgresql \
  -H "Content-Type: application/json" \
  -d '{
    "description": "MyApp Production DB",
    "plan": "business",
    "version": "15",
    "nodes": [
      {
        "region": "GRA",
        "networkId": null,
        "subnetId": null
      }
    ],
    "nodesList": [
      {
        "flavor": "db1-7",
        "region": "GRA"
      }
    ]
  }'
```

### 4. Load Balancer

```bash
# Create load balancer
curl -X POST https://api.ovh.com/v1/cloud/project/{serviceName}/loadbalancer \
  -d '{
    "description": "MyApp LB",
    "region": "GRA7",
    "size": "S"
  }'

# Add backend
curl -X POST https://api.ovh.com/v1/cloud/project/{serviceName}/loadbalancer/{loadBalancerId}/backend \
  -d '{
    "name": "backend-pool",
    "protocol": "http",
    "balancer": "roundrobin",
    "servers": [
      {
        "address": "10.0.0.10",
        "port": 8080
      }
    ]
  }'
```

### 5. Terraform with OVHCloud

```hcl
# Configure provider
terraform {
  required_providers {
    ovh = {
      source = "ovh/ovh"
    }
  }
}

provider "ovh" {
  endpoint           = "ovh-eu"
  application_key    = var.ovh_application_key
  application_secret = var.ovh_application_secret
  consumer_key       = var.ovh_consumer_key
}

# Create Kubernetes cluster
resource "ovh_cloud_project_kube" "my_kube_cluster" {
  service_name = var.service_name
  name         = "myapp-prod"
  region       = "GRA7"
  version      = "1.28"
}

# Create node pool
resource "ovh_cloud_project_kube_nodepool" "node_pool" {
  service_name  = var.service_name
  kube_id       = ovh_cloud_project_kube.my_kube_cluster.id
  name          = "default-pool"
  flavor_name   = "b2-7"
  desired_nodes = 3
  min_nodes     = 2
  max_nodes     = 10
  autoscale     = true
}
```

## 🎯 Mejores Prácticas

1. **GDPR Compliant** - Datos en Europa
2. **Precios competitivos** - Mejor relación calidad-precio
3. **Terraform provider** disponible
4. **S3-compatible** Object Storage
5. **Managed Kubernetes** sin lock-in
6. **API completa** para automatización

## 📚 Recursos

- [OVHCloud Documentation](https://docs.ovh.com/)
- [OVHCloud API](https://api.ovh.com/)
- [Terraform OVH Provider](https://registry.terraform.io/providers/ovh/ovh/latest/docs)

---

**Versión:** 1.0.0

