---
name: nielsen-error-prevention
description:
  Diseña interfaces que previenen errores antes de que ocurran. Use cuando
  diseñe formularios, acciones destructivas, o flujos donde los usuarios pueden
  cometer errores costosos.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: heuristics
---

# Prevención de Errores

## Resumen

Mejor que buenos mensajes de error es un diseño cuidadoso que prevenga que los
problemas ocurran en primer lugar. Eliminar condiciones propensas a errores o
verificar y presentar opciones de confirmación antes de que los usuarios se
comprometan con acciones.

## Origen

- **Autor**: Jakob Nielsen
- **Año**: 1994 (refinado 2020)
- **Fuente**: Nielsen Norman Group - "10 Usability Heuristics for User Interface
  Design"

## Fundamento Psicológico

Los humanos cometen dos tipos de errores: **slips** (errores de atención) y
**mistakes** (errores de intención). Los slips ocurren cuando la acción
ejecutada difiere de la intencionada; los mistakes cuando el plan mental es
incorrecto. El diseño preventivo aborda ambos tipos anticipando fallos humanos
predecibles.

## Aplicación en Diseño

### Prevención de Slips

- Auto-completado en campos de búsqueda
- Sugerencias en tiempo real mientras escribe
- Defaults inteligentes pre-seleccionados
- Separación visual de acciones destructivas

### Prevención de Mistakes

- Wizards que guían paso a paso
- Validación inline antes de submit
- Preview de cambios antes de confirmar
- Restricciones que hacen imposible opciones inválidas

### Validación de Formularios

- Validación en tiempo real (no solo al submit)
- Formatos aceptados mostrados como placeholder
- Mensajes de ayuda contextuales
- Indicadores de requisitos (\*, opcional)

### Confirmaciones Inteligentes

- Diálogos de confirmación para acciones irreversibles
- Repetir información crítica (email de confirmación)
- Comparar antes/después en cambios masivos
- Tiempo de espera antes de ejecutar (countdown)

## Ejemplos

- **Google Search**: "Quizás quisiste decir..." para errores ortográficos
- **GitHub**: Branch protection rules previenen push a main
- **Stripe**: Validación de tarjeta con Luhn algorithm en tiempo real
- **Slack**: Advertencia al mencionar @channel en canales grandes
- **Gmail**: Detecta "adjunto" en texto sin archivos adjuntos

## Anti-patterns

- ❌ Validación solo al enviar formulario
- ❌ Campos de texto libre para datos estructurados (fechas, teléfonos)
- ❌ Acciones destructivas junto a acciones frecuentes
- ❌ Permitir guardar datos incompletos/inválidos
- ❌ Mensajes de error genéricos sin indicar qué corregir

## Métricas

- **Form Abandonment Rate**: Abandonos por frustración con errores
- **Error Rate per Field**: Errores por campo de formulario
- **Time to Complete Form**: Reducido con validación inline
- **Prevention vs Recovery Ratio**: Errores prevenidos vs corregidos

## Principios Relacionados

- [[poka-yoke]] - Diseño a prueba de errores
- [[constraints-principle]] - Restricciones que previenen errores
- [[postels-law]] - Ser liberal en lo que aceptas

## Referencias

- Nielsen, J. (1994). "Usability Engineering". Morgan Kaufmann
- Norman, D. (2013). "The Design of Everyday Things". Basic Books
- https://www.nngroup.com/articles/slips/
