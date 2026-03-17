---
name: nielsen-match-real-world
description:
  Asegura que el sistema use lenguaje y conceptos familiares para los usuarios.
  Use cuando escriba copy, diseñe iconografía, o estructure información para que
  coincida con modelos mentales del usuario.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: heuristics
---

# Coincidencia entre el Sistema y el Mundo Real

## Resumen

El sistema debe hablar el idioma del usuario, usando palabras, frases y
conceptos familiares, en lugar de términos técnicos orientados al sistema.
Seguir convenciones del mundo real hace que la información aparezca en orden
natural y lógico.

## Origen

- **Autor**: Jakob Nielsen
- **Año**: 1994 (refinado 2020)
- **Fuente**: Nielsen Norman Group - "10 Usability Heuristics for User Interface
  Design"

## Fundamento Psicológico

Los usuarios llegan con **modelos mentales** formados por experiencias previas
en el mundo físico y digital. Cuando la interfaz coincide con estos modelos, el
aprendizaje es más rápido y los errores disminuyen. El principio de
**transferencia de conocimiento** permite que habilidades existentes se apliquen
a nuevos contextos.

## Aplicación en Diseño

### Lenguaje Natural

- Evitar jerga técnica: "Error 404" → "Página no encontrada"
- Usar verbos activos: "Guardar cambios" en lugar de "Persistir datos"
- Adaptar vocabulario al dominio del usuario (médico, legal, etc.)
- Mensajes de error en lenguaje humano, no códigos

### Metáforas Visuales

- Carpetas para organizar archivos
- Carrito de compras en e-commerce
- Papelera para elementos eliminados
- Sobre para correo electrónico

### Organización de Información

- Orden alfabético para listas de países/nombres
- Orden cronológico para eventos/historial
- Agrupación por categorías familiares
- Jerarquías que reflejen estructuras reales

### Convenciones Culturales

- Formato de fechas según región (DD/MM/YYYY vs MM/DD/YYYY)
- Símbolos de moneda apropiados
- Direcciones de lectura (LTR vs RTL)
- Colores con significado cultural (rojo = peligro en occidente)

## Ejemplos

- **Apple Notes**: Simula papel rayado con tipografía manuscrita
- **Kindle**: Paginación y "pasar páginas" como libro físico
- **Calendario de Google**: Vista mensual con cuadrícula familiar
- **Spotify**: "Biblioteca" y "Listas de reproducción" como colección física
- **Banking apps**: Terminología de estados de cuenta tradicionales

## Anti-patterns

- ❌ Mensajes como "NullPointerException" mostrados al usuario
- ❌ Botones con labels técnicos: "Submit", "Execute", "Invoke"
- ❌ Fechas en formato ISO sin localización: "2024-01-15T14:30:00Z"
- ❌ Iconos abstractos sin tooltip explicativo
- ❌ Menús organizados por arquitectura técnica, no por tareas del usuario

## Métricas

- **Task Success Rate**: % de tareas completadas sin ayuda
- **Time on Task**: Reducción cuando la UI es intuitiva
- **Error Rate**: Errores causados por malinterpretación
- **Learnability Score**: Tiempo para dominar funcionalidad básica

## Principios Relacionados

- [[jakobs-law]] - Los usuarios esperan patrones conocidos
- [[least-astonishment]] - El sistema debe comportarse predeciblemente
- [[past-experience]] - Gestalt de experiencia pasada

## Referencias

- Nielsen, J. (1994). "Usability Engineering". Morgan Kaufmann
- Norman, D. (2013). "The Design of Everyday Things". Basic Books
- https://www.nngroup.com/articles/match-system-real-world/
