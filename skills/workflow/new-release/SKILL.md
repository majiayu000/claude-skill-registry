---
name: new-release
description: Crear nueva release de un plugin del marketplace actualizando versiones. Usar cuando se modifique un plugin y necesite nueva version.
---

# New Release

## Overview

Actualiza la version de uno o mas plugins del marketplace tras realizar cambios.

## When to Use

- Tras modificar codigo de un plugin
- Cuando el usuario pida "nueva release" o "actualizar version"
- Despues de agregar features o fix bugs en plugins

## Instructions

1. **Identificar plugin(s) modificados**
   - Revisar cambios recientes
   - Confirmar con usuario si hay duda

2. **Actualizar version en ambos archivos:**
   - `.claude-plugin/marketplace.json` - entrada del plugin en array `plugins`
   - `plugins/{nombre-plugin}/.claude-plugin/plugin.json` - version del plugin

3. **Incrementar version segun cambio:**
   - PATCH (0.0.X): fixes, ajustes menores
   - MINOR (0.X.0): nuevas features
   - MAJOR (X.0.0): breaking changes

4. **Verificar consistencia**
   - Ambos archivos deben tener la misma version

## Archivos a Modificar

Ver `references/file-locations.md` para rutas exactas.

## Examples

```
User: "haz release del plugin custom-hooks"
Claude:
1. Lee marketplace.json y plugin.json
2. Incrementa version (ej: 1.0.0 -> 1.0.1)
3. Edita ambos archivos
4. Confirma cambios
```

```
User: "nueva release de fabric-helper y superclaude"
Claude:
1. Actualiza ambos plugins
2. Incrementa versiones en los 4 archivos correspondientes
```
