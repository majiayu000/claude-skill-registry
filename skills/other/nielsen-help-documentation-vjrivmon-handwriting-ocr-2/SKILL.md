---
name: nielsen-help-documentation
description:
  Proporciona documentación accesible y orientada a tareas. Use cuando diseñe
  sistemas de ayuda, onboarding, tooltips, o documentación de usuario.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: heuristics
---

# Ayuda y Documentación

## Resumen

Aunque es mejor si el sistema puede usarse sin documentación, puede ser
necesario proporcionar ayuda y documentación. Esta información debe ser fácil de
buscar, enfocada en la tarea del usuario, listar pasos concretos a seguir, y no
ser demasiado extensa.

## Origen

- **Autor**: Jakob Nielsen
- **Año**: 1994 (refinado 2020)
- **Fuente**: Nielsen Norman Group - "10 Usability Heuristics for User Interface
  Design"

## Fundamento Psicológico

Los usuarios acceden a la ayuda en momentos de frustración o bloqueo
(**help-seeking behavior**). La documentación efectiva debe minimizar la carga
cognitiva adicional y resolver el problema rápidamente. El modelo de
**aprendizaje situado** indica que la ayuda contextual es más efectiva que
manuales genéricos.

## Aplicación en Diseño

### Ayuda Contextual

- Tooltips informativos en elementos complejos
- Hints inline en formularios
- Botones de "?" junto a funciones avanzadas
- Onboarding tours para nuevas features

### Documentación Estructurada

- Búsqueda efectiva en docs
- Categorización por tareas, no por features
- Ejemplos y casos de uso concretos
- Videos y GIFs para procesos complejos

### Accesibilidad de la Ayuda

- Accesible desde cualquier punto (F1, "?")
- No bloquear la tarea actual al buscar ayuda
- Quick start guides para empezar rápido
- FAQs para problemas comunes

### Formato Efectivo

- Pasos numerados y concretos
- Screenshots actualizados
- Texto escaneable (headers, bullets)
- Longitud apropiada (ni muy corto ni muy extenso)

## Ejemplos

- **Notion**: Help overlay contextual con search
- **Figma**: Interactive tutorials integrados
- **Stripe Docs**: Código ejecutable en la documentación
- **Slack**: Tips del día y onboarding progresivo
- **GitHub**: Guides paso a paso con screenshots

## Anti-patterns

- ❌ Manuales PDF de 200 páginas sin índice
- ❌ Ayuda que requiere salir de la aplicación
- ❌ Documentación desactualizada
- ❌ Solo FAQs sin documentación estructurada
- ❌ Chatbots que no resuelven problemas reales

## Métricas

- **Help Seeking Frequency**: Qué tan seguido los usuarios buscan ayuda
- **Help Success Rate**: % que resuelve su problema con docs
- **Time in Documentation**: Tiempo hasta encontrar respuesta
- **Search Success Rate**: % de búsquedas exitosas en docs

## Principios Relacionados

- [[progressive-disclosure]] - Revelar complejidad gradualmente
- [[nielsen-recognition-recall]] - Información visible cuando se necesita
- [[nielsen-match-real-world]] - Lenguaje del usuario

## Referencias

- Nielsen, J. (1994). "Usability Engineering". Morgan Kaufmann
- Lave, J. & Wenger, E. (1991). "Situated Learning". Cambridge University Press
- https://www.nngroup.com/articles/help-and-documentation/
