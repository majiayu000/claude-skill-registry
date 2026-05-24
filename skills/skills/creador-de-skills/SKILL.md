---
name: creador-de-skills
description: Diseña y genera Skills para Antigravity con estructura predecible, reutilizable y lista para producción. Usar cuando se necesite crear un nuevo skill o convertir un proceso en procedimiento estándar.
---

# Creador de Skills para Antigravity

Skill especializado en diseñar y generar Skills estructurados para el entorno de Antigravity. Produce salidas completas con carpetas, archivos SKILL.md y recursos opcionales.

## Cuándo usar este skill

- Cuando el usuario pida crear un skill nuevo
- Cuando el usuario quiera convertir un prompt largo en un procedimiento reutilizable
- Cuando se necesite estandarizar un proceso repetitivo
- Cuando haya que documentar un workflow como skill
- Cuando el usuario diga "hacé un skill para X"

## Inputs necesarios

- **Objetivo del skill**: ¿Qué debe hacer? (obligatorio)
- **Contexto de uso**: ¿Cuándo se activa? (obligatorio)
- **Nivel de libertad**: alta/media/baja (opcional, se infiere si no se da)
- **Formato de salida esperado**: tabla, lista, JSON, markdown, etc. (opcional)
- **Recursos adicionales**: plantillas, tokens, ejemplos (opcional)

> **Regla**: Si falta el objetivo o el contexto, PREGUNTAR antes de generar.

## Workflow

### Fase 1: Entender

1. Leer el objetivo del usuario
2. Identificar si es skill simple (3-6 pasos) o complejo (fases múltiples)
3. Determinar nivel de libertad según riesgo:
   - **Alta libertad**: brainstorming, ideas, alternativas
   - **Media libertad**: documentos, copys, estructuras
   - **Baja libertad**: scripts, comandos, operaciones técnicas

### Fase 2: Diseñar

4. Definir nombre del skill (minúsculas, guiones, máx 40 chars)
5. Escribir descripción (tercera persona, español, máx 220 chars)
6. Listar triggers concretos (cuándo se activa)
7. Definir inputs necesarios
8. Definir output exacto (formato específico)

### Fase 3: Generar

9. Crear estructura de carpeta
10. Escribir SKILL.md con frontmatter YAML
11. Agregar recursos solo si aportan valor real

### Fase 4: Validar

12. Verificar checklist:
    - [ ] Nombre cumple reglas (minúsculas, guiones, ≤40 chars)
    - [ ] Descripción en tercera persona, ≤220 chars
    - [ ] Triggers claros y concretos
    - [ ] Inputs definidos
    - [ ] Output con formato exacto
    - [ ] Sin archivos innecesarios

## Instrucciones

### Reglas de nombre (YAML)

```yaml
# ✅ Correcto
name: planificar-video
name: auditar-landing
name: responder-emails

# ❌ Incorrecto
name: Planificar_Video      # mayúsculas y guion bajo
name: skill-para-marketing  # muy genérico
name: herramienta-chatgpt   # nombre de herramienta innecesario
```

### Reglas de descripción

- En español
- Tercera persona
- Máximo 220 caracteres
- Dice QUÉ hace y CUÁNDO usarlo
- Sin marketing, solo operativo

### Estructura de carpetas

```
.agent/skills/<nombre-del-skill>/
├── SKILL.md           # Obligatorio
├── recursos/          # Opcional: guías, plantillas, tokens
├── scripts/           # Opcional: utilidades ejecutables
└── ejemplos/          # Opcional: implementaciones de referencia
```

### Principios de escritura

1. **Claridad sobre longitud**: pocas reglas, muy claras
2. **No relleno**: sin explicaciones tipo blog
3. **Separación de responsabilidades**: estilo → recursos, pasos → workflow
4. **Pedir datos cuando falten**: si un input es crítico, preguntar
5. **Salida estandarizada**: formato exacto definido

### Manejo de errores

- Si el output no cumple formato → volver al paso de diseño y ajustar
- Si hay ambigüedad → preguntar antes de asumir
- Si falta información crítica → solicitar al usuario antes de generar

## Output (formato exacto)

Cuando se crea un skill, la salida debe seguir este formato:

```markdown
## Carpeta

`.agent/skills/<nombre-del-skill>/`

## SKILL.md

---

name: <nombre-del-skill>
description: <descripción breve en tercera persona>

---

# <Título del skill>

## Cuándo usar este skill

- trigger 1
- trigger 2

## Inputs necesarios

- input 1 (obligatorio/opcional)
- input 2

## Workflow

1. Paso 1
2. Paso 2
3. Paso 3

## Instrucciones

[Detalles específicos del skill]

## Output (formato exacto)

[Definición del formato de salida]

## Recursos opcionales (solo si aplica)

- `recursos/<archivo>.md` - descripción
- `scripts/<archivo>.sh` - descripción
```

---

## Ideas de skills sugeridos

Si el usuario está explorando qué skills crear, sugerir:

| Skill              | Descripción                                                 |
| ------------------ | ----------------------------------------------------------- |
| `estilo-y-marca`   | Define tokens de marca, tono de voz, paleta de colores      |
| `planificar-video` | Estructura guiones y planificación de contenido audiovisual |
| `auditar-landing`  | Revisa landing pages con checklist de UX/SEO/conversión     |
| `debug-app`        | Proceso sistemático para diagnosticar bugs en aplicaciones  |
| `responder-emails` | Genera respuestas con tono específico según contexto        |
| `documentar-api`   | Crea documentación estándar para endpoints                  |
| `revisar-codigo`   | Checklist de code review con principios SOLID               |
