---
name: banking-expert
version: 1.0.0
description: Expert-level banking systems, core banking, regulations, and banking technology
category: professional
tags: [banking, finance, core-banking, regulations, payments]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Banking Expert

Expert guidance for banking systems, core banking platforms, regulatory compliance, and banking technology.

## Core Concepts

### Banking Systems
- Core banking systems (CBS)
- Account management
- Transaction processing
- Payment systems (ACH, SWIFT, SEPA)
- Loan management
- Risk management systems

### Regulations
- Basel III/IV capital requirements
- Know Your Customer (KYC)
- Anti-Money Laundering (AML)
- GDPR for banking
- PSD2 (Payment Services Directive)
- Dodd-Frank Act

### Key Technologies
- Real-time payment processing
- Mobile banking
- Open banking APIs
- Digital wallets
- Blockchain in banking
- AI for fraud detection

## Account Management

```python
from decimal import Decimal
from datetime import datetime
from enum import Enum

class AccountType(Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"
    LOAN = "loan"

class Account:
    def __init__(self, account_number: str, account_type: AccountType,
                 customer_id: str, balance: Decimal = Decimal('0')):
        self.account_number = account_number
        self.type = account_type
        self.customer_id = customer_id
        self.balance = balance
        self.status = "ACTIVE"
        self.created_at = datetime.now()

    def deposit(self, amount: Decimal) -> dict:
        """Deposit funds with validation"""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.balance += amount

        return {
            "transaction_id": self.generate_transaction_id(),
            "type": "DEPOSIT",
            "amount": amount,
            "balance": self.balance,
            "timestamp": datetime.now()
        }

    def withdraw(self, amount: Decimal) -> dict:
        """Withdraw funds with balance check"""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if self.balance < amount:
            raise ValueError("Insufficient funds")

        self.balance -= amount

        return {
            "transaction_id": self.generate_transaction_id(),
            "type": "WITHDRAWAL",
            "amount": amount,
            "balance": self.balance,
            "timestamp": datetime.now()
        }

    def transfer(self, to_account: 'Account', amount: Decimal) -> dict:
        """Transfer funds between accounts"""
        # Withdraw from source
        withdrawal = self.withdraw(amount)

        try:
            # Deposit to destination
            deposit = to_account.deposit(amount)

            return {
                "transaction_id": self.generate_transaction_id(),
                "type": "TRANSFER",
                "from_account": self.account_number,
                "to_account": to_account.account_number,
                "amount": amount,
                "timestamp": datetime.now()
            }
        except Exception as e:
            # Rollback on failure
            self.deposit(amount)
            raise e
```

## KYC/AML Compliance

```python
class KYCService:
    def verify_customer(self, customer_data: dict) -> dict:
        """Perform KYC verification"""
        verification_results = {
            "identity_verified": False,
            "address_verified": False,
            "sanctions_clear": False,
            "pep_check_clear": False,
            "risk_level": "HIGH"
        }

        # Identity verification
        verification_results["identity_verified"] = self.verify_identity(
            customer_data["id_document"]
        )

        # Address verification
        verification_results["address_verified"] = self.verify_address(
            customer_data["proof_of_address"]
        )

        # Sanctions screening
        verification_results["sanctions_clear"] = self.screen_sanctions(
            customer_data["name"],
            customer_data["date_of_birth"]
        )

        # PEP (Politically Exposed Person) check
        verification_results["pep_check_clear"] = self.check_pep(
            customer_data["name"]
        )

        # Calculate risk level
        verification_results["risk_level"] = self.calculate_risk_level(
            verification_results
        )

        return verification_results

class AMLMonitoring:
    def monitor_transaction(self, transaction: dict) -> dict:
        """Monitor transaction for suspicious activity"""
        flags = []

        # Large transaction
        if transaction["amount"] > 10000:
            flags.append("LARGE_TRANSACTION")

        # Rapid succession of transactions
        if self.check_velocity(transaction["account_id"]):
            flags.append("HIGH_VELOCITY")

        # Unusual pattern
        if self.check_pattern(transaction):
            flags.append("UNUSUAL_PATTERN")

        # International transfer to high-risk country
        if transaction.get("international") and \
           self.is_high_risk_country(transaction.get("destination")):
            flags.append("HIGH_RISK_COUNTRY")

        if flags:
            self.file_suspicious_activity_report(transaction, flags)

        return {
            "flagged": len(flags) > 0,
            "flags": flags,
            "risk_score": self.calculate_aml_risk_score(flags)
        }
```

## Payment Processing

```python
class PaymentProcessor:
    def process_ach_payment(self, payment: dict) -> dict:
        """Process ACH payment"""
        # Validate routing and account numbers
        if not self.validate_routing_number(payment["routing_number"]):
            raise ValueError("Invalid routing number")

        # Create ACH file
        ach_batch = self.create_ach_batch([payment])

        # Submit to ACH network
        submission_result = self.submit_to_ach_network(ach_batch)

        return {
            "payment_id": payment["id"],
            "status": "PENDING",
            "expected_settlement": self.calculate_settlement_date(),
            "trace_number": submission_result["trace_number"]
        }

    def process_wire_transfer(self, wire: dict) -> dict:
        """Process SWIFT wire transfer"""
        # Generate SWIFT message
        swift_message = self.create_swift_mt103(wire)

        # Send via SWIFT network
        result = self.send_swift_message(swift_message)

        return {
            "wire_id": wire["id"],
            "status": "SENT",
            "swift_reference": result["reference"],
            "fee": self.calculate_wire_fee(wire["amount"])
        }
```

## Interest Calculation

```python
class InterestCalculator:
    @staticmethod
    def calculate_simple_interest(principal: Decimal, rate: Decimal,
                                  days: int) -> Decimal:
        """Calculate simple interest"""
        return principal * rate * days / 365

    @staticmethod
    def calculate_compound_interest(principal: Decimal, annual_rate: Decimal,
                                   years: int, compounds_per_year: int = 12) -> Decimal:
        """Calculate compound interest"""
        rate_per_period = annual_rate / compounds_per_year
        num_periods = years * compounds_per_year

        return principal * ((1 + rate_per_period) ** num_periods - 1)

    @staticmethod
    def calculate_loan_payment(principal: Decimal, annual_rate: Decimal,
                              months: int) -> Decimal:
        """Calculate monthly loan payment"""
        monthly_rate = annual_rate / 12

        payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
                  ((1 + monthly_rate) ** months - 1)

        return payment.quantize(Decimal('0.01'))
```

## Best Practices

- Implement two-factor authentication
- Use encryption for sensitive data (at rest and in transit)
- Maintain complete audit trails
- Implement real-time fraud detection
- Ensure ACID compliance for transactions
- Regular security audits and penetration testing
- Implement rate limiting on APIs
- Use tokenization for sensitive data
- Maintain disaster recovery and business continuity plans
- Regular regulatory compliance reviews

## Anti-Patterns

❌ Storing sensitive data unencrypted
❌ No transaction logging/audit trail
❌ Synchronous payment processing
❌ Ignoring regulatory compliance
❌ No fraud detection mechanisms
❌ Using floats for money calculations
❌ No backup and recovery procedures

## Resources

- Basel Committee: https://www.bis.org/bcbs/
- SWIFT Standards: https://www.swift.com/standards
- PSD2: https://ec.europa.eu/info/law/payment-services-psd-2
- FFIEC: https://www.ffiec.gov/
