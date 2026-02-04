---
name: "Smart Doc Keeper"
description: "Actualiza documentación y skills usando el protocolo 'Non-Destructive Fusion'. Garantiza que el contenido previo se preserve."
trigger: "Cuando el usuario diga 'actualiza la doc', 'documenta este cambio' o tras editar código importante."
scope: "MAINTENANCE"
auto-invoke: false
---

# Protocolo de Documentación "Smart Fusion"

Tu objetivo es mantener la documentación viva sin matar la historia. Eres un **Bibliotecario**, no una trituradora de papel.

> [!CRITICAL]
> **PROTOCOLO DE SEGURIDAD DE DATOS**: Antes de guardar cualquier archivo `.md`, debes tener el contenido ORIGINAL completo en tu contexto. Si no leíste el archivo entero, NO LO TOQUES.

## 1. El Flujo de Fusión (The Fusion Flow)

Cuando debas actualizar un documento (ej. `docs/CHATS_LOGIC.md` tras agregar una función):

1.  **Lectura Total:** Lee el archivo objetivo completo (`read_file`).
2.  **Identificación de Anclaje:** Busca un título o sección donde lógicamente encaje lo nuevo.
    * *Ejemplo:* Si agregaste "Botón de Pánico", busca `## 2. Endpoints & Payloads` o crea `## 3. Nuevas Funcionalidades`.
3.  **Construcción en Memoria:**
    * `[Contenido Viejo Superior]`
    * `+ [Tu Nuevo Contenido]`
    * `[Contenido Viejo Inferior]`
4.  **Escritura:** Guarda el archivo completo fusionado.

## 2. Estrategias de Actualización

### A. Estrategia "Append" (La más segura)
Úsala para bitácoras, changelogs o guías de migración.
* **Acción:** No toques nada de lo existente. Agrega una nueva sección H2 (`##`) al final del documento con la fecha y el cambio.
* *Ejemplo:* `## [v6.2] Nueva integración Chatwoot - Enero 2026` al final de `REPORTE_MASTER.md`.

### B. Estrategia "Injection" (Listas y Tablas)
Úsala para agregar endpoints a `API_REFERENCE.md` o variables a `INFRASTRUCTURE.md`.
* **Acción:** Localiza la tabla o lista existente. Inserta la nueva fila respetando el formato Markdown (`| Col | Col |`). Mantén el resto de filas intactas.

### C. Estrategia "Deprecation" (Reemplazo)
Úsala SOLO si una función vieja dejó de existir.
* **Acción:** En lugar de borrar el texto viejo, envuélvelo en un bloque de alerta:
    ```markdown
    > [!WARNING] DEPRECATED (v6.0)
    > El siguiente método ya no se usa, pero se mantiene por referencia histórica.
    > [Texto Viejo...]
    
    ### Nueva Implementación (v6.2)
    [Texto Nuevo...]
    ```

## 3. Verificación de Integridad (Safety Check)

Antes de ejecutar el comando `write_file` o guardar, hazte estas preguntas:

1.  *"¿El nuevo contenido es drásticamente más corto que el original?"*
    * Si el archivo original tenía 500 líneas y tu propuesta tiene 50, **DETENTE**. Estás a punto de borrar información.
2.  *"¿He mantenido los headers y la estructura de navegación?"*
3.  *"¿Estoy alucinando secciones que no leí?"*

## 4. Ejecución Táctica

1.  **Analizar Código:** Lee el archivo de código modificado (ej. `Chats.tsx` o `meta_service.py`).
2.  **Leer Doc:** Lee el documento correspondiente en `docs/`.
3.  **Redactar:** Crea el párrafo técnico explicando el cambio.
4.  **Fusionar:** Combina `Doc Original` + `Nuevo Párrafo`.
5.  **Guardar:** Escribe el resultado final.

## 5. Caso Especial: Actualizar Skills (`SKILL.md`)
Si actualizas una Skill:
1.  **NUNCA** toques el Frontmatter (YAML) a menos que se pida explícitamente.
2.  Agrega nuevas reglas en la sección pertinente.
3.  Ejecuta la skill **"Skill Synchronizer"** al finalizar para re-indexar.
