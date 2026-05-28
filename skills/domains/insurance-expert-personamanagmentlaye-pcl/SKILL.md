---
name: insurance-expert
version: 1.0.0
description: Expert-level insurance systems, underwriting, claims processing, actuarial analysis, risk assessment, and insurtech solutions
category: domains
tags: [insurance, underwriting, claims, actuarial, risk, insurtech]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Insurance Expert

Expert guidance for insurance systems, underwriting, claims processing, actuarial analysis, risk assessment, fraud detection, and modern insurtech solutions.

## Core Concepts

### Insurance Systems
- Policy Administration Systems (PAS)
- Claims Management Systems
- Underwriting workstations
- Actuarial modeling systems
- Reinsurance management
- Agency management systems
- Document management

### Insurance Types
- Property & Casualty (P&C)
- Life insurance
- Health insurance
- Auto insurance
- Commercial insurance
- Specialty insurance
- Cyber insurance

### Standards and Regulations
- ACORD standards (insurance data exchange)
- SOX compliance
- State insurance regulations
- NAIC (National Association of Insurance Commissioners)
- GDPR for customer data
- Anti-money laundering (AML)

## Policy Administration System

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional
from enum import Enum

class PolicyStatus(Enum):
    QUOTED = "quoted"
    BOUND = "bound"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    LAPSED = "lapsed"

class CoverageType(Enum):
    LIABILITY = "liability"
    COLLISION = "collision"
    COMPREHENSIVE = "comprehensive"
    MEDICAL = "medical"
    UNINSURED_MOTORIST = "uninsured_motorist"

@dataclass
class Insured:
    """Insured party information"""
    insured_id: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: dict
    phone: str
    email: str
    drivers_license: str
    credit_score: int

@dataclass
class Coverage:
    """Insurance coverage details"""
    coverage_type: CoverageType
    limit: Decimal
    deductible: Decimal
    premium: Decimal

@dataclass
class Policy:
    """Insurance policy"""
    policy_number: str
    insured: Insured
    policy_type: str  # 'auto', 'home', 'life', etc.
    effective_date: datetime
    expiration_date: datetime
    status: PolicyStatus
    coverages: List[Coverage]
    total_premium: Decimal
    payment_plan: str  # 'annual', 'semi-annual', 'quarterly', 'monthly'
    underwriter_id: str
    risk_score: float

class PolicyAdministrationSystem:
    """Policy administration and management"""

    def __init__(self):
        self.policies = {}
        self.quotes = {}

    def generate_quote(self, application: dict) -> dict:
        """Generate insurance quote"""
        # Extract applicant information
        insured = Insured(
            insured_id=self._generate_id(),
            first_name=application['first_name'],
            last_name=application['last_name'],
            date_of_birth=application['date_of_birth'],
            address=application['address'],
            phone=application['phone'],
            email=application['email'],
            drivers_license=application.get('drivers_license', ''),
            credit_score=application.get('credit_score', 700)
        )

        # Calculate risk score
        risk_score = self._calculate_risk_score(insured, application)

        # Determine coverages and premiums
        coverages = self._determine_coverages(application, risk_score)

        # Calculate total premium
        total_premium = sum(c.premium for c in coverages)

        # Apply discounts
        discounts = self._calculate_discounts(application)
        discount_amount = total_premium * (sum(discounts.values()) / 100)
        total_premium = total_premium - discount_amount

        quote = {
            'quote_id': self._generate_id(),
            'insured': insured,
            'policy_type': application['policy_type'],
            'coverages': coverages,
            'total_premium': total_premium,
            'risk_score': risk_score,
            'discounts': discounts,
            'valid_until': datetime.now() + timedelta(days=30)
        }

        self.quotes[quote['quote_id']] = quote

        return quote

    def _calculate_risk_score(self, insured: Insured, application: dict) -> float:
        """Calculate risk score for underwriting"""
        score = 50.0  # Base score

        # Age factor (auto insurance)
        age = (datetime.now() - insured.date_of_birth).days / 365.25
        if age < 25:
            score += 20
        elif age < 65:
            score -= 10
        else:
            score += 5

        # Credit score factor
        if insured.credit_score < 600:
            score += 15
        elif insured.credit_score > 750:
            score -= 10

        # Driving history (auto insurance)
        if application.get('accidents_3yr', 0) > 0:
            score += application['accidents_3yr'] * 10

        if application.get('violations_3yr', 0) > 0:
            score += application['violations_3yr'] * 5

        # Claims history
        if application.get('claims_5yr', 0) > 0:
            score += application['claims_5yr'] * 8

        return max(0, min(100, score))  # Normalize to 0-100

    def _determine_coverages(self, application: dict, risk_score: float) -> List[Coverage]:
        """Determine coverages and calculate premiums"""
        coverages = []
        base_rate = Decimal('500')

        # Risk multiplier
        risk_multiplier = Decimal(str(1 + (risk_score / 100)))

        if application['policy_type'] == 'auto':
            # Liability coverage (required)
            coverages.append(Coverage(
                coverage_type=CoverageType.LIABILITY,
                limit=Decimal('100000'),
                deductible=Decimal('0'),
                premium=base_rate * risk_multiplier
            ))

            # Collision coverage
            if application.get('include_collision', True):
                deductible = Decimal(str(application.get('collision_deductible', 500)))
                premium = base_rate * Decimal('0.6') * risk_multiplier
                # Adjust premium based on deductible
                premium = premium * (Decimal('1000') / deductible) * Decimal('0.5')

                coverages.append(Coverage(
                    coverage_type=CoverageType.COLLISION,
                    limit=Decimal(str(application.get('vehicle_value', 25000))),
                    deductible=deductible,
                    premium=premium
                ))

            # Comprehensive coverage
            if application.get('include_comprehensive', True):
                deductible = Decimal(str(application.get('comprehensive_deductible', 500)))
                premium = base_rate * Decimal('0.3') * risk_multiplier

                coverages.append(Coverage(
                    coverage_type=CoverageType.COMPREHENSIVE,
                    limit=Decimal(str(application.get('vehicle_value', 25000))),
                    deductible=deductible,
                    premium=premium
                ))

        return coverages

    def _calculate_discounts(self, application: dict) -> dict:
        """Calculate applicable discounts"""
        discounts = {}

        # Multi-policy discount
        if application.get('has_other_policies', False):
            discounts['multi_policy'] = 15  # 15%

        # Good driver discount
        if application.get('accidents_3yr', 0) == 0 and application.get('violations_3yr', 0) == 0:
            discounts['good_driver'] = 10  # 10%

        # Safety features discount
        if application.get('has_airbags', False):
            discounts['safety_features'] = 5  # 5%

        # Anti-theft discount
        if application.get('has_alarm', False):
            discounts['anti_theft'] = 5  # 5%

        return discounts

    def bind_policy(self, quote_id: str) -> Policy:
        """Bind quote to create active policy"""
        quote = self.quotes.get(quote_id)
        if not quote:
            raise ValueError("Quote not found")

        # Check if quote is still valid
        if datetime.now() > quote['valid_until']:
            raise ValueError("Quote has expired")

        policy_number = self._generate_policy_number()

        policy = Policy(
            policy_number=policy_number,
            insured=quote['insured'],
            policy_type=quote['policy_type'],
            effective_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=365),
            status=PolicyStatus.ACTIVE,
            coverages=quote['coverages'],
            total_premium=quote['total_premium'],
            payment_plan='annual',
            underwriter_id='UW001',
            risk_score=quote['risk_score']
        )

        self.policies[policy_number] = policy

        return policy

    def renew_policy(self, policy_number: str) -> dict:
        """Renew existing policy"""
        policy = self.policies.get(policy_number)
        if not policy:
            return {'error': 'Policy not found'}

        # Re-evaluate risk and premium
        # In production, would pull updated data
        new_risk_score = policy.risk_score * 0.95  # Loyalty discount factor

        # Calculate new premium (with inflation adjustment)
        inflation_factor = Decimal('1.03')  # 3% increase
        new_premium = policy.total_premium * inflation_factor * Decimal(str(0.95))  # Renewal discount

        return {
            'policy_number': policy_number,
            'current_premium': float(policy.total_premium),
            'renewal_premium': float(new_premium),
            'effective_date': policy.expiration_date,
            'expiration_date': policy.expiration_date + timedelta(days=365)
        }

    def cancel_policy(self, policy_number: str, reason: str, effective_date: datetime = None) -> dict:
        """Cancel policy"""
        policy = self.policies.get(policy_number)
        if not policy:
            return {'error': 'Policy not found'}

        if effective_date is None:
            effective_date = datetime.now()

        # Calculate earned premium
        days_active = (effective_date - policy.effective_date).days
        total_days = (policy.expiration_date - policy.effective_date).days
        earned_premium = policy.total_premium * (Decimal(days_active) / Decimal(total_days))

        # Calculate refund
        refund_amount = policy.total_premium - earned_premium

        policy.status = PolicyStatus.CANCELLED

        return {
            'policy_number': policy_number,
            'cancellation_date': effective_date.isoformat(),
            'reason': reason,
            'earned_premium': float(earned_premium),
            'refund_amount': float(refund_amount)
        }

    def _generate_policy_number(self) -> str:
        """Generate unique policy number"""
        import uuid
        return f"POL-{uuid.uuid4().hex[:10].upper()}"

    def _generate_id(self) -> str:
        import uuid
        return uuid.uuid4().hex[:12].upper()
```

## Claims Management System

```python
from enum import Enum

class ClaimStatus(Enum):
    REPORTED = "reported"
    INVESTIGATING = "investigating"
    APPROVED = "approved"
    DENIED = "denied"
    CLOSED = "closed"

@dataclass
class Claim:
    """Insurance claim"""
    claim_number: str
    policy_number: str
    claim_type: str  # 'collision', 'theft', 'liability', etc.
    date_of_loss: datetime
    reported_date: datetime
    description: str
    estimated_loss: Decimal
    status: ClaimStatus
    adjuster_id: Optional[str]
    reserve_amount: Decimal
    paid_amount: Decimal
    deductible: Decimal

class ClaimsManagementSystem:
    """Claims processing and management"""

    def __init__(self):
        self.claims = {}
        self.fraud_detector = FraudDetectionSystem()

    def file_claim(self, claim_data: dict) -> Claim:
        """File new insurance claim"""
        claim_number = self._generate_claim_number()

        claim = Claim(
            claim_number=claim_number,
            policy_number=claim_data['policy_number'],
            claim_type=claim_data['claim_type'],
            date_of_loss=claim_data['date_of_loss'],
            reported_date=datetime.now(),
            description=claim_data['description'],
            estimated_loss=Decimal(str(claim_data.get('estimated_loss', 0))),
            status=ClaimStatus.REPORTED,
            adjuster_id=None,
            reserve_amount=Decimal('0'),
            deductible=Decimal(str(claim_data.get('deductible', 0))),
            paid_amount=Decimal('0')
        )

        # Fraud detection screening
        fraud_result = self.fraud_detector.screen_claim(claim)
        if fraud_result['fraud_score'] > 0.8:
            claim.status = ClaimStatus.INVESTIGATING
            self._flag_for_siu(claim, fraud_result)  # Special Investigation Unit

        # Auto-assign adjuster
        claim.adjuster_id = self._assign_adjuster(claim)

        # Set reserve amount
        claim.reserve_amount = self._calculate_reserve(claim)

        self.claims[claim_number] = claim

        return claim

    def investigate_claim(self, claim_number: str) -> dict:
        """Investigate claim details"""
        claim = self.claims.get(claim_number)
        if not claim:
            return {'error': 'Claim not found'}

        claim.status = ClaimStatus.INVESTIGATING

        # Gather evidence
        investigation_steps = [
            'Review policy coverage',
            'Verify loss details',
            'Inspect damage',
            'Review police report (if applicable)',
            'Interview claimant',
            'Review medical records (if applicable)',
            'Obtain repair estimates'
        ]

        return {
            'claim_number': claim_number,
            'status': claim.status.value,
            'investigation_steps': investigation_steps,
            'estimated_completion': (datetime.now() + timedelta(days=14)).isoformat()
        }

    def approve_claim(self, claim_number: str, approved_amount: Decimal) -> dict:
        """Approve claim for payment"""
        claim = self.claims.get(claim_number)
        if not claim:
            return {'error': 'Claim not found'}

        # Validate coverage
        if not self._validate_coverage(claim):
            return {'error': 'Loss not covered under policy'}

        # Apply deductible
        payment_amount = approved_amount - claim.deductible
        if payment_amount <= 0:
            return {'error': 'Approved amount does not exceed deductible'}

        claim.status = ClaimStatus.APPROVED
        claim.paid_amount = payment_amount

        # Process payment
        payment_result = self._process_payment(claim, payment_amount)

        return {
            'claim_number': claim_number,
            'approved_amount': float(approved_amount),
            'deductible': float(claim.deductible),
            'payment_amount': float(payment_amount),
            'payment_method': payment_result['method'],
            'payment_date': datetime.now().isoformat()
        }

    def deny_claim(self, claim_number: str, reason: str) -> dict:
        """Deny claim"""
        claim = self.claims.get(claim_number)
        if not claim:
            return {'error': 'Claim not found'}

        claim.status = ClaimStatus.DENIED

        # Send denial letter
        self._send_denial_letter(claim, reason)

        return {
            'claim_number': claim_number,
            'status': 'denied',
            'reason': reason,
            'appeal_deadline': (datetime.now() + timedelta(days=60)).isoformat()
        }

    def _calculate_reserve(self, claim: Claim) -> Decimal:
        """Calculate reserve amount for claim"""
        # Reserve is an estimate of total claim cost
        # Based on claim type and severity
        reserve_multipliers = {
            'collision': Decimal('1.5'),
            'theft': Decimal('1.3'),
            'liability': Decimal('2.0'),
            'comprehensive': Decimal('1.4')
        }

        multiplier = reserve_multipliers.get(claim.claim_type, Decimal('1.5'))
        reserve = claim.estimated_loss * multiplier

        return reserve

    def _assign_adjuster(self, claim: Claim) -> str:
        """Auto-assign claim to adjuster"""
        # Would use load balancing and expertise matching
        return "ADJ001"

    def _validate_coverage(self, claim: Claim) -> bool:
        """Validate that loss is covered under policy"""
        # Would check policy coverages against claim type
        return True

    def _process_payment(self, claim: Claim, amount: Decimal) -> dict:
        """Process claim payment"""
        # Integration with payment system
        return {'method': 'direct_deposit', 'transaction_id': 'TXN123'}

    def _flag_for_siu(self, claim: Claim, fraud_result: dict):
        """Flag claim for Special Investigation Unit"""
        # Implementation would notify SIU
        pass

    def _send_denial_letter(self, claim: Claim, reason: str):
        """Send claim denial letter"""
        # Implementation would generate and send letter
        pass

    def _generate_claim_number(self) -> str:
        import uuid
        return f"CLM-{uuid.uuid4().hex[:10].upper()}"

class FraudDetectionSystem:
    """Fraud detection for claims"""

    def screen_claim(self, claim: Claim) -> dict:
        """Screen claim for fraud indicators"""
        fraud_score = 0.0
        indicators = []

        # Check for suspicious patterns
        # Late reporting
        days_to_report = (claim.reported_date - claim.date_of_loss).days
        if days_to_report > 30:
            fraud_score += 0.2
            indicators.append('Late reporting')

        # High loss amount
        if claim.estimated_loss > Decimal('50000'):
            fraud_score += 0.15
            indicators.append('High loss amount')

        # Multiple claims (would check historical data)
        # Implementation would query claim history

        return {
            'fraud_score': fraud_score,
            'indicators': indicators,
            'recommendation': 'investigate' if fraud_score > 0.5 else 'proceed'
        }
```

## Actuarial Analysis

```python
import numpy as np
from scipy import stats

class ActuarialAnalysis:
    """Actuarial modeling and analysis"""

    def calculate_loss_ratio(self,
                            total_claims_paid: Decimal,
                            total_premiums_earned: Decimal) -> dict:
        """Calculate loss ratio"""
        if total_premiums_earned == 0:
            return {'error': 'No premiums earned'}

        loss_ratio = (total_claims_paid / total_premiums_earned) * 100

        # Interpret loss ratio
        if loss_ratio < 60:
            assessment = "Profitable"
        elif loss_ratio < 75:
            assessment = "Target range"
        elif loss_ratio < 100:
            assessment = "Unprofitable"
        else:
            assessment = "Significant losses"

        return {
            'loss_ratio': float(loss_ratio),
            'claims_paid': float(total_claims_paid),
            'premiums_earned': float(total_premiums_earned),
            'assessment': assessment
        }

    def calculate_combined_ratio(self,
                                 loss_ratio: float,
                                 expense_ratio: float) -> dict:
        """Calculate combined ratio"""
        combined_ratio = loss_ratio + expense_ratio

        profitable = combined_ratio < 100

        return {
            'combined_ratio': combined_ratio,
            'loss_ratio': loss_ratio,
            'expense_ratio': expense_ratio,
            'profitable': profitable,
            'underwriting_gain_loss': 100 - combined_ratio
        }

    def estimate_reserves(self, claim_data: List[dict]) -> dict:
        """Estimate loss reserves using chain ladder method"""
        # Simplified chain ladder method
        # In production, would use more sophisticated methods

        open_claims = [c for c in claim_data if c['status'] != 'closed']
        total_incurred = sum(c['paid_amount'] + c['reserve'] for c in open_claims)

        return {
            'total_reserve': total_incurred,
            'open_claim_count': len(open_claims),
            'method': 'chain_ladder'
        }

    def price_product(self,
                     expected_claims: Decimal,
                     expense_ratio: float,
                     profit_margin: float) -> Decimal:
        """Calculate premium for insurance product"""
        # Pure premium (expected losses)
        pure_premium = expected_claims

        # Load for expenses
        expense_load = pure_premium * Decimal(str(expense_ratio / 100))

        # Load for profit
        profit_load = pure_premium * Decimal(str(profit_margin / 100))

        # Total premium
        total_premium = pure_premium + expense_load + profit_load

        return total_premium.quantize(Decimal('0.01'))
```

## Best Practices

### Underwriting
- Use consistent risk assessment criteria
- Implement automated underwriting for simple cases
- Maintain underwriting guidelines documentation
- Use predictive analytics for risk scoring
- Conduct regular portfolio reviews
- Segment risks appropriately
- Monitor loss ratios by segment

### Claims Processing
- Provide 24/7 claim reporting
- Assign adjusters quickly
- Set appropriate reserves
- Communicate regularly with claimants
- Implement fraud detection
- Track claim cycle time
- Use photos and video for inspections

### Fraud Prevention
- Screen all claims for fraud indicators
- Use predictive analytics
- Maintain Special Investigation Unit (SIU)
- Share fraud data industry-wide
- Train staff on fraud detection
- Implement identity verification
- Monitor for organized fraud rings

### Compliance
- Maintain state licensing
- Follow NAIC model laws
- Implement proper data privacy controls
- Conduct regular compliance audits
- Maintain required reserves
- File timely regulatory reports
- Follow fair claims practices

## Anti-Patterns

❌ Manual underwriting for all policies
❌ No fraud detection system
❌ Slow claims processing
❌ Inadequate loss reserves
❌ Poor customer communication
❌ No data analytics
❌ Ignoring regulatory changes
❌ Inconsistent underwriting decisions
❌ No claims automation

## Resources

- ACORD Standards: https://www.acord.org/
- NAIC (National Association of Insurance Commissioners): https://www.naic.org/
- ISO (Insurance Services Office): https://www.verisk.com/iso/
- Society of Actuaries: https://www.soa.org/
- Casualty Actuarial Society: https://www.casact.org/
- Insurance Information Institute: https://www.iii.org/
- A.M. Best (ratings): https://www.ambest.com/
