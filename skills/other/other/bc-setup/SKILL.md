---
name: bc-setup
description: Set up a BigCommerce development environment — Stencil CLI, API credentials, sandbox stores, Catalyst, and developer tools. Use when starting a new BigCommerce project or configuring development tools.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Development Environment Setup

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/` for the developer center overview
2. Web-search `site:developer.bigcommerce.com stencil cli getting started` for Stencil CLI setup
3. Web-search `bigcommerce sandbox store trial` for sandbox/dev store options

## Developer Account & Store

### Getting Started

- Create a free trial or sandbox store at bigcommerce.com
- Partner/Developer sandbox stores are available through the BigCommerce Partner Program
- Each store has a unique **store hash** (found in the API path or admin URL)

### API Credentials

Create API credentials at Store Admin > Advanced Settings > API Accounts:
- **API Path** — `https://api.bigcommerce.com/stores/{store_hash}/v3/`
- **Client ID** — identifies your application
- **Access Token** — authenticates API requests (`X-Auth-Token` header)
- **Client Secret** — used in OAuth flow for apps
- OAuth **scopes** control access: products, orders, customers, content, etc.

## Stencil CLI

### Installation

```bash
npm install -g @bigcommerce/stencil-cli
```

Requires Node.js 18+ and npm.

### Initializing a Theme

```bash
stencil init
```

Prompts for:
- Store URL (e.g., `https://my-store.mybigcommerce.com`)
- API Token (Stencil-CLI scope token)
- Port for local dev server (default 3000)

Stores config in `.stencil` file (add to `.gitignore`).

### Key Commands

| Command | Description |
|---------|-------------|
| `stencil start` | Start local development server with live reload |
| `stencil bundle` | Bundle theme for upload |
| `stencil push` | Push theme to store (with options to activate) |
| `stencil pull` | Download current live theme |
| `stencil release` | Release theme update |

### Theme Directory Structure

```
cornerstone/                 # Default theme (fork this)
├── assets/
│   ├── scss/                # Stylesheets
│   ├── js/                  # JavaScript modules
│   └── img/                 # Static images
├── templates/
│   ├── layout/              # Master layout templates
│   ├── pages/               # Page templates
│   ├── components/          # Reusable partials
│   └── ...
├── lang/                    # Internationalization JSON
├── config.json              # Theme configuration & variations
├── schema.json              # Theme Editor schema
├── package.json             # Node dependencies
└── .stencil                 # Local CLI config (gitignored)
```

## Catalyst (Headless)

### Setup

```bash
npx create-catalyst-storefront@latest my-store
```

Creates a Next.js 14+ application pre-configured with:
- BigCommerce GraphQL Storefront API integration
- Product listing, detail, cart, and checkout pages
- Authentication flows
- Tailwind CSS styling

Requires: Node.js 18+, BigCommerce store with Storefront API token.

## App Development Setup

### Local Tunnel

For OAuth callback during development:
- Use `ngrok`, `cloudflared`, or similar tunnel
- Expose local port to a public HTTPS URL
- Set callback URL in Dev Tools Portal

### Developer Portal

Register apps at https://devtools.bigcommerce.com/:
- Set OAuth callback URL
- Configure required scopes
- Get Client ID and Client Secret

## Environment Variables

### Common Variables

```
BIGCOMMERCE_STORE_HASH=your_store_hash
BIGCOMMERCE_ACCESS_TOKEN=your_access_token
BIGCOMMERCE_CLIENT_ID=your_client_id
BIGCOMMERCE_CLIENT_SECRET=your_client_secret
BIGCOMMERCE_API_URL=https://api.bigcommerce.com/stores/{store_hash}/v3
```

Store in `.env` file (add to `.gitignore`). Never commit credentials.

## Best Practices

- Use sandbox/trial stores for development — never develop against production
- Store all credentials in environment variables, never in code
- Add `.stencil` and `.env` to `.gitignore`
- Fork Cornerstone (the default theme) for custom Stencil themes
- Use Catalyst for new headless projects
- Keep Stencil CLI updated: `npm update -g @bigcommerce/stencil-cli`

Fetch the BigCommerce developer center and Stencil CLI docs for exact setup steps, supported Node.js versions, and current CLI options before setting up.
