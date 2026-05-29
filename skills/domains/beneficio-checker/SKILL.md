---
name: beneficio-checker
description: Consultar benefícios sociais por CPF (Bolsa Família, BPC, CadÚnico)
---

## Função
Consulta benefícios sociais por CPF (Bolsa Família, BPC, CadÚnico).

## Tool do Agente
backend/app/agent/tools/consultar_beneficio.py

## API
POST /api/v1/agent/v2/chat
Body: {"message": "consultar benefício CPF 123.456.789-00"}

## Tabela
beneficiarios (cpf_hash, bf_ativo, bpc_ativo, cadunico_ativo)
