---
name: farmacia-finder
description: Encontrar Farmácias Populares próximas
---

## Função
Localiza farmácias credenciadas no Farmácia Popular.

## Tool do Agente
backend/app/agent/tools/buscar_farmacia.py

## MCP
GoogleMapsMCP (Places API)

## API
GET /api/v1/nearby/farmacias?lat=-23.55&lng=-46.63&program=farmacia_popular
