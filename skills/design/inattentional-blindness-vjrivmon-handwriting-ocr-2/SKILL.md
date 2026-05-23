---
name: inattentional-blindness
description:
  No percibimos lo que no esperamos ver. Use cuando diseñe elementos críticos
  que deben ser notados, o cuando coloque información fuera del flujo principal.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: perception
---

# Ceguera por Inatención

## Resumen

Cuando estamos enfocados en una tarea, podemos no percibir estímulos
inesperados, incluso si son conspicuos. Es diferente de mirar sin ver; es
literalmente no percibir lo que está frente a nosotros.

## Origen

- **Autores**: Arien Mack e Irvin Rock
- **Año**: 1992
- **Estudio**: "Inattentional Blindness"
- **Experimento famoso**: "Invisible Gorilla" (Simons & Chabris, 1999)

## Fundamento Psicológico

### Teoría de Carga Perceptual

- Recursos de atención son limitados
- Tareas demandantes consumen atención
- Lo inesperado compite por recursos
- Alta carga = más ceguera

### Factores que Aumentan

- Alta concentración en tarea
- Estímulo inesperado
- Estímulo periférico
- Baja relevancia percibida

## Aplicación en Diseño

### Elementos Críticos

- Posicionar en línea de visión natural
- Hacer relevantes para la tarea
- No depender de visión periférica
- Múltiples canales (visual + audio)

### Durante Flujos Intensivos

- Formularios: Validación inline, no solo al final
- Checkout: Resúmenes visibles durante proceso
- Gaming: HUD minimalista, cues importantes centrales
- Escritura: Autoguardado visible

### Prevenir Errores

- No asumir que algo fue "visto"
- Confirmaciones activas para acciones críticas
- Interrupciones controladas para info importante
- Timing: No mostrar cosas mientras usuario actúa

### Diseño de Alertas

- Modales para lo crítico (interrumpen tarea)
- Posición central para lo importante
- Animación para captar atención
- Contraste con el contexto

## Ejemplos

- **Error messages**: Mejor inline que en esquina
- **Unsaved changes**: Warning antes de salir
- **Security warnings**: Modales, no banners
- **Terms changes**: Requieren acción explícita
- **Price increases**: Highlight explícito

## Anti-patterns

- ❌ Info crítica en periféria
- ❌ Asumir que usuario "verá" algo
- ❌ Alertas mientras usuario escribe
- ❌ Elementos importantes entre distracciones
- ❌ Feedback crítico post-acción en zona no observada

## Métricas

- **Critical Info Miss Rate**: % de usuarios que no ven info crítica
- **Error Rate**: Por información no percibida
- **Eye Tracking**: Fixación en áreas críticas
- **Recall Tests**: Qué recuerdan de la pantalla

## Principios Relacionados

- [[change-blindness]] - No notar cambios
- [[banner-blindness]] - Ignorar elementos tipo ad
- [[von-restorff-effect]] - Hacer lo crítico distintivo

## Referencias

- Mack, A. & Rock, I. (1998). "Inattentional Blindness"
- Simons, D.J. & Chabris, C.F. (1999). "Gorillas in Our Midst"
- https://www.nngroup.com/articles/inattentional-blindness/
