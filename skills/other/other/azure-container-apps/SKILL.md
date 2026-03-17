---
name: azure-container-apps
description: Deploy containerized apps with Azure Container Apps. Configure auto-scaling, Dapr integration, traffic splitting, and managed identities. Use for microservices, APIs, background jobs, and event-driven applications on Azure.
---

# Azure Container Apps

Expert guidance for serverless containers on Azure.

## CLI Setup

```bash
# Install extension
az extension add --name containerapp --upgrade

# Register providers
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```

## Create Environment

```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# Create Container Apps environment
az containerapp env create \
  --name myEnvironment \
  --resource-group myResourceGroup \
  --location eastus
```

## Deploy Container App

### From Image

```bash
az containerapp create \
  --name myapp \
  --resource-group myResourceGroup \
  --environment myEnvironment \
  --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest \
  --target-port 80 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 10 \
  --cpu 0.5 \
  --memory 1Gi
```

### From Source Code

```bash
az containerapp up \
  --name myapp \
  --resource-group myResourceGroup \
  --environment myEnvironment \
  --source . \
  --ingress external \
  --target-port 8080
```

## YAML Configuration

```yaml
# containerapp.yaml
properties:
  managedEnvironmentId: /subscriptions/.../managedEnvironments/myEnvironment
  configuration:
    ingress:
      external: true
      targetPort: 8080
      transport: http
      traffic:
        - weight: 100
          latestRevision: true
    registries:
      - server: myregistry.azurecr.io
        identity: system
    secrets:
      - name: db-connection
        value: "Server=..."
  template:
    containers:
      - name: myapp
        image: myregistry.azurecr.io/myapp:latest
        resources:
          cpu: 0.5
          memory: 1Gi
        env:
          - name: DATABASE_URL
            secretRef: db-connection
          - name: ENVIRONMENT
            value: production
        probes:
          - type: Liveness
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          - type: Readiness
            httpGet:
              path: /ready
              port: 8080
    scale:
      minReplicas: 1
      maxReplicas: 30
      rules:
        - name: http-scaling
          http:
            metadata:
              concurrentRequests: "100"
```

## Scaling Rules

### HTTP Scaling

```yaml
scale:
  minReplicas: 0
  maxReplicas: 100
  rules:
    - name: http-rule
      http:
        metadata:
          concurrentRequests: "50"
```

### Queue-based Scaling (Azure Queue)

```yaml
scale:
  minReplicas: 0
  maxReplicas: 30
  rules:
    - name: queue-rule
      azureQueue:
        queueName: myqueue
        queueLength: 10
        auth:
          - secretRef: queue-connection
            triggerParameter: connection
```

### Custom Metrics (KEDA)

```yaml
scale:
  minReplicas: 0
  maxReplicas: 50
  rules:
    - name: kafka-rule
      custom:
        type: kafka
        metadata:
          bootstrapServers: kafka:9092
          consumerGroup: mygroup
          topic: mytopic
          lagThreshold: "100"
```

## Dapr Integration

### Enable Dapr

```yaml
properties:
  configuration:
    dapr:
      enabled: true
      appId: myapp
      appPort: 8080
      appProtocol: http
```

### Dapr Components

```yaml
# pubsub.yaml
componentType: pubsub.azure.servicebus
metadata:
  - name: connectionString
    secretRef: servicebus-connection
secrets:
  - name: servicebus-connection
    value: "Endpoint=sb://..."
scopes:
  - myapp
  - worker
```

## Traffic Splitting

```bash
# Create new revision
az containerapp update \
  --name myapp \
  --resource-group myResourceGroup \
  --image myapp:v2 \
  --revision-suffix v2

# Split traffic
az containerapp ingress traffic set \
  --name myapp \
  --resource-group myResourceGroup \
  --revision-weight myapp--v1=80 myapp--v2=20
```

## Jobs

### Scheduled Job

```bash
az containerapp job create \
  --name myjob \
  --resource-group myResourceGroup \
  --environment myEnvironment \
  --trigger-type Schedule \
  --cron-expression "0 */6 * * *" \
  --image myregistry.azurecr.io/myjob:latest \
  --cpu 0.5 \
  --memory 1Gi \
  --replica-timeout 1800 \
  --replica-retry-limit 3
```

### Event-driven Job

```yaml
properties:
  configuration:
    triggerType: Event
    replicaTimeout: 1800
    eventTriggerConfig:
      scale:
        minExecutions: 0
        maxExecutions: 10
        rules:
          - name: queue-trigger
            type: azure-queue
            metadata:
              queueName: jobs
              queueLength: "1"
```

## Bicep Deployment

```bicep
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: appName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: environment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
        transport: 'http'
        corsPolicy: {
          allowedOrigins: ['https://myapp.com']
          allowedMethods: ['GET', 'POST']
        }
      }
      secrets: [
        {
          name: 'registry-password'
          value: containerRegistry.listCredentials().passwords[0].value
        }
      ]
      registries: [
        {
          server: '${containerRegistry.name}.azurecr.io'
          username: containerRegistry.name
          passwordSecretRef: 'registry-password'
        }
      ]
    }
    template: {
      containers: [
        {
          name: appName
          image: '${containerRegistry.name}.azurecr.io/${appName}:${imageTag}'
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            {
              name: 'ASPNETCORE_ENVIRONMENT'
              value: 'Production'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
        rules: [
          {
            name: 'http-scale'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
        ]
      }
    }
  }
}
```

## Managed Identity

```bash
# Enable system-assigned identity
az containerapp identity assign \
  --name myapp \
  --resource-group myResourceGroup \
  --system-assigned

# Grant access to Key Vault
az keyvault set-policy \
  --name mykeyvault \
  --object-id <identity-principal-id> \
  --secret-permissions get list
```

## Monitoring

```bash
# View logs
az containerapp logs show \
  --name myapp \
  --resource-group myResourceGroup \
  --type console

# Stream logs
az containerapp logs show \
  --name myapp \
  --resource-group myResourceGroup \
  --follow

# View system logs
az containerapp logs show \
  --name myapp \
  --resource-group myResourceGroup \
  --type system
```

## Resources

- [Azure Container Apps Documentation](https://learn.microsoft.com/azure/container-apps/)
- [Container Apps Samples](https://github.com/Azure-Samples/container-apps-samples)
