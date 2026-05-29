---
name: mvp-generator
description: Genera MVPs completos desde SPEC.md orquestando todos los agentes especializados
allowed-tools: Task, Read, Write, Bash, Glob, Grep
---

# MVP Generator Skill

Generas MVPs completos y funcionales a partir de especificaciones SPEC.md, orquestando los 7 agentes especializados en secuencia óptima.

## Requisito Previo

Antes de ejecutar este skill, DEBE existir un archivo SPEC.md en `.claude/specs/`.
Si no existe, indicar al usuario que primero ejecute `/project:interview <nombre>`.

## Workflow de Generación

### Fase 1: Validación (Secuencial)
1. Leer SPEC.md desde `.claude/specs/$ARGUMENTS.md`
2. Validar que contenga todas las secciones requeridas:
   - [ ] Resumen Ejecutivo
   - [ ] Declaración del Problema
   - [ ] Usuarios Objetivo
   - [ ] Requisitos Funcionales (mínimo 3 features)
   - [ ] Arquitectura Técnica
   - [ ] Especificaciones UI/UX
3. Si falta alguna sección, solicitar al usuario que complete la entrevista

### Fase 2: Foundation (Paralelo)
Lanzar en paralelo:
- **Agente 01-project-setup**: Inicializar estructura del proyecto
- **Agente 02-git-cicd**: Configurar Git y CI/CD

Esperar a que ambos completen antes de continuar.

### Fase 3: Architecture (Secuencial)
- **Agente 03-architecture**: Diseñar arquitectura basada en SPEC
- Presentar arquitectura al usuario para aprobación
- Si no aprueba, iterar con feedback

### Fase 4: Implementation (Paralelo)
Lanzar en paralelo:
- **Agente 04-ui-ux**: Implementar interfaces (invocar /ux-expert si es necesario)
- **Agente 05-testing**: Escribir tests (TDD)

### Fase 5: Polish (Paralelo)
Lanzar en paralelo:
- **Agente 06-documentation**: Generar documentación
- **Agente 07-deployment**: Configurar deployment

### Fase 6: Delivery (Secuencial)
1. Ejecutar suite completa de tests
2. Verificar que todos los tests pasen
3. Si hay fallos, iterar hasta corregir
4. Crear commit con mensaje descriptivo
5. Crear PR con resumen del MVP

## Uso de Task Tool para Orquestación

```
# Ejemplo de lanzamiento paralelo
Task(subagent_type="general-purpose", prompt="...", run_in_background=true)
Task(subagent_type="general-purpose", prompt="...", run_in_background=true)
```

## Criterios de Éxito

El MVP está completo cuando:
- [ ] Estructura de proyecto creada
- [ ] CI/CD configurado
- [ ] Arquitectura implementada
- [ ] UI funcional para features core
- [ ] Tests con cobertura >= 80%
- [ ] Documentación generada
- [ ] Deployment configurado
- [ ] Todos los tests pasan
- [ ] PR creado

## Output Esperado

Al finalizar, el sistema habrá generado:
1. Proyecto funcional con todas las features del MVP
2. Suite de tests completa
3. Documentación (README, API docs)
4. Configuración de CI/CD
5. Configuración de deployment
6. PR listo para review

## Manejo de Errores

Si algún agente falla:
1. Registrar el error
2. Intentar reiniciar el agente (máximo 2 intentos)
3. Si persiste, notificar al usuario y preguntar cómo proceder
4. Ofrecer opciones: reintentar, saltar, o abortar
