---
name: crear-widget
description: Usar al crear un nuevo widget en el dashboard que muestre datos de una API
---

## Cuándo usar esta skill

- Al añadir un nuevo widget/card al dashboard
- Cuando se necesite mostrar datos de un endpoint en el frontend
- Para crear componentes visuales que consuman `/api/[recurso]`

## Contexto necesario antes de empezar

1. Leer `static/js/dashboard.js` para ver patrones existentes
2. Verificar que el endpoint API existe en `blueprints/main.py`
3. Identificar el ID del contenedor HTML en `templates/dashboard.html`

## Pasos

### 1. Añadir contenedor HTML en `templates/dashboard.html`

```html
<!-- N) NUEVO WIDGET -->
<div class="card span-3 min-h-200 animate-fade-in">
    <div class="card__header">
        <h3 class="card__title">🆕 Nuevo Widget</h3>
    </div>
    <div id="nuevoWidgetStats" class="card__content">
        <!-- Skeleton mientras carga -->
        <div class="skeleton"></div>
    </div>
</div>
```

### 2. Añadir método en `static/js/dashboard.js`

```javascript
// ========== NUEVO WIDGET ==========
async loadNuevoWidget() {
  const container = document.getElementById('nuevoWidgetStats');
  if (!container) return;

  try {
    const data = await utils.fetchJSON('/api/nuevo', { timeout: 15000 });
    
    if (!data || data.error) {
      throw new Error(data?.error || 'Datos no disponibles');
    }
    
    container.innerHTML = `
      <div class="metric">
        <span class="metric__value">${data.valor}</span>
        <span class="metric__label">${data.label}</span>
      </div>
    `;
    
    console.log('✅ Nuevo widget cargado:', data);
  } catch (error) {
    utils.handleError(error, 'Nuevo Widget API', container);
  }
}
```

### 3. Registrar en `loadInitialData()`

```javascript
await Promise.allSettled([
  this.loadWeatherData(),
  this.loadMealieStats(),
  this.loadPiHoleStats(),
  this.loadEnergyData(),
  this.loadSettleUpData(),
  this.loadNuevoWidget()  // ← Añadir aquí
]);
```

### 4. (Opcional) Añadir refresh periódico en `setupEventListeners()`

```javascript
this.addInterval(() => {
  this.loadNuevoWidget();
}, 5 * 60 * 1000); // Cada 5 minutos
```

<patrones_criticos>
SIEMPRE:
- Verificar que el contenedor existe antes de operar: `if (!container) return;`
- Usar `utils.fetchJSON()` con timeout
- Manejar errores con `utils.handleError(error, 'Context', container)`
- Loguear éxito con `console.log('✅ ...')`

NUNCA:
- Usar `fetch()` directamente sin timeout
- Ignorar el caso de error o datos vacíos
- Hardcodear datos en el frontend

PREFERENTEMENTE:
- Mostrar skeleton/placeholder mientras carga
- Usar clases CSS existentes (metric, card, etc.)
- Añadir emoji descriptivo en el título
</patrones_criticos>

## Ejemplos reales del proyecto

- `loadPiHoleStats()` - Widget con métricas numéricas
- `loadWeatherData()` - Widget complejo con forecast
- `loadMealieStats()` - Widget con lista de items
- `loadSettleUpData()` - Widget con estado y valores

## Checklist de validación

- [ ] Contenedor HTML tiene ID único
- [ ] Método usa `utils.fetchJSON()` con timeout
- [ ] Errores manejados con `utils.handleError()`
- [ ] Registrado en `loadInitialData()`
- [ ] Widget se renderiza correctamente en navegador
