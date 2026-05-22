---
name: progressive-disclosure
description:
  Revela información y opciones gradualmente según se necesitan. Use cuando
  simplifique interfaces complejas, diseñe onboarding, o maneje configuraciones
  avanzadas.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Progressive Disclosure (Revelación Progresiva)

## Resumen

Presentar solo la información y opciones necesarias en cada momento, revelando
detalles adicionales bajo demanda. Reduce la complejidad percibida sin eliminar
funcionalidad.

## Origen

- **Autor**: J.M. Keller (educación), aplicado a HCI por varios autores
- **Año**: ~1980s
- **Contexto**: Originado en diseño instruccional

## Fundamento Psicológico

La carga cognitiva aumenta con la cantidad de información visible. Mostrar todo
a la vez abruma y dificulta la toma de decisiones. Al revelar gradualmente, los
usuarios pueden construir comprensión paso a paso.

## Aplicación en Diseño

### Interfaces Complejas

- Opciones avanzadas ocultas por defecto
- "Show more" para detalles adicionales
- Menús expandibles
- Tooltips con información extra

### Formularios

- Campos condicionales que aparecen según contexto
- Wizards multi-paso
- "Opcional" sections colapsadas
- Validación progresiva

### Contenido

- Abstracts con "Read more"
- Cards con preview expandible
- FAQs colapsables
- Nested comments/replies

### Configuraciones

- Básico vs Avanzado
- Defaults sensibles con customización opcional
- "Expert mode" para usuarios avanzados
- Settings agrupados por frecuencia de uso

## Ejemplos

- **Gmail**: "Show trimmed content" en emails largos
- **Amazon**: "See all reviews" para más contenido
- **Slack**: Threads colapsados
- **GitHub**: Diffs colapsados por archivo
- **iOS Settings**: Opciones anidadas en profundidad

## Anti-patterns

- ❌ Ocultar información crítica
- ❌ Demasiados niveles de anidamiento
- ❌ "Show more" sin indicar qué se verá
- ❌ Features principales ocultas
- ❌ Progresión sin poder retroceder

## Métricas

- **Feature Discoverability**: % que encuentra features avanzadas
- **Progressive Engagement**: Usuarios que exploran más
- **Cognitive Load Score**: Evaluación de complejidad
- **Task Completion Rate**: Por nivel de disclosure

## Principios Relacionados

- [[millers-law]] - Limitar información visible
- [[hicks-law]] - Menos opciones, decisiones más rápidas
- [[cognitive-load]] - Manejar carga cognitiva

## Referencias

- Keller, J.M. (1987). "Development and use of the ARCS model"
- Nielsen, J. (2006). "Progressive Disclosure"
- https://www.nngroup.com/articles/progressive-disclosure/
