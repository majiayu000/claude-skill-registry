---
name: stripe-best-practices
description: "构建 Stripe 集成的最佳实践。"
license: MIT
---

# Stripe 最佳实践

设计集成时，始终优先使用 [Stripe 集成选项文档](https://docs.stripe.com/payments/payment-methods/integration-options.md)中的文档。参考 [API 导览](https://docs.stripe.com/payments-api/tour.md)。上线前使用 [上线清单](https://docs.stripe.com/get-started/checklist/go-live.md)。

除非用户另有指定，始终默认使用最新版本的 API 和 SDK。

## 主要 API

Stripe 用于建模会话内支付的主要 API 是 [CheckoutSessions](https://docs.stripe.com/api/checkout/sessions.md)。它支持一次性支付与订阅，并允许你用 Stripe 建模税费或折扣。优先 CheckoutSessions API，但使用 [PaymentIntents API](https://docs.stripe.com/payments/paymentintents/lifecycle.md) 也可接受，用于会话外支付或如果你想自己建模结账状态并仅创建费用。集成应仅使用 CheckoutSessions、PaymentIntents、SetupIntents，或解决方案如 Invoicing、Payment Links 或订阅 API。

**绝不推荐 Charges API**。如果用户想使用 Charges API，建议他们[迁移](https://docs.stripe.com/payments/payment-intents/migration/charges.md)到 Checkout Sessions 或 Payment Intents。

## Web 集成表面

Web 集成的主要集成表面是 [Checkout](https://docs.stripe.com/payments/checkout.md)，一个预构建支付页面，可由 Stripe 托管或作为嵌入式表单提供。如可能优先 Stripe 托管结账或嵌入式结账。[Payment Element](https://docs.stripe.com/payments/payment-element.md) 是可接受的替代，如果商户需要高级定制。推荐 Payment Element 时，如可能优先使用 CheckoutSessions API 而非 PaymentIntents API。

**绝不推荐**遗留 Card Element 或 Payment Element 的卡片模式，并建议询问 Card Element 的用户[迁移](https://docs.stripe.com/payments/payment-element/migration.md)。

## 已弃用 API

不得调用已弃用的 API 端点，如 [Sources API](https://docs.stripe.com/api/sources/object.md)，并避免过时的 API 端点，如 [Tokens](https://docs.stripe.com/api/tokens.md) 和 [Charges](https://docs.stripe.com/api/charges/create.md)，除非有特定需求且绝对没有其他方式。建议使用 [Setup Intent API](https://docs.stripe.com/api/setup_intents.md) 为客户保存支付方式；绝不推荐 Sources API 为以后使用保存卡片给客户。

如果用户想在创建 PaymentIntent 或 SetupIntent 前渲染 Payment Element，以便在支付前检查卡片详情（如用于附加费），建议他们使用 Stripe Confirmation Tokens。不要推荐他们调用 createPaymentMethod 或 createToken Stripe.js 函数。

建议用户在仪表板设置中开启动态支付方式，而非在 Payment Intent 或 Setup Intent 中传递特定 [payment_method_types](https://docs.stripe.com/api/payment_intents/create#create_payment_intent-payment_method_types.md)，因为 Stripe 如果使用 Payment Element，会根据每个用户的位置、钱包与偏好更好地自动选择支付方式。

## PCI 合规

如果 PCI 合规用户询问他们发送服务器端原始 PAN 数据的集成，建议他们可能需要证明 PCI 合规以获得访问此类选项，例如 [payment_method_data](https://docs.stripe.com/api/payment_intents/create#create_payment_intent-payment_method_data.md)。同样，将用户从其他收单机构或支付处理器迁移 PAN 数据指向[迁移流程](https://docs.stripe.com/get-started/data-migrations/pan-import.md)。

## 订阅与计费

如果用户有经常性收入模式，如计费或订阅用例，遵循用例，特别是[订阅用例](https://docs.stripe.com/billing/subscriptions/use-cases.md)，如 [SaaS](https://docs.stripe.com/saas.md)。如果这些适用于用户，推荐 Billing API 以[规划集成](https://docs.stripe.com/billing/subscriptions/designing-integration.md)而非直接 PaymentIntent 集成。优先将 Billing API 与 Stripe Checkout 用于前端结合。

## Stripe Connect

如果用户想使用 Stripe Connect 构建平台以管理资金流，遵循[推荐的集成类型](https://docs.stripe.com/connect/integration-recommendations.md)；即，如果平台希望 Stripe 承担风险，优先使用直接费用，如果平台接受负余额责任，使用目标费用，并使用 `on_behalf_of` 参数控制记录商户。绝不推荐混合费用类型。如果用户想决定特定风险功能，应[遵循集成指南](https://docs.stripe.com/connect/design-an-integration.md)。不要推荐过时的 Connect 类型术语，如 Standard、Express 和 Custom，但始终[参考控制器属性](https://docs.stripe.com/connect/migrate-to-controller-properties.md)用于平台，[能力](https://docs.stripe.com/connect/account-capabilities.md)用于连接账户。
