# Skill: OVHCloud Backend Deployment

## Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-ovhcloud` |
| **Nivel** | Intermedio |
| **Version** | 1.1.0 |
| **Keywords** | `ovh`, `ovhcloud`, `kubernetes`, `object-storage`, `terraform` |

## Keywords

- `ovh`, `ovhcloud`, `managed-kubernetes`, `object-storage`, `@skill:ovhcloud`

## Descripcion

OVHCloud ofrece servicios cloud europeos para backends Flutter: Managed Kubernetes, Object Storage, Databases, y mas con precios competitivos.

## Instalacion CLI

### OVHCloud CLI (ovhcloud-cli)

```bash
# Install via curl
curl -fsSL https://raw.githubusercontent.com/ovh/ovhcloud-cli/main/install.sh | sh

# Or via Homebrew
brew install --cask ovh/tap/ovhcloud-cli

# Or via Go
go install github.com/ovh/ovhcloud-cli/cmd/ovhcloud@latest
```

### Autenticacion

```bash
# Login with OVHCloud account
ovhcloud login

# Or via environment variables
export OVH_ENDPOINT="ovh-eu"
export OVH_APPLICATION_KEY="your_app_key"
export OVH_APPLICATION_SECRET="your_app_secret"
export OVH_CONSUMER_KEY="your_consumer_key"
```

### Comandos utiles

```bash
# List Kubernetes clusters
ovhcloud cloud project kube list --service-name $SERVICE_NAME

# Get kubeconfig
ovhcloud cloud project kube kubeconfig --service-name $SERVICE_NAME --kube-id $KUBE_ID

# Create cluster
ovhcloud cloud project kube create \
  --service-name $SERVICE_NAME \
  --name my-cluster \
  --region GRA7 \
  --version 1.28

# Add node pool
ovhcloud cloud project kube nodepool create \
  --service-name $SERVICE_NAME \
  --kube-id $KUBE_ID \
  --name default-pool \
  --flavor-name b2-7 \
  --desired-nodes 3 \
  --min-nodes 2 \
  --max-nodes 10 \
  --autoscale true
```

## Terraform Provider

### Configuracion

```hcl
terraform {
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = "~> 1.0"
    }
  }
}

provider "ovh" {
  endpoint           = "ovh-eu"  # or ovh-ca, ovh-us
  application_key    = var.ovh_application_key
  application_secret = var.ovh_application_secret
  consumer_key       = var.ovh_consumer_key
}

# Optional: via environment variables
# OVH_APPLICATION_KEY, OVH_APPLICATION_SECRET, OVH_CONSUMER_KEY
```

### Recursos Kubernetes

```hcl
# Create Kubernetes cluster
resource "ovh_cloud_project_kube" "cluster" {
  service_name = var.service_name
  name         = "altrupets-prod"
  region       = "GRA7"
  version      = "1.28"

  timeouts {
    create = "15m"
    delete = "15m"
  }
}

# Create node pool
resource "ovh_cloud_project_kube_nodepool" "nodepool" {
  service_name  = var.service_name
  kube_id       = ovh_cloud_project_kube.cluster.id
  name          = "default-pool"
  flavor_name   = "b2-7"
  desired_nodes = 3
  min_nodes     = 2
  max_nodes     = 10
  autoscale     = true
}

# Get kubeconfig
data "ovh_cloud_project_kube_kubeconfig" "kubeconfig" {
  service_name = var.service_name
  kube_id      = ovh_cloud_project_kube.cluster.id
}
```

### Recursos PostgreSQL

```hcl
# OVH Managed PostgreSQL
resource "ovh_cloud_project_database_postgresql" "postgres" {
  service_name = var.service_name
  description  = "AltruPets Production DB"
  plan         = "business"
  version      = "15"

  nodes {
    region = "GRA7"
  }

  node {
    flavor = "db1-7"
    region = "GRA7"
  }
}

# Get credentials
data "ovh_cloud_project_database_postgresql_credentials" "creds" {
  service_name = var.service_name
  id           = ovh_cloud_project_database_postgresql.postgres.id
}

data "ovh_cloud_project_database_postgresql_endpoint" "endpoint" {
  service_name = var.service_name
  id           = ovh_cloud_project_database_postgresql.postgres.id
}
```

## Regiones disponibles

| Region | Codigo | Pais |
|--------|--------|------|
| Gravelines | GRA7, GRA11 | Francia |
| Strasbourg | SBG5 | Francia |
| Paris | RBX | Francia |
| Beauharnois | BHS | Canada |
| Hillsboro | WAW | USA |

## Flavors

### Kubernetes nodes

| Flavor | vCPUs | RAM | Uso |
|--------|-------|-----|-----|
| b2-7 | 2 | 7GB | Dev/QA |
| b2-15 | 2 | 15GB | Staging |
| c2-7 | 4 | 7GB | Production |
| c2-15 | 4 | 15GB | Production |
| r2-15 | 4 | 15GB | RAM-intensive |

### Database nodes

| Flavor | vCPUs | RAM | Storage |
|--------|-------|-----|---------|
| db1-7 | 2 | 7GB | 50GB |
| db1-15 | 2 | 15GB | 100GB |
| db2-7 | 4 | 7GB | 50GB |
| db2-15 | 4 | 15GB | 100GB |

## Managed Kubernetes

### OVHCloud CLI

```bash
# Create cluster
ovhcloud public cloud volume create \
  --service-name $SERVICE_NAME \
  --region GRA7 \
  --size 100 \
  --type classic

# Attach volume to instance
ovhcloud public cloud volume attach \
  --service-name $SERVICE_NAME \
  --region GRA7 \
  --volume-id $VOLUME_ID \
  --instance-id $INSTANCE_ID
```

### Terraform con Object Storage

```python
import boto3

s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    endpoint_url='https://s3.gra.io.cloud.ovh.net',
    region_name='gra'
)

# Create bucket
s3_client.create_bucket(Bucket='altrupets-storage')
```

## Mejores Practicas

1. **GDPR Compliant** - Datos en Europa
2. **Terraform provider** oficial disponible
3. **CLI** para tareas rapidas
4. **S3-compatible** Object Storage
5. **Managed Kubernetes** sin lock-in
6. **Secrets en Infisical** - No hardcodear credenciales

## Recursos

- [OVHCloud Documentation](https://docs.ovh.com/)
- [OVHCloud API](https://api.ovh.com/)
- [Terraform OVH Provider](https://registry.terraform.io/providers/ovh/ovh/latest/docs)
- [OVHCloud CLI GitHub](https://github.com/ovh/ovhcloud-cli)

---

**Version:** 1.1.0
