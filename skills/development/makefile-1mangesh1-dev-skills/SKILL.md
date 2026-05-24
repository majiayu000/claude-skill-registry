---
name: makefile
description: Makefile patterns for project automation and build tasks. Use when user asks to "create Makefile", "add make target", "automate with make", "build commands", or set up project automation with GNU Make.
---

# Makefile

Project automation with GNU Make.

## Basic Structure

```makefile
# Variables
APP_NAME := myapp
VERSION := 1.0.0

# Default target (first target)
.DEFAULT_GOAL := help

# Phony targets (not files)
.PHONY: help build run test clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build the application
	go build -o bin/$(APP_NAME) ./cmd/$(APP_NAME)

run: ## Run the application
	go run ./cmd/$(APP_NAME)

test: ## Run tests
	go test -v ./...

clean: ## Clean build artifacts
	rm -rf bin/ dist/
```

## Common Patterns

### Development Workflow

```makefile
.PHONY: dev build test lint format

dev: ## Start development server
	npm run dev

build: ## Build for production
	npm run build

test: ## Run tests
	npm test

lint: ## Run linter
	npm run lint

format: ## Format code
	npm run format

check: lint test ## Run all checks
```

### Docker Targets

```makefile
IMAGE_NAME := myapp
IMAGE_TAG := latest

.PHONY: docker-build docker-run docker-push

docker-build: ## Build Docker image
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run: ## Run Docker container
	docker run -p 8080:8080 $(IMAGE_NAME):$(IMAGE_TAG)

docker-push: ## Push to registry
	docker push $(IMAGE_NAME):$(IMAGE_TAG)
```

### Database Tasks

```makefile
.PHONY: db-up db-down db-migrate db-seed

db-up: ## Start database
	docker compose up -d db

db-down: ## Stop database
	docker compose down

db-migrate: ## Run migrations
	npx prisma migrate dev

db-seed: ## Seed database
	npx prisma db seed
```

### Environment Setup

```makefile
.PHONY: setup install deps

setup: install deps ## Full setup
	@echo "Setup complete!"

install: ## Install tools
	brew install go node

deps: ## Install dependencies
	go mod download
	npm install
```

## Variables

```makefile
# Simple assignment
CC := gcc

# Recursive (evaluated when used)
FILES = $(shell find . -name "*.go")

# Conditional
DEBUG ?= 0
ifeq ($(DEBUG), 1)
    CFLAGS += -g
endif

# Environment
export NODE_ENV := production
```

## Dependencies

```makefile
# Target depends on prerequisites
build: src/main.go src/utils.go
	go build -o app $^

# Pattern rules
%.o: %.c
	$(CC) -c $< -o $@

# Order-only (directory creation)
build: | bin
	go build -o bin/app

bin:
	mkdir -p bin
```

## Conditionals

```makefile
OS := $(shell uname -s)

ifeq ($(OS), Darwin)
    OPEN := open
else
    OPEN := xdg-open
endif

docs: ## Open documentation
	$(OPEN) docs/index.html
```

## Useful Recipes

### Include Other Files

```makefile
-include .env
include scripts/docker.mk
```

### Silent Execution

```makefile
install:
	@echo "Installing..."
	@npm install
```

### Multi-line Commands

```makefile
deploy:
	@echo "Deploying..." && \
	npm run build && \
	aws s3 sync dist/ s3://bucket/
```

### Run with Args

```bash
# make run ARGS="--port 3000"
```

```makefile
run:
	node server.js $(ARGS)
```

## Project Template

```makefile
.DEFAULT_GOAL := help
SHELL := /bin/bash

# ============================================
# Variables
# ============================================
APP_NAME := myapp
VERSION := $(shell git describe --tags --always)

# ============================================
# Development
# ============================================
.PHONY: dev build test lint

dev: ## Start dev server
	npm run dev

build: ## Build project
	npm run build

test: ## Run tests
	npm test

lint: ## Run linter
	npm run lint

# ============================================
# Docker
# ============================================
.PHONY: docker-build docker-up docker-down

docker-build: ## Build image
	docker build -t $(APP_NAME):$(VERSION) .

docker-up: ## Start services
	docker compose up -d

docker-down: ## Stop services
	docker compose down

# ============================================
# Utilities
# ============================================
.PHONY: clean help

clean: ## Clean artifacts
	rm -rf dist/ node_modules/

help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
```
