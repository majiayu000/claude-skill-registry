---
name: cras-finder
description: Encontrar CRAS próximos por CEP ou GPS
---

## Função
Localiza CRAS mais próximos por CEP ou GPS.

## Tool do Agente
backend/app/agent/tools/buscar_cras.py

## MCP
GoogleMapsMCP (Places API)

## API
GET /api/v1/nearby/cras?lat=-23.55&lng=-46.63&limit=5
