---
name: healthcare-expert
version: 1.0.0
description: Expert-level healthcare systems, medical informatics, HIPAA compliance, and health data standards
category: domains
tags: [healthcare, medical, hipaa, hl7, fhir, ehr]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Healthcare Expert

Expert guidance for healthcare systems, medical informatics, regulatory compliance (HIPAA), and health data standards (HL7, FHIR).

## Core Concepts

### Healthcare IT
- Electronic Health Records (EHR)
- Health Information Exchange (HIE)
- Clinical Decision Support Systems
- Telemedicine platforms
- Medical imaging systems (PACS)
- Laboratory information systems

### Standards and Protocols
- HL7 (Health Level 7)
- FHIR (Fast Healthcare Interoperability Resources)
- DICOM (Digital Imaging and Communications in Medicine)
- ICD-10 (diagnostic codes)
- CPT (procedure codes)
- SNOMED CT (clinical terminology)

### Regulatory Compliance
- HIPAA (Health Insurance Portability and Accountability Act)
- HITECH Act
- GDPR for health data
- FDA regulations for medical devices
- 21 CFR Part 11 for electronic records

## FHIR Resource Handling

```python
from fhirclient import client
from fhirclient.models import patient, observation, medication
from datetime import datetime

# FHIR Client setup
settings = {
    'app_id': 'my_healthcare_app',
    'api_base': 'https://fhir.example.com/r4'
}
smart = client.FHIRClient(settings=settings)

# Patient resource
def create_patient(first_name, last_name, gender, birth_date):
    """Create FHIR Patient resource"""
    p = patient.Patient()
    p.name = [{
        'use': 'official',
        'family': last_name,
        'given': [first_name]
    }]
    p.gender = gender  # 'male', 'female', 'other', 'unknown'
    p.birthDate = birth_date.isoformat()

    return p.create(smart.server)

# Observation resource (vital signs)
def create_vital_signs_observation(patient_id, code, value, unit):
    """Create vital signs observation"""
    obs = observation.Observation()
    obs.status = 'final'
    obs.category = [{
        'coding': [{
            'system': 'http://terminology.hl7.org/CodeSystem/observation-category',
            'code': 'vital-signs',
            'display': 'Vital Signs'
        }]
    }]

    obs.code = {
        'coding': [{
            'system': 'http://loinc.org',
            'code': code,  # e.g., '8867-4' for heart rate
            'display': 'Heart rate'
        }]
    }

    obs.subject = {'reference': f'Patient/{patient_id}'}
    obs.effectiveDateTime = datetime.now().isoformat()

    obs.valueQuantity = {
        'value': value,
        'unit': unit,
        'system': 'http://unitsofmeasure.org',
        'code': unit
    }

    return obs.create(smart.server)

# Search patients
def search_patients(family_name=None, given_name=None):
    """Search for patients by name"""
    search = patient.Patient.where(struct={})

    if family_name:
        search = search.where(struct={'family': family_name})
    if given_name:
        search = search.where(struct={'given': given_name})

    return search.perform(smart.server)

# Get patient observations
def get_patient_observations(patient_id, category=None):
    """Retrieve patient observations"""
    search = observation.Observation.where(struct={
        'patient': patient_id
    })

    if category:
        search = search.where(struct={'category': category})

    return search.perform(smart.server)
```

## HL7 v2 Message Processing

```python
import hl7

# Parse HL7 message
def parse_hl7_message(message_text):
    """Parse HL7 v2 message"""
    h = hl7.parse(message_text)

    # Extract message type
    message_type = str(h.segment('MSH')[9])

    # Extract patient information from PID segment
    pid = h.segment('PID')
    patient_info = {
        'patient_id': str(pid[3]),
        'name': str(pid[5]),
        'dob': str(pid[7]),
        'gender': str(pid[8])
    }

    return {
        'message_type': message_type,
        'patient': patient_info
    }

# Create ADT^A01 message (Patient Admission)
def create_admission_message(patient_id, patient_name, dob, gender):
    """Create HL7 ADT^A01 admission message"""
    message = hl7.Message(
        "MSH",
        [
            "MSH", "|", "^~\\&", "SENDING_APP", "SENDING_FACILITY",
            "RECEIVING_APP", "RECEIVING_FACILITY",
            datetime.now().strftime("%Y%m%d%H%M%S"), "",
            "ADT^A01", "MSG00001", "P", "2.5"
        ]
    )

    # PID segment
    message.append(hl7.Segment(
        "PID",
        [
            "PID", "", "", patient_id, "",
            patient_name, "", dob, gender
        ]
    ))

    # PV1 segment (Patient Visit)
    message.append(hl7.Segment(
        "PV1",
        [
            "PV1", "", "I", "ER", "", "", "",
            "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", ""
        ]
    ))

    return str(message)

# Validate HL7 message
def validate_hl7_message(message_text):
    """Validate HL7 message structure"""
    try:
        h = hl7.parse(message_text)

        # Check required segments
        if not h.segment('MSH'):
            return False, "Missing MSH segment"

        # Verify message structure
        msh = h.segment('MSH')
        if len(msh) < 12:
            return False, "Invalid MSH segment"

        return True, "Valid HL7 message"
    except Exception as e:
        return False, f"Parsing error: {str(e)}"
```

## HIPAA Compliance Implementation

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import hashlib
import logging
from datetime import datetime

class HIPAACompliantLogger:
    """HIPAA-compliant logging system"""

    def __init__(self, log_file):
        self.logger = logging.getLogger('hipaa_audit')
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_access(self, user_id, patient_id, action, phi_accessed):
        """Log PHI access (HIPAA audit requirement)"""
        self.logger.info(
            f"USER:{user_id} | PATIENT:{patient_id} | "
            f"ACTION:{action} | PHI:{phi_accessed}"
        )

    def log_modification(self, user_id, resource_type, resource_id, changes):
        """Log data modifications"""
        self.logger.info(
            f"USER:{user_id} | MODIFIED:{resource_type}/{resource_id} | "
            f"CHANGES:{changes}"
        )

    def log_disclosure(self, user_id, patient_id, recipient, purpose):
        """Log PHI disclosure"""
        self.logger.info(
            f"DISCLOSURE | USER:{user_id} | PATIENT:{patient_id} | "
            f"TO:{recipient} | PURPOSE:{purpose}"
        )

class PHIEncryption:
    """Encryption for Protected Health Information"""

    def __init__(self, master_key):
        self.fernet = Fernet(master_key)

    def encrypt_phi(self, data):
        """Encrypt PHI data"""
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data)

    def decrypt_phi(self, encrypted_data):
        """Decrypt PHI data"""
        decrypted = self.fernet.decrypt(encrypted_data)
        return decrypted.decode()

    @staticmethod
    def hash_identifier(identifier):
        """Hash patient identifiers for de-identification"""
        return hashlib.sha256(identifier.encode()).hexdigest()

class HIPAAAccessControl:
    """Role-based access control for HIPAA compliance"""

    ROLES = {
        'physician': ['read', 'write', 'prescribe'],
        'nurse': ['read', 'write'],
        'administrative': ['read'],
        'patient': ['read_own']
    }

    def __init__(self, user_role):
        self.role = user_role
        self.permissions = self.ROLES.get(user_role, [])

    def can_access(self, action, patient_id, user_patient_id=None):
        """Check if user can perform action"""
        if action not in self.permissions:
            if action == 'read' and 'read_own' in self.permissions:
                return patient_id == user_patient_id
            return False

        return True

    def require_permission(self, action):
        """Decorator for enforcing permissions"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if action not in self.permissions:
                    raise PermissionError(
                        f"Role '{self.role}' lacks permission: {action}"
                    )
                return func(*args, **kwargs)
            return wrapper
        return decorator
```

## Electronic Health Record System

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Patient:
    """Patient record"""
    patient_id: str
    mrn: str  # Medical Record Number
    first_name: str
    last_name: str
    dob: datetime
    gender: str
    ssn: Optional[str]  # Encrypted
    address: dict
    phone: str
    email: str
    emergency_contact: dict
    insurance: dict

@dataclass
class Encounter:
    """Clinical encounter"""
    encounter_id: str
    patient_id: str
    encounter_date: datetime
    encounter_type: str  # 'inpatient', 'outpatient', 'emergency'
    chief_complaint: str
    provider_id: str
    facility_id: str
    diagnosis_codes: List[str]  # ICD-10
    procedure_codes: List[str]  # CPT
    notes: str

@dataclass
class Medication:
    """Medication order"""
    medication_id: str
    patient_id: str
    drug_name: str
    dosage: str
    frequency: str
    route: str  # 'oral', 'IV', etc.
    start_date: datetime
    end_date: Optional[datetime]
    prescriber_id: str
    pharmacy_notes: str

class EHRSystem:
    """Electronic Health Record system"""

    def __init__(self, db, logger, access_control, encryption):
        self.db = db
        self.logger = logger
        self.access_control = access_control
        self.encryption = encryption

    def get_patient_record(self, user_id, patient_id):
        """Retrieve patient record with audit logging"""
        # Check permissions
        if not self.access_control.can_access('read', patient_id):
            self.logger.log_access(
                user_id, patient_id, 'DENIED', 'patient_record'
            )
            raise PermissionError("Access denied")

        # Log access
        self.logger.log_access(
            user_id, patient_id, 'READ', 'patient_record'
        )

        # Retrieve and decrypt
        patient = self.db.get_patient(patient_id)
        if patient.ssn:
            patient.ssn = self.encryption.decrypt_phi(patient.ssn)

        return patient

    def create_encounter(self, user_id, encounter: Encounter):
        """Create clinical encounter"""
        if not self.access_control.can_access('write', encounter.patient_id):
            raise PermissionError("Cannot create encounter")

        # Encrypt sensitive data
        if encounter.notes:
            encounter.notes = self.encryption.encrypt_phi(encounter.notes)

        # Save encounter
        self.db.save_encounter(encounter)

        # Log creation
        self.logger.log_modification(
            user_id, 'encounter', encounter.encounter_id, 'created'
        )

        return encounter

    def get_patient_medications(self, user_id, patient_id):
        """Get active medications for patient"""
        if not self.access_control.can_access('read', patient_id):
            raise PermissionError("Access denied")

        self.logger.log_access(
            user_id, patient_id, 'READ', 'medications'
        )

        return self.db.get_active_medications(patient_id)

    def prescribe_medication(self, user_id, medication: Medication):
        """Prescribe new medication"""
        if not self.access_control.can_access('prescribe', medication.patient_id):
            raise PermissionError("Cannot prescribe medication")

        # Drug interaction check
        active_meds = self.get_patient_medications(user_id, medication.patient_id)
        interactions = self.check_drug_interactions(medication, active_meds)

        if interactions:
            return {'status': 'warning', 'interactions': interactions}

        self.db.save_medication(medication)

        self.logger.log_modification(
            user_id, 'medication', medication.medication_id, 'prescribed'
        )

        return {'status': 'success', 'medication_id': medication.medication_id}

    def check_drug_interactions(self, new_med, existing_meds):
        """Check for drug-drug interactions"""
        # This would integrate with a drug interaction database
        interactions = []
        # Implementation would check against drug interaction database
        return interactions
```

## Best Practices

### Security and Compliance
- Encrypt PHI at rest and in transit
- Implement comprehensive audit logging
- Use role-based access control
- Conduct regular security assessments
- Implement data backup and disaster recovery
- Train staff on HIPAA requirements
- Use de-identification for research data

### Data Standards
- Use standard terminologies (SNOMED, LOINC)
- Implement FHIR for interoperability
- Support HL7 messaging
- Use ICD-10 for diagnoses
- Use CPT for procedures
- Validate data quality

### System Design
- Design for high availability
- Implement redundancy
- Ensure data integrity
- Support audit trails
- Enable patient access portals
- Integrate with HIE networks

## Anti-Patterns

❌ Storing PHI unencrypted
❌ No audit logging
❌ Inadequate access controls
❌ Using proprietary formats
❌ No data backup strategy
❌ Ignoring interoperability standards
❌ Weak authentication

## Resources

- FHIR Specification: https://hl7.org/fhir/
- HL7 International: https://www.hl7.org/
- HIPAA Guidelines: https://www.hhs.gov/hipaa/
- ICD-10: https://www.who.int/classifications/icd/
- LOINC: https://loinc.org/
- SNOMED CT: https://www.snomed.org/
