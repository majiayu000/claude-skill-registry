---
name: "Skill_Forge_Master"
description: "Arquitecto y generador de Skills. Define, estructura y registra nuevas capacidades para el agente Antigravity."
trigger: "crear skill, nueva habilidad, skill architect, forge skill, capability, nueva skill"
scope: "META"
auto-invoke: true
---

# Skill Forge Master - Platform AI Solutions

## 1. Concepto: Meta-Cognición Estructurada

### Filosofía
Una **Skill** no es solo código; es un **paquete de conocimiento ejecutable**.
Este Master Skill actúa como la "fábrica" que estandariza cómo el agente aprende nuevas capacidades.

### Proceso de Forjado
1. **Analysis**: Entender qué problema resuelve la nueva skill.
2. **Definition**: Determinar scope, triggers y dependencias.
3. **Architecting**: Diseñar la estructura de datos y flujos necesarios.
4. **Generation**: Crear el archivo `SKILL.md` con las 10 secciones estándar.
5. **Registration**: Inscribir la skill en `agents.md` para su descubrimiento.

## 2. Estructura Canónica de una Skill

Toda nueva Skill DEBE seguir esta plantilla rigurosa:

### YAML Frontmatter
```yaml
---
name: "Nombre_De_La_Skill" (SnakeCase o PascalCase)
description: "Descripción concisa en español de qué hace."
trigger: "palabras, clave, que, activan, la, skill" (lista separada por comas)
scope: "DOMINIO" (BACKEND, FRONTEND, DB, SECURITY, etc.)
auto-invoke: true (casi siempre true)
---
```

### Secciones Obligatorias (Markdown)

1. **Concepto**: Filosofía y arquitectura de alto nivel (Diagramas ASCII).
2. **Modelo de Datos**: Tablas SQL, Schemas Pydantic/TypeScript.
3. **Frontend Implementation**: Componentes, Hooks, Estado.
4. **Backend Implementation**: Endpoints, Servicios, Lógica de Negocio.
5. **Integraciones**: APIs externas, Webhooks, Auth flows.
6. **Persistencia**: Cómo y dónde se guardan los datos.
7. **Troubleshooting**: Errores comunes y soluciones (Causa -> Solución).
8. **Security**: Best practices específicas del dominio.
9. **Checklist de Implementación**: Lista de tareas verificables.

## 3. Flujo de Generación (The Forge Protocol)

### Fase 1: Entrevista de Requerimientos
El usuario pide "Crear una skill para X".
El Forge Master debe identificar:
- **Objetivo**: ¿Qué debe lograr?
- **Tecnologías**: ¿Qué APIs o librerías usa?
- **Dependencias**: ¿Requiere DB, Frontend, Backend o todo?

### Fase 2: Generación del Artefacto
Crear el archivo en `.agent/skills/[Skill_Name]/SKILL.md`.

**Reglas de Oro de Generación:**
- **Idioma**: Español técnico.
- **Formato**: Markdown estricto (headers, code blocks).
- **Código**: Incluir snippets realistas y funcionales (no placeholders vagos).
- **Rigor**: No omitir secciones. Si no aplica, explicar por qué.

### Fase 3: Registro en el Cerebro
Actualizar `.agent/agents.md` agregando la nueva skill en la tabla correspondiente:

```markdown
| **[Nombre_Skill](ruta)** | `triggers` | Descripción corta |
```

## 4. Ejemplo: "Discount Engine Specialist"

Si el usuario pide una skill para manejar descuentos:

1. **Analizar**: Necesita DB (tablas descuentos), Backend (cálculo de precio), Frontend (UI de cupones).
2. **Estructurar**:
   - `discounts` table (code, type, value, valid_until).
   - `apply_discount` service logic.
   - `CartSummary` component update.
3. **Generar**: Escribir `SKILL.md` completo.
4. **Registrar**: Agregar a `agents.md` bajo "Commerce & Integrations".

## 5. Troubleshooting (Meta-Errores)

### "La skill no se activa"
- **Causa**: Triggers mal definidos o no agregada a `agents.md`.
- **Solución**: Revisar YAML frontmatter y entrada en `agents.md`.

### "El agente alucina código viejo"
- **Causa**: La skill no define claramente los estándares nuevos (ej: usar `useApi` en vez de `fetch`).
- **Solución**: Reforzar la sección de "Anti-Patrones" o "Implementation" en la Skill.

### "Skill demasiado genérica"
- **Causa**: Falta de detalle en la sección de "Backend/Frontend Implementation".
- **Solución**: Re-generar la skill incluyendo nombres de tablas y funciones exactas del proyecto.

## 6. Checklist de Creación

- [ ] Carpeta creada: `.agent/skills/[Nombre]/`
- [ ] Archivo `SKILL.md` creado
- [ ] Frontmatter YAML válido
- [ ] 10 Secciones completas
- [ ] Código de ejemplo verificado con `.antigravity_rules`
- [ ] Registrada en `.agent/agents.md`
- [ ] Usuario notificado

---

**Tip**: Una buena Skill no solo dice *qué* hacer, sino *cómo* hacerlo siguiendo la arquitectura soberana del proyecto.
