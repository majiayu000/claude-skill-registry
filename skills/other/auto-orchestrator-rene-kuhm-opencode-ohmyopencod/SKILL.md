---
name: auto-orchestrator
description: "Sistema de auto-routing que detecta el tipo de tarea y activa el agente especializado correcto automáticamente. Se activa con cualquier tarea de desarrollo."
allowed-tools:
  - Task
  - Read
  - Glob
  - Grep
---

# Auto-Orchestrator - Sistema de Routing Inteligente

## Activación Automática

Este skill se activa cuando el usuario hace cualquier pedido de desarrollo. Analiza la intención y delega al agente correcto.

---

## Mapa de Decisión Rápida

```
PALABRA CLAVE → AGENTE → subagent_type
─────────────────────────────────────────────────────
error|bug|falla|roto|crash     → debugger
crear|component|page|feature   → builder
arquitectura|diseño|sistema    → architect
seguridad|audit|OWASP|vuln     → security-auditor
test|coverage|vitest           → test-engineer
docs|README|documentar         → docs-writer
Next.js|React|GSAP|animation   → general-architect
explorar|buscar|encontrar      → Explore
planificar|ADR|diseño sistema  → Plan
commit|PR|git|release          → general-purpose (skill /commit)
deploy|docker|k8s|CI           → devops
```

---

## Implementación

Cuando recibas una tarea:

### 1. Detectar Intención
```typescript
const detectIntent = (input: string) => {
  const patterns = {
    debug: /error|bug|falla|roto|crash|no funciona|exception/i,
    security: /seguridad|vulnerab|OWASP|XSS|SQL|injection|audit/i,
    test: /test|coverage|vitest|playwright|jest|spec/i,
    docs: /document|README|docs|JSDoc|guía/i,
    architecture: /arquitectura|diseño.*sistema|estructura|planific/i,
    animation: /Next\.js|React|GSAP|Framer|Lenis|animaci/i,
    explore: /explor|busc|encontr|dónde.*está|qué.*archivo/i,
    build: /cre[aá]|implement|component|feature|página|hacer/i,
    devops: /deploy|docker|kubernetes|CI|CD|pipeline/i,
    git: /commit|PR|pull.*request|merge|release|push/i,
  };

  for (const [intent, pattern] of Object.entries(patterns)) {
    if (pattern.test(input)) return intent;
  }
  return 'general';
};
```

### 2. Mapear a Agente
```typescript
const agentMap = {
  debug: { agent: 'debugger', type: 'debugger' },
  security: { agent: 'security-auditor', type: 'security-auditor' },
  test: { agent: 'test-engineer', type: 'test-engineer' },
  docs: { agent: 'docs-writer', type: 'docs-writer' },
  architecture: { agent: 'architect', type: 'architect' },
  animation: { agent: 'general-architect', type: 'general-architect' },
  explore: { agent: 'Explore', type: 'Explore' },
  build: { agent: 'builder', type: 'builder' },
  devops: { agent: 'devops', type: 'devops' },
  git: { agent: 'general-purpose', type: 'general-purpose' },
  general: { agent: 'general-purpose', type: 'general-purpose' },
};
```

### 3. Delegar
```
Task(
  subagent_type: agentMap[intent].type,
  prompt: "Contexto completo de la tarea del usuario",
  description: "Descripción corta de la tarea"
)
```

---

## Flujo Visual

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO ENVÍA TAREA                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  AUTO-ORCHESTRATOR                          │
│                                                             │
│  1. Analizar palabras clave                                │
│  2. Detectar intención                                      │
│  3. Seleccionar agente                                      │
│  4. Delegar con contexto completo                          │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
      ┌──────────┐    ┌──────────┐    ┌──────────┐
      │ debugger │    │ builder  │    │ security │
      └──────────┘    └──────────┘    └──────────┘
            │               │               │
            └───────────────┼───────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  RESPUESTA AL USUARIO                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Ejemplos de Uso

### Error → Debugger
```
Input: "La app crashea cuando hago login"
Output: Task(debugger) → "Investigar crash en login"
```

### Feature → Builder
```
Input: "Necesito un formulario de contacto"
Output: Task(builder) → "Implementar formulario de contacto"
```

### Arquitectura → Architect
```
Input: "Cómo debería estructurar el módulo de pagos?"
Output: Task(architect) → "Diseñar arquitectura de módulo de pagos"
```

### Animación → General Architect
```
Input: "Quiero una landing con animaciones tipo Awwwards"
Output: Task(general-architect) → "Diseñar landing con GSAP/Framer Motion"
```

---

## Prioridad de Detección

Si hay múltiples matches, usar esta prioridad:

1. **Security** (siempre primero si se menciona seguridad)
2. **Debug** (errores tienen prioridad)
3. **Test** (testing es específico)
4. **Architecture** (antes de implementar)
5. **Animation/Next.js** (stack específico)
6. **Build** (implementación general)
7. **General** (fallback)
