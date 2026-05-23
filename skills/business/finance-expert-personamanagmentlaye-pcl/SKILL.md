---
name: finance-expert
version: 1.0.0
description: Expert-level financial systems, FinTech, banking, payments, and financial technology
category: domains
tags: [finance, fintech, banking, payments, trading, accounting]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(*)
---

# Finance Expert

Expert guidance for financial systems, FinTech applications, banking platforms, payment processing, and financial technology development.

## Core Concepts

### Financial Systems
- Core banking systems
- Payment processing
- Trading platforms
- Risk management
- Regulatory compliance (PCI-DSS, SOX, Basel III)
- Financial reporting

### FinTech Stack
- Payment gateways (Stripe, PayPal, Square)
- Banking APIs (Plaid, Yodlee)
- Blockchain/crypto
- Open Banking APIs
- Mobile banking
- Digital wallets

### Key Challenges
- Security and fraud prevention
- Real-time processing
- High availability (99.999%)
- Regulatory compliance
- Data privacy
- Transaction accuracy

## Payment Processing

```python
# Payment gateway integration (Stripe)
import stripe
from decimal import Decimal

stripe.api_key = "sk_test_..."

class PaymentService:
    def create_payment_intent(self, amount: Decimal, currency: str = "usd"):
        """Create payment intent with idempotency"""
        return stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            payment_method_types=["card"],
            metadata={"order_id": "12345"}
        )

    def process_refund(self, payment_intent_id: str, amount: Decimal = None):
        """Process full or partial refund"""
        return stripe.Refund.create(
            payment_intent=payment_intent_id,
            amount=int(amount * 100) if amount else None
        )

    def handle_webhook(self, payload: str, signature: str):
        """Handle Stripe webhook events"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )

            if event.type == "payment_intent.succeeded":
                payment_intent = event.data.object
                self.handle_successful_payment(payment_intent)
            elif event.type == "payment_intent.payment_failed":
                payment_intent = event.data.object
                self.handle_failed_payment(payment_intent)

            return {"status": "success"}
        except ValueError:
            return {"status": "invalid_payload"}
```

## Banking Integration

```python
# Open Banking API integration (Plaid)
from plaid import Client
from plaid.errors import PlaidError

class BankingService:
    def __init__(self):
        self.client = Client(
            client_id="...",
            secret="...",
            environment="sandbox"
        )

    def create_link_token(self, user_id: str):
        """Create link token for Plaid Link"""
        response = self.client.LinkToken.create({
            "user": {"client_user_id": user_id},
            "client_name": "My App",
            "products": ["auth", "transactions"],
            "country_codes": ["US"],
            "language": "en"
        })
        return response["link_token"]

    def exchange_public_token(self, public_token: str):
        """Exchange public token for access token"""
        response = self.client.Item.public_token.exchange(public_token)
        return {
            "access_token": response["access_token"],
            "item_id": response["item_id"]
        }

    def get_accounts(self, access_token: str):
        """Get user's bank accounts"""
        response = self.client.Accounts.get(access_token)
        return response["accounts"]

    def get_transactions(self, access_token: str, start_date: str, end_date: str):
        """Get transactions for date range"""
        response = self.client.Transactions.get(
            access_token,
            start_date,
            end_date
        )
        return response["transactions"]
```

## Financial Calculations

```python
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta

class FinancialCalculator:
    @staticmethod
    def calculate_interest(principal: Decimal, rate: Decimal, periods: int) -> Decimal:
        """Calculate compound interest"""
        return principal * ((1 + rate) ** periods - 1)

    @staticmethod
    def calculate_loan_payment(principal: Decimal, annual_rate: Decimal, months: int) -> Decimal:
        """Calculate monthly loan payment (amortization)"""
        monthly_rate = annual_rate / 12
        payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
                  ((1 + monthly_rate) ** months - 1)
        return payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @staticmethod
    def calculate_npv(cash_flows: list[Decimal], discount_rate: Decimal) -> Decimal:
        """Calculate Net Present Value"""
        npv = Decimal('0')
        for i, cf in enumerate(cash_flows):
            npv += cf / ((1 + discount_rate) ** i)
        return npv.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @staticmethod
    def calculate_roi(gain: Decimal, cost: Decimal) -> Decimal:
        """Calculate Return on Investment"""
        return ((gain - cost) / cost * 100).quantize(Decimal('0.01'))
```

## Fraud Detection

```python
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class FraudDetectionService:
    def __init__(self):
        self.model = RandomForestClassifier()

    def extract_features(self, transaction: dict) -> dict:
        """Extract features for fraud detection"""
        return {
            "amount": transaction["amount"],
            "hour_of_day": transaction["timestamp"].hour,
            "day_of_week": transaction["timestamp"].weekday(),
            "merchant_category": transaction["merchant_category"],
            "is_international": transaction["is_international"],
            "card_present": transaction["card_present"],
            "transaction_velocity_1h": self.get_velocity(transaction, hours=1),
            "transaction_velocity_24h": self.get_velocity(transaction, hours=24)
        }

    def predict_fraud(self, transaction: dict) -> dict:
        """Predict if transaction is fraudulent"""
        features = self.extract_features(transaction)
        fraud_probability = self.model.predict_proba([features])[0][1]

        return {
            "is_fraud": fraud_probability > 0.8,
            "fraud_score": fraud_probability,
            "risk_level": self.get_risk_level(fraud_probability)
        }

    def get_risk_level(self, score: float) -> str:
        if score > 0.9:
            return "CRITICAL"
        elif score > 0.7:
            return "HIGH"
        elif score > 0.5:
            return "MEDIUM"
        else:
            return "LOW"
```

## Regulatory Compliance

```python
# PCI-DSS Compliance
class PCICompliantPaymentHandler:
    def process_payment(self, card_data: dict):
        # Never store full card number, CVV, or PIN
        # Tokenize card data immediately
        token = self.tokenize_card(card_data)

        # Store only last 4 digits and token
        payment_record = {
            "token": token,
            "last_4": card_data["number"][-4:],
            "exp_month": card_data["exp_month"],
            "exp_year": card_data["exp_year"]
        }

        return self.process_with_token(token)

    def tokenize_card(self, card_data: dict) -> str:
        # Use payment gateway tokenization
        return stripe.Token.create(card=card_data)["id"]

# KYC/AML Compliance
class ComplianceService:
    def verify_customer(self, customer_data: dict) -> dict:
        """Perform KYC verification"""
        # Identity verification
        identity_verified = self.verify_identity(customer_data)

        # Sanctions screening
        sanctions_clear = self.screen_sanctions(customer_data)

        # Risk assessment
        risk_level = self.assess_risk(customer_data)

        return {
            "verified": identity_verified and sanctions_clear,
            "risk_level": risk_level,
            "requires_manual_review": risk_level == "HIGH"
        }
```

## Best Practices

### Security
- Never log sensitive financial data (PAN, CVV)
- Use tokenization for card storage
- Implement strong encryption (AES-256)
- Use TLS 1.2+ for all communications
- Implement rate limiting and fraud detection
- Regular security audits

### Data Handling
- Use Decimal type for money (never float)
- Store amounts in smallest currency unit (cents)
- Implement idempotency for all transactions
- Maintain complete audit trails
- Handle timezone conversions properly

### Transaction Processing
- Implement two-phase commits
- Use database transactions (ACID)
- Handle network failures gracefully
- Implement retry logic with exponential backoff
- Support transaction reversals and refunds

## Anti-Patterns

❌ Using float for money calculations
❌ Storing credit card data unencrypted
❌ No transaction logging/audit trail
❌ Synchronous payment processing
❌ No idempotency in payment APIs
❌ Ignoring PCI-DSS compliance
❌ No fraud detection

## Resources

- PCI-DSS: https://www.pcisecuritystandards.org/
- Stripe API: https://stripe.com/docs/api
- Plaid: https://plaid.com/docs/
- Open Banking: https://www.openbanking.org.uk/
