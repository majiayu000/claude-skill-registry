---
name: lobe-vidol
version: "1.0.0"
description: LobeVidol - Virtual idol creation platform with MMD dance support, VRM character customization, multi-provider LLM integration, and interactive 3D conversations
---

# LobeVidol Skill

**LobeVidol** (Vidol Studio) is an open-source virtual idol creation platform that enables anyone to create, customize, and interact with 3D virtual characters. It combines conversational AI with MMD (MikuMikuDance) animation support, VRM model customization, and multi-provider LLM integration for immersive virtual idol experiences.

**Key Value Proposition**: Create virtual idols with exquisite UI design, MMD dance choreography, VRM character customization, and seamless AI-powered conversations - all through an accessible web interface or self-hosted deployment.

## When to Use This Skill

- Deploying LobeVidol via Vercel or self-hosted
- Configuring AI model providers (OpenAI, Claude, Ollama, 20+ providers)
- Creating custom virtual characters with VRM models
- Setting up MMD dance choreography and stages
- Configuring character personalities and touch responses
- Integrating TTS/STT for voice conversations
- Publishing characters or dances to the marketplace
- Troubleshooting deployment or configuration issues

## When NOT to Use This Skill

- For LobeChat (different project - chat-focused, not idol-focused)
- For general MMD editing (use MikuMikuDance directly)
- For VRM model creation (use VRoid Studio or Blender)
- For AI model API usage without virtual idols (use provider-specific skills)

---

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     LobeVidol / Vidol Studio                     │
│                     (Next.js + TypeScript)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  AI Providers │    │   Characters  │    │    Dances     │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • OpenAI      │    │ • VRM models  │    │ • MMD/VMD     │
│ • Claude      │    │ • Personality │    │ • PMX stages  │
│ • Gemini      │    │ • Touch resp. │    │ • Choreograph │
│ • Ollama      │    │ • Voice (TTS) │    │ • Mixamo lib  │
│ • 20+ more    │    │ • Marketplace │    │ • Marketplace │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   3D Engine   │    │   Features    │    │  Deployment   │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • Three.js    │    │ • Text chat   │    │ • Vercel      │
│ • three-vrm   │    │ • Video chat  │    │ • Self-host   │
│ • mmd-parser  │    │ • TTS/STT     │    │ • PWA         │
│ • Animations  │    │ • Streaming   │    │ • Docker      │
└───────────────┘    └───────────────┘    └───────────────┘
```

### Project Statistics

| Metric | Value |
|--------|-------|
| GitHub Stars | 887+ |
| Forks | 122+ |
| Contributors | Multiple |
| Total Commits | 865+ |
| Primary Language | TypeScript (99.5%) |
| License | Apache 2.0 |

### Supported AI Providers (22+)

| Provider | Type | Notes |
|----------|------|-------|
| **OpenAI** | Cloud | GPT-4, GPT-3.5 series |
| **Anthropic** | Cloud | Claude 3.5, Claude 3 |
| **Google Gemini** | Cloud | Gemini Pro, Flash |
| **Azure OpenAI** | Cloud | Enterprise option |
| **Ollama** | Local | Run models locally |
| **Groq** | Cloud | Fast inference |
| **DeepSeek** | Cloud | Coding focused |
| **Moonshot AI** | Cloud | Chinese provider |
| **OpenRouter** | Cloud | Multi-model gateway |
| **Together AI** | Cloud | Open source models |
| **Perplexity** | Cloud | Search-enhanced |
| **Amazon Bedrock** | Cloud | AWS managed |
| **Baichuan** | Cloud | Chinese provider |
| **MiniMax** | Cloud | Chinese provider |
| **Zhipu AI** | Cloud | Chinese provider |
| **Tongyi Qianwen** | Cloud | Alibaba Cloud |
| **Tencent Hunyuan** | Cloud | Chinese provider |
| **iFlytek Xinghuo** | Cloud | Chinese provider |
| **Wenxin Qianfan** | Cloud | Baidu |
| **SiliconCloud** | Cloud | Cloud service |
| **Fireworks AI** | Cloud | Fast inference |
| **GitHub Models** | Cloud | GitHub integration |

---

## Quick Start

### Prerequisites

- Node.js 18+ or Bun (recommended)
- Git
- API key for at least one AI provider

### Installation

```bash
# Clone repository
git clone https://github.com/lobehub/lobe-vidol.git
cd lobe-vidol

# Install dependencies (Bun recommended)
bun install
# Or with npm
npm install

# Start development server
bun dev
# Or with npm
npm run dev
```

### Access

Open `http://localhost:3000` in your browser.

### Live Demo

Try without installation: https://vidol.lobehub.com

---

## Configuration

### Environment Variables

Create `.env.local` file:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-xxx
OPENAI_PROXY_URL=  # Optional proxy

# Azure OpenAI (alternative)
AZURE_API_KEY=xxx
AZURE_ENDPOINT=https://xxx.openai.azure.com

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-xxx

# Google Gemini
GOOGLE_API_KEY=xxx

# Ollama (local models)
OLLAMA_PROXY_URL=http://localhost:11434

# OpenRouter (multi-provider)
OPENROUTER_API_KEY=sk-or-xxx

# Voice Services
OPENAI_TTS_API_KEY=sk-xxx  # For TTS
EDGE_TTS_ENABLED=true      # Microsoft Edge TTS
```

### Provider Configuration in UI

1. Click Settings (gear icon)
2. Navigate to "Language Model" section
3. Select provider from dropdown
4. Enter API key
5. Choose model variant
6. Test connection

---

## Character Creation

### VRM Model Support

LobeVidol uses VRM (Virtual Reality Model) format for 3D characters:

**Getting VRM Models:**
- **VRoid Hub**: https://hub.vroid.com - Free community models
- **VRoid Studio**: Create your own characters
- **Blender**: Convert existing 3D models with VRM addon
- **Unity**: Export VRM using UniVRM plugin

### Character Configuration

```typescript
// Character configuration structure
interface Character {
  // Basic Info
  name: string;
  avatar: string;          // Image URL
  description: string;
  greeting: string;        // Initial message
  gender: 'male' | 'female' | 'other';
  category: string;

  // AI Personality
  systemRole: string;      // LLM system prompt

  // Voice Settings
  tts: {
    enabled: boolean;
    voice: string;         // Voice ID
    speed: number;
    pitch: number;
  };

  // 3D Model
  model: {
    url: string;           // VRM file URL
    scale: number;
    position: [number, number, number];
  };

  // Touch Responses
  touch: {
    head: string[];        // Responses when head touched
    face: string[];
    arm: string[];
    chest: string[];
    leg: string[];
  };
}
```

### System Role (Personality)

The `systemRole` field defines the character's personality:

```markdown
You are Luna, a cheerful virtual idol who loves singing and dancing.

## Personality Traits
- Energetic and optimistic
- Loves discussing music and dance
- Speaks with enthusiasm and occasional cute expressions
- Always supportive and encouraging

## Speech Patterns
- Uses casual, friendly language
- Occasionally adds "~" at end of sentences
- Expresses emotions openly

## Background
- A rising virtual idol from Vidol Studio
- Dreams of performing at major virtual concerts
- Enjoys interacting with fans and learning new dances
```

### Touch Response Configuration

Configure how characters respond to interaction:

```json
{
  "touch": {
    "head": [
      "Ehehe~ That tickles!",
      "Are you petting me? How sweet~",
      "My hair took forever to style!"
    ],
    "face": [
      "W-what are you doing?",
      "My cheeks are getting warm...",
      "Do I have something on my face?"
    ],
    "arm": [
      "Want to hold hands?",
      "My arm? Is something there?",
      "Let's dance together!"
    ]
  }
}
```

---

## Dance & Animation

### MMD Support

LobeVidol supports MikuMikuDance (MMD) content:

**Supported Formats:**
- **VMD**: Vocaloid Motion Data (dance animations)
- **PMX**: Polygon Model eXtended (3D stages)
- **VRMA**: VRM Animation files

### Adding Dances

1. **Prepare Files:**
   - Dance motion file (.vmd)
   - Audio file (.mp3, .wav)
   - Optional: Stage file (.pmx)

2. **Upload via UI:**
   - Navigate to Dance section
   - Click "Upload Dance"
   - Select motion and audio files
   - Configure stage (optional)

3. **Test Dance:**
   - Preview with selected character
   - Adjust timing if needed
   - Save to library

### Built-in Animation Libraries

**Mixamo Integration:**
- Idle animations
- Walking/running
- Gestures and expressions
- Poses for photos

**Dance Presets:**
- Popular MMD choreography
- Various music genres
- Community contributions

### Stage Configuration

```typescript
interface Stage {
  name: string;
  model: string;      // PMX file URL
  scale: number;
  lighting: {
    ambient: string;  // Hex color
    directional: string;
    intensity: number;
  };
  background: {
    type: 'color' | 'image' | 'video';
    value: string;
  };
}
```

---

## Voice Features

### Text-to-Speech (TTS)

**Supported TTS Providers:**

| Provider | Quality | Languages | Cost |
|----------|---------|-----------|------|
| OpenAI Audio | High | Multi | Paid |
| Microsoft Edge | High | Multi | Free |
| Browser TTS | Medium | Varies | Free |

**Configuration:**
```bash
# OpenAI TTS
OPENAI_TTS_API_KEY=sk-xxx
OPENAI_TTS_MODEL=tts-1-hd

# Edge TTS (free)
EDGE_TTS_ENABLED=true
EDGE_TTS_VOICE=en-US-AriaNeural
```

### Speech-to-Text (STT)

Enable voice input for conversations:

```bash
# OpenAI Whisper
OPENAI_STT_API_KEY=sk-xxx
OPENAI_STT_MODEL=whisper-1

# Browser STT (free)
BROWSER_STT_ENABLED=true
```

### Voice Selection

```typescript
// Available voices (Edge TTS examples)
const voices = {
  english: [
    'en-US-AriaNeural',      // Female, friendly
    'en-US-GuyNeural',       // Male, casual
    'en-GB-SoniaNeural',     // Female, British
  ],
  japanese: [
    'ja-JP-NanamiNeural',    // Female, natural
    'ja-JP-KeitaNeural',     // Male, natural
  ],
  chinese: [
    'zh-CN-XiaoxiaoNeural',  // Female, friendly
    'zh-CN-YunxiNeural',     // Male, narrator
  ]
};
```

---

## Marketplace

### Character Marketplace

Browse and download community characters:

1. Open Character Market in sidebar
2. Browse by category or search
3. Preview character (3D model, personality)
4. Download to local library

### Publishing Characters

1. Create character with complete configuration
2. Click "Upload to Market"
3. Fill metadata (tags, description)
4. Submit for review
5. GitHub issue created automatically
6. Community review process
7. Merged into marketplace

### Dance Marketplace

Access MMD dance resources:

- Various choreography styles
- Multiple music genres
- Stage environments
- Community contributions

---

## Deployment

### Vercel Deployment (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/lobehub/lobe-vidol)

1. Click "Deploy with Vercel"
2. Connect GitHub account
3. Configure environment variables
4. Deploy

### Docker Deployment

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
# Build and run
docker build -t lobe-vidol .
docker run -p 3000:3000 \
  -e OPENAI_API_KEY=sk-xxx \
  lobe-vidol
```

### Docker Compose

```yaml
version: '3.8'
services:
  lobe-vidol:
    build: .
    ports:
      - "3000:3000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
```

### Self-Hosted Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 2 GB | 4 GB |
| Storage | 5 GB | 20 GB |
| Network | Broadband | Low latency |

---

## PWA Support

LobeVidol supports Progressive Web App installation:

### Desktop Installation

1. Open https://vidol.lobehub.com in Chrome/Edge
2. Click install icon in address bar
3. Confirm installation
4. Launch from desktop

### Mobile Installation

1. Open in mobile browser (Chrome/Safari)
2. Tap "Share" or menu icon
3. Select "Add to Home Screen"
4. Launch from home screen

### PWA Features

- Offline capable (cached assets)
- Native-like experience
- Push notifications (future)
- Background sync

---

## API Reference

### Chat Endpoint

```typescript
// POST /api/chat
interface ChatRequest {
  messages: Array<{
    role: 'user' | 'assistant' | 'system';
    content: string;
  }>;
  model: string;
  character?: string;  // Character ID
  stream?: boolean;
}

interface ChatResponse {
  content: string;
  model: string;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}
```

### Character API

```typescript
// GET /api/characters
interface CharacterListResponse {
  characters: Character[];
  total: number;
}

// GET /api/characters/:id
interface CharacterResponse {
  character: Character;
}

// POST /api/characters
interface CreateCharacterRequest {
  name: string;
  systemRole: string;
  model: string;  // VRM URL
  // ... other fields
}
```

---

## Troubleshooting

### Common Issues

**VRM Model Not Loading:**
```
Error: Failed to load VRM model
```
- Verify VRM file URL is accessible
- Check CORS settings if hosted externally
- Ensure VRM version compatibility (0.x or 1.0)

**Dance Animation Issues:**
```
Error: VMD file parsing failed
```
- Check file encoding (Japanese characters)
- Verify VMD format compatibility
- Try re-exporting from MMD

**API Connection Errors:**
```
Error: Failed to connect to OpenAI
```
- Verify API key is valid
- Check proxy settings if behind firewall
- Confirm model name is correct

**TTS Not Working:**
```
Error: TTS initialization failed
```
- Enable Edge TTS as fallback
- Check browser permissions for audio
- Verify API key for OpenAI TTS

### Performance Optimization

**3D Rendering:**
- Reduce model polygon count
- Disable shadows on mobile
- Use lower resolution textures

**Network:**
- Enable response streaming
- Cache static assets
- Use CDN for models

---

## Best Practices

### Character Design

1. **Clear Personality**: Define distinct traits in systemRole
2. **Consistent Voice**: Match TTS voice to character personality
3. **Natural Responses**: Include varied touch responses
4. **Quality Model**: Use optimized VRM with proper rigging

### Performance

1. **Optimize Models**: Keep VRM under 20MB
2. **Compress Textures**: Use WebP or compressed PNG
3. **Stream Responses**: Enable for better UX
4. **Cache Assets**: Leverage browser caching

### Security

1. **API Keys**: Never expose in client-side code
2. **Rate Limiting**: Implement for public deployments
3. **Input Validation**: Sanitize user inputs
4. **CORS**: Configure properly for custom domains

---

## Resources

### Official Links

- **Live Demo**: https://vidol.lobehub.com
- **Documentation**: https://docs.vidol.chat
- **GitHub**: https://github.com/lobehub/lobe-vidol
- **Discord**: https://discord.gg/AYFPHvv2jT

### Related Tools

- **VRoid Hub**: https://hub.vroid.com - VRM model library
- **VRoid Studio**: https://vroid.com/studio - Character creator
- **MikuMikuDance**: MMD animation software
- **Mixamo**: https://mixamo.com - Animation library

### Community Resources

- Character marketplace contributions
- Dance marketplace submissions
- Discord community support
- GitHub issues and discussions

---

## Version History

- **Current**: Development active
- **Tech Stack**: Next.js, TypeScript, Three.js, three-vrm
- **License**: Apache 2.0

---

**Last Updated**: 2026-01-13
**Skill Version**: 1.0.0
**Source**: https://github.com/lobehub/lobe-vidol
