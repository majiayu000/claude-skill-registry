---
name: "EasyPanel DevOps"
description: "Experto en Dockerización, Docker Compose y despliegue en EasyPanel."
trigger: "Cuando toque Dockerfile, docker-compose.yml o variables de entorno."
scope: "DEVOPS"
auto-invoke: true
---

# Protocolo de Despliegue EasyPanel

1. **Gestión de Puertos:**
   - El `orchestrator` SIEMPRE escucha en `8000` (interno).
   - El frontend escucha en `80` (dentro de Nginx).
   - Si cambias un puerto en `Dockerfile`, avisa para actualizar la config en EasyPanel.

2. **Persistencia (Volúmenes):**
   - Si agregas una funcionalidad que guarda archivos (ej. `uploads/`), asegúrate de que la ruta esté mapeada en los volúmenes persistentes de EasyPanel, o se perderán en el próximo deploy.

3. **Variables de Entorno (Build vs Runtime):**
   - `VITE_` variables se inyectan en **BUILD TIME**. Si las cambias, hay que reconstruir la imagen.
   - Variables de Backend (Python) son **RUNTIME**. Solo requieren reinicio.
