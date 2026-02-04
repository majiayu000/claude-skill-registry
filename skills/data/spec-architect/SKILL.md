---
name: "Spec Architect"
description: "Genera y valida archivos de especificación (.spec.md) siguiendo el estándar SDD v2.0."
trigger: "Cuando el usuario diga 'crea una especificación', 'planifica esta feature' o use el comando '/specify'."
scope: "PLANNING"
auto-invoke: false
---

# Protocolo de Arquitectura de Especificaciones (SDD v2.0)

Tu objetivo es eliminar la ambigüedad. No escribes código; escribes el *plano* del código.

## 1. Fase de Generación (/specify)

Cuando el usuario describe una funcionalidad, genera un archivo en `specs/` (créala si no existe) con el nombre `YYYY-MM-DD_nombre-feature.spec.md`.

**Plantilla Maestra Obligatoria:**

```markdown
# [Nombre del Feature]

## 1. Contexto y Objetivos
- **Problema:** [Descripción del dolor]
- **Solución:** [Descripción de la funcionalidad]
- **KPIs:** [Cómo medimos el éxito]

## 2. Esquemas de Datos
- **Entradas:** [JSON Schema o Interface TS]
- **Salidas:** [JSON Schema o Interface TS]
- **Persistencia:** [Cambios en DB: Tablas, Columnas, Tipos]

## 3. Lógica de Negocio (Invariantes)
- SI [Condición A] ENTONCES [Resultado B]
- RESTRICCIÓN: [Regla de seguridad o negocio inviolable]

## 4. Stack y Restricciones
- **Tecnología:** [Librerías específicas, versiones]
- **Soberanía:** [Cómo se garantiza el aislamiento del tenant]

## 5. Criterios de Aceptación (Gherkin)
- **Escenario 1:**
  - DADO que [Precondición]
  - CUANDO [Acción]
  - ENTONCES [Resultado esperado]
```

## 2. Fase de Refinamiento (/refine)

Antes de dar por buena una especificación:

1. **Analiza**: ¿Hay ambigüedades? ¿Faltan casos borde?
2. **Cuestiona**: Pregunta al usuario sobre detalles técnicos no definidos (ej. "¿Qué pasa si la API externa falla?").
3. **Valida**: Asegura que cumple con `AGENTS.md` (Protocolo Soberano).

## 3. Fase de Auditoría (/audit)

Si el usuario pide auditar una implementación contra su spec:

1. Lee el archivo `.spec.md`.
2. Lee el código implementado.
3. Reporta desviaciones ("Spec Drift"):
   - "El código usa `float` pero la spec pedía `decimal`."
   - "Falta la validación de seguridad definida en la sección 3."

## 4. Reglas de Oro

1. **La Spec es Ley**: Si el código contradice la spec, el código está mal (o la spec debe actualizarse explícitamente).
2. **Atomicidad**: Una spec debe ser implementable en un solo sprint o tarea grande. Si es muy grande, divídela.
3. **Trazabilidad**: Cada spec debe referenciar el issue/ticket que la originó.
4. **Versionado**: Si una spec cambia, crea una nueva versión (ej. `v2_nombre-feature.spec.md`) y marca la anterior como `[DEPRECATED]`.

## 5. Comandos Disponibles

### `/specify [idea]`
Genera una nueva especificación a partir de una idea vaga.

**Ejemplo**:
```
Usuario: /specify sistema de notificaciones push
Antigravity: [Genera specs/2026-01-27_push-notifications.spec.md]
```

### `/refine [spec_file]`
Revisa una especificación existente y sugiere mejoras.

**Ejemplo**:
```
Usuario: /refine specs/2026-01-27_push-notifications.spec.md
Antigravity: [Analiza y pregunta sobre casos borde]
```

### `/audit [spec_file] [code_files]`
Compara la implementación contra la especificación.

**Ejemplo**:
```
Usuario: /audit specs/2026-01-27_push-notifications.spec.md orchestrator_service/notifications.py
Antigravity: [Reporta desviaciones]
```

## 6. Integración con el Flujo de Trabajo

1. **Antes de codificar**: Siempre genera una spec con `/specify`.
2. **Durante el desarrollo**: Si encuentras ambigüedades, actualiza la spec (no el código).
3. **Después de implementar**: Ejecuta `/audit` para validar que cumpliste la spec.
4. **En code review**: El revisor debe tener acceso a la spec para validar coherencia.

## 7. Ejemplo Completo

**Usuario dice**: "Necesito un sistema para que los agentes puedan pausar conversaciones temporalmente"

**Antigravity genera**: `specs/2026-01-27_conversation-pause.spec.md`

```markdown
# Sistema de Pausa de Conversaciones

## 1. Contexto y Objetivos
- **Problema:** Los agentes no pueden pausar conversaciones cuando necesitan investigar o consultar con un supervisor.
- **Solución:** Agregar un botón "Pausar" que congela la conversación por un tiempo definido.
- **KPIs:** Reducir tiempo de respuesta en casos complejos en 30%.

## 2. Esquemas de Datos
- **Entradas:**
  ```typescript
  interface PauseRequest {
    conversation_id: string;
    duration_minutes: number; // 15, 30, 60, 120
    reason?: string;
  }
  ```
- **Salidas:**
  ```typescript
  interface PauseResponse {
    paused_until: string; // ISO 8601
    status: "paused" | "active";
  }
  ```
- **Persistencia:**
  - Tabla: `chat_conversations`
  - Nueva columna: `paused_until TIMESTAMPTZ NULL`
  - Nueva columna: `pause_reason TEXT NULL`

## 3. Lógica de Negocio (Invariantes)
- SI `paused_until > NOW()` ENTONCES el agente IA NO debe responder.
- SI `paused_until <= NOW()` ENTONCES reactivar automáticamente.
- RESTRICCIÓN: Solo el agente humano que pausó puede despausar manualmente.

## 4. Stack y Restricciones
- **Tecnología:** PostgreSQL TIMESTAMPTZ, React useState para UI.
- **Soberanía:** La pausa es por conversación, no afecta a otros tenants.

## 5. Criterios de Aceptación (Gherkin)
- **Escenario 1: Pausar conversación**
  - DADO que soy un agente humano en una conversación activa
  - CUANDO hago clic en "Pausar por 30 min"
  - ENTONCES la conversación se marca como pausada hasta dentro de 30 minutos
  - Y el agente IA no responde durante ese período

- **Escenario 2: Reactivación automática**
  - DADO que una conversación está pausada hasta las 14:00
  - CUANDO el reloj marca las 14:01
  - ENTONCES la conversación se reactiva automáticamente
  - Y el agente IA puede volver a responder
```

---

**Nota**: Esta skill trabaja en conjunto con `/plan` (genera el plan de implementación) y `/implement` (ejecuta el código).
