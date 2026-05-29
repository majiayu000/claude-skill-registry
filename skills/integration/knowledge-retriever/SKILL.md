---
name: knowledge-retriever
description: Standardized system for indexing, querying, and retrieving external knowledge sources (URLs, Databases, Documentation).
trigger: knowledge OR docs OR retriever OR references OR external-source OR documentation OR how-to
scope: global
weight: 5.0
---

# Knowledge Retriever Skill 🧠

## 🎯 Objetivo

Proveer un mecanismo estandarizado y "lógico-topológico" para acceder a fuentes de conocimiento externas (URLs, Documentación Oficial) sin alucinar.

## 🏗️ Arquitectura

El sistema se basa en un **Índice Maestro (`knowledge/LIBRARY.md`)** que actúa como el "Córtex Externo" de Gentleman.

### 1. El Índice (`knowledge/LIBRARY.md`)

Es un archivo Markdown estructurado que la IA puede leer (topológicamente) para encontrar la fuente de verdad adecuada.

**Formato Estándar:**

```markdown
| Topic        | Description                             | Source URL  | Tags              |
| ------------ | --------------------------------------- | ----------- | ----------------- |
| Copilot Test | Testing strategies for microsft copilot | https://... | #testing #copilot |
```

### 2. El Protocolo de Consulta

Cuando el usuario pregunta "¿Cómo hago X?", el agente:

1. Detecta la intención de búsqueda (trigger: `knowledge`).
2. Lee `knowledge/LIBRARY.md`.
3. Selecciona la fuente más relevante.
4. (Opcional) Usa un browser tool para leer el contenido real si es necesario.
5. Responde basado en la fuente.

## 🚀 Uso

Simplemente menciona "knowledge base", "referencia", o "búscalo en la librería".

## 🛠️ Comandos (Futuro)

- `/add-knowledge <url> <desc>`: Agregar nueva fuente.
- `/query-knowledge <topic>`: Buscar en el índice.
