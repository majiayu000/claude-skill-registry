---
name: budget-lifecycle-rules
description: Garante a integridade das transições de status e hierarquia do Budget.
---

# Regras de Negócio do Orçamento

Sempre que manipular modelos ou controllers de Orçamento (Budget):
1. **Hierarquia Rígida**: Respeite a estrutura `Budget` -> `Service` -> `ServiceItem`.
2. **Sincronia de Status**: Alterações no Orçamento devem disparar atualizações automáticas nos Serviços vinculados.
3. **Imutabilidade**: Bloqueie edições em orçamentos com status `PENDING`.
4. **Regra de Conclusão**: Um Orçamento só pode ser `COMPLETED` se todos os seus Serviços estiverem finalizados.
