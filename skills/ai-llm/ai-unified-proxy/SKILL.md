---
name: ai-unified-proxy
description: Unified AI Proxy - API multi-proveedor gratuita con rotación automática, streaming, y zero vendor lock-in
trigger: ai-proxy OR multi-provider OR free-tier OR ai-routing OR streaming OR unified-ai OR round-robin OR bun-api
scope: global
weight: 4.5
---

# AI Unified Proxy Architecture

## 🎯 Objetivo

Crear una API unificada de IA que:

- ✅ No dependa de NADIE (zero vendor lock-in)
- ✅ Use capas gratuitas de múltiples proveedores
- ✅ Rote servicios automáticamente (round-robin)
- ✅ Soporte streaming de tokens (SSE)
- ✅ Sea extensible (local + cloud)
- ✅ Se despliegue fácil en VPS (Coolify)

---

## 🧱 Stack Tecnológico

### Runtime: Bun (B)

**Por qué Bun:**

- ⚡ Ultra rápido (alternativa a Node.js)
- 📦 `bun install` - gestor de paquetes integrado
- 🚀 `bun run` - ejecutor nativo
- 📘 TypeScript nativo sin configuración
- 🎯 Ideal para APIs livianas

**Instalación:**

```bash
curl -fsSL https://bun.sh/install | bash
```

### Servidor: Bun.serve()

**Características:**

- HTTP server nativo (sin Express/Fastify)
- Puerto dinámico: `process.env.PORT || 3000`
- Manejo manual de rutas (control total)
- Performance superior

---

## 🧠 Arquitectura Lógica

```
Client
  |
POST /chat
  |
API Gateway (Bun)
  |
Round-Robin Selector
  |
AI Service Adapter (contrato común)
  |
┌─────────┬──────────┬─────────┬────────────┬─────────┐
│  Grok   │ Cerebras │ Gemini  │ OpenRouter │  Local  │
└─────────┴──────────┴─────────┴────────────┴─────────┘
  |
Streaming Response (SSE)
```

**Flujo de datos:**

1. Cliente envía mensajes a `/chat`
2. Gateway valida y parsea JSON
3. Selector elige próximo servicio (round-robin)
4. Servicio procesa con su SDK específico
5. Tokens se streamean vía Server-Sent Events
6. Cliente recibe respuesta progresiva

---

## 📜 Contrato Común (Clave del Sistema)

### Tipo: ChatMessage

```typescript
type ChatMessage = {
  role: "system" | "user" | "assistant";
  content: string;
};
```

### Interfaz: AIService

```typescript
interface AIService {
  name: string;
  chat(messages: ChatMessage[]): AsyncIterable<string>;
}
```

### 👉 Regla de Oro

> **Todo proveedor que cumpla este contrato entra al sistema sin tocar el core.**

**Beneficios:**

- ✅ Adapter Pattern implementado
- ✅ Plug & Play de nuevos servicios
- ✅ Cero acoplamiento con proveedores
- ✅ Testing aislado por servicio

---

## 🔁 Balanceo: Round Robin

### Estado Global

```typescript
const services: AIService[] = [];
let currentServiceIndex = 0;
```

### Selector

```typescript
function getNextService(): AIService {
  const service = services[currentServiceIndex];
  currentServiceIndex = (currentServiceIndex + 1) % services.length;
  return service;
}
```

### Ventajas

- ✅ Reparte carga equitativamente
- ✅ Extiende cuotas gratuitas
- ✅ Evita bloqueos por rate limit
- ✅ Sin estado complejo (stateless)

### Evolución Futura

```typescript
// Weighted Round Robin (según calidad/velocidad)
const services = [
  { service: grok, weight: 3 }, // 3x más frecuente
  { service: cerebras, weight: 2 }, // 2x
  { service: gemini, weight: 1 }, // 1x
];

// Health-aware routing
services.filter((s) => s.isHealthy());
```

---

## 🌊 Streaming (Clave Diferencial)

### Técnica: Async Generator + yield

```typescript
async function* streamResponse(service: AIService, messages: ChatMessage[]) {
  for await (const token of service.chat(messages)) {
    yield token;
  }
}
```

### Respuesta: Server-Sent Events (SSE)

**Headers requeridos:**

```typescript
{
  'Content-Type': 'text/event-stream',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive'
}
```

**Formato de datos:**

```
data: {"token":"Hola"}\n\n
data: {"token":" mundo"}\n\n
data: {"done":true}\n\n
```

### Beneficios

- ⚡ Respuesta progresiva (tipo ChatGPT)
- 📉 Menor latencia percibida
- 🔗 Compatible con frontend en tiempo real
- 🎯 Backpressure natural

---

## 🧩 Servicios IA (Plugins)

### 1️⃣ Grok (xAI)

**Free Tier:**

- ~60 req/min
- Modelos: Moonshot, Kimi K2

**Implementación:**

```typescript
// services/grok.ts
import { OpenAI } from "openai";

const client = new OpenAI({
  apiKey: process.env.GROK_API_KEY,
  baseURL: "https://api.x.ai/v1",
});

export const grokService: AIService = {
  name: "Grok",
  async *chat(messages) {
    const stream = await client.chat.completions.create({
      model: "grok-beta",
      messages,
      stream: true,
    });

    for await (const chunk of stream) {
      const token = chunk.choices[0]?.delta?.content;
      if (token) yield token;
    }
  },
};
```

---

### 2️⃣ Cerebras

**Free Tier:**

- 30 req/min
- 1M tokens/día
- Modelos: GPT-OSS, Zhipu GLM-4.6

**Características:**

- Muy rápido en inferencia
- Excelente para tareas simples

**Implementación:**

```typescript
// services/cerebras.ts
import { Cerebras } from "@cerebras/cerebras_cloud_sdk";

const client = new Cerebras({
  apiKey: process.env.CEREBRAS_API_KEY,
});

export const cerebrasService: AIService = {
  name: "Cerebras",
  async *chat(messages) {
    const stream = await client.chat.completions.create({
      model: "llama3.1-8b",
      messages,
      stream: true,
    });

    for await (const chunk of stream) {
      const token = chunk.choices[0]?.delta?.content;
      if (token) yield token;
    }
  },
};
```

---

### 🔌 Otros Servicios Compatibles

| Servicio            | Free Tier         | Velocidad  | Casos de uso           |
| ------------------- | ----------------- | ---------- | ---------------------- |
| **Gemini** (Google) | 15 RPM            | Media      | Razonamiento general   |
| **OpenRouter**      | Modelos gratis    | Variable   | Agregador multi-modelo |
| **Ollama**          | Ilimitado (local) | Depende HW | Offline, privacidad    |
| **LM Studio**       | Ilimitado (local) | Depende HW | UI + local             |

**Ejemplo Gemini:**

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

export const geminiService: AIService = {
  name: "Gemini",
  async *chat(messages) {
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });
    const chat = model.startChat({ history: messages.slice(0, -1) });
    const result = await chat.sendMessageStream(
      messages[messages.length - 1].content,
    );

    for await (const chunk of result.stream) {
      yield chunk.text();
    }
  },
};
```

---

## 📁 Estructura de Proyecto

```
ai-unified-proxy/
├── services/
│   ├── grok.ts          # Integración Grok/xAI
│   ├── cerebras.ts      # Integración Cerebras
│   ├── gemini.ts        # Integración Google Gemini
│   └── ollama.ts        # Integración local Ollama
├── types/
│   ├── chat-message.ts  # Tipo ChatMessage
│   └── ai-service.ts    # Interfaz AIService
├── index.ts             # API Gateway principal
├── .env                 # Variables de entorno (NUNCA commitear)
├── .env.example         # Template de .env
├── package.json         # Dependencias
├── nixpacks.toml        # Config de build Coolify
├── tsconfig.json        # Config TypeScript
└── README.md            # Documentación
```

---

## ⚙️ Implementación: index.ts (API Gateway)

### Código completo:

```typescript
import { grokService } from "./services/grok";
import { cerebrasService } from "./services/cerebras";
import type { ChatMessage, AIService } from "./types/ai-service";

// Estado global
const services: AIService[] = [grokService, cerebrasService];
let currentServiceIndex = 0;

// Selector Round Robin
function getNextService(): AIService {
  const service = services[currentServiceIndex];
  currentServiceIndex = (currentServiceIndex + 1) % services.length;
  return service;
}

// Servidor HTTP
Bun.serve({
  port: process.env.PORT || 3000,

  async fetch(req) {
    const url = new URL(req.url);

    // Ruta: POST /chat
    if (req.method === "POST" && url.pathname === "/chat") {
      try {
        // Parse body
        const body = await req.json();
        const messages = body.messages as ChatMessage[];

        // Validación básica
        if (!Array.isArray(messages) || messages.length === 0) {
          return new Response("Invalid messages", { status: 400 });
        }

        // Seleccionar servicio
        const service = getNextService();
        console.log(`[${new Date().toISOString()}] Using: ${service.name}`);

        // Stream de respuesta
        const stream = new ReadableStream({
          async start(controller) {
            try {
              for await (const token of service.chat(messages)) {
                const data = `data: ${JSON.stringify({ token })}\n\n`;
                controller.enqueue(new TextEncoder().encode(data));
              }

              // Mensaje de finalización
              controller.enqueue(
                new TextEncoder().encode(
                  `data: ${JSON.stringify({ done: true })}\n\n`,
                ),
              );
            } catch (error) {
              console.error(`Error with ${service.name}:`, error);
              controller.enqueue(
                new TextEncoder().encode(
                  `data: ${JSON.stringify({ error: error.message })}\n\n`,
                ),
              );
            } finally {
              controller.close();
            }
          },
        });

        // Respuesta SSE
        return new Response(stream, {
          headers: {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            Connection: "keep-alive",
          },
        });
      } catch (error) {
        return new Response(`Error: ${error.message}`, { status: 500 });
      }
    }

    // Fallback
    return new Response("Not Found", { status: 404 });
  },
});

console.log(`🚀 AI Proxy running on port ${process.env.PORT || 3000}`);
```

---

## 🔐 Variables de Entorno

### `.env` (NUNCA commitear)

```bash
# API Keys
GROK_API_KEY=xai-xxxxxxxxxxxxx
CEREBRAS_API_KEY=csk-xxxxxxxxxxxxx
GEMINI_API_KEY=AIzaxxxxxxxxxxxxx

# Server
PORT=3000
NODE_ENV=production
```

### `.env.example` (Template)

```bash
# API Keys (obtener en respectivos dashboards)
GROK_API_KEY=your_grok_key_here
CEREBRAS_API_KEY=your_cerebras_key_here
GEMINI_API_KEY=your_gemini_key_here

# Server config
PORT=3000
NODE_ENV=production
```

### ⚠️ Buenas Prácticas

- Solo runtime, no buildtime
- Usar `.gitignore` para `.env`
- Nunca hardcodear keys
- Validar keys al inicio

---

## 🚀 Deploy en Coolify

### Paso 1: Preparar VPS

**Requisitos mínimos:**

- 2 vCPU
- 8 GB RAM (4 GB suficiente)
- 20 GB disco
- Ubuntu 22.04 LTS

**Proveedores recomendados:**

- Hostinger VPS (~$5/mes)
- Hetzner Cloud (~€4/mes)
- DigitalOcean Droplets (~$6/mes)

### Paso 2: Instalar Coolify

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

**Acceder:** `http://your-vps-ip:8000`

### Paso 3: Configurar proyecto en Coolify

1. **New Resource** → **Git Repository**
2. Conectar tu repo (GitHub/GitLab)
3. Configurar:
   - **Build Pack**: Nixpacks
   - **Port**: 3000
   - **Environment Variables**: Agregar API keys

### Paso 4: nixpacks.toml

```toml
[setup]
packages = ["bun"]

[install]
cmds = ["bun install"]

[start]
cmd = "bun run index.ts"

[variables]
PORT = "3000"
```

### Paso 5: Deploy

- Coolify detecta cambios en Git
- Build automático con Nixpacks
- Deploy con zero-downtime
- Logs en vivo en UI

---

## 🧪 Testing

### Testing Local

```bash
# Instalar dependencias
bun install

# Crear .env con tus keys
cp .env.example .env
# (editar .env con tus API keys)

# Correr servidor
bun run index.ts
```

### Testing con curl

```bash
curl -N -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages":[
      {"role":"user","content":"Explica Fibonacci en JavaScript"}
    ]
  }'
```

**Resultado esperado:**

```
data: {"token":"Aquí"}

data: {"token":" tienes"}

data: {"token":" una"}

data: {"token":" implementación"}
...
data: {"done":true}
```

### Testing con JavaScript

```javascript
const eventSource = new EventSource("/chat", {
  method: "POST",
  body: JSON.stringify({
    messages: [{ role: "user", content: "Hola mundo" }],
  }),
});

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.done) {
    eventSource.close();
  } else {
    console.log(data.token);
  }
};
```

---

## 🧠 Metodologías Implícitas

| Pattern                     | Descripción                        | Beneficio      |
| --------------------------- | ---------------------------------- | -------------- |
| **Adapter Pattern**         | Cada proveedor es un plugin        | Extensibilidad |
| **Gateway Pattern**         | API única para múltiples servicios | Simplicidad    |
| **Backpressure Natural**    | Streaming controla flujo           | Performance    |
| **Fail Soft**               | Rotación automática                | Resiliencia    |
| **Cost-Aware Architecture** | Gratis primero, pago último        | Economía       |

---

## 🔮 Extensiones Naturales

### 1. Weighted Round Robin

```typescript
const services = [
  { service: grok, weight: 3, quality: 0.9 },
  { service: cerebras, weight: 2, quality: 0.85 },
  { service: gemini, weight: 1, quality: 0.95 },
];

// Selector basado en peso y calidad
function getWeightedService() {
  const totalWeight = services.reduce((sum, s) => sum + s.weight, 0);
  let random = Math.random() * totalWeight;

  for (const item of services) {
    random -= item.weight;
    if (random <= 0) return item.service;
  }
}
```

### 2. Health Checks

```typescript
interface AIService {
  name: string;
  chat(messages: ChatMessage[]): AsyncIterable<string>;
  healthCheck(): Promise<boolean>; // Nuevo
}

async function getHealthyService() {
  const healthy = await Promise.all(
    services.map(async (s) => ({
      service: s,
      isHealthy: await s.healthCheck(),
    })),
  );
  return healthy.find((h) => h.isHealthy)?.service;
}
```

### 3. Fallback Local Automático

```typescript
const services = [
  grokService,
  cerebrasService,
  geminiService,
  ollamaService, // Último recurso (local, siempre available)
];
```

### 4. Cache Semántica

```typescript
import { similarity } from "ml-distance";

const cache = new Map<string, string>();

function getCachedResponse(prompt: string) {
  for (const [cachedPrompt, response] of cache) {
    if (similarity(prompt, cachedPrompt) > 0.95) {
      return response;
    }
  }
  return null;
}
```

### 5. Rate Limit Aware Routing

```typescript
interface AIService {
  name: string;
  rateLimitRemaining: number;
  rateLimitReset: Date;
  chat(messages: ChatMessage[]): AsyncIterable<string>;
}

function getRateLimitSafeService() {
  return services.find((s) => s.rateLimitRemaining > 0) || services[0];
}
```

### 6. Observabilidad

```typescript
import { logger } from "./logger";

for await (const token of service.chat(messages)) {
  logger.info({
    service: service.name,
    timestamp: Date.now(),
    tokenLength: token.length,
  });
  yield token;
}
```

### 7. Policy Engine

```typescript
function selectServiceByTask(task: string) {
  if (task.includes("código")) return cerebrasService; // Rápido
  if (task.includes("razonamiento")) return geminiService; // Inteligente
  return grokService; // Default
}
```

---

## 🚨 Troubleshooting

### Problema: "No streaming"

**Causa:** Headers SSE incorrectos  
**Solución:**

```typescript
{
  'Content-Type': 'text/event-stream',  // No 'application/json'
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive'
}
```

### Problema: "Rate limit exceeded"

**Causa:** Todas las APIs agotadas  
**Solución:** Agregar más proveedores o fallback local

### Problema: "Bun not found en Coolify"

**Causa:** nixpacks.toml incorrecto  
**Solución:**

```toml
[setup]
packages = ["bun"]  # Asegurar que esté presente
```

### Problema: "CORS errors"

**Solución:**

```typescript
headers: {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Content-Type': 'text/event-stream',
  // ...
}
```

---

## 📚 Related Skills

- `cloud-ready` - Deploy y gestión en VPS
- `ai-security` - Protección contra prompt injection
- `conventional-commits` - Versionado semántico
- `machine-health` - Monitoreo de recursos

---

## 🧠 Resumen Brutal (1 Línea)

> **Una API de IA modular, gratuita, extensible y sin vendor lock-in, basada en contratos, streaming y rotación inteligente de proveedores.**

---

**Ready to deploy. 🚀**
