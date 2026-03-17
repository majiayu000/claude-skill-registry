---
name: least-astonishment
description:
  El sistema debe comportarse como el usuario espera. Use cuando diseñe
  interacciones, tome decisiones sobre comportamientos, o evalúe sorpresas en la
  UX.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Principio de Mínima Sorpresa

## Resumen

Un sistema debe comportarse de manera que minimice la sorpresa del usuario. Si
una función necesaria es inherentemente sorprendente, puede ser necesario
rediseñar.

## Origen

- **Contexto**: Diseño de lenguajes de programación y sistemas
- **Popularizado**: IBM Systems Journal, comunidad Unix
- **Año**: ~1970s-1980s

## Fundamento

Las sorpresas son costosas:

- Causan errores y confusión
- Erosionan confianza
- Aumentan carga cognitiva
- Generan frustración
- Requieren soporte

## Expectativas del Usuario

### Formadas por:

- Experiencias previas con el sistema
- Convenciones de plataforma
- Patrones de industria
- Conocimiento del mundo real
- Promesas del producto

### Violaciones típicas:

- Comportamiento inesperado de controles
- Side effects no comunicados
- Resultados diferentes a los anticipados
- Cambios sin aviso

## Aplicación en Diseño

### Interacciones

- Botón "Guardar" debe guardar, no preguntar
- "Cancelar" debe cancelar sin efectos
- Back debe volver, no ir a otro lugar
- Links deben llevar a donde dicen

### Comportamientos

- Acciones consistentes en toda la app
- Resultados proporcionales a acciones
- Sin side effects inesperados
- Cambios de estado claros

### Comunicación

- Nombrar features por lo que hacen
- Mensajes que coinciden con acciones
- Errores que explican qué pasó
- Confirmaciones que confirman lo esperado

### Datos

- Cambios guardados cuando se espera
- Datos mostrados actualizados
- Ordenamientos predecibles
- Filtros que funcionan como se nombran

## Ejemplos

- **Gmail Undo Send**: Comportamiento inesperado pero comunicado
- **iOS Back Gesture**: Siempre vuelve al contexto anterior
- **Browser Refresh**: Recarga la página actual
- **Ctrl+S**: Siempre guarda
- **ESC**: Siempre cierra/cancela

## Anti-patterns

- ❌ "Close" que guarda automáticamente sin avisar
- ❌ Links que abren modales en lugar de navegar
- ❌ Ordenamiento que cambia sin input
- ❌ Acciones con side effects ocultos
- ❌ Back que pierde cambios sin warning

## Métricas

- **Expectation Match Score**: Comportamiento vs expectativa
- **Surprise Event Rate**: Acciones con resultados inesperados
- **User Error Rate**: Errores por comportamiento sorprendente
- **Trust Score**: Confianza en el sistema

## Principios Relacionados

- [[jakobs-law]] - Expectativas de otros sitios
- [[nielsen-consistency]] - Comportamiento consistente
- [[feedback-principle]] - Comunicar qué está pasando

## Referencias

- Saltzer, J.H. & Kaashoek, M.F. (2009). "Principles of Computer System Design"
- Raymond, E.S. (2003). "The Art of Unix Programming"
- https://www.nngroup.com/articles/principle-of-least-surprise/
