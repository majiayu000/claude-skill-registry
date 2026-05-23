---
name: planificacion-pro
description: Convierte una idea en un plan ejecutable por fases, con checklist, riesgos y entregables. Úsalo cuando haya que pasar de idea a acción sin improvisar.
---

# Planificación Pro

Skill especializado en convertir ideas o proyectos en planes de acción estructurados con fases, tiempos, entregables y gestión de riesgos.

## Cuándo usar este skill

- Cuando el usuario pida un plan paso a paso, una estrategia o una hoja de ruta
- Cuando haya que entregar algo (landing, vídeo, proyecto, lanzamiento) con tiempos
- Cuando el usuario tenga muchas tareas sueltas y quiera ordenarlas
- Cuando se necesite convertir una idea vaga en acciones concretas
- Cuando alguien diga "¿cómo organizo esto?" o "necesito un plan para X"

## Inputs necesarios

> **Regla**: Si falta alguno de estos inputs, PREGUNTAR antes de planificar.

| Input                    | Descripción                                                 | Obligatorio |
| ------------------------ | ----------------------------------------------------------- | ----------- |
| **Resultado final**      | ¿Qué significa "terminado"? Definición clara del entregable | ✅ Sí       |
| **Fecha límite / ritmo** | Hoy, esta semana, este mes, sin prisa                       | ✅ Sí       |
| **Recursos disponibles** | Herramientas, equipo, presupuesto, tiempo diario            | ✅ Sí       |
| **Criterios de éxito**   | ¿Qué debe cumplir para estar bien?                          | ✅ Sí       |
| **Nivel del usuario**    | Principiante / intermedio / avanzado                        | Opcional    |

## Workflow

### Fase 1: Definir el resultado

1. Escribir el resultado final en 1 frase clara
2. Listar 3 criterios de éxito medibles

### Fase 2: Estructurar por fases (máx. 4)

| Fase                          | Propósito                                            |
| ----------------------------- | ---------------------------------------------------- |
| **1. Preparación**            | Reunir recursos, definir alcance, configurar entorno |
| **2. Producción / Ejecución** | Crear, desarrollar, construir el entregable          |
| **3. Revisión / QA**          | Verificar calidad, corregir errores, pulir           |
| **4. Publicación / Entrega**  | Lanzar, entregar, comunicar resultado                |

### Fase 3: Detallar cada fase

3. Para cada fase, definir:
   - Tareas en orden de ejecución
   - Entregable claro (qué sale de esa fase)
   - Tiempo estimado por tarea
   - Dependencias (si aplica)

### Fase 4: Gestionar riesgos

4. Identificar 3–5 riesgos con formato:
   - **Si pasa X** → **hago Y**

### Fase 5: Validar

5. Crear checklist final de verificación

## Instrucciones

### Reglas de calidad

| Regla                   | Aplicación                                   |
| ----------------------- | -------------------------------------------- |
| Evitar planes infinitos | Priorizar lo que desbloquea lo siguiente     |
| Indicar dependencias    | "Esto depende de X terminado"                |
| Adaptar al nivel        | Principiante = menos pasos, opciones simples |
|                         | Avanzado = optimizaciones y atajos           |
| Tiempos realistas       | Incluir buffer del 20% para imprevistos      |

### Criterios para buenos entregables

Un entregable bien definido debe responder:

- ¿Qué es exactamente? (archivo, deploy, documento)
- ¿Cómo sé que está listo?
- ¿Quién lo recibe o dónde se publica?

### Manejo de errores

- Si el plan es demasiado largo → dividir en sprints/etapas
- Si hay ambigüedad en el resultado final → reclarificar antes de continuar
- Si los recursos son insuficientes → proponer versión MVP primero
- Si hay dependencias circulares → reorganizar orden de tareas

## Output (formato exacto)

```markdown
## 🎯 Resultado Final

**Objetivo**: [1 frase clara de qué significa "terminado"]

### Criterios de éxito

1. ✅ [Criterio medible 1]
2. ✅ [Criterio medible 2]
3. ✅ [Criterio medible 3]

---

## 📋 Plan por Fases

### Fase 1: Preparación

**Entregable**: [Qué sale de esta fase]
**Duración estimada**: [X horas/días]

| #   | Tarea   | Tiempo | Dependencia |
| --- | ------- | ------ | ----------- |
| 1.1 | [Tarea] | Xh     | -           |
| 1.2 | [Tarea] | Xh     | 1.1         |

---

### Fase 2: Producción / Ejecución

**Entregable**: [Qué sale de esta fase]
**Duración estimada**: [X horas/días]

| #   | Tarea   | Tiempo | Dependencia |
| --- | ------- | ------ | ----------- |
| 2.1 | [Tarea] | Xh     | Fase 1      |
| 2.2 | [Tarea] | Xh     | 2.1         |

---

### Fase 3: Revisión / QA

**Entregable**: [Qué sale de esta fase]
**Duración estimada**: [X horas/días]

| #   | Tarea   | Tiempo | Dependencia |
| --- | ------- | ------ | ----------- |
| 3.1 | [Tarea] | Xh     | Fase 2      |
| 3.2 | [Tarea] | Xh     | 3.1         |

---

### Fase 4: Publicación / Entrega

**Entregable**: [Qué sale de esta fase]
**Duración estimada**: [X horas/días]

| #   | Tarea   | Tiempo | Dependencia |
| --- | ------- | ------ | ----------- |
| 4.1 | [Tarea] | Xh     | Fase 3      |
| 4.2 | [Tarea] | Xh     | 4.1         |

---

## ⚠️ Riesgos y Mitigación

| #   | Si pasa... | Hago...                |
| --- | ---------- | ---------------------- |
| 1   | [Riesgo 1] | [Acción de mitigación] |
| 2   | [Riesgo 2] | [Acción de mitigación] |
| 3   | [Riesgo 3] | [Acción de mitigación] |
| 4   | [Riesgo 4] | [Acción de mitigación] |
| 5   | [Riesgo 5] | [Acción de mitigación] |

---

## ✅ Checklist Final de Validación

### Antes de empezar

- [ ] Tengo todos los recursos necesarios
- [ ] Entiendo el resultado final esperado
- [ ] Conozco la fecha límite

### Antes de entregar

- [ ] Cumple criterio de éxito 1
- [ ] Cumple criterio de éxito 2
- [ ] Cumple criterio de éxito 3
- [ ] Revisé calidad / QA
- [ ] Está listo para publicar/entregar

---

## 📊 Resumen

| Métrica                   | Valor        |
| ------------------------- | ------------ |
| **Total de fases**        | X            |
| **Total de tareas**       | X            |
| **Tiempo estimado total** | X horas/días |
| **Riesgos identificados** | X            |
```
