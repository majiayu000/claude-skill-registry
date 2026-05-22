---
name: iac-generator
description: |
  Gera codigo de infraestrutura baseado em arquitetura definida.
  Suporta Terraform, Bicep, e Kubernetes manifests.
  Use quando: criar infraestrutura, gerar IaC, configurar deploy.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - WebFetch
user-invocable: true
---

# IaC Generator Skill

## Proposito

Esta skill gera codigo de Infrastructure as Code seguindo melhores praticas.

## Provedores Suportados

### Azure

- Container Apps
- Azure Kubernetes Service (AKS)
- Azure SQL / PostgreSQL Flexible Server
- Key Vault
- Service Bus
- Application Insights
- Storage Account
- Virtual Network

### AWS

- ECS/Fargate
- EKS
- RDS (PostgreSQL, MySQL)
- Secrets Manager
- SQS/SNS
- CloudWatch
- S3
- VPC

### Kubernetes

- Deployments
- Services (ClusterIP, LoadBalancer, NodePort)
- ConfigMaps / Secrets
- Ingress / Gateway API
- NetworkPolicies
- PodSecurityStandards
- HorizontalPodAutoscaler

## Comandos

### /iac-init

Inicializa estrutura de IaC para o projeto:

```bash
/iac-init
```

Cria:
- `.agentic_sdlc/projects/{id}/iac/terraform/`
- `main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`
- `.github/workflows/terraform.yml`

### /iac-module {provider} {resource}

Gera modulo Terraform para recurso especifico:

```bash
/iac-module azure container-app
/iac-module aws ecs-service
/iac-module k8s deployment
```

### /iac-secure

Executa analise de seguranca em IaC:

```bash
/iac-secure
```

Executa:
- checkov scan
- tfsec scan
- Gera relatorio de findings

## Templates

### Azure Container App

```hcl
# main.tf
resource "azurerm_container_app" "main" {
  name                         = var.app_name
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    container {
      name   = "api"
      image  = var.container_image
      cpu    = var.cpu
      memory = var.memory

      dynamic "env" {
        for_each = var.environment_variables
        content {
          name        = env.key
          secret_name = env.value.secret ? env.key : null
          value       = env.value.secret ? null : env.value.value
        }
      }
    }

    min_replicas = var.min_replicas
    max_replicas = var.max_replicas
  }

  ingress {
    allow_insecure_connections = false
    external_enabled           = var.external_ingress
    target_port                = var.target_port
    transport                  = "http"

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}
```

### Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.name }}
  labels:
    app: {{ .Values.name }}
spec:
  replicas: {{ .Values.replicas }}
  selector:
    matchLabels:
      app: {{ .Values.name }}
  template:
    metadata:
      labels:
        app: {{ .Values.name }}
    spec:
      containers:
        - name: {{ .Values.name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.port }}
          resources:
            limits:
              cpu: {{ .Values.resources.limits.cpu }}
              memory: {{ .Values.resources.limits.memory }}
            requests:
              cpu: {{ .Values.resources.requests.cpu }}
              memory: {{ .Values.resources.requests.memory }}
          envFrom:
            - configMapRef:
                name: {{ .Values.name }}-config
            - secretRef:
                name: {{ .Values.name }}-secrets
          livenessProbe:
            httpGet:
              path: /health
              port: {{ .Values.port }}
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /ready
              port: {{ .Values.port }}
            initialDelaySeconds: 5
            periodSeconds: 10
```

## Checklist de Seguranca

Antes de gerar IaC, verificar:

- [ ] Secrets via Key Vault / Secrets Manager (nunca hardcoded)
- [ ] Network isolation (VNets/VPCs com subnets privadas)
- [ ] TLS everywhere (HTTPS, encrypted connections)
- [ ] Least privilege RBAC (roles minimas necessarias)
- [ ] Audit logging habilitado
- [ ] Encryption at rest (databases, storage)
- [ ] Private endpoints onde possivel
- [ ] Backup configurado
- [ ] Tags de custo aplicadas

## Integracao com SDLC

| Fase | Acao IaC |
|------|----------|
| Fase 3 (Arquitetura) | Definir recursos necessarios |
| Fase 5 (Implementacao) | Gerar codigo IaC |
| Fase 6 (Qualidade) | Security scan de IaC |
| Fase 7 (Release) | Apply em staging/prod |

## Workflow de Deploy

```yaml
deploy_workflow:
  1_plan:
    - terraform init
    - terraform plan -out=tfplan
    - Revisar plan

  2_apply_staging:
    - terraform apply tfplan
    - Verificar deploy
    - Smoke tests

  3_apply_production:
    - Aprovacao humana
    - terraform apply tfplan
    - Monitorar metricas
    - Rollback se necessario
```

## CI/CD Pipeline

GitHub Actions workflow gerado automaticamente:

```yaml
name: Terraform
on:
  push:
    branches: [main]
    paths:
      - '.agentic_sdlc/**/iac/**'
  pull_request:
    branches: [main]
    paths:
      - '.agentic_sdlc/**/iac/**'

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform plan -no-color
        continue-on-error: true

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .agentic_sdlc/projects/*/iac/terraform
```

## Pontos de Pesquisa

Para templates atualizados:
- "terraform azure container apps module"
- "terraform aws ecs best practices"
- "kubernetes deployment security best practices"
