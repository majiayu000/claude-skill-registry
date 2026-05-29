---
name: lateralize-projects
description: Lateralización de conocimiento Gentleman a otros proyectos - sync, propagación y evolución continua.
trigger: lateralize OR propagate OR sync OR ingest OR spread knowledge
scope: global
---

# Skill: Lateralize Projects

## Contexto

Lateralización = Aplicar conocimiento de Gentleman a otros proyectos del Hive. Gentleman es el cerebro central; los proyectos son extremidades que consumen y contribuyen conocimiento.

## Reglas Críticas

1. **Gentleman es Source of Truth** - No crear conocimiento duplicado en proyectos hijos.
2. **Pull, nunca Push** - Proyectos sincronizan desde Gentleman, no al revés.
3. **Registrar en Manifest** - Todo item nuevo debe estar en SKILL_MANIFEST.md.
4. **Clean Plate Protocol** - Archivos de ingesta se vacían tras procesarse.

## Flujo de Lateralización

```
┌─────────────────────────────────────────────────────────┐
│                  LATERALIZATION FLOW                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐      ┌─────────────┐                   │
│  │  GENTLEMAN  │      │   PROJECT   │                   │
│  │  (Cortex)   │◄────►│   (Limb)    │                   │
│  └──────┬──────┘      └──────┬──────┘                   │
│         │                    │                           │
│    knowledge/           .gentleman/                      │
│    ├── chuletas/        └── skills/  (symlink or copy)  │
│    ├── protocols/                                        │
│    └── EUREKA/                                          │
│                                                          │
│  COMMANDS:                                               │
│  • python sync_ai.py --verify    → Audit knowledge      │
│  • python sync_ai.py --ingest X  → Ingest from project  │
│  • python sync_ai.py --propagate → Push to projects     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Procedimiento

### 1. Verificar Estado
```bash
cd D:\Proyectos\gentleman
python sync_ai.py --verify
```

Revisar:
- `Manifested Items` vs `Physical Items`
- `MISSING FROM DISK` → Crear o remover del manifest
- `UNREGISTERED` → Agregar al manifest

### 2. Ingestar desde Proyecto
```bash
python sync_ai.py --ingest raphael
python sync_ai.py --ingest aliciastore
```

Esto trae:
- EUREKA patches encontrados
- Lecciones aprendidas
- Nuevas chuletas

### 3. Propagar a Proyectos
```bash
python sync_ai.py --propagate
```

Esto sincroniza:
- Skills actualizados
- Protocolos nuevos
- AGENTS.md template

### 4. Crear Nuevo Item

```python
# Template para nueva chuleta
"""
# SKILL: [NOMBRE]

> "Quote memorable"

---

## 1. [Sección Principal]

### [Subsección]
| Columna1 | Columna2 |
|----------|----------|
| Dato1    | Dato2    |

### Implementación
```python
def ejemplo():
    pass
```

---

**Status:** RESEARCH COMPLETE ✅
"""
```

### 5. Registrar en Manifest

Agregar línea en `knowledge/SKILL_MANIFEST.md`:
```markdown
| `NOMBRE.md` | Descripción breve. | Categoría | **New** |
```

### 6. Git Sync
```bash
git add -A
git commit -m "feat(knowledge): add [item]"
git push
```

## Ejemplo Completo

```python
# lateralize.py - Script de lateralización
from pathlib import Path
import shutil

GENTLEMAN = Path("D:/Proyectos/gentleman")
PROJECTS = ["raphael", "aliciastore", "terrazos"]

def lateralize_skill(skill_name: str):
    """Copiar skill a todos los proyectos."""
    skill_path = GENTLEMAN / "skills" / skill_name
    
    if not skill_path.exists():
        print(f"Skill {skill_name} not found")
        return
    
    for project in PROJECTS:
        target = Path(f"D:/Proyectos/{project}/.gentleman/skills/{skill_name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        
        if target.exists():
            shutil.rmtree(target)
        
        shutil.copytree(skill_path, target)
        print(f"✅ {skill_name} → {project}")

def ingest_eureka(project: str):
    """Traer EUREKA patches de un proyecto."""
    source = Path(f"D:/Proyectos/{project}/docs/EUREKA")
    
    if not source.exists():
        return
    
    for patch in source.glob("*.md"):
        target = GENTLEMAN / "knowledge" / "EUREKA" / patch.name
        if not target.exists():
            shutil.copy2(patch, target)
            print(f"📥 Ingested: {patch.name}")
```

## Recursos Relacionados

| Recurso | Descripción |
|---------|-------------|
| `sync_ai.py` | Script principal de sincronización |
| `SKILL_MANIFEST.md` | Registro de todo el conocimiento |
| `PROTOCOL_KNOWLEDGE_EVOLUTION.md` | Auto-evolución |
| `GENTLEMAN_TO_RAPHAEL.md` | Comunicación entre cerebros |
