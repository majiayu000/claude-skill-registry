---
name: Cryptocurrency Payment
description: Enabling direct peer-to-peer cryptocurrency transactions without intermediaries, including direct wallet payments, payment processors, transaction monitoring, and blockchain confirmation.
---

# Cryptocurrency Payment

> **Current Level:** Advanced  
> **Domain:** Blockchain / Payments

---

## Overview

Cryptocurrency payments enable direct peer-to-peer transactions without intermediaries. This guide covers direct wallet payments, payment processors, and transaction monitoring for accepting crypto payments in applications.

## Crypto Payment Concepts

```
Customer → Payment Request → Wallet → Blockchain → Confirmation → Order Complete
```

**Payment Methods:**
1. **Direct Wallet** - Customer sends crypto directly
2. **Payment Processor** - Third-party handles payments
3. **Smart Contract** - Automated payment handling

## Direct Wallet Payments

```typescript
// services/crypto-payment.service.ts
import { ethers } from 'ethers';

export class CryptoPaymentService {
  constructor(
    private provider: ethers.providers.Provider,
    private merchantAddress: string
  ) {}

  async createPaymentRequest(
    amount: string,
    currency: 'ETH' | 'USDC' | 'DAI'
  ): Promise<PaymentRequest> {
    const paymentId = this.generatePaymentId();
    const expiresAt = Date.now() + 15 * 60 * 1000; // 15 minutes

    return {
      paymentId,
      merchantAddress: this.merchantAddress,
      amount,
      currency,
      expiresAt,
      status: 'pending'
    };
  }

  async monitorPayment(
    paymentId: string,
    expectedAmount: string
  ): Promise<PaymentStatus> {
    const filter = {
      address: this.merchantAddress,
      topics: []
    };

    return new Promise((resolve) => {
      this.provider.on(filter, async (log) => {
        const tx = await this.provider.getTransaction(log.transactionHash);
        
        if (tx.to === this.merchantAddress) {
          const receivedAmount = ethers.utils.formatEther(tx.value);
          
          if (receivedAmount === expectedAmount) {
            resolve({
              paymentId,
              status: 'confirmed',
              transactionHash: tx.hash,
              amount: receivedAmount
            });
          }
        }
      });
    });
  }

  async verifyPayment(
    transactionHash: string,
    expectedAmount: string
  ): Promise<boolean> {
    const receipt = await this.provider.getTransactionReceipt(transactionHash);
    
    if (!receipt || receipt.status !== 1) {
      return false;
    }

    const tx = await this.provider.getTransaction(transactionHash);
    const receivedAmount = ethers.utils.formatEther(tx.value);

    return (
      tx.to === this.merchantAddress &&
      receivedAmount === expectedAmount &&
      receipt.confirmations >= 3
    );
  }

  private generatePaymentId(): string {
    return `pay_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

interface PaymentRequest {
  paymentId: string;
  merchantAddress: string;
  amount: string;
  currency: string;
  expiresAt: number;
  status: 'pending' | 'confirmed' | 'expired';
}

interface PaymentStatus {
  paymentId: string;
  status: string;
  transactionHash: string;
  amount: string;
}
```

## Payment Processors

### Coinbase Commerce

```typescript
// services/coinbase-commerce.service.ts
import axios from 'axios';

export class CoinbaseCommerceService {
  private apiKey = process.env.COINBASE_COMMERCE_API_KEY!;
  private baseUrl = 'https://api.commerce.coinbase.com';

  async createCharge(data: CreateChargeDto): Promise<Charge> {
    const response = await axios.post(
      `${this.baseUrl}/charges`,
      {
        name: data.name,
        description: data.description,
        pricing_type: 'fixed_price',
        local_price: {
          amount: data.amount,
          currency: data.currency
        },
        metadata: data.metadata
      },
      {
        headers: {
          'X-CC-Api-Key': this.apiKey,
          'X-CC-Version': '2018-03-22'
        }
      }
    );

    return response.data.data;
  }

  async getCharge(chargeId: string): Promise<Charge> {
    const response = await axios.get(
      `${this.baseUrl}/charges/${chargeId}`,
      {
        headers: {
          'X-CC-Api-Key': this.apiKey,
          'X-CC-Version': '2018-03-22'
        }
      }
    );

    return response.data.data;
  }

  async listCharges(): Promise<Charge[]> {
    const response = await axios.get(
      `${this.baseUrl}/charges`,
      {
        headers: {
          'X-CC-Api-Key': this.apiKey,
          'X-CC-Version': '2018-03-22'
        }
      }
    );

    return response.data.data;
  }

  verifyWebhook(signature: string, payload: string): boolean {
    const crypto = require('crypto');
    const webhookSecret = process.env.COINBASE_WEBHOOK_SECRET!;

    const expectedSignature = crypto
      .createHmac('sha256', webhookSecret)
      .update(payload)
      .digest('hex');

    return signature === expectedSignature;
  }
}

interface CreateChargeDto {
  name: string;
  description: string;
  amount: string;
  currency: string;
  metadata?: Record<string, any>;
}

interface Charge {
  id: string;
  code: string;
  name: string;
  description: string;
  hosted_url: string;
  pricing: {
    local: { amount: string; currency: string };
    bitcoin?: { amount: string; currency: string };
    ethereum?: { amount: string; currency: string };
  };
  payments: Payment[];
  timeline: TimelineEvent[];
}

interface Payment {
  network: string;
  transaction_id: string;
  status: string;
  value: {
    local: { amount: string; currency: string };
    crypto: { amount: string; currency: string };
  };
}

interface TimelineEvent {
  time: string;
  status: string;
}
```

### NOWPayments

```typescript
// services/nowpayments.service.ts
export class NOWPaymentsService {
  private apiKey = process.env.NOWPAYMENTS_API_KEY!;
  private baseUrl = 'https://api.nowpayments.io/v1';

  async createPayment(data: CreatePaymentDto): Promise<Payment> {
    const response = await axios.post(
      `${this.baseUrl}/payment`,
      {
        price_amount: data.amount,
        price_currency: data.currency,
        pay_currency: data.payCurrency,
        order_id: data.orderId,
        order_description: data.description,
        ipn_callback_url: data.callbackUrl
      },
      {
        headers: {
          'x-api-key': this.apiKey
        }
      }
    );

    return response.data;
  }

  async getPaymentStatus(paymentId: string): Promise<PaymentStatus> {
    const response = await axios.get(
      `${this.baseUrl}/payment/${paymentId}`,
      {
        headers: {
          'x-api-key': this.apiKey
        }
      }
    );

    return response.data;
  }

  async getAvailableCurrencies(): Promise<string[]> {
    const response = await axios.get(
      `${this.baseUrl}/currencies`,
      {
        headers: {
          'x-api-key': this.apiKey
        }
      }
    );

    return response.data.currencies;
  }

  async getEstimatedPrice(
    amount: number,
    fromCurrency: string,
    toCurrency: string
  ): Promise<EstimatedPrice> {
    const response = await axios.get(
      `${this.baseUrl}/estimate`,
      {
        params: {
          amount,
          currency_from: fromCurrency,
          currency_to: toCurrency
        },
        headers: {
          'x-api-key': this.apiKey
        }
      }
    );

    return response.data;
  }
}

interface CreatePaymentDto {
  amount: number;
  currency: string;
  payCurrency: string;
  orderId: string;
  description: string;
  callbackUrl: string;
}

interface EstimatedPrice {
  currency_from: string;
  currency_to: string;
  estimated_amount: string;
}
```

## Transaction Monitoring

```typescript
// services/transaction-monitor.service.ts
export class TransactionMonitorService {
  private provider: ethers.providers.Provider;

  constructor(provider: ethers.providers.Provider) {
    this.provider = provider;
  }

  async waitForConfirmations(
    txHash: string,
    confirmations: number = 3
  ): Promise<ethers.providers.TransactionReceipt> {
    const receipt = await this.provider.waitForTransaction(txHash, confirmations);
    return receipt;
  }

  async getTransactionStatus(txHash: string): Promise<TransactionStatus> {
    const [tx, receipt] = await Promise.all([
      this.provider.getTransaction(txHash),
      this.provider.getTransactionReceipt(txHash)
    ]);

    if (!receipt) {
      return {
        status: 'pending',
        confirmations: 0
      };
    }

    const currentBlock = await this.provider.getBlockNumber();
    const confirmations = currentBlock - receipt.blockNumber + 1;

    return {
      status: receipt.status === 1 ? 'confirmed' : 'failed',
      confirmations,
      blockNumber: receipt.blockNumber,
      gasUsed: receipt.gasUsed.toString()
    };
  }

  monitorAddress(
    address: string,
    callback: (tx: ethers.providers.TransactionResponse) => void
  ): () => void {
    const filter = {
      address,
      topics: []
    };

    const listener = async (log: ethers.providers.Log) => {
      const tx = await this.provider.getTransaction(log.transactionHash);
      if (tx.to === address) {
        callback(tx);
      }
    };

    this.provider.on(filter, listener);

    return () => {
      this.provider.off(filter, listener);
    };
  }
}

interface TransactionStatus {
  status: 'pending' | 'confirmed' | 'failed';
  confirmations: number;
  blockNumber?: number;
  gasUsed?: string;
}
```

## Payment Confirmation

```typescript
// services/payment-confirmation.service.ts
export class PaymentConfirmationService {
  async confirmPayment(
    transactionHash: string,
    expectedAmount: string,
    expectedRecipient: string
  ): Promise<ConfirmationResult> {
    const provider = new ethers.providers.InfuraProvider('mainnet');
    
    // Wait for confirmations
    const receipt = await provider.waitForTransaction(transactionHash, 3);

    if (receipt.status !== 1) {
      return {
        confirmed: false,
        reason: 'Transaction failed'
      };
    }

    // Verify transaction details
    const tx = await provider.getTransaction(transactionHash);

    if (tx.to?.toLowerCase() !== expectedRecipient.toLowerCase()) {
      return {
        confirmed: false,
        reason: 'Incorrect recipient'
      };
    }

    const receivedAmount = ethers.utils.formatEther(tx.value);
    if (receivedAmount !== expectedAmount) {
      return {
        confirmed: false,
        reason: 'Incorrect amount'
      };
    }

    return {
      confirmed: true,
      transactionHash,
      amount: receivedAmount,
      confirmations: receipt.confirmations
    };
  }
}

interface ConfirmationResult {
  confirmed: boolean;
  reason?: string;
  transactionHash?: string;
  amount?: string;
  confirmations?: number;
}
```

## Multi-Currency Support

```typescript
// services/multi-currency.service.ts
export class MultiCurrencyService {
  private supportedCurrencies = ['ETH', 'BTC', 'USDC', 'USDT', 'DAI'];

  async getExchangeRate(from: string, to: string): Promise<number> {
    // Use CoinGecko API
    const response = await fetch(
      `https://api.coingecko.com/api/v3/simple/price?ids=${from}&vs_currencies=${to}`
    );

    const data = await response.json();
    return data[from.toLowerCase()][to.toLowerCase()];
  }

  async convertAmount(
    amount: number,
    from: string,
    to: string
  ): Promise<number> {
    const rate = await this.getExchangeRate(from, to);
    return amount * rate;
  }

  async getPriceInCrypto(
    usdAmount: number,
    cryptocurrency: string
  ): Promise<string> {
    const cryptoAmount = await this.convertAmount(usdAmount, 'usd', cryptocurrency);
    return cryptoAmount.toFixed(8);
  }
}
```

## Webhook Handling

```typescript
// pages/api/webhooks/coinbase.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import crypto from 'crypto';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Verify webhook signature
  const signature = req.headers['x-cc-webhook-signature'] as string;
  const payload = JSON.stringify(req.body);

  if (!verifySignature(signature, payload)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const event = req.body;

  // Handle different event types
  switch (event.type) {
    case 'charge:confirmed':
      await handleChargeConfirmed(event.data);
      break;

    case 'charge:failed':
      await handleChargeFailed(event.data);
      break;

    case 'charge:pending':
      await handleChargePending(event.data);
      break;
  }

  res.json({ success: true });
}

function verifySignature(signature: string, payload: string): boolean {
  const webhookSecret = process.env.COINBASE_WEBHOOK_SECRET!;
  
  const expectedSignature = crypto
    .createHmac('sha256', webhookSecret)
    .update(payload)
    .digest('hex');

  return signature === expectedSignature;
}

async function handleChargeConfirmed(data: any): Promise<void> {
  // Update order status
  await db.order.update({
    where: { id: data.metadata.order_id },
    data: {
      status: 'paid',
      transactionHash: data.payments[0].transaction_id
    }
  });

  // Send confirmation email
  await emailService.sendOrderConfirmation(data.metadata.order_id);
}

async function handleChargeFailed(data: any): Promise<void> {
  await db.order.update({
    where: { id: data.metadata.order_id },
    data: { status: 'payment_failed' }
  });
}

async function handleChargePending(data: any): Promise<void> {
  await db.order.update({
    where: { id: data.metadata.order_id },
    data: { status: 'payment_pending' }
  });
}
```

---

## Quick Start

### Payment Request

```typescript
interface PaymentRequest {
  orderId: string
  amount: number  // in crypto (e.g., 0.01 ETH)
  currency: 'ETH' | 'BTC' | 'USDT'
  recipientAddress: string
}

async function createPaymentRequest(request: PaymentRequest) {
  const payment = await db.payments.create({
    data: {
      orderId: request.orderId,
      amount: request.amount,
      currency: request.currency,
      recipientAddress: request.recipientAddress,
      status: 'pending',
      expiresAt: addMinutes(new Date(), 15)  // 15 min expiry
    }
  })
  
  return {
    address: request.recipientAddress,
    amount: request.amount,
    currency: request.currency,
    qrCode: generateQRCode(`${request.currency}:${request.recipientAddress}?amount=${request.amount}`)
  }
}
```

### Transaction Monitoring

```typescript
async function monitorTransaction(txHash: string) {
  const provider = new ethers.providers.JsonRpcProvider(RPC_URL)
  
  // Wait for confirmations
  const receipt = await provider.waitForTransaction(txHash, 3)  // 3 confirmations
  
  if (receipt.status === 1) {
    await updatePaymentStatus(txHash, 'confirmed')
  } else {
    await updatePaymentStatus(txHash, 'failed')
  }
}
```

---

## Production Checklist

- [ ] **Wallet Integration**: Support multiple wallets
- [ ] **Payment Processing**: Payment processor or direct wallet
- [ ] **Transaction Monitoring**: Monitor blockchain transactions
- [ ] **Confirmations**: Wait for multiple confirmations
- [ ] **Amount Verification**: Verify exact payment amount
- [ ] **Address Verification**: Verify recipient address
- [ ] **Expiry**: Payment request expiry
- [ ] **Refunds**: Refund process
- [ ] **Security**: Secure private keys
- [ ] **Testing**: Test on testnets first
- [ ] **Compliance**: Follow local regulations
- [ ] **Documentation**: Document payment flow

---

## Anti-patterns

### ❌ Don't: No Confirmations

```typescript
// ❌ Bad - Accept after 1 confirmation
const receipt = await provider.waitForTransaction(txHash, 1)
await completeOrder(orderId)  // Too risky!
```

```typescript
// ✅ Good - Wait for multiple confirmations
const receipt = await provider.waitForTransaction(txHash, 3)  // 3 confirmations
await completeOrder(orderId)  // Safer
```

### ❌ Don't: Store Private Keys

```typescript
// ❌ Bad - Store private keys
const wallet = new ethers.Wallet('0x...private-key...')  // Exposed!
```

```typescript
// ✅ Good - Use payment processor
// Or hardware wallet
// Never store private keys in code
```

---

## Integration Points

- **Wallet Connection** (`35-blockchain-web3/wallet-connection/`) - User wallets
- **Smart Contracts** (`35-blockchain-web3/smart-contracts/`) - Contract payments
- **Payment Gateways** (`30-ecommerce/payment-gateways/`) - Payment patterns

---

## Further Reading

- [Ethereum Payment Processing](https://ethereum.org/en/developers/docs/transactions/)
- [Bitcoin Payment Processing](https://bitcoin.org/en/developer-guide)

## Best Practices

1. **Confirmations** - Wait for multiple confirmations
2. **Amount Verification** - Verify exact payment amount
3. **Address Verification** - Verify recipient address
4. **Webhook Security** - Verify webhook signatures
5. **Timeout Handling** - Set payment expiration times
6. **Multi-Currency** - Support multiple cryptocurrencies
7. **Price Updates** - Update crypto prices regularly
8. **Refunds** - Implement refund mechanism
9. **Testing** - Test on testnets first
10. **Compliance** - Follow local regulations

## Resources

- [Coinbase Commerce](https://commerce.coinbase.com/docs/)
- [NOWPayments](https://nowpayments.io/doc/api)
- [BitPay](https://bitpay.com/docs/)
- [CoinGecko API](https://www.coingecko.com/en/api)
