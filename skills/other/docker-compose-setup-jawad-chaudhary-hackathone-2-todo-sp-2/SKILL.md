---
name: docker-compose-setup
description: Setup docker-compose for Todo app services. Use for local dev environment.
---
# DockerComposeSetup Instructions
Input: Services (frontend, backend, db).
Output: YAML config.
Steps:
1. Define services with builds and ports.
Example YAML:
version: '3'
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://user:pass@neon-host/db