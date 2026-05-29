---
name: pharmacy-supply-chain
description: When the user wants to optimize pharmacy supply chain operations, manage medication distribution, ensure pharmaceutical compliance, or handle controlled substances. Also use when the user mentions "pharmacy logistics," "drug distribution," "controlled substances," "340B program," "formulary management," "medication safety," "specialty pharmacy," "drug shortages," "DEA compliance," "pharmaceutical traceability," or "DSCSA compliance." For hospital materials management, see hospital-logistics. For clinical trial drugs, see clinical-trial-logistics.
---

# Pharmacy Supply Chain

You are an expert in pharmacy supply chain management and pharmaceutical distribution. Your goal is to ensure safe, compliant, cost-effective distribution of medications while maintaining regulatory compliance, managing controlled substances, and preventing drug shortages.

## Initial Assessment

Before optimizing pharmacy supply chain, understand:

1. **Pharmacy Type & Scope**
   - Pharmacy type? (hospital, retail, specialty, mail-order, 340B)
   - Number of locations? (single site vs. health system)
   - Patient volume and prescription volume?
   - Service lines? (inpatient, outpatient, infusion, specialty)

2. **Regulatory Environment**
   - DEA registration status and schedules handled?
   - State board of pharmacy requirements?
   - 340B program participation?
   - DSCSA (Drug Supply Chain Security Act) compliance?
   - Accreditations? (Joint Commission, ACHC, URAC)

3. **Inventory & Formulary**
   - Number of formulary drugs?
   - Inventory investment and turns?
   - High-cost specialty medications?
   - Controlled substance volume?
   - Generic vs. brand mix?

4. **Current Challenges**
   - Drug shortages impact?
   - Expiry and waste levels?
   - Controlled substance diversion risk?
   - 340B compliance gaps?
   - Distribution inefficiencies?

---

## Pharmacy Supply Chain Framework

### Pharmaceutical Distribution Channels

**1. Wholesaler/Distributor Model**
- Primary distribution channel (80-90% of drugs)
- Major wholesalers: McKesson, Cardinal Health, AmerisourceBergen
- Benefits: Broad selection, daily delivery, credit terms
- Considerations: Wholesaler fees, contract compliance

**2. Direct from Manufacturer**
- Specialty medications
- Limited distribution drugs
- High-volume generics (cost savings)
- Vaccines and biologics
- Benefits: Lower cost, better supply assurance
- Considerations: Minimum order quantities, less frequent delivery

**3. 340B Contract Pharmacy**
- Covered entities purchase at 340B ceiling price
- Dispense to eligible patients
- Significant cost savings
- Complex compliance requirements

**4. Specialty Pharmacy Distribution**
- High-cost, complex medications
- Limited distribution networks
- Patient support services
- Prior authorization and reimbursement support

---

## DSCSA Compliance & Traceability

### Drug Supply Chain Security Act (DSCSA)

**Requirements:**
- Product tracing at package level (serialization)
- Verification of product legitimacy
- Detection and response to suspect/illegitimate products
- Systems and processes for tracing

**Timeline:**
- 2023: Enhanced drug distribution security
- 2024: Full electronic, interoperable tracing (November 2024)

**Implementation:**

```python
import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class ProductIdentifier:
    """
    DSCSA-compliant product identifier
    """
    gtin: str  # Global Trade Item Number (NDC in GTIN-14 format)
    serial_number: str
    lot_number: str
    expiration_date: datetime

    def to_serialized_string(self):
        """Convert to DSCSA format"""
        exp_date = self.expiration_date.strftime("%y%m%d")
        return f"(01){self.gtin}(21){self.serial_number}(10){self.lot_number}(17){exp_date}"

    @staticmethod
    def from_2d_barcode(barcode_string):
        """Parse 2D Data Matrix barcode"""
        import re

        patterns = {
            'gtin': r'\(01\)(\d{14})',
            'serial_number': r'\(21\)([A-Za-z0-9]+)',
            'lot_number': r'\(10\)([A-Za-z0-9]+)',
            'expiration_date': r'\(17\)(\d{6})'
        }

        data = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, barcode_string)
            if match:
                value = match.group(1)
                if field == 'expiration_date':
                    data[field] = datetime.strptime(value, "%y%m%d")
                else:
                    data[field] = value

        return ProductIdentifier(**data) if data else None

@dataclass
class TransactionInformation:
    """
    DSCSA Transaction Information (TI)
    """
    product_identifier: ProductIdentifier
    transaction_date: datetime
    ship_from: str  # Business name and address
    ship_to: str
    quantity: int

@dataclass
class TransactionHistory:
    """
    DSCSA Transaction History (TH) - full chain of ownership
    """
    transactions: List[TransactionInformation]

    def add_transaction(self, transaction: TransactionInformation):
        """Add transaction to history"""
        self.transactions.append(transaction)

    def verify_chain_of_custody(self):
        """Verify unbroken chain of custody"""
        if len(self.transactions) < 2:
            return True

        for i in range(len(self.transactions) - 1):
            current = self.transactions[i]
            next_trans = self.transactions[i + 1]

            # Verify ship_to of current matches ship_from of next
            if current.ship_to != next_trans.ship_from:
                return False

        return True

@dataclass
class TransactionStatement:
    """
    DSCSA Transaction Statement (TS) - attestation of legitimacy
    """
    product_identifier: ProductIdentifier
    statement_date: datetime
    authorized_entity: str
    attestation: str = "Product is legitimate and not counterfeit"

class DSCSATraceabilitySystem:
    """
    Manage DSCSA traceability and compliance
    """

    def __init__(self, business_name, dea_number, license_number):
        self.business_name = business_name
        self.dea_number = dea_number
        self.license_number = license_number
        self.inventory = {}
        self.transactions = []

    def receive_product(self, product_id: ProductIdentifier, quantity: int,
                        transaction_info: TransactionInformation,
                        transaction_history: TransactionHistory,
                        transaction_statement: TransactionStatement):
        """
        Receive product with DSCSA documentation
        """

        # Verify transaction history
        if not transaction_history.verify_chain_of_custody():
            raise ValueError("Chain of custody verification failed")

        # Verify product identifier matches
        if product_id.serial_number != transaction_info.product_identifier.serial_number:
            raise ValueError("Product identifier mismatch")

        # Store product in inventory with TI/TH/TS
        inventory_key = f"{product_id.gtin}-{product_id.serial_number}"

        self.inventory[inventory_key] = {
            'product_identifier': product_id,
            'quantity': quantity,
            'received_date': datetime.now(),
            'transaction_information': transaction_info,
            'transaction_history': transaction_history,
            'transaction_statement': transaction_statement,
            'status': 'in_stock'
        }

        return inventory_key

    def dispense_product(self, inventory_key: str, quantity: int,
                         patient_or_customer: str):
        """
        Dispense product to patient or transfer to another entity
        """

        if inventory_key not in self.inventory:
            raise ValueError(f"Product {inventory_key} not found in inventory")

        product_record = self.inventory[inventory_key]

        if product_record['quantity'] < quantity:
            raise ValueError(f"Insufficient quantity. Available: {product_record['quantity']}")

        # Create transaction record
        transaction = {
            'type': 'dispensed',
            'product_identifier': product_record['product_identifier'],
            'quantity': quantity,
            'date': datetime.now(),
            'recipient': patient_or_customer
        }

        self.transactions.append(transaction)

        # Update inventory
        product_record['quantity'] -= quantity

        if product_record['quantity'] == 0:
            product_record['status'] = 'dispensed'

        return transaction

    def verify_product(self, serialized_string: str):
        """
        Verify product legitimacy using DSCSA data
        """

        product_id = ProductIdentifier.from_2d_barcode(serialized_string)

        if not product_id:
            return {'verified': False, 'reason': 'Invalid product identifier'}

        inventory_key = f"{product_id.gtin}-{product_id.serial_number}"

        if inventory_key in self.inventory:
            product = self.inventory[inventory_key]
            return {
                'verified': True,
                'product': product_id,
                'status': product['status'],
                'received_date': product['received_date']
            }
        else:
            return {'verified': False, 'reason': 'Product not found in inventory'}

    def suspect_product_investigation(self, inventory_key: str, reason: str):
        """
        Quarantine and investigate suspect product
        """

        if inventory_key not in self.inventory:
            raise ValueError(f"Product {inventory_key} not found")

        product = self.inventory[inventory_key]
        product['status'] = 'quarantined'
        product['quarantine_reason'] = reason
        product['quarantine_date'] = datetime.now()

        # Notify FDA and trading partners as required
        investigation = {
            'product': product['product_identifier'],
            'reason': reason,
            'date': datetime.now(),
            'actions_taken': 'Product quarantined, investigation initiated'
        }

        return investigation

# Example usage
dscsa_system = DSCSATraceabilitySystem(
    business_name="Memorial Hospital Pharmacy",
    dea_number="FM1234563",
    license_number="PHY-12345"
)

# Create product identifier
product = ProductIdentifier(
    gtin="00300123456789",  # NDC in GTIN-14 format
    serial_number="ABC123XYZ789",
    lot_number="LOT2024-A",
    expiration_date=datetime(2026, 12, 31)
)

# Transaction information
trans_info = TransactionInformation(
    product_identifier=product,
    transaction_date=datetime.now(),
    ship_from="McKesson Corporation, 1234 Distributor Way",
    ship_to="Memorial Hospital Pharmacy, 5678 Hospital Blvd",
    quantity=100
)

# Transaction history
trans_history = TransactionHistory(transactions=[trans_info])

# Transaction statement
trans_statement = TransactionStatement(
    product_identifier=product,
    statement_date=datetime.now(),
    authorized_entity="McKesson Corporation"
)

# Receive product
inventory_key = dscsa_system.receive_product(
    product_id=product,
    quantity=100,
    transaction_info=trans_info,
    transaction_history=trans_history,
    transaction_statement=trans_statement
)

print(f"Product received: {inventory_key}")

# Verify product
barcode = product.to_serialized_string()
verification = dscsa_system.verify_product(barcode)
print(f"Product verified: {verification['verified']}")
```

---

## Controlled Substance Management

### DEA Controlled Substance Schedules

**Schedule I:** No accepted medical use, high abuse potential
- Examples: Heroin, LSD, marijuana (federally)
- Not typically in pharmacy

**Schedule II:** High abuse potential, accepted medical use
- Examples: Oxycodone, morphine, fentanyl, amphetamine, cocaine
- Requirements: Written prescription (with exceptions), no refills, secure storage

**Schedule III:** Moderate abuse potential
- Examples: Codeine/acetaminophen, ketamine, testosterone
- Requirements: Written or electronic Rx, up to 5 refills in 6 months

**Schedule IV:** Low abuse potential
- Examples: Alprazolam, diazepam, tramadol, zolpidem
- Requirements: Written or electronic Rx, up to 5 refills in 6 months

**Schedule V:** Lowest abuse potential
- Examples: Cough preparations with <200mg codeine
- Requirements: May have OTC availability in some states

### Perpetual Inventory System

```python
import pandas as pd
from datetime import datetime
from enum import Enum

class ControlledSubstanceSchedule(Enum):
    SCHEDULE_II = "C-II"
    SCHEDULE_III = "C-III"
    SCHEDULE_IV = "C-IV"
    SCHEDULE_V = "C-V"

class TransactionType(Enum):
    RECEIVED = "received"
    DISPENSED = "dispensed"
    WASTED = "wasted"
    RETURNED = "returned"
    TRANSFERRED = "transferred"
    DESTROYED = "destroyed"

class ControlledSubstanceManager:
    """
    Perpetual inventory system for controlled substances
    """

    def __init__(self, pharmacy_name, dea_number):
        self.pharmacy_name = pharmacy_name
        self.dea_number = dea_number
        self.inventory = {}
        self.transactions = []

    def add_drug(self, drug_id, drug_name, ndc, schedule, strength, form):
        """
        Add controlled substance to formulary
        """

        self.inventory[drug_id] = {
            'drug_id': drug_id,
            'drug_name': drug_name,
            'ndc': ndc,
            'schedule': schedule,
            'strength': strength,
            'form': form,
            'quantity_on_hand': 0,
            'unit_of_measure': 'each'
        }

    def record_transaction(self, drug_id, transaction_type, quantity,
                          performer, witness=None, metadata=None):
        """
        Record controlled substance transaction

        Parameters:
        - drug_id: Drug identifier
        - transaction_type: Type of transaction (TransactionType enum)
        - quantity: Quantity (positive for additions, negative for removals)
        - performer: Person performing transaction
        - witness: Witness required for Schedule II (optional for others)
        - metadata: Additional data (Rx number, patient, waste reason, etc.)
        """

        if drug_id not in self.inventory:
            raise ValueError(f"Drug {drug_id} not in inventory")

        drug = self.inventory[drug_id]

        # Schedule II requires witness for dispensing and waste
        if drug['schedule'] == ControlledSubstanceSchedule.SCHEDULE_II:
            if transaction_type in [TransactionType.DISPENSED, TransactionType.WASTED]:
                if not witness:
                    raise ValueError("Witness required for Schedule II dispensing/waste")

        # Create transaction record
        transaction = {
            'transaction_id': len(self.transactions) + 1,
            'timestamp': datetime.now(),
            'drug_id': drug_id,
            'drug_name': drug['drug_name'],
            'ndc': drug['ndc'],
            'schedule': drug['schedule'].value,
            'transaction_type': transaction_type.value,
            'quantity': quantity,
            'balance_before': drug['quantity_on_hand'],
            'balance_after': drug['quantity_on_hand'] + quantity,
            'performer': performer,
            'witness': witness,
            'metadata': metadata or {}
        }

        # Update inventory
        drug['quantity_on_hand'] += quantity

        if drug['quantity_on_hand'] < 0:
            raise ValueError(f"Negative inventory not allowed. Current: {drug['quantity_on_hand']}")

        # Store transaction
        self.transactions.append(transaction)

        return transaction

    def receive_order(self, drug_id, quantity, invoice_number, supplier, received_by):
        """
        Receive controlled substance order
        """

        return self.record_transaction(
            drug_id=drug_id,
            transaction_type=TransactionType.RECEIVED,
            quantity=quantity,
            performer=received_by,
            metadata={
                'invoice_number': invoice_number,
                'supplier': supplier
            }
        )

    def dispense_prescription(self, drug_id, quantity, rx_number, patient_id,
                             pharmacist, technician_witness=None):
        """
        Dispense controlled substance prescription
        """

        return self.record_transaction(
            drug_id=drug_id,
            transaction_type=TransactionType.DISPENSED,
            quantity=-quantity,  # Negative for removal
            performer=pharmacist,
            witness=technician_witness,
            metadata={
                'rx_number': rx_number,
                'patient_id': patient_id
            }
        )

    def waste_medication(self, drug_id, quantity, reason, pharmacist, witness):
        """
        Waste controlled substance (expired, damaged, etc.)
        """

        return self.record_transaction(
            drug_id=drug_id,
            transaction_type=TransactionType.WASTED,
            quantity=-quantity,
            performer=pharmacist,
            witness=witness,
            metadata={'waste_reason': reason}
        )

    def physical_count(self, drug_id, counted_quantity, counted_by, witness=None):
        """
        Perform physical count and reconcile with perpetual inventory
        """

        if drug_id not in self.inventory:
            raise ValueError(f"Drug {drug_id} not in inventory")

        drug = self.inventory[drug_id]
        system_quantity = drug['quantity_on_hand']
        discrepancy = counted_quantity - system_quantity

        count_record = {
            'drug_id': drug_id,
            'drug_name': drug['drug_name'],
            'ndc': drug['ndc'],
            'schedule': drug['schedule'].value,
            'count_date': datetime.now(),
            'system_quantity': system_quantity,
            'physical_count': counted_quantity,
            'discrepancy': discrepancy,
            'counted_by': counted_by,
            'witness': witness
        }

        return count_record

    def perpetual_inventory_report(self, drug_id=None, schedule=None):
        """
        Generate perpetual inventory report
        """

        transactions_df = pd.DataFrame(self.transactions)

        if drug_id:
            transactions_df = transactions_df[transactions_df['drug_id'] == drug_id]

        if schedule:
            transactions_df = transactions_df[transactions_df['schedule'] == schedule.value]

        return transactions_df

    def biennial_inventory_report(self):
        """
        DEA biennial (every 2 years) inventory report
        """

        inventory_list = []

        for drug_id, drug in self.inventory.items():
            inventory_list.append({
                'drug_name': drug['drug_name'],
                'ndc': drug['ndc'],
                'schedule': drug['schedule'].value,
                'strength': drug['strength'],
                'form': drug['form'],
                'quantity_on_hand': drug['quantity_on_hand']
            })

        inventory_df = pd.DataFrame(inventory_list)
        inventory_df = inventory_df.sort_values(['schedule', 'drug_name'])

        report = {
            'pharmacy_name': self.pharmacy_name,
            'dea_number': self.dea_number,
            'report_date': datetime.now(),
            'inventory': inventory_df
        }

        return report

# Example usage
cs_manager = ControlledSubstanceManager(
    pharmacy_name="Memorial Hospital Pharmacy",
    dea_number="FM1234563"
)

# Add controlled substances to formulary
cs_manager.add_drug(
    drug_id='OXY-5MG',
    drug_name='Oxycodone',
    ndc='00406-0505-62',
    schedule=ControlledSubstanceSchedule.SCHEDULE_II,
    strength='5mg',
    form='Tablet'
)

cs_manager.add_drug(
    drug_id='DIAZ-5MG',
    drug_name='Diazepam',
    ndc='00591-3445-01',
    schedule=ControlledSubstanceSchedule.SCHEDULE_IV,
    strength='5mg',
    form='Tablet'
)

# Receive order
cs_manager.receive_order(
    drug_id='OXY-5MG',
    quantity=500,
    invoice_number='INV-123456',
    supplier='McKesson',
    received_by='RPh John Smith'
)

# Dispense prescriptions
cs_manager.dispense_prescription(
    drug_id='OXY-5MG',
    quantity=30,
    rx_number='RX-001234',
    patient_id='PT-567890',
    pharmacist='RPh John Smith',
    technician_witness='Tech Jane Doe'  # Schedule II requires witness
)

# Waste expired medication
cs_manager.waste_medication(
    drug_id='OXY-5MG',
    quantity=10,
    reason='Expired',
    pharmacist='RPh John Smith',
    witness='RPh Mary Johnson'
)

# Physical count
count = cs_manager.physical_count(
    drug_id='OXY-5MG',
    counted_quantity=460,
    counted_by='RPh John Smith',
    witness='RPh Mary Johnson'
)

print(f"Physical Count - Expected: {count['system_quantity']}, Counted: {count['physical_count']}, Discrepancy: {count['discrepancy']}")

# Generate perpetual inventory report
report = cs_manager.perpetual_inventory_report(drug_id='OXY-5MG')
print("\nPerpetual Inventory Report:")
print(report[['timestamp', 'transaction_type', 'quantity', 'balance_after', 'performer']])
```

---

## 340B Program Compliance

### 340B Drug Pricing Program

**Overview:**
- Federal program requiring manufacturers to provide outpatient drugs at reduced prices
- Eligible entities: Safety-net providers (hospitals, FQHCs, Ryan White clinics)
- Savings can be 20-50% off wholesale acquisition cost
- Complex compliance requirements

**Key Compliance Requirements:**
1. Patient eligibility determination
2. Drug diversion prevention
3. Duplicate discount prevention
4. Accurate record-keeping
5. Contract pharmacy compliance

```python
class Patient340BEligibility:
    """
    Determine 340B patient eligibility
    """

    def __init__(self, covered_entity_id, entity_type):
        self.covered_entity_id = covered_entity_id
        self.entity_type = entity_type  # DSH, PED, CAH, FQHC, etc.

    def check_eligibility(self, patient_id, encounter_data):
        """
        Determine if patient is eligible for 340B

        Patient must meet all criteria:
        1. Established relationship with covered entity
        2. Received healthcare service from covered entity
        3. Covered entity has responsibility for care
        4. Drug prescribed by provider of covered entity
        5. Drug dispensed by eligible pharmacy
        """

        criteria = {
            'established_patient': self._check_established_patient(patient_id, encounter_data),
            'received_service': self._check_service_received(encounter_data),
            'provider_responsibility': self._check_provider_responsibility(encounter_data),
            'eligible_prescriber': self._check_eligible_prescriber(encounter_data),
            'eligible_pharmacy': self._check_eligible_pharmacy(encounter_data)
        }

        # All criteria must be met
        eligible = all(criteria.values())

        return {
            'eligible': eligible,
            'criteria_results': criteria,
            'reason': self._eligibility_reason(criteria) if not eligible else 'Meets all criteria'
        }

    def _check_established_patient(self, patient_id, encounter_data):
        """Check if patient has established relationship"""
        # Implementation would check patient registration, prior visits, etc.
        return encounter_data.get('established_patient', False)

    def _check_service_received(self, encounter_data):
        """Check if patient received service from covered entity"""
        return encounter_data.get('service_location') == self.covered_entity_id

    def _check_provider_responsibility(self, encounter_data):
        """Check if covered entity has responsibility for patient care"""
        return encounter_data.get('responsible_entity') == self.covered_entity_id

    def _check_eligible_prescriber(self, encounter_data):
        """Check if prescriber is employed/contracted by covered entity"""
        return encounter_data.get('prescriber_entity') == self.covered_entity_id

    def _check_eligible_pharmacy(self, encounter_data):
        """Check if pharmacy is covered entity or registered contract pharmacy"""
        pharmacy = encounter_data.get('dispensing_pharmacy')
        return pharmacy in [self.covered_entity_id] or \
               pharmacy in self._get_contract_pharmacies()

    def _get_contract_pharmacies(self):
        """Get list of registered contract pharmacies"""
        # Would query HRSA database
        return ['CONTRACT-PHARM-001', 'CONTRACT-PHARM-002']

    def _eligibility_reason(self, criteria):
        """Generate reason for ineligibility"""
        failed = [k for k, v in criteria.items() if not v]
        return f"Failed criteria: {', '.join(failed)}"

class Program340BManager:
    """
    Manage 340B program operations and compliance
    """

    def __init__(self, covered_entity_id):
        self.covered_entity_id = covered_entity_id
        self.eligibility_checker = Patient340BEligibility(covered_entity_id, 'DSH')
        self.purchases = []
        self.dispenses = []

    def process_prescription(self, rx_data, patient_id, encounter_data):
        """
        Process prescription and determine 340B eligibility
        """

        # Check patient eligibility
        eligibility = self.eligibility_checker.check_eligibility(patient_id, encounter_data)

        # Check drug eligibility (some drugs excluded from 340B)
        drug_eligible = self._check_drug_eligibility(rx_data['ndc'])

        # Determine if 340B pricing applies
        use_340b = eligibility['eligible'] and drug_eligible

        dispense_record = {
            'rx_number': rx_data['rx_number'],
            'patient_id': patient_id,
            'ndc': rx_data['ndc'],
            'quantity': rx_data['quantity'],
            'dispense_date': datetime.now(),
            '340b_eligible': use_340b,
            'eligibility_reason': eligibility['reason'],
            'acquisition_cost': self._get_acquisition_cost(rx_data['ndc'], use_340b)
        }

        self.dispenses.append(dispense_record)

        return dispense_record

    def _check_drug_eligibility(self, ndc):
        """
        Check if drug is eligible for 340B pricing

        Exclusions:
        - Orphan drugs for rare diseases (when used for that disease)
        - Drugs for cosmetic purposes
        - Drugs for fertility
        """
        # Simplified - would check against exclusion list
        return True

    def _get_acquisition_cost(self, ndc, use_340b):
        """Get drug acquisition cost (340B or WAC)"""
        # Simplified - would query pricing database
        wac_price = 100.00
        price_340b = wac_price * 0.60  # Typical 40% discount

        return price_340b if use_340b else wac_price

    def duplicate_discount_check(self, rx_data, patient_insurance):
        """
        Prevent duplicate discounts (340B + Medicaid rebate)

        Covered entities cannot receive 340B discount AND Medicaid rebate
        """

        is_medicaid = patient_insurance.get('payer_type') == 'Medicaid'
        is_340b = rx_data.get('340b_eligible', False)

        if is_medicaid and is_340b:
            # Options:
            # 1. Carve-out: Don't bill Medicaid, use 340B
            # 2. Carve-in: Bill Medicaid, don't use 340B
            return {
                'duplicate_risk': True,
                'recommendation': 'Use 340B pricing, do not bill Medicaid for rebate'
            }

        return {'duplicate_risk': False}

    def diversion_audit(self, start_date, end_date):
        """
        Audit for drug diversion (using 340B drugs for ineligible patients)
        """

        dispenses_df = pd.DataFrame(self.dispenses)

        # Filter date range
        dispenses_df = dispenses_df[
            (dispenses_df['dispense_date'] >= start_date) &
            (dispenses_df['dispense_date'] <= end_date)
        ]

        # Identify potential diversion
        ineligible_340b = dispenses_df[
            (dispenses_df['340b_eligible'] == False) &
            (dispenses_df['acquisition_cost'] < 100)  # Using 340B-priced inventory
        ]

        audit_results = {
            'total_dispenses': len(dispenses_df),
            '340b_dispenses': len(dispenses_df[dispenses_df['340b_eligible'] == True]),
            'potential_diversion_events': len(ineligible_340b),
            'diversion_details': ineligible_340b
        }

        return audit_results

# Example usage
program_340b = Program340BManager(covered_entity_id='CE-001')

# Process prescription
rx = {
    'rx_number': 'RX-123456',
    'ndc': '00406-0505-62',
    'quantity': 30
}

encounter = {
    'established_patient': True,
    'service_location': 'CE-001',
    'responsible_entity': 'CE-001',
    'prescriber_entity': 'CE-001',
    'dispensing_pharmacy': 'CE-001'
}

dispense = program_340b.process_prescription(rx, patient_id='PT-789', encounter_data=encounter)
print(f"340B Eligible: {dispense['340b_eligible']}")
print(f"Acquisition Cost: ${dispense['acquisition_cost']:.2f}")

# Duplicate discount check
insurance = {'payer_type': 'Medicaid', 'member_id': 'MCD123456'}
duplicate_check = program_340b.duplicate_discount_check(dispense, insurance)
print(f"Duplicate discount risk: {duplicate_check['duplicate_risk']}")
```

---

## Drug Shortage Management

### Shortage Response Framework

```python
import pandas as pd
from datetime import datetime, timedelta

class DrugShortageManager:
    """
    Manage drug shortages and implement mitigation strategies
    """

    def __init__(self, pharmacy_name):
        self.pharmacy_name = pharmacy_name
        self.shortages = []
        self.inventory = {}

    def declare_shortage(self, drug_id, drug_name, ndc, shortage_reason,
                        expected_duration_days, therapeutic_alternatives=None):
        """
        Declare drug shortage
        """

        shortage = {
            'shortage_id': f"SHORT-{len(self.shortages)+1}",
            'drug_id': drug_id,
            'drug_name': drug_name,
            'ndc': ndc,
            'declared_date': datetime.now(),
            'shortage_reason': shortage_reason,
            'expected_resolution': datetime.now() + timedelta(days=expected_duration_days),
            'status': 'active',
            'therapeutic_alternatives': therapeutic_alternatives or [],
            'mitigation_actions': []
        }

        self.shortages.append(shortage)

        return shortage

    def mitigation_strategy(self, shortage_id):
        """
        Develop mitigation strategy for shortage

        Strategies:
        1. Therapeutic substitution
        2. Dosage form modification
        3. Conservation (restrict to critical patients)
        4. Alternative suppliers
        5. Compounding
        """

        shortage = next((s for s in self.shortages if s['shortage_id'] == shortage_id), None)

        if not shortage:
            raise ValueError(f"Shortage {shortage_id} not found")

        strategies = []

        # Check for therapeutic alternatives
        if shortage['therapeutic_alternatives']:
            strategies.append({
                'strategy': 'therapeutic_substitution',
                'description': f"Substitute with: {', '.join(shortage['therapeutic_alternatives'])}",
                'priority': 1
            })

        # Check current inventory
        current_qty = self.inventory.get(shortage['drug_id'], {}).get('quantity', 0)
        days_supply = self._calculate_days_supply(shortage['drug_id'], current_qty)

        if days_supply < 7:
            strategies.append({
                'strategy': 'conservation',
                'description': 'Restrict to critical patients only (ICU, life-saving)',
                'priority': 1
            })

        # Alternative sourcing
        strategies.append({
            'strategy': 'alternative_sourcing',
            'description': 'Contact alternative distributors and direct manufacturers',
            'priority': 2
        })

        # Compounding option (if appropriate)
        if self._can_compound(shortage['drug_id']):
            strategies.append({
                'strategy': 'compounding',
                'description': 'Compound in-house or outsource to 503B',
                'priority': 3
            })

        shortage['mitigation_actions'] = strategies

        return strategies

    def _calculate_days_supply(self, drug_id, quantity):
        """Calculate days of supply remaining based on usage"""
        # Simplified - would use historical usage data
        avg_daily_usage = 10
        return quantity / avg_daily_usage if avg_daily_usage > 0 else 0

    def _can_compound(self, drug_id):
        """Check if drug can be compounded"""
        # Simplified - would check formulary
        return True

    def prioritize_patients(self, drug_id, patient_list):
        """
        Prioritize patients for shortage allocation

        Priority levels:
        1. Life-saving/critical care
        2. Prevent serious morbidity
        3. Symptomatic relief
        """

        prioritized = []

        for patient in patient_list:
            # Determine priority based on indication
            indication = patient.get('indication', '')

            if any(critical in indication.lower() for critical in ['sepsis', 'shock', 'arrest', 'seizure']):
                priority = 1
                priority_desc = 'Critical - Life-saving'
            elif any(serious in indication.lower() for serious in ['infection', 'pain-severe', 'surgery']):
                priority = 2
                priority_desc = 'High - Prevent serious morbidity'
            else:
                priority = 3
                priority_desc = 'Medium - Symptomatic relief'

            prioritized.append({
                'patient_id': patient['patient_id'],
                'indication': indication,
                'priority': priority,
                'priority_description': priority_desc,
                'prescriber': patient.get('prescriber'),
                'requested_quantity': patient.get('quantity')
            })

        # Sort by priority
        prioritized.sort(key=lambda x: x['priority'])

        return pd.DataFrame(prioritized)

    def shortage_report(self):
        """
        Generate active shortages report
        """

        active_shortages = [s for s in self.shortages if s['status'] == 'active']

        if not active_shortages:
            return None

        report = []

        for shortage in active_shortages:
            current_qty = self.inventory.get(shortage['drug_id'], {}).get('quantity', 0)
            days_supply = self._calculate_days_supply(shortage['drug_id'], current_qty)

            report.append({
                'shortage_id': shortage['shortage_id'],
                'drug_name': shortage['drug_name'],
                'ndc': shortage['ndc'],
                'declared_date': shortage['declared_date'],
                'expected_resolution': shortage['expected_resolution'],
                'reason': shortage['shortage_reason'],
                'current_inventory': current_qty,
                'days_supply': round(days_supply, 1),
                'alternatives': ', '.join(shortage['therapeutic_alternatives']),
                'mitigation_actions': len(shortage['mitigation_actions'])
            })

        return pd.DataFrame(report)

# Example usage
shortage_mgr = DrugShortageManager("Memorial Hospital Pharmacy")

# Add inventory
shortage_mgr.inventory['PROP-100MG'] = {'quantity': 50}

# Declare shortage
shortage = shortage_mgr.declare_shortage(
    drug_id='PROP-100MG',
    drug_name='Propofol 100mg/10mL',
    ndc='63323-0269-10',
    shortage_reason='Manufacturing delay at primary supplier',
    expected_duration_days=45,
    therapeutic_alternatives=['Etomidate', 'Ketamine']
)

print(f"Shortage declared: {shortage['shortage_id']}")

# Develop mitigation strategy
strategies = shortage_mgr.mitigation_strategy(shortage['shortage_id'])
print("\nMitigation Strategies:")
for strategy in strategies:
    print(f"  {strategy['priority']}. {strategy['strategy']}: {strategy['description']}")

# Prioritize patients
patients = [
    {'patient_id': 'PT-001', 'indication': 'Septic shock - ICU', 'prescriber': 'Dr. Smith', 'quantity': 20},
    {'patient_id': 'PT-002', 'indication': 'Elective surgery - General anesthesia', 'prescriber': 'Dr. Jones', 'quantity': 20},
    {'patient_id': 'PT-003', 'indication': 'Status epilepticus', 'prescriber': 'Dr. Brown', 'quantity': 10}
]

prioritized = shortage_mgr.prioritize_patients('PROP-100MG', patients)
print("\nPrioritized Patient Allocation:")
print(prioritized[['patient_id', 'indication', 'priority_description', 'requested_quantity']])
```

---

## Specialty Pharmacy Operations

### High-Cost Medication Management

```python
class SpecialtyPharmacyManager:
    """
    Manage specialty pharmacy operations for high-cost medications
    """

    def __init__(self, pharmacy_name):
        self.pharmacy_name = pharmacy_name
        self.specialty_drugs = {}
        self.prior_authorizations = {}

    def add_specialty_drug(self, drug_id, drug_name, ndc, indication,
                          unit_cost, limited_distribution=False,
                          rems_required=False, storage_requirements=None):
        """
        Add specialty drug to formulary
        """

        self.specialty_drugs[drug_id] = {
            'drug_id': drug_id,
            'drug_name': drug_name,
            'ndc': ndc,
            'indication': indication,
            'unit_cost': unit_cost,
            'limited_distribution': limited_distribution,
            'rems_required': rems_required,  # Risk Evaluation and Mitigation Strategy
            'storage_requirements': storage_requirements or 'Room temperature'
        }

    def prior_authorization(self, drug_id, patient_id, prescriber,
                           diagnosis_code, clinical_justification,
                           insurance_info):
        """
        Submit prior authorization request
        """

        pa_id = f"PA-{len(self.prior_authorizations)+1}"

        pa_request = {
            'pa_id': pa_id,
            'drug_id': drug_id,
            'patient_id': patient_id,
            'prescriber': prescriber,
            'diagnosis_code': diagnosis_code,
            'clinical_justification': clinical_justification,
            'insurance_info': insurance_info,
            'submission_date': datetime.now(),
            'status': 'pending',
            'determination': None,
            'determination_date': None
        }

        self.prior_authorizations[pa_id] = pa_request

        return pa_request

    def financial_assistance_screening(self, patient_id, drug_id, annual_income,
                                      insurance_coverage):
        """
        Screen for patient financial assistance programs
        """

        drug = self.specialty_drugs.get(drug_id)

        if not drug:
            raise ValueError(f"Drug {drug_id} not found")

        # Calculate estimated patient cost
        if insurance_coverage:
            copay = insurance_coverage.get('copay', drug['unit_cost'] * 0.30)
            coinsurance_pct = insurance_coverage.get('coinsurance', 0)
        else:
            copay = drug['unit_cost']
            coinsurance_pct = 100

        estimated_annual_cost = copay * 12  # Assuming monthly therapy

        # Assistance program eligibility (simplified)
        assistance_programs = []

        # Manufacturer copay assistance
        if insurance_coverage and copay > 50:
            assistance_programs.append({
                'program': 'Manufacturer Copay Card',
                'estimated_savings': min(copay * 0.80, 12000),  # Up to $12K/year typical
                'eligibility': 'Commercial insurance required'
            })

        # Patient assistance program (PAP)
        federal_poverty_level = 30000  # Simplified
        if annual_income < federal_poverty_level * 5:
            assistance_programs.append({
                'program': 'Manufacturer Patient Assistance Program (PAP)',
                'estimated_savings': drug['unit_cost'],
                'eligibility': f'Income <500% FPL (${federal_poverty_level * 5:,.0f})'
            })

        # Foundation assistance
        if estimated_annual_cost > annual_income * 0.10:  # >10% of income
            assistance_programs.append({
                'program': 'Independent Charitable Foundation',
                'estimated_savings': estimated_annual_cost * 0.50,
                'eligibility': 'Disease-specific, income-based'
            })

        return {
            'patient_id': patient_id,
            'drug_name': drug['drug_name'],
            'estimated_annual_cost': round(estimated_annual_cost, 2),
            'pct_of_income': round(estimated_annual_cost / annual_income * 100, 1) if annual_income > 0 else 0,
            'assistance_programs': assistance_programs
        }

# Example usage
specialty_pharm = SpecialtyPharmacyManager("Memorial Specialty Pharmacy")

# Add specialty drug
specialty_pharm.add_specialty_drug(
    drug_id='HUMIRA-40MG',
    drug_name='Adalimumab (Humira)',
    ndc='00074-4339-02',
    indication='Rheumatoid Arthritis, Crohn\'s Disease',
    unit_cost=6000,
    limited_distribution=False,
    rems_required=False,
    storage_requirements='Refrigerated 2-8°C'
)

# Prior authorization
pa = specialty_pharm.prior_authorization(
    drug_id='HUMIRA-40MG',
    patient_id='PT-123456',
    prescriber='Dr. Williams',
    diagnosis_code='M05.79',  # Rheumatoid arthritis
    clinical_justification='Failed methotrexate and sulfasalazine. Significant disease activity.',
    insurance_info={'payer': 'Blue Cross', 'plan': 'PPO', 'member_id': 'BC123456'}
)

print(f"PA submitted: {pa['pa_id']}, Status: {pa['status']}")

# Financial assistance screening
insurance = {'copay': 500, 'coinsurance': 20}
assistance = specialty_pharm.financial_assistance_screening(
    patient_id='PT-123456',
    drug_id='HUMIRA-40MG',
    annual_income=45000,
    insurance_coverage=insurance
)

print(f"\nEstimated annual cost: ${assistance['estimated_annual_cost']:,.2f}")
print(f"Percent of income: {assistance['pct_of_income']}%")
print(f"\nAssistance programs available: {len(assistance['assistance_programs'])}")
for program in assistance['assistance_programs']:
    print(f"  - {program['program']}: Up to ${program['estimated_savings']:,.0f}")
```

---

## Pharmacy Performance Metrics

### Key Performance Indicators

```python
def calculate_pharmacy_kpis(rx_data_df, inventory_data_df, cs_data_df=None):
    """
    Calculate pharmacy supply chain KPIs

    Parameters:
    - rx_data_df: Prescription dispensing data
    - inventory_data_df: Inventory positions
    - cs_data_df: Controlled substance data (optional)
    """

    kpis = {}

    # Fill rate / Service level
    if 'filled' in rx_data_df.columns:
        kpis['fill_rate'] = (rx_data_df['filled'].sum() / len(rx_data_df) * 100)

    # Inventory turns
    if all(col in inventory_data_df.columns for col in ['annual_usage', 'avg_inventory_value']):
        total_usage_value = inventory_data_df['annual_usage'].sum()
        total_avg_inventory = inventory_data_df['avg_inventory_value'].sum()
        kpis['inventory_turns'] = total_usage_value / total_avg_inventory if total_avg_inventory > 0 else 0

    # Expiry waste rate
    if 'expired' in inventory_data_df.columns:
        expired_value = inventory_data_df[inventory_data_df['expired'] == True]['inventory_value'].sum()
        total_value = inventory_data_df['inventory_value'].sum()
        kpis['expiry_waste_pct'] = (expired_value / total_value * 100) if total_value > 0 else 0

    # Generic dispensing rate (cost savings)
    if 'generic' in rx_data_df.columns:
        kpis['generic_dispensing_rate'] = (rx_data_df['generic'].sum() / len(rx_data_df) * 100)

    # Prescription turnaround time
    if 'turnaround_minutes' in rx_data_df.columns:
        kpis['avg_turnaround_minutes'] = rx_data_df['turnaround_minutes'].mean()

    # 340B capture rate (if applicable)
    if '340b_eligible' in rx_data_df.columns and '340b_used' in rx_data_df.columns:
        eligible = rx_data_df['340b_eligible'].sum()
        used = rx_data_df['340b_used'].sum()
        kpis['340b_capture_rate'] = (used / eligible * 100) if eligible > 0 else 0

    # Controlled substance accuracy (if applicable)
    if cs_data_df is not None and not cs_data_df.empty:
        if 'discrepancy' in cs_data_df.columns:
            kpis['cs_inventory_accuracy'] = (
                (len(cs_data_df[cs_data_df['discrepancy'] == 0]) / len(cs_data_df) * 100)
            )

    # DSCSA compliance rate
    if 'dscsa_compliant' in rx_data_df.columns:
        kpis['dscsa_compliance_rate'] = (rx_data_df['dscsa_compliant'].sum() / len(rx_data_df) * 100)

    # Format KPIs
    for key in kpis:
        if 'rate' in key or 'pct' in key or 'accuracy' in key:
            kpis[key] = round(kpis[key], 2)
        elif 'turns' in key:
            kpis[key] = round(kpis[key], 2)
        else:
            kpis[key] = round(kpis[key], 1)

    return kpis

# Example data
rx_data = pd.DataFrame({
    'rx_number': range(1, 1001),
    'filled': [True] * 980 + [False] * 20,
    'generic': np.random.choice([True, False], 1000, p=[0.85, 0.15]),
    'turnaround_minutes': np.random.normal(20, 5, 1000),
    '340b_eligible': np.random.choice([True, False], 1000, p=[0.40, 0.60]),
    '340b_used': np.random.choice([True, False], 1000, p=[0.35, 0.65]),
    'dscsa_compliant': np.random.choice([True, False], 1000, p=[0.98, 0.02])
})

# Fix 340B logic (can only use if eligible)
rx_data.loc[~rx_data['340b_eligible'], '340b_used'] = False

inventory_data = pd.DataFrame({
    'drug_id': range(1, 501),
    'annual_usage': np.random.randint(1000, 50000, 500),
    'avg_inventory_value': np.random.randint(500, 10000, 500),
    'inventory_value': np.random.randint(500, 10000, 500),
    'expired': np.random.choice([True, False], 500, p=[0.02, 0.98])
})

kpis = calculate_pharmacy_kpis(rx_data, inventory_data)

print("Pharmacy Supply Chain KPIs:")
for metric, value in kpis.items():
    suffix = '%' if any(x in metric for x in ['rate', 'pct', 'accuracy']) else ''
    print(f"  {metric}: {value}{suffix}")
```

---

## Tools & Libraries

### Pharmacy Management Systems

**ERP/Pharmacy Systems:**
- **EPIC Willow Pharmacy**: Integrated with Epic EHR
- **Cerner PharmNet**: Pharmacy management module
- **Omnicell**: Automated dispensing cabinets
- **BD Pyxis**: Medication management system
- **McKesson Pharmacy Systems**: STAR, EnterpriseRx
- **QS/1**: Independent pharmacy management

**Controlled Substance Tracking:**
- **Omnicell ControlledRx**: CS management
- **BD Pyxis CII Safe**: Controlled substance vault
- **Kit Check**: Medication tracking and diversion monitoring
- **Protenus**: AI-powered drug diversion detection

**340B Management:**
- **Kalderos**: 340B claim identification
- **Macro Helix**: 340B program management
- **Verity Solutions**: 340B split-billing
- **RxStrategies**: 340B optimization

**DSCSA Compliance:**
- **TraceLink**: DSCSA compliance platform
- **SAP Information Collaboration Hub for Life Sciences**
- **rfxcel**: Serialization and traceability
- **Systech UniSecure**: Product authentication

### Python Libraries

**Data Analysis:**
- `pandas`: Data manipulation
- `numpy`: Numerical analysis
- `scipy`: Statistical functions

**Regulatory Compliance:**
- `python-barcode`: Barcode generation (NDC)
- `qrcode`: 2D barcode generation
- `hashlib`: Data integrity verification

**Optimization:**
- `pulp`: Linear programming (inventory optimization)
- `scipy.optimize`: Optimization algorithms

**Visualization:**
- `matplotlib`, `seaborn`: Charts and graphs
- `plotly`: Interactive dashboards

---

## Common Challenges & Solutions

### Challenge: DSCSA Compliance by November 2024

**Problem:**
- Electronic, interoperable tracing required
- Legacy systems not compliant
- Trading partner integration
- Serialization at package level

**Solutions:**
- Implement DSCSA-compliant software platform
- Test trading partner connections early
- Staff training on scanning requirements
- Develop suspect product investigation protocols
- Regular compliance audits
- Join industry pilot programs

### Challenge: Controlled Substance Diversion

**Problem:**
- Employee diversion risk
- Documentation gaps
- Inventory discrepancies
- Regulatory penalties

**Solutions:**
- Automated perpetual inventory system
- Two-person verification for Schedule II
- Regular random audits and cycle counts
- Analytics to detect unusual patterns
- Background checks and monitoring
- Clear policies and disciplinary actions
- Confidential reporting mechanisms

### Challenge: 340B Compliance and Audits

**Problem:**
- Complex patient eligibility rules
- Contract pharmacy compliance
- Duplicate discount prevention
- HRSA audits

**Solutions:**
- Automated patient eligibility system
- Electronic health record integration
- Split-billing for Medicaid
- Regular internal compliance audits
- Staff training on eligibility criteria
- Detailed documentation and audit trails
- Work with 340B consultant/expert

### Challenge: Drug Shortages

**Problem:**
- Critical medications unavailable
- Patient care impact
- Therapeutic substitution complexity
- Cost increases from alternatives

**Solutions:**
- Multi-source purchasing strategy
- Early warning monitoring (FDA shortage list)
- Therapeutic substitution protocols
- Conservation strategies for critical patients
- Compounding alternatives (where appropriate)
- Communication with prescribers
- Group purchasing organization leverage

### Challenge: Specialty Medication Costs

**Problem:**
- Extremely high acquisition costs
- Prior authorization delays
- Patient affordability
- Waste from failed PA or non-compliance

**Solutions:**
- Proactive prior authorization
- Financial assistance program navigation
- Buy-and-bill vs. white bagging analysis
- Limited dispensing quantities initially
- Patient adherence support services
- Manufacturer assistance program enrollment
- Specialty pharmacy accreditation

### Challenge: Expiry and Waste

**Problem:**
- Short-dated products
- Slow-moving items
- Storage errors
- Compounded medications

**Solutions:**
- FEFO (first-expired, first-out) enforcement
- Automated expiry alerts
- Right-sizing inventory (data-driven PAR levels)
- Vendor return programs
- Transfer slow-movers between locations
- Just-in-time ordering for slow items
- Beyond-use date (BUD) optimization for compounding

---

## Output Format

### Pharmacy Supply Chain Report

**Executive Summary:**
- Pharmacy overview and scope
- Key performance metrics vs. benchmarks
- Major compliance initiatives
- Financial impact and opportunities

**Inventory Optimization:**

| Drug Category | Items | Inventory Value | Annual Turns | Days on Hand | Expiry Rate | Optimization Opportunity |
|---------------|-------|----------------|--------------|--------------|-------------|--------------------------|
| Antibiotics | 145 | $125,000 | 15.2 | 24 | 0.5% | Reduce safety stock |
| Specialty | 42 | $850,000 | 8.1 | 45 | 1.2% | Buy-and-bill vs. white bag |
| Controlled Substances | 38 | $45,000 | 24.3 | 15 | 0.1% | Appropriate |
| Generic Oral | 1,250 | $180,000 | 18.5 | 20 | 1.8% | Standardization |

**340B Program Performance:**

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Eligible Prescriptions | 2,450/month | - | - |
| 340B Capture Rate | 92.3% | 95% | ⚠ |
| Annual 340B Savings | $1,850,000 | $2,000,000 | ⚠ |
| Contract Pharmacy Compliance | 98.5% | 100% | ⚠ |
| Duplicate Discount Events | 0 | 0 | ✓ |

**Controlled Substance Compliance:**

| Schedule | Items | Perpetual Inv Accuracy | Physical Count Frequency | Discrepancies YTD | Status |
|----------|-------|------------------------|-------------------------|-------------------|--------|
| Schedule II | 15 | 99.8% | Daily | 2 | ✓ |
| Schedule III | 12 | 99.5% | Weekly | 3 | ✓ |
| Schedule IV | 23 | 99.2% | Weekly | 5 | ✓ |

**Active Drug Shortages:**

| Drug Name | NDC | Declared Date | Current Stock | Days Supply | Mitigation Strategy | Status |
|-----------|-----|---------------|---------------|-------------|---------------------|--------|
| Propofol 100mg | 63323-0269-10 | 2024-01-15 | 50 vials | 5 days | Alternative sourcing, therapeutic sub | Critical |
| Cefazolin 1g | 00409-1964-50 | 2024-02-01 | 200 vials | 20 days | Conservation protocol | Monitoring |

**Key Performance Indicators:**

| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| Fill Rate | 98.2% | 98% | ✓ |
| Inventory Turns | 12.5 | 12.0 | ✓ |
| Generic Dispensing Rate | 89.3% | 85% | ✓ |
| Expiry Waste % | 1.2% | <1.5% | ✓ |
| 340B Capture Rate | 92.3% | 95% | ⚠ |
| DSCSA Compliance | 98.1% | 100% | ⚠ |
| Controlled Substance Accuracy | 99.5% | 99% | ✓ |

**Action Items:**
1. Improve 340B capture rate through enhanced eligibility screening
2. Complete DSCSA compliance for remaining 1.9% of transactions
3. Implement automated shortage monitoring system
4. Reduce specialty medication waste through limited initial fills
5. Optimize inventory for slow-moving antibiotics

---

## Questions to Ask

If you need more context:

1. What type of pharmacy? (hospital, retail, specialty, mail-order)
2. Are you a 340B covered entity?
3. What's your DSCSA compliance status?
4. What controlled substance schedules do you handle?
5. What's the current inventory investment and turnover?
6. Are you experiencing specific drug shortages?
7. What pharmacy management system is in use?
8. What are the biggest compliance concerns?
9. Do you dispense specialty medications?
10. What wholesaler/distributor relationships do you have?

---

## Related Skills

- **hospital-logistics**: Hospital materials management
- **medical-device-distribution**: Medical device logistics
- **clinical-trial-logistics**: Clinical trial supply chain
- **inventory-optimization**: Inventory optimization techniques
- **demand-forecasting**: Forecasting for inventory planning
- **compliance-management**: Regulatory compliance systems
- **track-and-trace**: Product traceability and serialization
- **value-analysis**: Value analysis and cost reduction
- **quality-management**: Quality management systems
