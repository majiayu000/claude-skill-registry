---
name: openfda-animal
description: Query the openFDA Animal and Veterinary endpoints for adverse event reports, approved animal drug products, and veterinary device data. REST API access to FDA CVM public datasets.
---

# OpenFDA Animal & Veterinary

## Overview

openFDA provides free, public REST API access to FDA CVM (Center for Veterinary Medicine) databases of animal drug adverse events, approved animal products, and veterinary device data. This skill covers API endpoints, query syntax, searchable fields, rate limits, and SDK integration for veterinary AI applications.

## When to Use

- User queries adverse event frequency for a veterinary drug
- User searches for FDA-approved animal drug products (NADA database)
- User researches safety signals or patterns in veterinary pharmacovigilance
- User programmatically integrates FDA data into a VetClaw application
- Keywords: openFDA, FDA CVM, adverse event, animal drug, NADA, API, veterinary device, safety signal

## API Endpoints

**Animal & Veterinary Events (Adverse Event Reports):**
```
https://api.fda.gov/animalandveterinary/event.json
```
Searchable fields: animal species, drug name, adverse reaction, outcome, date reported

**Approved Animal Drug Products (NADA Database):**
```
https://api.fda.gov/animalandveterinary/approved_animal_drug_applications.json
```
Searchable fields: trade name, generic name, applicant, approval date, species

**Veterinary Device Events:**
```
https://api.fda.gov/animalandveterinary/device_event.json
```
Searchable fields: device type, malfunction, injury, manufacturer

## Query Syntax

**Basic GET Request:**
```
https://api.fda.gov/animalandveterinary/event.json?search=FIELD:VALUE&limit=10&skip=0
```

**Common Parameters:**
- `search`: Query expression (field-value pairs connected with AND/OR)
- `limit`: Results per page (1-1000, default 20)
- `skip`: Offset for pagination (for results >1000)
- `count`: Aggregate count by field instead of returning individual records
- `sort`: Order results (field name)

**Boolean Operators:**
- `AND`: Both conditions must match
- `OR`: Either condition matches
- `NOT`: Exclude results matching condition
- Parentheses for complex expressions: `(field1:value1 OR field1:value2) AND field2:value3`

**Field Query Examples:**
```
drug.name:"amoxicillin" AND animal.species:"canine"
reaction.veddra_term_name:"hepatotoxicity"
date_received:[20200101 TO 20241231]
outcome:"Fatal"
```

## Searchable Fields - Adverse Events

**Drug Fields:**
- `drug.name` - Generic or brand name
- `drug.dose_value` - Numerical dose
- `drug.dose_unit` - Unit (mg, mL, etc.)
- `drug.route` - Route of administration (PO, IV, IM, topical, etc.)
- `drug.frequency` - Dosing frequency

**Animal Fields:**
- `animal.species` - Species affected (canine, feline, equine, bovine, avian, etc.)
- `animal.breed` - Breed (searchable for canine predisposition studies)
- `animal.age_value` - Numerical age
- `animal.age_unit` - Unit (year, month, week, day)
- `animal.sex` - Male, female, unknown
- `animal.weight_value` - Weight (for dose-response analysis)

**Reaction Fields:**
- `reaction.veddra_term_name` - VEDDRA (Veterinary Dictionary for Drug Event Reports and Analysis) standardized term
- `reaction.outcome` - Death, Euthanasia, Serious, Non-serious, Recovered, Recovering, Unknown
- `reaction.severity` - Severity classification

**Report Fields:**
- `date_received` - Date FDA received report (ISO 8601 format: YYYYMMDD)
- `report_id` - Unique FDA adverse event ID
- `serious` - Boolean (whether report indicates serious adverse outcome)

## Common Veterinary VEDDRA Terms

| Term | Category | Examples |
|------|----------|----------|
| Hepatotoxicity | Organ toxicity | Elevated ALT, liver damage |
| Nephrotoxicity | Organ toxicity | Elevated creatinine, kidney failure |
| Cardiotoxicity | Organ toxicity | Arrhythmias, myocarditis |
| Gastrointestinal | System | Vomiting, diarrhea, hemorrhage |
| Dermatitis | Skin | Rash, hives, edema |
| Anaphylaxis | Immune | Shock, acute hypersensitivity |
| Thrombocytopenia | Hematologic | Low platelet count, bleeding |
| Seizure | Neurologic | Convulsions, ataxia |
| Death | Fatal | Lethal outcome |

## Rate Limits

- **Without API key:** 240 requests per minute, 1,000 requests per day
- **With API key (free):** 240 requests per minute, 120,000 requests per day
- **Rate Limit Headers:** Response includes `X-Rate-Limit-Limit`, `X-Rate-Limit-Remaining`
- **Exceeding Limits:** Server returns HTTP 429 (Too Many Requests); implement exponential backoff retry

**Register for API Key:**
https://open.fda.gov/apis/authentication/

## VetClaw SDK Integration

VetClaw includes reference clients for this API. See `sdk/` in the repo root.

**Python** (`sdk/python/openfda_vet.py`):
```python
from openfda_vet import OpenFDAVet

client = OpenFDAVet(api_key="YOUR_KEY")

# Search adverse events by species and drug
events = client.search(species="Dog", drug="Amoxicillin", limit=100)

# Count adverse events by reaction for a specific drug
reactions = client.top_reactions("Cat", drug="Methimazole")

# Count adverse events by outcome
outcomes = client.count("reaction.outcome", species="Dog", drug="Ivermectin")
```

**TypeScript** (`sdk/typescript/openfda-vet.ts`):
```typescript
import { OpenFDAVet } from "./openfda-vet";

const client = new OpenFDAVet("YOUR_KEY");

// Search adverse events
const events = await client.search({ species: "Dog", drug: "Amoxicillin", limit: 100 });

// Count top reactions
const reactions = await client.topReactions("Cat", "Methimazole");

// Paginate through results
for await (const page of client.paginate({ species: "Dog", drug: "Ivermectin" })) {
  for (const event of page) console.log(event.safetyreportid);
}
```

## Practical Query Examples

**Query 1: MDR1 Sensitivity to Ivermectin**
```
Search for ivermectin adverse events in herding breeds (known MDR1 mutation risk):
drug.name:"ivermectin"
  AND animal.breed:("Collie" OR "Australian Shepherd" OR "Sheltie")
  AND reaction.outcome:("Death" OR "Serious" OR "Euthanasia")
Limit: 100
```

**Query 2: Acetaminophen in Cats (Lethal Combination)**
```
drug.name:"acetaminophen" AND animal.species:"feline"
Expected outcome: High rate of hepatotoxicity, death (acetaminophen is lethal to cats)
```

**Query 3: Drug Withdrawal Time Safety**
```
Drug: penicillin, Animal: bovine, Outcome: Recovery with residue concerns
Verify no unusual severe outcomes reported; extract timeline to recovery
```

**Query 4: Breed Predisposition to Drug Reaction**
```
reaction.veddra_term_name:"seizure"
  AND (drug.name:"phenobarbital" OR drug.name:"levetiracetam")
  AND animal.species:"canine"
Group by breed to identify predispositions
```

**Query 5: Time-Based Safety Trend**
```
drug.name:"enalapril"
  AND animal.species:"feline"
  AND date_received:[20150101 TO 20241231]
Count by year to track safety signal emergence over time
```

## Response Structure

**Adverse Event Record Example:**
```json
{
  "report_id": "123456789",
  "date_received": "2024-03-15",
  "animal": {
    "species": "canine",
    "breed": "Labrador Retriever",
    "age_value": 5,
    "age_unit": "year",
    "sex": "female",
    "weight_value": 30,
    "weight_unit": "kg"
  },
  "drug": {
    "name": "amoxicillin",
    "dose_value": 250,
    "dose_unit": "mg",
    "route": "oral",
    "frequency": "twice daily"
  },
  "reaction": {
    "veddra_term_name": "vomiting",
    "outcome": "Recovered",
    "severity": "moderate"
  },
  "serious": false
}
```

## Use Cases in Veterinary AI

1. **Safety Signal Detection:** Aggregate adverse events by drug-species-breed to identify unexpected patterns (e.g., increased hepatotoxicity in specific breed using drug X)

2. **Pharmacovigilance Monitoring:** Track trends in serious adverse events over time; alert veterinarians to emerging safety signals

3. **Breed-Specific Dosing Refinement:** Identify adverse event clusters by breed; inform precision medicine protocols

4. **Drug Interaction Warnings:** Cross-reference adverse events to identify potential drug-drug interactions not captured in single-drug studies

5. **Clinical Decision Support:** When recommending a drug, query recent adverse events to provide evidence-based safety profile to veterinarian

## Limitations

- **Reporting Bias:** Adverse events are voluntarily reported; underreporting of minor side effects, overreporting of serious outcomes
- **Incomplete Data:** Many adverse event reports lack complete signalment (breed, age), dosing information, or outcome details
- **Temporal Lag:** FDA data is typically 6-12 months behind current clinical use; emerging signals may not be captured
- **Causality Uncertainty:** Reported adverse event may not be causally related to drug (confounding variables, concurrent medications)
- **Approved Drug Products Database:** Limited to FDA-approved products; extralabel use (common in veterinary medicine) not captured
- **This skill is reference only:** Data interpretation requires clinical expertise; not a substitute for veterinary consultation

## Sources

- **OpenFDA Documentation:** https://open.fda.gov/apis/
- **OpenFDA Animal & Veterinary Guide:** https://open.fda.gov/apis/animalandveterinary/
- **FDA CVM:** https://www.fda.gov/animal-veterinary
- **VEDDRA Terminology:** Available in FDA CVM databases
- **VetClaw SDK Documentation:** Reference sdk/ folder for Python/TypeScript client libraries

## Rate Limit Best Practices

- Implement exponential backoff (wait 2^attempt seconds if rate limited)
- Cache results locally to minimize API calls
- Use `count` endpoint instead of fetching all records if only aggregate data needed
- Batch queries by date range to reduce total requests
- Monitor `X-Rate-Limit-Remaining` header; pause if approaching limit
