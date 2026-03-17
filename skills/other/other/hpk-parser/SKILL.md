---
name: hpk-parser
description: Comprehensive HPK (proprietary healthcare message format) parser and explainer. Supports 100+ message types across patient administration (ID, MV, CV), supply chain (PR, FO, MA, CO, LI, RO, FA), inventory (SO, IM), organizational structure (ST, UT), and financial operations (RD, DD). Uses @erp-pas/hpk-dictionary as source of truth. Validates structure, extracts fields, explains business context, maps to HL7 v2.5/IHE PAM, and troubleshoots integration issues.
---

# HPK Message Parser and Explainer

## Overview

This skill parses and explains HPK (Healthcare Protocol Kernel) messages - a proprietary pipe-delimited healthcare message format used in the Hexagone system for French healthcare environments. The parser supports 100+ message types across multiple domains (patient administration, supply chain, inventory, financial, organizational), identifies message types, extracts all fields, validates structure, and provides human-readable explanations based on the official HPK dictionary and specifications.

**Primary Sources of Truth**:
1. **HPK Dictionary** (`@erp-pas/hpk-dictionary`) - GitLab repository with complete message schemas, field definitions, and validation rules
2. **HPK ADT Message Specification** - Comprehensive field definitions for patient administration messages
3. **HPK GEF Specification** - Workflow integration and economic/financial management messages

**Coverage**:
- **Patient Administration**: Identity (ID), Movements (MV), Coverage (CV) - 12+ message types
- **Supply Chain**: Products (PR), Suppliers (FO), Markets (MA), Orders (CO), Deliveries (LI), Receptions (RO) - 20+ message types
- **Financial**: Invoices (FA), Miscellaneous Receipts (RD) - 4+ message types
- **Inventory**: Stock movements (SO), Asset inventory (IM) - 5+ message types
- **Organizational**: Structures (ST), Users (UT) - 6+ message types
- **Requests**: Creation requests (DD) - 2+ message types

**When to use this skill:**
- Parse and explain any HPK message (raw text input from any system domain)
- Identify HPK message type and mode (ID|M1|C, MV|M2|C, PR|M0|C, etc.)
- Extract and label all HPK fields according to specification
- Validate HPK message structure, field count, and data types
- Understand HPK business rules and field mappings
- Debug HPK message issues or data quality problems
- Document HPK message examples with explanations
- Verify HPK dictionary compliance and field definitions
- Map HPK messages to HL7 v2.5 or IHE PAM equivalents
- Analyze HPK message flows in Hexagone WEB integration scenarios
- Support development of HPK message generators or parsers
- Troubleshoot Hexagone WEB to external system interfaces

## HPK Message Format

HPK messages use pipe (`|`) as field delimiter with the following structure:

```
Type|Message|Mode|Emetteur|Date|User|...additional fields...
```

**Core Fields (positions 0-5):**
- **Field 0**: Message Type (`ID` = Identity, `MV` = Movement, `CV` = Coverage)
- **Field 1**: Message Code (`M1`, `M2`, `M3`, `M6`, `M8`, `M9`, `MT`, `CE`, `B1`, etc.)
- **Field 2**: Mode (`C` = Creation, `M` = Modification, `D` = Deletion)
- **Field 3**: Emetteur (Sender/Source System)
- **Field 4**: Date/Time (format: `YYYYMMDDHHmmss`)
- **Field 5**: User ID

## Message Types

### Identity Messages (ID|*)

#### ID|M1 - Patient Identity (Creation/Modification)
**Purpose**: Patient demographic information (registration)

**Field Structure** (38 fields total):
```
0:  Type (ID)
1:  Message (M1)
2:  Mode (C/M/D)
3:  Emetteur (Sender)
4:  Date (YYYYMMDDHHmmss)
5:  User
6:  IPP (Patient ID)
7:  Nom (Last Name)
8:  Prénom (First Name)
9:  Date de naissance (YYYYMMDD)
10: Sexe (M/F/U)
11: Adresse
12: Code postal
13: Ville
14: Pays
15: Téléphone
16: Téléphone portable
17: Email
18: Nom de naissance
19: Prénom usuel
20: Situation familiale
21: Nombre d'enfants
22: Profession
23: Médecin traitant
24: Établissement de naissance
25: Ville de naissance
26: Pays de naissance
27: Nationalité
28: INS (Identifiant National de Santé)
29: INS-C (Calcul)
30: NIR (Numéro de Sécurité Sociale)
31: Clé NIR
32: OID NIR
33: Matricule d'identité
34: Pays identité
35: Date décès (YYYYMMDD)
36: Indicateur de décès
37: Commentaire
```

**Example**:
```
ID|M1|C|HEXAGONE|20260122120000|USER001|PAT12345|DUPONT|JEAN|19750315|M|15 RUE DE LA PAIX|75001|PARIS|FRA|0612345678||||||||||||||||||||||||||||||
```

**Explanation**:
- **Type**: Identity message
- **Code**: M1 (Patient demographics)
- **Mode**: C (Creation - new patient registration)
- **Patient**: DUPONT JEAN, born 15/03/1975, Male
- **Contact**: 06 12 34 56 78, 15 RUE DE LA PAIX, 75001 PARIS, France
- **System**: Message from HEXAGONE system, user USER001, timestamp 22/01/2026 12:00:00

#### ID|MT - Treating Physician
**Purpose**: Assign or update patient's treating physician (médecin traitant)

**Field Structure** (13 fields total):
```
0:  Type (ID)
1:  Message (MT)
2:  Mode (C/M/D)
3:  Emetteur
4:  Date
5:  User
6:  IPP
7:  Code médecin traitant
8:  Nom médecin traitant
9:  Prénom médecin traitant
10: Spécialité
11: Date début
12: Date fin
```

**Example**:
```
ID|MT|C|HEXAGONE|20260122120000|USER001|PAT12345|PR_MARTIN|MARTIN|SOPHIE|CARDIOLOGUE|20260122||
```

**Explanation**:
- **Type**: Identity message
- **Code**: MT (Médecin Traitant - Treating Physician)
- **Mode**: C (Creation - assign new treating physician)
- **Patient**: PAT12345
- **Physician**: Dr. MARTIN SOPHIE, Cardiologist, code PR_MARTIN
- **Effective**: From 22/01/2026 (no end date)

#### ID|CE - Informed Consent
**Purpose**: Record patient consent for treatment/data processing

**Field Structure** (11 fields total):
```
0:  Type (ID)
1:  Message (CE)
2:  Mode (C/M/D)
3:  Emetteur
4:  Date
5:  User
6:  IPP
7:  Type consentement
8:  Statut (OUI/NON)
9:  Date début validité
10: Date fin validité
```

### Movement Messages (MV|*)

#### MV|M2 - Patient Admission
**Purpose**: Hospital admission (admission hospitalière)

**Field Structure** (19 fields total):
```
0:  Type (MV)
1:  Message (M2)
2:  Mode (C/M/D)
3:  Emetteur
4:  Date
5:  User
6:  IPP
7:  Numéro de séjour (Visit ID)
8:  Date/heure entrée (YYYYMMDDHHmmss)
9:  Mode d'entrée (URGENCE/MUTATION/DOMICILE)
10: Établissement
11: Service
12: Unité fonctionnelle (UF)
13: Lit
14: Médecin responsable
15: Provenance
16: Type hospitalisation
17: Mode de traitement
18: Motif d'admission
```

**Example**:
```
MV|M2|C|HEXAGONE|20260122140000|USER001|PAT12345|VIS20260122001|20260122140000|URGENCE|CHU_PARIS|CARDIO|UF_CARDIO_01|LIT_001|PR_MARTIN|||||||
```

**Explanation**:
- **Type**: Movement message
- **Code**: M2 (Hospital admission)
- **Mode**: C (Creation - new admission)
- **Patient**: PAT12345
- **Visit**: VIS20260122001 (unique visit identifier)
- **Admission**: 22/01/2026 14:00:00 via Emergency Department
- **Location**: CHU_PARIS, Cardiology service, UF_CARDIO_01, Bed LIT_001
- **Care Team**: Attending physician PR_MARTIN

#### MV|M3 - Status Change
**Purpose**: Change in patient administrative status

**Field Structure**:
```
0-5:  Common fields (Type, Message, Mode, Emetteur, Date, User)
6:    IPP
7:    Numéro de séjour
8:    Ancien statut
9:    Nouveau statut
10:   Date changement statut
11:   Motif changement
```

#### MV|M6 - Unit Entry/Transfer
**Purpose**: Patient transfer between units or services

**Field Structure** (18 fields total):
```
0:  Type (MV)
1:  Message (M6)
2:  Mode (C/M/D)
3:  Emetteur
4:  Date
5:  User
6:  IPP
7:  Numéro de séjour
8:  Nouvelle UF
9:  Nouveau lit
10: Nouveau service
11: Ancienne UF
12: Ancien lit
13: Ancien service
14: Date/heure mouvement
15: Mode de transfert
16: Nouveau médecin responsable
17: Motif de transfert
```

**Example**:
```
MV|M6|C|HEXAGONE|20260123090000|USER002|PAT12345|VIS20260122001|UF_NEURO_01|LIT_102|NEURO|UF_CARDIO_01|LIT_001|CARDIO||||||
```

**Explanation**:
- **Type**: Movement message
- **Code**: M6 (Unit transfer)
- **Mode**: C (Creation - new transfer event)
- **Patient**: PAT12345 in visit VIS20260122001
- **From**: Cardiology UF_CARDIO_01, Bed LIT_001
- **To**: Neurology UF_NEURO_01, Bed LIT_102
- **Timestamp**: 23/01/2026 09:00:00

#### MV|M8 - Unit Exit
**Purpose**: Exit from functional unit (without discharge)

**Field Structure**:
```
0-5:  Common fields
6:    IPP
7:    Numéro de séjour
8:    UF de sortie
9:    Date/heure sortie UF
10:   Destination
11:   Mode de sortie
```

#### MV|M9 - Hospital Discharge
**Purpose**: Patient discharge from hospital

**Field Structure** (14 fields total):
```
0:  Type (MV)
1:  Message (M9)
2:  Mode (C/M/D)
3:  Emetteur
4:  Date
5:  User
6:  IPP
7:  Numéro de séjour
8:  Date/heure sortie (YYYYMMDDHHmmss)
9:  Mode de sortie (DOMICILE/MUTATION/DECES)
10: Destination
11: État à la sortie (AMELIORE/STATIONNAIRE/AGGRAVE)
12: Médecin ayant autorisé la sortie
13: Motif de sortie
```

**Example**:
```
MV|M9|C|HEXAGONE|20260125180000|USER003|PAT12345|VIS20260122001|20260125180000|DOMICILE||AMELIORE||||
```

**Explanation**:
- **Type**: Movement message
- **Code**: M9 (Hospital discharge)
- **Mode**: C (Creation - new discharge event)
- **Patient**: PAT12345, visit VIS20260122001
- **Discharge**: 25/01/2026 18:00:00
- **Destination**: DOMICILE (Home)
- **Status**: AMELIORE (Improved condition)

#### MV|B1 - Urgency/Box Movement
**Purpose**: Emergency department box movement

**Field Structure**:
```
0-5:  Common fields
6:    IPP
7:    Numéro de passage aux urgences
8:    Box de départ
9:    Box d'arrivée
10:   Date/heure mouvement
11:   Motif
```

#### MV|MT - Temporary Movement
**Purpose**: Temporary patient movement (exam, procedure)

**Field Structure**:
```
0-5:  Common fields
6:    IPP
7:    Numéro de séjour
8:    Lieu de départ
9:    Lieu d'arrivée
10:   Date/heure départ
11:   Date/heure retour prévue
12:   Motif (EXAMEN/BLOC/RADIOLOGIE)
```

### Coverage Messages (CV|*)

#### CV|M1 - Insurance Coverage
**Purpose**: Patient insurance and coverage information

**Field Structure** (20 fields total):
```
0:  Type (CV)
1:  Message (M1)
2:  Mode (C/M/D)
3:  Emetteur
4:  Date
5:  User
6:  IPP
7:  Organisme payeur
8:  Code régime
9:  Caisse
10: Centre
11: Numéro adhérent
12: Clé adhérent
13: Rang bénéficiaire
14: Date début droits
15: Date fin droits
16: Type couverture (CPAM/MUTUELLE/AME)
17: Taux de remboursement
18: ALD (Affection Longue Durée)
19: CMU/CMUC
```

**Example**:
```
CV|M1|C|HEXAGONE|20260122120000|USER001|PAT12345|CPAM75|01|750|001|1234567890|12|00|20260101|20261231|CPAM|100|OUI|NON
```

**Explanation**:
- **Type**: Coverage message
- **Code**: M1 (Insurance information)
- **Patient**: PAT12345
- **Insurer**: CPAM 75 (Paris Social Security), code 01/750/001
- **Member**: #1234567890, key 12, rank 00 (primary insured)
- **Validity**: 01/01/2026 to 31/12/2026
- **Coverage**: CPAM (National Health Insurance), 100% reimbursement
- **Special**: ALD (Long-term condition) = YES, CMU = NO

## Parsing Logic

When asked to parse an HPK message:

### Step 1: Split and Identify

1. **Split by pipe delimiter**: `fields = message.split('|')`

2. **Identify message type**: Check fields[0], fields[1], and fields[2]
   - Type: fields[0] (ID, MV, CV, PR, FO, MA, CO, LI, RO, FA, SO, RD, IM, DD, UT, ST)
   - Message code: fields[1] (M1, M2, M3, M6, M8, M9, MT, CE, B1, etc.)
   - Mode: fields[2] (C=Creation, M=Modification, S/D=Suppression/Deletion)

3. **Look up in HPK Dictionary**: Use message key `{Type}|{Message}` to get field definitions from `@erp-pas/hpk-dictionary`

### Step 2: Extract Base Fields

Extract standard header fields (always present in positions 0-5):

| Position | Field | Format | Description |
|----------|-------|--------|-------------|
| 0 | Type | 2 chars | Message category |
| 1 | Message | 2 chars | Specific message type |
| 2 | Mode | 1 char | Operation (C/M/S/D) |
| 3 | Emetteur | 15 chars | Sender system |
| 4 | Date | 16 chars | Timestamp (YYYYMMDDHHMISSnn) |
| 5 | User | 50 chars | User identifier |

### Step 3: Extract Type-Specific Fields

Based on message type, extract remaining fields:

**ID|M1** (Identity - fields 6-37):
- 6: IPP (Patient ID)
- 7: Nom (Last Name)
- 8: Prénom (First Name)
- 9: Date de naissance (YYYYMMDD)
- 10: Sexe (M/F/U)
- 11-37: Additional demographic fields

**MV|M2** (Admission - fields 6-18):
- 6: IPP
- 7: Numéro de séjour (Visit ID)
- 8: Date/heure entrée
- 9: Mode d'entrée
- 10-18: Location and care team details

**MV|M6** (Transfer - fields 6-17):
- 6: IPP
- 7: Numéro de séjour
- 8-10: New location (UF, Bed, Service)
- 11-13: Previous location
- 14-17: Transfer details

**MV|M9** (Discharge - fields 6-13):
- 6: IPP
- 7: Numéro de séjour
- 8: Date/heure sortie
- 9: Mode de sortie
- 10-13: Discharge details

**CV|M1** (Coverage - fields 6-19):
- 6: IPP
- 7-19: Insurance and coverage details

### Step 4: Format Data

Apply formatting based on data types:

1. **Date fields** (YYYYMMDD):
   - Parse: `20260122` → `22/01/2026`
   - Validation: Check valid date

2. **DateTime fields** (YYYYMMDDHHMISSnn):
   - Parse: `20260122140530` → `22/01/2026 14:05:30`
   - nn = centiseconds (usually ignored in display)

3. **Enumerated values**:
   - Gender: M (Male), F (Female), U (Unknown)
   - Mode: C (Creation), M (Modification), S/D (Suppression)
   - Entry modes: URGENCE, MUTATION, DOMICILE, etc.

4. **Empty fields**: 
   - Empty string or consecutive pipes `||`
   - Display as "Not provided" or leave blank

### Step 5: Validate Message

Using HPK Dictionary definitions:

1. **Field count validation**:
   ```
   expected_count = len(dictionary[message_key].fields)
   actual_count = len(fields)
   if actual_count != expected_count:
       warn("Field count mismatch")
   ```

2. **Required field validation**:
   ```
   for field_def in dictionary[message_key].fields:
       if field_def.isMandatory and not fields[field_def.position]:
           error(f"Missing required field: {field_def.description}")
   ```

3. **Type validation**:
   - Date: Check format YYYYMMDD and valid date
   - Number: Check numeric and within range
   - String: Check length <= maximum

4. **Length validation**:
   ```
   if len(field_value) > field_def.length:
       warn(f"Field exceeds maximum length: {field_def.description}")
   ```

### Step 6: Generate Explanation

Provide context and interpretation:

1. **Message purpose**: Describe what this message does
2. **Operation type**: Explain C/M/S/D mode
3. **Key data points**: Highlight important clinical/administrative data
4. **Business context**: Explain workflow implications
5. **Related messages**: Mention typical message sequences

## Validation Rules

### Structural Validation

1. **Message format**: Must start with valid Type|Message|Mode pattern
2. **Uppercase header**: First 6 fields must be uppercase
3. **Pipe delimiter**: Fields separated by `|` (ASCII 124)
4. **No spaces**: Empty fields represented as `||` not `| |`
5. **Trailing pipes**: May have trailing pipes for optional fields

### Field-Level Validation

From HPK Dictionary `isMandatory` and `type` properties:

1. **Required fields**: Must not be empty if `isMandatory: true`
2. **Date format**: Must match YYYYMMDD or YYYYMMDDHHMISSnn
3. **Numeric fields**: Must contain only digits (and decimal point if applicable)
4. **Length limits**: Must not exceed `length` property from dictionary
5. **Enumerated values**: Must match allowed values (check `comment` field)

### Business Logic Validation

From HPK specifications and business rules:

1. **IPP consistency**: Same IPP across related messages in a sequence
2. **Visit number**: MV messages for same episode must share visit number
3. **Date sequences**: 
   - Admission date ≤ Transfer date ≤ Discharge date
   - Start date ≤ End date for coverage periods
4. **Location references**: Service/Unit/Bed must exist in organizational structure
5. **Practitioner references**: Physician codes must be valid in system

### Data Quality Checks

1. **Date reasonableness**:
   - Birth date not in future
   - Admission date within reasonable range
   - Not more than 120 years old (unless special case)

2. **Identifier formats**:
   - IPP: Check format and checksum (if applicable)
   - NIR: 15 digits (13 + 2 key) with Luhn validation
   - FINESS: 9 digits for facilities

3. **Code validity**:
   - Gender codes: M, F, U only
   - Country codes: ISO 3166-1 alpha-3 (FRA, etc.)
   - Insurance regime codes: Check against référentiel

### Error Reporting

When validation fails, report:

```markdown
**Validation Issues**:
❌ **Error**: Missing required field at position 7 (Last Name)
⚠️  **Warning**: Field 9 (Birth Date) exceeds maximum length
⚠️  **Warning**: Field count mismatch - expected 38, got 35
ℹ️  **Info**: Optional field 16 (Mobile phone) not provided
```

Severity levels:
- **Error** (❌): Message cannot be processed
- **Warning** (⚠️): Message may have issues but can be processed
- **Info** (ℹ️): Optional fields or minor issues

## Example Output Format

When parsing a message, provide:

```markdown
### HPK Message Analysis

**Raw Message**:
```
[original HPK message]
```

**Message Identification**:
- Type: [ID/MV/CV]
- Code: [M1/M2/M6/M9/etc.]
- Full Name: [descriptive name]
- Operation: [Creation/Modification/Deletion]

**Core Fields**:
- Sender System: [emetteur]
- Timestamp: [formatted date/time]
- User: [user ID]

**[Type]-Specific Fields**:
[List all relevant fields with labels and values]

**Business Context**:
[Explain what this message represents and its purpose]

**Validation**:
- Field count: [actual] (expected: [expected for this type])
- Required fields: [✓ or ✗ for each required field]
- Date formats: [✓ or ✗]
- Enumerated values: [✓ or ✗]
```

## HPK Dictionary Integration

### GitLab Repository
**Repository**: https://gitlab-erp-pas.dedalus.lan/erp-pas/hexagone/hpk-dictionary  
**Package**: `@erp-pas/hpk-dictionary` (NPM)  
**Version**: 1.0.5+  
**Purpose**: Authoritative source of truth for all HPK message definitions

### Dictionary Structure

The HPK dictionary is an NPM package that provides comprehensive message definitions for the Hexagone healthcare system. Each message type includes:

```javascript
{
  description: String,        // Human-readable message description
  fields: Array[{
    position: Number,         // Field position (1-based)
    description: String,      // Field description
    length: Number,          // Maximum field length
    type: String,            // Data type (String, Number, Date, etc.)
    isMandatory: Boolean,    // Required field flag
    comment: String          // Additional notes/rules
  }]
}
```

### Dictionary Access Example

```javascript
const hpk = require('@erp-pas/hpk-dictionary')

// Access message definition
const idM1 = hpk.segments['ID|M1']
console.log(idM1.description)  // "Suppression Identité Patient"

// Iterate through field definitions
idM1.fields.forEach(field => {
  console.log(`${field.position}. ${field.description} (${field.type}, max: ${field.length})`)
  if (field.isMandatory) console.log('   ⚠️  Required')
})
```

### Message Categories in Dictionary

The HPK dictionary defines 100+ message types across these domains:

#### Identity & User Management (ID, UT)
- **ID|M1**: Patient identity creation/modification
- **ID|MT**: Treating physician assignment
- **ID|CE**: Informed consent
- **UT|A1**: User account management

#### Patient Movements (MV)
- **MV|M2**: Hospital admission
- **MV|M3**: Administrative status change
- **MV|M6**: Unit/service transfer
- **MV|M8**: Functional unit exit
- **MV|M9**: Hospital discharge
- **MV|B1**: Emergency box movement
- **MV|MT**: Temporary movement (exam, procedure)

#### Coverage & Financial (CV, FA)
- **CV|M1**: Insurance coverage information
- **FA|FE**: Invoice header
- **FA|FL**: Invoice lines

#### Organizational Structure (ST)
- **ST|EJ**: Legal establishment (Établissement Juridique)
- **ST|EG**: Geographic establishment (Établissement Géographique)
- **ST|BA**: Building (Bâtiment)
- **ST|ET**: Floor (Étage)
- **ST|CH**: Room (Chambre)

#### Supply Chain Management (PR, FO, MA, CO, LI, RO)
- **PR|M0-M5**: Product management
- **FO|M1-M3**: Supplier management
- **MA|M1-M3**: Contract/market management
- **CO|M1-M2**: Orders
- **LI|M1-M2**: External deliveries
- **RO|M1-M2**: Receptions

#### Inventory & Stock (SO, IM)
- **SO|S1**: Stock output
- **SO|I1**: Inventory
- **SO|T1**: Stock transfer
- **SO|L1**: Pre-established lists
- **IM|M1**: Asset inventory

#### Miscellaneous (RD, DD)
- **RD|E1/L1**: Miscellaneous receipts
- **DD|M1/K1**: Request messages

### Using Dictionary for Validation

When parsing HPK messages, use the dictionary to:

1. **Validate field count**: Check actual vs. expected field count from dictionary
2. **Verify required fields**: Use `isMandatory` flag to ensure all required fields present
3. **Type validation**: Use `type` field to validate data format (Date, Number, String)
4. **Length validation**: Use `length` field to ensure values don't exceed maximum
5. **Business rules**: Use `comment` field for additional validation logic

### Field Type Reference

From HPK dictionary:
- **String**: Text fields (alphanumeric)
- **Number**: Numeric fields (may include decimal precision like `9999.99`)
- **Date**: Date fields (YYYYMMDD or YYYYMMDDHHMISSnn format)
- **Boolean**: True/False values (represented as T/F or O/N in French: Oui/Non)

## Reference Documentation

**Primary Source of Truth**:
- [HPK Dictionary Repository](https://gitlab-erp-pas.dedalus.lan/erp-pas/hexagone/hpk-dictionary) - Complete message definitions with field schemas, validation rules, and data types

**Internal Documentation**:
- [HPK ADT Message Specification](../../docs/hpk-adt-message.md) - Complete field definitions and business rules for ADT messages
- [HPK GEF Specification](../../docs/specification-hpk-gef.md) - Workflow and integration details for economic and financial management

**Related Standards** (for context):
- IHE PAM 2.10 Specification: https://github.com/Interop-Sante/ihe.iti.pam.fr
- HL7 v2.5 Standard: http://www.hl7.eu/HL7v2x/v25/std25/ch02.html

## Important Notes

### Message Format Standards
1. **First 6 fields MUST be uppercase** (Type, Message, Mode, Emetteur, Date, User)
2. **Pipe separator**: Use `|` as field delimiter
3. **Empty fields**: Represented by consecutive pipes `||` (no spaces)
4. **Maximum lengths**: Specified in dictionary - do not exceed
5. **Date format**: YYYYMMDDHHMISSnn (where nn = centiseconds)
## HPK to HL7 Mapping

### Standard Message Mappings

HPK messages are often mapped to HL7 v2.5 / IHE PAM format for interoperability. The fixtures directory contains examples of these mappings.

#### Identity Messages (ID) → HL7 ADT Messages

| HPK Message | HL7 Message | IHE Event | Description |
|-------------|-------------|-----------|-------------|
| ID\|M1\|C   | ADT^A28     | Patient Add | Register new patient |
| ID\|M1\|M   | ADT^A31     | Patient Update | Update patient demographics |
| ID\|M1\|D   | ADT^A29     | Patient Delete | Delete patient record |
| ID\|MT\|C   | ADT^A28     | - | Add/update treating physician |
| ID\|CE\|C   | ADT^A28     | - | Record informed consent |

#### Movement Messages (MV) → HL7 ADT Messages

| HPK Message | HL7 Message | IHE Event | Description |
|-------------|-------------|-----------|-------------|
| MV\|M2\|C   | ADT^A01     | Admit Patient [ITI-31] | Hospital admission |
| MV\|M3\|C   | ADT^A06     | - | Status change (to outpatient) |
| MV\|M6\|C   | ADT^A02     | Transfer Patient [ITI-32] | Unit/service transfer |
| MV\|M8\|C   | ADT^A02     | - | Unit exit (internal transfer) |
| MV\|M9\|C   | ADT^A03     | Discharge Patient [ITI-33] | Hospital discharge |
| MV\|B1\|C   | ADT^A02     | - | Emergency box movement |
| MV\|MT\|C   | ADT^A09/A10 | - | Temporary leave/return |

#### Coverage Messages (CV) → HL7 Segments

| HPK Message | HL7 Segments | Description |
|-------------|--------------|-------------|
| CV\|M1\|C   | IN1 + IN2    | Primary insurance |
| CV\|M1\|M   | IN1 + IN2    | Insurance update |

### Key Field Mappings

#### HPK ID|M1 → HL7 ADT PID Segment

| HPK Field (Position) | HPK Description | HL7 Field | HL7 Description |
|---------------------|-----------------|-----------|-----------------|
| 6 | IPP | PID-3 | Patient Identifier List |
| 7 | Nom | PID-5.1 | Patient Name - Family Name |
| 8 | Prénom | PID-5.2 | Patient Name - Given Name |
| 9 | Date de naissance | PID-7 | Date/Time of Birth |
| 10 | Sexe | PID-8 | Administrative Sex |
| 11-14 | Adresse, CP, Ville, Pays | PID-11 | Patient Address |
| 15-16 | Téléphone | PID-13 | Phone Number - Home |
| 28 | INS | PID-3 | National Health ID (OID 1.2.250.1.213.1.4.8) |
| 30-31 | NIR + Clé | PID-3 | Social Security Number (OID 1.2.250.1.213.1.4.10) |

#### HPK MV|M2 → HL7 ADT PV1 Segment

| HPK Field (Position) | HPK Description | HL7 Field | HL7 Description |
|---------------------|-----------------|-----------|-----------------|
| 7 | Numéro de séjour | PV1-19 | Visit Number |
| 8 | Date/heure entrée | PV1-44 | Admit Date/Time |
| 9 | Mode d'entrée | PV1-4 | Admission Type |
| 10 | Établissement | PV1-3.1 | Assigned Patient Location - Facility |
| 11 | Service | PV1-3.2 | Assigned Patient Location - Building |
| 12 | Unité fonctionnelle | PV1-3.3 | Assigned Patient Location - Floor |
| 13 | Lit | PV1-3.4 | Assigned Patient Location - Bed |
| 14 | Médecin responsable | PV1-7 | Attending Doctor |

#### HPK MV|M9 → HL7 ADT PV1 Segment

| HPK Field (Position) | HPK Description | HL7 Field | HL7 Description |
|---------------------|-----------------|-----------|-----------------|
| 8 | Date/heure sortie | PV1-45 | Discharge Date/Time |
| 9 | Mode de sortie | PV1-36 | Discharge Disposition |
| 11 | État à la sortie | PV1-52 | Patient Condition Code |

### Integration Patterns

#### Pattern 1: Hexagone WEB → Service Echange → External System

```
[Hexagone WEB] --HPK--> [Service Echange] --HPK/HL7--> [External System]
                              ↓
                        [HPK Dictionary]
                        [Mapping Rules]
```

**Flow**:
1. Event occurs in Hexagone WEB (admission, transfer, discharge)
2. HPK message generated using dictionary definitions
3. Message stored in Oracle database queue
4. Service Echange/Hexaflux processes message
5. Message transformed to HL7 (if needed) using mapping rules
6. Message sent to external system via configured connector
7. Acknowledgment received and logged

#### Pattern 2: External System → Hexagone WEB (Synchronous)

```
[External System] --Request--> [Hexagone WEB API] --HPK Event--> [Database]
                                       ↓
                                 [HPK Message]
                                       ↓
                              [Service Echange] --HPK--> [Other Systems]
```

**Flow**:
1. External system makes synchronous request to Hexagone WEB
2. Hexagone WEB processes request and updates database
3. Database trigger generates HPK message
4. Message prioritized (high priority for synchronous requests)
5. Service Echange broadcasts message to other systems
6. Response returned to original requester

#### Pattern 3: Message Sequencing

Typical HPK message sequences for common workflows:

**New Patient Admission**:
```
1. ID|M1|C    - Register patient identity
2. CV|M1|C    - Add insurance coverage
3. MV|M2|C    - Admit patient to hospital
4. [Optional] ID|MT|C - Assign treating physician
```

**Patient Transfer**:
```
1. MV|M8|C    - Exit from current unit
2. MV|M6|C    - Transfer to new unit
3. [If needed] MV|M3|C - Status change
```

**Patient Discharge**:
```
1. MV|M9|C    - Discharge from hospital
2. [Optional] ID|M1|M - Update address if changed
3. [Optional] CV|M1|M - Update coverage end date
```

### OID References (French Healthcare)

Important OIDs for HPK to HL7 mapping:

| Identifier Type | OID | Description |
|----------------|-----|-------------|
| INS-C | 1.2.250.1.213.1.4.8 | Identifiant National de Santé Calculé |
| INS-A | 1.2.250.1.213.1.4.9 | Identifiant National de Santé Attesté |
| NIR | 1.2.250.1.213.1.4.10 | Numéro de Sécurité Sociale |
| IPP | 1.2.250.1.213.1.4.2 | Identifiant Permanent du Patient (local) |
| FINESS | 1.2.250.1.71.4.2.2 | Identifiant Établissement |
| RPPS | 1.2.250.1.71.4.2.1 | Répertoire Partagé des Professionnels de Santé |

## Troubleshooting Common Issues

### Issue 1: Field Count Mismatch

**Symptom**: Message has fewer/more fields than expected
```
Expected 38 fields for ID|M1, got 35
```

**Causes**:
- Missing trailing pipes for optional fields
- Extra pipes in text data (address, names)
- Message truncated during transmission

**Solution**:
1. Check HPK dictionary for expected field count
2. Verify all required fields present
3. Check for unescaped pipes in data
4. Add missing trailing pipes for optional fields

### Issue 2: Date Format Errors

**Symptom**: Invalid date format or parsing errors
```
Field 9 (Birth Date): "1975/03/15" - expected YYYYMMDD
```

**Causes**:
- Wrong date format (slashes instead of numeric)
- Invalid date values (e.g., 20260231)
- Missing leading zeros

**Solution**:
1. Verify format is exactly YYYYMMDD (8 digits)
2. For DateTime: YYYYMMDDHHMISSnn (16 digits)
3. Validate date is real (no Feb 31, etc.)
4. Pad with zeros if needed (e.g., "2026315" → "20260315")

### Issue 3: Uppercase Requirement

**Symptom**: Message rejected by receiver
```
Field 3 (Emetteur): "Hexagone" - must be uppercase
```

**Causes**:
- Mixed case in header fields (positions 0-5)
- Case sensitive validation in receiving system

**Solution**:
1. Convert first 6 fields to uppercase
2. Keep patient names in proper case (fields 7-8 in ID|M1)
3. Check specification for case requirements per field

### Issue 4: Empty vs Missing Fields

**Symptom**: Required field appears empty
```
Field 7 (Last Name): "" - required field missing
```

**Causes**:
- Consecutive pipes `||` instead of value
- Space character ` ` interpreted as empty
- Null vs empty string handling

**Solution**:
1. For required fields: must contain non-empty value
2. For optional fields: use `||` (consecutive pipes)
3. Never use spaces to represent empty: `| |` is wrong
4. Trim whitespace from field values

### Issue 5: Character Encoding

**Symptom**: Special characters corrupted
```
"Hôpital" appears as "H?pital"
```

**Causes**:
- UTF-8 vs ISO-8859-1 encoding mismatch
- Accented characters not properly encoded

**Solution**:
1. Verify encoding specification (usually UTF-8 or ISO-8859-1)
2. Ensure consistent encoding throughout pipeline
3. Test with accented characters: é, è, à, ô, ç
4. Consider normalization for comparison (remove accents)

## Practical Usage Examples

### Example 1: Parse Identity Message

**Input**:
```
ID|M1|C|HEXAGONE|20260122120000|USER001|PAT12345|DUPONT|JEAN|19750315|M|15 RUE DE LA PAIX|75001|PARIS|FRA|0612345678||||||||||||||||||||||||||||||||||||||
```

**Expected Output**:
```markdown
### HPK Message Analysis

**Message Type**: ID|M1|C - Patient Identity Creation

**Core Information**:
- System: HEXAGONE
- Timestamp: 22/01/2026 12:00:00
- User: USER001
- Operation: Creation (new patient registration)

**Patient Demographics**:
- IPP: PAT12345
- Name: DUPONT JEAN
- Birth Date: 15/03/1975 (50 years old)
- Gender: Male
- Address: 15 RUE DE LA PAIX, 75001 PARIS, France
- Phone: 06 12 34 56 78

**Business Context**:
This message registers a new patient in the system. The IPP (PAT12345) will be used to identify this patient in all subsequent messages (admissions, transfers, etc.). The message was generated by USER001 on 22/01/2026 at 12:00.

**Validation**: ✓ All required fields present, correct format
```

### Example 2: Parse Admission Message

**Input**:
```
MV|M2|C|HEXAGONE|20260122140000|USER001|PAT12345|VIS20260122001|20260122140000|URGENCE|CHU_PARIS|CARDIO|UF_CARDIO_01|LIT_001|PR_MARTIN|||||||
```

**Expected Output**:
```markdown
### HPK Message Analysis

**Message Type**: MV|M2|C - Patient Admission

**Core Information**:
- System: HEXAGONE
- Timestamp: 22/01/2026 14:00:00
- User: USER001
- Operation: Creation (new admission)

**Patient & Visit**:
- IPP: PAT12345
- Visit Number: VIS20260122001
- Admission Date/Time: 22/01/2026 14:00:00

**Admission Details**:
- Entry Mode: URGENCE (Emergency admission)
- Facility: CHU_PARIS
- Service: CARDIO (Cardiology)
- Functional Unit: UF_CARDIO_01
- Bed: LIT_001
- Attending Physician: PR_MARTIN

**Business Context**:
Patient PAT12345 admitted to CHU Paris Cardiology department via emergency room on 22/01/2026 at 14:00. The visit is assigned number VIS20260122001 which will track all movements during this hospital stay. Patient assigned to bed LIT_001 in functional unit UF_CARDIO_01 under care of Dr. PR_MARTIN.

**HL7 Mapping**: Maps to ADT^A01 (Admit Patient) - IHE PAM [ITI-31]

**Validation**: ✓ All required fields present
```

### Example 3: Parse Message Sequence

**Input (Multiple Messages)**:
```
1. ID|M1|C|HEXAGONE|20260122120000|USER001|PAT12345|DUPONT|JEAN|19750315|M|...
2. CV|M1|C|HEXAGONE|20260122120100|USER001|PAT12345|CPAM75|01|750|...
3. MV|M2|C|HEXAGONE|20260122140000|USER002|PAT12345|VIS001|20260122140000|URGENCE|...
4. MV|M6|C|HEXAGONE|20260123090000|USER003|PAT12345|VIS001|UF_NEURO|...
5. MV|M9|C|HEXAGONE|20260125180000|USER002|PAT12345|VIS001|20260125180000|DOMICILE|...
```

**Expected Output**:
```markdown
### HPK Message Sequence Analysis

**Workflow**: Complete Patient Episode

**Timeline**:

**22/01/2026 12:00** - Patient Registration (ID|M1|C)
- Patient DUPONT JEAN (IPP: PAT12345) registered by USER001

**22/01/2026 12:01** - Insurance Added (CV|M1|C) [+1 min]
- CPAM Paris coverage added by USER001

**22/01/2026 14:00** - Emergency Admission (MV|M2|C) [+2h]
- Admitted via emergency, Visit: VIS001 by USER002

**23/01/2026 09:00** - Transfer (MV|M6|C) [+19h]
- Transferred to Neurology by USER003

**25/01/2026 18:00** - Discharge (MV|M9|C) [+2d 9h]
- Discharged home by USER002

**Summary**:
- Episode duration: 3 days 6 hours
- Visit VIS001 completed
- 3 users involved
- ✓ Logical sequence maintained
- ✓ Chronological order correct

**HL7 Equivalent**: ADT^A28 → ADT^A28 → ADT^A01 → ADT^A02 → ADT^A03
```

## Quick Reference

### Core Message Types

#### Patient Administration (ID, MV, CV)

| HPK Message | Full Name | Purpose | HL7 Equivalent |
|-------------|-----------|---------|----------------|
| ID\|M1\|C/M/D | Patient Identity | Patient demographics and registration | ADT^A28/A31/A29 |
| ID\|MT\|C/M/D | Treating Physician | Assign/update médecin traitant | ADT^A28 |
| ID\|CE\|C/M/D | Informed Consent | Record patient consent | ADT^A28 |
| MV\|M2\|C/M/D | Admission | Hospital admission | ADT^A01 |
| MV\|M3\|C/M/D | Status Change | Administrative status change | ADT^A06 |
| MV\|M6\|C/M/D | Transfer | Unit/service transfer | ADT^A02 |
| MV\|M8\|C/M/D | Unit Exit | Exit from functional unit | ADT^A02 |
| MV\|M9\|C/M/D | Discharge | Hospital discharge | ADT^A03 |
| MV\|B1\|C/M/D | Box Movement | Emergency department box movement | ADT^A02 |
| MV\|MT\|C/M/D | Temporary Movement | Temporary movement (exam, procedure) | ADT^A09/A10 |
| CV\|M1\|C/M/D | Coverage | Insurance and coverage information | IN1/IN2 |

#### User Management (UT)

| HPK Message | Full Name | Purpose |
|-------------|-----------|---------|
| UT\|A1\|C/M/S | User Account | Create/modify/delete user accounts |

#### Organizational Structure (ST)

| HPK Message | Full Name | Purpose |
|-------------|-----------|---------|
| ST\|EJ\|C/M | Legal Establishment | Établissement Juridique (legal entity) |
| ST\|EG\|C/M | Geographic Establishment | Établissement Géographique (physical site) |
| ST\|BA\|C/M/S | Building | Bâtiment (building structure) |
| ST\|ET\|C/M/S | Floor | Étage (floor level) |
| ST\|CH\|C/M/S | Room | Chambre/Pièce (room/space) |

#### Supply Chain - Products & Suppliers (PR, FO)

| HPK Message | Full Name | Purpose |
|-------------|-----------|---------|
| PR\|M0\|C/M/S | Product - General Data | General product information |
| PR\|M1\|C/M/S | Product - Pharmacy Info | Pharmacy-specific product data |
| PR\|M2\|C/M/S | Product - Therapeutic Book | Therapeutic formulary information |
| PR\|M3\|C/M/S | Product - Accounting Info | Accounting and financial data |
| PR\|M4\|C/M/S | Product - Economic Info | Economic management information |
| PR\|M5\|C/M/S | Product - Store Info | Store/warehouse information |
| FO\|M1\|C/M/S | Supplier - General Info | General supplier information |
| FO\|M2\|C/M/S | Supplier - Bank Details | Bank domiciliation details |
| FO\|M3\|C/M/S | Supplier - Order Points | Order contact points |

#### Supply Chain - Orders & Deliveries (MA, CO, LI, RO)

| HPK Message | Full Name | Purpose |
|-------------|-----------|---------|
| MA\|M1\|C/M/S | Market - Header | Contract/market header |
| MA\|M2\|C/M/S | Market - Lines | Contract/market line items |
| MA\|M3\|C/M/S | Market - Suppliers | Suppliers by market |
| CO\|M1\|C/M/S | Order - Header | Purchase order header |
| CO\|M2\|C/M/S | Order - Lines | Purchase order line items |
| LI\|M1\|C/M | Delivery - Lines | External delivery lines |
| LI\|M2\|C/M | Delivery - Lot Lines | Delivery lines with lot management |
| RO\|M1\|C/M/S | Reception - Lines | Reception lines |
| RO\|M2\|C/M | Reception - Lot Lines | Reception lines with lot management |

#### Financial (FA, RD)

| HPK Message | Full Name | Purpose |
|-------------|-----------|---------|
| FA\|FE\|C | Invoice - Header | Facture Entête (invoice header) |
| FA\|FL\|C | Invoice - Lines | Facture Lignes (invoice line items) |
| RD\|E1\|C | Misc Receipt - Header | Recettes diverses header |
| RD\|L1\|C | Misc Receipt - Lines | Recettes diverses line items |

#### Inventory & Stock (SO, IM)

| HPK Message | Full Name | Purpose |
|-------------|-----------|---------|
| SO\|S1\|C | Stock Output | Sortie (stock withdrawal) |
| SO\|I1\|C | Inventory | Inventaire (stock count) |
| SO\|T1\|C | Stock Transfer | Transfert (internal transfer) |
| SO\|L1\|C | Pre-established Lists | Listes pré établies |
| IM\|M1\|C | Asset Inventory | Inventaire mobilier (asset tracking) |

#### Requests (DD)

| HPK Message | Full Name | Purpose |
|-------------|-----------|---------|
| DD\|M1\|C | Identity Request | Demande de création identité |
| DD\|K1\|C | Act Request | Demande de création acte |

### Operation Modes

| Mode | French | English | Description |
|------|--------|---------|-------------|
| **C** | Création | Creation | Create new record |
| **M** | Modification | Modification | Update existing record |
| **S** | Suppression | Deletion | Delete/remove record |
| **D** | Deletion | Deletion | Delete (alternate notation) |

### Common Field Patterns

**Standard Header** (all messages):
```
Type|Message|Mode|Emetteur|Date|User|...
```

**Date Formats**:
- Short date: `YYYYMMDD` (e.g., `20260122`)
- Full timestamp: `YYYYMMDDHHMISSnn` (e.g., `20260122140530`)
- nn = centiseconds (1/100 second)

**Gender Codes**:
- `M` = Male (Masculin)
- `F` = Female (Féminin)
- `U` = Unknown (Inconnu)

**French Administrative Terms**:
- IPP = Identifiant Permanent du Patient (Patient Permanent ID)
- INS = Identifiant National de Santé (National Health ID)
- NIR = Numéro d'Inscription au Répertoire (Social Security Number)
- UF = Unité Fonctionnelle (Functional Unit)
- FINESS = Fichier National des Établissements Sanitaires et Sociaux
- CPAM = Caisse Primaire d'Assurance Maladie (Health Insurance Fund)
- ALD = Affection Longue Durée (Long-term Condition)
- CMU = Couverture Maladie Universelle (Universal Health Coverage)
