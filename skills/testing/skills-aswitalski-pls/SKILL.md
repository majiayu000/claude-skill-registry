---
name: skills-aswitalski-pls
description: 'There are four different project variants:'
---

### Name
Build Project

### Description
There are four different project variants:
- Alpha: the main project variant
- Beta: the experimental variant
- Gamma: the testing variant
- Delta: the production variant

The build command can be specified in many ways like:
- "build Alpha" or "build main variant" points to Alpha
- "build Beta", "build experimental" points to Beta
- "build Gamma", "build testing variant" points to Gamma
- "build Delta", "build production" points to Delta

Builds always need to be run from the project's root directory.

The build process typically requires only compilation.
The generation script needs to be run only when major changes are made.

If the user requests compilation only, the project generation script
does not have to be run and can be just skipped.

The steps provided should specify the variant name directly.

### Steps
- Navigate to the {VARIANT} project's root directory
- Execute the {VARIANT} project generation script
- Compile the {VARIANT}'s source code

### Execution
- [Navigate To Project]
- Run: python3 ./scripts/generate.py --release
- make build -j 8
