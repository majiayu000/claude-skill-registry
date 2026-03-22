---
name: limpiar-duplicados
description: Usar al detectar código duplicado que debe consolidarse en una sola implementación
---

## Cuándo usar esta skill

- Al detectar funciones/métodos duplicados en el código
- Cuando ruff o análisis manual identifique código repetido
- Para consolidar lógica similar en helpers reutilizables

## Contexto necesario antes de empezar

1. Identificar las ubicaciones exactas del código duplicado
2. Verificar que las implementaciones son idénticas o casi idénticas
3. Determinar cuál es la versión "correcta" a mantener
4. Verificar si hay tests que cubran el código

## Pasos

### 1. Identificar duplicados

Buscar patrones comunes:
```bash
# Buscar funciones con mismo nombre
ruff check . --select=F811  # Redefinition of unused name
```

O revisar manualmente archivos grandes como `dashboard.js` o `main.py`.

### 2. Comparar implementaciones

- ¿Son exactamente iguales?
- ¿Hay diferencias menores (typos, mejoras)?
- ¿Cuál es la versión más completa/correcta?

### 3. Eliminar duplicado

**Opción A: Eliminar la segunda definición**
```javascript
// ANTES: Dos definiciones de loadInitialData()
async loadInitialData() { /* primera */ }
// ... código intermedio ...
async loadInitialData() { /* segunda - ELIMINAR */ }

// DESPUÉS: Solo una definición
async loadInitialData() { /* mantener la mejor */ }
```

**Opción B: Extraer a función helper**
```javascript
// ANTES: Lógica repetida en múltiples lugares
async loadWidgetA() {
  const container = document.getElementById('a');
  if (!container) return;
  try { /* fetch y render */ }
  catch (e) { utils.handleError(e, 'A', container); }
}

async loadWidgetB() {
  const container = document.getElementById('b');
  if (!container) return;
  try { /* fetch y render similar */ }
  catch (e) { utils.handleError(e, 'B', container); }
}

// DESPUÉS: Helper reutilizable
async loadWidget(containerId, apiUrl, renderFn) {
  const container = document.getElementById(containerId);
  if (!container) return;
  try {
    const data = await utils.fetchJSON(apiUrl);
    container.innerHTML = renderFn(data);
  } catch (e) {
    utils.handleError(e, containerId, container);
  }
}
```

### 4. Verificar que no se rompe nada

```bash
ruff check .
python -c "from app import app"
# Probar en navegador
```

<patrones_criticos>
SIEMPRE:
- Verificar comportamiento antes y después
- Mantener la versión más completa/correcta
- Ejecutar validaciones después de limpiar
- Hacer commit separado para la limpieza

NUNCA:
- Eliminar código sin verificar que es realmente duplicado
- Asumir que dos funciones con mismo nombre hacen lo mismo
- Limpiar y añadir features en el mismo commit

PREFERENTEMENTE:
- Extraer a helper si el patrón se repite 3+ veces
- Documentar por qué se eligió una versión sobre otra
- Usar `@refactor` como tipo de commit
</patrones_criticos>

## Duplicados conocidos en este proyecto

### `static/js/dashboard.js`
- `loadInitialData()` - líneas 24-47 y 49-72 (DUPLICADO)
- `renderDocumentsTree()` - líneas 328-355 y 383-410 (DUPLICADO)
- `renderDocumentNode()` - líneas 357-381 y 412-436 (DUPLICADO)

### Cómo arreglarlos
1. Eliminar la segunda definición de cada función
2. Verificar que el dashboard funciona
3. Commit: `refactor(js): eliminar funciones duplicadas en dashboard.js`

## Checklist de validación

- [ ] Duplicados identificados correctamente
- [ ] Versión correcta mantenida
- [ ] Segunda definición eliminada
- [ ] `ruff check .` pasa
- [ ] App funciona en navegador
- [ ] Commit con tipo `refactor`
