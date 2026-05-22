---
name: shopline-payments
description: >
  USE WHEN: 用戶詢問 SHOPLINE Payments 金流串接、導轉式付款流程、建立結帳交易（sessionUrl）、
  returnUrl 回跳處理、Webhook 簽章驗證、交易查詢、退款/請款/取消操作，
  或整合 LINE Pay、信用卡、ATM、街口支付（JKO）等台灣在地付款方式。
  DO NOT USE WHEN: 詢問其他金流服務（如綠界 ECPay、藍新 NewebPay、TapPay）、
  非台灣地區金流、或 SHOPLINE 電商平台非金流相關功能。
argument-hint: "[feature: checkout/query/refund/capture/cancel/webhook]"
user-invocable: true
metadata:
  author: Clancy Lin
  version: 1.1.0
  documentation: https://docs.shoplinepayments.com/
  last-verified: 2026-02-01
---

# SHOPLINE Payments 金流串接指南

此技能提供 SHOPLINE Payments 金流串接的完整文檔與程式碼範例。

## 概述

SHOPLINE Payments 提供兩種串接方式：

| 串接方式 | 說明 | 適用場景 |
|---------|------|---------|
| **導轉式** | 透過 API 取得付款頁 URL，導轉顧客至 SHOPLINE 付款頁 | 串接簡單，適合快速整合 |
| **內嵌式** | 透過 SDK + API 將付款表單內嵌於特店網站（詳見 [`references/embedded.md`](references/embedded.md)） | 支援綁卡/快捷/定期交易等進階功能 |

## 環境設定

### 環境 URL

| 環境 | Base URL |
|------|----------|
| 沙盒環境 | `https://api-sandbox.shoplinepayments.com` |
| 正式環境 | `https://api.shoplinepayments.com` |

### 必要金鑰

| 金鑰 | 用途 |
|-----|------|
| `merchantId` | 特店 ID |
| `apiKey` | Server API 串接認證 |
| `clientKey` | SDK 串接認證（內嵌式使用） |
| `signKey` | Webhook Event 通知簽章驗證 |

## 文檔結構

根據用戶需求，參考以下文檔：

| 需求 | 文檔 | 說明 |
|------|------|------|
| 建立結帳交易 | [`references/redirect.md`](references/redirect.md) | 導轉式結帳交易 API |
| **內嵌式串接** | [`references/embedded.md`](references/embedded.md) | **SDK + API 內嵌式串接指南** |
| 查詢交易 | [`references/query.md`](references/query.md) | 查詢結帳/付款交易狀態 |
| 退款 | [`references/refund.md`](references/refund.md) | 建立退款交易 |
| 請款/取消 | [`references/capture-cancel.md`](references/capture-cancel.md) | 信用卡請款與取消授權 |
| Webhook | [`references/webhook.md`](references/webhook.md) | 事件通知與簽章驗證 |
| 錯誤碼 | [`references/error-codes.md`](references/error-codes.md) | 錯誤碼完整參考 |
| 沙盒測試 | [`references/sandbox.md`](references/sandbox.md) | 測試卡號與測試規則 |
| 付款方式 | [`references/payment-methods.md`](references/payment-methods.md) | 支援的付款方式說明 |

## 工作流程

### 導轉式串接流程（本專案主要使用）

```
1. 特店後端呼叫「建立結帳交易」API
2. 取得 sessionUrl
3. 前端導轉顧客至 sessionUrl（SHOPLINE 付款頁）
4. 顧客完成付款後自動導回 returnUrl
5. 特店透過 Webhook 接收付款結果
6. （建議）主動查詢交易狀態二次確認
```

### 內嵌式串接流程

```
1. 前端引入 JS SDK（NPM 或 CDN）
2. 初始化 SDK 並呈現收銀台
3. 顧客填寫付款資訊並點擊結帳
4. SDK 建立 paySession
5. 後端呼叫「建立付款交易」API（帶入 paySession）
6. 前端呼叫 payment.pay(nextAction) 發起付款
7. 完成 3D 驗證（如需要）後導回 returnUrl
8. 透過 Webhook 接收付款結果
```

> 完整內嵌式串接說明請參考 [`references/embedded.md`](references/embedded.md)

### API 認證機制

所有 Server-API 請求必須包含以下 HTTP Header：

```
Content-Type: application/json
merchantId: <YOUR-MERCHANT-ID>
apiKey: <YOUR-API-KEY>
requestId: <UNIQUE-REQUEST-ID>
```

> **補充**：若為平台特店（Platform Connect）請另外帶入 `platformId`；建議在「建立結帳交易」等具冪等需求的請求帶入 `idempotentKey`，避免重複下單。

## 快速範例

### JavaScript - 建立結帳交易

```javascript
async function createCheckoutSession(orderData) {
  const response = await fetch('https://api-sandbox.shoplinepayments.com/api/v1/trade/sessions/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'merchantId': process.env.SHOPLINE_MERCHANT_ID,
      'apiKey': process.env.SHOPLINE_API_KEY,
      'requestId': Date.now().toString()
    },
    body: JSON.stringify({
      referenceId: orderData.orderId,
      amount: { value: orderData.amount * 100, currency: 'TWD' },
      returnUrl: orderData.returnUrl,
      mode: 'regular',
      allowPaymentMethodList: ['CreditCard', 'LinePay'],
      customer: {
        personalInfo: {
          firstName: orderData.name,
          email: orderData.email,
          phone: orderData.phone
        }
      },
      client: { ip: orderData.clientIp }
    })
  });
  return await response.json();
}
```

## 程式碼範例

完整的程式碼範例請參考：

- [`scripts/checkout.js`](scripts/checkout.js) - Node.js 建立結帳交易
- [`scripts/webhook.js`](scripts/webhook.js) - Webhook 簽章驗證
- [`scripts/gas-integration.js`](scripts/gas-integration.js) - Google Apps Script 整合

## 重要注意事項

1. **金額格式**：台幣金額需 × 100（如 100 元傳入 10000）
2. **訂單號唯一**：`referenceId` 不可重複
3. **HTTPS 必須**：所有 API 請求必須使用 HTTPS
4. **金鑰保密**：`apiKey` 和 `signKey` 不可暴露在前端
5. **退款時效**：付款交易可退款時效為 180 天
6. **取消授權**：只能在請款前取消，請款後只能退款

## Troubleshooting

### 金額格式錯誤 (Error 1004)

**問題**：收到 `1004 Param error`
**原因**：金額未轉換為「分」
**解決**：`amount.value = 實際金額 * 100`（如 100 元傳 10000）

### 重複訂單號 (Error 1001)

**問題**：收到 `1001 Order exist`
**原因**：`referenceId` 已被使用
**解決**：確保每筆訂單使用唯一的 `referenceId`

### API 認證失敗 (Error ACCESS_DENIED)

**問題**：收到 `ACCESS_DENIED`
**原因**：
1. `apiKey` 或 `merchantId` 錯誤
2. 使用沙盒金鑰呼叫正式環境（或反之）
**解決**：確認金鑰正確且環境對應

### Webhook 收不到通知

**問題**：付款完成後未收到 Webhook
**原因**：
1. Webhook URL 未設定（需聯繫 SLP 窗口申請）
2. URL 非 HTTPS
3. 伺服器防火牆阻擋
4. 回應非 HTTP 200
**解決**：確認 URL 可公開存取並回應 200

### Webhook 簽章驗證失敗

**問題**：簽章比對不符
**原因**：
1. `signKey` 錯誤
2. payload 組合方式錯誤（應為 `timestamp.bodyString`）
3. body 被解析後重新序列化導致格式改變
**解決**：使用原始 body 字串進行簽章計算

### 沙盒測試一直失敗

**問題**：測試交易都失敗
**原因**：金額不符合測試規則
**解決**：
- 非 3D 交易：金額去掉 00 後為**奇數**才會成功（如 101, 501）
- 3D 交易：金額為 3 的倍數進入 3D 流程（如 300, 600）

### 退款失敗 (Error 1014/4701)

**問題**：收到「無可退款金額」或「退款金額超過可退金額」
**原因**：
1. 已全額退款
2. 退款金額超過原交易可退金額
**解決**：查詢原交易確認可退款金額

### 取消授權失敗 (Error 6002)

**問題**：收到「交易已請款，無法取消」
**原因**：已請款的交易無法取消授權
**解決**：請款後只能使用「退款」功能
