---
name: container-apps-gpu-2025
description: Azure Container Apps GPU support 2025 features including serverless GPU, Dapr integration, and scale-to-zero
---

# Azure Container Apps GPU Support - 2025 Features

Complete knowledge base for Azure Container Apps with GPU support, serverless capabilities, and Dapr integration (2025 GA features).

## Overview

Azure Container Apps is a serverless container platform with native GPU support, Dapr integration, and scale-to-zero capabilities for cost-efficient AI/ML workloads.

## Key 2025 Features (Build Announcements)

### 1. Serverless GPU (GA)
- **Automatic scaling**: Scale GPU workloads based on demand
- **Scale-to-zero**: Pay only when GPU is actively used
- **Per-second billing**: Granular cost control
- **Optimized cold start**: Fast initialization for AI models
- **Reduced operational overhead**: No infrastructure management

### 2. Dedicated GPU (GA)
- **Consistent performance**: Dedicated GPU resources
- **Simplified AI deployment**: Easy model hosting
- **Long-running workloads**: Ideal for training and continuous inference
- **Multiple GPU types**: NVIDIA A100, T4, and more

### 3. Dynamic Sessions with GPU (Early Access)
- **Sandboxed execution**: Run untrusted AI-generated code
- **Hyper-V isolation**: Enhanced security
- **GPU-powered Python interpreter**: Handle compute-intensive AI workloads
- **Scale at runtime**: Dynamic resource allocation

### 4. Foundry Models Integration
- **Deploy AI models directly**: During container app creation
- **Ready-to-use models**: Pre-configured inference endpoints
- **Azure AI Foundry**: Seamless integration

### 5. Workflow with Durable Task Scheduler (Preview)
- **Long-running workflows**: Reliable orchestration
- **State management**: Automatic persistence
- **Event-driven**: Trigger workflows from events

### 6. Native Azure Functions Support
- **Functions runtime**: Run Azure Functions in Container Apps
- **Consistent development**: Same code, serverless execution
- **Event triggers**: All Functions triggers supported

### 7. Dapr Integration (GA)
- **Service discovery**: Built-in DNS-based discovery
- **State management**: Distributed state stores
- **Pub/sub messaging**: Reliable messaging patterns
- **Service invocation**: Resilient service-to-service calls
- **Observability**: Integrated tracing and metrics

## Creating Container Apps with GPU

### Basic Container App with Serverless GPU

```bash
# Create Container Apps environment
az containerapp env create \
  --name myenv \
  --resource-group MyRG \
  --location eastus \
  --logs-workspace-id <workspace-id> \
  --logs-workspace-key <workspace-key>

# Create Container App with GPU
az containerapp create \
  --name myapp-gpu \
  --resource-group MyRG \
  --environment myenv \
  --image myregistry.azurecr.io/ai-model:latest \
  --cpu 4 \
  --memory 8Gi \
  --gpu-type nvidia-a100 \
  --gpu-count 1 \
  --min-replicas 0 \
  --max-replicas 10 \
  --ingress external \
  --target-port 8080
```

### Production-Ready Container App with GPU

```bash
az containerapp create \
  --name myapp-gpu-prod \
  --resource-group MyRG \
  --environment myenv \
  \
  # Container configuration
  --image myregistry.azurecr.io/ai-model:latest \
  --registry-server myregistry.azurecr.io \
  --registry-identity system \
  \
  # Resources
  --cpu 4 \
  --memory 8Gi \
  --gpu-type nvidia-a100 \
  --gpu-count 1 \
  \
  # Scaling
  --min-replicas 0 \
  --max-replicas 20 \
  --scale-rule-name http-scaling \
  --scale-rule-type http \
  --scale-rule-http-concurrency 10 \
  \
  # Networking
  --ingress external \
  --target-port 8080 \
  --transport http2 \
  --exposed-port 8080 \
  \
  # Security
  --registry-identity system \
  --env-vars "AZURE_CLIENT_ID=secretref:client-id" \
  \
  # Monitoring
  --dapr-app-id myapp \
  --dapr-app-port 8080 \
  --dapr-app-protocol http \
  --enable-dapr \
  \
  # Identity
  --system-assigned
```

## Container Apps Environment Configuration

### Environment with Zone Redundancy

```bash
az containerapp env create \
  --name myenv-prod \
  --resource-group MyRG \
  --location eastus \
  --logs-workspace-id <workspace-id> \
  --logs-workspace-key <workspace-key> \
  --zone-redundant true \
  --enable-workload-profiles true
```

### Workload Profiles (Dedicated GPU)

```bash
# Create environment with workload profiles
az containerapp env create \
  --name myenv-gpu \
  --resource-group MyRG \
  --location eastus \
  --enable-workload-profiles true

# Add GPU workload profile
az containerapp env workload-profile add \
  --name myenv-gpu \
  --resource-group MyRG \
  --workload-profile-name gpu-profile \
  --workload-profile-type GPU-A100 \
  --min-nodes 0 \
  --max-nodes 10

# Create container app with GPU profile
az containerapp create \
  --name myapp-dedicated-gpu \
  --resource-group MyRG \
  --environment myenv-gpu \
  --workload-profile-name gpu-profile \
  --image myregistry.azurecr.io/training-job:latest \
  --cpu 8 \
  --memory 16Gi \
  --min-replicas 1 \
  --max-replicas 5
```

## GPU Scaling Rules

### Custom Prometheus Scaling

```bash
az containerapp create \
  --name myapp-gpu-prometheus \
  --resource-group MyRG \
  --environment myenv \
  --image myregistry.azurecr.io/ai-model:latest \
  --cpu 4 \
  --memory 8Gi \
  --gpu-type nvidia-a100 \
  --gpu-count 1 \
  --min-replicas 0 \
  --max-replicas 10 \
  --scale-rule-name gpu-utilization \
  --scale-rule-type custom \
  --scale-rule-custom-type prometheus \
  --scale-rule-metadata \
    serverAddress=http://prometheus.monitoring.svc.cluster.local:9090 \
    metricName=gpu_utilization \
    threshold=80 \
    query="avg(nvidia_gpu_utilization{app='myapp'})"
```

### Queue-Based Scaling (Azure Service Bus)

```bash
az containerapp create \
  --name myapp-queue-processor \
  --resource-group MyRG \
  --environment myenv \
  --image myregistry.azurecr.io/batch-processor:latest \
  --cpu 4 \
  --memory 8Gi \
  --gpu-type nvidia-t4 \
  --gpu-count 1 \
  --min-replicas 0 \
  --max-replicas 50 \
  --scale-rule-name queue-scaling \
  --scale-rule-type azure-servicebus \
  --scale-rule-metadata \
    queueName=ai-jobs \
    namespace=myservicebus \
    messageCount=5 \
  --scale-rule-auth connection=servicebus-connection
```

## Dapr Integration

### Enable Dapr on Container App

```bash
az containerapp create \
  --name myapp-dapr \
  --resource-group MyRG \
  --environment myenv \
  --image myregistry.azurecr.io/myapp:latest \
  --enable-dapr \
  --dapr-app-id myapp \
  --dapr-app-port 8080 \
  --dapr-app-protocol http \
  --dapr-http-max-request-size 4 \
  --dapr-http-read-buffer-size 4 \
  --dapr-log-level info \
  --dapr-enable-api-logging true
```

### Dapr State Store (Azure Cosmos DB)

```yaml
# Create Dapr component for state store
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.azure.cosmosdb
  version: v1
  metadata:
    - name: url
      value: "https://mycosmosdb.documents.azure.com:443/"
    - name: masterKey
      secretRef: cosmosdb-key
    - name: database
      value: "mydb"
    - name: collection
      value: "state"
```

```bash
# Create the component
az containerapp env dapr-component set \
  --name myenv \
  --resource-group MyRG \
  --dapr-component-name statestore \
  --yaml component.yaml
```

### Dapr Pub/Sub (Azure Service Bus)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.azure.servicebus.topics
  version: v1
  metadata:
    - name: connectionString
      secretRef: servicebus-connection
    - name: consumerID
      value: "myapp"
```

### Service-to-Service Invocation

```python
# Python example using Dapr SDK
from dapr.clients import DaprClient

with DaprClient() as client:
    # Invoke another service
    response = client.invoke_method(
        app_id='other-service',
        method_name='process',
        data='{"input": "data"}'
    )

    # Save state
    client.save_state(
        store_name='statestore',
        key='mykey',
        value='myvalue'
    )

    # Publish message
    client.publish_event(
        pubsub_name='pubsub',
        topic_name='orders',
        data='{"orderId": "123"}'
    )
```

## AI Model Deployment Patterns

### OpenAI-Compatible Endpoint

```dockerfile
# Dockerfile for vLLM model serving
FROM vllm/vllm-openai:latest

ENV MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct"
ENV GPU_MEMORY_UTILIZATION=0.9
ENV MAX_MODEL_LEN=4096

CMD ["--model", "${MODEL_NAME}", \
     "--gpu-memory-utilization", "${GPU_MEMORY_UTILIZATION}", \
     "--max-model-len", "${MAX_MODEL_LEN}", \
     "--port", "8080"]
```

```bash
# Deploy vLLM model
az containerapp create \
  --name llama-inference \
  --resource-group MyRG \
  --environment myenv \
  --image vllm/vllm-openai:latest \
  --cpu 8 \
  --memory 32Gi \
  --gpu-type nvidia-a100 \
  --gpu-count 1 \
  --min-replicas 1 \
  --max-replicas 5 \
  --target-port 8080 \
  --ingress external \
  --env-vars \
    MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct" \
    GPU_MEMORY_UTILIZATION="0.9" \
    HF_TOKEN=secretref:huggingface-token
```

### Stable Diffusion Image Generation

```bash
az containerapp create \
  --name stable-diffusion \
  --resource-group MyRG \
  --environment myenv \
  --image myregistry.azurecr.io/stable-diffusion:latest \
  --cpu 4 \
  --memory 16Gi \
  --gpu-type nvidia-a100 \
  --gpu-count 1 \
  --min-replicas 0 \
  --max-replicas 10 \
  --target-port 7860 \
  --ingress external \
  --scale-rule-name http-scaling \
  --scale-rule-type http \
  --scale-rule-http-concurrency 1
```

### Batch Processing Job

```bash
az containerapp job create \
  --name batch-training-job \
  --resource-group MyRG \
  --environment myenv \
  --trigger-type Manual \
  --image myregistry.azurecr.io/training:latest \
  --cpu 8 \
  --memory 32Gi \
  --gpu-type nvidia-a100 \
  --gpu-count 2 \
  --parallelism 1 \
  --replica-timeout 7200 \
  --replica-retry-limit 3 \
  --env-vars \
    DATASET_URL="https://mystorage.blob.core.windows.net/datasets/train.csv" \
    MODEL_OUTPUT="https://mystorage.blob.core.windows.net/models/" \
    EPOCHS="100"

# Execute job
az containerapp job start \
  --name batch-training-job \
  --resource-group MyRG
```

## Monitoring and Observability

### Application Insights Integration

```bash
az containerapp create \
  --name myapp-monitored \
  --resource-group MyRG \
  --environment myenv \
  --image myregistry.azurecr.io/myapp:latest \
  --env-vars \
    APPLICATIONINSIGHTS_CONNECTION_STRING=secretref:appinsights-connection
```

### Query Logs

```bash
# Stream logs
az containerapp logs show \
  --name myapp-gpu \
  --resource-group MyRG \
  --follow

# Query with Log Analytics
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "ContainerAppConsoleLogs_CL | where ContainerAppName_s == 'myapp-gpu' | take 100"
```

### Metrics and Alerts

```bash
# Create metric alert for GPU usage
az monitor metrics alert create \
  --name high-gpu-usage \
  --resource-group MyRG \
  --scopes $(az containerapp show -g MyRG -n myapp-gpu --query id -o tsv) \
  --condition "avg Requests > 100" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action <action-group-id>
```

## Security Best Practices

### Managed Identity

```bash
# Create with system-assigned identity
az containerapp create \
  --name myapp-identity \
  --resource-group MyRG \
  --environment myenv \
  --system-assigned \
  --image myregistry.azurecr.io/myapp:latest

# Get identity principal ID
IDENTITY_ID=$(az containerapp show -g MyRG -n myapp-identity --query identity.principalId -o tsv)

# Assign role to access Key Vault
az role assignment create \
  --assignee $IDENTITY_ID \
  --role "Key Vault Secrets User" \
  --scope /subscriptions/<sub-id>/resourceGroups/MyRG/providers/Microsoft.KeyVault/vaults/mykeyvault

# Use user-assigned identity
az identity create --name myapp-identity --resource-group MyRG
IDENTITY_RESOURCE_ID=$(az identity show -g MyRG -n myapp-identity --query id -o tsv)

az containerapp create \
  --name myapp-user-identity \
  --resource-group MyRG \
  --environment myenv \
  --user-assigned $IDENTITY_RESOURCE_ID \
  --image myregistry.azurecr.io/myapp:latest
```

### Secret Management

```bash
# Add secrets
az containerapp secret set \
  --name myapp-gpu \
  --resource-group MyRG \
  --secrets \
    huggingface-token="<token>" \
    api-key="<key>"

# Reference secrets in environment variables
az containerapp update \
  --name myapp-gpu \
  --resource-group MyRG \
  --set-env-vars \
    HF_TOKEN=secretref:huggingface-token \
    API_KEY=secretref:api-key
```

## Cost Optimization

### Scale-to-Zero Configuration

```bash
az containerapp create \
  --name myapp-scale-zero \
  --resource-group MyRG \
  --environment myenv \
  --image myregistry.azurecr.io/myapp:latest \
  --min-replicas 0 \
  --max-replicas 10 \
  --scale-rule-name http-scaling \
  --scale-rule-type http \
  --scale-rule-http-concurrency 10
```

**Cost savings**: Pay only when requests are being processed. GPU costs are per-second when active.

### Right-Sizing Resources

```bash
# Start with minimal resources
--cpu 2 --memory 4Gi --gpu-count 1

# Monitor and adjust based on actual usage
az monitor metrics list \
  --resource $(az containerapp show -g MyRG -n myapp-gpu --query id -o tsv) \
  --metric "CpuPercentage,MemoryPercentage"
```

### Use Spot/Preemptible GPUs (Future Feature)

When available, configure spot instances for non-critical workloads to save up to 80% on GPU costs.

## Troubleshooting

### Check Revision Status

```bash
az containerapp revision list \
  --name myapp-gpu \
  --resource-group MyRG \
  --output table
```

### View Revision Details

```bash
az containerapp revision show \
  --name <revision-name> \
  --app myapp-gpu \
  --resource-group MyRG
```

### Restart Container App

```bash
az containerapp update \
  --name myapp-gpu \
  --resource-group MyRG \
  --force-restart
```

### GPU Not Available

If GPU is not provisioning:
1. Check region availability: Not all regions support GPU
2. Verify quota: Request quota increase if needed
3. Check workload profile: Ensure GPU workload profile is created

## Best Practices

✓ Use scale-to-zero for intermittent workloads
✓ Implement health probes (liveness and readiness)
✓ Use managed identities for authentication
✓ Store secrets in Azure Key Vault
✓ Enable Dapr for microservices patterns
✓ Configure appropriate scaling rules
✓ Monitor GPU utilization and adjust resources
✓ Use Container Apps jobs for batch processing
✓ Implement retry logic for transient failures
✓ Use Application Insights for observability

## References

- [Container Apps GPU Documentation](https://learn.microsoft.com/en-us/azure/container-apps/gpu-support)
- [Dapr Integration](https://learn.microsoft.com/en-us/azure/container-apps/dapr-overview)
- [Scaling Rules](https://learn.microsoft.com/en-us/azure/container-apps/scale-app)
- [Build 2025 Announcements](https://azure.microsoft.com/en-us/blog/container-apps-build-2025/)

Azure Container Apps with GPU support provides the ultimate serverless platform for AI/ML workloads!
