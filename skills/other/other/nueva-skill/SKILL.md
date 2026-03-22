---
name: nueva-skill
description: Usar al detectar una tarea repetitiva que merece convertirse en skill
---

## Cuándo usar esta skill

- Cuando una tarea se repite frecuentemente
- Al identificar un patrón que debería documentarse
- Cuando el usuario pida crear una nueva skill

## Contexto necesario antes de empezar

1. Identificar la tarea repetitiva
2. Documentar los pasos que se siguen
3. Identificar patrones críticos (SIEMPRE/NUNCA/PREFERENTEMENTE)
4. Definir checklist de validación

## Pasos

### 1. Crear carpeta de skill

```bash
mkdir .windsurf/skills/[nombre-skill]
```

### 2. Crear SKILL.md con estructura

```markdown
---
name: nombre-skill
description: [Una línea clara de CUÁNDO invocar esta skill]
---

## Cuándo usar esta skill
[Lista de triggers específicos]

## Contexto necesario antes de empezar
[Qué archivos leer, qué información recopilar]

## Pasos
[Numerados, con rutas REALES del proyecto]

<patrones_criticos>
SIEMPRE: [lista]
NUNCA: [lista]
PREFERENTEMENTE: [lista]
</patrones_criticos>

## Checklist de validación
- [ ] [comando] pasa sin errores
- [ ] ...
```

### 3. Registrar en orchestrator.md

Añadir la nueva skill a la tabla de skills disponibles.

<patrones_criticos>
SIEMPRE:
- Descripción clara de cuándo usar la skill
- Pasos concretos y accionables
- Checklist de validación al final
- Usar rutas reales del proyecto

NUNCA:
- Skills demasiado genéricas
- Duplicar información que ya está en rules
- Pasos vagos o ambiguos

PREFERENTEMENTE:
- Incluir ejemplos del proyecto
- Mantener skills enfocadas en una tarea
- Actualizar orchestrator.md al crear skill
</patrones_criticos>

## Checklist de validación

- [ ] Skill tiene descripción clara
- [ ] Pasos son accionables
- [ ] Checklist de validación incluido
- [ ] Registrada en orchestrator.md
