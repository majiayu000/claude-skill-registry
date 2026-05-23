---
name: button-styles
description: Sistema de estilos de botones consistentes para iqEngi (Cards, CTAs, Formularios)
---

# Sistema de Botones Consistentes - iqEngi

Este skill define los estilos de botones estándar para mantener consistencia visual en todo el proyecto.

## Filosofía de Diseño

- **Jerarquía Visual**: Primary para acciones principales, Outline para secundarias
- **Consistencia**: Mismo hover, transiciones y tamaños base
- **Accesibilidad**: Contraste AA garantizado con `text-white` sobre primary

---

## 🎨 Clases Base de Botones

### 1. Botón Primary (CTA Principal)

Usar para: **Inscribirse, Comprar, Guardar, Enviar, Ver Detalles principal**

```html
<!-- Tamaño Normal (Cards, Formularios) -->
<button class="btn btn-primary h-10 min-h-[40px] px-6 text-white shadow-md shadow-primary/20 hover:bg-[var(--color-btn-hover)] hover:border-[var(--color-btn-hover)] hover:shadow-lg hover:shadow-[var(--color-btn-hover)]/40 hover:scale-[1.03] rounded-xl transition-all duration-300">
  Acción Principal
</button>

<!-- Tamaño Grande (Hero, CTAs destacados) -->
<button class="btn btn-primary btn-lg min-w-[160px] rounded-full shadow-lg shadow-primary/30 hover:bg-[var(--color-btn-hover)] hover:border-[var(--color-btn-hover)] hover:shadow-xl hover:shadow-[var(--color-btn-hover)]/40 hover:scale-105 transition-all duration-300">
  Explorar Cursos
</button>
```

### 2. Botón Outline (Secundario)

Usar para: **Ver Detalles, Cancelar, Opciones alternativas**

```html
<!-- Tamaño Normal -->
<button class="btn btn-outline h-10 min-h-[40px] hover:!bg-[var(--color-btn-hover)] hover:!border-[var(--color-btn-hover)] hover:!text-white rounded-xl transition-all duration-300">
  Ver Detalles
</button>

<!-- Tamaño Grande -->
<button class="btn btn-outline btn-lg rounded-full hover:bg-[var(--color-btn-hover)] hover:border-[var(--color-btn-hover)] hover:text-white hover:scale-105 transition-all duration-300">
  Saber Más
</button>
```

### 3. Botón Ghost (Terciario/Navegación)

Usar para: **Enlaces de navegación, acciones de bajo énfasis**

```html
<button class="btn btn-ghost btn-lg min-w-[160px] rounded-full hover:bg-[var(--color-surface-2)]">
  Unirse a la Comunidad
</button>
```

---

## 📐 Reglas de Tamaño

| Contexto | Tamaño Base | Altura | Border Radius |
|----------|-------------|--------|---------------|
| Cards (CourseCard, Cards) | Normal | `h-10 min-h-[40px]` | `rounded-xl` |
| Hero / CTA sections | `btn-lg` | Auto | `rounded-full` |
| Formularios | Normal | `h-10 min-h-[40px]` | `rounded-xl` |
| Navbar | `btn-sm` o Normal | Auto | Default |

---

## 🎭 Estados de Hover (Obligatorios)

Todos los botones deben incluir:

```css
/* Para Primary */
hover:bg-[var(--color-btn-hover)]
hover:border-[var(--color-btn-hover)]
hover:shadow-lg
hover:shadow-[var(--color-btn-hover)]/40
hover:scale-[1.03]  /* o hover:scale-105 para btn-lg */
transition-all duration-300

/* Para Outline */
hover:!bg-[var(--color-btn-hover)]
hover:!border-[var(--color-btn-hover)]
hover:!text-white
transition-all duration-300
```

---

## 📋 Plantillas Copiables

### Card con dos botones (CourseCard)

```tsx
<div className="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-base-200">
  <a 
    href={`/cursos/${slug}`} 
    className="btn btn-outline h-10 min-h-[40px] hover:!bg-[var(--color-btn-hover)] hover:!border-[var(--color-btn-hover)] hover:!text-white rounded-xl transition-all duration-300"
  >
    Ver Detalles
  </a>
  <button className="btn btn-primary h-10 min-h-[40px] text-white shadow-md shadow-primary/20 hover:bg-[var(--color-btn-hover)] hover:border-[var(--color-btn-hover)] hover:shadow-lg hover:shadow-[var(--color-btn-hover)]/40 hover:scale-[1.03] uppercase font-bold tracking-wide rounded-xl transition-all duration-300">
    Inscribirme
  </button>
</div>
```

### Hero CTA (dos botones)

```tsx
<div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
  <a
    href="/cursos"
    className="btn btn-primary btn-lg min-w-[160px] rounded-full shadow-lg shadow-primary/30 hover:bg-[var(--color-btn-hover)] hover:border-[var(--color-btn-hover)] hover:shadow-xl hover:shadow-[var(--color-btn-hover)]/40 hover:scale-105 transition-all duration-300"
  >
    Explorar Cursos
  </a>
  <a
    href="/comunidad"
    className="btn btn-ghost btn-lg min-w-[160px] rounded-full hover:bg-[var(--color-surface-2)]"
  >
    Unirse a la Comunidad
  </a>
</div>
```

### Botón único en Card simple

```astro
<a 
  href={`/cursos/${slug}`} 
  class="btn btn-primary h-10 min-h-[40px] px-6 text-white shadow-md shadow-primary/20 hover:bg-[var(--color-btn-hover)] hover:border-[var(--color-btn-hover)] hover:shadow-lg hover:shadow-[var(--color-btn-hover)]/40 hover:scale-[1.03] uppercase font-bold tracking-wide w-full md:w-auto rounded-xl transition-all duration-300"
>
  Ver Detalles
</a>
```

---

## ⚠️ Antipatrones (NO HACER)

```html
<!-- ❌ Sin hover states -->
<button class="btn btn-primary">Acción</button>

<!-- ❌ Mezclar estilos de tamaño -->
<button class="btn btn-primary btn-lg h-10">Inconsistente</button>

<!-- ❌ Border radius inconsistente -->
<button class="btn btn-primary rounded-md">No usar rounded-md</button>

<!-- ❌ Colores hardcodeados -->
<button class="bg-purple-500 hover:bg-purple-600">No usar colores directos</button>
```

---

## 🔧 Variables CSS Relacionadas

Definidas en `src/styles/global.css`:

| Variable | Uso |
|----------|-----|
| `--color-primary` | Color base del btn-primary |
| `--color-btn-hover` | Color hover (azul #2b7fff) |
| `--color-surface-2` | Background hover para btn-ghost |

---

## Ejemplos de Archivos Correctos

- `src/components/molecules/CourseCard.tsx` - Patrón de 2 botones en card
- `src/components/home/Hero.tsx` - CTA principal con btn-lg
- `src/components/sections/CoursesHero.astro` - Hero con botones primary + outline
