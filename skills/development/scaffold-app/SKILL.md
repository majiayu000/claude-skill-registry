---
name: scaffold-app
description: Generate complete starter applications with Payram integration for Express, Next.js, FastAPI, Laravel, Gin, and Spring Boot
---

# Scaffold Payram Application

## Overview

This skill provides instructions for scaffolding complete starter applications with Payram integration. Instead of adding Payram to existing projects, you'll generate new applications from scratch with payments, payouts, and webhooks pre-configured. Each scaffold includes a web console for testing functionality without writing frontend code.

## When to Use This Skill

Use this skill when you need to:

- Create a new project with Payram integration from scratch
- Build proof-of-concept or demo applications quickly
- Learn Payram API patterns through working examples
- Generate reference implementations for your team
- Prototype new features before adding to production code

## Prerequisites

Before starting, ensure you have:

- Completed the `setup-payram` skill (understand environment configuration)
- Chosen your target framework (Express, Next.js, FastAPI, Laravel, Gin, Spring Boot)
- Development tools installed (Node.js/Python/PHP/Go/Java)
- Basic familiarity with your chosen framework

---

## Instructions

### Part 1: Understanding Scaffold Structure

#### 1.1 What's Included

All scaffolds provide:

1. **Environment Configuration**
   - `.env.example` with Payram variables
   - Configuration loading/validation

2. **Payment Endpoints**
   - `POST /api/payments/create` - Create payment
   - `GET /api/payments/:referenceId` - Check status

3. **Payout Endpoints**
   - `POST /api/payouts/create` - Create payout
   - `GET /api/payouts/:id` - Check status

4. **Webhook Handler** (optional)
   - `POST /api/payram/webhook` - Receive events

5. **Web Console** (browser UI)
   - Test payments visually
   - Test payouts visually
   - View API responses

6. **Package Configuration**
   - Dependencies (Payram SDK, framework, etc.)
   - Scripts for running/building

#### 1.2 Directory Structures

**Express:**

```
payram-express-starter/
├── package.json
├── .env.example
├── index.js
└── public/
    └── index.html
```

**Next.js:**

```
payram-nextjs-starter/
├── package.json
├── .env.example
├── next.config.js
├── app/
│   ├── page.tsx
│   └── api/
│       ├── payments/
│       │   ├── create/route.ts
│       │   └── [referenceId]/route.ts
│       ├── payouts/
│       │   ├── create/route.ts
│       │   └── [id]/route.ts
│       └── payram/
│           └── webhook/route.ts
└── lib/
    └── payram.ts
```

**FastAPI:**

```
payram-fastapi-starter/
├── requirements.txt
├── .env.example
├── main.py
└── templates/
    └── index.html
```

**Laravel:**

```
payram-laravel-starter/
├── composer.json
├── .env.example
├── routes/
│   └── api.php
├── app/
│   └── Http/
│       └── Controllers/
│           └── PayramController.php
└── resources/
    └── views/
        └── console.blade.php
```

**Gin:**

```
payram-gin-starter/
├── go.mod
├── .env.example
├── main.go
├── handlers/
│   └── payram.go
└── static/
    └── index.html
```

**Spring Boot:**

```
payram-spring-boot-starter/
├── pom.xml
├── .env.example
├── src/
│   └── main/
│       ├── java/com/example/payram/
│       │   ├── PayramApplication.java
│       │   └── controller/
│       │       └── PayramController.java
│       └── resources/
│           ├── application.properties
│           └── static/
│               └── index.html
```

---

### Part 2: Framework-Specific Instructions

#### 2.1 Express Scaffold

**Step 1: Create Directory Structure**

```bash
mkdir payram-express-starter
cd payram-express-starter
```

**Step 2: Initialize Node Project**

```bash
npm init -y
```

**Step 3: Install Dependencies**

```bash
npm install express cors dotenv payram
```

**Step 4: Create .env.example**

**File:** `.env.example`

```bash
PAYRAM_BASE_URL=https://your-merchant.payram.com
PAYRAM_API_KEY=pk_test_your_api_key_here
PORT=3000
```

**Step 5: Create Main Server File**

**File:** `index.js`

```javascript
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { Payram } from 'payram';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY,
  baseUrl: process.env.PAYRAM_BASE_URL,
});

// Payment endpoints
app.post('/api/payments/create', async (req, res) => {
  try {
    const {
      amount = 1,
      customerEmail = 'demo@example.com',
      customerId = 'demo-customer',
    } = req.body;

    const checkout = await payram.payments.initiatePayment({
      amountInUSD: Number(amount),
      customerEmail,
      customerId,
    });

    res.json(checkout);
  } catch (error) {
    console.error('Payment creation failed:', error);
    res.status(500).json({
      error: 'payment_create_failed',
      details: error.message,
    });
  }
});

app.get('/api/payments/:referenceId', async (req, res) => {
  try {
    const payment = await payram.payments.getPaymentRequest(req.params.referenceId);
    res.json(payment);
  } catch (error) {
    console.error('Payment status check failed:', error);
    res.status(500).json({
      error: 'payment_status_failed',
      details: error.message,
    });
  }
});

// Payout endpoints
app.post('/api/payouts/create', async (req, res) => {
  try {
    const {
      amount = '1',
      currencyCode = 'USDT',
      blockchainCode = 'ETH',
      customerID = 'demo-customer',
      email = 'merchant@example.com',
      toAddress = '0xfeedfacecafebeefdeadbeefdeadbeefdeadbeef',
      mobileNumber = '+15555555555',
      residentialAddress = '123 Main St, City, Country',
    } = req.body;

    const payout = await payram.payouts.createPayout({
      customerID,
      email,
      blockchainCode,
      currencyCode,
      amount: String(amount),
      toAddress,
      mobileNumber,
      residentialAddress,
    });

    res.json(payout);
  } catch (error) {
    console.error('Payout creation failed:', error);
    res.status(500).json({
      error: 'payout_create_failed',
      details: error.message,
    });
  }
});

app.get('/api/payouts/:id', async (req, res) => {
  try {
    const payout = await payram.payouts.getPayoutById(Number(req.params.id));
    res.json(payout);
  } catch (error) {
    console.error('Payout status check failed:', error);
    res.status(500).json({
      error: 'payout_status_failed',
      details: error.message,
    });
  }
});

// Webhook endpoint
app.post('/api/payram/webhook', (req, res) => {
  console.log('Payram webhook event received:', req.body);

  // TODO: Validate API-Key header
  // TODO: Process event based on status

  res.json({ message: 'Webhook received successfully' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Payram Express starter running on http://localhost:${PORT}`);
  console.log(`Open http://localhost:${PORT} to access the test console`);
});
```

**Step 6: Create Web Console**

**File:** `public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Payram Test Console</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #f5f5f5;
        padding: 20px;
      }
      .container {
        max-width: 1200px;
        margin: 0 auto;
        background: white;
        border-radius: 8px;
        padding: 30px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      h1 {
        color: #333;
        margin-bottom: 30px;
      }
      .section {
        margin-bottom: 40px;
        padding: 20px;
        background: #f9f9f9;
        border-radius: 6px;
      }
      h2 {
        color: #555;
        margin-bottom: 15px;
        font-size: 20px;
      }
      .form-group {
        margin-bottom: 15px;
      }
      label {
        display: block;
        margin-bottom: 5px;
        font-weight: 500;
        color: #666;
      }
      input,
      button {
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
      }
      button {
        background: #0066cc;
        color: white;
        border: none;
        cursor: pointer;
        font-weight: 600;
        margin-top: 10px;
      }
      button:hover {
        background: #0052a3;
      }
      .response {
        margin-top: 15px;
        padding: 15px;
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        font-family: monospace;
        font-size: 12px;
        white-space: pre-wrap;
        word-break: break-all;
        max-height: 300px;
        overflow-y: auto;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>🚀 Payram Test Console</h1>

      <!-- Payments Section -->
      <div class="section">
        <h2>💳 Create Payment</h2>
        <div class="form-group">
          <label>Amount (USD)</label>
          <input type="number" id="paymentAmount" value="10" step="0.01" />
        </div>
        <div class="form-group">
          <label>Customer Email</label>
          <input type="email" id="customerEmail" value="customer@example.com" />
        </div>
        <div class="form-group">
          <label>Customer ID</label>
          <input type="text" id="customerId" value="demo-customer-001" />
        </div>
        <button onclick="createPayment()">Create Payment</button>
        <div id="paymentResponse" class="response" style="display:none;"></div>
      </div>

      <!-- Payouts Section -->
      <div class="section">
        <h2>💰 Create Payout</h2>
        <div class="form-group">
          <label>Amount</label>
          <input type="text" id="payoutAmount" value="5" />
        </div>
        <div class="form-group">
          <label>Currency Code</label>
          <input type="text" id="currencyCode" value="USDT" />
        </div>
        <div class="form-group">
          <label>Blockchain Code</label>
          <input type="text" id="blockchainCode" value="ETH" />
        </div>
        <div class="form-group">
          <label>To Address</label>
          <input type="text" id="toAddress" value="0xfeedfacecafebeefdeadbeefdeadbeefdeadbeef" />
        </div>
        <button onclick="createPayout()">Create Payout</button>
        <div id="payoutResponse" class="response" style="display:none;"></div>
      </div>

      <!-- Status Check Section -->
      <div class="section">
        <h2>🔍 Check Status</h2>
        <div class="form-group">
          <label>Payment Reference ID</label>
          <input type="text" id="paymentRefId" placeholder="Enter payment reference ID" />
        </div>
        <button onclick="checkPaymentStatus()">Check Payment Status</button>
        <div id="paymentStatusResponse" class="response" style="display:none;"></div>

        <div class="form-group" style="margin-top: 20px;">
          <label>Payout ID</label>
          <input type="number" id="payoutId" placeholder="Enter payout ID" />
        </div>
        <button onclick="checkPayoutStatus()">Check Payout Status</button>
        <div id="payoutStatusResponse" class="response" style="display:none;"></div>
      </div>
    </div>

    <script>
      async function createPayment() {
        const amount = document.getElementById('paymentAmount').value;
        const customerEmail = document.getElementById('customerEmail').value;
        const customerId = document.getElementById('customerId').value;

        const response = await fetch('/api/payments/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ amount, customerEmail, customerId }),
        });

        const data = await response.json();
        displayResponse('paymentResponse', data);

        if (data.reference_id) {
          document.getElementById('paymentRefId').value = data.reference_id;
          alert(`Payment created! Reference: ${data.reference_id}\n\nCheckout URL: ${data.url}`);
        }
      }

      async function createPayout() {
        const amount = document.getElementById('payoutAmount').value;
        const currencyCode = document.getElementById('currencyCode').value;
        const blockchainCode = document.getElementById('blockchainCode').value;
        const toAddress = document.getElementById('toAddress').value;

        const response = await fetch('/api/payouts/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ amount, currencyCode, blockchainCode, toAddress }),
        });

        const data = await response.json();
        displayResponse('payoutResponse', data);

        if (data.id) {
          document.getElementById('payoutId').value = data.id;
          alert(`Payout created! ID: ${data.id}\nStatus: ${data.status}`);
        }
      }

      async function checkPaymentStatus() {
        const referenceId = document.getElementById('paymentRefId').value;
        if (!referenceId) {
          alert('Please enter a payment reference ID');
          return;
        }

        const response = await fetch(`/api/payments/${referenceId}`);
        const data = await response.json();
        displayResponse('paymentStatusResponse', data);
      }

      async function checkPayoutStatus() {
        const payoutId = document.getElementById('payoutId').value;
        if (!payoutId) {
          alert('Please enter a payout ID');
          return;
        }

        const response = await fetch(`/api/payouts/${payoutId}`);
        const data = await response.json();
        displayResponse('payoutStatusResponse', data);
      }

      function displayResponse(elementId, data) {
        const element = document.getElementById(elementId);
        element.style.display = 'block';
        element.textContent = JSON.stringify(data, null, 2);
      }
    </script>
  </body>
</html>
```

**Step 7: Update package.json**

```json
{
  "name": "payram-express-starter",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node index.js",
    "dev": "node --watch index.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "payram": "latest"
  }
}
```

**Step 8: Run Application**

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with real credentials
nano .env

# Start server
npm start

# Open browser
open http://localhost:3000
```

---

#### 2.2 Next.js Scaffold

**Quick Start:**

```bash
# Create Next.js app
npx create-next-app@latest payram-nextjs-starter --typescript --tailwind --app --no-src-dir

cd payram-nextjs-starter

# Install Payram SDK
npm install payram

# Create .env.local
cat > .env.local << 'EOF'
PAYRAM_BASE_URL=https://your-merchant.payram.com
PAYRAM_API_KEY=pk_test_your_api_key_here
EOF
```

**Create API Routes:**

**File:** `app/api/payments/create/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Payram } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function POST(request: NextRequest) {
  try {
    const {
      amount = 1,
      customerEmail = 'demo@example.com',
      customerId = 'demo',
    } = await request.json();

    const checkout = await payram.payments.initiatePayment({
      amountInUSD: Number(amount),
      customerEmail,
      customerId,
    });

    return NextResponse.json(checkout);
  } catch (error: any) {
    return NextResponse.json(
      { error: 'payment_create_failed', details: error.message },
      { status: 500 },
    );
  }
}
```

**File:** `app/api/payments/[referenceId]/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Payram } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function GET(request: NextRequest, { params }: { params: { referenceId: string } }) {
  try {
    const payment = await payram.payments.getPaymentRequest(params.referenceId);
    return NextResponse.json(payment);
  } catch (error: any) {
    return NextResponse.json(
      { error: 'payment_status_failed', details: error.message },
      { status: 500 },
    );
  }
}
```

**Similar patterns for payouts and webhooks.**

---

#### 2.3 FastAPI Scaffold

**Quick Start:**

```bash
mkdir payram-fastapi-starter
cd payram-fastapi-starter

# Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
payram==1.0.0
EOF

# Install dependencies
pip install -r requirements.txt

# Create .env
cat > .env << 'EOF'
PAYRAM_BASE_URL=https://your-merchant.payram.com
PAYRAM_API_KEY=pk_test_your_api_key_here
EOF
```

**File:** `main.py`

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Payram FastAPI Starter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Initialize Payram client here
# from payram import Payram
# payram = Payram(
#     api_key=os.getenv('PAYRAM_API_KEY'),
#     base_url=os.getenv('PAYRAM_BASE_URL')
# )

class PaymentRequest(BaseModel):
    amount: float = 1.0
    customerEmail: str = "demo@example.com"
    customerId: str = "demo-customer"

class PayoutRequest(BaseModel):
    amount: str = "1"
    currencyCode: str = "USDT"
    blockchainCode: str = "ETH"
    customerID: str = "demo-customer"
    email: str = "merchant@example.com"
    toAddress: str = "0xfeedfacecafebeefdeadbeefdeadbeefdeadbeef"
    mobileNumber: str = "+15555555555"
    residentialAddress: str = "123 Main St"

@app.post("/api/payments/create")
async def create_payment(req: PaymentRequest):
    try:
        # TODO: Call payram.payments.initiate_payment(...)
        return {"message": "Payment endpoint - implement with Payram SDK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/payments/{reference_id}")
async def get_payment_status(reference_id: str):
    try:
        # TODO: Call payram.payments.get_payment_request(reference_id)
        return {"message": "Payment status endpoint - implement with Payram SDK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/payouts/create")
async def create_payout(req: PayoutRequest):
    try:
        # TODO: Call payram.payouts.create_payout(...)
        return {"message": "Payout endpoint - implement with Payram SDK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/payouts/{payout_id}")
async def get_payout_status(payout_id: int):
    try:
        # TODO: Call payram.payouts.get_payout_by_id(payout_id)
        return {"message": "Payout status endpoint - implement with Payram SDK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/payram/webhook")
async def handle_webhook(payload: dict):
    print("Webhook received:", payload)
    return {"message": "Webhook received successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run:**

```bash
python main.py
# or
uvicorn main:app --reload
```

---

### Part 3: Common Patterns

#### 3.1 Error Handling

All scaffolds should include:

```javascript
try {
  const result = await payram.payments.initiatePayment(...);
  return success(result);
} catch (error) {
  console.error('Payram API error:', error);
  return error_response({
    error: 'operation_failed',
    details: error.message,
    // Don't expose internal errors to clients
  });
}
```

#### 3.2 Environment Validation

Check configuration on startup:

```javascript
if (!process.env.PAYRAM_BASE_URL || !process.env.PAYRAM_API_KEY) {
  console.error('ERROR: Payram environment variables not configured');
  console.error('Please copy .env.example to .env and fill in your credentials');
  process.exit(1);
}
```

#### 3.3 CORS Configuration

Allow frontend to call APIs:

```javascript
app.use(
  cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
    methods: ['GET', 'POST'],
    credentials: true,
  }),
);
```

---

## Best Practices

### 1. Never Commit Credentials

```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# Always provide .env.example
cp .env .env.example
# Replace values with placeholders in .env.example
```

### 2. Use Environment-Specific Configuration

```
.env.development   # Local development
.env.test          # Testing
.env.production    # Production (managed via deployment)
```

### 3. Add Health Check Endpoint

```javascript
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    payramConfigured: !!(process.env.PAYRAM_BASE_URL && process.env.PAYRAM_API_KEY),
  });
});
```

### 4. Log API Interactions

```javascript
console.log('[Payram] Creating payment:', {
  amount,
  customerId,
  timestamp: new Date().toISOString(),
});
```

### 5. Validate Input

```javascript
if (!amount || amount <= 0) {
  return res.status(400).json({ error: 'Invalid amount' });
}

if (!customerId || customerId.trim().length === 0) {
  return res.status(400).json({ error: 'Customer ID required' });
}
```

---

## Troubleshooting

### Port Already in Use

**Error:** `EADDRINUSE: address already in use`

**Solution:**

```bash
# Find process using port
lsof -ti:3000

# Kill process
kill -9 $(lsof -ti:3000)

# Or use different port
PORT=3001 npm start
```

### Module Not Found

**Error:** `Cannot find module 'payram'`

**Solution:**

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Environment Variables Not Loading

**Cause:** .env file not in project root or not loaded.

**Solution:**

```bash
# Check file exists
ls -la .env

# Verify dotenv is loaded
# Add to top of your main file:
require('dotenv').config(); // CommonJS
# or
import 'dotenv/config';     // ESM
```

---

## Related Skills

- **setup-payram**: Configure credentials after scaffolding
- **integrate-payments**: Understand payment patterns used in scaffolds
- **integrate-payouts**: Understand payout patterns
- **handle-webhooks**: Enhance webhook handlers in scaffolds

---

## Summary

You now know how to scaffold complete Payram applications:

1. **Express**: Node.js with simple file structure
2. **Next.js**: React with App Router and API routes
3. **FastAPI**: Python async web framework
4. **Laravel**: PHP MVC framework (similar patterns)
5. **Gin**: Go web framework (similar patterns)
6. **Spring Boot**: Java enterprise framework (similar patterns)

**All scaffolds include:**

- Payment creation and status checking
- Payout creation and status checking
- Webhook handling (optional)
- Web console for testing
- Environment configuration
- Error handling

**Next Steps:**

- Choose your framework
- Follow framework-specific instructions
- Copy .env.example to .env and configure
- Run the application
- Test via web console
- Customize for your needs
