---
name: build-scaffold
description: Set up the project foundation. Directory structure, configs, dependencies.
---

# Build Scaffold

When starting a new project:
1. Create clean directory structure
2. Initialize with the chosen technology
3. Set up basic configuration
4. Verify it runs with a "hello world" or equivalent
5. Tell user: "框架搭好了，我来开始做功能。"

Rules:
- Keep structure flat and simple. No over-engineering.
- Every file has a clear purpose. No boilerplate for the sake of boilerplate.
- If using Go: single main.go to start, split files only when needed
- If using Node: minimal package.json, no unnecessary dependencies
