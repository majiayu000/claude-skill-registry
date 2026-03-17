---
name: git-commits
description: Genera mensajes de commit descriptivos siguiendo Conventional Commits. Analiza cambios y sugiere mensajes claros. Úsalo cuando escribas commits o menciones "commit".
---

# Git Commits - Conventional Commits

Skill para escribir commits siguiendo Conventional Commits en el proyecto Erica Ávalos.

## Formato Estándar

```
<tipo>(<scope>): <descripción>

<cuerpo opcional>

<footer opcional>
```

### Tipos Permitidos

- **feat**: Nueva funcionalidad
- **fix**: Bug fix
- **docs**: Cambios en documentación
- **style**: Cambios de formato (espacios, comas, etc)
- **refactor**: Refactoring de código (ni feat ni fix)
- **perf**: Mejoras de performance
- **chore**: Cambios en configuración, build, assets
- **ui**: Cambios en interfaz (color, layout, animaciones)

### Scope para este Proyecto

- `ui` - Secciones HTML (hero, about, services, projects, contact)
- `styles` - CSS y paleta de colores
- `assets` - Imágenes, SVGs
- `scripts` - JavaScript funcionalidad
- `config` - .claude/, .gitignore, package.json
- `docs` - README, CLAUDE.md, comentarios

## Proceso

### 1. Analizar Cambios

```bash
git status
git diff --staged
```

### 2. Identificar Tipo y Scope

- ¿Es feature nueva? → `feat`
- ¿Es bug fix? → `fix`
- ¿Es solo docs? → `docs`
- ¿Es solo CSS? → `style`
- ¿Es refactor? → `refactor`

### 3. Generar Mensaje

**Reglas:**
- Máximo 72 caracteres en primera línea
- Imperativo ("add" no "added")
- Sin punto final
- Minúsculas después de los dos puntos
- Body explica el "por qué", no el "qué"

**Ejemplos para este proyecto:**

```
feat(styles): aplicar paleta Tierra y Herencia #3

Cambiar de dark mode a light mode usando colores 2026:
- Arcilla #B66E41 (primario)
- Taupe Café #8C6C50 (secundario)
- Óxido #9B372E (confianza)

Implementa regla 60-30-10 con neutrales emocionales.
```

```
fix(ui): corregir email typo en contact section

Cambiar eriaavalos85@gmail.com por eriavalos85@gmail.com
en líneas 287, 292 y 329 de index.html
```

```
ui(scripts): refactorizar main.js con namespaces

Modularizar funcionalidad en objetos:
- MobileNav
- SmoothScroll
- ScrollAnimations
- Lightbox

Mejora mantenibilidad y legibilidad.
```

```
chore(assets): optimizar imágenes JPG

Comprimir proyecto-*.jpg de 5.5MB a 1.5MB usando ImageMagick.
Calidad: 80%, resize máximo 1200x1200px.
```

```
docs(claude): agregar .claude/CLAUDE.md completo

Documentación del proyecto incluyendo:
- Sistema de diseño (paleta #3)
- Convenciones de código
- Instrucciones de desarrollo
```

```
ui(hero): agregar eyebrow sobre sección hero

Nuevo elemento p.hero-eyebrow con:
- "Gasista Matriculada • Maestro Mayor de Obras"
- Estilo: uppercase, letter-spacing, color arcilla
```

```
style(css): eliminar CSS duplicado

Remover:
- .mat-item svg (líneas 185-191)
- .exp-badge strong (líneas 195-202)
- .service-header-icon (líneas 206-211)
- .project-tag (líneas 215-228)
- .contact-card-centered (líneas 232-241)
- .contact-row:hover (líneas 244-255)
- .icon-small (líneas 258-263)

Reducción: 833 → 750 líneas.
```

## Reglas

1. **Primera línea < 72 caracteres**
2. **Línea en blanco entre header y body**
3. **Body explica el "por qué", no el "qué"**
4. **Footer para issue references (Closes #123)**
5. **Breaking changes con "BREAKING CHANGE:" en footer**

## Anti-Patrones (❌ Evitar)

```
❌ "updated files"
❌ "fixes"
❌ "WIP"
❌ "changes"
❌ "asdf"
❌ "final version"
❌ "this should work now"
```

## Flujo de Trabajo

1. Hacer cambios en el código
2. Revisar cambios: `git diff`
3. Preguntar a Claude: "Genera mensaje de commit para estos cambios"
4. Claude analiza y genera mensaje siguiendo Conventional Commits
5. Commit: `git commit -m "mensaje generado"`

## Referencias

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
