---
name: openai-chatkit
description: Framework de OpenAI para construir interfaces de chat AI personalizables con React. Incluye componentes UI pre-construidos, streaming de respuestas, manejo de archivos y gestión de threads.
trigger: chatkit OR openai chat OR chat ui OR chat components OR agent builder
scope: frontend
---

# OpenAI ChatKit

## Contexto

OpenAI ChatKit es un framework frontend para construir e integrar experiencias de chat AI personalizables en aplicaciones web. Proporciona componentes React pre-construidos para interfaces de chat con características como streaming de respuestas, adjuntos de archivos y gestión de conversaciones.

## Paquetes

| Paquete                   | Descripción                                                   |
| ------------------------- | ------------------------------------------------------------- |
| `@openai/chatkit-react`   | Hooks y componentes React para renderizar la interfaz de chat |
| `openai-chatkit` (Python) | SDK para backend avanzado con control total                   |

## Instalación

```bash
# React (Frontend)
npm install @openai/chatkit-react

# Python (Backend avanzado)
pip install openai-chatkit
```

## Reglas Críticas

- **Siempre** requiere un backend para autenticación y conexión con OpenAI APIs
- **Nunca** exponer API keys en el frontend - usar `client_secret` generado por el servidor
- **Siempre** manejar el streaming de respuestas correctamente
- **Preferir** la integración recomendada (Agent Builder) para setup rápido

## Arquitectura

### Integración Recomendada (Rápida)

1. Frontend: ChatKit React components
2. Backend: OpenAI Agent Builder hostea y escala
3. Tu servidor: Solo genera `client_token` para iniciar sesiones

### Integración Avanzada (Control Total)

1. Frontend: ChatKit React components
2. Backend: Tu servidor con ChatKit Python SDK
3. Control completo sobre herramientas, lógica y almacenamiento

## Procedimiento de Implementación

### 1. Setup del Agent Workflow

Crear un agent workflow en OpenAI Agent Builder que define el comportamiento del AI.

### 2. Backend - Generación de Token

```python
from openai import OpenAI

client = OpenAI()

def create_chat_session(user_id: str):
    """Genera un client_secret para iniciar una sesión de chat."""
    response = client.beta.realtime.sessions.create(
        model="gpt-4o-realtime-preview",
        voice="verse",
        modalities=["text"]
    )
    return response.client_secret
```

### 3. Frontend - Renderizar ChatKit

```tsx
import { ChatKit, useChatKit } from "@openai/chatkit-react";

interface ChatContainerProps {
  clientSecret: string;
}

function ChatContainer({ clientSecret }: ChatContainerProps) {
  const { config, events } = useChatKit({
    clientSecret,
    onMessage: (message) => {
      console.log("New message:", message);
    },
    onError: (error) => {
      console.error("Chat error:", error);
    },
  });

  return <ChatKit config={config} events={events} className="h-full w-full" />;
}

export default ChatContainer;
```

### 4. Streaming de Respuestas

```tsx
import { ChatKit } from "@openai/chatkit-react";

function StreamingChat({ clientSecret }: { clientSecret: string }) {
  return (
    <ChatKit
      clientSecret={clientSecret}
      streamingEnabled={true}
      onStreamStart={() => console.log("Streaming started")}
      onStreamEnd={() => console.log("Streaming ended")}
    />
  );
}
```

## Características Principales

| Feature                 | Descripción                                             |
| ----------------------- | ------------------------------------------------------- |
| **UI Customization**    | Personalización profunda de la interfaz                 |
| **Response Streaming**  | Streaming en tiempo real de respuestas                  |
| **Tool Integration**    | Visualización de acciones agénticas                     |
| **Rich Widgets**        | Widgets interactivos para diferentes tipos de contenido |
| **Attachment Handling** | Manejo de archivos adjuntos                             |
| **Thread Management**   | Gestión de conversaciones y threads                     |

## Ejemplo Completo

```tsx
// app/chat/page.tsx (Next.js App Router)
"use client";

import { useEffect, useState } from "react";
import { ChatKit } from "@openai/chatkit-react";

export default function ChatPage() {
  const [clientSecret, setClientSecret] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function initChat() {
      try {
        // Obtener client_secret desde tu backend
        const response = await fetch("/api/chat/init", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });
        const { client_secret } = await response.json();
        setClientSecret(client_secret);
      } catch (error) {
        console.error("Failed to init chat:", error);
      } finally {
        setLoading(false);
      }
    }
    initChat();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        Loading...
      </div>
    );
  }

  if (!clientSecret) {
    return <div className="text-red-500">Failed to initialize chat</div>;
  }

  return (
    <div className="h-screen w-full">
      <ChatKit
        clientSecret={clientSecret}
        theme="dark"
        placeholder="Ask me anything..."
      />
    </div>
  );
}
```

## Recursos

- [GitHub - chatkit-js](https://github.com/openai/chatkit-js)
- [GitHub - Advanced Samples](https://github.com/openai/openai-chatkit-advanced-samples)
- [NPM - @openai/chatkit-react](https://www.npmjs.com/package/@openai/chatkit-react)
- [OpenAI Platform Docs](https://platform.openai.com/docs/guides/chatkit)
