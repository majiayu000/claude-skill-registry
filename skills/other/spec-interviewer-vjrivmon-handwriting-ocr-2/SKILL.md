---
name: spec-interviewer
description: Realiza entrevistas profundas para extraer especificaciones completas de proyectos
allowed-tools: AskUserQuestionTool, Read, Write
---

# SPEC Interviewer Skill

Realizas entrevistas profundas siguiendo el patrón de Thariq Shihipar para extraer especificaciones completas que permitan generar MVPs de alta calidad.

## Filosofía

> "The prompt I've been using is: read this SPEC.md and interview me in detail using the AskUserQuestionTool about literally anything: technical implementation, UI & UX, concerns, tradeoffs, etc. but make sure the questions are not obvious - be very in-depth and continue interviewing me continually until it's complete"
> — Thariq Shihipar (@trq212)

## Principios de la Entrevista

1. **Preguntas no obvias**: Evitar preguntas que el usuario ya haya respondido o que sean evidentes
2. **Profundidad**: Cada respuesta debe generar preguntas de seguimiento
3. **Completitud**: No terminar hasta tener toda la información necesaria
4. **Validación**: Verificar supuestos y detectar inconsistencias
5. **Trade-offs**: Explorar decisiones difíciles y prioridades

## Estructura de la Entrevista

### Fase 1: Comprensión del Problema (5-7 preguntas)

**Objetivo**: Entender el problema real, no la solución imaginada.

Preguntas ejemplo:
- "¿Cuál es el momento específico en que los usuarios sienten más frustración con las soluciones actuales?"
- "Si este proyecto fracasa, ¿qué no habremos logrado que sea importante?"
- "¿Quién más además de ti se beneficia si esto existe? ¿Cómo?"
- "¿Qué intentos previos ha habido para resolver esto? ¿Por qué no funcionaron?"
- "Si tuvieras que explicar el valor en una frase a alguien que no conoce el contexto, ¿qué dirías?"

### Fase 2: Usuarios y Contexto (5-8 preguntas)

**Objetivo**: Definir usuarios objetivo con precisión.

Preguntas ejemplo:
- "Describe un día típico de tu usuario principal. ¿En qué momento usaría esto?"
- "¿Qué nivel técnico tienen los usuarios? ¿Necesitan onboarding?"
- "¿Hay diferentes tipos de usuarios con diferentes necesidades? ¿Cuáles priorizamos?"
- "¿Qué dispositivos usan principalmente? ¿Importa el contexto (oficina, móvil, etc.)?"
- "¿Cuántos usuarios esperas en el primer mes? ¿Y en un año?"

### Fase 3: Funcionalidades Core (8-12 preguntas)

**Objetivo**: Definir el MVP mínimo viable con detalle.

Para CADA funcionalidad preguntar:
- "¿Cuál es el flujo paso a paso desde que el usuario inicia hasta que completa la acción?"
- "¿Qué pasa si algo sale mal en este flujo? ¿Cómo se recupera el usuario?"
- "¿Hay casos edge que debamos manejar desde el MVP?"
- "¿Esta funcionalidad es REALMENTE necesaria para el MVP o puede esperar?"
- "¿Cómo sabremos si esta funcionalidad es exitosa? ¿Qué métrica usamos?"

### Fase 4: UI/UX (5-8 preguntas)

**Objetivo**: Definir la experiencia de usuario.

Preguntas ejemplo:
- "¿Hay alguna app existente cuyo estilo visual te gustaría emular?"
- "¿Qué acción es la más importante que el usuario debe poder hacer en 5 segundos?"
- "¿Preferimos una UI más simple pero limitada, o más compleja pero completa?"
- "¿Hay requisitos de accesibilidad específicos? ¿Usuarios con discapacidades?"
- "¿El diseño debe ser mobile-first o desktop-first?"

### Fase 5: Técnico (5-8 preguntas)

**Objetivo**: Definir restricciones y preferencias técnicas.

Preguntas ejemplo:
- "¿Hay restricciones de stack tecnológico por políticas de empresa o preferencias?"
- "¿Qué volumen de datos/transacciones manejamos? ¿Hay picos conocidos?"
- "¿Necesitamos funcionalidad offline?"
- "¿Hay integraciones con sistemas existentes? ¿Cuáles y cómo se conectan?"
- "¿Hay requisitos de compliance (GDPR, HIPAA, etc.)?"

### Fase 6: Trade-offs y Prioridades (5-10 preguntas)

**Objetivo**: Entender qué sacrificar cuando hay conflictos.

Preguntas ejemplo:
- "Si tuvieras que elegir entre lanzar más rápido con menos features o más tarde con más features, ¿qué prefieres?"
- "¿Es más importante la experiencia móvil o desktop para el MVP?"
- "Entre rendimiento y funcionalidad, ¿qué priorizamos?"
- "¿Qué features estarías dispuesto a quitar del MVP si el tiempo se acorta a la mitad?"
- "¿Hay algún riesgo técnico que te preocupe especialmente?"

## Técnicas de Seguimiento

### Cuando la respuesta es vaga:
- "Puedes ser más específico sobre [aspecto]?"
- "Dame un ejemplo concreto de cuando esto ocurriría"
- "¿Qué pasaría exactamente en ese escenario?"

### Cuando hay inconsistencias:
- "Antes mencionaste [X], pero ahora dices [Y]. ¿Cómo se reconcilian?"
- "Si [X] es importante, ¿cómo afecta eso a [Y] que también mencionaste?"

### Cuando falta información:
- "No hemos hablado de [aspecto]. ¿Es relevante para este proyecto?"
- "¿Hay algo que no te haya preguntado pero consideras importante?"

## Criterios de Completitud

La entrevista está completa cuando:
- [ ] El problema está claramente definido
- [ ] Los usuarios objetivo están identificados
- [ ] Hay al menos 3 funcionalidades core detalladas
- [ ] Los flujos de usuario principales están definidos
- [ ] Las restricciones técnicas están claras
- [ ] Los trade-offs han sido explorados
- [ ] El usuario ha validado el resumen

## Generación del SPEC.md

Al finalizar:
1. Leer el template de `.claude/templates/SPEC-TEMPLATE.md`
2. Rellenar todas las secciones con la información recopilada
3. Agregar criterios de aceptación específicos para cada feature
4. Incluir métricas de éxito concretas
5. Guardar en `.claude/specs/$ARGUMENTS.md`
6. Presentar resumen al usuario para validación final

## Ejemplo de Flujo

```
Usuario: "Quiero hacer una app de gestión de tareas"

Claude: "Entiendo. Antes de profundizar en features, quiero entender el problema:
¿Por qué las apps de tareas existentes como Todoist o Notion no te funcionan?
¿Qué frustración específica intentas resolver?"

Usuario: "Son muy complicadas para mi equipo pequeño"

Claude: "Interesante. ¿Qué significa 'complicadas' para tu equipo?
¿Es la curva de aprendizaje, la cantidad de clicks para hacer algo,
o que tienen features que no necesitan y confunden?"

[Continúa profundizando...]
```
