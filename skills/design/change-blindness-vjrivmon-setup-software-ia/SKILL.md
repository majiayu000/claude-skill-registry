---
name: change-blindness
description:
  Los usuarios no notan cambios que ocurren fuera de su foco de atención. Use
  cuando diseñe actualizaciones de estado, notificaciones, o cambios dinámicos
  en la UI.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: perception
---

# Ceguera al Cambio

## Resumen

Las personas frecuentemente no notan cambios significativos en su entorno visual
cuando el cambio ocurre durante una interrupción visual o fuera de su foco de
atención.

## Origen

- **Autores**: Ronald Rensink, Kevin O'Regan, James Clark
- **Año**: 1997
- **Estudio**: "To See or Not to See"
- **Experimento**: "Flicker paradigm" y "mudsplash" experiments

## Fundamento Psicológico

### Atención Focalizada

- Solo procesamos una porción del campo visual
- La atención es necesaria para percibir cambios
- Visión periférica tiene baja resolución
- Cambios gradual son especialmente invisibles

### Factores de Invisibilidad

- Cambio durante saccade (movimiento ocular)
- Cambio durante parpadeo
- Cambio durante interrupción visual
- Cambio fuera del foco de atención
- Cambio gradual (boiling frog)

## Aplicación en Diseño

### Llamar Atención al Cambio

- Animaciones de transición
- Colores temporales de highlight
- Movimiento hacia el cambio
- Sonidos o haptics

### Estados Dinámicos

- Indicadores de "nuevo" o "actualizado"
- Badges con contadores
- Timestamps visibles
- Comparación antes/después

### Actualizaciones en Tiempo Real

- Notificaciones explícitas
- Toasts para cambios importantes
- Scroll to change
- Flash/pulse en elemento cambiado

### Evitar Pérdida de Cambios

- No cambiar durante scroll del usuario
- No actualizar mientras usuario lee
- Dar control sobre actualizaciones
- Mantener contexto tras cambios

## Ejemplos

- **Facebook**: Badge rojo para notificaciones
- **Slack**: Indicador de "nuevos mensajes abajo"
- **Gmail**: Flash amarillo en mensajes nuevos
- **Google Docs**: Cursor con nombre de colaborador
- **VS Code**: Highlight de líneas modificadas

## Anti-patterns

- ❌ Cambiar contenido sin notificar
- ❌ Actualizar datos mientras usuario los lee
- ❌ Remover elementos sin animación
- ❌ Agregar contenido lejos del foco
- ❌ Cambios que modifican layout sin aviso

## Métricas

- **Change Detection Rate**: % de cambios notados
- **Time to Notice**: Tiempo para detectar cambio
- **Missed Update Rate**: Cambios ignorados
- **User Confusion Reports**: Soporte por "desaparecido"

## Principios Relacionados

- [[inattentional-blindness]] - No ver lo inesperado
- [[feedback-principle]] - Comunicar cambios de estado
- [[nielsen-visibility]] - Estado visible del sistema

## Referencias

- Rensink, R.A. et al. (1997). "To See or Not to See"
- Simons, D.J. & Levin, D.T. (1997). "Change Blindness"
- https://www.nngroup.com/articles/change-blindness/
