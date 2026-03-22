---
name: acp-setup
description: Scaffold an ACP merchant server project — install dependencies, import OpenAPI specs and JSON schemas, configure environment, and create initial endpoint stubs. Use when starting a new ACP implementation from scratch.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
disable-model-invocation: true
---

# ACP Project Setup

## Before writing code

1. **Fetch the latest spec version**: Web-search `site:github.com agentic-commerce-protocol CHANGELOG` for the current spec version
2. **Fetch the OpenAPI specs**: Fetch from `https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/tree/main/spec` — download the latest versioned checkout and delegate-payment OpenAPI YAML files
3. **Fetch the get-started guide**: Fetch `https://developers.openai.com/commerce/guides/get-started/` for onboarding steps
4. **Check for SDK packages**: Search PyPI for `agentic-commerce-protocol` and npm for ACP-related packages. Note: there is no official standalone SDK — most implementations use the OpenAPI spec directly or reference implementations like Medusa.js

## What This Skill Does

Scaffolds a new ACP merchant server project:

1. **Detect language/framework** — Python (FastAPI/Flask/Django), TypeScript (Express/Fastify/Medusa), Go, etc.
2. **Install dependencies** — HTTP framework, JSON schema validation, HMAC library, UUID generation
3. **Import OpenAPI spec** — Download the latest versioned spec from the GitHub repo
4. **Create configuration** — Environment variables for API keys, webhook secrets, API version, PSP credentials
5. **Stub endpoints** — Create route stubs for the 5 checkout operations + webhook receiver
6. **Set up middleware** — Bearer token auth, idempotency key extraction, API version header validation, request logging

## Configuration Essentials

These must be externalized (env vars or config file):
- `ACP_API_KEY` — Bearer token for authentication
- `ACP_API_VERSION` — Spec version (YYYY-MM-DD format)
- `ACP_WEBHOOK_SECRET` — HMAC signing key for webhooks
- `STRIPE_API_KEY` — If using Stripe as PSP for delegated payment
- `ACP_MERCHANT_ID` — Merchant identifier for SPT scoping

## Project Structure Pattern

```
merchant-server/
├── config/                  # Environment and settings
├── routes/
│   ├── checkout.py/ts       # 5 checkout endpoints
│   ├── webhooks.py/ts       # Webhook receiver
│   └── health.py/ts         # Health check
├── middleware/
│   ├── auth.py/ts           # Bearer token validation
│   ├── idempotency.py/ts    # Idempotency key handling
│   └── versioning.py/ts     # API-Version header validation
├── models/                  # Data models from JSON schema
├── services/
│   ├── checkout.py/ts       # Business logic
│   ├── payment.py/ts        # PSP integration
│   └── inventory.py/ts      # Stock management
├── schemas/                 # OpenAPI + JSON schemas
└── tests/
```

Fetch the OpenAPI spec for exact endpoint paths, request/response shapes, and status codes before generating stubs.
