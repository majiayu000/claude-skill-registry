---
name: lobe-chat
version: "1.0.0"
description: LobeChat - Open-source AI agent workspace with multi-provider LLM support, plugin system, knowledge base RAG, 505+ agents, and self-hosting options via Docker/Vercel
---

# LobeChat Skill

**LobeChat** is an open-source, modern AI agent workspace that provides a unified platform for conversing with multiple AI systems. It supports 20+ LLM providers (OpenAI, Claude, Gemini, Ollama), features a plugin marketplace with 40+ plugins, an agent marketplace with 505+ pre-built agents, knowledge base with RAG, and flexible deployment options.

**Key Value Proposition**: Deploy a private, customizable AI chat interface with multi-model support, extensible plugins, file upload/RAG capabilities, and beautiful modern UI - all self-hosted or cloud-deployed.

## When to Use This Skill

- Deploying LobeChat via Docker, Vercel, or other platforms
- Configuring multi-provider LLM support (OpenAI, Claude, Ollama)
- Creating custom agents with system prompts
- Developing LobeChat plugins
- Setting up knowledge base and file upload features
- Configuring authentication (Clerk, NextAuth)
- Troubleshooting deployment or configuration issues

## When NOT to Use This Skill

- For generic OpenAI/Claude API usage (use provider-specific skills)
- For other chat interfaces like Open WebUI (different project)
- For building AI agents from scratch (LobeChat is a ready-made solution)
- For mobile app development (LobeChat is web-based with PWA)

---

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       LobeChat Workspace                         │
│                     (Next.js + TypeScript)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  AI Providers │    │    Agents     │    │   Plugins     │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • OpenAI      │    │ • 505+ pre-   │    │ • 40+ plugins │
│ • Claude      │    │   built       │    │ • Web search  │
│ • Gemini      │    │ • Custom      │    │ • Code exec   │
│ • Ollama      │    │ • Marketplace │    │ • Weather     │
│ • Azure       │    │ • System      │    │ • Custom SDK  │
│ • Groq        │    │   prompts     │    │               │
│ • 20+ more    │    │               │    │               │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Knowledge Base│    │   Features    │    │  Deployment   │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • File upload │    │ • TTS/STT     │    │ • Docker      │
│ • RAG         │    │ • Vision      │    │ • Vercel      │
│ • pgvector    │    │ • Artifacts   │    │ • Alibaba     │
│ • Embeddings  │    │ • DALL-E      │    │ • Zeabur      │
│               │    │ • MCP         │    │ • Self-host   │
└───────────────┘    └───────────────┘    └───────────────┘
```

### Project Statistics

| Metric | Value |
|--------|-------|
| GitHub Stars | 70.1k+ |
| Forks | 14.4k+ |
| Contributors | 313+ |
| Total Commits | 8,248+ |
| Plugins | 40+ |
| Agents | 505+ |
| Languages | TypeScript (98.5%) |

### Supported AI Providers

| Provider | Models | Notes |
|----------|--------|-------|
| **OpenAI** | GPT-4o, GPT-4, GPT-3.5 | Primary provider |
| **Anthropic** | Claude 3.5, Claude 3 | Full model support |
| **Google** | Gemini Pro, Gemini Flash | Vision support |
| **Azure OpenAI** | All OpenAI models | Enterprise option |
| **Ollama** | Llama, Mistral, etc. | Local models |
| **Groq** | Llama, Mixtral | Fast inference |
| **Moonshot** | Kimi models | Chinese provider |
| **01 AI** | Yi models | Chinese provider |
| **Together AI** | Open source models | Many models |
| **ChatGLM** | GLM-4 | Chinese provider |
| **Perplexity** | pplx-* models | Search-enhanced |
| **Mistral** | Mistral models | European provider |
| **DeepSeek** | DeepSeek models | Coding focused |

---

## Quick Start

### One-Click Vercel Deployment

```bash
# Deploy to Vercel (simplest option)
# Click "Deploy" button on GitHub repo or:
npx vercel --prod
```

### Docker Deployment (Client-Side DB)

```bash
# Quick start with local storage
docker run -d \
  --name lobe-chat \
  -p 3210:3210 \
  -e OPENAI_API_KEY=sk-your-key \
  lobehub/lobe-chat
```

### Docker Deployment (Server-Side DB)

```bash
# Full deployment with PostgreSQL
docker run -d \
  --name lobe-chat-db \
  -p 3210:3210 \
  -e DATABASE_URL=postgres://user:pass@host:5432/lobechat \
  -e KEY_VAULTS_SECRET=$(openssl rand -base64 32) \
  -e OPENAI_API_KEY=sk-your-key \
  lobehub/lobe-chat-database
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  lobe-chat:
    image: lobehub/lobe-chat-database
    ports:
      - "3210:3210"
    environment:
      - DATABASE_URL=postgres://postgres:password@db:5432/lobechat
      - KEY_VAULTS_SECRET=${KEY_VAULTS_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - NEXT_AUTH_SECRET=${NEXT_AUTH_SECRET}
    depends_on:
      - db

  db:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=lobechat
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
# Generate secrets
export KEY_VAULTS_SECRET=$(openssl rand -base64 32)
export NEXT_AUTH_SECRET=$(openssl rand -base64 32)
export OPENAI_API_KEY=sk-your-key

# Start services
docker-compose up -d
```

---

## Environment Variables

### Core Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes (or other provider) |
| `ACCESS_CODE` | Password protection | No |
| `PROXY_URL` | Proxy for API requests | No |

### Database Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_SERVICE_MODE` | `client` or `server` | `client` |
| `DATABASE_URL` | PostgreSQL connection string | - |
| `DATABASE_DRIVER` | `node` or `neon` | `node` |
| `KEY_VAULTS_SECRET` | Encryption key for user data | Required for server mode |

### Provider API Keys

```bash
# Set provider keys as needed
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
AZURE_API_KEY=...
GROQ_API_KEY=gsk_...
OLLAMA_PROXY_URL=http://localhost:11434
```

### Feature Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `FEATURE_FLAGS` | Enable/disable features | `+webSearch,-imageGen` |
| `DEFAULT_AGENT_CONFIG` | Default agent settings | JSON config |
| `SYSTEM_AGENT` | System function models | JSON config |
| `PLUGINS_INDEX_URL` | Custom plugin marketplace | URL |
| `AGENTS_INDEX_URL` | Custom agent marketplace | URL |

### Authentication

```bash
# NextAuth (Docker)
NEXT_AUTH_SECRET=$(openssl rand -base64 32)
NEXTAUTH_URL=https://your-domain.com

# Clerk (Vercel)
CLERK_SECRET_KEY=sk_...
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
```

---

## Custom Agents

### Creating an Agent

1. **Open Agent Panel** → Click "+" to create new agent
2. **Configure Settings**:
   - Name and description
   - Avatar and tags
   - System prompt
   - Model selection
   - Temperature and parameters

### Agent Configuration Structure

```json
{
  "meta": {
    "name": "Code Assistant",
    "description": "Expert programming assistant",
    "avatar": "🤖",
    "tags": ["coding", "development"]
  },
  "config": {
    "systemRole": "You are an expert programmer...",
    "model": "gpt-4o",
    "params": {
      "temperature": 0.3,
      "max_tokens": 4096
    },
    "plugins": ["web-search", "code-interpreter"],
    "tts": {
      "enabled": true,
      "voice": "alloy"
    }
  }
}
```

### System Prompt Best Practices

```markdown
# Role Definition
You are [role name], an expert in [domain].

# Core Competencies
- [Skill 1]
- [Skill 2]
- [Skill 3]

# Guidelines
1. [Guideline 1]
2. [Guideline 2]

# Response Format
- Use markdown formatting
- Include code examples when relevant
- Cite sources when possible

# Constraints
- Do not [constraint 1]
- Always [requirement 1]
```

### Submitting to Agent Marketplace

1. Fork [lobe-chat-agents](https://github.com/lobehub/lobe-chat-agents)
2. Create agent JSON in `agents/` directory
3. Add metadata and system prompt
4. Submit pull request

---

## Plugin Development

### Plugin Architecture

```
Plugin
├── manifest.json      # Plugin definition
├── api/
│   └── endpoint.ts    # Server-side handlers
└── ui/
    └── index.tsx      # Optional frontend UI
```

### Quick Start with Template

```bash
# Clone official template
git clone https://github.com/lobehub/chat-plugin-template.git
cd chat-plugin-template
npm install
npm run dev
# Runs on http://localhost:3400
```

### Plugin Manifest

```json
{
  "identifier": "weather-plugin",
  "version": "1.0.0",
  "api": [
    {
      "url": "http://localhost:3400/api/weather",
      "name": "getWeather",
      "description": "Get current weather for a location",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "City name"
          }
        },
        "required": ["city"]
      }
    }
  ],
  "ui": {
    "url": "http://localhost:3400",
    "height": 400,
    "width": 600
  },
  "gateway": "http://localhost:3400/api/gateway"
}
```

### API Handler Example

```typescript
// api/weather.ts
import { createErrorResponse } from '@lobehub/chat-plugin-sdk';

export const runtime = 'edge';

export async function POST(req: Request) {
  try {
    const { city } = await req.json();

    // Fetch weather data
    const response = await fetch(
      `https://api.weather.com/v1/current?city=${city}`
    );
    const data = await response.json();

    return Response.json({
      temperature: data.temp,
      condition: data.condition,
      city: city
    });
  } catch (error) {
    return createErrorResponse(500, 'Failed to fetch weather');
  }
}
```

### Frontend UI Communication

```typescript
// ui/index.tsx
import { fetchPluginMessage } from '@lobehub/chat-plugin-sdk/client';

export default function PluginUI() {
  const [message, setMessage] = useState(null);

  useEffect(() => {
    fetchPluginMessage().then(setMessage);
  }, []);

  return (
    <div>
      {message && <pre>{JSON.stringify(message, null, 2)}</pre>}
    </div>
  );
}
```

### Plugin SDK

```bash
# Install SDK
npm install @lobehub/chat-plugin-sdk @lobehub/chat-plugins-gateway
```

```typescript
// Using gateway for local development
import { createGateway } from '@lobehub/chat-plugins-gateway';

const gateway = createGateway({
  plugins: ['./manifest.json']
});
```

### Publishing Plugin

1. Deploy to Vercel/Docker
2. Fork [lobe-chat-plugins](https://github.com/lobehub/lobe-chat-plugins)
3. Add plugin entry to index
4. Submit pull request

---

## Knowledge Base & RAG

### Requirements

- Server-side database deployment
- PostgreSQL with pgvector extension
- Embedding model configured

### Database Setup

```sql
-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Vectors stored automatically by LobeChat
```

### Supported File Types

- Documents: PDF, DOCX, TXT, MD
- Images: PNG, JPG, WEBP (with vision)
- Audio: MP3, WAV (with transcription)
- Video: MP4 (with transcription)

### Using Knowledge Base

1. **Upload Files** → Drag and drop or click upload
2. **Create Collection** → Organize related files
3. **Attach to Agent** → Link knowledge base to agent
4. **Query** → Agent uses RAG to answer from documents

### Environment Variables for RAG

```bash
# Embedding provider (optional, uses OpenAI by default)
EMBEDDING_MODEL=text-embedding-3-small

# Vector search settings
VECTOR_SEARCH_LIMIT=10
VECTOR_SEARCH_THRESHOLD=0.7
```

---

## MCP (Model Context Protocol)

LobeChat supports MCP for connecting to external tools and data sources.

### Enabling MCP

```bash
# Environment variable
MCP_ENABLED=true
```

### MCP Server Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "/path/to/files"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    }
  }
}
```

---

## Features

### Voice Conversation (TTS/STT)

```bash
# Enable TTS
TTS_ENABLED=true
TTS_PROVIDER=openai  # or edge, elevenlabs

# Enable STT
STT_ENABLED=true
STT_PROVIDER=openai  # or browser
```

### Image Generation

```bash
# DALL-E
DALL_E_ENABLED=true

# Image settings
AI_IMAGE_DEFAULT_IMAGE_NUM=4
```

### Artifacts

Artifacts enable real-time creation and visualization of:
- SVG graphics
- HTML/CSS pages
- React components
- Interactive visualizations

### Chain of Thought

Visualize model reasoning steps for transparency in complex tasks.

### Branching Conversations

Create non-linear dialogue trees, exploring multiple conversation paths.

---

## Deployment Options

### Vercel (Recommended for Quick Start)

1. Fork repository
2. Import to Vercel
3. Set environment variables
4. Deploy

### Docker

```bash
# Basic
docker pull lobehub/lobe-chat
docker run -p 3210:3210 lobehub/lobe-chat

# With database
docker pull lobehub/lobe-chat-database
docker run -p 3210:3210 \
  -e DATABASE_URL=... \
  lobehub/lobe-chat-database
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lobe-chat
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lobe-chat
  template:
    metadata:
      labels:
        app: lobe-chat
    spec:
      containers:
      - name: lobe-chat
        image: lobehub/lobe-chat-database
        ports:
        - containerPort: 3210
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: lobe-secrets
              key: database-url
```

### Other Platforms

- **Zeabur**: One-click deployment
- **Sealos**: Kubernetes-based
- **Alibaba Cloud**: China-optimized
- **Railway**: Simple hosting

---

## Authentication

### NextAuth (Docker/Self-hosted)

```bash
# Required
NEXT_AUTH_SECRET=$(openssl rand -base64 32)
NEXTAUTH_URL=https://your-domain.com

# OAuth Providers
GITHUB_ID=...
GITHUB_SECRET=...

GOOGLE_ID=...
GOOGLE_SECRET=...
```

### Clerk (Vercel)

```bash
CLERK_SECRET_KEY=sk_...
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_WEBHOOK_SECRET=whsec_...
```

### Access Code (Simple)

```bash
# Password protection
ACCESS_CODE=your-secret-code
```

---

## Troubleshooting

### API Connection Issues

```
Error: Failed to connect to OpenAI
```

**Solutions**:
1. Verify API key is correct
2. Check `PROXY_URL` if behind firewall
3. Ensure network allows API access

### Database Connection Failed

```
Error: Connection refused to PostgreSQL
```

**Solutions**:
1. Verify `DATABASE_URL` format
2. Check PostgreSQL is running
3. Ensure pgvector extension installed
4. Verify network/firewall settings

### Plugin Not Loading

```
Error: Plugin manifest not found
```

**Solutions**:
1. Verify manifest URL is accessible
2. Check CORS settings on plugin server
3. Verify gateway configuration for local plugins

### Knowledge Base Search Fails

```
Error: Vector search failed
```

**Solutions**:
1. Ensure pgvector extension enabled
2. Check embedding model configuration
3. Verify file was properly indexed

### Authentication Errors

```
Error: NextAuth session invalid
```

**Solutions**:
1. Regenerate `NEXT_AUTH_SECRET`
2. Clear browser cookies
3. Verify `NEXTAUTH_URL` matches domain

---

## Best Practices

### Security

1. **Always use `ACCESS_CODE`** for public deployments
2. **Generate strong secrets** with `openssl rand -base64 32`
3. **Use HTTPS** in production
4. **Rotate API keys** regularly
5. **Enable authentication** for multi-user setups

### Performance

1. **Use server-side DB** for production
2. **Configure caching** for static assets
3. **Use CDN** via `NEXT_PUBLIC_ASSET_PREFIX`
4. **Optimize model selection** based on task

### Agents

1. **Clear system prompts** improve response quality
2. **Lower temperature** (0.3-0.5) for factual tasks
3. **Higher temperature** (0.7-0.9) for creative tasks
4. **Use plugins** for external data access

---

## Resources

### Official Links
- [Website](https://lobehub.com)
- [Documentation](https://lobehub.com/docs)
- [GitHub](https://github.com/lobehub/lobe-chat)
- [Discord](https://discord.gg/lobeHub)

### Marketplaces
- [Plugin Store](https://lobehub.com/plugins)
- [Agent Store](https://lobehub.com/agents)

### Development
- [Plugin Template](https://github.com/lobehub/chat-plugin-template)
- [Plugin SDK](https://github.com/lobehub/chat-plugin-sdk)
- [Agent Repository](https://github.com/lobehub/lobe-chat-agents)
- [Plugin Repository](https://github.com/lobehub/lobe-chat-plugins)

### Related Projects
- [Lobe SD Theme](https://github.com/lobehub/sd-webui-lobe-theme)
- [Lobe i18n](https://github.com/lobehub/lobe-i18n)
- [Lobe Commit](https://github.com/lobehub/lobe-commit)

---

## Version History

- **1.0.0** (2026-01-13): Initial skill release
  - Complete deployment guide (Docker, Vercel, Compose)
  - All environment variables documented
  - Custom agent creation workflow
  - Plugin development with SDK
  - Knowledge base and RAG setup
  - MCP integration
  - Authentication options (Clerk, NextAuth)
  - 20+ AI provider configurations
  - Troubleshooting guide
