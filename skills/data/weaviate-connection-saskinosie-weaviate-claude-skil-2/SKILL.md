---
name: weaviate-connection
description: Connect to local Weaviate vector database and verify connection health
version: 2.0.0
author: Scott Askinosie
dependencies:
  - weaviate-local-setup
---

# Weaviate Connection Skill

This skill helps you connect to a **local Weaviate database** instance running in Docker and verify the connection is healthy.

## Important Note

**This skill is designed for LOCAL Weaviate instances only.** Claude Desktop and Claude Web have network restrictions that prevent connections to external services like Weaviate Cloud.

**To use these skills, you must run Weaviate locally using Docker.** See the `weaviate-local-setup` skill first.

## Purpose

Establish and test connections to local Weaviate vector databases running on localhost.

## When to Use This Skill

- User wants to connect to their local Weaviate database
- User needs to verify their Weaviate connection is working
- User asks to check Weaviate health or status
- After starting Weaviate with Docker

## Prerequisites Check

**BEFORE proceeding, Claude should verify:**

1. **Python environment is set up** (from `weaviate-local-setup` skill)
   - Virtual environment exists at `.venv/`
   - Dependencies are installed

2. **Weaviate Docker container is running**
   - Check with `docker ps | grep weaviate`
   - If not running, guide user to start it

3. **Environment file exists**
   - `.env` file is present
   - Has required variables set

### Automated Prerequisites Check

```python
import subprocess
import sys
import os
from pathlib import Path

def check_prerequisites():
    """Check all prerequisites before connecting to Weaviate"""
    print("🔍 Checking prerequisites...\n")

    all_checks_passed = True

    # Check 1: Virtual environment
    venv_path = Path(".venv")
    if venv_path.exists():
        print("✅ Virtual environment found")
    else:
        print("⚠️  No virtual environment found")
        print("   Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
        print("✅ Virtual environment created")

    # Check 2: Dependencies
    try:
        import weaviate
        from dotenv import load_dotenv
        print("✅ Python dependencies installed")
    except ImportError:
        print("⚠️  Missing dependencies")
        print("   Installing weaviate-client and python-dotenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
                              "weaviate-client", "python-dotenv"])
        print("✅ Dependencies installed")

    # Check 3: Docker container
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    if "weaviate" in result.stdout:
        print("✅ Weaviate Docker container is running")
    else:
        print("❌ Weaviate Docker container not found")
        print("   Please start Weaviate first:")
        print("   cd weaviate-local-setup && docker-compose up -d")
        all_checks_passed = False

    # Check 4: .env file
    if Path(".env").exists():
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found")
        print("   Creating .env from template...")
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ .env file created")
            print("   Please edit .env and add your API keys if needed")
        else:
            print("❌ No .env.example found")
            all_checks_passed = False

    print("\n" + "="*50)
    if all_checks_passed:
        print("✅ All prerequisites met! Ready to connect.")
    else:
        print("❌ Some prerequisites missing. Please resolve them first.")
    print("="*50 + "\n")

    return all_checks_passed

# Run the check
if __name__ == "__main__":
    check_prerequisites()
```

**Claude should run this check automatically when this skill is loaded.**

## Requirements

- Python 3.8+
- weaviate-client library (`pip install weaviate-client`)
- **Local Weaviate instance running in Docker** (see `weaviate-local-setup` skill)
- Docker Desktop running

## Connection Instructions

### Step 1: Ensure Weaviate is Running Locally

Before connecting, verify Weaviate Docker container is running:

```bash
# Check if Weaviate is running
docker ps | grep weaviate

# If not running, start it with docker-compose
cd weaviate-local-setup
docker-compose up -d

# Verify Weaviate is ready
curl http://localhost:8080/v1/.well-known/ready
```

### Step 2: Install Dependencies

```bash
pip install weaviate-client python-dotenv
```

### Step 3: Configure Environment Variables

Update your `.env` file for local connection:

```bash
# .env file
WEAVIATE_URL=localhost:8080
WEAVIATE_API_KEY=  # Leave empty for local instances

# Optional: Only needed if using these vectorizers
OPENAI_API_KEY=your-openai-key
COHERE_API_KEY=your-cohere-key
```

### Step 4: Create Connection Code

**Basic Connection (Recommended):**

```python
import weaviate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to local Weaviate
client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051
)

# Test the connection
try:
    # Check if client is ready
    if client.is_ready():
        print("✅ Connected to local Weaviate successfully!")

        # Get cluster metadata
        meta = client.get_meta()
        print(f"📦 Weaviate version: {meta.get('version', 'unknown')}")

        # List collections
        collections = client.collections.list_all()
        print(f"\n📚 Found {len(collections)} collections:")
        for name, config in collections.items():
            print(f"  - {name}")
    else:
        print("❌ Connection failed - Weaviate not ready")

except Exception as e:
    print(f"❌ Error connecting to Weaviate: {str(e)}")
    print("\n💡 Make sure Weaviate is running:")
    print("   docker ps | grep weaviate")

finally:
    # Always close the connection
    client.close()
```

**Connection with API Headers (for OpenAI/Cohere vectorizers):**

```python
import weaviate
import os
from dotenv import load_dotenv

load_dotenv()

# Connect with API key headers
client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051,
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY"),  # Optional
        "X-Cohere-Api-Key": os.getenv("COHERE_API_KEY")   # Optional
    }
)

try:
    if client.is_ready():
        print("✅ Connected to local Weaviate with API headers!")

except Exception as e:
    print(f"❌ Error: {str(e)}")

finally:
    client.close()
```

### Step 5: Verify Connection Health

After connecting, check:
- ✅ Client is ready (`client.is_ready()`)
- ✅ Can retrieve metadata (`client.get_meta()`)
- ✅ Can list collections (`client.collections.list_all()`)

## Best Practices

1. **Start Docker First**: Always ensure Weaviate container is running before connecting
2. **Use Environment Variables**: Store configuration in `.env` file
3. **Close Connections**: Always close the client when done to prevent memory leaks
4. **Error Handling**: Wrap connection code in try/except blocks
5. **Connection Reuse**: Keep one client instance per session, don't create multiple
6. **Check Docker Status**: Use `docker ps` to verify Weaviate is running

## Common Issues

### Issue: "Connection refused" or "Cannot connect to localhost:8080"
**Solution**: Weaviate Docker container is not running
```bash
# Check if container is running
docker ps | grep weaviate

# Start Weaviate
cd weaviate-local-setup
docker-compose up -d

# Wait 10-15 seconds for startup, then verify
curl http://localhost:8080/v1/.well-known/ready
```

### Issue: "Port 8080 already in use"
**Solution**: Another service is using port 8080
```bash
# Find what's using port 8080
lsof -i :8080

# Either stop that service, or modify docker-compose.yml to use a different port
# Change ports: - "8081:8080" in docker-compose.yml
```

### Issue: "Docker daemon not running"
**Solution**: Start Docker Desktop application

### Issue: "Module not found: weaviate"
**Solution**: Install the client library
```bash
pip install weaviate-client
```

## Environment Variables Template

```bash
# .env file for LOCAL Weaviate
WEAVIATE_URL=localhost:8080
WEAVIATE_API_KEY=  # Leave empty for local

# Optional vectorizer API keys
OPENAI_API_KEY=your-openai-key
COHERE_API_KEY=your-cohere-key
ANTHROPIC_API_KEY=your-anthropic-key
```

## Quick Test Script

Save this as `test_connection.py`:

```python
import weaviate

# Connect to local Weaviate
client = weaviate.connect_to_local()

try:
    if client.is_ready():
        print("✅ Connected successfully!")
        meta = client.get_meta()
        print(f"📦 Version: {meta.get('version')}")
    else:
        print("❌ Not ready")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client.close()
```

Run it:
```bash
python test_connection.py
```

## Next Steps

After establishing connection:
- Use **weaviate-collection-manager** skill to create and manage collections
- Use **weaviate-data-ingestion** skill to add data to collections
- Use **weaviate-query-agent** skill to search and retrieve data

## Additional Resources

- [Weaviate Python Client Docs](https://weaviate.io/developers/weaviate/client-libraries/python)
- [Weaviate Docker Installation](https://weaviate.io/developers/weaviate/installation/docker-compose)
- [Local Weaviate Setup Guide](../weaviate-local-setup/SKILL.md)