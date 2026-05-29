---
name: synthkernel
description: Structure your APP using SynthKernel, a type-safe and composable meta architecture for modular monolith development in TypeScript.
license: MIT
---

## About SynthKernel

SynthKernel is a TypeScript software architecture that helps you write efficient, clean and modular code.

Typical practice of SynthKernel consists a module loader class and module classes:

- The module loader class manages module lifecycles, orchestrates types, and behaves as an facade at the surface of your app logic.
- All module classes extend a `BaseModule` class, they define APIs, execute actual logic, augment the loader class and wire each other via dependency injection.
- Types are resolved via generics orchestration.
- Modules are composed to the loader to form an APP. A module loader can also be a module of a parent loader.
- It is applicable to almost all use cases, including but not limited to backend service, complex automation, CLI application, and canvas rendering engine.

## File System Conventions

SynthKernel should be structured in a tree pattern.

A loader together with the base module and all its direct modules should be placed flatly in one folder:

- the file accommodating the loader should be named `index.ts`
- base module named `BaseModule.ts`
- types named `types.ts`
- all modules are named `(module name in PascalCase).ts`
- no restriction to the name of other files

It's a standard practice to turn a over-bloated module into a new loader-module structure, then simply turn the module into a folder with the same requirements above.

## When to Use

- At the early stage of development, when you have clues of logic yet haven't written any code.
- You don't have a clear architecture convention.
- During refactors when you aim to split some large modules or make the project modular.
- You are adding new functionalities and considering to make a new module, wanting to understand SynthKernel.

## When Not to Use

- You are not supposed to create or change the architecture.
- You are developing front-end web UI which has its own conventions.
- You are serving for a simple project (loc < 200) where a classical monolith is more convenient.

## Actions

- If you are implementing SynthKernel from scratch or refactoring existing code to adopt SynthKernel, go to [start](start.md).
- If you are adding a new module or splitting modules, go to [maintenance](maintenance.md).
- You can find an example of standard practice in [./example](example/README.md).
