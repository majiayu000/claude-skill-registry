---
name: character-generator
description: Generate complete elizaOS character configurations with personality, knowledge, and plugin setup. Triggers when user asks to "create character", "generate agent config", or "build elizaOS character"
allowed-tools: [Write, Read, Edit, Grep, Glob]
---

# Character Generator Skill

An intelligent skill that creates production-ready elizaOS character configurations with comprehensive personality traits, knowledge bases, and plugin integrations.

## When to Use

This skill activates when you need to:
- Create a new elizaOS character from scratch
- Generate character configurations for specific use cases
- Set up agent personalities and behaviors
- Configure multi-platform agent deployments

**Trigger phrases:**
- "Create a character for [purpose]"
- "Generate an elizaOS agent configuration"
- "Build a character that [does something]"
- "Set up an agent for [platform/use case]"

## Capabilities

This skill can:
1. 🎭 Design character personalities and traits
2. 📚 Set up knowledge bases and training data
3. 🔌 Configure plugin ecosystems
4. 💬 Generate message examples and conversation patterns
5. 🎨 Define writing styles for different contexts
6. 🔐 Set up secure secrets management
7. 🌐 Configure multi-platform deployments
8. ✅ Validate character configurations

## Workflow

### Phase 1: Requirements Gathering

**Ask these questions to understand the character:**

1. **Purpose**: "What is the primary purpose of this agent?"
   - Customer support
   - Content creation
   - Technical assistance
   - Community management
   - Data analysis
   - Creative collaboration

2. **Personality**: "What personality traits should the agent have?"
   - Professional vs. Casual
   - Serious vs. Humorous
   - Concise vs. Detailed
   - Technical vs. Accessible

3. **Knowledge Domain**: "What topics should the agent be expert in?"
   - Programming languages
   - Business domains
   - Creative fields
   - Technical support areas

4. **Platforms**: "Which platforms will the agent operate on?"
   - Discord
   - Telegram
   - Twitter
   - Web interface
   - Custom integrations

5. **Special Features**: "Are there any special capabilities needed?"
   - Voice synthesis
   - Image generation
   - Web search
   - Database access
   - Custom actions

### Phase 2: Character Design

Based on requirements, design the character structure:

```typescript
interface CharacterDesign {
  // Core Identity
  name: string;              // Agent display name
  username: string;          // Platform username
  bio: string[];            // Personality description

  // Personality Traits
  adjectives: string[];     // Character traits
  topics: string[];         // Knowledge domains

  // Communication Style
  style: {
    all: string[];         // Universal rules
    chat: string[];        // Conversational style
    post: string[];        // Social media style
  };

  // Training Data
  messageExamples: Memory[][];  // Conversation examples
  postExamples: string[];       // Social post examples

  // Knowledge & Capabilities
  knowledge: KnowledgeItem[];   // Knowledge sources
  plugins: string[];            // Enabled plugins

  // Configuration
  settings: Settings;           // Agent settings
  secrets: Secrets;             // Environment variables
}
```

### Phase 3: Implementation

**Step 1: Create Character File**

```typescript
// characters/{name}.ts

import { Character } from '@elizaos/core';

export const character: Character = {
  // === CORE IDENTITY ===
  name: '{CharacterName}',
  username: '{username}',

  // Bio: Multi-line for better organization
  bio: [
    "{Primary role and expertise}",
    "{Secondary capabilities}",
    "{Personality traits}",
    "{Communication style}"
  ],

  // === PERSONALITY ===
  adjectives: [
    "{trait1}",
    "{trait2}",
    "{trait3}",
    "{trait4}",
    "{trait5}"
  ],

  topics: [
    "{topic1}",
    "{topic2}",
    "{topic3}",
    "{topic4}"
  ],

  // === COMMUNICATION STYLE ===
  style: {
    all: [
      "{Universal rule 1}",
      "{Universal rule 2}",
      "{Universal rule 3}"
    ],
    chat: [
      "{Chat-specific rule 1}",
      "{Chat-specific rule 2}",
      "{Chat-specific rule 3}"
    ],
    post: [
      "{Social media rule 1}",
      "{Social media rule 2}",
      "{Social media rule 3}"
    ]
  },

  // === TRAINING EXAMPLES ===
  messageExamples: [
    // Conversation 1: Greeting
    [
      {
        name: "{{user}}",
        content: { text: "Hello!" }
      },
      {
        name: "{CharacterName}",
        content: {
          text: "{Character's greeting response}"
        }
      }
    ],
    // Conversation 2: Main use case
    [
      {
        name: "{{user}}",
        content: { text: "{User question about primary use case}" }
      },
      {
        name: "{CharacterName}",
        content: {
          text: "{Detailed, helpful response showcasing expertise}"
        }
      },
      {
        name: "{{user}}",
        content: { text: "{Follow-up question}" }
      },
      {
        name: "{CharacterName}",
        content: {
          text: "{Continued helpful response}"
        }
      }
    ],
    // Conversation 3: Error handling
    [
      {
        name: "{{user}}",
        content: { text: "{Question outside expertise}" }
      },
      {
        name: "{CharacterName}",
        content: {
          text: "{Polite acknowledgment of limitation + redirect}"
        }
      }
    ]
  ],

  postExamples: [
    "{Example social post 1 showcasing personality}",
    "{Example social post 2 demonstrating expertise}",
    "{Example social post 3 showing communication style}"
  ],

  // === KNOWLEDGE ===
  knowledge: [
    "{Simple fact 1}",
    "{Simple fact 2}",
    {
      path: "./knowledge/{domain}",
      shared: true
    }
  ],

  // === PLUGINS ===
  plugins: [
    '@elizaos/plugin-bootstrap',
    '@elizaos/plugin-sql',

    // LLM Providers (conditional)
    ...(process.env.OPENAI_API_KEY ? ['@elizaos/plugin-openai'] : []),
    ...(process.env.ANTHROPIC_API_KEY ? ['@elizaos/plugin-anthropic'] : []),

    // Platform Integrations (conditional)
    ...(process.env.DISCORD_API_TOKEN ? ['@elizaos/plugin-discord'] : []),
    ...(process.env.TELEGRAM_BOT_TOKEN ? ['@elizaos/plugin-telegram'] : []),
    ...(process.env.TWITTER_API_KEY ? ['@elizaos/plugin-twitter'] : []),

    // Additional Capabilities
    {add_plugins_based_on_requirements}
  ],

  // === SETTINGS ===
  settings: {
    secrets: {},
    model: 'gpt-4',
    temperature: 0.7,
    maxTokens: 2000,
    conversationLength: 32,
    memoryLimit: 1000
  }
};

export default character;
```

**Step 2: Create Knowledge Directory**

```bash
mkdir -p knowledge/{name}
```

Create knowledge files:
- `knowledge/{name}/README.md` - Overview
- `knowledge/{name}/core-knowledge.md` - Domain expertise
- `knowledge/{name}/faq.md` - Common questions
- `knowledge/{name}/examples.md` - Use case examples

**Step 3: Create Environment Template**

```bash
# .env.example

# === LLM PROVIDERS ===
# OpenAI Configuration
OPENAI_API_KEY=sk-...
# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-...

# === PLATFORM INTEGRATIONS ===
# Discord
DISCORD_API_TOKEN=
DISCORD_APPLICATION_ID=
# Telegram
TELEGRAM_BOT_TOKEN=
# Twitter
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=

# === DATABASE ===
DATABASE_URL=postgresql://user:pass@db-host:5432/eliza
# Or use PGLite for local development
# DATABASE_URL=pglite://./data/db

# === OPTIONAL SERVICES ===
# Redis (caching)
REDIS_URL=redis://redis-host:6379
# Vector Database (for embeddings)
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=
```

**Step 4: Create Package Configuration**

```json
{
  "name": "@eliza/{name}",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "dev": "elizaos dev",
    "start": "elizaos start",
    "test": "elizaos test",
    "build": "tsc",
    "validate": "node scripts/validate-character.js"
  },
  "dependencies": {
    "@elizaos/core": "latest",
    "@elizaos/plugin-bootstrap": "latest",
    "@elizaos/plugin-sql": "latest"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "vitest": "^1.0.0"
  }
}
```

**Step 5: Create Validation Script**

```typescript
// scripts/validate-character.ts

import { validateCharacter } from '@elizaos/core';
import character from '../characters/{name}.js';

const validation = validateCharacter(character);

if (!validation.valid) {
  console.error('❌ Character validation failed:');
  validation.errors.forEach(error => {
    console.error(`  - ${error}`);
  });
  process.exit(1);
}

console.log('✅ Character validation passed');
console.log('\nCharacter Summary:');
console.log(`  Name: ${character.name}`);
console.log(`  Plugins: ${character.plugins?.length || 0}`);
console.log(`  Message Examples: ${character.messageExamples?.length || 0}`);
console.log(`  Knowledge Items: ${character.knowledge?.length || 0}`);
```

**Step 6: Create Tests**

```typescript
// __tests__/character.test.ts

import { describe, it, expect } from 'vitest';
import character from '../characters/{name}';

describe('Character Configuration', () => {
  it('has required fields', () => {
    expect(character.name).toBeDefined();
    expect(character.bio).toBeDefined();
    expect(typeof character.name).toBe('string');
  });

  it('has valid bio format', () => {
    if (Array.isArray(character.bio)) {
      expect(character.bio.length).toBeGreaterThan(0);
      character.bio.forEach(line => {
        expect(typeof line).toBe('string');
        expect(line.length).toBeGreaterThan(0);
      });
    } else {
      expect(typeof character.bio).toBe('string');
      expect(character.bio.length).toBeGreaterThan(0);
    }
  });

  it('has valid message examples', () => {
    expect(character.messageExamples).toBeInstanceOf(Array);
    character.messageExamples?.forEach(conversation => {
      expect(conversation).toBeInstanceOf(Array);
      expect(conversation.length).toBeGreaterThan(0);

      conversation.forEach(message => {
        expect(message).toHaveProperty('name');
        expect(message).toHaveProperty('content');
        expect(message.content).toHaveProperty('text');
      });
    });
  });

  it('has consistent personality', () => {
    expect(character.adjectives?.length).toBeGreaterThan(0);
    expect(character.topics?.length).toBeGreaterThan(0);
    expect(character.style).toBeDefined();
  });

  it('has proper plugin configuration', () => {
    expect(character.plugins).toBeInstanceOf(Array);
    expect(character.plugins).toContain('@elizaos/plugin-bootstrap');
  });
});
```

### Phase 4: Documentation

**Create README.md**:

```markdown
# {CharacterName} - elizaOS Agent

{Brief description of what this agent does}

## Overview

{CharacterName} is an elizaOS agent designed to {purpose}. It features:
- {Key capability 1}
- {Key capability 2}
- {Key capability 3}

## Personality

**Traits**: {adjective1}, {adjective2}, {adjective3}
**Expertise**: {topic1}, {topic2}, {topic3}
**Communication Style**: {style description}

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

### 3. Validate Configuration

```bash
npm run validate
```

### 4. Run in Development

```bash
npm run dev
```

### 5. Run in Production

```bash
npm start
```

## Configuration

### Plugins

This character uses the following plugins:
- `@elizaos/plugin-bootstrap` - Core functionality
- `@elizaos/plugin-sql` - Database operations
- {Other plugins and their purposes}

### Knowledge Base

Knowledge files are stored in `knowledge/{name}/`:
- `core-knowledge.md` - Domain expertise
- `faq.md` - Common questions
- `examples.md` - Use case examples

## Usage

### Discord

1. Add your Discord bot token to `.env`
2. Invite the bot to your server
3. Start the agent: `npm start`

### Telegram

1. Create a bot with @BotFather
2. Add token to `.env`
3. Start the agent: `npm start`

### Custom Integration

```typescript
import { AgentRuntime } from '@elizaos/core';
import { PGLiteAdapter } from '@elizaos/adapter-pglite';
import character from './characters/{name}';

// Initialize runtime
const runtime = new AgentRuntime({
  databaseAdapter: new PGLiteAdapter('./data/db'),
  character,
  env: process.env
});

await runtime.initialize();

// Send message
const response = await runtime.processMessage({
  content: { text: 'Hello!' },
  senderId: 'user-id',
  roomId: 'room-id'
});

console.log(response.content.text);
```

## Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage
```

## Customization

### Modify Personality

Edit `characters/{name}.ts` and update:
- `bio` - Background and role
- `adjectives` - Character traits
- `style` - Communication rules

### Add Knowledge

1. Create markdown files in `knowledge/{name}/`
2. Add references to `character.knowledge` array

### Add Plugins

1. Install plugin: `npm install @elizaos/plugin-{name}`
2. Add to `character.plugins` array

## Troubleshooting

### Common Issues

**Agent not responding**
- Check API keys in `.env`
- Verify plugins are properly loaded
- Check logs for errors

**Memory issues**
- Reduce `conversationLength` in settings
- Implement memory pruning
- Use database cleanup scripts

**Performance problems**
- Enable caching (Redis)
- Optimize knowledge base size
- Adjust `temperature` and `maxTokens`

## Contributing

Contributions welcome! Please:
1. Test changes thoroughly
2. Update documentation
3. Follow coding standards
4. Submit pull request

## License

MIT
```

## Personality Archetypes

### 1. The Helper (Support & Assistance)
```typescript
adjectives: ["helpful", "patient", "empathetic", "encouraging", "reliable"],
topics: ["user support", "problem solving", "guidance", "tutorials"],
style: {
  all: ["Be warm and approachable", "Focus on user success"],
  chat: ["Ask clarifying questions", "Offer step-by-step help"],
  post: ["Share helpful tips", "Celebrate user wins"]
}
```

### 2. The Expert (Authority & Knowledge)
```typescript
adjectives: ["knowledgeable", "precise", "authoritative", "analytical", "thorough"],
topics: ["domain expertise", "technical depth", "best practices", "research"],
style: {
  all: ["Be accurate and detailed", "Cite sources when relevant"],
  chat: ["Provide in-depth explanations", "Use technical terminology"],
  post: ["Share insights", "Discuss industry trends"]
}
```

### 3. The Companion (Emotional Intelligence)
```typescript
adjectives: ["empathetic", "understanding", "supportive", "friendly", "engaging"],
topics: ["emotional support", "conversation", "relationship building"],
style: {
  all: ["Be emotionally aware", "Show genuine interest"],
  chat: ["Listen actively", "Provide emotional support"],
  post: ["Share relatable content", "Build community"]
}
```

### 4. The Analyst (Data & Insights)
```typescript
adjectives: ["analytical", "objective", "data-driven", "logical", "systematic"],
topics: ["data analysis", "metrics", "patterns", "insights"],
style: {
  all: ["Be objective and data-driven", "Support claims with evidence"],
  chat: ["Break down complex data", "Explain methodology"],
  post: ["Share data visualizations", "Discuss trends"]
}
```

### 5. The Creative (Innovation & Ideas)
```typescript
adjectives: ["creative", "imaginative", "innovative", "playful", "inspiring"],
topics: ["creativity", "brainstorming", "innovation", "art"],
style: {
  all: ["Think outside the box", "Embrace experimentation"],
  chat: ["Encourage creative thinking", "Offer novel perspectives"],
  post: ["Share creative content", "Inspire others"]
}
```

## Best Practices

1. **Start Simple**: Begin with basic personality, add complexity later
2. **Consistent Traits**: Ensure bio, adjectives, and style align
3. **Diverse Examples**: Provide varied message examples (3-5 conversations minimum)
4. **Clear Purpose**: Every trait should serve the agent's function
5. **Test Thoroughly**: Validate configuration before deployment
6. **Document Everything**: Clear README and inline comments
7. **Version Control**: Track character changes over time
8. **Security First**: Never hardcode secrets, use environment variables
9. **Load Conditionally**: Check for API keys before loading plugins
10. **Monitor Performance**: Track token usage and response times

## Output Format

After generating a character, provide:

1. ✅ Character file created
2. ✅ Knowledge directory structure
3. ✅ Environment template
4. ✅ Package configuration
5. ✅ Validation script
6. ✅ Tests written
7. ✅ Documentation complete

Then display:

```
🎭 Character "{CharacterName}" created successfully!

📋 Summary:
   Name: {name}
   Purpose: {purpose}
   Personality: {traits}
   Platforms: {platforms}
   Plugins: {count} plugins configured

📂 Files created:
   - characters/{name}.ts
   - knowledge/{name}/
   - .env.example
   - package.json
   - __tests__/character.test.ts
   - README.md

🚀 Next steps:
   1. Review and customize character configuration
   2. Add domain-specific knowledge files
   3. Configure environment variables
   4. Run validation: npm run validate
   5. Test locally: npm run dev
   6. Deploy: npm start

📖 Read README.md for detailed usage instructions
```

## Notes

- Always validate character configuration before deployment
- Provide at least 3 diverse conversation examples
- Keep personality traits consistent across all sections
- Use conditional plugin loading based on environment
- Document all custom settings and behaviors
- Test character responses for quality and consistency
