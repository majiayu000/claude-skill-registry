---
name: In-Game Purchases
description: Enabling monetization through virtual goods and currencies with virtual economy design, store implementation, payment integration, and purchase validation for gaming applications.
---

# In-Game Purchases

> **Current Level:** Intermediate  
> **Domain:** Gaming / Payments

---

## Overview

In-game purchases enable monetization through virtual goods and currencies. This guide covers virtual economy, store implementation, and payment integration for building monetization systems that provide value to players while generating revenue.

## Virtual Economy Design

```typescript
// Currency types
enum CurrencyType {
  SOFT = 'soft', // Earned through gameplay (coins)
  HARD = 'hard', // Purchased with real money (gems)
  PREMIUM = 'premium' // Subscription currency
}

// Price tiers
const PRICE_TIERS = {
  small: { amount: 100, price: 0.99 },
  medium: { amount: 500, price: 4.99 },
  large: { amount: 1200, price: 9.99 },
  mega: { amount: 3000, price: 19.99 }
};
```

## Database Schema

```sql
-- currencies table
CREATE TABLE currencies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  player_id UUID REFERENCES players(id) ON DELETE CASCADE,
  
  soft_currency BIGINT DEFAULT 0,
  hard_currency BIGINT DEFAULT 0,
  premium_currency BIGINT DEFAULT 0,
  
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(player_id)
);

-- items table
CREATE TABLE items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key VARCHAR(100) UNIQUE NOT NULL,
  
  name VARCHAR(255) NOT NULL,
  description TEXT,
  icon_url VARCHAR(500),
  
  category VARCHAR(100),
  rarity VARCHAR(50),
  
  price_soft INTEGER,
  price_hard INTEGER,
  price_usd DECIMAL(10,2),
  
  stackable BOOLEAN DEFAULT TRUE,
  max_stack INTEGER,
  
  metadata JSONB,
  
  active BOOLEAN DEFAULT TRUE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_category (category),
  INDEX idx_key (key)
);

-- player_inventory table
CREATE TABLE player_inventory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  player_id UUID REFERENCES players(id) ON DELETE CASCADE,
  item_id UUID REFERENCES items(id) ON DELETE CASCADE,
  
  quantity INTEGER DEFAULT 1,
  
  acquired_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(player_id, item_id),
  INDEX idx_player (player_id)
);

-- transactions table
CREATE TABLE transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  player_id UUID REFERENCES players(id) ON DELETE CASCADE,
  
  type VARCHAR(50) NOT NULL,
  item_id UUID REFERENCES items(id),
  
  currency_type VARCHAR(50),
  amount INTEGER,
  
  price_usd DECIMAL(10,2),
  
  platform VARCHAR(50),
  platform_transaction_id VARCHAR(255),
  receipt TEXT,
  
  status VARCHAR(50) DEFAULT 'pending',
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_player (player_id),
  INDEX idx_platform_tx (platform_transaction_id)
);
```

## Store Implementation

```typescript
// services/store.service.ts
export class StoreService {
  async getStoreItems(category?: string): Promise<StoreItem[]> {
    const items = await db.item.findMany({
      where: {
        active: true,
        ...(category && { category })
      }
    });

    return items.map(item => this.toStoreItem(item));
  }

  async purchaseWithSoftCurrency(
    playerId: string,
    itemKey: string,
    quantity: number = 1
  ): Promise<Purchase> {
    const item = await db.item.findUnique({ where: { key: itemKey } });

    if (!item || !item.priceSoft) {
      throw new Error('Item not available for soft currency');
    }

    const totalCost = item.priceSoft * quantity;

    // Check balance
    const currency = await db.currency.findUnique({ where: { playerId } });

    if (!currency || currency.softCurrency < totalCost) {
      throw new Error('Insufficient soft currency');
    }

    // Deduct currency
    await db.currency.update({
      where: { playerId },
      data: {
        softCurrency: { decrement: totalCost }
      }
    });

    // Add to inventory
    await this.addToInventory(playerId, item.id, quantity);

    // Record transaction
    await db.transaction.create({
      data: {
        playerId,
        itemId: item.id,
        type: 'purchase',
        currencyType: 'soft',
        amount: totalCost,
        status: 'completed'
      }
    });

    return {
      itemId: item.id,
      quantity,
      cost: totalCost,
      currencyType: 'soft'
    };
  }

  async purchaseWithHardCurrency(
    playerId: string,
    itemKey: string,
    quantity: number = 1
  ): Promise<Purchase> {
    const item = await db.item.findUnique({ where: { key: itemKey } });

    if (!item || !item.priceHard) {
      throw new Error('Item not available for hard currency');
    }

    const totalCost = item.priceHard * quantity;

    const currency = await db.currency.findUnique({ where: { playerId } });

    if (!currency || currency.hardCurrency < totalCost) {
      throw new Error('Insufficient hard currency');
    }

    await db.currency.update({
      where: { playerId },
      data: {
        hardCurrency: { decrement: totalCost }
      }
    });

    await this.addToInventory(playerId, item.id, quantity);

    await db.transaction.create({
      data: {
        playerId,
        itemId: item.id,
        type: 'purchase',
        currencyType: 'hard',
        amount: totalCost,
        status: 'completed'
      }
    });

    return {
      itemId: item.id,
      quantity,
      cost: totalCost,
      currencyType: 'hard'
    };
  }

  private async addToInventory(
    playerId: string,
    itemId: string,
    quantity: number
  ): Promise<void> {
    await db.playerInventory.upsert({
      where: {
        playerId_itemId: { playerId, itemId }
      },
      create: {
        playerId,
        itemId,
        quantity
      },
      update: {
        quantity: { increment: quantity }
      }
    });
  }

  private toStoreItem(item: any): StoreItem {
    return {
      id: item.id,
      key: item.key,
      name: item.name,
      description: item.description,
      iconUrl: item.iconUrl,
      category: item.category,
      rarity: item.rarity,
      prices: {
        soft: item.priceSoft,
        hard: item.priceHard,
        usd: item.priceUsd
      }
    };
  }
}

interface StoreItem {
  id: string;
  key: string;
  name: string;
  description: string;
  iconUrl: string;
  category: string;
  rarity: string;
  prices: {
    soft: number | null;
    hard: number | null;
    usd: number | null;
  };
}

interface Purchase {
  itemId: string;
  quantity: number;
  cost: number;
  currencyType: string;
}
```

## Payment Integration

```typescript
// services/payment.service.ts
export class PaymentService {
  async initiatePurchase(
    playerId: string,
    productId: string,
    platform: 'ios' | 'android' | 'web'
  ): Promise<PurchaseIntent> {
    const product = await db.item.findUnique({ where: { key: productId } });

    if (!product || !product.priceUsd) {
      throw new Error('Product not available');
    }

    const transaction = await db.transaction.create({
      data: {
        playerId,
        itemId: product.id,
        type: 'iap',
        priceUsd: product.priceUsd,
        platform,
        status: 'pending'
      }
    });

    return {
      transactionId: transaction.id,
      productId,
      price: product.priceUsd,
      platform
    };
  }

  async completePurchase(
    transactionId: string,
    receipt: string,
    platformTransactionId: string
  ): Promise<void> {
    const transaction = await db.transaction.findUnique({
      where: { id: transactionId }
    });

    if (!transaction) {
      throw new Error('Transaction not found');
    }

    // Verify receipt
    const isValid = await this.verifyReceipt(
      receipt,
      transaction.platform!,
      platformTransactionId
    );

    if (!isValid) {
      throw new Error('Invalid receipt');
    }

    // Update transaction
    await db.transaction.update({
      where: { id: transactionId },
      data: {
        receipt,
        platformTransactionId,
        status: 'completed'
      }
    });

    // Grant items/currency
    await this.grantPurchase(transaction);
  }

  private async verifyReceipt(
    receipt: string,
    platform: string,
    transactionId: string
  ): Promise<boolean> {
    if (platform === 'ios') {
      return this.verifyAppleReceipt(receipt);
    } else if (platform === 'android') {
      return this.verifyGoogleReceipt(receipt, transactionId);
    }

    return false;
  }

  private async verifyAppleReceipt(receipt: string): Promise<boolean> {
    const response = await fetch('https://buy.itunes.apple.com/verifyReceipt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        'receipt-data': receipt,
        'password': process.env.APPLE_SHARED_SECRET
      })
    });

    const data = await response.json();
    return data.status === 0;
  }

  private async verifyGoogleReceipt(
    receipt: string,
    transactionId: string
  ): Promise<boolean> {
    // Use Google Play Developer API
    const { google } = require('googleapis');
    const androidpublisher = google.androidpublisher('v3');

    try {
      const result = await androidpublisher.purchases.products.get({
        packageName: process.env.ANDROID_PACKAGE_NAME,
        productId: receipt,
        token: transactionId,
        auth: process.env.GOOGLE_SERVICE_ACCOUNT
      });

      return result.data.purchaseState === 0; // 0 = purchased
    } catch (error) {
      return false;
    }
  }

  private async grantPurchase(transaction: any): Promise<void> {
    const item = await db.item.findUnique({
      where: { id: transaction.itemId }
    });

    if (!item) return;

    // If currency pack
    if (item.category === 'currency') {
      await db.currency.update({
        where: { playerId: transaction.playerId },
        data: {
          hardCurrency: { increment: item.metadata.amount }
        }
      });
    } else {
      // If item
      await db.playerInventory.upsert({
        where: {
          playerId_itemId: {
            playerId: transaction.playerId,
            itemId: item.id
          }
        },
        create: {
          playerId: transaction.playerId,
          itemId: item.id,
          quantity: 1
        },
        update: {
          quantity: { increment: 1 }
        }
      });
    }
  }
}

interface PurchaseIntent {
  transactionId: string;
  productId: string;
  price: number;
  platform: string;
}
```

## Inventory Management

```typescript
// services/inventory.service.ts
export class InventoryService {
  async getInventory(playerId: string): Promise<InventoryItem[]> {
    const items = await db.playerInventory.findMany({
      where: { playerId },
      include: { item: true }
    });

    return items.map(i => ({
      id: i.id,
      itemId: i.item.id,
      name: i.item.name,
      iconUrl: i.item.iconUrl,
      quantity: i.quantity,
      rarity: i.item.rarity,
      acquiredAt: i.acquiredAt
    }));
  }

  async useItem(playerId: string, itemId: string): Promise<void> {
    const inventoryItem = await db.playerInventory.findUnique({
      where: {
        playerId_itemId: { playerId, itemId }
      }
    });

    if (!inventoryItem || inventoryItem.quantity <= 0) {
      throw new Error('Item not in inventory');
    }

    // Apply item effect
    await this.applyItemEffect(playerId, itemId);

    // Decrease quantity
    if (inventoryItem.quantity === 1) {
      await db.playerInventory.delete({
        where: { id: inventoryItem.id }
      });
    } else {
      await db.playerInventory.update({
        where: { id: inventoryItem.id },
        data: {
          quantity: { decrement: 1 }
        }
      });
    }
  }

  private async applyItemEffect(playerId: string, itemId: string): Promise<void> {
    const item = await db.item.findUnique({ where: { id: itemId } });

    if (!item || !item.metadata) return;

    // Apply effects based on item type
    switch (item.metadata.type) {
      case 'health_potion':
        await this.healPlayer(playerId, item.metadata.amount);
        break;

      case 'xp_boost':
        await this.applyXPBoost(playerId, item.metadata.duration);
        break;
    }
  }

  private async healPlayer(playerId: string, amount: number): Promise<void> {
    // Implementation
  }

  private async applyXPBoost(playerId: string, duration: number): Promise<void> {
    // Implementation
  }
}

interface InventoryItem {
  id: string;
  itemId: string;
  name: string;
  iconUrl: string;
  quantity: number;
  rarity: string;
  acquiredAt: Date;
}
```

## Gifting System

```typescript
// services/gifting.service.ts
export class GiftingService {
  async sendGift(
    senderId: string,
    recipientId: string,
    itemId: string
  ): Promise<void> {
    // Check if sender has item
    const senderItem = await db.playerInventory.findUnique({
      where: {
        playerId_itemId: { playerId: senderId, itemId }
      }
    });

    if (!senderItem || senderItem.quantity <= 0) {
      throw new Error('Item not in inventory');
    }

    // Remove from sender
    await db.playerInventory.update({
      where: { id: senderItem.id },
      data: {
        quantity: { decrement: 1 }
      }
    });

    // Add to recipient
    await db.playerInventory.upsert({
      where: {
        playerId_itemId: { playerId: recipientId, itemId }
      },
      create: {
        playerId: recipientId,
        itemId,
        quantity: 1
      },
      update: {
        quantity: { increment: 1 }
      }
    });

    // Notify recipient
    io.to(`player:${recipientId}`).emit('gift-received', {
      senderId,
      itemId
    });
  }
}
```

## Best Practices

1. **Economy Balance** - Balance earning vs spending
2. **Receipt Validation** - Always validate receipts
3. **Fraud Prevention** - Detect and prevent fraud
4. **Clear Pricing** - Show clear prices
5. **Inventory Limits** - Set reasonable limits
6. **Transaction Logs** - Log all transactions
7. **Refunds** - Handle refund requests
8. **Analytics** - Track purchase metrics
9. **Testing** - Test with sandbox accounts
10. **Compliance** - Follow platform guidelines

---

## Quick Start

### Virtual Store

```typescript
interface StoreItem {
  id: string
  name: string
  description: string
  price: {
    currency: 'soft' | 'hard' | 'premium'
    amount: number
  }
  category: 'consumable' | 'permanent' | 'subscription'
}

async function purchaseItem(
  playerId: string,
  itemId: string
): Promise<PurchaseResult> {
  const item = await getStoreItem(itemId)
  const player = await getPlayer(playerId)
  
  // Check balance
  if (player.currency[item.price.currency] < item.price.amount) {
    throw new Error('Insufficient funds')
  }
  
  // Deduct currency
  await deductCurrency(playerId, item.price.currency, item.price.amount)
  
  // Grant item
  await grantItem(playerId, itemId)
  
  return { success: true, item }
}
```

### Receipt Validation

```typescript
// iOS receipt validation
async function validateIOSReceipt(receiptData: string): Promise<boolean> {
  const response = await fetch('https://buy.itunes.apple.com/verifyReceipt', {
    method: 'POST',
    body: JSON.stringify({
      'receipt-data': receiptData,
      'password': process.env.IOS_SHARED_SECRET
    })
  })
  
  const result = await response.json()
  return result.status === 0
}
```

---

## Production Checklist

- [ ] **Virtual Economy**: Design balanced virtual economy
- [ ] **Store Implementation**: In-game store
- [ ] **Payment Integration**: Payment gateway integration
- [ ] **Receipt Validation**: Validate receipts server-side
- [ ] **Currency Management**: Manage virtual currencies
- [ ] **Item Management**: Item granting and tracking
- [ ] **Analytics**: Track purchase metrics
- [ ] **Testing**: Test purchase flows
- [ ] **Documentation**: Document purchase system
- [ ] **Security**: Prevent cheating
- [ ] **Compliance**: Meet app store requirements
- [ ] **Support**: Customer support for purchases

---

## Anti-patterns

### ❌ Don't: Trust Client

```typescript
// ❌ Bad - Client-side validation
if (player.coins >= item.price) {
  player.coins -= item.price
  grantItem(item)  // Client can cheat!
}
```

```typescript
// ✅ Good - Server-side validation
if (player.coins >= item.price) {
  await deductCurrency(playerId, 'soft', item.price)
  await grantItem(playerId, itemId)  // Server is authoritative
}
```

### ❌ Don't: No Receipt Validation

```typescript
// ❌ Bad - No validation
await processPurchase(purchaseData)
// Fake purchases possible!
```

```typescript
// ✅ Good - Validate receipts
const isValid = await validateReceipt(purchaseData.receipt)
if (isValid) {
  await processPurchase(purchaseData)
}
```

---

## Integration Points

- **Payment Gateways** (`30-ecommerce/payment-gateways/`) - Payment processing
- **Game Analytics** (`38-gaming-features/game-analytics/`) - Purchase analytics
- **Achievements** (`38-gaming-features/achievements/`) - Purchase rewards

---

## Further Reading

- [In-Game Purchase Best Practices](https://www.apple.com/app-store/review/guidelines/#in-app-purchase)
- [Virtual Economy Design](https://www.gamedeveloper.com/design/virtual-economy-design)

## Resources

- [Apple In-App Purchase](https://developer.apple.com/in-app-purchase/)
- [Google Play Billing](https://developer.android.com/google/play/billing)
- [Stripe](https://stripe.com/)
- [Virtual Economy Design](https://www.gamedeveloper.com/business/designing-a-virtual-economy)
