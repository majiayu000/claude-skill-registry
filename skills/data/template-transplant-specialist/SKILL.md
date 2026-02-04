---
name: Template Transplant Specialist
description: Extrae y distribuye instrucciones de un system prompt legacy en las capas correctas (Wizard, Tool Config, Sistema Interno).
---

# 🧬 Template Transplant Specialist

## Propósito

Esta skill te permite **extraer system prompts de proyectos legacy** y distribuirlos correctamente en la arquitectura multi-capa de Platform AI Solutions:

1. **Wizard** (configuración del agente en el frontend)
2. **Tool Config** (instrucciones tácticas y guías de respuesta por herramienta)
3. **Interno** (reglas de sistema no editables)

## Cuándo Usar Esta Skill

- Tienes un system prompt legacy de otro proyecto (ej: Pointe Coach, E-commerce Bot)
- Necesitas integrarlo en Platform AI Solutions manteniendo su esencia
- Quieres asegurar que las instrucciones estén en los lugares correctos

## Proceso de Trasplante

### Paso 1: Análisis del System Prompt

Lee el system prompt completo del proyecto legacy y identifica las 3 capas:

#### 📋 WIZARD (Editable por Usuario)
Campos que van en `orchestrator_service/app/api/agents.py` → `AGENT_TEMPLATES`:

- **business_name**: Nombre de la tienda/negocio
- **business_context**: Descripción del rubro
- **tone_and_personality**: Estilo de comunicación (tono, puntuación, voseo, etc.)
- **synonym_dictionary**: Diccionario de sinónimos (mapeo de términos informales a categorías base)
- **business_rules**: Reglas de negocio específicas (derivaciones, políticas, envíos, fitting, etc.)
- **catalog_knowledge**: Mapa de categorías y estructura del catálogo
- **store_website**: URL de la  tienda

#### 🔧 TOOL CONFIG (Por Herramienta)
Instrucciones por tool en `orchestrator_service/main.py` → `tactical_injections` + `response_guides`:

Para cada herramienta, extraé:
- **Táctica**: Reglas de CUÁNDO y CÓMO usar la tool (gatillos, validaciones, mapeos)
- **Guía de Respuesta**: Reglas de CÓMO formatear la salida (estructura, CTAs, limitaciones)

Herramientas típicas:
- `search_specific_products`
- `browse_general_storefront`
- `search_by_category`
- `derivhumano`
- `orders`
- `cupones_list`
- `search_knowledge_base`
- `sendemail`

#### ⚙️ INTERNO (Sistema - Hardcoded)
Reglas que van en el core del system prompt (no editables por el usuario):

- **PRIORIDADES**: Orden de ejecución (JSON Output, Veracidad, Anti-Repetición, Anti-Bucle)
- **REGLA DE VERACIDAD**: Prohibiciones de inventar datos (precios, stock, links)
- **REGLAS DE CONTENIDO**: Formato de texto (prohibido markdown, URLs limpias, etc.)
- **FORMAT INSTRUCTIONS**: Esquema JSON de salida

### Paso 2: Extracción Textual

Creá un documento `.md` con la distribución extraída:

```markdown
# 🎨 WIZARD

### business_name
[TEXTO EXTRAÍDO]

### tone_and_personality
[TEXTO EXTRAÍDO]

...

# 🔧 TOOL CONFIG

### search_specific_products

**TÁCTICA:**
[TEXTO EXTRAÍDO]

**GUÍA DE RESPUESTA:**
[TEXTO EXTRAÍDO]

...

# ⚙️ INTERNO

### PRIORIDADES
[TEXTO EXTRAÍDO]

...
```

Guardá este documento en `docs/plantilla_[nombre_proyecto].md`.

### Paso 3: Integración en el Código

#### Opción A: Hardcoded Template (Legacy/Fallback)

Editá `orchestrator_service/app/api/agents.py`:

```python
AGENT_TEMPLATES = {
    "sales": {
        "defaultValue": {
            "agent_name": "[business_name extraído]",
            "agent_tone": "[tone_and_personality extraído]",
            "synonym_dictionary": "[synonym_dictionary extraído]",
            "business_rules": "[business_rules extraído]",
            "catalog_knowledge": "[catalog_knowledge extraído]",
            "store_website": "[store_website extraído]"
        }
    }
}
```

#### Opción B: Database Template (Recomendado - v7.2+)

Insertá el template directamente en la base de datos para que sea dinámico y global:

```sql
INSERT INTO agents (
    name, role, system_prompt_template, config, enabled_tools, 
    is_template, tenant_id, is_active
) VALUES (
    'Nombre del Template', 
    'sales', 
    'Eres un asistente virtual de...', -- Prompt Base
    '{
        "agent_name": "...",
        "agent_tone": "...", 
        "business_rules": "...",
        "synonym_dictionary": "...",
        "store_description": "..."
    }'::jsonb,
    '["search_specific_products", "search_by_category", "orders"]'::jsonb,
    TRUE, -- Marcado como Template
    NULL, -- NULL = Global (Visible para todos)
    FALSE -- Inactivo por defecto
);
```

> [!IMPORTANT]
> Los templates en DB aparecen automáticamente en el Wizard. El Orchestrator los identifica por `is_template = TRUE`. Si `tenant_id` es `NULL`, la plantilla es **Global**.

#### B. Actualizar Tool Instructions

Editá `orchestrator_service/main.py`:

```python
tactical_injections = {
    "search_specific_products": """[TÁCTICA EXTRAÍDA COMPLETA]""",
    "derivhumano": """[TÁCTICA EXTRAÍDA COMPLETA]""",
    # ... resto de tools
}

response_guides = {
    "search_specific_products": """[GUÍA DE RESPUESTA EXTRAÍDA COMPLETA]""",
    "derivhumano": """[GUÍA DE RESPUESTA EXTRAÍDA COMPLETA]""",
    # ... resto de tools
}
```

### Paso 4: Verificación

1. **Frontend**: Abrí el Agent Wizard y verificá que los campos estén pre-poblados
2. **Tool Modal**: Abrí "Configurar Herramientas" y verificá que las instrucciones aparezcan
3. **Chat Test**: Probá el agente con consultas típicas del dominio

## Ejemplo Completo: Pointe Coach

Ver `docs/plantilla pointe coach example.md` para referencia completa.

### Extractos Clave

#### Wizard - Tono y Personalidad
```
**Estilo:** Hablá como una compañera de danza experta. Usá "vos", sé cálida y empática.
**Puntuación (ESTRICTO):** Usá solo el signo de pregunta al final (`?`), nunca el de apertura (`¿`).
**Naturalidad:** Usá frases puente como "Mirá", "Te cuento", "Fijate", "Dale".
```

#### Tool Config - search_specific_products

**TÁCTICA:**
```
BÚSQUEDA INTELIGENTE: Si piden "Malla Negra", busca solo "Malla" (o "Leotardo") y filtra vos mismo si hay variantes en negro.

REGLA DE MAPEO: Antes de usar esta tool, compará la palabra con el Diccionario de Sinónimos.

GATE: Usa `search_specific_products` SIEMPRE que pidan algo específico.
```

**GUÍA DE RESPUESTA:**
```
OBJETIVO PRINCIPAL: Mostrar 3 OPCIONES si la tool devuelve suficientes resultados.

FORMATO DE PRESENTACIÓN (WHATSAPP - LIMPIO):
Secuencia OBLIGATORIA: Intro -> Prod 1 -> Prod 2 -> Prod 3 -> CTA.

REGLA DE CALL TO ACTION:
- CASO 1 (SOLO ZAPATILLAS DE PUNTA): Ofrecer "Fitting"
- CASO 2 (MUCHOS PRODUCTOS): Link a la web
- CASO 3 (POCOS PRODUCTOS): Cierre de servicio
```

## Checklist de Integración

- [ ] Documento de plantilla creado en `docs/plantilla_[proyecto].md`
- [ ] `AGENT_TEMPLATES` actualizado en `agents.py` con wizard defaults
- [ ] `tactical_injections` actualizado en `main.py` con tácticas completas
- [ ] `response_guides` actualizado en `main.py` con guías completas
- [ ] Wizard muestra campos pre-poblados
- [ ] Modal "Configurar Herramientas" muestra instrucciones
- [ ] Agente responde según la personalidad y reglas del legacy

## Reglas de Oro

1. **COPIA TEXTUAL**: No resumas ni adaptes. Copia el texto EXACTO del legacy.
2. **RESPETA LA DISTRIBUCIÓN**: Si una instrucción menciona "SIEMPRE" o es una regla crítica, va en Tool Config o Interno, NO en Wizard.
3. **MÁXIMA FIDELIDAD**: El objetivo es que el agente se comporte IDÉNTICAMENTE al legacy.
4. **DOCUMENTA TODO**: El archivo `.md` de plantilla es la fuente de verdad.

## Troubleshooting

### Problema: Las instrucciones no aparecen en el modal
**Causa**: El endpoint `/admin/tools` no está retornando `prompt_injection` y `response_guide`.  
**Solución**: Verificá que `admin_routes.py` → `get_tools` esté usando `SYSTEM_TOOL_INJECTIONS` y `SYSTEM_TOOL_RESPONSE_GUIDES`.

### Problema: El agente no sigue las reglas
**Causa**: Las instrucciones están en el lugar equivocado (ej: reglas críticas en Wizard en vez de Interno).  
**Solución**: Revisá la distribución y movelas a la capa correcta.

### Problema: El tono no coincide con el legacy
**Causa**: `tone_and_personality` incompleto o genérico.  
**Solución**: Extraé TODO el bloque de "TONO Y PERSONALIDAD" del legacy, incluyendo puntuación, voseo, frases puente, y prohibiciones.

## Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `docs/plantilla_[proyecto].md` | **Fuente de verdad** del trasplante |
| `orchestrator_service/app/api/agents.py` | Wizard defaults (AGENT_TEMPLATES) |
| `orchestrator_service/main.py` | Tool instructions (tactical_injections + response_guides) |
| `orchestrator_service/admin_routes.py` | Endpoint que sirve las tools con sus instructions |
| `frontend_react/src/views/Stores.tsx` | Modal "Configurar Herramientas" |
