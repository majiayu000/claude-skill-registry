---
name: Contract Drafter
slug: contract-drafter
description: Generate legal contracts from templates with variable substitution and clause management
category: document-creation
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create contract"
  - "draft agreement"
  - "generate contract"
  - "make NDA"
  - "service agreement"
tags:
  - contracts
  - legal
  - agreements
  - templates
  - nda
---

# Contract Drafter

The Contract Drafter skill automates the generation of legal contracts and agreements from templates. It handles variable substitution, conditional clauses, signature blocks, and document formatting. This skill is essential for creating NDAs, service agreements, employment contracts, and other legal documents consistently and efficiently.

**IMPORTANT DISCLAIMER:** This skill generates documents from templates and does NOT provide legal advice. All generated contracts should be reviewed by a qualified attorney before use. The skill is designed to streamline document creation, not replace legal counsel.

## Core Workflows

### Workflow 1: Generate from Standard Template
**Purpose:** Create a contract from a pre-defined template with variable substitution

**Steps:**
1. Select contract type (NDA, Service Agreement, etc.)
2. Load template with placeholders
3. Collect required information (parties, dates, terms)
4. Validate all required fields are present
5. Substitute variables in template
6. Handle conditional clauses based on parameters
7. Generate final document (PDF or DOCX)
8. Add signature blocks and execution details

**Implementation:**
```javascript
const Docxtemplater = require('docxtemplater');
const PizZip = require('pizzip');
const fs = require('fs');

function generateContract(templatePath, contractData, outputPath) {
  // Load template
  const content = fs.readFileSync(templatePath, 'binary');
  const zip = new PizZip(content);

  const doc = new Docxtemplater(zip, {
    paragraphLoop: true,
    linebreaks: true
  });

  // Prepare data with defaults and calculations
  const data = {
    // Party information
    party1Name: contractData.party1.name,
    party1Address: contractData.party1.address,
    party1Email: contractData.party1.email,
    party2Name: contractData.party2.name,
    party2Address: contractData.party2.address,
    party2Email: contractData.party2.email,

    // Contract details
    effectiveDate: contractData.effectiveDate,
    expirationDate: contractData.expirationDate,
    term: contractData.term || 'one (1) year',

    // Financial terms (if applicable)
    paymentAmount: contractData.paymentAmount,
    paymentSchedule: contractData.paymentSchedule,
    currency: contractData.currency || 'USD',

    // Specific terms
    scope: contractData.scope,
    deliverables: contractData.deliverables,

    // Conditional clauses
    includeNonCompete: contractData.includeNonCompete || false,
    nonCompetePeriod: contractData.nonCompetePeriod || '12 months',
    nonCompeteRadius: contractData.nonCompeteRadius || '50 miles',

    includeConfidentiality: contractData.includeConfidentiality !== false,
    confidentialityPeriod: contractData.confidentialityPeriod || '5 years',

    // Governing law
    governingState: contractData.governingState || 'Delaware',
    governingCountry: contractData.governingCountry || 'United States',

    // Dates
    currentDate: new Date().toLocaleDateString(),
    currentYear: new Date().getFullYear()
  };

  // Render template
  doc.setData(data);
  doc.render();

  // Save output
  const buf = doc.getZip().generate({
    type: 'nodebuffer',
    compression: 'DEFLATE'
  });

  fs.writeFileSync(outputPath, buf);

  return {
    outputPath,
    contractType: contractData.contractType,
    parties: [data.party1Name, data.party2Name],
    effectiveDate: data.effectiveDate
  };
}
```

### Workflow 2: NDA Generator
**Purpose:** Create Non-Disclosure Agreements with standard or custom terms

**Steps:**
1. Identify NDA type (mutual or one-way)
2. Collect party information
3. Define confidential information scope
4. Set disclosure term and duration
5. Specify exclusions from confidentiality
6. Add remedies and jurisdiction clauses
7. Generate signature pages
8. Create final NDA document

**Implementation:**
```javascript
function generateNDA(ndaData, outputPath) {
  const templatePath = ndaData.type === 'mutual'
    ? './templates/mutual-nda.docx'
    : './templates/one-way-nda.docx';

  const contractData = {
    contractType: 'Non-Disclosure Agreement',

    // Parties
    party1: ndaData.disclosingParty,
    party2: ndaData.receivingParty,

    // NDA-specific terms
    effectiveDate: ndaData.effectiveDate || new Date().toISOString().split('T')[0],
    confidentialityPeriod: ndaData.confidentialityPeriod || '3 years',

    // Purpose of disclosure
    purpose: ndaData.purpose || 'evaluation of a potential business relationship',

    // Scope definition
    confidentialDefinition: ndaData.confidentialDefinition || `any non-public information disclosed by the Disclosing Party to the Receiving Party, whether orally, in writing, or in any other form`,

    // Exclusions
    exclusions: [
      'Information that is publicly available through no breach of this Agreement',
      'Information rightfully received from a third party without breach of any confidentiality obligation',
      'Information independently developed without use of Confidential Information',
      'Information required to be disclosed by law or court order'
    ],

    // Return of materials clause
    includeReturnClause: ndaData.includeReturnClause !== false,
    returnPeriod: ndaData.returnPeriod || '30 days',

    // Governing law
    governingState: ndaData.governingState,
    arbitration: ndaData.arbitration || false
  };

  return generateContract(templatePath, contractData, outputPath);
}

// Example usage:
const nda = generateNDA({
  type: 'mutual',
  disclosingParty: {
    name: 'Acme Corp',
    address: '123 Business St, City, State 12345',
    email: 'legal@acme.com'
  },
  receivingParty: {
    name: 'Widget LLC',
    address: '456 Commerce Ave, City, State 67890',
    email: 'contracts@widget.com'
  },
  purpose: 'evaluation of potential partnership for joint product development',
  confidentialityPeriod: '5 years',
  governingState: 'California'
}, './output/nda-acme-widget.docx');
```

### Workflow 3: Service Agreement Generator
**Purpose:** Create service contracts with scope, deliverables, and payment terms

**Steps:**
1. Define service provider and client information
2. Specify scope of services in detail
3. List deliverables and timelines
4. Set payment terms (fixed, hourly, milestone-based)
5. Define intellectual property ownership
6. Add termination clauses
7. Include liability limitations
8. Generate agreement with all terms

**Implementation:**
```javascript
function generateServiceAgreement(serviceData, outputPath) {
  const contractData = {
    contractType: 'Service Agreement',

    party1: serviceData.serviceProvider,
    party2: serviceData.client,

    effectiveDate: serviceData.effectiveDate,
    term: serviceData.term || 'ongoing until completion',

    // Scope of services
    scope: serviceData.services.map(s => s.description).join('\n'),
    deliverables: serviceData.deliverables,

    // Payment terms
    paymentStructure: serviceData.paymentStructure, // 'fixed', 'hourly', 'milestone'
    totalAmount: serviceData.totalAmount,
    hourlyRate: serviceData.hourlyRate,
    milestones: serviceData.milestones || [],
    paymentSchedule: serviceData.paymentSchedule,
    paymentTerms: serviceData.paymentTerms || 'Net 30',

    // Intellectual property
    ipOwnership: serviceData.ipOwnership || 'client', // 'client', 'provider', 'shared'
    includeWorkForHire: serviceData.includeWorkForHire !== false,

    // Termination
    terminationNotice: serviceData.terminationNotice || '30 days',
    includeTerminationForConvenience: serviceData.includeTerminationForConvenience !== false,

    // Liability
    liabilityLimit: serviceData.liabilityLimit || 'total amount paid under this Agreement',
    includeIndemnification: serviceData.includeIndemnification !== false,

    // Confidentiality
    includeConfidentiality: true,
    confidentialityPeriod: '3 years',

    governingState: serviceData.governingState
  };

  return generateContract('./templates/service-agreement.docx', contractData, outputPath);
}
```

### Workflow 4: Clause Library Management
**Purpose:** Manage reusable contract clauses for different situations

**Steps:**
1. Define clause library with categories
2. Store standard clauses with variables
3. Create clause variations for different scenarios
4. Tag clauses by jurisdiction and type
5. Allow clause selection during contract generation
6. Support custom clause insertion
7. Maintain clause version history

**Implementation:**
```javascript
const clauseLibrary = {
  confidentiality: {
    standard: `The Receiving Party shall hold in strict confidence and not disclose to any third parties any Confidential Information disclosed by the Disclosing Party, except as approved in writing by the Disclosing Party.`,

    withExceptions: `The Receiving Party shall hold in strict confidence and not disclose to any third parties any Confidential Information disclosed by the Disclosing Party, except: (a) to its employees, contractors, and advisors who have a legitimate need to know and are bound by confidentiality obligations; or (b) as required by law.`,

    mutual: `Each Party agrees to hold the other Party's Confidential Information in strict confidence and to use such information solely for the purposes of {purpose}.`
  },

  termination: {
    forConvenience: `Either Party may terminate this Agreement at any time, with or without cause, upon {terminationNotice} written notice to the other Party.`,

    forCause: `Either Party may terminate this Agreement immediately upon written notice if the other Party materially breaches this Agreement and fails to cure such breach within {cureperiod} days after receiving written notice thereof.`,

    combined: `Either Party may terminate this Agreement: (a) for convenience upon {terminationNotice} written notice; or (b) immediately for cause if the other Party materially breaches this Agreement and fails to cure within {curePeriod} days.`
  },

  liability: {
    limitation: `IN NO EVENT SHALL EITHER PARTY'S LIABILITY UNDER THIS AGREEMENT EXCEED {liabilityLimit}.`,

    exclusion: `NEITHER PARTY SHALL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS, LOSS OF DATA, OR BUSINESS INTERRUPTION.`,

    combined: `IN NO EVENT SHALL EITHER PARTY'S LIABILITY EXCEED {liabilityLimit}. NEITHER PARTY SHALL BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES.`
  },

  payment: {
    net30: `Client shall pay all undisputed invoices within thirty (30) days of the invoice date.`,

    upfront: `Client shall pay {percentage}% of the total fees upon execution of this Agreement, with the remainder due upon {milestone}.`,

    milestone: `Payments shall be made according to the following milestones:\n{milestoneList}`
  }
};

function insertClause(clauseCategory, clauseType, variables = {}) {
  let clause = clauseLibrary[clauseCategory][clauseType];

  // Replace variables
  Object.keys(variables).forEach(key => {
    const regex = new RegExp(`{${key}}`, 'g');
    clause = clause.replace(regex, variables[key]);
  });

  return clause;
}
```

### Workflow 5: Contract Review Checklist
**Purpose:** Validate generated contracts against a checklist of required elements

**Steps:**
1. Define checklist for contract type
2. Parse generated contract
3. Check for required sections
4. Validate party information completeness
5. Verify dates are logical (effective before expiration)
6. Ensure signature blocks are present
7. Check for placeholder text that wasn't replaced
8. Generate review report

**Implementation:**
```javascript
function reviewContract(contractPath, contractType) {
  const content = fs.readFileSync(contractPath, 'utf8');

  const checklist = {
    nda: [
      { item: 'Party names and addresses', required: true },
      { item: 'Effective date', required: true },
      { item: 'Definition of confidential information', required: true },
      { item: 'Obligations of receiving party', required: true },
      { item: 'Exclusions from confidentiality', required: true },
      { item: 'Term/duration of confidentiality', required: true },
      { item: 'Return of materials clause', required: false },
      { item: 'Governing law and jurisdiction', required: true },
      { item: 'Signature blocks', required: true }
    ],
    serviceAgreement: [
      { item: 'Party names and addresses', required: true },
      { item: 'Scope of services', required: true },
      { item: 'Deliverables', required: true },
      { item: 'Payment terms and amounts', required: true },
      { item: 'Timeline/term', required: true },
      { item: 'Intellectual property ownership', required: true },
      { item: 'Termination provisions', required: true },
      { item: 'Limitation of liability', required: true },
      { item: 'Governing law', required: true },
      { item: 'Signature blocks', required: true }
    ]
  };

  const items = checklist[contractType] || checklist.nda;
  const results = [];

  items.forEach(checkItem => {
    // Simple text search (in production, use more sophisticated parsing)
    const found = content.toLowerCase().includes(checkItem.item.toLowerCase());

    results.push({
      item: checkItem.item,
      required: checkItem.required,
      present: found,
      status: found ? 'PASS' : (checkItem.required ? 'FAIL' : 'WARN')
    });
  });

  // Check for unreplaced placeholders
  const placeholders = content.match(/\{[^}]+\}/g) || [];

  return {
    contractType,
    checklistResults: results,
    passedRequired: results.filter(r => r.required).every(r => r.present),
    unreplacedPlaceholders: placeholders,
    review: {
      passed: results.filter(r => r.status === 'PASS').length,
      failed: results.filter(r => r.status === 'FAIL').length,
      warnings: results.filter(r => r.status === 'WARN').length
    }
  };
}
```

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Generate contract | "create [contract type] for [parties]" |
| NDA | "generate NDA between [party1] and [party2]" |
| Service agreement | "create service agreement" |
| Add clause | "insert [clause type] clause" |
| Review contract | "check contract for completeness" |
| Custom template | "use custom contract template" |
| Batch generate | "create contracts for [list]" |

## Best Practices

- **Legal Review:** ALWAYS have contracts reviewed by an attorney before use
- **Version Control:** Track template versions and changes
- **Jurisdiction-Specific:** Use templates appropriate for the governing jurisdiction
- **Plain Language:** Use clear, understandable language when possible
- **Definitions:** Define all key terms clearly in the contract
- **Completeness:** Ensure all required sections are present before finalizing
- **Variables:** Validate all variables are replaced before generating final document
- **Formatting:** Maintain consistent formatting for professional appearance
- **Signatures:** Include proper signature blocks with date and title fields
- **Backup:** Store all generated contracts securely
- **Audit Trail:** Maintain records of when and how contracts were generated
- **Custom Review:** Each contract should be reviewed for specific circumstances

## Common Patterns

**Employment Contract:**
```javascript
const employmentData = {
  contractType: 'Employment Agreement',
  employer: { name: 'Acme Corp', address: '...' },
  employee: { name: 'John Doe', address: '...' },
  position: 'Senior Developer',
  startDate: '2025-02-01',
  salary: 120000,
  benefits: ['Health insurance', '401k matching', 'PTO'],
  probationPeriod: '90 days',
  includeNonCompete: true,
  nonCompetePeriod: '12 months'
};
```

**Consulting Agreement:**
```javascript
const consultingData = {
  serviceProvider: { name: 'Jane Smith Consulting', ... },
  client: { name: 'Widget Inc', ... },
  services: [
    { description: 'Strategic planning consultation', hours: 20 },
    { description: 'Market analysis', hours: 40 }
  ],
  paymentStructure: 'hourly',
  hourlyRate: 250,
  term: '3 months',
  ipOwnership: 'client'
};
```

## Dependencies

Install required packages:
```bash
npm install docxtemplater pizzip
npm install pdf-lib          # For PDF manipulation
npm install handlebars       # Alternative templating
```

## Error Handling

- **Missing Required Fields:** Validate all required data before generation
- **Invalid Dates:** Ensure effective date is before expiration date
- **Template Not Found:** Verify template file exists before processing
- **Variable Mismatch:** Check that all template variables have data
- **File Permissions:** Handle read/write errors gracefully
- **Legal Compliance:** Include disclaimers about legal review requirement

## Advanced Features

**Electronic Signature Integration:**
```javascript
const docusign = require('docusign-esign');

async function sendForSignature(contractPath, signers) {
  // DocuSign or other e-signature integration
  // Send contract for electronic signature
}
```

**Contract Versioning:**
```javascript
const contractVersion = {
  version: '1.2',
  templateId: 'service-agreement-v1.2',
  changes: 'Updated liability clause per legal review',
  approvedBy: 'Legal Team',
  approvedDate: '2025-01-01'
};
```

**Multi-Jurisdiction Support:**
```javascript
const jurisdictionClauses = {
  california: {
    governingLaw: 'This Agreement shall be governed by the laws of the State of California.',
    arbitration: 'Mandatory arbitration under California law'
  },
  newYork: {
    governingLaw: 'This Agreement shall be governed by the laws of the State of New York.',
    arbitration: 'JAMS arbitration in New York County'
  }
};
```