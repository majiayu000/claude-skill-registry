---
name: postels-law
description:
  Sé conservador en lo que envías, liberal en lo que aceptas. Use cuando diseñe
  validaciones de formularios, APIs, o maneje inputs de usuario.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: cognitive-laws
---

# Ley de Postel (Principio de Robustez)

## Resumen

Sé conservador en lo que haces, sé liberal en lo que aceptas de otros. En
diseño: acepta inputs variados del usuario, pero produce outputs consistentes y
predecibles.

## Origen

- **Autor**: Jon Postel
- **Año**: 1980
- **Fuente**: RFC 761 - Transmission Control Protocol (TCP)

## Fundamento Psicológico

Los usuarios cometen errores y tienen diferentes formas de expresar la misma
intención. Un sistema robusto interpreta la intención del usuario en lugar de
rechazar variaciones válidas. Esto reduce frustración y aumenta la tasa de
éxito.

## Aplicación en Diseño

### Inputs Flexibles

- Aceptar múltiples formatos de fecha (01/15/2024, 15-01-2024, Jan 15)
- Normalizar espacios, guiones, paréntesis en teléfonos
- Ignorar mayúsculas/minúsculas cuando no importa
- Permitir pegado de texto con formato

### Validación Inteligente

- Corregir errores obvios automáticamente
- Sugerir correcciones antes de rechazar
- Validar intención, no formato exacto
- Mensajes de error que guían, no solo rechazan

### Outputs Consistentes

- Formato estandarizado independiente del input
- Respuestas predecibles del sistema
- Documentación clara de lo que el sistema hace
- Datos almacenados en formato canónico

### Tolerancia a Errores

- Auto-corrección ortográfica
- Búsqueda fuzzy que encuentra aproximaciones
- Parseo tolerante de datos copiados
- Recuperación graceful de inputs inesperados

## Ejemplos

- **Google Search**: Corrige ortografía automáticamente
- **Stripe**: Acepta números de tarjeta con o sin espacios/guiones
- **GitHub**: URLs case-insensitive para repos
- **Slack**: Detecta y formatea URLs, emails, código
- **Excel**: Interpreta múltiples formatos de fecha

## Anti-patterns

- ❌ Rechazar email por capitalización
- ❌ Exigir formato exacto de teléfono (XXX-XXX-XXXX)
- ❌ Fallar por espacios extra en inputs
- ❌ Case-sensitive en búsquedas de usuario
- ❌ Rechazar datos válidos por formato inesperado

## Métricas

- **Input Acceptance Rate**: % de inputs aceptados vs rechazados
- **Auto-correction Accuracy**: Correcciones correctas vs incorrectas
- **Form Completion Rate**: Mejora con validación flexible
- **Support Tickets**: Reducción por mejor manejo de inputs

## Principios Relacionados

- [[nielsen-error-prevention]] - Prevenir errores por formato
- [[teslers-law]] - Sistema absorbe complejidad de normalización
- [[poka-yoke]] - Hacer difícil el error

## Referencias

- Postel, J. (1980). RFC 761 - Transmission Control Protocol
- RFC 1122 - Requirements for Internet Hosts
- https://lawsofux.com/postels-law/
