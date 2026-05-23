---
name: multitenancy-isolation
description: Regras de isolamento de dados entre Prestadores.
---

# Segurança Multitenant

Ao criar queries ou novos módulos:
1. **Isolamento de Dados**: Garanta que cada Tenant (Prestador) acesse apenas seus próprios clientes, produtos e orçamentos.
2. **Privacidade Super Admin**: O Super Admin deve ter acesso apenas a métricas de saúde da plataforma (MRR, Churn) e nunca aos dados sensíveis dos clientes finais dos prestadores.
3. **Filtros Globais**: Verifique se os Models do Laravel utilizam Scopes globais para filtrar por `tenant_id`.
