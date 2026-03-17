---
name: nielsen-error-recovery
description:
  Diseña mensajes de error claros que ayuden a los usuarios a recuperarse. Use
  cuando implemente manejo de errores, validaciones, o estados de fallo en la
  interfaz.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: heuristics
---

# Ayuda a los Usuarios a Reconocer, Diagnosticar y Recuperarse de Errores

## Resumen

Los mensajes de error deben expresarse en lenguaje claro (sin códigos), indicar
precisamente el problema y sugerir constructivamente una solución.

## Origen

- **Autor**: Jakob Nielsen
- **Año**: 1994 (refinado 2020)
- **Fuente**: Nielsen Norman Group - "10 Usability Heuristics for User Interface
  Design"

## Fundamento Psicológico

Los errores causan frustración y pueden dañar la confianza del usuario en el
sistema. Mensajes claros y accionables transforman una experiencia negativa en
una oportunidad de aprendizaje. El **modelo de procesamiento de errores** de
Reason sugiere que la recuperación requiere: detección, diagnóstico y
corrección.

## Aplicación en Diseño

### Lenguaje Humano

- Sin códigos técnicos: "Error 500" → "Algo salió mal"
- Tono empático, no culpabilizador
- Vocabulario del usuario, no del sistema
- Brevedad sin perder claridad

### Indicación Precisa

- Señalar exactamente qué campo tiene el error
- Highlight visual del elemento problemático
- Scroll automático hacia el error
- Íconos distintivos (⚠️, ❌)

### Soluciones Constructivas

- Sugerir cómo corregir el problema
- Ofrecer acciones alternativas
- Links a recursos de ayuda
- Botones de retry cuando aplique

### Prevención de Pérdida de Datos

- Guardar borrador automáticamente
- Mantener inputs válidos al corregir errores
- No limpiar formularios completos por un error
- Permitir volver atrás y editar

## Ejemplos

- **GitHub**: "File not found. Check if the file exists or if you have access"
- **Stripe**: Errores de tarjeta específicos con sugerencias
- **Slack**: "Can't reach Slack. Check your connection" con botón Retry
- **Twitter**: Guarda borradores cuando falla el envío
- **Google Forms**: Resalta campos específicos con error

## Anti-patterns

- ❌ "Error occurred" sin más información
- ❌ Códigos hexadecimales o stack traces al usuario
- ❌ Mensajes que culpan al usuario
- ❌ Errores que desaparecen sin poder leerlos
- ❌ Formularios que se limpian al fallar

## Métricas

- **Error Recovery Rate**: % usuarios que se recuperan exitosamente
- **Time to Recovery**: Tiempo desde error hasta completar tarea
- **Repeat Error Rate**: Mismo error cometido múltiples veces
- **Abandonment After Error**: % que abandona tras un error

## Principios Relacionados

- [[nielsen-error-prevention]] - Mejor prevenir que curar
- [[nielsen-visibility]] - Hacer visible el estado de error
- [[postels-law]] - Aceptar variaciones, informar problemas

## Referencias

- Nielsen, J. (1994). "Usability Engineering". Morgan Kaufmann
- Reason, J. (1990). "Human Error". Cambridge University Press
- https://www.nngroup.com/articles/error-message-guidelines/
