---
name: cognitive-load
description:
  La cantidad de esfuerzo mental requerido para procesar información. Use cuando
  diseñe interfaces complejas, flujos de onboarding, o sistemas de información.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: perception
---

# Carga Cognitiva

## Resumen

La carga cognitiva es la cantidad total de esfuerzo mental utilizado en la
memoria de trabajo. Las interfaces deben minimizar la carga innecesaria para que
los usuarios puedan enfocarse en sus tareas.

## Origen

- **Autor**: John Sweller
- **Año**: 1988
- **Fuente**: "Cognitive Load During Problem Solving"
- **Contexto**: Teoría del aprendizaje instruccional

## Tipos de Carga Cognitiva

### Intrínseca

- Complejidad inherente de la tarea
- No se puede eliminar, solo gestionar
- Depende del conocimiento previo
- Ejemplo: Aprender a programar

### Extrínseca (Germane)

- Esfuerzo para aprender y construir esquemas
- Deseable y productiva
- Ejemplo: Conectar conceptos nuevos con previos

### Irrelevante (Extraneous)

- Causada por mal diseño
- Debe minimizarse siempre
- Ejemplo: UI confusa, instrucciones poco claras

## Aplicación en Diseño

### Reducir Carga Irrelevante

- Eliminar elementos decorativos sin función
- Simplificar navegación
- Agrupar información relacionada
- Usar patrones conocidos

### Gestionar Carga Intrínseca

- Dividir tareas complejas en pasos
- Progressive disclosure
- Ayuda contextual
- Scaffolding temporal

### Optimizar Carga Germane

- Ejemplos y analogías
- Feedback formativo
- Conexiones explícitas
- Práctica espaciada

### UI/UX Específico

- Limitar opciones visibles (Hick's Law)
- Chunking de información (Miller's Law)
- Reconocimiento sobre recuerdo
- Defaults inteligentes

## Ejemplos

- **Wizard patterns**: Dividen procesos complejos
- **Smart defaults**: Reducen decisiones necesarias
- **Autofill**: Elimina entrada manual
- **Templates**: Punto de partida, no hoja en blanco
- **Inline validation**: Feedback inmediato

## Anti-patterns

- ❌ Demasiadas opciones simultáneas
- ❌ Información no relacionada en misma vista
- ❌ Instrucciones largas antes de acción
- ❌ UI que requiere memorización
- ❌ Interrupciones frecuentes durante tareas

## Métricas

- **Task Completion Rate**: Éxito bajo carga
- **Time on Task**: Tiempo para completar
- **Error Rate**: Errores por sobrecarga
- **NASA-TLX Score**: Medición subjetiva de carga
- **Eye Tracking Fixations**: Patrones de búsqueda

## Principios Relacionados

- [[millers-law]] - Límite de memoria de trabajo
- [[hicks-law]] - Carga de decisión
- [[progressive-disclosure]] - Revelar complejidad gradualmente

## Referencias

- Sweller, J. (1988). "Cognitive Load During Problem Solving"
- Mayer, R.E. (2001). "Multimedia Learning"
- https://www.nngroup.com/articles/minimize-cognitive-load/
