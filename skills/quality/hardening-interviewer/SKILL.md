---
name: hardening-interviewer
description:
  Realiza entrevistas de feedback post-MVP para identificar bugs, mejoras UX,
  problemas de performance, seguridad y features faltantes
allowed-tools: AskUserQuestionTool, Read, Write
---

# Hardening Interviewer Skill

Realizas entrevistas de feedback post-MVP especializadas en identificar
problemas, bugs y mejoras necesarias para fortalecer el producto antes de
producción.

## Filosofía

> "La diferencia entre un MVP y un producto de producción está en los detalles
> que solo el usuario real puede revelarte después de usar el sistema."

## Diferencias vs spec-interviewer

| Aspecto   | spec-interviewer        | hardening-interviewer |
| --------- | ----------------------- | --------------------- |
| Objetivo  | Explorar lo desconocido | Encontrar problemas   |
| Asume     | Usuario tiene idea      | Usuario usó el MVP    |
| Preguntas | 30-40 exploratorias     | 15-25 directas        |
| Output    | SPEC.md                 | FEEDBACK.md           |
| Enfoque   | Qué construir           | Qué arreglar/mejorar  |

## Principios de la Entrevista

1. **Orientada a problemas**: Buscar activamente lo que no funciona
2. **Concreta**: Pedir ejemplos específicos, no opiniones generales
3. **Priorizada**: Siempre pedir severidad y urgencia
4. **Reproducible**: Obtener pasos exactos para replicar bugs
5. **Accionable**: Cada issue debe poder convertirse en tarea

## Estructura de la Entrevista

### Fase 1: BUGS - Errores Críticos (3-5 preguntas)

**Objetivo**: Identificar bugs que rompen funcionalidad.

Preguntas clave:

- "¿Hay alguna funcionalidad que directamente no funciona o da error?"
- "¿Has visto errores en la consola del navegador o mensajes de error
  inesperados?"
- "¿Hay algún flujo que se queda colgado o no termina como debería?"
- "¿El problema ocurre siempre o es intermitente? ¿En qué condiciones?"
- "¿El bug aparece en algún dispositivo o navegador específico?"

Para cada bug reportado, obtener:

- **Qué pasa** vs **Qué debería pasar**
- **Pasos exactos** para reproducir
- **Frecuencia**: Siempre, a veces, aleatorio
- **Contexto**: Navegador, dispositivo, datos específicos

### Fase 2: UX - Experiencia de Usuario (3-5 preguntas)

**Objetivo**: Identificar fricciones en la experiencia.

Preguntas clave:

- "¿Hay alguna acción que requiera más clicks de los que esperabas?"
- "¿Hubo algún momento en que no supiste qué hacer o dónde ir?"
- "¿Falta feedback visual en alguna acción (loading, confirmación, error)?"
- "¿Hay elementos de UI que no respondan como esperas (botones, links, inputs)?"
- "¿El diseño se ve bien en móvil o hay problemas de layout?"

Para cada issue UX, obtener:

- **Dónde** ocurre (pantalla/componente)
- **Qué esperabas** vs **Qué encontraste**
- **Impacto**: Molesto, confuso, bloqueante

### Fase 3: PERFORMANCE - Rendimiento (2-4 preguntas)

**Objetivo**: Identificar lentitudes y problemas de rendimiento.

Preguntas clave:

- "¿Hay alguna pantalla que tarde demasiado en cargar?"
- "¿Alguna acción se siente lenta (guardar, buscar, filtrar)?"
- "¿Has notado lag o parpadeos en la interfaz?"
- "¿La app se siente pesada o consume mucha memoria/batería?"

Para cada issue de performance, obtener:

- **Dónde** ocurre
- **Tiempo aproximado** de espera actual
- **Tiempo aceptable** según el usuario

### Fase 4: SECURITY - Seguridad (2-3 preguntas)

**Objetivo**: Identificar vulnerabilidades obvias.

Preguntas clave:

- "¿Pudiste acceder a datos o funciones que no deberías?"
- "¿Hay información sensible visible que debería estar oculta?"
- "¿La sesión expira correctamente? ¿Probaste cerrar y volver?"
- "¿Probaste introducir datos inesperados (caracteres especiales, textos
  largos)?"

Para cada issue de seguridad, obtener:

- **Tipo de vulnerabilidad** (auth, data leak, XSS, etc.)
- **Qué datos/acciones están en riesgo**
- **Cómo lo reproduciste**

### Fase 5: FEATURES - Funcionalidades Faltantes (2-4 preguntas)

**Objetivo**: Identificar gaps funcionales.

Preguntas clave:

- "¿Hay alguna funcionalidad prometida en el SPEC que no encontraste?"
- "¿Qué feature 'obvia' asumiste que existiría y no estaba?"
- "¿Qué te impidió completar un flujo que querías hacer?"
- "¿Hay alguna integración que esperabas y no funciona?"

Para cada feature faltante, obtener:

- **Qué falta** exactamente
- **Por qué es importante** (valor)
- **Prioridad**: Critical, High, Medium, Low

### Fase 6: PRIORIZACIÓN (2-3 preguntas)

**Objetivo**: Establecer orden de ejecución.

Preguntas clave:

- "De todo lo mencionado, ¿cuáles son los 3 problemas TOP que bloquean uso
  real?"
- "¿Hay algo que consideres must-fix antes de mostrar a usuarios reales?"
- "Si solo pudiéramos arreglar la mitad, ¿cuáles elegirías?"

## Técnicas de Profundización

### Cuando la respuesta es vaga:

- "Dame un ejemplo concreto de cuándo pasó esto"
- "¿Puedes mostrarme exactamente dónde ocurre?"
- "¿Qué estabas intentando hacer cuando lo notaste?"

### Cuando el usuario no recuerda:

- "¿En qué pantalla estabas cuando lo viste?"
- "¿Fue durante un flujo específico como [login, checkout, etc.]?"
- "¿Puedes intentar reproducirlo ahora?"

### Cuando hay muchos issues:

- "Ordenemos por impacto: ¿cuál rompe más la experiencia?"
- "¿Cuál de estos te haría dejar de usar el producto?"
- "¿Alguno de estos tiene workaround temporal?"

## Clasificación de Severidad

### CRITICAL (Bloqueante)

- El sistema no se puede usar
- Pérdida de datos
- Vulnerabilidad de seguridad grave
- Error que afecta a todos los usuarios

### HIGH (Importante)

- Funcionalidad core no funciona correctamente
- Experiencia muy degradada
- Bug que afecta a muchos usuarios
- Performance inaceptable (>5 segundos)

### MEDIUM (Molesto)

- Funcionalidad secundaria con problemas
- UX inconveniente pero usable
- Bug con workaround conocido
- Performance lenta pero tolerable (2-5 segundos)

### LOW (Cosmético)

- Issues visuales menores
- Mejoras "nice to have"
- Edge cases poco frecuentes

## Criterios de Completitud

La entrevista está completa cuando:

- [ ] Se han explorado las 5 categorías (BUGS, UX, PERF, SEC, FEAT)
- [ ] Cada issue tiene severidad asignada
- [ ] Los issues críticos tienen pasos de reproducción
- [ ] El usuario ha priorizado los issues
- [ ] Se ha generado FEEDBACK.md completo

## Generación del FEEDBACK.md

Al finalizar:

1. Leer template de `.claude/templates/FEEDBACK-TEMPLATE.md`
2. Categorizar todos los issues recopilados
3. Asignar IDs únicos (BUG-001, UX-001, PERF-001, etc.)
4. Incluir pasos de reproducción donde aplique
5. Guardar en `.claude/feedback/FEEDBACK-<proyecto>.md`
6. Mostrar resumen con conteo por severidad

## Ejemplo de Flujo

```
Claude: "Empecemos por los bugs críticos. ¿Hay alguna funcionalidad que
directamente no funcione o dé error?"

Usuario: "El login falla con emails en mayúsculas"

Claude: "Entendido. ¿Qué error exacto ves? ¿Un mensaje, una pantalla en blanco,
o simplemente no pasa nada?"

Usuario: "Dice 'email no encontrado' aunque el usuario existe"

Claude: "Perfecto, eso es un bug de validación. ¿Esto pasa solo con emails
que tienen letras mayúsculas o también con otros formatos?"

[Continúa profundizando hasta tener todos los detalles...]

Claude: "De 1 a 10, donde 10 es 'no puedo usar la app sin esto',
¿qué tan crítico es este bug?"

Usuario: "8, es bastante malo"

Claude: "Lo clasifico como HIGH entonces. ¿Hay algún otro bug similar
con el login o auth?"
```

## Output Esperado

1. FEEDBACK.md estructurado con todos los issues
2. Conteo por categoría y severidad
3. Lista priorizada del usuario
4. Issues listos para convertirse en historias
