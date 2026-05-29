---
name: health-record-assistant
description: |
  Connect to and analyze a user's health records from their patient portal via SMART on FHIR.
  Use when the user wants to review medical records, understand lab results, see medications,
  analyze health trends, identify care gaps, or answer questions about personal health data.
---

# Health Record Assistant

Fetch and analyze electronic health records from patient portals using SMART on FHIR.

## When to Use

- User asks about their health records, medical history, or test results
- User wants to understand medications, conditions, or treatments
- User asks about lab trends or health metrics over time
- User wants to identify care gaps or preventive care needs
- User wants summaries of visits or clinical notes

## Analysis Philosophy

**Unless the user specifically asks for a live app or artifact**, you should:

1. **Download data into your computational environment** and analyze it manually
2. **Inspect structured data** by writing and running code to process FHIR resources
3. **Read clinical notes in full** where relevant - grep through attachments, identify important notes, read them completely
4. **Use your judgment** to evaluate what's clinically significant, iterate on your analysis, and refine your understanding
5. **Synthesize thoughtful answers** based on your exploration of the data

This approach is important because:
- You can see intermediate results, catch errors, and improve your analysis
- You can apply clinical reasoning as you explore, not just execute blind code
- You can identify which notes are worth reading fully vs. skimming
- Complex health questions often require iterative investigation

**If the user wants a live artifact/app**, pre-processing is still valuable:
- Do your exploratory analysis first
- Identify the key data points and insights
- Then build the artifact with pre-processed results or focused queries
- This avoids shipping analysis code you can't see or debug

## How to Connect

Helper scripts are provided in `scripts/` to simplify the workflow.

**Prerequisites:** These scripts require [Bun](https://bun.sh) to be installed:
```bash
curl -fsSL https://bun.sh/install | bash
```

### Step 1: Create a Session

```bash
bun scripts/create-session.ts
```

Output:
```json
{
  "sessionId": "abc123...",
  "userUrl": "https://health-skillz.exe.xyz/connect/abc123...",
  "pollUrl": "https://health-skillz.exe.xyz/api/poll/abc123...",
  "privateKeyJwk": { "kty": "EC", "crv": "P-256", "d": "...", ... }
}
```

**Save the `privateKeyJwk`** - you'll need it to decrypt the data.

### Step 2: Show the User a Link

Present `userUrl` to the user as a clickable link:

> **To access your health records, please click this link:**
>
> [Connect Your Health Records]({userUrl})
>
> You'll sign into your patient portal (like Epic MyChart), and your records will be securely transferred for analysis.
> 
> 🔒 Your data is end-to-end encrypted - only this conversation can decrypt it.

### Step 3: Finalize and Decrypt

Once the user has connected their provider(s) and clicked "Done - Send to AI":

```bash
bun scripts/finalize-session.ts <sessionId> '<privateKeyJwk>' ./health-data
```

This script:
1. Polls until data is ready (outputs JSON status lines while waiting)
2. Decrypts each provider's data
3. Writes one JSON file per provider:

Example output:
```
{"status":"polling","sessionId":"abc123..."}
{"status":"waiting","sessionStatus":"collecting","providerCount":1,"attempt":1}
{"status":"ready","providerCount":1}
{"status":"decrypting"}
{"status":"wrote_file","file":"./health-data/unitypoint-health.json","provider":"UnityPoint Health","resources":277,"attachments":82}
{"status":"done","files":["./health-data/unitypoint-health.json"]}
```

Result:

```
health-data/
  unitypoint-health.json
  mayo-clinic.json
```

Each file contains a single provider's data:

```typescript
interface ProviderData {
  name: string;
  fhirBaseUrl: string;
  connectedAt: string;
  fhir: {
    Patient?: Patient[];
    Condition?: Condition[];
    Observation?: Observation[];
    MedicationRequest?: MedicationRequest[];
    Procedure?: Procedure[];
    Immunization?: Immunization[];
    AllergyIntolerance?: AllergyIntolerance[];
    Encounter?: Encounter[];
    DiagnosticReport?: DiagnosticReport[];
    DocumentReference?: DocumentReference[];
    CareTeam?: CareTeam[];
    Goal?: Goal[];
  };
  attachments: Attachment[];
}

interface Attachment {
  resourceType: string;      // "DocumentReference" or "DiagnosticReport"
  resourceId: string;        // FHIR resource ID this attachment came from
  contentType: string;       // MIME type: "text/html", "text/rtf", "application/xml", etc.
  contentPlaintext: string | null;  // Extracted plain text (for text formats)
  contentBase64: string | null;     // Raw content, base64 encoded
}
```

Each provider is a separate slice - no merging, preserves data provenance.

## Working with FHIR Data

### Available Resource Types

```javascript
data.fhir.Patient           // Demographics (name, DOB, contact)
data.fhir.Condition         // Diagnoses and health problems
data.fhir.MedicationRequest // Prescribed medications
data.fhir.Observation       // Lab results, vital signs
data.fhir.Procedure         // Surgeries and procedures
data.fhir.Immunization      // Vaccination records
data.fhir.AllergyIntolerance// Allergies and reactions
data.fhir.Encounter         // Healthcare visits
data.fhir.DocumentReference // Clinical documents
data.fhir.DiagnosticReport  // Lab panels, imaging reports
```

### Example: Get Lab Results by LOINC Code

```javascript
function getLabsByLoinc(loincCode) {
  return data.fhir.Observation?.filter(obs =>
    obs.code?.coding?.some(c => c.code === loincCode)
  ).map(obs => ({
    value: obs.valueQuantity?.value,
    unit: obs.valueQuantity?.unit,
    date: obs.effectiveDateTime,
    flag: obs.interpretation?.[0]?.coding?.[0]?.code // H, L, N
  })).sort((a, b) => new Date(b.date) - new Date(a.date));
}

// Common LOINC codes:
// 4548-4  = Hemoglobin A1c
// 2345-7  = Glucose
// 2093-3  = Total Cholesterol
// 2085-9  = HDL Cholesterol
// 13457-7 = LDL Cholesterol
// 2160-0  = Creatinine
// 8480-6  = Systolic Blood Pressure
// 8462-4  = Diastolic Blood Pressure
// 718-7   = Hemoglobin
// 39156-5 = BMI
```

### Example: List Active Medications

```javascript
const activeMeds = data.fhir.MedicationRequest
  ?.filter(m => m.status === 'active')
  .map(m => ({
    name: m.medicationCodeableConcept?.coding?.[0]?.display,
    dosage: m.dosageInstruction?.[0]?.text,
    prescribedDate: m.authoredOn
  }));
```

### Example: Get Active Conditions

```javascript
const conditions = data.fhir.Condition
  ?.filter(c => c.clinicalStatus?.coding?.[0]?.code === 'active')
  .map(c => ({
    name: c.code?.coding?.[0]?.display,
    onsetDate: c.onsetDateTime
  }));
```

### Understanding Attachments

The `attachments` array contains clinical documents extracted from `DocumentReference` and `DiagnosticReport` resources. Each attachment has:

- **`contentPlaintext`**: Extracted readable text (for HTML, RTF, XML, plain text formats)
- **`contentBase64`**: Raw file content, base64 encoded (always present)
- **`contentType`**: MIME type like `text/html`, `text/rtf`, `application/xml`

Common patterns from Epic:
- Most DocumentReferences have 2 attachments: one `text/html` and one `text/rtf` (same content, different formats)
- RTF files contain Epic-specific markup that gets stripped during plaintext extraction
- All attachments are fetched (no artificial limits)

For analysis, use `contentPlaintext` - it's clean and searchable. The `contentBase64` is available if you need the original format.

### Example: Search Clinical Notes

The `attachments` array contains extracted text from clinical documents:

```javascript
function searchNotes(searchTerm) {
  return data.attachments?.filter(att =>
    att.contentPlaintext?.toLowerCase().includes(searchTerm.toLowerCase())
  ).map(att => {
    const text = att.contentPlaintext || '';
    const idx = text.toLowerCase().indexOf(searchTerm.toLowerCase());
    const start = Math.max(0, idx - 150);
    const end = Math.min(text.length, idx + searchTerm.length + 150);
    return {
      context: text.substring(start, end),
      docType: att.resourceType
    };
  });
}

// Example: Find mentions of diabetes
const diabetesNotes = searchNotes('diabetes');
```

### Example: Check for Care Gaps

```javascript
function checkCareGaps(patientAge) {
  const gaps = [];
  const now = new Date();
  
  // Colonoscopy (age 45+, every 10 years)
  if (patientAge >= 45) {
    const colonoscopy = data.fhir.Procedure?.find(p =>
      p.code?.coding?.[0]?.display?.toLowerCase().includes('colonoscopy')
    );
    const lastDate = colonoscopy ? new Date(colonoscopy.performedDateTime) : null;
    const yearsSince = lastDate ? (now - lastDate) / (365 * 24 * 60 * 60 * 1000) : Infinity;
    if (yearsSince > 10) {
      gaps.push('Colonoscopy may be due (last: ' + (lastDate?.toLocaleDateString() || 'never') + ')');
    }
  }
  
  // Annual flu shot
  const fluShot = data.fhir.Immunization?.find(i =>
    i.vaccineCode?.coding?.[0]?.display?.toLowerCase().includes('influenza') &&
    new Date(i.occurrenceDateTime).getFullYear() === now.getFullYear()
  );
  if (!fluShot) {
    gaps.push('Annual flu shot may be due');
  }
  
  return gaps;
}
```

### Example: Analyze Lab Trends

```javascript
function analyzeTrend(loincCode, testName) {
  const values = getLabsByLoinc(loincCode);
  if (values.length < 2) return `${testName}: Insufficient data for trend`;
  
  const recent = values[0];
  const previous = values[1];
  const change = ((recent.value - previous.value) / previous.value * 100).toFixed(1);
  
  let trend = 'stable';
  if (change > 5) trend = `increased ${change}%`;
  if (change < -5) trend = `decreased ${Math.abs(change)}%`;
  
  return `${testName}: ${recent.value} ${recent.unit} (${trend} from ${previous.value})`;
}

// Example
analyzeTrend('4548-4', 'A1c');
```

## Combining Structured + Unstructured Data

The power is combining FHIR resources with clinical note text:

```javascript
// 1. Check if patient has diabetes diagnosis
const hasDiabetes = data.fhir.Condition?.some(c =>
  c.code?.coding?.[0]?.display?.toLowerCase().includes('diabetes')
);

// 2. Get A1c trend
const a1cValues = getLabsByLoinc('4548-4');

// 3. Find related medications
const diabetesMeds = data.fhir.MedicationRequest?.filter(m =>
  ['metformin', 'insulin', 'glipizide', 'januvia'].some(drug =>
    m.medicationCodeableConcept?.coding?.[0]?.display?.toLowerCase().includes(drug)
  )
);

// 4. Search notes for management discussions
const managementNotes = searchNotes('diabetes');

// Now provide comprehensive diabetes analysis
```

## Important Guidelines

1. **Be empathetic** - Health data is personal. Be supportive and clear.
2. **Not medical advice** - Always remind users to discuss findings with their healthcare provider.
3. **Use plain language** - Translate medical jargon into understandable terms.
4. **Respect privacy** - Data is temporary and session-based.

## Testing

For testing with Epic's sandbox:
- Username: `fhircamila`
- Password: `epicepic1`


