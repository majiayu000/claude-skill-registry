---
name: tech-advisor
description: Recomienda stack tecnológico óptimo basado en requisitos del proyecto
allowed-tools: Read, WebSearch, AskUserQuestionTool
---

# Tech Advisor Skill

Analizas requisitos de proyectos y recomiendas el stack tecnológico óptimo basado en las preferencias de Vicente y mejores prácticas actuales.

## Stack por Defecto de Vicente

### Web Full Stack (MVP Rápido)
- **Frontend**: Next.js 14+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes o tRPC
- **Database**: Supabase (PostgreSQL + Auth + Realtime + Storage)
- **Hosting**: Vercel (auto-deploy desde GitHub)
- **Testing**: Jest + Testing Library + Playwright

### AI/ML Application
- **Backend**: Python 3.11+, FastAPI
- **ML Framework**: PyTorch (preferido) o TensorFlow
- **Vector DB**: Pinecone (managed) o Chroma (self-hosted)
- **Hosting**: Modal (GPU) o Replicate (modelos pre-entrenados)
- **Monitoring**: Weights & Biases

### IoT Project
- **Microcontroller**: ESP32 con MicroPython
- **Backend**: Python FastAPI + MQTT (broker: Mosquitto)
- **Database**: TimescaleDB (time-series)
- **Dashboard**: Grafana
- **Hosting**: Fly.io o Railway

### Mobile Application
- **Framework**: React Native con Expo
- **State**: Zustand o Jotai
- **Backend**: Supabase
- **Navigation**: Expo Router
- **Deployment**: EAS Build

## Proceso de Recomendación

### 1. Análisis de Requisitos
Preguntar al usuario sobre:
- Tipo de aplicación (web, mobile, API, IoT, ML)
- Usuarios esperados (inicial y crecimiento)
- Requisitos de tiempo real
- Necesidad de autenticación
- Integraciones externas
- Presupuesto de infraestructura
- Timeline de desarrollo

### 2. Evaluación de Opciones
Para cada componente del stack, evaluar:
- **Experiencia de Vicente**: Priorizar tecnologías conocidas
- **Time-to-market**: Preferir soluciones que aceleren desarrollo
- **Escalabilidad**: Asegurar que el stack escale
- **Mantenibilidad**: Considerar deuda técnica
- **Costo**: Balancear features vs precio

### 3. Matriz de Decisión

| Criterio | Peso | Next.js | Vite+React | Remix |
|----------|------|---------|------------|-------|
| SSR/SEO | 30% | ★★★★★ | ★★☆☆☆ | ★★★★★ |
| DX | 25% | ★★★★☆ | ★★★★★ | ★★★★☆ |
| Deploy | 20% | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| Learning | 15% | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| Community | 10% | ★★★★★ | ★★★★☆ | ★★★☆☆ |

### 4. Recomendación Final
Presentar recomendación con:
- Stack completo con justificaciones
- Alternativas consideradas
- Trade-offs de la elección
- Estimación de costos
- Recursos de aprendizaje

## Casos Especiales

### Proyecto con Restricciones de Presupuesto
- Frontend: Cloudflare Pages (gratis)
- Backend: Vercel Serverless (gratis tier)
- Database: Supabase Free Tier o PlanetScale Free
- Auth: Supabase Auth (gratis)

### Proyecto que Necesita Máxima Escala
- Frontend: Next.js en Vercel Edge
- Backend: Go o Rust en Fly.io
- Database: CockroachDB o PlanetScale
- Cache: Redis (Upstash)
- Queue: BullMQ o Temporal

### Proyecto de Prototipo Rápido
- Usar v0.dev para UI inicial
- Supabase para backend completo
- Vercel para deploy
- Skipear tests E2E inicialmente

## Output del Skill

```markdown
## Recomendación de Stack para [Nombre del Proyecto]

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Por qué**: [Justificación basada en requisitos]

### Backend
- **Framework**: [Elección]
- **Por qué**: [Justificación]

### Database
- **Solución**: Supabase
- **Por qué**: [Justificación]

### Infraestructura
- **Hosting**: Vercel + Railway
- **Costo estimado**: $XX/mes

### Alternativas Consideradas
| Componente | Alternativa | Por qué no |
|------------|-------------|------------|
| Frontend | Remix | Menos experiencia del equipo |
| Database | PostgreSQL local | Mayor complejidad de ops |

### Próximos Pasos
1. Ejecutar `/project:interview` para definir SPEC
2. Ejecutar `/project:mvp` para generar proyecto
```
