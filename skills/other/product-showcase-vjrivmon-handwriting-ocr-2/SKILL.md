---
name: product-showcase
description: |
  Genera demos visuales y contenido LinkedIn con metodo PAR para productos tech.
  Usar cuando tienes MVP listo para mostrar al mundo.
allowed-tools: Read, Write, WebFetch, Glob, Bash
---

# Product Showcase Skill

Este skill te ayuda a crear demos profesionales y contenido de LinkedIn para
mostrar tus proyectos tecnicos. Utiliza el metodo PAR
(Problema-Accion-Resultado) para comunicar el valor de tu producto de forma
efectiva.

## Cuando Usar Este Skill

- Tienes un MVP funcional listo para mostrar
- Quieres crear contenido para LinkedIn/Twitter
- Necesitas una landing page profesional
- Quieres documentar el valor de tu proyecto

## Flujo de Trabajo

1. **Analizar el Proyecto**
   - Identificar el problema que resuelve
   - Documentar la solucion innovadora
   - Recopilar metricas y resultados

2. **Generar Contenido PAR**
   - Problema: El dolor que existe
   - Accion: Tu solucion unica
   - Resultado: Metricas concretas

3. **Crear Visuales**
   - Before/After del producto
   - Graficos de benchmarks
   - Diagrama de arquitectura

4. **Estructurar Landing**
   - Hero con propuesta de valor
   - Seccion de problema
   - Demo interactiva
   - Llamada a la accion

## Metodo PAR Explicado

### P - Problema

El problema debe ser:

- Especifico y medible ("45% de error" no "muchos errores")
- Relatable (el lector debe identificarse)
- Doloroso (que motive a buscar solucion)

Ejemplo:

> "Pase horas transcribiendo apuntes que ningun OCR podia leer. Google Lens,
> Tesseract... todos fallaban con MI letra."

### A - Accion (Tu Solucion)

La accion debe mostrar:

- Que hace diferente tu solucion
- Por que es un "oceano azul" (sin competencia directa)
- La innovacion tecnica clave

Ejemplo:

> "Cree un sistema RAG que APRENDE de mis correcciones. Cada vez que corrijo un
> error, el sistema lo recuerda."

### R - Resultado

Los resultados deben ser:

- Cuantificables (numeros especificos)
- Comparativos (vs alternativas)
- Impresionantes pero creibles

Ejemplo:

> "82% accuracy inicial -> 95%+ despues de 50 correcciones Modelo qwen2.5vl
> supera a minicpm-v en 26 puntos"

## Templates Disponibles

### 1. linkedin-par.md

Template para posts de LinkedIn usando metodo PAR. Incluye estructura, hashtags
recomendados y CTA.

### 2. landing-structure.md

Estructura de landing page con secciones:

- Hero
- Problema
- Solucion
- Demo
- Benchmark
- CTA

### 3. demo-script.md

Guion para grabar video demo o GIF. Incluye timing y puntos clave a mostrar.

## Checklist UX Demo

Antes de publicar, verifica:

- [ ] Valor entendible en <10 segundos
- [ ] Before/after visualmente claro
- [ ] Numeros destacados y legibles
- [ ] CTA claro y visible
- [ ] Mobile-friendly
- [ ] Velocidad de carga <3s
- [ ] Sin errores de consola
- [ ] Links funcionando
- [ ] Imagenes optimizadas

## Frameworks Recomendados

| Caso de Uso | Framework          | Razon                     |
| ----------- | ------------------ | ------------------------- |
| Demo rapida | Tailwind + shadcn  | Setup minimo, profesional |
| Dashboard   | Next.js + Recharts | SSR, charts nativos       |
| Landing SEO | Astro              | Ultra rapido, estatico    |
| App ML      | Streamlit/Gradio   | Rapido para AI demos      |
| Showcase    | Next.js 14         | Full-stack, Vercel deploy |

## Visuales Esenciales

### 1. Before/After

- Slider interactivo
- Izquierda: estado actual/competencia
- Derecha: tu solucion

### 2. Benchmark Chart

- Barras horizontales
- Tu solucion destacada en verde
- Competencia en gris/rojo

### 3. Arquitectura

- Diagrama simple del flujo
- Iconos reconocibles
- Maximo 5-7 elementos

### 4. Metricas Hero

- Numero grande y destacado
- Descripcion corta
- Contexto comparativo

## Hashtags Recomendados

### Tech/Dev

#MachineLearning #Python #OpenSource #AI #DeepLearning #ComputerVision

### Producto

#ProductDevelopment #MVP #Startup #TechInnovation #BuildInPublic

### Comunidad

#DevCommunity #100DaysOfCode #LearnInPublic #IndieHacker

## Ejemplo de Post Completo

```markdown
Sabes que los OCR genericos tienen hasta 45% de error con letra manuscrita?

**El Problema:** Pase horas transcribiendo apuntes que ningun OCR podia leer.
Google Lens, Tesseract, apps de notas... todos fallaban con MI letra.

**La Solucion:** Cree un sistema RAG que APRENDE de mis correcciones. Cada vez
que corrijo un error, el sistema lo recuerda.

**Resultados:**

- 82% accuracy inicial -> 95%+ despues de 50 correcciones
- Modelo qwen2.5vl supera a minicpm-v en 26 puntos
- <100ms para aplicar correcciones

[GIF: Before/After]

Demo: [link] Repo: [link]

Stack: Python + SQLite + Ollama Lo mejor: funciona con tu propia GPU.

#MachineLearning #OCR #Python #OpenSource #RAG
```

## Recursos

- [Excalidraw](https://excalidraw.com) - Diagramas de arquitectura
- [Gifski](https://gif.ski) - Crear GIFs de alta calidad
- [Recharts](https://recharts.org) - Graficos React
- [shadcn/ui](https://ui.shadcn.com) - Componentes UI
