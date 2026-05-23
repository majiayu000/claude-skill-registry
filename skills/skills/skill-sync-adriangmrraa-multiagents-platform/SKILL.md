---
name: "Skill Synchronizer"
description: "Lee los metadatos de todas las skills y actualiza el índice en AGENTS.md."
trigger: "Después de crear o modificar una skill, o cuando el usuario diga 'sincronizar skills'."
scope: "SYSTEM"
auto-invoke: true
---

# Protocolo de Sincronización de Skills

Tu objetivo es mantener el `AGENTS.md` actualizado con un índice vivo de capacidades.

## 1. Escaneo de Skills
1.  Busca recursivamente en `.agent/skills/`.
2.  Para cada carpeta, lee el archivo `SKILL.md`.
3.  Extrae el bloque YAML (Frontmatter) para obtener: `name`, `description` y `trigger`.

## 2. Generación del Índice
Formatea la información extraída en una tabla Markdown:

| Skill Name | Trigger | Descripción |
| :--- | :--- | :--- |
| **Sovereign Backend** | *Backend, API, DB* | Experto en FastAPI y Credenciales. |
| **Nexus UI** | *Frontend, React* | Componentes visuales y Hooks. |

## 3. Inyección Quirúrgica
1.  Lee el archivo `AGENTS.md` en la raíz.
2.  Busca la sección `## 5. Available Skills Index`.
    - Si no existe, créala al final del archivo.
3.  Reemplaza **solo** el contenido de esa sección con la nueva tabla generada.
4.  **IMPORTANTE:** No toques ninguna otra sección del archivo (Project Identity, Architecture, etc.).

## 4. Confirmación
Al finalizar, responde: *"✅ Índice de Skills sincronizado. [N] habilidades detectadas."*
