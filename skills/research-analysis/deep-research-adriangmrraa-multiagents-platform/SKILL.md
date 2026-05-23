---
name: "Deep Researcher"
description: "Investiga documentación oficial y valida soluciones en internet antes de implementar."
trigger: "Antes de usar una librería nueva, al enfrentar un error desconocido, o cuando el usuario diga 'investiga esto'."
scope: "GLOBAL"
auto-invoke: true
---

# Protocolo de Investigación (Measure Twice, Cut Once)

Tu objetivo es validar la viabilidad técnica leyendo fuentes externas actualizadas antes de escribir código.

## 1. Estrategia de Búsqueda
Antes de asumir una sintaxis o función:
1.  **Identifica los Actores:** ¿Qué tecnologías están involucradas? (ej. *FastAPI, Pydantic v2, Supabase Vector*).
2.  **Formula Queries Precisas:**
    - Mal: "Cómo usar pydantic"
    - Bien: "Pydantic v2 model_validator syntax example"
    - Bien: "Supabase pgvector python client insert guide"
3.  **Ejecuta Búsqueda:** Utiliza tus herramientas de navegación/búsqueda para leer la documentación oficial o issues de GitHub recientes.

## 2. Validación de Contexto (Sovereign Check)
Cruza la información encontrada con las reglas de `AGENTS.md`:
- ¿La solución encontrada requiere variables de entorno globales? -> **Descartar** (Viola Protocolo Soberano).
- ¿La librería sugerida es compatible con Python 3.10+ asíncrono? -> **Verificar**.

## 3. Síntesis del Plan
Antes de escribir el código final, genera un breve resumen:
> "He investigado la documentación de [Librería].
> La versión actual requiere usar el método X en lugar de Y.
> Este es el plan de implementación compatible con Nexus v6..."

## 4. Anti-Patrones a Evitar
- No uses tutoriales de más de 2 años de antigüedad sin verificar.
- No inventes importaciones. Si la documentación no lo menciona, no existe.
