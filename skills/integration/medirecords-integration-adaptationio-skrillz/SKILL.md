---
name: medirecords-integration
description: Complete MediRecords FHIR/REST API integration guide for Dr. Sophia AI consultations. Covers two-phase workflow (FHIR Encounter creation + REST notes append), patient search, SOAP note formatting, and troubleshooting. Use when integrating MediRecords API, creating consultations, debugging FHIR/REST endpoints, or saving AI consultations to patient records.
---

# MediRecords Integration Guide

## Overview

Access the complete guide for integrating Dr. Sophia AI consultations with MediRecords EHR system using FHIR v1 and REST v1 APIs. This skill provides the two-phase workflow, API credentials, FHIR schemas, troubleshooting guide, and test scripts.

**Keywords**: MediRecords, FHIR API, REST API, consultation creation, SOAP notes, encounter, EHR integration, patient records, clinical documentation

**Status**: ✅ Fully tested and working (verified Oct 22, 2025)

## When to Use This Skill

- Creating consultations in MediRecords
- Integrating AI consultation workflow
- Debugging FHIR/REST API issues
- Saving SOAP notes to patient records
- Understanding two-phase consultation process
- Troubleshooting HTTP 409/500/400 errors

## The Two-Phase Process

MediRecords requires **TWO separate API calls** to create a complete consultation:

### Phase 1: FHIR API - Create Encounter
- **Endpoint**: `POST https://api.medirecords.com/fhir/v1/Encounter`
- **Token**: FHIR token (see [references/api-credentials.md](references/api-credentials.md))
- **Purpose**: Create consultation structure
- **Result**: Encounter ID for Phase 2

### Phase 2: REST API - Append Notes
- **Endpoint**: `POST https://api.medirecords.com/v1/patients/{id}/consults/{encounterId}/consultnote/append`
- **Token**: REST token (different from FHIR!)
- **Purpose**: Add clinical documentation (SOAP notes)
- **Result**: Consultation visible in MediRecords UI

## Critical Requirements

✅ **Must create encounter with `status: "finished"`** (not "in-progress")
✅ **Must include `serviceProvider` field** (practice ID)
✅ **Must append notes within 1 hour** of encounter `endTime`
✅ **Use FHIR token for Phase 1, REST token for Phase 2** (different tokens!)

## Quick Start Workflow

### Step 1: Search for Patient
```javascript
const searchResponse = await fetch(
  'https://api.medirecords.com/fhir/v1/Patient?email=patient@example.com',
  {
    headers: {
      'Authorization': `Bearer ${FHIR_TOKEN}`,
      'Content-Type': 'application/fhir+json'
    }
  }
);
const patientData = await searchResponse.json();
const patientId = patientData.entry[0].resource.id;
```

### Step 2: Create Finished Encounter (Phase 1)
```javascript
const encounterResponse = await fetch(
  'https://api.medirecords.com/fhir/v1/Encounter',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${FHIR_TOKEN}`,
      'Content-Type': 'application/fhir+json'
    },
    body: JSON.stringify({
      resourceType: 'Encounter',
      status: 'finished',  // ✅ MUST be "finished"
      class: {
        system: 'http://terminology.hl7.org/CodeSystem/v3-ActCode',
        code: 'AMB',
        display: 'ambulatory'
      },
      subject: { reference: `Patient/${patientId}` },
      participant: [{
        individual: { reference: `Practitioner/${DR_SOPHIA_ID}` }
      }],
      serviceProvider: {  // ✅ REQUIRED!
        reference: `Organization/${PRACTICE_ID}`
      },
      period: {
        start: new Date(Date.now() - 30*60000).toISOString(),
        end: new Date().toISOString()
      }
    })
  }
);
const encounter = await encounterResponse.json();
const encounterId = encounter.id;
```

### Step 3: Append SOAP Notes (Phase 2)
```javascript
const soapNotes = `
<div id="stamp">
  <div><strong>${new Date().toLocaleString('en-AU')}</strong></div>
  <div><strong>Dr. Sophia AI - Consultation Notes</strong></div>
</div>
<p><strong>Chief Complaint:</strong> Headaches for 3 months</p>
<p><strong>Subjective:</strong> Patient reports...</p>
<p><strong>Objective:</strong> BP 145/92...</p>
<p><strong>Assessment:</strong> Uncontrolled hypertension</p>
<p><strong>Plan:</strong> Adjust medication...</p>
`;

const noteResponse = await fetch(
  `https://api.medirecords.com/v1/patients/${patientId}/consults/${encounterId}/consultnote/append`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${REST_TOKEN}`,  // ✅ Different token!
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ consultNote: soapNotes })
  }
);
```

## What Works vs What Doesn't

| Feature | Status | Details |
|---------|--------|---------|
| Create finished consultation | ✅ Works | Use FHIR API with `status: "finished"` |
| Append notes (unlimited) | ✅ Works | Use REST API within 1 hour |
| HTML formatting in notes | ✅ Works | Supports p, strong, div, ul, li, br, table |
| Multiple appends | ✅ Works | Can append multiple times within 1 hour |
| Create "in-progress" consult | ❌ Blocked | API returns HTTP 409 error |
| Update consult status | ❌ No endpoint | Cannot change status after creation |
| Update/replace notes | ❌ No endpoint | Can only append, not edit |

## Detailed Documentation

For complete API credentials, FHIR schemas, and troubleshooting guide, see:

- **API Credentials**: [references/api-credentials.md](references/api-credentials.md)
- **FHIR Schemas**: [references/fhir-schemas.md](references/fhir-schemas.md)
- **Troubleshooting**: [references/troubleshooting-guide.md](references/troubleshooting-guide.md)

## Testing

Run integration test script:
```bash
cd .claude/skills/medirecords-integration
./scripts/test-consultation.sh willie@adaptation.io
```

Expected output:
```
✅ Encounter created: [encounter-id]
✅ Notes appended: [note-id]
✅ Consultation visible in MediRecords UI
```

## Integration with Dr. Sophia AI

Add to backend consultation handler (`/backend/backend-proxy-enhanced-current.js`):

```javascript
// After consultation completes and SOAP notes extracted
if (req.body.patientIdentifier && shouldSaveToMedirecords(aiResponse)) {
  try {
    const consultationData = {
      chiefComplaint: extractedData.chiefComplaint,
      subjective: extractedData.subjective,
      objective: extractedData.objective,
      assessment: extractedData.assessment,
      plan: extractedData.plan,
      prescriptions: extractedData.prescriptions
    };

    const result = await createDrSophiaConsultationWithNotes(
      req.body.patientIdentifier,
      consultationData
    );

    console.log(`✅ Consultation saved: ${result.encounterId}`);
  } catch (error) {
    console.error('❌ Failed to save consultation:', error);
    // Don't fail the response - consultation still worked
  }
}
```

## Common Issues Quick Reference

| Error | Cause | Fix |
|-------|-------|-----|
| HTTP 409 | Status "in-progress" | Change to "finished" |
| HTTP 500 | Missing serviceProvider | Add practice Organization reference |
| HTTP 400 (notes) | >1 hour since endTime | Use recent timestamps |
| Notes don't appear | Wrong token for append | Use REST token (not FHIR) |
| HTML not rendering | Unsupported tags | Use only: p, strong, div, ul, li, br, table |

## Verified Test Results

**Patient**: Willie Prosek (willie@adaptation.io)
**Last Verified**: October 22, 2025 at 8:17 PM
**Encounters Created**: 3+ consultations
**Notes Appended**: Multiple times per consultation
**UI Verification**: ✅ All consultations visible in MediRecords
**HTML Formatting**: ✅ Preserved correctly
**Character Limit**: ✅ Tested up to 1,975 characters

---

**Status**: Production-ready, fully tested
**API Version**: FHIR v1 + REST v1
**Test Patient**: willie@adaptation.io
**Last Updated**: October 22, 2025
