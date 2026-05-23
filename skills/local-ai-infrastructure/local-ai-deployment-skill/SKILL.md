---
skill: 'local-ai-deployment'
version: '2.0.0'
updated: '2025-12-31'
category: 'local-ai-infrastructure'
complexity: 'advanced'
prerequisite_skills:
  - 'hardware-sizing'
composable_with:
  - 'mlops-operations'
  - 'data-sovereignty'
  - 'production-readiness'
  - 'open-source-licensing'
---

# Local AI Deployment Skill

## Overview
Expertise in deploying and configuring self-hosted LLM platforms for enterprise environments, ensuring data sovereignty, performance optimization, and production-grade reliability without external dependencies.

## Key Capabilities
- Self-hosted LLM platform selection and configuration
- Containerized deployment (Docker, Kubernetes, Podman)
- Model serving optimization (quantization, batching, caching)
- Air-gapped and network-isolated deployments
- High availability and load balancing
- API gateway and authentication integration

## Self-Hosted LLM Platforms

### Platform Comparison Matrix

| Platform | Type | Best For | API Compat | GPU Support | Ease of Use |
|----------|------|----------|------------|-------------|-------------|
| **vLLM** | Inference server | High throughput | OpenAI | NVIDIA, AMD | Medium |
| **SGLang** | Inference server | Production | OpenAI | NVIDIA, AMD | Medium |
| **LocalAI** | Multi-modal | Flexibility | OpenAI | NVIDIA, CPU | Good |
| **llama.cpp** | Native | CPU, edge | Custom | All | Medium |

### Platform Selection Guide


**Choose vLLM when:**
- Production-grade throughput required
- High concurrency (many simultaneous users)
- OpenAI API compatibility needed
- Continuous batching for efficiency
- Enterprise Linux servers with NVIDIA GPUs

**Choose SGLang when:**
- Enterprise Hugging Face stack preferred
- AMD GPU support needed (ROCm)
- Tensor parallelism across multiple GPUs
- Strict performance requirements

**Choose LocalAI when:**
- Multi-modal capabilities needed (vision, audio)
- Want to run multiple model types
- Need drop-in OpenAI replacement
- CPU-only inference acceptable

## Deployment Configurations

### Docker Compose Templates

#### Production vLLM Setup
```yaml
version: '0.13.0'
services:
  vllm:
    image: vllm/vllm-openai:latest
    container_name: vllm
    ports:
      - "8000:8000"
    volumes:
      - /mnt/models:/models:ro
      - ./config:/config:ro
    environment:
      - CUDA_VISIBLE_DEVICES=0,1
    command: >
      --model /models/<MODEL_DIR>
      --tensor-parallel-size 2
      --max-model-len 8192
      --max-num-seqs 256
      --gpu-memory-utilization 0.90
      --enable-prefix-caching
      --api-key ${VLLM_API_KEY}
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 2
              capabilities: [gpu]
        limits:
          memory: 128G
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5

  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - vllm
    restart: unless-stopped
```

#### Multi-Model LocalAI Setup
```yaml
version: '3.8'
services:
  localai:
    image: localai/localai:latest-aio-gpu-nvidia-cuda-12
    container_name: localai
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models
      - ./config:/config
    environment:
      - THREADS=8
      - CONTEXT_SIZE=4096
      - MODELS_PATH=/models
      - CONFIG_FILE=/config/models.yaml
      - BUILD_TYPE=cublas
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped
```

### Kubernetes Deployment

#### vLLM StatefulSet
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vllm
  namespace: ai-inference
spec:
  serviceName: vllm
  replicas: 2
  selector:
    matchLabels:
      app: vllm
  template:
    metadata:
      labels:
        app: vllm
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 2
            memory: "128Gi"
            cpu: "32"
          requests:
            nvidia.com/gpu: 2
            memory: "64Gi"
            cpu: "16"
        volumeMounts:
        - name: model-storage
          mountPath: /models
        - name: config
          mountPath: /config
        env:
        - name: VLLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: vllm-secrets
              key: api-key
        args:
        - "--model"
        - "/models/<MODEL_DIR>"
        - "--tensor-parallel-size"
        - "2"
        - "--max-model-len"
        - "8192"
        - "--port"
        - "8000"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 300
          periodSeconds: 30
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 120
          periodSeconds: 10
      volumes:
      - name: config
        configMap:
          name: vllm-config
      nodeSelector:
        accelerator: nvidia-a100
      tolerations:
      - key: nvidia.com/gpu
        operator: Exists
        effect: NoSchedule
  volumeClaimTemplates:
  - metadata:
      name: model-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 500Gi
```

## Inference Optimization

### Quantization Reference

| Format | Precision | Size Reduction | Quality Loss | Speed Impact | Platform |
|--------|-----------|----------------|--------------|--------------|----------|
| FP16 | 16-bit | 0% (baseline) | None | Baseline | vLLM, TGI |
| INT8 | 8-bit | 50% | Minimal | -10% | vLLM (bitsandbytes) |
| AWQ | 4-bit | 75% | Small | +0-10% | vLLM |
| GPTQ | 4-bit | 75% | Small | +0-10% | vLLM, TGI |
| GGUF Q4_K_M | 4-bit | 75% | Small | Varies | llama.cpp |
| GGUF Q2_K | 2-bit | 87% | Moderate | Varies | llama.cpp |

### vLLM Optimization Parameters
```bash
# Maximum throughput configuration
vllm serve /models/<MODEL_DIR> \
  --tensor-parallel-size 2 \              # Multi-GPU parallelism
  --max-model-len 8192 \                  # Context length (shorter = faster)
  --max-num-seqs 256 \                    # Max concurrent sequences
  --gpu-memory-utilization 0.90 \         # VRAM usage (0.90 = 90%)
  --enable-prefix-caching \               # Cache common prefixes
  --enable-chunked-prefill \              # Better batching
  --max-num-batched-tokens 32768 \        # Batch size limit
  --disable-log-requests                  # Reduce logging overhead
```

## Edge/Endpoint Deployment (llama.cpp)

Use llama.cpp when you need lightweight endpoints close to developers (CPU/Metal/CUDA), offline edge nodes, or segmented networks. Treat vLLM/SGLang as the central “model serving plane” and llama.cpp as the “endpoint plane”.

```bash
# Example (binary name varies by build; often `llama-server`)
# Expose a minimal local endpoint on port 8081
./llama-server -m /mnt/models/<MODEL_FILE>.gguf -c 8192 --host 0.0.0.0 --port 8081

# Basic smoke test (API shape depends on build/flags)
curl -s http://localhost:8081/health || true
```

### Performance Tuning Checklist

- [ ] **GPU Memory:** Set --gpu-memory-utilization to 0.85-0.95
- [ ] **Context Length:** Reduce --max-model-len to minimum required
- [ ] **Batching:** Enable continuous batching (default in vLLM)
- [ ] **Prefix Caching:** Enable for repetitive prompts
- [ ] **Tensor Parallelism:** Use for multi-GPU setups
- [ ] **Quantization:** Consider AWQ/GPTQ for memory-constrained setups
- [ ] **CUDA Settings:** Set CUDA_VISIBLE_DEVICES explicitly
- [ ] **Persistence Mode:** Enable nvidia-smi -pm 1

## Air-Gapped Deployment

### Offline Package Preparation
```bash
#!/bin/bash
# prepare-offline-package.sh

PACKAGE_DIR="./offline-llm-package"
mkdir -p ${PACKAGE_DIR}/{images,models,configs}

# 1. Save Docker images
docker pull vllm/vllm-openai:latest
docker pull nginx:alpine
docker save vllm/vllm-openai:latest -o ${PACKAGE_DIR}/images/vllm.tar
docker save nginx:alpine -o ${PACKAGE_DIR}/images/nginx.tar

# 2. Download models (example model package)
pip install huggingface-hub
# Download from your approved model source (Hugging Face / internal registry)
# Prefer new-generation families such as Qwen-Next, MiniMax-M2, GLM-4.6.
huggingface-cli download <provider>/<model> \
  --local-dir ${PACKAGE_DIR}/models/<MODEL_DIR>

# 3. Copy configurations
cp docker-compose.yml ${PACKAGE_DIR}/configs/
cp nginx.conf ${PACKAGE_DIR}/configs/
cp .env.example ${PACKAGE_DIR}/configs/

# 4. Create installation script
cat > ${PACKAGE_DIR}/install.sh << 'EOF'
#!/bin/bash
docker load -i images/vllm.tar
docker load -i images/nginx.tar
cp -r models /mnt/ai-models/
cp configs/* /opt/llm/
cd /opt/llm && docker compose up -d
EOF
chmod +x ${PACKAGE_DIR}/install.sh

# 5. Package for transfer
tar -czvf offline-llm-package.tar.gz ${PACKAGE_DIR}
```

### Air-Gapped Installation
```bash
#!/bin/bash
# install-airgapped.sh

# Verify we're offline
if ping -c 1 google.com &>/dev/null; then
  echo "WARNING: Network connectivity detected. Expected air-gapped environment."
  exit 1
fi

# Load Docker images
docker load -i /media/transfer/images/vllm.tar
docker load -i /media/transfer/images/nginx.tar

# Copy models
cp -r /media/transfer/models/* /mnt/ai-models/

# Copy and customize configuration
cp /media/transfer/configs/* /opt/llm/
# Edit /opt/llm/.env with local settings

# Start services
cd /opt/llm && docker compose up -d

# Verify
curl http://localhost:8000/health
```

## API Gateway Configuration

### NGINX Configuration
```nginx
upstream vllm_backend {
    server vllm:8000;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name llm.internal.company.com;

    ssl_certificate /etc/nginx/certs/server.crt;
    ssl_certificate_key /etc/nginx/certs/server.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # Request size limit
    client_max_body_size 10M;

    location /v1/ {
        proxy_pass http://vllm_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Connection "";

        # Streaming support
        proxy_buffering off;
        proxy_read_timeout 300s;

        # Authentication (example: header-based)
        if ($http_authorization = "") {
            return 401;
        }
    }

    location /health {
        proxy_pass http://vllm_backend/health;
        access_log off;
    }

    location /metrics {
        proxy_pass http://vllm_backend/metrics;
        # Restrict to monitoring network
        allow 10.0.0.0/8;
        deny all;
    }
}
```

## Best Practices

### Security
1. Always use TLS for API endpoints
2. Implement API key or token authentication
3. Restrict network access to internal networks only
4. Enable audit logging for all requests
5. Regularly update container images and models
6. Use secrets management for API keys

### Performance
1. Size hardware for 20-30% headroom above expected load
2. Use NVMe SSDs for model storage
3. Enable persistence mode for GPUs
4. Monitor GPU memory and utilization continuously
5. Implement request queuing for load spikes

### Operations
1. Implement health checks and automatic restarts
2. Set up comprehensive monitoring and alerting
3. Create runbooks for common operations
4. Test backup and recovery procedures
5. Document all configuration changes

### Scalability
1. Use load balancing for multiple replicas
2. Implement horizontal scaling based on metrics
3. Plan capacity 3-6 months ahead
4. Consider model-level sharding for large deployments

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Insufficient VRAM | Model loading fails | Size GPU properly, use quantization |
| No health checks | Silent failures | Implement liveness/readiness probes |
| No rate limiting | Resource exhaustion | Configure per-user/IP limits |
| Missing TLS | Data exposure | Always use HTTPS |
| Outdated images | Security vulnerabilities | Regular update schedule |
| No monitoring | Blind to issues | Comprehensive observability |

## Deployment Checklist

### Pre-Deployment
- [ ] Hardware meets requirements (GPU, RAM, storage)
- [ ] Network configuration complete
- [ ] TLS certificates obtained
- [ ] API authentication configured
- [ ] Models downloaded and verified

### Deployment
- [ ] Container images loaded
- [ ] Configuration files in place
- [ ] Environment variables set
- [ ] Services started successfully
- [ ] Health checks passing

### Post-Deployment
- [ ] Smoke tests successful
- [ ] Monitoring active
- [ ] Alerting configured
- [ ] Documentation updated
- [ ] Stakeholders notified

This skill provides comprehensive guidance for deploying production-grade local AI infrastructure with complete data sovereignty.
