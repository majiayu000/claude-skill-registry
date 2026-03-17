---
description: Imported skill package from vercel
name: package
signature: 269ddd9e123a4c27c78ac9074e867688afa5f350828da88a480b2918917b4e55
source: /a0/tmp/skills_research/vercel/packages/react-best-practices-build/package.json
---

{
  "name": "react-best-practices-build",
  "version": "1.0.0",
  "description": "Build tooling for React Best Practices skill",
  "type": "module",
  "scripts": {
    "build": "pnpm build-agents && pnpm extract-tests",
    "build-agents": "tsx src/build.ts",
    "validate": "tsx src/validate.ts",
    "extract-tests": "tsx src/extract-tests.ts",
    "migrate": "tsx src/migrate.ts",
    "dev": "pnpm build && pnpm validate"
  },
  "keywords": [
    "react",
    "performance",
    "guidelines",
    "llm",
    "agents"
  ],
  "license": "MIT",
  "devDependencies": {
    "@types/node": "^20.0.0",
    "tsx": "^4.7.0",
    "typescript": "^5.3.0"
  }
}
