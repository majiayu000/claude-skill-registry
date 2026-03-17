---
name: javascript
description: >
  JavaScript essentials for vibecoders. Activated when Claude works with .js/.mjs/.jsx/.ts files.
  Covers the language concepts most commonly encountered during vibecoding.
---

# JavaScript — CodeSensei Teaching Module

## What is JavaScript?
- **Analogy:** If HTML is the skeleton and CSS is the skin, JavaScript is the brain and muscles. It makes things HAPPEN — clicks, animations, data loading, form validation.
- **Key insight:** JavaScript runs in the browser (frontend) AND on the server (backend with Node.js). Same language, two different environments.

## Core Concepts to Teach (in order of frequency during vibecoding)

### const / let / var
- `const` = a constant, can't be reassigned (use this most of the time)
- `let` = a variable that can change
- `var` = the old way, avoid it (mention only if Claude uses it)
- **Quiz:** "Why did Claude use `const` instead of `let` here?"

### Arrow Functions `() => {}`
- **Analogy:** A shorthand recipe card. Instead of writing "Function: do this thing," you write "=> do this thing"
- This is the #1 syntax that confuses beginners. Normalize it early.

### Objects `{}`
- **Analogy:** A filing cabinet with labeled drawers. Each drawer (property) has a name and contains something.
- `{ name: "Juan", age: 25 }` — the object has two "drawers"

### Arrays `[]`
- **Analogy:** A numbered list. Items have positions (starting from 0, not 1!)
- `.map()`, `.filter()`, `.forEach()` — the "assembly line" methods

### Async/Await
- **Analogy:** Ordering food at a restaurant. You place the order (`await`) and the kitchen works on it while you chat. When it's ready, it arrives. You don't stand at the kitchen door waiting.
- **Key insight:** Some things take time (loading data, saving to database). `await` means "wait for this to finish before moving on."

### Import/Export
- **Analogy:** Sharing tools between workshops. `export` puts a tool in the shared toolbox. `import` grabs it from there.
- **Key insight:** This is how code is organized into separate files that work together.

### Template Literals `` `Hello ${name}` ``
- **Analogy:** Mad Libs — the backtick string has blanks (`${}`) that get filled in with real values.

## Common Patterns in Vibecoded Projects
- `fetch()` — asking another server for data (like calling a restaurant for delivery)
- `.then()` / `.catch()` — what to do when the data arrives / if something goes wrong
- `JSON.parse()` / `JSON.stringify()` — translating between text and data objects
- `console.log()` — leaving yourself a note to see what's happening (debugging)

## What NOT to Teach Early
- Prototypes, closures, `this` keyword, generators, symbols, proxies
- These are advanced topics that vibecoders rarely encounter directly
