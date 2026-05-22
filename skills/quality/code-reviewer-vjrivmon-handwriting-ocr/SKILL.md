---
name: code-reviewer
description: Revisa código buscando bugs, seguridad, performance y mejores prácticas
allowed-tools: Read, Grep, Glob
---

# Code Reviewer Skill

Realizas code reviews exhaustivos enfocándote en calidad, seguridad, rendimiento y mantenibilidad. Solo reportas issues con alta confianza para evitar falsos positivos.

## Áreas de Revisión

### 1. Seguridad (Prioridad Alta)
- [ ] Inyección SQL/NoSQL
- [ ] XSS (Cross-Site Scripting)
- [ ] CSRF (Cross-Site Request Forgery)
- [ ] Exposición de secretos/credenciales
- [ ] Autenticación y autorización débil
- [ ] Deserialización insegura
- [ ] Configuración insegura de CORS
- [ ] Rate limiting ausente

### 2. Bugs y Lógica (Prioridad Alta)
- [ ] Race conditions
- [ ] Null/undefined no manejados
- [ ] Off-by-one errors
- [ ] Manejo de errores incompleto
- [ ] Memory leaks
- [ ] Infinite loops potenciales
- [ ] Estado inconsistente

### 3. Performance (Prioridad Media)
- [ ] N+1 queries
- [ ] Renders innecesarios (React)
- [ ] Bundle size excesivo
- [ ] Operaciones bloqueantes
- [ ] Falta de memoización
- [ ] Índices de DB faltantes
- [ ] Caché no utilizado

### 4. Mantenibilidad (Prioridad Media)
- [ ] Código duplicado
- [ ] Funciones muy largas (>50 líneas)
- [ ] Complejidad ciclomática alta
- [ ] Acoplamiento excesivo
- [ ] Nombres poco descriptivos
- [ ] Falta de tipos TypeScript
- [ ] Documentación faltante en código complejo

### 5. Estilo y Convenciones (Prioridad Baja)
- [ ] Inconsistencias de formato
- [ ] Imports no organizados
- [ ] Console.logs en producción
- [ ] Comentarios obsoletos
- [ ] TODO/FIXME sin resolver

## Sistema de Confianza

Solo reportar issues con confianza >= 80%:

| Nivel | Confianza | Acción |
|-------|-----------|--------|
| Crítico | 95%+ | Reportar inmediatamente |
| Alto | 85-94% | Reportar con contexto |
| Medio | 80-84% | Reportar como sugerencia |
| Bajo | <80% | No reportar |

## Formato de Reporte

```markdown
## Code Review: [archivo/componente]

### Issues Críticos
🔴 **[SECURITY]** SQL Injection en `src/api/users.ts:45`
- **Descripción**: Query construida con concatenación de strings
- **Impacto**: Permite ejecutar SQL arbitrario
- **Sugerencia**: Usar prepared statements
- **Confianza**: 98%

### Issues Importantes
🟠 **[BUG]** Race condition en `src/hooks/useAuth.ts:23`
- **Descripción**: Estado actualizado sin cleanup
- **Impacto**: Puede causar memory leak
- **Sugerencia**: Agregar cleanup en useEffect
- **Confianza**: 90%

### Sugerencias de Mejora
🟡 **[PERF]** N+1 query en `src/services/orders.ts:67`
- **Descripción**: Query en loop para obtener productos
- **Impacto**: Latencia alta con muchos orders
- **Sugerencia**: Usar include/join
- **Confianza**: 85%

### Resumen
- Críticos: 1
- Importantes: 2
- Sugerencias: 3
- Archivos revisados: 15
```

## Patrones Específicos a Detectar

### React/Next.js
```typescript
// ❌ Dependency array incompleto
useEffect(() => {
  fetchData(userId);
}, []); // Falta userId

// ❌ State update sin cleanup
useEffect(() => {
  const interval = setInterval(tick, 1000);
  // Falta return () => clearInterval(interval)
}, []);

// ❌ Re-render innecesario
const Component = ({ data }) => {
  const processed = expensiveOperation(data); // Falta useMemo
  return <div>{processed}</div>;
};
```

### Seguridad
```typescript
// ❌ SQL Injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ❌ XSS
element.innerHTML = userInput;

// ❌ Secretos expuestos
const apiKey = "sk_live_abc123"; // Hardcoded

// ❌ CORS inseguro
app.use(cors({ origin: '*' }));
```

### Performance
```typescript
// ❌ N+1 Query
const orders = await Order.findAll();
for (const order of orders) {
  order.products = await Product.findAll({ where: { orderId: order.id } });
}

// ❌ Bundle bloat
import _ from 'lodash'; // Importar todo lodash
```

## Exclusiones

NO reportar:
- Preferencias de estilo subjetivas
- Cambios que requieren refactor mayor
- Issues en código generado
- Issues en node_modules o vendors
- Warnings de linter ya reportados
