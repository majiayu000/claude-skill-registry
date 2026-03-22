---
name: refactor
description: Usar al refactorizar código existente sin cambiar funcionalidad
---

## Cuándo usar esta skill

- Al mejorar estructura de código sin cambiar comportamiento
- Cuando se detecten code smells o duplicación
- Para aplicar patrones más limpios

## Contexto necesario antes de empezar

1. Leer el código a refactorizar completamente
2. Identificar tests existentes (si los hay)
3. Entender el comportamiento actual
4. Definir qué se va a mejorar y qué NO se va a tocar

## Pasos

### 1. Análisis
- Identificar el problema (duplicación, complejidad, naming, etc.)
- Verificar si hay tests que cubran el código
- Documentar comportamiento actual

### 2. Plan de refactor
- Listar cambios específicos a realizar
- Definir orden de cambios (de menor a mayor riesgo)
- Identificar puntos de verificación

### 3. Ejecutar refactor
- Hacer cambios incrementales
- Verificar después de cada cambio significativo
- Mantener commits pequeños y atómicos

### 4. Validación
```bash
ruff check .
ruff format --check .
python -c "from app import app"
pytest tests/ -v  # si hay tests
```

### 5. Test manual
- Verificar que el comportamiento no ha cambiado
- Probar casos edge si aplica

<patrones_criticos>
SIEMPRE:
- Leer tests antes de tocar código
- Verificar comportamiento antes y después
- Commits pequeños y descriptivos
- Mantener la API pública igual

NUNCA:
- Cambiar comportamiento durante refactor
- Eliminar código "muerto" sin confirmar
- Refactorizar y añadir features al mismo tiempo
- Ignorar tests que fallen

PREFERENTEMENTE:
- Extraer funciones/métodos pequeños
- Mejorar nombres para claridad
- Reducir anidación de código
</patrones_criticos>

## Refactors comunes en este proyecto

1. **Ordenar imports** → `ruff check --fix .`
2. **Extraer lógica a cliente** → Mover de `main.py` a `*_client.py`
3. **Eliminar duplicación** → Crear función helper
4. **Mejorar error handling** → Añadir logging consistente

## Checklist de validación

- [ ] Comportamiento idéntico al original
- [ ] `ruff check .` pasa
- [ ] Tests pasan (si existen)
- [ ] La app arranca correctamente
- [ ] No se han tocado archivos fuera del scope
