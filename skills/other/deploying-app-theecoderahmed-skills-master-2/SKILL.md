---
name: deploying-app
description: Prepares applications for production by generating Dockerfiles, CI/CD pipelines, and platform configurations. Supports Docker, Vercel, Netlify, and GitHub Actions.
---

# Deployment & DevOps Engineer

## When to use this skill
- When the user asks "how do I put this online?" or "deploy this to Vercel".
- When the user needs to "dockerize" the app.
- When setting up automated testing/deployment (CI/CD).

## Workflow
1.  **Identify Target**: Where is it going?
    - **PaaS**: Vercel (Next.js), Netlify (Static), Heroku/Railway (Node/Python).
    - **Container**: Docker (Universal).
    - **Mobile**: App Store (iOS) & Google Play (Android) via Fastlane.
2.  **Configuration**: Generate the specific config file.
    - Vercel: `vercel.json` (rarely needed, usually zero-config).
    - Docker: `Dockerfile` + `.dockerignore`.
    - Mobile: `fastlane/Appfile` + `fastlane/Fastfile`.
    - GitHub: `.github/workflows/deploy.yml`.
3.  **Optimization**: Ensure build scripts are efficient (multi-stage builds for Docker).

## Instructions

### 1. Docker Strategy (The Universal Container)
Always use **Multi-Stage Builds** to keep images small.
- **Stage 1 (Builder)**: Install all dependencies, build the app.
- **Stage 2 (Runner)**: Copy ONLY the build output (e.g., `.next/standlone`, `dist/`) to a lightweight Alpine Node/Python image.

### 2. Docker Next Steps (After generating Dockerfile)
1.  **Build It**: `docker build -t my-app .`
2.  **Test It**: `docker run -p 3000:3000 my-app`
3.  **Ship It**: Push to a registry (Docker Hub, AWS ECR) -> `docker push my-repo/my-app`.

### 3. Mobile Deployment (Fastlane)
For React Native or Flutter:
- **Init**: Run `fastlane init` inside `android/` and `ios/` folders.
- **Match**: Use `fastlane match` to handle painful iOS certificates automatically.
- **Lanes**: Create a `deploy` lane that increments build number -> builds app -> uploads to Store.

### 4. CI/CD Pipelines (GitHub Actions)
Standard "Build & Test" workflow:
- Trigger: `push` to `main`.
- Job 1: Checkout code.
- Job 2: Install dependencies (cache them!).
- Job 3: Run Tests (`npm test`).
- Job 4: (Optional) Deploy to staging/prod.

### 3. Platform Specifics
- **Vercel**: Ensure "Root Directory" is set correctly if using a monorepo.
- **Railway/Heroku**: Require a valid `PORT` env variable reference in code.

## Self-Correction Checklist
- "Did I create a `.dockerignore`?" -> Critical to prevent `node_modules` from bloating the build context.
- "Did I expose the right port?" -> Check `EXPOSE 3000` in Dockerfile.
