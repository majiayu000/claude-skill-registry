# 🚀 Skill: GitHub Actions CI/CD

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-github-actions` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `github-actions`, `ci`, `cd`, `pipeline`, `automation`, `workflow` |
| **Referencia** | [GitHub Actions Docs](https://docs.github.com/en/actions) |

## 🔑 Keywords para Invocación

- `github-actions`
- `ci`
- `cd`
- `pipeline`
- `workflow`
- `automation`
- `@skill:github-actions`

### Ejemplos de Prompts

```
Configura CI/CD con GitHub Actions para Flutter
```

```
Crea workflow de testing y deployment automatizado
```

```
@skill:github-actions - Pipeline completo para monorepo
```

## 📖 Descripción

GitHub Actions proporciona CI/CD nativo de GitHub para automatizar testing, building y deployment de aplicaciones Flutter y sus backends en un monorepo. Incluye workflows para frontend (Flutter) y backend (Node.js, Python, Go, etc.).

### ✅ Cuándo Usar Este Skill

- Proyecto alojado en GitHub
- Necesitas CI/CD integrado nativamente
- Pipelines simples a medianos
- Free tier generoso (2000 min/mes)
- Monorepo con frontend Flutter + Backend

### ❌ Cuándo NO Usar Este Skill

- Proyecto en GitLab/Bitbucket
- Necesitas runners on-premise complejos
- Preferencia por otras herramientas CI/CD

## 🏗️ Estructura de Monorepo

```
my-app-monorepo/
├── .github/
│   └── workflows/
│       ├── flutter-ci.yml
│       ├── flutter-cd.yml
│       ├── backend-ci.yml
│       ├── backend-cd.yml
│       └── monorepo-pr.yml
├── mobile/                    # Flutter app
│   ├── lib/
│   ├── test/
│   └── pubspec.yaml
├── backend/                   # Backend (Node.js/Python/Go)
│   ├── src/
│   ├── tests/
│   └── package.json
├── infrastructure/            # IaC (Terraform/etc)
└── shared/                    # Shared code/protos
```

## 💻 Implementación

### 1. Flutter CI Workflow

```yaml
# .github/workflows/flutter-ci.yml
name: Flutter CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'mobile/**'
      - '.github/workflows/flutter-ci.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'mobile/**'

jobs:
  analyze:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: mobile

    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'
          cache: true

      - name: Get dependencies
        run: flutter pub get

      - name: Verify formatting
        run: dart format --output=none --set-exit-if-changed .

      - name: Analyze code
        run: flutter analyze --fatal-infos

      - name: Run custom lints
        run: dart run custom_lint

  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: mobile

    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'
          cache: true

      - name: Get dependencies
        run: flutter pub get

      - name: Run tests with coverage
        run: flutter test --coverage --reporter expanded

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./mobile/coverage/lcov.info
          flags: flutter
          name: flutter-coverage

  build-android:
    needs: [analyze, test]
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: mobile

    steps:
      - uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'
          cache: 'gradle'

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'
          cache: true

      - name: Get dependencies
        run: flutter pub get

      - name: Build APK
        run: flutter build apk --release

      - name: Build App Bundle
        run: flutter build appbundle --release

      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: android-apk
          path: mobile/build/app/outputs/flutter-apk/app-release.apk
          retention-days: 7

      - name: Upload AAB artifact
        uses: actions/upload-artifact@v4
        with:
          name: android-aab
          path: mobile/build/app/outputs/bundle/release/app-release.aab
          retention-days: 7

  build-ios:
    needs: [analyze, test]
    runs-on: macos-latest
    defaults:
      run:
        working-directory: mobile

    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'
          cache: true

      - name: Get dependencies
        run: flutter pub get

      - name: Build iOS (no codesign)
        run: flutter build ios --release --no-codesign

      - name: Upload iOS build
        uses: actions/upload-artifact@v4
        with:
          name: ios-build
          path: mobile/build/ios/iphoneos/
          retention-days: 7
```

### 2. Backend CI Workflow (Node.js Example)

```yaml
# .github/workflows/backend-ci.yml
name: Backend CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
      - '.github/workflows/backend-ci.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'backend/**'

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
          cache-dependency-path: backend/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Lint code
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage/lcov.info
          flags: backend
          name: backend-coverage

  docker-build:
    needs: lint-and-test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: false
          tags: myapp-backend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 3. Monorepo PR Checks

```yaml
# .github/workflows/monorepo-pr.yml
name: Monorepo PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      mobile: ${{ steps.filter.outputs.mobile }}
      backend: ${{ steps.filter.outputs.backend }}
      infrastructure: ${{ steps.filter.outputs.infrastructure }}

    steps:
      - uses: actions/checkout@v4

      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            mobile:
              - 'mobile/**'
            backend:
              - 'backend/**'
            infrastructure:
              - 'infrastructure/**'

  mobile-checks:
    needs: detect-changes
    if: needs.detect-changes.outputs.mobile == 'true'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          cache: true

      - name: Run mobile checks
        working-directory: mobile
        run: |
          flutter pub get
          flutter analyze
          flutter test

  backend-checks:
    needs: detect-changes
    if: needs.detect-changes.outputs.backend == 'true'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'
          cache: 'npm'
          cache-dependency-path: backend/package-lock.json

      - name: Run backend checks
        working-directory: backend
        run: |
          npm ci
          npm run lint
          npm test

  infrastructure-checks:
    needs: detect-changes
    if: needs.detect-changes.outputs.infrastructure == 'true'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0

      - name: Terraform Format
        working-directory: infrastructure
        run: terraform fmt -check

      - name: Terraform Validate
        working-directory: infrastructure
        run: |
          terraform init -backend=false
          terraform validate
```

### 4. Flutter CD Workflow

```yaml
# .github/workflows/flutter-cd.yml
name: Flutter CD

on:
  push:
    tags:
      - 'mobile-v*.*.*'

jobs:
  deploy-android:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'

      - name: Decode keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
        run: |
          echo "$KEYSTORE_BASE64" | base64 -d > android/app/keystore.jks
        working-directory: mobile

      - name: Create key.properties
        env:
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        run: |
          cat <<EOF > android/key.properties
          storePassword=$KEYSTORE_PASSWORD
          keyPassword=$KEY_PASSWORD
          keyAlias=$KEY_ALIAS
          storeFile=keystore.jks
          EOF
        working-directory: mobile

      - name: Get dependencies
        run: flutter pub get
        working-directory: mobile

      - name: Build App Bundle
        run: flutter build appbundle --release
        working-directory: mobile

      - name: Setup Play Store credentials
        env:
          PLAY_STORE_CREDENTIALS: ${{ secrets.PLAY_STORE_CREDENTIALS }}
        run: echo "$PLAY_STORE_CREDENTIALS" > play-store-credentials.json

      - name: Deploy to Play Store
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJson: play-store-credentials.json
          packageName: com.example.myapp
          releaseFiles: mobile/build/app/outputs/bundle/release/app-release.aab
          track: production
          status: completed

  deploy-ios:
    runs-on: macos-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'

      - name: Get dependencies
        run: flutter pub get
        working-directory: mobile

      - name: Install CocoaPods
        run: gem install cocoapods

      - name: Build iOS IPA
        run: flutter build ipa --release
        working-directory: mobile

      - name: Upload to TestFlight
        uses: apple-actions/upload-testflight-build@v1
        with:
          app-path: mobile/build/ios/ipa/*.ipa
          issuer-id: ${{ secrets.APP_STORE_ISSUER_ID }}
          api-key-id: ${{ secrets.APP_STORE_API_KEY_ID }}
          api-private-key: ${{ secrets.APP_STORE_API_PRIVATE_KEY }}
```

### 5. Backend CD Workflow

```yaml
# .github/workflows/backend-cd.yml
name: Backend CD

on:
  push:
    tags:
      - 'backend-v*.*.*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract version from tag
        id: version
        run: echo "version=${GITHUB_REF#refs/tags/backend-v}" >> $GITHUB_OUTPUT

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: |
            myorg/myapp-backend:${{ steps.version.outputs.version }}
            myorg/myapp-backend:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to Kubernetes (via kubectl)
        env:
          KUBECONFIG_CONTENT: ${{ secrets.KUBECONFIG }}
        run: |
          echo "$KUBECONFIG_CONTENT" > kubeconfig.yaml
          export KUBECONFIG=kubeconfig.yaml
          kubectl set image deployment/myapp-backend \
            myapp-backend=myorg/myapp-backend:${{ steps.version.outputs.version }} \
            -n production
          kubectl rollout status deployment/myapp-backend -n production
```

### 6. Reusable Workflows

```yaml
# .github/workflows/reusable-flutter-test.yml
name: Reusable Flutter Test

on:
  workflow_call:
    inputs:
      working-directory:
        required: true
        type: string
      flutter-version:
        required: false
        type: string
        default: '3.35.0'

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ${{ inputs.working-directory }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ inputs.flutter-version }}
          cache: true

      - name: Get dependencies
        run: flutter pub get

      - name: Run tests
        run: flutter test --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ${{ inputs.working-directory }}/coverage/lcov.info
```

## 🔐 Secrets Configuration

Configurar en: **Settings > Secrets and variables > Actions**

### Flutter/Mobile Secrets

```
KEYSTORE_BASE64              # Android keystore en base64
KEYSTORE_PASSWORD            # Password del keystore
KEY_ALIAS                    # Alias de la key
KEY_PASSWORD                 # Password de la key
PLAY_STORE_CREDENTIALS       # JSON credentials de Play Store
APP_STORE_ISSUER_ID         # App Store Connect issuer ID
APP_STORE_API_KEY_ID        # App Store Connect API key ID
APP_STORE_API_PRIVATE_KEY   # App Store Connect private key
```

### Backend/Infrastructure Secrets

```
DOCKER_USERNAME              # Docker Hub username
DOCKER_PASSWORD              # Docker Hub password
KUBECONFIG                   # Kubernetes config
AWS_ACCESS_KEY_ID           # AWS credentials (si usas AWS)
AWS_SECRET_ACCESS_KEY       # AWS secret key
```

### General Secrets

```
CODECOV_TOKEN               # Token de Codecov
SLACK_WEBHOOK_URL           # Webhook para notificaciones
```

## 🎯 Mejores Prácticas

### 1. Path Filtering

```yaml
# Solo ejecutar cuando cambien archivos específicos
on:
  push:
    paths:
      - 'mobile/**'
      - '.github/workflows/flutter-ci.yml'
```

### 2. Caching

```yaml
# Cache de dependencias Flutter
- uses: subosito/flutter-action@v2
  with:
    flutter-version: '3.35.0'
    cache: true

# Cache de Gradle (Android)
- uses: actions/setup-java@v4
  with:
    cache: 'gradle'

# Cache de npm (Backend)
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
```

### 3. Matrix Strategy

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node-version: [18.x, 20.x]
```

### 4. Environments

```yaml
jobs:
  deploy:
    environment: production  # Requiere approval
    runs-on: ubuntu-latest
```

### 5. Concurrency Control

```yaml
# Cancelar runs anteriores del mismo PR
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## 📊 Status Badges

```markdown
![Flutter CI](https://github.com/org/repo/workflows/Flutter%20CI/badge.svg)
![Backend CI](https://github.com/org/repo/workflows/Backend%20CI/badge.svg)
[![codecov](https://codecov.io/gh/org/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/org/repo)
```

## 🚀 Comandos Útiles

```bash
# Crear tag para release de mobile
git tag -a mobile-v1.0.0 -m "Mobile release 1.0.0"
git push origin mobile-v1.0.0

# Crear tag para release de backend
git tag -a backend-v1.0.0 -m "Backend release 1.0.0"
git push origin backend-v1.0.0

# Ver workflows con GitHub CLI
gh run list

# Ver logs de workflow específico
gh run view <run-id> --log

# Re-run failed workflow
gh run rerun <run-id>

# Trigger workflow manual
gh workflow run flutter-ci.yml
```

## 📚 Recursos Adicionales

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flutter CI/CD Best Practices](https://docs.flutter.dev/deployment/cd)
- [Monorepo Workflows](https://github.com/actions/toolkit/blob/main/docs/action-versioning.md)

## 🔗 Skills Relacionados

- [Terraform](../terraform/SKILL.md) - Infrastructure as Code
- [ArgoCD](../argocd/SKILL.md) - GitOps deployment
- [AWS](../aws/SKILL.md) - AWS deployment
- [Docker](../docker/SKILL.md) - Containerization

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
