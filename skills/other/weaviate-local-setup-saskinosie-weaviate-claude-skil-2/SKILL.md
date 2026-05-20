---
name: weaviate-local-setup
description: Set up and manage a local Weaviate instance using Docker
version: 1.0.0
dependencies: []
---

# Weaviate Local Setup Skill

Run Weaviate locally using Docker for development, testing, and avoiding network restrictions in Claude Desktop/Web.

## Why Use Local Weaviate?

**Benefits:**
- No network restrictions in Claude Desktop/Web
- Free (no cloud costs)
- Full control over data and configuration
- Fast development/testing cycles
- Works offline
- No API key management for cloud instances

**Best for:**
- Development and testing
- Learning Weaviate
- Working in Claude Desktop with network restrictions
- Privacy-sensitive projects

## Prerequisites

**Required:**
- Docker Desktop installed and running
- Available ports: 8080 (Weaviate), 8081 (optional for Weaviate Console)
- Python 3.8+ installed

**Optional (for specific vectorizers):**
- OpenAI API key (for text2vec-openai)
- Cohere API key (for text2vec-cohere)
- Anthropic API key (for generative-anthropic)

## Python Environment Setup

**IMPORTANT: Do this FIRST before using any Weaviate skills!**

Claude will create a virtual environment and install dependencies to avoid conflicts with your system Python.

### Step 1: Create Virtual Environment

```bash
# Navigate to the weaviate-claude-skills directory
cd ~/Documents/weaviate-claude-skills

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install weaviate-client python-dotenv

# Optional: Install additional packages for specific vectorizers
pip install openai  # If using OpenAI vectorizer
pip install cohere  # If using Cohere vectorizer
```

**Or install everything at once:**
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation

```python
import subprocess
import sys

# Check if dependencies are installed
try:
    import weaviate
    from dotenv import load_dotenv
    print("✅ All required packages are installed!")
except ImportError as e:
    print(f"❌ Missing package: {e}")
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                          "weaviate-client", "python-dotenv"])
    print("✅ Dependencies installed successfully!")
```

### When Using Claude

**Claude will check and ensure dependencies are installed before running any Weaviate code.**

If you see errors about missing packages, Claude will:
1. Check if the virtual environment exists
2. Create it if needed
3. Install required dependencies
4. Proceed with your request

**Pro Tip:** Keep the virtual environment activated throughout your Claude session for best results.

## Quick Start

### Option 1: Basic Setup (No API Keys Required)

Use Weaviate's built-in vectorizer (no external API needed):

```bash
# Start Weaviate with transformers (runs locally, no API key)
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -p 50051:50051 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  -e DEFAULT_VECTORIZER_MODULE='text2vec-transformers' \
  -e ENABLE_MODULES='text2vec-transformers' \
  -e TRANSFORMERS_INFERENCE_API='http://t2v-transformers:8080' \
  -e CLUSTER_HOSTNAME='node1' \
  semitechnologies/weaviate:1.28.1

# Start the transformers module
docker run -d \
  --name t2v-transformers \
  -e ENABLE_CUDA=0 \
  semitechnologies/transformers-inference:sentence-transformers-multi-qa-MiniLM-L6-cos-v1
```

**Connection:**
```
WEAVIATE_URL=localhost:8080
WEAVIATE_API_KEY=  # Leave empty for local
```

### Option 2: With OpenAI Vectorizer

Use OpenAI embeddings (requires OpenAI API key):

```bash
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -p 50051:50051 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  -e DEFAULT_VECTORIZER_MODULE='text2vec-openai' \
  -e ENABLE_MODULES='text2vec-openai,generative-openai' \
  -e CLUSTER_HOSTNAME='node1' \
  semitechnologies/weaviate:1.28.1
```

**Connection (.env):**
```
WEAVIATE_URL=localhost:8080
WEAVIATE_API_KEY=  # Leave empty
OPENAI_API_KEY=your-openai-key-here
```

### Option 3: Docker Compose (Recommended for Production)

See `docker-compose.yml` in this folder (created separately).

```bash
# Start Weaviate
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f weaviate

# Stop Weaviate
docker-compose down

# Stop and remove data
docker-compose down -v
```

## Docker Commands Reference

### Container Management

```bash
# Start Weaviate
docker start weaviate

# Stop Weaviate
docker stop weaviate

# Restart Weaviate
docker restart weaviate

# Check if running
docker ps | grep weaviate

# View logs
docker logs weaviate

# Follow logs in real-time
docker logs -f weaviate

# Remove container (keeps data)
docker rm weaviate

# Remove container and data volume
docker rm -v weaviate
```

### Health Checks

```bash
# Check if Weaviate is ready
curl http://localhost:8080/v1/.well-known/ready

# Check Weaviate metadata
curl http://localhost:8080/v1/meta

# Expected response:
# {"hostname":"http://[::]:8080","modules":{...},"version":"1.28.1"}
```

### Data Persistence

Weaviate data is stored in Docker volumes. To persist data across container restarts:

```bash
# Create a named volume
docker volume create weaviate-data

# Run with named volume
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -v weaviate-data:/var/lib/weaviate \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  semitechnologies/weaviate:1.28.1

# List volumes
docker volume ls

# Inspect volume
docker volume inspect weaviate-data

# Backup data (export volume to tar)
docker run --rm -v weaviate-data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/weaviate-backup.tar.gz /data

# Restore data (import tar to volume)
docker run --rm -v weaviate-data:/data -v $(pwd):/backup \
  ubuntu tar xzf /backup/weaviate-backup.tar.gz -C /
```

## Python Connection Code

Once Weaviate is running locally, connect using:

```python
import weaviate
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to local Weaviate (no authentication)
client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051
)

try:
    print("✅ Connected to local Weaviate!")

    # Check if ready
    if client.is_ready():
        print("🟢 Weaviate is ready")

        # Get metadata
        meta = client.get_meta()
        print(f"📦 Version: {meta['version']}")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    client.close()
```

**Alternative connection with API key header (if enabled):**

```python
client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051,
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    }
)
```

## Environment Variables for Local Setup

Update your `.env` file:

```bash
# Local Weaviate Connection
WEAVIATE_URL=localhost:8080
WEAVIATE_API_KEY=  # Leave empty for local instances

# Vectorizer API Keys (only needed if using these vectorizers)
OPENAI_API_KEY=your-openai-api-key
COHERE_API_KEY=your-cohere-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
HUGGINGFACE_API_KEY=your-huggingface-api-key
```

## Available Vectorizer Modules

### Text Vectorizers

| Module | Description | API Key Required | Best For |
|--------|-------------|------------------|----------|
| `text2vec-transformers` | Local embeddings using transformers | No | Development, offline work |
| `text2vec-openai` | OpenAI embeddings (ada-002) | Yes (OpenAI) | Production, high quality |
| `text2vec-cohere` | Cohere embeddings | Yes (Cohere) | Multilingual, semantic search |
| `text2vec-huggingface` | HuggingFace models | Optional | Custom models |
| `text2vec-palm` | Google PaLM embeddings | Yes (Google) | Google ecosystem |

### Multi-Modal Vectorizers

| Module | Description | API Key Required |
|--------|-------------|------------------|
| `multi2vec-clip` | OpenAI CLIP (text + images) | No (local) |
| `multi2vec-bind` | ImageBind (text, image, audio) | No (local) |
| `img2vec-neural` | Image-only vectorization | No (local) |

### Generative Modules (for RAG)

| Module | Description | API Key Required |
|--------|-------------|------------------|
| `generative-openai` | GPT-3.5/GPT-4 for RAG | Yes (OpenAI) |
| `generative-cohere` | Cohere Generate | Yes (Cohere) |
| `generative-anthropic` | Claude for RAG | Yes (Anthropic) |
| `generative-palm` | Google PaLM | Yes (Google) |

## Docker Image Tags

**Stable versions:**
- `semitechnologies/weaviate:1.28.1` (latest stable)
- `semitechnologies/weaviate:1.27.0`
- `semitechnologies/weaviate:1.26.0`

**Preview/Beta:**
- `semitechnologies/weaviate:preview`

**Module images:**
- `semitechnologies/transformers-inference:sentence-transformers-multi-qa-MiniLM-L6-cos-v1`
- `semitechnologies/transformers-inference:sentence-transformers-all-MiniLM-L6-v2`
- `semitechnologies/multi2vec-clip:sentence-transformers-clip-ViT-B-32`

## Common Issues & Troubleshooting

### Port Already in Use

```bash
# Check what's using port 8080
lsof -i :8080

# Kill the process (if needed)
kill -9 <PID>

# Or run Weaviate on a different port
docker run -d -p 8081:8080 --name weaviate ...
```

### Container Won't Start

```bash
# Check logs
docker logs weaviate

# Remove and recreate
docker rm -f weaviate
docker run ...
```

### Cannot Connect from Python

```python
# Make sure you're using the correct connection method for local
client = weaviate.connect_to_local()  # NOT connect_to_weaviate_cloud()

# Check Weaviate is actually running
# curl http://localhost:8080/v1/.well-known/ready
```

### Data Not Persisting

Make sure you're using a volume:

```bash
docker run -v weaviate-data:/var/lib/weaviate ...
```

### Module Not Available

Enable the module in the `ENABLE_MODULES` environment variable:

```bash
-e ENABLE_MODULES='text2vec-openai,generative-openai'
```

## Performance Tuning

### Memory Limits

```bash
# Set memory limits
docker run -d \
  --name weaviate \
  --memory="4g" \
  --memory-swap="4g" \
  ...
```

### CPU Limits

```bash
# Limit CPUs
docker run -d \
  --name weaviate \
  --cpus="2.0" \
  ...
```

### Query Defaults

```bash
# Increase default query limit
-e QUERY_DEFAULTS_LIMIT=100

# Set maximum query results
-e QUERY_MAXIMUM_RESULTS=10000
```

## Weaviate Console (Optional UI)

Run the Weaviate Console for a web UI:

```bash
docker run -d \
  --name weaviate-console \
  -p 8081:8080 \
  semitechnologies/weaviate-console:latest

# Access at: http://localhost:8081
# Enter Weaviate URL: http://localhost:8080
```

## Migration: Cloud to Local

### Export from Cloud

```python
import weaviate
import json

# Connect to cloud
cloud_client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=weaviate.auth.Auth.api_key(os.getenv("WEAVIATE_API_KEY"))
)

collection = cloud_client.collections.get("YourCollection")

# Export all objects
objects = []
for item in collection.iterator():
    objects.append({
        "properties": item.properties,
        "vector": item.vector
    })

# Save to file
with open("export.json", "w") as f:
    json.dump(objects, f)

cloud_client.close()
```

### Import to Local

```python
# Connect to local
local_client = weaviate.connect_to_local()

# Create collection (same schema as cloud)
# ... create collection code ...

# Import data
collection = local_client.collections.get("YourCollection")

with collection.batch.dynamic() as batch:
    for obj in objects:
        batch.add_object(properties=obj["properties"], vector=obj.get("vector"))

local_client.close()
```

## Best Practices

1. **Use Docker Compose** for complex setups with multiple modules
2. **Always use volumes** for data persistence
3. **Monitor logs** during development: `docker logs -f weaviate`
4. **Backup regularly** using volume exports
5. **Use transformers module** for development (no API costs)
6. **Switch to OpenAI** for production (better quality)
7. **Set memory limits** to prevent OOM crashes
8. **Test connections** before importing large datasets

## Integration with Other Skills

This skill works perfectly with:
- `weaviate-connection` - Just use `localhost:8080` as the URL
- `weaviate-collection-manager` - Create collections on local instance
- `weaviate-data-ingestion` - Upload data locally (faster, no network limits)
- `weaviate-query-agent` - Query local data (faster responses)

## Example Workflow

```bash
# 1. Start Weaviate locally
docker run -d --name weaviate -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  semitechnologies/weaviate:1.28.1

# 2. Verify it's running
curl http://localhost:8080/v1/.well-known/ready

# 3. Update .env
# WEAVIATE_URL=localhost:8080
# WEAVIATE_API_KEY=

# 4. Use other skills normally
# Claude: "Connect to my local Weaviate instance"
# Claude: "Create a collection called Documents"
# Claude: "Upload these 100 PDFs"
# Claude: "Search for information about X"
```

## Resources

- [Weaviate Docker Installation](https://weaviate.io/developers/weaviate/installation/docker-compose)
- [Weaviate Modules](https://weaviate.io/developers/weaviate/modules)
- [Docker Documentation](https://docs.docker.com/)
- [Weaviate Python Client](https://weaviate.io/developers/weaviate/client-libraries/python)

---

**Built for the Weaviate Skills Collection**

*Questions? Check the main README or Weaviate documentation.*
