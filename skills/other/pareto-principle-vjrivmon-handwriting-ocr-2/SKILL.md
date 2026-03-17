---
name: pareto-principle
description:
  El 80% de resultados viene del 20% de causas. Use cuando priorice features,
  diseñe interfaces, o decida dónde invertir esfuerzo de diseño.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Principio de Pareto (Regla 80/20)

## Resumen

Aproximadamente el 80% de los efectos provienen del 20% de las causas. En
diseño: el 80% del uso viene del 20% de las features. Enfoca esfuerzo en lo que
más importa.

## Origen

- **Autor**: Vilfredo Pareto (economía), Joseph Juran (management)
- **Año**: 1896 (Pareto), 1940s (aplicación generalizada)
- **Observación original**: 80% de la tierra en Italia era propiedad del 20% de
  la población

## Aplicaciones en UX/Producto

### Feature Usage

- 80% del tiempo se usa 20% de features
- Priorizar las features más usadas
- No todas las features son iguales
- Simplificar eliminando lo poco usado

### User Segments

- 20% de usuarios generan 80% del revenue
- Focus en usuarios más valiosos
- Diseñar para casos de uso principales
- Power users vs casual users

### Bugs y Errores

- 20% de bugs causan 80% de crashes
- Priorizar bugs de alto impacto
- Fix the vital few
- Monitorear los más críticos

### Desarrollo

- 20% del código genera 80% del valor
- Iterar en lo que importa
- MVP = 20% que da 80% del valor
- Technical debt estratégico

## Aplicación en Diseño

### Priorización de UI

- Features principales prominentes
- Acciones frecuentes accesibles
- Caminos felices optimizados
- Edge cases en opciones avanzadas

### Research

- Encontrar los problemas del 80%
- User journeys más comunes
- Pain points de mayor impacto
- Quick wins de alto valor

### Testing

- Testear flujos principales exhaustivamente
- Smoke tests para el resto
- Monitorear el 20% crítico
- A/B tests en lo de alto impacto

### Métricas

- Definir las pocas métricas que importan
- KPIs vs vanity metrics
- Focus en outcomes principales
- North star metric

## Ejemplos

- **Word processors**: Mayoría usa solo bold, italic, lists
- **Photoshop**: Crop, resize, levels = uso mayoritario
- **Excel**: Pocas funciones dominan el uso
- **Gmail**: Inbox, compose, search = 80% del uso
- **Slack**: DMs y few channels = uso principal

## Anti-patterns

- ❌ Tratar todas las features como iguales
- ❌ Optimizar edge cases antes de main flows
- ❌ Features para 5% de usuarios en prime real estate
- ❌ Equal testing effort para todo
- ❌ Métricas que no reflejan valor real

## Métricas

- **Feature Usage Distribution**: Confirmar la distribución
- **User Segment Analysis**: Valor por segmento
- **Task Frequency Analysis**: Tareas más comunes
- **Impact vs Effort Matrix**: ROI de mejoras

## Principios Relacionados

- [[hicks-law]] - Reducir opciones a las importantes
- [[progressive-disclosure]] - Ocultar el 80% menos usado
- [[kiss-principle]] - Simplicidad en lo principal

## Referencias

- Pareto, V. (1896). "Cours d'économie politique"
- Juran, J.M. (1954). "The Non-Pareto Principle"
- Koch, R. (1998). "The 80/20 Principle"
