---
name: brazilian-data-utils
description: Skill para gerar e validar dados brasileiros (CPF/CNPJ) no Easy Budget.
---

# Utilitários de Dados Brasileiros

Esta skill deve ser usada sempre que o desenvolvedor precisar testar o cadastro de Clientes (Pessoa Física ou Jurídica) ou a lógica de DTOs que envolvem documentos.

## Regras de Geração:
- Gerar CPFs matematicamente válidos via algoritmo de Módulo 11.
- Sempre oferecer a versão "apenas números" e a versão "formatada".
- **Contexto de Negócio:** Se o usuário pedir um 'Customer PF', use esta skill para preencher o campo `document` no `ProviderDTO` ou `CustomerDTO`.

## Regras de Validação:
- Ao analisar códigos de validação, verifique se a lógica de pesos (10 a 2 e 11 a 2) está correta para evitar erros de persistência.
