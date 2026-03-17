---
name: constraints-principle
description:
  Limita acciones posibles para prevenir errores. Use cuando diseñe formularios,
  flujos críticos, o sistemas donde los errores son costosos.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: design-principles
---

# Principio de Restricciones (Constraints)

## Resumen

Las restricciones limitan las acciones posibles del usuario, previniendo errores
al hacer imposible o difícil realizar acciones incorrectas. Guían al usuario
hacia el camino correcto.

## Origen

- **Autor**: Don Norman
- **Año**: 1988
- **Fuente**: "The Design of Everyday Things"

## Tipos de Restricciones

### Físicas

- Forma que solo permite un uso
- USB-C que entra de cualquier lado
- Tarjeta SIM que solo cabe de una forma
- En digital: campos con máximo de caracteres

### Semánticas

- Significado que restringe opciones
- Un semáforo solo puede estar rojo, amarillo o verde
- En digital: dropdowns con opciones válidas

### Culturales

- Convenciones sociales
- Rojo = peligro/stop
- Verde = ok/continuar
- En digital: patrones aprendidos

### Lógicas

- Relaciones naturales entre elementos
- En formularios: campos que se habilitan condicionalmente
- Validaciones que previenen estados imposibles

## Aplicación en Diseño

### Formularios

- Input types específicos (email, tel, date)
- Min/max en campos numéricos
- Dropdowns en lugar de texto libre
- Campos disabled hasta completar prerrequisitos

### Flujos de Trabajo

- Steps que no se pueden saltar
- Validación antes de continuar
- Confirm antes de acciones destructivas
- Permisos basados en roles

### Datos

- Formatos predefinidos (fecha, teléfono)
- Ranges en sliders
- Opciones mutuamente excluyentes
- Límites de caracteres

### Navegación

- Estados disabled para opciones no disponibles
- Rutas bloqueadas hasta completar requisitos
- Logout que no permite volver sin login
- Deep links validados

## Ejemplos

- **Date pickers**: Solo fechas válidas seleccionables
- **Stripe**: Formato de tarjeta forzado
- **Git**: Branch protection rules
- **Forms**: Required fields
- **USB-C**: Reversible por diseño

## Anti-patterns

- ❌ Permitir datos inválidos que luego fallan
- ❌ Campos de texto libre para datos estructurados
- ❌ Acciones destructivas sin confirmación
- ❌ Estados inconsistentes posibles
- ❌ Constraints tan estrictas que frustran

## Métricas

- **Error Prevention Rate**: Errores evitados por constraints
- **Form Validation Failures**: Fallos en validación
- **Invalid State Occurrences**: Estados imposibles alcanzados
- **User Frustration Score**: Balance constraints/flexibilidad

## Principios Relacionados

- [[poka-yoke]] - Diseño a prueba de errores
- [[nielsen-error-prevention]] - Prevenir antes que curar
- [[postels-law]] - Balance entre flexibilidad y rigor

## Referencias

- Norman, D. (2013). "The Design of Everyday Things"
- Lidwell, W. et al. (2010). "Universal Principles of Design"
- https://www.nngroup.com/articles/slips/
