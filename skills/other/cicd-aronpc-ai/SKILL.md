---
name: cicd
description: >-
  Configura CI/CD com GitHub Actions, Docker e deploy automatizado. Use quando precisar criar pipelines de CI/CD, configurar Docker, ou automatizar deploys de projetos Laravel.
compatibility: GitHub Actions, Docker, Laravel 11+
metadata:
  author: aronpc
  version: 1.0.0
  category: devops
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# cicd

## Resumo
Configura CI/CD com GitHub Actions para Laravel incluindo build Docker e deploy automatizado.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `workflow` | Para integrar com branches e commits |
| `qa` | Para pipelines de qualidade |
| `testing` | Para pipelines de teste |
| `docs` | Para atualizar docs pós-deploy |

## Quando usar

Use esta skill sempre que:
- Configurar CI/CD para projetos Laravel
- Automatizar builds
- Configurar deploy automático
- Criar workflows de teste
- Configurar multi-arch Docker builds

## Workflows

| Workflow | Trigger | Função |
|----------|---------|---------|
| `build-docker.yml` | Push para main/develop | Build + push imagens Docker |
| `trigger-deploy.yml` | Após build sucesso | Webhook para Coolify |

## Workflow de Build Docker

### Trigger

```yaml
on:
  push:
    branches:
      - main
      - develop
```

### Passos

1. **Checkout** - Código fonte
2. **Setup Bun** - Gerenciador de pacotes JS
3. **Setup PHP 8.5** - Runtime PHP
4. **Composer install** - Dependências PHP (no-dev)
5. **Build frontend** - Assets React/Inertia
6. **Build Filament** - Assets admin
7. **Docker buildx** - Multi-arch builds
8. **Push GHCR** - Registro container

### Setup de Ambiente

```yaml
- name: Install NPM/Bun
  uses: oven-sh/setup-bun@v2

- name: Install PHP & Composer
  uses: shivammathur/setup-php@v2
  with:
    php-version: '8.5'
    extensions: mbstring, dom, fileinfo, pdo, pdo_mysql
```

### Build de Assets

```yaml
- name: Install Composer Dependencies
  run: composer install --no-dev --no-interaction --prefer-dist --optimize-autoloader

- name: Build Frontend Assets
  run: |
    bun install
    bun run build
    bun run build:ssr

- name: Build Filament Assets
  run: |
    php artisan filament:assets
    php artisan filament:upgrade --no-interaction
    php artisan view:clear
```

## Docker Buildx com Cache

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
  with:
    driver: docker-container

- name: Cache Docker Layers
  uses: actions/cache@v5
  with:
    path: /tmp/.buildx-cache
    key: docker-${{ runner.os }}-${{ github.ref_name }}-${{ github.sha }}
    restore-keys: |
      docker-${{ runner.os }}-${{ github.ref_name }}-
      docker-${{ runner.os }}-main-
```

## Build de Multi-Imagem

```yaml
- name: Build & Push FrankenPHP Image (App)
  uses: docker/build-push-action@v6
  with:
    push: true
    context: .
    file: ./docker/frankenphp/Dockerfile
    cache-from: type=local,src=/tmp/.buildx-cache
    cache-to: type=local,dest=/tmp/.buildx-cache-new,mode=max
    tags: |
      ghcr.io/${{ github.repository }}-frankenphp:${{ github.ref_name }}

- name: Build & Push FPM/Nginx Image (Workers/Tasks)
  uses: docker/build-push-action@v6
  with:
    push: true
    context: .
    file: ./docker/php/Dockerfile
    target: ci
    tags: |
      ghcr.io/${{ github.repository }}:${{ github.ref_name }}
```

## Estratégia de Tags

```yaml
tags: |
  ghcr.io/${{ github.repository }}-frankenphp:${{ github.ref_name }}

# Latest apenas para main
- name: Push Latest FrankenPHP
  if: github.ref_name == 'main'
  uses: docker/build-push-action@v6
  with:
    tags: |
      ghcr.io/${{ github.repository }}-frankenphp:latest
```

## Workflow de Trigger Deploy

```yaml
name: Trigger Deploy

on:
  workflow_run:
    workflows: ["Docker Build"]
    types: [completed]
    branches: [main, develop]

jobs:
  trigger-webhook:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - name: Trigger Deploy Webhook
        uses: fjogeleit/http-request-action@v1
        with:
          url: ${{ vars.DEPLOY_WEBHOOK_URL }}
          method: GET
```

## Secrets Requeridos

| Secret | Uso |
|--------|-----|
| `GHCR_PAT` | Token para push imagens |
| `DEPLOY_WEBHOOK_URL` | URL webhook Coolify |

## Estratégia de Branch

| Branch | Tag | Deploy |
|--------|-----|--------|
| `main` | `latest`, `main` | Produção |
| `develop` | `develop` | Staging |

## Solução de Problemas

### Cache não funcionando

Verifique se o cache move está no final:

```yaml
- name: Move Cache
  run: |
    rm -rf /tmp/.buildx-cache
    mv /tmp/.buildx-cache-new /tmp/.buildx-cache
```

### Build falhando

```bash
# Testar build localmente
docker buildx build \
  -f docker/frankenphp/Dockerfile \
  --platform linux/amd64,linux/arm64 \
  -t test-image .
```

### Deploy não triggerando

Verifique:
1. `build-docker.yml` completou com sucesso
2. `trigger-deploy.yml` tem trigger correto
3. `DEPLOY_WEBHOOK_URL` está configurada

## Exemplos de Workflows Completos

### Build Docker Workflow Completo

```yaml
name: Docker Build

on:
  push:
    branches:
      - main
      - develop

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: docker-container

      - name: Cache Docker Layers
        uses: actions/cache@v5
        with:
          path: /tmp/.buildx-cache
          key: docker-${{ runner.os }}-${{ github.ref_name }}-${{ github.sha }}
          restore-keys: |
            docker-${{ runner.os }}-${{ github.ref_name }}-
            docker-${{ runner.os }}-main-

      - name: Install NPM/Bun
        uses: oven-sh/setup-bun@v2

      - name: Install PHP & Composer
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.5'
          extensions: mbstring, dom, fileinfo, pdo, pdo_mysql

      - name: Install Composer Dependencies
        run: composer install --no-dev --no-interaction --prefer-dist --optimize-autoloader

      - name: Build Frontend Assets
        run: |
          bun install
          bun run build
          bun run build:ssr

      - name: Build Filament Assets
        run: |
          php artisan filament:assets
          php artisan filament:upgrade --no-interaction
          php artisan view:clear

      - name: Build & Push FrankenPHP Image
        uses: docker/build-push-action@v6
        with:
          push: true
          context: .
          file: ./docker/frankenphp/Dockerfile
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache-new,mode=max
          tags: |
            ghcr.io/${{ github.repository }}-frankenphp:${{ github.ref_name }}

      - name: Move Cache
        run: |
          rm -rf /tmp/.buildx-cache
          mv /tmp/.buildx-cache-new /tmp/.buildx-cache

      - name: Push Latest Tag
        if: github.ref_name == 'main'
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: |
            ghcr.io/${{ github.repository }}-frankenphp:latest
```

### Trigger Deploy Workflow Completo

```yaml
name: Trigger Deploy

on:
  workflow_run:
    workflows: ["Docker Build"]
    types: [completed]
    branches: [main, develop]

jobs:
  trigger-webhook:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    steps:
      - name: Trigger Deploy Webhook
        uses: fjogeleit/http-request-action@v1
        with:
          url: ${{ vars.DEPLOY_WEBHOOK_URL }}
          method: GET
```

## Melhores Práticas

### ✅ FAÇA

- Use cache Docker para builds mais rápidos
- Use multi-arch builds para compatibilidade
- Separe builds de app e workers
- Use tags específicos por branch
- Configure webhooks para deploy automático
- Monitore status dos workflows
- Use secrets para dados sensíveis
- Mantenha workflows documentados

### ❌ NÃO FAÇA

- Não hardcode credenciais nos workflows
- Não use builds sem cache
- Não skip testes antes do build
- Não push imagens sem tags
- Não use branches instáveis para produção
- Não ignore falhas de build

## Checklist de Configuração

Antes de usar CI/CD em produção:

- [ ] GitHub Actions configurado
- [ ] Secrets configurados (GHCR_PAT, DEPLOY_WEBHOOK_URL)
- [ ] Workflows testados localmente
- [ ] Multi-arch builds funcionando
- [ ] Cache Docker configurado
- [ ] Webhooks configurados
- [ ] Deploy automático testado
- [ ] Rollback planejado

## Referências

- [GitHub Actions Documentation](https://docs.github.com/en/actions) - Documentação oficial
- [Docker Build Push Action](https://github.com/docker/build-push-action) - Action oficial
