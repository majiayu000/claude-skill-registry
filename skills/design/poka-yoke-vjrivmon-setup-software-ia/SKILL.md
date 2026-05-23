---
name: poka-yoke
description:
  Diseño a prueba de errores que hace imposible el uso incorrecto. Use cuando
  diseñe flujos críticos, formularios, o sistemas donde los errores tienen
  consecuencias.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Poka-Yoke (A Prueba de Errores)

## Resumen

Diseñar sistemas de manera que sea imposible o muy difícil cometer errores.
Prevenir errores por diseño, no por instrucciones o entrenamiento.

## Origen

- **Autor**: Shigeo Shingo (Toyota Production System)
- **Año**: 1960s
- **Contexto**: Manufactura lean
- **Significado**: "Evitar errores inadvertidos" en japonés

## Tipos de Poka-Yoke

### Prevention (Prevención)

- Hace imposible el error
- USB-C que entra de cualquier lado
- Forms que no aceptan formato inválido
- Botones disabled hasta que sea válido

### Detection (Detección)

- Alerta antes de que el error cause daño
- Spell check mientras escribes
- "¿Olvidaste el adjunto?"
- Validación antes de submit

### Facilitation (Facilitación)

- Hace más fácil lo correcto que lo incorrecto
- Defaults sensibles
- Autocompletado
- Sugerencias contextuales

## Aplicación en Diseño

### Formularios

- Input masks para formatos específicos
- Dropdowns en lugar de texto libre
- Validación en tiempo real
- Required fields claramente marcados

### Acciones Destructivas

- Confirmación con typing del nombre
- Delays antes de ejecutar
- Undo disponible
- Soft deletes antes de permanent

### Datos

- Formato automático (teléfonos, tarjetas)
- Límites de caracteres
- Validación de checksums
- Detección de duplicados

### Flujos

- Steps que no se pueden saltar
- Prerrequisitos enforced
- State machine que previene estados inválidos
- Guards en navegación

## Ejemplos

- **GitHub**: "Type repository name to confirm delete"
- **Gmail**: "You mentioned attachment but didn't attach"
- **ATMs**: Card returns before cash
- **Microwave**: Door switch prevents operation when open
- **Stripe**: Luhn validation en tiempo real

## Anti-patterns

- ❌ Depender de instrucciones para prevenir errores
- ❌ Warnings que se pueden ignorar
- ❌ Validación solo al final del proceso
- ❌ Errores que solo se detectan después
- ❌ Poka-yoke tan restrictivo que frustra

## Métricas

- **Error Prevention Rate**: Errores evitados
- **Error Recovery Time**: Tiempo para corregir
- **Support Tickets**: Por errores de usuario
- **Data Quality Score**: Datos válidos ingresados

## Principios Relacionados

- [[constraints-principle]] - Restringir acciones inválidas
- [[nielsen-error-prevention]] - Prevenir antes de curar
- [[postels-law]] - Flexibilidad con validación

## Referencias

- Shingo, S. (1986). "Zero Quality Control"
- Norman, D. (2013). "The Design of Everyday Things"
- https://www.nngroup.com/articles/slips/
