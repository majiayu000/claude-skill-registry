---
name: proxy-pay
description: Quick command to create a payment via Proxy. Usage: /proxy-pay [amount] [merchant] [description]. Creates payment intent and provisions virtual card.
disable-model-invocation: true
argument-hint: "[amount] [merchant] [description]"
---

# Make a Payment

Create a payment intent and get a virtual card.

## Usage

```
/proxy-pay 49.99 Amazon office supplies
/proxy-pay 150 "Best Buy" laptop stand
/proxy-pay 29.99 Netflix monthly subscription
```

## Instructions

Parse the request from: $ARGUMENTS

### Step 1: Check Balance
```
Call: proxy.balance.get
If insufficient: Inform user, offer proxy.funding.get
```

### Step 2: Create Intent
```
Call: proxy.intents.create
Parameters:
  - merchant: (from request)
  - amount: (parse number)
  - description: (remaining text or generate one)
```

### Step 3: Handle Response

**If `status: "pending"` or `status: "card_issued"`:**
```
Call: proxy.cards.get_sensitive
Provide card details formatted as:

Card Number: 4111 1111 1111 1111
CVV: 123
Expiry: 12/26
Billing ZIP: 10001
```

**If `status: "pending_approval"`:**
```
Inform user: "This purchase requires approval because it exceeds
your auto-approve limit. You'll be notified when approved."
```

**If error:**
```
Explain the error clearly based on error code.
Provide resolution steps.
```
