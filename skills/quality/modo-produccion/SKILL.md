---
name: modo-produccion
description: Revisa una app/landing, detecta problemas típicos, propone mejoras y aplica correcciones con un checklist fijo para dejarlo listo para enseñar o publicar.
---

# Modo Producción (QA + Fix)

Skill especializado en revisión de calidad y corrección rápida de apps/landings antes de presentar, grabar o publicar. Aplica un checklist fijo y ejecuta correcciones mínimas de alto impacto.

## Cuándo usar este skill

- Cuando ya tenés algo generado (landing/app) y querés dejarlo "presentable"
- Cuando algo funciona "a medias" (móvil raro, imágenes rotas, botones sin acción, espaciados feos)
- Antes de enseñarlo a un cliente, grabarlo o publicarlo
- Cuando el usuario diga "revisá esto antes de publicar" o "dejalo listo para producción"
- Después de terminar desarrollo y antes de deploy

## Inputs necesarios

> **Regla**: Si falta alguno de estos inputs, PREGUNTAR antes de revisar.

| Input                    | Descripción                                        | Obligatorio |
| ------------------------ | -------------------------------------------------- | ----------- |
| **Archivo principal**    | Ruta del archivo (ej: `index.html`, `src/App.tsx`) | ✅ Sí       |
| **Objetivo de revisión** | "Lista para enseñar" o "Lista para publicar"       | ✅ Sí       |
| **Restricciones**        | No cambiar branding / copy / estructura / etc.     | ✅ Sí       |

### Diferencia entre objetivos

| Objetivo                | Nivel de exigencia      | Foco                                    |
| ----------------------- | ----------------------- | --------------------------------------- |
| **Lista para enseñar**  | Funcional + presentable | Que no haya errores visibles en demo    |
| **Lista para publicar** | Producción completa     | SEO, accesibilidad, performance, mobile |

## Checklist de Calidad (orden fijo)

### A) Funciona y se ve ✅

| #   | Verificación                                       | Crítico |
| --- | -------------------------------------------------- | ------- |
| A1  | Abre la preview / localhost sin errores en consola | 🔴 Sí   |
| A2  | Imágenes cargan y no hay rutas rotas               | 🔴 Sí   |
| A3  | Tipografías y estilos se aplican correctamente     | 🔴 Sí   |
| A4  | Links y botones funcionan (no hay 404)             | 🔴 Sí   |
| A5  | No hay errores de JavaScript en consola            | 🔴 Sí   |

### B) Responsive (móvil primero) 📱

| #   | Verificación                                        | Crítico  |
| --- | --------------------------------------------------- | -------- |
| B1  | Se ve bien en móvil (no se corta contenido)         | 🔴 Sí    |
| B2  | No hay scroll horizontal                            | 🔴 Sí    |
| B3  | Botones y textos tienen tamaños legibles (min 16px) | 🟡 Media |
| B4  | Secciones con espaciado coherente                   | 🟡 Media |
| B5  | Imágenes escalan correctamente                      | 🟡 Media |

### C) Copy y UX básica ✍️

| #   | Verificación                                     | Crítico  |
| --- | ------------------------------------------------ | -------- |
| C1  | Titular claro y coherente con la propuesta       | 🟡 Media |
| C2  | CTAs consistentes (mismo verbo, misma intención) | 🟡 Media |
| C3  | No hay texto "placeholder" tipo lorem ipsum      | 🔴 Sí    |
| C4  | Información de contacto correcta                 | 🔴 Sí    |
| C5  | Sin typos evidentes                              | 🟡 Media |

### D) Accesibilidad mínima ♿

| #   | Verificación                                 | Crítico  |
| --- | -------------------------------------------- | -------- |
| D1  | Contraste razonable en textos (4.5:1 mínimo) | 🟡 Media |
| D2  | Imágenes con atributo alt                    | 🟡 Media |
| D3  | Estructura de headings (h1, h2, h3) lógica   | 🟡 Media |
| D4  | Formularios con labels asociados             | 🟡 Media |

### E) SEO básico (solo para "publicar") 🔍

| #   | Verificación                          | Crítico  |
| --- | ------------------------------------- | -------- |
| E1  | Title tag presente y descriptivo      | 🔴 Sí    |
| E2  | Meta description presente             | 🟡 Media |
| E3  | Un solo h1 por página                 | 🟡 Media |
| E4  | URLs amigables (sin caracteres raros) | 🟡 Media |

## Workflow

### Paso 1: Diagnóstico rápido

1. Abrir el proyecto/archivo
2. Ejecutar checklist completo
3. Generar lista de 5–10 problemas priorizados por criticidad (🔴 primero)

### Paso 2: Plan de arreglos

4. Listar máximo 8 cambios con formato:
   - **Qué**: descripción del cambio
   - **Por qué**: problema que resuelve
   - **Dónde**: archivo y línea aproximada

### Paso 3: Aplicar cambios

5. Modificar archivos necesarios
6. Aplicar correcciones de menor a mayor impacto
7. Mantener cambios mínimos (no refactorizar todo)

### Paso 4: Validación

8. Volver a abrir preview
9. Verificar checklist de nuevo
10. Confirmar que no se rompió nada

### Paso 5: Resumen final

11. Listar cambios hechos
12. Indicar qué queda opcional para mejorar después

## Instrucciones

### Reglas obligatorias

| Regla                                                      | Razón                   |
| ---------------------------------------------------------- | ----------------------- |
| No cambiar estilo de marca si existe skill de marca activo | Consistencia            |
| No rehacer todo: corregir lo mínimo                        | Velocidad + bajo riesgo |
| Si hay conflicto "bonito" vs "claro" → priorizar claridad  | UX > estética           |
| Máximo 8 cambios por pasada                                | Evitar romper cosas     |
| Siempre validar después de cambios                         | Detectar regresiones    |

### Prioridad de correcciones

```
1. 🔴 Errores críticos (app no funciona, errores JS, 404)
2. 🔴 Problemas de mobile (scroll horizontal, contenido cortado)
3. 🟡 UX/Copy (placeholders, typos, CTAs inconsistentes)
4. 🟡 Accesibilidad (contraste, alts, headings)
5. 🟢 Mejoras opcionales (optimizaciones, pulido visual)
```

### Manejo de errores

- Si hay demasiados problemas (>15) → priorizar solo 🔴 críticos primero
- Si un cambio rompe otra cosa → revertir y buscar alternativa
- Si las restricciones impiden arreglar algo crítico → notificar al usuario

## Output (formato exacto)

```markdown
## 🔍 Diagnóstico

### Problemas encontrados (priorizados)

| #   | Problema      | Categoría | Criticidad | Archivo         |
| --- | ------------- | --------- | ---------- | --------------- |
| 1   | [Descripción] | A/B/C/D/E | 🔴/🟡/🟢   | [archivo:línea] |
| 2   | [Descripción] | A/B/C/D/E | 🔴/🟡/🟢   | [archivo:línea] |
| ... | ...           | ...       | ...        | ...             |

**Total**: X problemas (Y críticos, Z medios)

---

## 🔧 Plan de Arreglos

| #   | Qué cambio | Por qué                 | Dónde           |
| --- | ---------- | ----------------------- | --------------- |
| 1   | [Cambio]   | [Problema que resuelve] | [archivo:línea] |
| 2   | [Cambio]   | [Problema que resuelve] | [archivo:línea] |
| ... | ...        | ...                     | ...             |

---

## ✅ Cambios Aplicados

1. ✅ [Cambio 1] - [archivo]
2. ✅ [Cambio 2] - [archivo]
3. ✅ [Cambio 3] - [archivo]
   ...

---

## 📊 Resultado

### Estado: ✅ OK para [enseñar/publicar] | ⚠️ Requiere más trabajo

### Checklist post-fix

| Categoría           | Estado   |
| ------------------- | -------- |
| A) Funciona y se ve | ✅/⚠️/❌ |
| B) Responsive       | ✅/⚠️/❌ |
| C) Copy y UX        | ✅/⚠️/❌ |
| D) Accesibilidad    | ✅/⚠️/❌ |
| E) SEO (si aplica)  | ✅/⚠️/❌ |

### Mejoras opcionales (para después)

- [ ] [Mejora 1]
- [ ] [Mejora 2]
- [ ] [Mejora 3]

---

## 📝 Notas

[Observaciones adicionales, advertencias o recomendaciones]
```
