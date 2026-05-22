---
name: kiss-principle
description:
  Keep It Simple, Stupid - evita complejidad innecesaria. Use cuando diseñe
  interfaces, arquitectura, o tome decisiones que afecten la simplicidad del
  sistema.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Principio KISS

## Resumen

"Keep It Simple, Stupid" - Los sistemas funcionan mejor si se mantienen simples
en lugar de complicados. La simplicidad debe ser un objetivo clave del diseño.

## Origen

- **Autor**: Kelly Johnson (Lockheed Skunk Works)
- **Año**: 1960s
- **Contexto**: Diseño de aviones militares
- **Criterio original**: Un avión debía poder ser reparado por un mecánico
  promedio en condiciones de combate con herramientas limitadas

## Diferencia con Occam's Razor

- **Occam**: Elegir la explicación más simple entre alternativas
- **KISS**: Diseñar activamente para simplicidad desde el inicio

## Aplicación en Diseño

### Interfaces

- Un propósito claro por pantalla
- Flujos lineales vs ramificados
- Opciones mínimas para tareas comunes
- Complejidad oculta, no eliminada

### Interacciones

- Clicks mínimos para tareas frecuentes
- Gestos simples e intuitivos
- Feedback claro e inmediato
- Estados predecibles

### Información

- Jerarquía clara de contenido
- Texto conciso y escaneable
- Datos relevantes, no todos los datos
- Visualizaciones simples

### Código

- Funciones pequeñas con propósito único
- Naming claro y descriptivo
- Evitar abstracción prematura
- Documentación donde el código no es claro

## Ejemplos

- **Craiglist**: UI básica, altamente funcional
- **Google Search**: Una caja, un botón
- **Dropbox**: "Put files here, access anywhere"
- **WhatsApp**: Mensajería sin features excesivas
- **Stripe Checkout**: Pago en una pantalla

## Anti-patterns

- ❌ Feature creep sin control
- ❌ Settings para todo
- ❌ UI que requiere manual
- ❌ Arquitectura sobre-engineered
- ❌ "Por si lo necesitamos después"

## KISS en Práctica

### Preguntas para evaluar

- ¿Puede un nuevo usuario entender esto?
- ¿Qué puedo quitar sin perder valor?
- ¿Por qué esto necesita ser complicado?
- ¿Hay una forma más simple de lograr lo mismo?

### Balance

- Simple ≠ simplista
- Potencia cuando se necesita
- Complejidad justificada
- Progressive disclosure para avanzados

## Métricas

- **Time to First Value**: Rapidez para lograr objetivo
- **Feature Adoption Rate**: Uso real de features
- **Support Ticket Rate**: Problemas por confusión
- **New User Success Rate**: Éxito sin ayuda

## Principios Relacionados

- [[occams-razor]] - Preferir lo simple
- [[teslers-law]] - Complejidad irreducible
- [[progressive-disclosure]] - Ocultar complejidad

## Referencias

- Johnson, K. (1960s). Lockheed Martin Skunk Works
- Maeda, J. (2006). "The Laws of Simplicity"
- https://www.interaction-design.org/literature/article/kiss-keep-it-simple-stupid
