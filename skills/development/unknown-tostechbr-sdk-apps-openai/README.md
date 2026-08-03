<div align="center">

# SDK Apps Collection

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)](https://nodejs.org/)
[![Protocol](https://img.shields.io/badge/Protocol-MCP-orange)](https://modelcontextprotocol.io/)

**A curated gallery of interactive applications developed with the OpenAI Apps SDK and Model Context Protocol.**

[Architecture](#architecture) • [Projects](#projects) • [Getting Started](#getting-started) • [Repository](https://github.com/tostechbr/sdk-apps-openai)

</div>

---

## Overview

This repository demonstrates advanced integration patterns between Large Language Models (LLMs) and interactive user interfaces. By leveraging the **Model Context Protocol (MCP)**, these applications allow ChatGPT to render dynamic widgets, visualize data in real-time, and perform complex actions beyond simple text generation.

The collection serves as a reference implementation for developers building the next generation of AI-native applications.

## Projects

| Project | Description | Key Technologies | Status |
| :--- | :--- | :--- | :--- |
| **[Real Estate Map](./apps/real-estate)** | Interactive property search engine with dynamic map visualization and filtering capabilities. | Google Maps API, SSE, Zod, MCP | 🟢 Active |
| **[Medical Appointment](./apps/medical-appointment)** | Doctor scheduling system with availability checking, booking, and ambiguity handling. | Supabase, STDIO, Zod, MCP | 🟢 Active |


## Architecture

All applications in this monorepo share a unified architectural pattern designed for scalability and maintainability:

- **Protocol:** Model Context Protocol (MCP) for standardized LLM communication.
- **Transport:** Server-Sent Events (SSE) over HTTP for persistent, bi-directional data flow.
- **Backend:** Node.js/TypeScript services implementing tool definitions and business logic.
- **Frontend:** Lightweight, zero-dependency HTML/JS widgets injected directly into the chat interface.

## Getting Started

Follow these steps to set up the environment and run the demo applications locally.

### Prerequisites

| Requirement | Version | Purpose |
| :--- | :--- | :--- |
| **Node.js** | v18.0.0+ | Javascript Runtime |
| **npm** | v9.0.0+ | Package Manager |
| **Google Maps Key** | Active | Required for Real Estate App |

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tostechbr/sdk-apps-openai.git
   cd sdk-apps-openai
   ```

2. Navigate to the target application directory (e.g., Real Estate):
   ```bash
   cd apps/real-estate
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Configure environment variables (create `.env` file):
   ```bash
   cp .env.example .env
   # Edit .env with your specific API keys
   ```

## Development Workflow

We recommend using the **MCP Inspector** for local development and testing of tool definitions before integration with ChatGPT.

```bash
# Start the development server
npm run dev

# In a separate terminal, launch the Inspector
npx @modelcontextprotocol/inspector sse http://localhost:8787/mcp
```

## Contributing

We welcome contributions to expand this collection of use cases. Please ensure all new modules follow the established directory structure and include comprehensive documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
