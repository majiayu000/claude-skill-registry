---
name: build-fix
description: Fix build errors with minimal changes
agent: build-error-resolver
user-invocable: true
---

Fix the build error: $ARGUMENTS. Apply minimal surgical fix. Verify with dotnet build or npm run build.