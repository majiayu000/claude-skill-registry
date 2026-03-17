---
name: fair-forge-lambda
description: Generate AWS Lambda deployment boilerplate for Fair-Forge modules. Use when deploying Fair-Forge metrics (BestOf, Toxicity, Bias), runners (test execution against AI systems), or generators (synthetic dataset creation) to AWS Lambda. Handles local wheel installation since fair-forge is not on PyPI.
---

# Fair-Forge Lambda Deployment

Generate AWS Lambda container deployment for Fair-Forge modules. Builds wheel from local repository since fair-forge is not available on PyPI.

## Supported Modules

| Module Type | Extras | Use Case |
|-------------|--------|----------|
| Metrics | `bestof`, `toxicity`, `bias`, `context`, `conversational`, `humanity` | Evaluate AI responses |
| Runners | `runners` | Execute tests against AI systems |
| Generators | `generators`, `generators-alquimia` | Create synthetic test datasets |

## Workflow

### 1. Generate Lambda Project

Create the deployment directory:

```
examples/{module}/aws-lambda/
├── Dockerfile       # Multi-stage build: wheel + Lambda
├── handler.py       # Lambda entrypoint
├── run.py           # Business logic (customize this)
├── requirements.txt # Additional runtime dependencies
├── README.md        # API documentation
└── scripts/
    ├── deploy.sh
    ├── update.sh
    └── cleanup.sh
```

Copy templates from `assets/templates/` and scripts from `scripts/`.

### 2. CRITICAL: Update Dockerfile Paths

The Dockerfile is built with the **repo root as context** (not the aws-lambda directory). You MUST update the COPY paths to use full paths from the repo root:

```dockerfile
# UPDATE these lines in the Dockerfile:
COPY examples/{module}/aws-lambda/requirements.txt .
COPY examples/{module}/aws-lambda/handler.py examples/{module}/aws-lambda/run.py ${LAMBDA_TASK_ROOT}/
```

For example, for generators:
```dockerfile
COPY examples/generators/aws-lambda/requirements.txt .
COPY examples/generators/aws-lambda/handler.py examples/generators/aws-lambda/run.py ${LAMBDA_TASK_ROOT}/
```

### 3. Implement run.py

Edit `run.py` with your module logic. See reference docs for patterns:

- `references/metrics.md` - Metrics implementation patterns
- `references/runners.md` - Runners implementation patterns
- `references/generators.md` - Generators implementation patterns

### 4. Generate README.md

After deployment, create a README.md using the template from `assets/templates/README.md`. Replace the placeholders:

| Placeholder | Example |
|-------------|---------|
| `{MODULE_NAME}` | `Generators` |
| `{INVOKE_URL}` | `https://xxx.execute-api.us-east-2.amazonaws.com/run` |
| `{MODULE_EXTRA}` | `generators` |
| `{AWS_REGION}` | `us-east-2` |

See the template for full list of placeholders.

### 5. Deploy

From `examples/{module}/aws-lambda/`:

```bash
./scripts/deploy.sh {extra-name} us-east-2
```

Examples:
```bash
./scripts/deploy.sh bestof us-east-2      # BestOf metric
./scripts/deploy.sh runners us-east-2     # Runners module
./scripts/deploy.sh generators us-east-2  # Generators module
```

### 6. Update / Cleanup

```bash
./scripts/update.sh {extra-name} us-east-2   # Rebuild and update
./scripts/cleanup.sh {extra-name} us-east-2  # Remove all resources
```

## Dynamic LLM Connector API

For modules that use LLMs (generators, metrics), the API uses a dynamic connector pattern that allows runtime selection of LLM provider:

### Request Format

```json
{
  "connector": {
    "class_path": "langchain_groq.chat_models.ChatGroq",
    "params": {
      "model": "qwen/qwen3-32b",
      "api_key": "your-api-key",
      "temperature": 0.7
    }
  },
  "context": "...",
  "config": {...}
}
```

### Supported Connectors

| Provider | class_path |
|----------|-----------|
| Groq | `langchain_groq.chat_models.ChatGroq` |
| OpenAI | `langchain_openai.chat_models.ChatOpenAI` |
| Google Gemini | `langchain_google_genai.chat_models.ChatGoogleGenerativeAI` |
| Ollama | `langchain_ollama.chat_models.ChatOllama` |

### Connector Factory Implementation

The `create_llm_connector` function uses dynamic imports to instantiate any LangChain chat model:

```python
import importlib

def create_llm_connector(connector_config: dict):
    class_path = connector_config.get("class_path")
    params = connector_config.get("params", {})

    module_path, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)

    return cls(**params)
```

## Dockerfile Build Process

Multi-stage build:
1. **Builder stage**: Builds fair-forge wheel from local source
2. **Final stage**: Pre-installs numpy/scipy, installs wheel with module extras, copies handler

### numpy/scipy Compilation Workaround

The Lambda base image lacks compilers needed to build numpy/scipy from source. The Dockerfile pre-installs specific versions with pre-built manylinux wheels:

```dockerfile
# Pre-install numpy and scipy with manylinux wheels
RUN pip install "numpy==1.26.4" "scipy==1.14.1" --target "${LAMBDA_TASK_ROOT}"

# Constraints file prevents pip from upgrading these
RUN echo "numpy==1.26.4" > /tmp/constraints.txt && \
    echo "scipy==1.14.1" >> /tmp/constraints.txt

# Install fair-forge with constraints
ARG MODULE_EXTRA=bestof
RUN WHEEL=$(ls /tmp/*.whl) && pip install "${WHEEL}[${MODULE_EXTRA}]" --target "${LAMBDA_TASK_ROOT}" -c /tmp/constraints.txt
```

## Bundled Resources

### scripts/
- `deploy.sh` - Full deployment (ECR + Lambda + API Gateway)
- `update.sh` - Rebuild and update Lambda
- `cleanup.sh` - Remove all AWS resources

### assets/templates/
- `Dockerfile` - Multi-stage Lambda container build
- `handler.py` - Lambda entrypoint wrapper
- `run.py` - Business logic template (customize this)
- `requirements.txt` - Runtime dependencies with all LLM providers
- `README.md` - API documentation template with placeholders

### references/
- `metrics.md` - Metrics module implementation patterns
- `runners.md` - Runners module implementation patterns
- `generators.md` - Generators module implementation patterns

## Lambda Configuration

Default settings (adjust in deploy.sh):
- **Timeout**: 300 seconds (5 minutes)
- **Memory**: 2048 MB
- **Python**: 3.11

## Troubleshooting

### "file does not exist" during Docker build
The Dockerfile paths for `requirements.txt`, `handler.py`, and `run.py` must be updated to use full paths from the repo root. See step 2 above.

### scipy/numpy compilation errors
The template Dockerfile includes a workaround that pre-installs numpy and scipy from manylinux wheels. If you see errors like "NumPy requires GCC >= 9.3", ensure you're using the updated Dockerfile template.

### Wheel path duplication error
If you see `/tmp//tmp/filename.whl`, the wheel installation command is incorrect. Use:
```dockerfile
RUN WHEEL=$(ls /tmp/*.whl) && pip install "${WHEEL}[${MODULE_EXTRA}]" ...
```
NOT:
```dockerfile
RUN pip install "/tmp/$(ls /tmp/*.whl)[${MODULE_EXTRA}]" ...
```

### langchain import errors (e.g., "cannot import name 'ModelProfile'")
This indicates a version mismatch between langchain packages. Pin compatible versions in `requirements.txt`:
```
langchain-core>=0.3.0,<0.4.0
langchain-groq>=0.2.0,<0.3.0
```

### tiktoken Rust compiler error
If you see "can't find Rust compiler" when installing langchain-openai, pin tiktoken to a version with pre-built wheels:
```
tiktoken>=0.7.0,<0.8.0
```
