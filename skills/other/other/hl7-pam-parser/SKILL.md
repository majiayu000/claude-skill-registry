---
name: hl7-pam-parser
description: Parse and explain HL7 v2.5 IHE PAM (Patient Administration Management) messages. Identifies message type, extracts segments (MSH, EVN, PID, PV1, PV2), validates structure, and provides detailed explanations of ADT messages for patient administration workflows.
---

# HL7 IHE PAM Message Parser and Explainer

## Overview

This skill parses and explains HL7 v2.5 IHE PAM (Patient Administration Management) messages - the standard healthcare interoperability format for patient administration events. The parser identifies message types, extracts segments and fields, validates structure according to IHE PAM 2.10 specifications, and provides human-readable explanations.

**When to use this skill:**
- Parse and explain any HL7 ADT message (raw HL7 text)
- Identify HL7 message type and event code (ADT^A01, ADT^A02, etc.)
- Extract and label all segments and fields (MSH, EVN, PID, PV1, PV2)
- Validate HL7 message structure and required fields
- Understand IHE PAM business rules and field mappings
- Debug HL7 message issues or data quality problems
- Document HL7 message examples with explanations

## HL7 v2.5 Message Format

HL7 messages use specific delimiters:

```
Field delimiter:        |  (pipe)
Component delimiter:    ^  (caret)
Repetition delimiter:   ~  (tilde)
Escape character:       \  (backslash)
Subcomponent delimiter: &  (ampersand)
```

**Basic Structure**:
```
MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|Timestamp||MessageType|MessageControlId|ProcessingId|VersionId
EVN|EventTypeCode|RecordedDateTime|...
PID|SetId||PatientId||PatientName||BirthDate|Sex|...
PV1|SetId|PatientClass|AssignedPatientLocation|...
```

**Segment Terminators**: Each segment ends with carriage return (`\r`) or newline (`\n`)

## IHE PAM Message Types

### ADT Messages (Admit, Discharge, Transfer)

#### ADT^A01 - Admit/Visit Notification
**Purpose**: Patient admission to inpatient care or registration

**Required Segments**:
- MSH (Message Header)
- EVN (Event Type)
- PID (Patient Identification)
- PV1 (Patient Visit)

**Example**:
```
MSH|^~\&|HEXAFLUX|CHU_PARIS|TARGET|DEST|20260122140000||ADT^A01^ADT_A01|MSG001|P|2.5
EVN|A01|20260122140000|||USER001
PID|1||PAT12345^^^CHU_PARIS^PI||DUPONT^JEAN^^M.||19750315|M|||15 RUE DE LA PAIX^^PARIS^^75001^FRA||(33)612345678
PV1|1|I|CHU_PARIS^CARDIO^LIT_001^CHU_PARIS||||PR_MARTIN^MARTIN^SOPHIE|||CARDIO||||||||||VIS20260122001|||||||||||||||||||||||||20260122140000
```

**Explanation**:
- **Event**: A01 (Patient Admission)
- **Patient**: DUPONT JEAN (M.), born 15/03/1975
- **Patient ID**: PAT12345
- **Visit**: VIS20260122001
- **Location**: CHU_PARIS, Cardiology, Bed LIT_001
- **Admission**: 22/01/2026 14:00:00
- **Patient Class**: I (Inpatient)
- **Attending**: Dr. MARTIN SOPHIE

#### ADT^A02 - Transfer a Patient
**Purpose**: Patient transfer between units, rooms, or services

**Required Segments**:
- MSH, EVN, PID, PV1
- PV2 (optional but recommended for prior location)

**Example**:
```
MSH|^~\&|HEXAFLUX|CHU_PARIS|TARGET|DEST|20260123090000||ADT^A02^ADT_A02|MSG002|P|2.5
EVN|A02|20260123090000|||USER002
PID|1||PAT12345^^^CHU_PARIS^PI||DUPONT^JEAN^^M.||19750315|M
PV1|1|I|CHU_PARIS^NEURO^LIT_102^CHU_PARIS||||PR_DURAND^DURAND^PAUL|||NEURO||||||||||VIS20260122001
PV2||||||||||||||||||||||CHU_PARIS^CARDIO^LIT_001^CHU_PARIS
```

**Explanation**:
- **Event**: A02 (Patient Transfer)
- **Patient**: PAT12345 (DUPONT JEAN)
- **From**: Cardiology, Bed LIT_001 (PV2-1: prior location)
- **To**: Neurology, Bed LIT_102 (PV1-3: assigned location)
- **Transfer Time**: 23/01/2026 09:00:00

#### ADT^A03 - Discharge a Patient
**Purpose**: Patient discharge from hospital

**Required Segments**:
- MSH, EVN, PID, PV1

**Example**:
```
MSH|^~\&|HEXAFLUX|CHU_PARIS|TARGET|DEST|20260125180000||ADT^A03^ADT_A03|MSG003|P|2.5
EVN|A03|20260125180000|||USER003
PID|1||PAT12345^^^CHU_PARIS^PI||DUPONT^JEAN^^M.||19750315|M
PV1|1|I|CHU_PARIS^CARDIO^LIT_001^CHU_PARIS||||PR_MARTIN^MARTIN^SOPHIE|||CARDIO||||||||||VIS20260122001|||||||||||||||||||||||||||20260125180000|||||HOME
```

**Explanation**:
- **Event**: A03 (Patient Discharge)
- **Patient**: PAT12345 (DUPONT JEAN)
- **Discharge Time**: 25/01/2026 18:00:00 (PV1-45)
- **Discharge Disposition**: HOME (PV1-36)
- **Visit**: VIS20260122001

#### ADT^A04 - Register a Patient
**Purpose**: Pre-admission or outpatient registration

**Required Segments**:
- MSH, EVN, PID, PV1

#### ADT^A05 - Pre-admit a Patient
**Purpose**: Pre-admission notification

#### ADT^A06 - Change Outpatient to Inpatient
**Purpose**: Convert outpatient visit to inpatient admission

#### ADT^A07 - Change Inpatient to Outpatient
**Purpose**: Convert inpatient admission to outpatient visit

#### ADT^A08 - Update Patient Information
**Purpose**: Update patient demographics

**Example**:
```
MSH|^~\&|HEXAFLUX|CHU_PARIS|TARGET|DEST|20260122150000||ADT^A08^ADT_A08|MSG004|P|2.5
EVN|A08|20260122150000|||USER001
PID|1||PAT12345^^^CHU_PARIS^PI||DUPONT^JEAN^^M.||19750315|M|||15 RUE DE LA PAIX^^PARIS^^75001^FRA||(33)612345678|||||||1234567890123||FRA
PV1|1|O||||||||||||||||||||VIS20260122001
```

**Explanation**:
- **Event**: A08 (Update Patient Information)
- **Patient**: PAT12345 demographics updated
- **Updated Fields**: Address, phone, national identifier (NIR)

#### ADT^A11 - Cancel Admit
**Purpose**: Cancel a previous admission

#### ADT^A12 - Cancel Transfer
**Purpose**: Cancel a previous transfer

#### ADT^A13 - Cancel Discharge
**Purpose**: Cancel a previous discharge

## Segment Definitions

### MSH - Message Header (Required)
**Purpose**: Message metadata and routing information

**Field Structure**:
```
MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|Timestamp||MessageType^EventCode^MessageStructure|MessageControlId|ProcessingId|VersionId
```

**Key Fields**:
- MSH-3: Sending Application
- MSH-4: Sending Facility
- MSH-5: Receiving Application
- MSH-6: Receiving Facility
- MSH-7: Date/Time of Message (YYYYMMDDHHmmss)
- MSH-9: Message Type (ADT^A01^ADT_A01)
- MSH-10: Message Control ID (unique identifier)
- MSH-11: Processing ID (P=Production, T=Training, D=Debugging)
- MSH-12: Version ID (2.5)

### EVN - Event Type (Required)
**Purpose**: Event-specific information

**Field Structure**:
```
EVN|EventTypeCode|RecordedDateTime|EventDateTime|EventReasonCode|OperatorId
```

**Key Fields**:
- EVN-1: Event Type Code (A01, A02, A03, etc.)
- EVN-2: Recorded Date/Time (when event was recorded)
- EVN-3: Event Occurred Date/Time (when event actually occurred)
- EVN-5: Operator ID (user who triggered the event)

### PID - Patient Identification (Required)
**Purpose**: Patient demographic information

**Field Structure** (30+ fields):
```
PID|SetId||PatientId^^^AssigningAuthority^IdType~AltId||LastName^FirstName^MiddleName^Suffix^Prefix||BirthDate|Sex|PatientAlias|Race|PatientAddress||PhoneHome|PhoneBusiness|PrimaryLanguage|MaritalStatus|Religion|PatientAccountNumber|SSN|DriverLicense|MotherIdentifier|EthnicGroup|BirthPlace|MultipleBirth|BirthOrder|Citizenship|VeteranStatus|Nationality|DeathDateTime|DeathIndicator
```

**Key Fields**:
- PID-1: Set ID
- PID-3: Patient Identifier List (PatientId^^^Facility^PI)
- PID-5: Patient Name (LastName^FirstName^MiddleName^Suffix^Prefix)
- PID-7: Date of Birth (YYYYMMDD)
- PID-8: Sex (M/F/O/U)
- PID-11: Patient Address (Street^^City^^PostalCode^Country)
- PID-13: Phone Number - Home
- PID-14: Phone Number - Business
- PID-22: Ethnic Group
- PID-29: Death Date and Time
- PID-30: Death Indicator (Y/N)

### PV1 - Patient Visit (Required)
**Purpose**: Visit/encounter information

**Field Structure** (52 fields):
```
PV1|SetId|PatientClass|AssignedLocation^Room^Bed^Facility|AdmissionType|PreadmitNumber|PriorLocation|AttendingDoctor^LastName^FirstName|ReferringDoctor|ConsultingDoctor|HospitalService|TemporaryLocation|PreadmitTestIndicator|ReadmissionIndicator|AdmitSource|AmbulatoryStatus|VIPIndicator|AdmittingDoctor|PatientType|VisitNumber|FinancialClass
```

**Key Fields**:
- PV1-1: Set ID
- PV1-2: Patient Class (I=Inpatient, O=Outpatient, E=Emergency, R=Recurring)
- PV1-3: Assigned Patient Location (Facility^Service^Room^Bed)
- PV1-4: Admission Type (E=Emergency, R=Routine, etc.)
- PV1-6: Prior Patient Location (for transfers)
- PV1-7: Attending Doctor (DoctorId^LastName^FirstName)
- PV1-10: Hospital Service
- PV1-19: Visit Number (unique visit identifier)
- PV1-36: Discharge Disposition (HOME, SNF, EXP, etc.)
- PV1-44: Admit Date/Time
- PV1-45: Discharge Date/Time

### PV2 - Patient Visit - Additional Info (Optional)
**Purpose**: Extended visit information

**Key Fields**:
- PV2-1: Prior Pending Location (for transfers)
- PV2-3: Admit Reason
- PV2-8: Expected Discharge Date
- PV2-9: Expected Discharge Disposition
- PV2-47: Expected LOA Return Date/Time

## IHE PAM Mandatory Fields

### Required for All ADT Messages
- MSH-3: Sending Application
- MSH-4: Sending Facility
- MSH-7: Date/Time of Message
- MSH-9: Message Type
- MSH-10: Message Control ID
- MSH-12: Version ID (2.5)
- EVN-1: Event Type Code
- EVN-2: Recorded Date/Time
- PID-3: Patient Identifier
- PID-5: Patient Name
- PID-7: Date of Birth
- PID-8: Sex

### Required for Admission/Transfer Messages (A01, A02)
- PV1-2: Patient Class
- PV1-3: Assigned Patient Location
- PV1-19: Visit Number
- PV1-44: Admit Date/Time

### Required for Discharge Messages (A03)
- PV1-36: Discharge Disposition
- PV1-45: Discharge Date/Time

## Parsing Logic

When asked to parse an HL7 IHE PAM message:

1. **Split by segment terminator**: `segments = message.split('\r')` or `split('\n')`

2. **Parse MSH segment** (always first):
   - Extract delimiters from MSH-2: `^~\&`
   - Field delimiter: `|`
   - Component delimiter: `^`
   - Repetition delimiter: `~`
   - Escape character: `\`
   - Subcomponent delimiter: `&`

3. **Identify message type**: Check MSH-9
   - ADT^A01 = Admission
   - ADT^A02 = Transfer
   - ADT^A03 = Discharge
   - etc.

4. **Parse each segment**:
   - Split by field delimiter `|`
   - Parse components with `^`
   - Parse repetitions with `~`
   - Parse subcomponents with `&`

5. **Extract key fields**:
   - Patient ID (PID-3)
   - Patient name (PID-5)
   - Birth date (PID-7)
   - Visit number (PV1-19)
   - Location (PV1-3)
   - Dates (PV1-44, PV1-45)

6. **Validate structure**:
   - Check required segments present
   - Check required fields populated
   - Validate date formats (YYYYMMDD, YYYYMMDDHHmmss)
   - Validate code values (patient class, sex, etc.)

7. **Generate explanation**:
   - Identify message purpose
   - Explain event type
   - List key patient information
   - Describe visit/encounter details
   - Provide clinical context

## Example Output Format

When parsing a message, provide:

```markdown
### HL7 IHE PAM Message Analysis

**Raw Message**:
```
[original HL7 message with visible delimiters]
```

**Message Identification**:
- Message Type: ADT^A01
- Event Code: A01 (Admit/Visit Notification)
- Message Control ID: [MSH-10]
- Timestamp: [formatted MSH-7]
- Version: 2.5

**MSH - Message Header**:
- Sending Application: [MSH-3]
- Sending Facility: [MSH-4]
- Receiving Application: [MSH-5]
- Receiving Facility: [MSH-6]
- Processing ID: [MSH-11] (Production/Test)

**EVN - Event Type**:
- Event Code: [EVN-1]
- Recorded DateTime: [formatted EVN-2]
- Event Occurred: [formatted EVN-3]
- Operator: [EVN-5]

**PID - Patient Identification**:
- Patient ID: [PID-3]
- Patient Name: [formatted PID-5]
- Date of Birth: [formatted PID-7]
- Sex: [PID-8]
- Address: [formatted PID-11]
- Phone: [PID-13]
- [other relevant fields]

**PV1 - Patient Visit**:
- Patient Class: [PV1-2] ([description])
- Assigned Location: [formatted PV1-3]
- Attending Doctor: [formatted PV1-7]
- Hospital Service: [PV1-10]
- Visit Number: [PV1-19]
- Admit DateTime: [formatted PV1-44]
- [other relevant fields based on message type]

**PV2 - Additional Visit Info** (if present):
- Prior Location: [PV2-1]
- [other relevant fields]

**Business Context**:
[Explain what this message represents, the workflow event, and clinical significance]

**IHE PAM Compliance**:
- Required segments: [✓ or ✗ for MSH, EVN, PID, PV1]
- Required fields: [list of mandatory field validation results]
- Field formats: [✓ or ✗ for dates, codes, etc.]
```

## Common ADT Event Codes

| Code | Event Name | Purpose |
|------|------------|---------|
| A01 | Admit/Visit Notification | Patient admission to inpatient care |
| A02 | Transfer a Patient | Transfer between units/rooms |
| A03 | Discharge a Patient | Patient discharge from hospital |
| A04 | Register a Patient | Pre-admission or outpatient registration |
| A05 | Pre-admit a Patient | Notification of planned admission |
| A06 | Change Outpatient to Inpatient | Status change |
| A07 | Change Inpatient to Outpatient | Status change |
| A08 | Update Patient Information | Demographics update |
| A09 | Patient Departing - Tracking | Patient left facility temporarily |
| A10 | Patient Arriving - Tracking | Patient returned to facility |
| A11 | Cancel Admit | Cancel previous admission |
| A12 | Cancel Transfer | Cancel previous transfer |
| A13 | Cancel Discharge | Cancel previous discharge |
| A21 | Patient Goes on Leave of Absence | Temporary leave |
| A22 | Patient Returns from Leave of Absence | Return from leave |
| A28 | Add Person Information | Add new person to database |
| A31 | Update Person Information | Update person demographics |

## Patient Class Codes

| Code | Description |
|------|-------------|
| I | Inpatient |
| O | Outpatient |
| E | Emergency |
| P | Preadmit |
| R | Recurring patient |
| B | Obstetrics |
| C | Commercial Account |
| N | Not Applicable |
| U | Unknown |

## Discharge Disposition Codes

| Code | Description |
|------|-------------|
| HOME | Home or self care |
| SNF | Skilled nursing facility |
| RH | Rehabilitation facility |
| EXP | Expired (deceased) |
| HOS | Hospice |
| AADVICE | Left against medical advice |
| OTH | Other |

## Validation Rules

### Message Structure
- First segment MUST be MSH
- MSH-1 MUST be `|`
- MSH-2 MUST be `^~\&` (encoding characters)
- Segments MUST be separated by CR or LF
- Fields MUST be separated by `|`

### Required Segments by Message Type
- **A01, A04, A05**: MSH, EVN, PID, PV1
- **A02**: MSH, EVN, PID, PV1 (PV2 recommended for prior location)
- **A03**: MSH, EVN, PID, PV1
- **A08**: MSH, EVN, PID (PV1 optional)
- **A11, A12, A13**: MSH, EVN, PID

### Date/Time Formats
- Date: YYYYMMDD
- DateTime: YYYYMMDDHHmmss or YYYYMMDDHHmmss.SSSS
- Time: HHmmss

### Patient Identifier Format
- PID-3: PatientId^^^AssigningAuthority^IdentifierType
- Example: PAT12345^^^CHU_PARIS^PI

### Name Format
- PID-5: LastName^FirstName^MiddleName^Suffix^Prefix^Degree
- Example: DUPONT^JEAN^^M.

### Location Format
- PV1-3: PointOfCare^Room^Bed^Facility^LocationStatus^PersonLocationType^Building
- Example: CHU_PARIS^CARDIO^LIT_001^CHU_PARIS

## Reference Documentation

**IHE PAM Specification**:
- French: https://github.com/Interop-Sante/ihe.iti.pam.fr
- International: https://profiles.ihe.net/ITI/TF/Volume1/ch-14.html

**HL7 v2.5 Standard**:
- Official: http://www.hl7.eu/HL7v2x/v25/std25/ch02.html
- Segments: http://www.hl7.eu/HL7v2x/v25/std25/ch03.html
- Data Types: http://www.hl7.eu/HL7v2x/v25/std25/ch02a.html

**Related Tools**:
- simple-hl7 (Node.js): https://github.com/Bugs5382/node-hl7-client
- HAPI (Java): https://hapifhir.github.io/hapi-hl7v2/

## Quick Reference

### Delimiters
```
|  Field delimiter
^  Component delimiter
~  Repetition delimiter
\  Escape character
&  Subcomponent delimiter
```

### Common Fields
```
MSH-9  : Message Type (ADT^A01^ADT_A01)
MSH-10 : Message Control ID
EVN-1  : Event Type Code (A01, A02, etc.)
EVN-2  : Recorded DateTime
PID-3  : Patient ID
PID-5  : Patient Name
PID-7  : Birth Date
PID-8  : Sex
PV1-2  : Patient Class (I/O/E)
PV1-3  : Assigned Location
PV1-19 : Visit Number
PV1-44 : Admit DateTime
PV1-45 : Discharge DateTime
```
