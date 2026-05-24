---
name: teslers-law
description:
  Toda aplicación tiene complejidad irreducible que debe ir al sistema o al
  usuario. Use cuando simplifique flujos, automatice tareas, o decida dónde
  poner la complejidad.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: cognitive-laws
---

# Ley de Tesler (Conservación de la Complejidad)

## Resumen

Para cualquier sistema existe cierta cantidad de complejidad que no puede ser
reducida. Esta complejidad inherente debe ser manejada por el sistema o
transferida al usuario.

## Origen

- **Autor**: Larry Tesler
- **Año**: ~1984
- **Fuente**: Desarrollada durante su trabajo en Xerox PARC y Apple

## Fundamento Psicológico

La complejidad no desaparece, solo se mueve. Cuando el sistema absorbe
complejidad, el usuario tiene una experiencia más simple. Cuando el sistema es
"simple" internamente, la complejidad se transfiere al usuario. El objetivo es
encontrar el equilibrio óptimo donde el sistema maneja la complejidad que puede
automatizar.

## Aplicación en Diseño

### Sistema Absorbe Complejidad

- **Autocompletado**: Sistema predice, usuario solo confirma
- **Defaults inteligentes**: Valores pre-seleccionados basados en contexto
- **Validación automática**: Sistema verifica, no el usuario
- **Formateo automático**: Números de teléfono, tarjetas de crédito

### Usuario Asume Complejidad

- **Formularios detallados**: Cuando se necesita información específica
- **Configuraciones avanzadas**: Para usuarios que quieren control
- **Herramientas profesionales**: Complejidad justificada por poder

### Balance Óptimo

- Automatizar lo que se puede inferir
- Preguntar solo lo necesario
- Ofrecer opciones avanzadas sin forzarlas
- Progressive disclosure de complejidad

### Trade-offs

- Más automatización = menos flexibilidad
- Simplicidad extrema puede frustrar a expertos
- Algunas decisiones solo el usuario puede tomar

## Ejemplos

- **GPS Navigation**: Sistema calcula ruta, usuario solo elige destino
- **Gmail Smart Compose**: Predice texto, usuario acepta o ignora
- **Stripe**: Complejidad de pagos oculta tras API simple
- **Calendly**: Elimina ping-pong de emails para agendar
- **Zoom**: Un click para unirse vs configurar VoIP manualmente

## Anti-patterns

- ❌ Pedir información que el sistema podría inferir
- ❌ Formularios con campos que podrían auto-completarse
- ❌ Configuraciones obligatorias que podrían tener defaults
- ❌ Procesos manuales que podrían automatizarse
- ❌ Sobre-simplificación que elimina capacidades necesarias

## Métricas

- **User Effort Score**: Esfuerzo requerido del usuario
- **Automation Rate**: % de tareas automatizadas
- **Configuration Time**: Tiempo en setup inicial
- **Task Completion Rate**: Con automatización vs sin ella

## Principios Relacionados

- [[postels-law]] - Flexibilidad en inputs, rigor en outputs
- [[progressive-disclosure]] - Ocultar complejidad opcional
- [[poka-yoke]] - Diseño que previene errores

## Referencias

- Tesler, L. "The Law of Conservation of Complexity"
- Norman, D. (2013). "The Design of Everyday Things"
- https://lawsofux.com/teslers-law/
