---
name: compliance-management
description: When the user wants to manage regulatory compliance, ensure supply chain adherence to standards, or navigate trade regulations. Also use when the user mentions "regulatory compliance," "trade compliance," "customs," "import/export regulations," "certification management," "audit management," "REACH," "RoHS," "conflict minerals," "country of origin," or "trade restrictions." For sustainability compliance, see sustainable-sourcing. For quality standards, see quality-management.
---

# Compliance Management

You are an expert in supply chain compliance and regulatory management. Your goal is to help organizations navigate complex regulatory requirements, ensure adherence to standards, manage certifications, and mitigate compliance risks across global supply chains.

## Initial Assessment

Before implementing compliance management, understand:

1. **Regulatory Landscape**
   - What industries and products are in scope?
   - Geographic regions of operation?
   - Key regulatory frameworks applicable?
   - Recent compliance issues or violations?

2. **Compliance Maturity**
   - Current compliance processes and systems?
   - Dedicated compliance resources?
   - Supplier compliance requirements?
   - Audit and monitoring frequency?

3. **Risk Exposure**
   - Penalties for non-compliance?
   - Business disruption risks?
   - Reputational impact?
   - Customer requirements and audits?

4. **Supply Chain Complexity**
   - Number of suppliers and countries?
   - Product complexity and BOM depth?
   - Regulatory classification of products?
   - Import/export volumes?

---

## Regulatory Compliance Framework

### Key Regulatory Areas

**1. Trade Compliance**
- Import/export regulations
- Customs classification (HS codes)
- Country of origin determination
- Free Trade Agreements (FTA)
- Trade sanctions and embargoes
- Export controls (EAR, ITAR)

**2. Product Safety & Restrictions**
- REACH (EU chemicals)
- RoHS (Restriction of Hazardous Substances)
- Prop 65 (California)
- TSCA (US chemical substances)
- FDA (food, drugs, medical devices)
- CPSC (Consumer Product Safety)

**3. Environmental Compliance**
- WEEE (Waste Electrical Equipment)
- Packaging regulations
- Carbon reporting requirements
- Waste management regulations
- Environmental permits

**4. Social & Ethical Compliance**
- Conflict minerals (3TG: tin, tantalum, tungsten, gold)
- Forced labor (Uyghur Forced Labor Prevention Act)
- Child labor prohibitions
- Modern Slavery Acts (UK, Australia)
- Fair Labor Standards
- Human rights due diligence

**5. Data & Privacy**
- GDPR (EU data protection)
- CCPA (California privacy)
- Data localization requirements
- Cross-border data transfers

**6. Industry-Specific**
- Pharmaceutical (GMP, GDP)
- Automotive (IATF 16949)
- Aerospace (AS9100)
- Food safety (FSMA, HACCP)
- Medical devices (ISO 13485, FDA QSR)

---

## Compliance Management System

### Regulatory Database & Tracking

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ComplianceManager:
    """Comprehensive compliance management system"""

    def __init__(self):
        self.regulations = {}
        self.products = {}
        self.suppliers = {}
        self.certifications = []
        self.compliance_violations = []

    def add_regulation(self, reg_id, regulation_name, region, category,
                      effective_date, review_frequency_days=365):
        """
        Add regulation to track

        category: 'trade', 'product_safety', 'environmental', 'social', 'data'
        """

        self.regulations[reg_id] = {
            'regulation_name': regulation_name,
            'region': region,
            'category': category,
            'effective_date': effective_date,
            'review_frequency_days': review_frequency_days,
            'last_review_date': None,
            'next_review_date': None,
            'compliance_status': 'Pending Review'
        }

    def add_product(self, product_id, product_name, hs_code, materials,
                   target_markets, applicable_regulations):
        """
        Add product and its compliance requirements

        materials: list of material components
        applicable_regulations: list of regulation IDs that apply
        """

        self.products[product_id] = {
            'product_name': product_name,
            'hs_code': hs_code,
            'materials': materials,
            'target_markets': target_markets,
            'applicable_regulations': applicable_regulations,
            'compliance_status': {},
            'certifications_required': [],
            'certifications_obtained': []
        }

        # Initialize compliance status for each regulation
        for reg_id in applicable_regulations:
            self.products[product_id]['compliance_status'][reg_id] = 'Not Assessed'

    def assess_product_compliance(self, product_id):
        """
        Assess product compliance against applicable regulations

        Returns compliance gaps and required actions
        """

        if product_id not in self.products:
            return None

        product = self.products[product_id]
        compliance_assessment = {
            'product_id': product_id,
            'product_name': product['product_name'],
            'overall_status': 'Compliant',
            'regulations_assessed': [],
            'compliance_gaps': [],
            'actions_required': []
        }

        for reg_id in product['applicable_regulations']:
            if reg_id not in self.regulations:
                continue

            regulation = self.regulations[reg_id]

            # Check specific compliance based on regulation type
            gap_found = False

            if regulation['category'] == 'product_safety':
                # Example: Check for restricted substances
                if self._check_restricted_substances(product):
                    gap_found = True
                    compliance_assessment['compliance_gaps'].append({
                        'regulation': regulation['regulation_name'],
                        'issue': 'Product contains restricted substances',
                        'severity': 'Critical'
                    })
                    compliance_assessment['actions_required'].append({
                        'action': 'Reformulate product or obtain exemption',
                        'owner': 'Product Development',
                        'timeline': '90 days'
                    })

            elif regulation['category'] == 'trade':
                # Example: Check for proper classification
                if not product['hs_code']:
                    gap_found = True
                    compliance_assessment['compliance_gaps'].append({
                        'regulation': regulation['regulation_name'],
                        'issue': 'Missing HS code classification',
                        'severity': 'High'
                    })
                    compliance_assessment['actions_required'].append({
                        'action': 'Complete customs classification',
                        'owner': 'Trade Compliance',
                        'timeline': '30 days'
                    })

            # Update status
            status = 'Non-Compliant' if gap_found else 'Compliant'
            product['compliance_status'][reg_id] = status

            compliance_assessment['regulations_assessed'].append({
                'regulation_id': reg_id,
                'regulation_name': regulation['regulation_name'],
                'status': status
            })

            if gap_found:
                compliance_assessment['overall_status'] = 'Non-Compliant'

        return compliance_assessment

    def _check_restricted_substances(self, product):
        """Check if product contains restricted substances"""

        # Simplified check - in reality would check against substance database
        restricted_materials = ['lead', 'cadmium', 'mercury', 'hexavalent_chromium']

        for material in product['materials']:
            if material.lower() in restricted_materials:
                return True

        return False

    def add_supplier(self, supplier_id, supplier_name, country,
                    certifications, audit_date=None):
        """Add supplier and track compliance"""

        self.suppliers[supplier_id] = {
            'supplier_name': supplier_name,
            'country': country,
            'certifications': certifications,
            'last_audit_date': audit_date,
            'next_audit_date': self._calculate_next_audit(audit_date),
            'audit_frequency_days': 365,
            'compliance_score': None,
            'violations': []
        }

    def _calculate_next_audit(self, last_audit_date, frequency_days=365):
        """Calculate next audit date"""
        if last_audit_date:
            if isinstance(last_audit_date, str):
                last_audit_date = datetime.strptime(last_audit_date, '%Y-%m-%d')
            return last_audit_date + timedelta(days=frequency_days)
        return None

    def track_certification(self, entity_id, entity_type, cert_name,
                          cert_number, issue_date, expiry_date, status='Active'):
        """
        Track certifications for products, suppliers, or facilities

        entity_type: 'product', 'supplier', 'facility'
        """

        self.certifications.append({
            'entity_id': entity_id,
            'entity_type': entity_type,
            'certification_name': cert_name,
            'certification_number': cert_number,
            'issue_date': issue_date,
            'expiry_date': expiry_date,
            'status': status,
            'days_to_expiry': self._calculate_days_to_expiry(expiry_date)
        })

    def _calculate_days_to_expiry(self, expiry_date):
        """Calculate days until certification expires"""
        if isinstance(expiry_date, str):
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')

        today = datetime.now()
        days = (expiry_date - today).days

        return days

    def get_expiring_certifications(self, days_threshold=90):
        """Get certifications expiring within threshold"""

        expiring = []

        for cert in self.certifications:
            if cert['days_to_expiry'] <= days_threshold and cert['days_to_expiry'] >= 0:
                urgency = 'Critical' if cert['days_to_expiry'] <= 30 else 'High' if cert['days_to_expiry'] <= 60 else 'Medium'

                expiring.append({
                    'entity_id': cert['entity_id'],
                    'entity_type': cert['entity_type'],
                    'certification': cert['certification_name'],
                    'expiry_date': cert['expiry_date'],
                    'days_remaining': cert['days_to_expiry'],
                    'urgency': urgency
                })

        # Sort by days remaining
        expiring.sort(key=lambda x: x['days_remaining'])

        return pd.DataFrame(expiring) if expiring else pd.DataFrame()

    def generate_compliance_dashboard(self):
        """Generate compliance dashboard metrics"""

        # Product compliance
        total_products = len(self.products)
        compliant_products = sum(
            1 for p in self.products.values()
            if all(status == 'Compliant' for status in p['compliance_status'].values())
        )

        # Supplier compliance
        total_suppliers = len(self.suppliers)

        # Certifications
        total_certs = len(self.certifications)
        active_certs = sum(1 for c in self.certifications if c['status'] == 'Active')
        expiring_soon = sum(1 for c in self.certifications if 0 <= c['days_to_expiry'] <= 90)
        expired = sum(1 for c in self.certifications if c['days_to_expiry'] < 0)

        return {
            'products': {
                'total': total_products,
                'compliant': compliant_products,
                'compliance_rate': round(compliant_products / total_products * 100, 1) if total_products > 0 else 0
            },
            'suppliers': {
                'total': total_suppliers
            },
            'certifications': {
                'total': total_certs,
                'active': active_certs,
                'expiring_soon_90_days': expiring_soon,
                'expired': expired
            },
            'violations': {
                'total': len(self.compliance_violations)
            }
        }


# Example usage
compliance_mgr = ComplianceManager()

# Add regulations
compliance_mgr.add_regulation(
    'REG001',
    'RoHS Directive (EU)',
    region='European Union',
    category='product_safety',
    effective_date='2006-07-01'
)

compliance_mgr.add_regulation(
    'REG002',
    'REACH Regulation',
    region='European Union',
    category='product_safety',
    effective_date='2007-06-01'
)

compliance_mgr.add_regulation(
    'REG003',
    'Export Administration Regulations',
    region='United States',
    category='trade',
    effective_date='1979-03-30'
)

# Add products
compliance_mgr.add_product(
    'PROD001',
    'Electronic Widget',
    hs_code='8543.70.9900',
    materials=['plastic', 'copper', 'silicon'],
    target_markets=['EU', 'US', 'CN'],
    applicable_regulations=['REG001', 'REG002']
)

compliance_mgr.add_product(
    'PROD002',
    'Industrial Controller',
    hs_code='8537.10.9000',
    materials=['aluminum', 'steel', 'lead'],  # Contains restricted substance
    target_markets=['EU'],
    applicable_regulations=['REG001']
)

# Assess product compliance
assessment1 = compliance_mgr.assess_product_compliance('PROD001')
print(f"Product: {assessment1['product_name']}")
print(f"Overall Status: {assessment1['overall_status']}")
print(f"Compliance Gaps: {len(assessment1['compliance_gaps'])}")

assessment2 = compliance_mgr.assess_product_compliance('PROD002')
print(f"\nProduct: {assessment2['product_name']}")
print(f"Overall Status: {assessment2['overall_status']}")
if assessment2['compliance_gaps']:
    print("Gaps found:")
    for gap in assessment2['compliance_gaps']:
        print(f"  - {gap['issue']} (Severity: {gap['severity']})")

# Add suppliers
compliance_mgr.add_supplier(
    'SUP001',
    'Acme Manufacturing',
    country='China',
    certifications=['ISO9001', 'ISO14001'],
    audit_date='2025-06-15'
)

# Track certifications
compliance_mgr.track_certification(
    'SUP001',
    'supplier',
    'ISO 9001:2015',
    'ISO-9001-12345',
    issue_date='2022-06-15',
    expiry_date='2025-06-15',
    status='Active'
)

compliance_mgr.track_certification(
    'PROD001',
    'product',
    'CE Mark',
    'CE-2024-0001',
    issue_date='2024-01-10',
    expiry_date='2026-03-15',
    status='Active'
)

compliance_mgr.track_certification(
    'PROD001',
    'product',
    'FCC Certification',
    'FCC-ID-XYZ123',
    issue_date='2024-02-01',
    expiry_date='2026-02-20',
    status='Active'
)

# Get expiring certifications
expiring = compliance_mgr.get_expiring_certifications(days_threshold=180)
print("\n\nExpiring Certifications (next 180 days):")
if not expiring.empty:
    print(expiring[['certification', 'entity_id', 'days_remaining', 'urgency']])
else:
    print("None")

# Dashboard
dashboard = compliance_mgr.generate_compliance_dashboard()
print("\n\nCompliance Dashboard:")
print(f"Products: {dashboard['products']['compliant']}/{dashboard['products']['total']} compliant ({dashboard['products']['compliance_rate']}%)")
print(f"Certifications: {dashboard['certifications']['active']} active, {dashboard['certifications']['expiring_soon_90_days']} expiring soon")
```

---

## Trade Compliance

### HS Code Classification

```python
class TradeComplianceManager:
    """Manage trade compliance including HS codes, duties, and regulations"""

    def __init__(self):
        self.hs_code_database = self._load_hs_codes()
        self.duty_rates = {}
        self.fta_eligibility = {}

    def _load_hs_codes(self):
        """Load HS code database (simplified)"""
        return {
            '8543.70': {'description': 'Other electrical machines with individual functions',
                       'typical_duty_us': 0.028},
            '8537.10': {'description': 'Control panels with voltage ≤1000V',
                       'typical_duty_us': 0.026},
            '8471.30': {'description': 'Portable computers',
                       'typical_duty_us': 0.000},  # Duty-free under ITA
        }

    def classify_product(self, product_description, material_composition,
                        intended_use, suggested_hs_code=None):
        """
        Assist with HS code classification

        Returns classification with confidence level
        """

        # In reality, this would use ML/NLP and extensive HS code database
        # Simplified example

        classification = {
            'product_description': product_description,
            'suggested_hs_code': suggested_hs_code,
            'confidence': 'Medium',
            'classification_rationale': [],
            'requires_expert_review': False
        }

        # Check if suggested code is valid
        if suggested_hs_code:
            if suggested_hs_code[:7] in self.hs_code_database:
                classification['confidence'] = 'High'
                classification['classification_rationale'].append(
                    f"HS code {suggested_hs_code} is valid and matches product type"
                )
            else:
                classification['confidence'] = 'Low'
                classification['requires_expert_review'] = True
                classification['classification_rationale'].append(
                    "Suggested HS code not found in database - expert review needed"
                )

        # Check for complex products
        if len(material_composition) > 5:
            classification['requires_expert_review'] = True
            classification['classification_rationale'].append(
                "Complex multi-material product - binding ruling recommended"
            )

        return classification

    def calculate_landed_cost(self, product_cost, hs_code, origin_country,
                            dest_country, shipping_cost, insurance_cost=None):
        """
        Calculate total landed cost including duties and fees

        Simplified calculation
        """

        # Insurance (if not provided, estimate as 1% of product cost)
        if insurance_cost is None:
            insurance_cost = product_cost * 0.01

        # Customs value (FOB + freight + insurance)
        customs_value = product_cost + shipping_cost + insurance_cost

        # Get duty rate
        hs_prefix = hs_code[:7]
        duty_rate = self.hs_code_database.get(hs_prefix, {}).get('typical_duty_us', 0.05)

        # Calculate duty
        duty_amount = customs_value * duty_rate

        # MPF (Merchandise Processing Fee) - US specific
        mpf = customs_value * 0.003464
        mpf = max(27.75, min(mpf, 538.40))  # MPF has min and max

        # Harbor Maintenance Fee (if applicable) - 0.125% of cargo value
        hmf = customs_value * 0.00125 if dest_country == 'US' else 0

        # Total landed cost
        total_landed_cost = customs_value + duty_amount + mpf + hmf

        return {
            'product_cost': round(product_cost, 2),
            'shipping_cost': round(shipping_cost, 2),
            'insurance_cost': round(insurance_cost, 2),
            'customs_value': round(customs_value, 2),
            'duty_rate': round(duty_rate * 100, 2),
            'duty_amount': round(duty_amount, 2),
            'mpf': round(mpf, 2),
            'hmf': round(hmf, 2),
            'total_landed_cost': round(total_landed_cost, 2),
            'landed_cost_percentage': round(total_landed_cost / product_cost * 100, 1)
        }

    def check_fta_eligibility(self, hs_code, origin_country, dest_country):
        """
        Check Free Trade Agreement eligibility

        Simplified - in reality would check specific rules of origin
        """

        # Example FTA relationships
        fta_agreements = {
            ('US', 'MX'): 'USMCA',
            ('MX', 'US'): 'USMCA',
            ('US', 'CA'): 'USMCA',
            ('CA', 'US'): 'USMCA',
            ('US', 'SG'): 'US-Singapore FTA',
            ('SG', 'US'): 'US-Singapore FTA',
        }

        agreement = fta_agreements.get((origin_country, dest_country))

        if agreement:
            # Check rules of origin (simplified)
            eligible = True  # In reality, would check specific product rules

            return {
                'fta_eligible': eligible,
                'agreement': agreement,
                'duty_savings': 'Potentially duty-free' if eligible else 'N/A',
                'documentation_required': ['Certificate of Origin', 'Importer Declaration'],
                'origin_criteria': 'Must meet regional value content or tariff shift rules'
            }
        else:
            return {
                'fta_eligible': False,
                'agreement': None,
                'note': f'No FTA between {origin_country} and {dest_country}'
            }

    def screen_denied_parties(self, party_name, country):
        """
        Screen against denied parties lists

        In reality, would check against:
        - OFAC SDN List
        - BIS Denied Persons List
        - EU Sanctions List
        - UN Sanctions List
        """

        # Simplified screening
        # In production, integrate with compliance screening API

        denied_parties_sample = ['ABC Corp', 'XYZ Ltd', 'Bad Actor Inc']

        is_denied = party_name in denied_parties_sample

        screening_result = {
            'party_name': party_name,
            'country': country,
            'screening_status': 'DENIED' if is_denied else 'CLEAR',
            'lists_checked': ['OFAC SDN', 'BIS Denied Persons', 'EU Sanctions'],
            'screening_date': datetime.now().strftime('%Y-%m-%d'),
            'matches_found': 1 if is_denied else 0
        }

        if is_denied:
            screening_result['action_required'] = 'DO NOT TRANSACT - Escalate to Compliance Officer'
            screening_result['severity'] = 'Critical'

        return screening_result


# Example usage
trade_mgr = TradeComplianceManager()

# Classify product
classification = trade_mgr.classify_product(
    product_description='Handheld electronic device for industrial control',
    material_composition=['plastic', 'aluminum', 'circuit_board'],
    intended_use='Industrial process control',
    suggested_hs_code='8537.10.9000'
)

print("HS Code Classification:")
print(f"  Suggested Code: {classification['suggested_hs_code']}")
print(f"  Confidence: {classification['confidence']}")
print(f"  Requires Expert Review: {classification['requires_expert_review']}")

# Calculate landed cost
landed_cost = trade_mgr.calculate_landed_cost(
    product_cost=1000,
    hs_code='8537.10.9000',
    origin_country='CN',
    dest_country='US',
    shipping_cost=150,
    insurance_cost=15
)

print(f"\n\nLanded Cost Calculation:")
print(f"  Product Cost: ${landed_cost['product_cost']}")
print(f"  Customs Value: ${landed_cost['customs_value']}")
print(f"  Duty ({landed_cost['duty_rate']}%): ${landed_cost['duty_amount']}")
print(f"  Total Landed Cost: ${landed_cost['total_landed_cost']}")
print(f"  Total % of Product Cost: {landed_cost['landed_cost_percentage']}%")

# Check FTA eligibility
fta = trade_mgr.check_fta_eligibility(
    hs_code='8537.10.9000',
    origin_country='MX',
    dest_country='US'
)

print(f"\n\nFTA Eligibility:")
print(f"  Agreement: {fta.get('agreement', 'None')}")
print(f"  Eligible: {fta['fta_eligible']}")

# Screen denied party
screening = trade_mgr.screen_denied_parties('ABC Corp', 'IR')

print(f"\n\nDenied Party Screening:")
print(f"  Party: {screening['party_name']}")
print(f"  Status: {screening['screening_status']}")
```

---

## Tools & Libraries

### Python Libraries

**Compliance Management:**
- `pandas`: Data management
- `numpy`: Numerical computations
- `sqlalchemy`: Database connections

**Document Management:**
- `PyPDF2`: PDF processing
- `python-docx`: Word document handling
- `openpyxl`: Excel file handling

**Data Validation:**
- `cerberus`: Schema validation
- `pydantic`: Data validation
- `jsonschema`: JSON validation

**Automation:**
- `schedule`: Scheduled tasks
- `APScheduler`: Advanced scheduling
- `celery`: Distributed task queue

### Commercial Software

**Compliance Management:**
- **SAP GTS (Global Trade Services)**: Trade compliance
- **Amber Road (E2open)**: Global trade management
- **Descartes**: Customs and compliance
- **BluJay Solutions**: Trade compliance
- **Integration Point**: Trade compliance automation

**Product Compliance:**
- **Assent Compliance**: Supply chain compliance
- **Coupa Supplier Compliance**: Supplier management
- **EcoVadis**: Sustainability ratings
- **Sphera**: Product stewardship

**Regulatory Intelligence:**
- **UL Compliance**: Regulatory database
- **Enhesa**: Global regulatory intelligence
- **Intertek Inlight**: Compliance intelligence
- **Verisk 3E**: Environmental compliance

**Document Management:**
- **Ivalua**: Supplier compliance documents
- **TraceLink**: Serialization and compliance
- **MasterControl**: Document control systems

---

## Common Challenges & Solutions

### Challenge: Keeping Up with Regulatory Changes

**Problem:**
- Regulations constantly evolving
- Multiple jurisdictions
- Resource constraints

**Solutions:**
- Subscribe to regulatory intelligence services
- Automated alerts for regulation changes
- Industry associations and working groups
- Dedicated compliance team or specialist
- Annual compliance calendar
- Regulatory change impact assessments

### Challenge: Supplier Compliance Verification

**Problem:**
- Suppliers lack compliance knowledge
- Inconsistent documentation
- Difficult to verify claims

**Solutions:**
- Supplier compliance training programs
- Standardized compliance questionnaires
- Third-party audits and certifications
- Blockchain for supply chain traceability
- Contractual compliance requirements
- Risk-based supplier segmentation

### Challenge: Complex Product Compliance

**Problem:**
- Products contain hundreds of components
- Multi-tier supply chain visibility
- Conflicting requirements across markets

**Solutions:**
- Bill of Materials (BOM) management system
- Material declaration databases (IMDS, BOMcheck)
- Product lifecycle management (PLM) integration
- Design for compliance from start
- Restricted substance lists (RSL)
- Market-specific product variants

### Challenge: Documentation Management

**Problem:**
- Volume of compliance documents
- Expiring certifications
- Audit trail requirements

**Solutions:**
- Document management system (DMS)
- Automated expiration alerts
- Digital document workflows
- Version control and audit logs
- Centralized compliance repository
- Automated reminders for renewals

### Challenge: Trade Compliance Complexity

**Problem:**
- Tariff classification disputes
- Rules of origin determination
- Denied party screening
- Export control requirements

**Solutions:**
- Automated classification tools
- Binding ruling requests for critical products
- Real-time denied party screening
- Export license management system
- FTA qualification analysis
- Trade compliance audits

### Challenge: Demonstrating Compliance to Customers

**Problem:**
- Customer audits and questionnaires
- Different requirements per customer
- Proving due diligence

**Solutions:**
- Centralized compliance portal for customers
- Standard compliance certificates
- Third-party certifications and audits
- Transparency and documentation
- Compliance dashboard with real-time data
- Proactive compliance reporting

---

## Output Format

### Compliance Report

**Executive Summary:**
- Overall compliance status
- Critical gaps and violations
- Regulatory changes impacting business
- Required actions and timeline

**Regulatory Compliance Status:**

| Regulation | Region | Category | Status | Last Review | Next Review | Gaps |
|-----------|--------|----------|--------|-------------|-------------|------|
| RoHS | EU | Product Safety | Compliant | 2025-11-15 | 2026-11-15 | None |
| REACH | EU | Chemicals | Partial | 2025-10-01 | 2026-04-01 | 2 SVHCs |
| ITAR | US | Export Control | Compliant | 2025-09-20 | 2026-09-20 | None |
| Conflict Minerals | Global | Social | In Progress | 2025-12-01 | 2026-12-01 | Pending supplier declarations |

**Product Compliance:**

| Product | Markets | Regulations | Status | Certifications | Gaps |
|---------|---------|-------------|--------|----------------|------|
| Widget A | EU, US | RoHS, FCC | Compliant | CE, FCC | None |
| Widget B | EU | RoHS, REACH | Non-Compliant | CE (expired) | Lead content, expired cert |
| Controller X | US, CN | FCC, CCC | Partial | FCC | CCC pending |

**Supplier Compliance:**

| Supplier | Country | Certifications | Last Audit | Next Audit | Score | Status |
|----------|---------|----------------|------------|------------|-------|--------|
| Supplier A | China | ISO9001, ISO14001 | 2025-06-15 | 2026-06-15 | 85/100 | ✓ Compliant |
| Supplier B | Vietnam | ISO9001 | 2024-08-20 | 2025-08-20 | 72/100 | ⚠ Audit due soon |
| Supplier C | Mexico | None | Never | TBD | N/A | ✗ Audit required |

**Certification Tracker:**

| Entity | Certification | Number | Issue Date | Expiry Date | Days to Expiry | Action Required |
|--------|---------------|--------|------------|-------------|----------------|-----------------|
| Product A | CE Mark | CE-2024-001 | 2024-01-10 | 2026-03-15 | 445 | None |
| Supplier X | ISO 9001 | ISO-12345 | 2022-06-15 | 2025-06-15 | 142 | Renewal in progress |
| Facility 1 | EPA Permit | EPA-XYZ-001 | 2023-01-01 | 2026-01-01 | 342 | None |

**Action Items:**

| Priority | Action | Owner | Due Date | Status |
|----------|--------|-------|----------|--------|
| Critical | Renew ISO 9001 for Supplier X | Procurement | 2025-05-01 | In Progress |
| High | Complete conflict minerals survey | Supply Chain | 2026-01-31 | Not Started |
| High | Reformulate Product B to remove lead | R&D | 2026-03-31 | Planning |
| Medium | Conduct audit of Supplier C | Quality | 2026-02-28 | Scheduled |

---

## Questions to Ask

If you need more context:
1. What products and services are in scope?
2. What markets/regions do you operate in?
3. What regulatory frameworks apply to your industry?
4. Have there been recent compliance issues or violations?
5. What certifications are required for your products/suppliers?
6. How many suppliers and countries in your supply chain?
7. What import/export volumes and countries involved?
8. Are there customer-specific compliance requirements?
9. What compliance management systems are in place?
10. What's the compliance team structure and resources?

---

## Related Skills

- **supplier-risk-management**: For assessing compliance risks in suppliers
- **quality-management**: For quality standards and certifications
- **sustainable-sourcing**: For environmental and social compliance
- **carbon-footprint-tracking**: For carbon reporting compliance
- **contract-management**: For compliance terms in contracts
- **procurement-optimization**: For incorporating compliance in sourcing
- **supplier-selection**: For compliance criteria in supplier evaluation
- **track-and-trace**: For supply chain transparency and traceability
