---
name: Bankr Dev - Project Templates
description: This skill should be used when the user asks to "scaffold a Bankr project", "create new Bankr bot", "build a Bankr web service", "create Bankr dashboard", "build Bankr CLI tool", "project structure for Bankr", "Bankr project types", or needs guidance on directory structures and templates for different types of Bankr API integrations.
version: 1.0.0
---

# Bankr Project Templates

Directory structures and templates for Bankr API projects.

## Available Templates

| Template | Use Case | Key Features |
|----------|----------|--------------|
| **bot** | Automated tasks | Polling loop, scheduler, status streaming |
| **web-service** | HTTP APIs | REST endpoints, webhooks, async handling |
| **dashboard** | Web UIs | Frontend + backend, real-time updates |
| **cli** | Command-line tools | Subcommands, interactive prompts |

## Bot Template

For automated trading bots, price monitors, alert systems, and scheduled tasks.

### Directory Structure

```
{project-name}/
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── index.ts           # Main entry point with scheduler
│   ├── bankr-client.ts    # Bankr API client (from bankr-client-patterns skill)
│   ├── types.ts           # TypeScript interfaces
│   └── config.ts          # Configuration loading
└── scripts/
    └── run.sh             # Convenience script
```

### Key Features

- **Polling loop**: Configurable interval for recurring checks
- **Status streaming**: Real-time job status updates
- **Error handling**: Automatic retries with backoff
- **Environment config**: `.env` based configuration
- **Graceful shutdown**: Handles SIGINT/SIGTERM

### Use Cases

- Price monitoring and alerts
- Automated trading strategies
- Portfolio rebalancing
- Scheduled market analysis
- DCA automation

### Entry Point Pattern (index.ts)

```typescript
import { execute } from "./bankr-client";

const INTERVAL = 60000; // 1 minute

async function runBot() {
  console.log("Starting Bankr bot...");

  while (true) {
    try {
      const result = await execute(
        "Check ETH price",
        (msg) => console.log("Status:", msg)
      );

      if (result.status === "completed") {
        console.log("Result:", result.response);
        // Add your logic here
      }
    } catch (error) {
      console.error("Error:", error);
    }

    await new Promise(r => setTimeout(r, INTERVAL));
  }
}

runBot();
```

---

## Web Service Template

For HTTP APIs that wrap or extend Bankr functionality.

### Directory Structure

```
{project-name}/
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── index.ts           # Server entry point
│   ├── server.ts          # Express/Fastify server setup
│   ├── routes/
│   │   ├── health.ts      # Health check endpoint
│   │   └── bankr.ts       # Bankr proxy/extension routes
│   ├── bankr-client.ts    # Bankr API client
│   ├── types.ts           # TypeScript interfaces
│   └── config.ts          # Configuration loading
└── scripts/
    └── run.sh
```

### Key Features

- **REST API endpoints**: Clean API design
- **Request validation**: Input sanitization
- **Async job handling**: Non-blocking operations
- **Webhook support**: Callbacks on job completion
- **Rate limiting**: Prevent abuse
- **CORS**: Cross-origin support

### Use Cases

- API gateway for Bankr
- Custom trading APIs
- Webhook integrations
- Backend for mobile apps
- Microservice architecture

### Additional Dependencies

```json
{
  "dependencies": {
    "express": "^4.18.0"
  }
}
```

Or for Fastify:

```json
{
  "dependencies": {
    "fastify": "^4.25.0"
  }
}
```

---

## Dashboard Template

For web UIs with portfolio tracking, market analysis, or monitoring.

### Directory Structure

```
{project-name}/
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
├── server/
│   ├── index.ts           # Backend server
│   ├── bankr-client.ts    # Bankr API client
│   ├── routes/
│   │   └── api.ts         # API routes for frontend
│   └── types.ts
├── public/
│   ├── index.html         # Main HTML page
│   ├── styles.css         # Basic styles
│   └── app.js             # Frontend JavaScript
└── scripts/
    └── run.sh
```

### Key Features

- **Simple frontend**: HTML/CSS/JS (no build step required)
- **Backend API**: Express server for Bankr operations
- **Real-time updates**: Polling for status changes
- **Portfolio display**: Token balances and values
- **Market data**: Price charts and analysis

### Use Cases

- Portfolio tracking dashboard
- Trading interface
- Market monitoring
- Position management
- Analytics dashboard

### Frontend Pattern (app.js)

```javascript
async function checkPrice() {
  const response = await fetch('/api/price/ETH');
  const data = await response.json();
  document.getElementById('eth-price').textContent = data.price;
}

setInterval(checkPrice, 30000);
checkPrice();
```

---

## CLI Template

For command-line tools with subcommands and interactive features.

### Directory Structure

```
{project-name}/
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── index.ts           # CLI entry with commander.js
│   ├── commands/
│   │   ├── trade.ts       # Trading commands
│   │   ├── price.ts       # Price query commands
│   │   └── status.ts      # Job status commands
│   ├── bankr-client.ts    # Bankr API client
│   └── types.ts
└── scripts/
    └── run.sh
```

### Key Features

- **Commander.js**: CLI framework with subcommands
- **Interactive prompts**: User input when needed
- **Progress indicators**: Status during polling
- **Colored output**: Better UX
- **Help system**: Auto-generated from commands

### Use Cases

- Personal trading tool
- Scripting and automation
- DevOps integration
- Quick price checks
- Batch operations

### Additional Dependencies

```json
{
  "dependencies": {
    "commander": "^12.0.0"
  }
}
```

### CLI Pattern (index.ts)

```typescript
import { program } from "commander";
import { price } from "./commands/price";
import { trade } from "./commands/trade";

program
  .name("bankr-cli")
  .description("CLI for Bankr operations")
  .version("1.0.0");

program
  .command("price <token>")
  .description("Get token price")
  .action(price);

program
  .command("trade <action> <amount> <token>")
  .description("Execute a trade")
  .option("-c, --chain <chain>", "Target chain", "base")
  .action(trade);

program.parse();
```

---

## Choosing a Template

| Need | Recommended Template |
|------|---------------------|
| Automated recurring tasks | **bot** |
| HTTP API for integrations | **web-service** |
| Visual interface | **dashboard** |
| Terminal-based tool | **cli** |
| Price alerts | **bot** |
| Trading API | **web-service** |
| Portfolio viewer | **dashboard** |
| Quick trades | **cli** |

## Common Files

All templates share common files. Load the `bankr-client-patterns` skill for:
- `bankr-client.ts` - Complete API client
- `package.json` - Base dependencies
- `tsconfig.json` - TypeScript config
- `.env.example` - Environment template
- `.gitignore` - Standard ignores

## Next Steps After Scaffolding

1. **Install dependencies**: `bun install` or `npm install`
2. **Configure API key**: Copy `.env.example` to `.env` and add `BANKR_API_KEY`
3. **Customize**: Modify the template for your use case
4. **Run**: `bun dev` or `npm run dev` for development
5. **Build**: `bun run build` or `npm run build` for production
