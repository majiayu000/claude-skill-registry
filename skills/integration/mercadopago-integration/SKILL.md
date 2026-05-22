---
name: mercadopago-infrastructure
description: Padroniza o uso do MercadoPagoService agnóstico.
---

# Padrão de Integração Financeira

Ao implementar fluxos de pagamento:
1. **MercadoPagoService**: Use sempre a camada de infraestrutura agnóstica para gerar preferências e webhooks.
2. **Separação de Credenciais**:
   - **Assinaturas**: Use as credenciais da Plataforma (SaaS).
   - **Faturas (Invoices)**: Use as credenciais do Prestador (Provider) via `PaymentMercadoPagoInvoiceService`.
3. **Webhooks**: Garanta que o sistema trate o retorno da API para atualizar o status financeiro automaticamente.
