---
name: document-generation-pdf
description: Generate, fill, and assemble PDF documents at scale. Handles legal forms, contracts, invoices, certificates. Supports form filling (pdf-lib), template rendering (Puppeteer, LaTeX), digital signatures (DocuSign), and document assembly. Use for legal tech, HR automation, invoice generation. Activate on "PDF generation", "form filling", "document automation", "digital signatures". NOT for simple PDF viewing, basic file conversion, or OCR text extraction.
allowed-tools: Read,Write,Edit,Bash(npm:*,latex*)
---

# Document Generation & PDF Automation

Expert in generating, filling, and assembling PDF documents programmatically for legal, HR, and business workflows.

## When to Use

✅ **Use for**:
- Legal form automation (expungement, immigration, contracts)
- Invoice/receipt generation at scale
- Certificate creation (completion, participation, awards)
- Contract assembly from templates
- Government form filling (IRS, court filings)
- Multi-document packet creation

❌ **NOT for**:
- Simple PDF viewing (use browser or pdf.js)
- Basic file conversion (use online tools)
- OCR text extraction (use Tesseract.js or AWS Textract)
- PDF editing by hand (use Adobe Acrobat)

---

## Technology Selection

### pdf-lib vs Puppeteer vs LaTeX

| Feature | pdf-lib | Puppeteer | LaTeX |
|---------|---------|-----------|-------|
| Form filling | ✅ Native | ❌ Complex | ❌ No |
| Template rendering | ❌ No | ✅ HTML/CSS | ✅ Templates |
| Performance (1000 PDFs) | 5s | 60s | 30s |
| File size | Small | Medium | Small |
| Signature fields | ✅ Yes | ❌ No | ❌ No |
| Best for | Government forms | Invoices, reports | Academic papers |

**Timeline**:
- 2000s: LaTeX for academic documents
- 2010: PDFKit (Node.js) for generation
- 2017: Puppeteer for HTML → PDF
- 2019: pdf-lib for pure JS form filling
- 2024: pdf-lib is gold standard for forms

**Decision tree**:
```
Need to fill existing form? → pdf-lib
Need complex layouts? → Puppeteer (HTML/CSS)
Need academic formatting? → LaTeX
Need to merge PDFs? → pdf-lib
Need digital signatures? → pdf-lib + DocuSign API
```

---

## Common Anti-Patterns

### Anti-Pattern 1: Using Puppeteer for Simple Form Filling

**Novice thinking**: "I'll use Puppeteer for everything, it's versatile"

**Problem**: 12x slower, 10x more memory, can't preserve form fields.

**Wrong approach**:
```typescript
// ❌ Puppeteer for simple form filling (SLOW!)
import puppeteer from 'puppeteer';

async function fillForm(data: FormData): Promise<Buffer> {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Load PDF in browser
  await page.goto(`file://${pdfPath}`);

  // Somehow fill form fields? (hacky)
  await page.evaluate((data) => {
    // Can't easily access PDF form fields from DOM
    // Would need to convert PDF → HTML first
  }, data);

  const pdf = await page.pdf();
  await browser.close();

  return pdf;
}
```

**Why wrong**:
- Browser overhead (200MB+ RAM per instance)
- Can't access native PDF form fields
- Loses interactive form capabilities
- 12x slower than pdf-lib

**Correct approach**:
```typescript
// ✅ pdf-lib for form filling (FAST!)
import { PDFDocument } from 'pdf-lib';

async function fillForm(templatePath: string, data: FormData): Promise<Uint8Array> {
  // Load existing PDF form
  const existingPdfBytes = await fs.readFile(templatePath);
  const pdfDoc = await PDFDocument.load(existingPdfBytes);

  // Get form
  const form = pdfDoc.getForm();

  // Fill text fields
  form.getTextField('applicant_name').setText(data.name);
  form.getTextField('case_number').setText(data.caseNumber);
  form.getTextField('date_of_birth').setText(data.dob);

  // Fill checkboxes
  if (data.hasPriorConvictions) {
    form.getCheckBox('prior_convictions').check();
  }

  // Fill dropdowns
  form.getDropdown('state').select(data.state);

  // Flatten form (make non-editable)
  form.flatten();

  // Save
  return await pdfDoc.save();
}
```

**Performance comparison** (1000 PDFs):
- Puppeteer: 60 seconds, 4GB RAM
- pdf-lib: 5 seconds, 200MB RAM

**Timeline context**:
- 2017: Puppeteer released, everyone used it for PDFs
- 2019: pdf-lib released, proper form handling
- 2024: pdf-lib is standard for government forms

---

### Anti-Pattern 2: Not Flattening Forms

**Problem**: Users can edit filled forms, causing data inconsistencies.

**Wrong approach**:
```typescript
// ❌ Don't flatten - form stays editable
const pdfDoc = await PDFDocument.load(existingPdfBytes);
const form = pdfDoc.getForm();

form.getTextField('name').setText('John Doe');

const pdfBytes = await pdfDoc.save();
// User can open PDF and change "John Doe" to anything!
```

**Why wrong**:
- User can modify official documents
- Data doesn't match database
- Violates document integrity

**Correct approach**:
```typescript
// ✅ Flatten form after filling
const pdfDoc = await PDFDocument.load(existingPdfBytes);
const form = pdfDoc.getForm();

form.getTextField('name').setText('John Doe');

// Flatten (convert fields to static text)
form.flatten();

const pdfBytes = await pdfDoc.save();
// User can't edit filled values ✅
```

**When NOT to flatten**:
- Draft documents (user needs to review/edit)
- Multi-step workflows (partial completion)
- Templates for users to fill manually

---

### Anti-Pattern 3: Generating PDFs from HTML Without Page Breaks

**Novice thinking**: "HTML → PDF is easy with Puppeteer"

**Problem**: Content splits mid-sentence across pages.

**Wrong approach**:
```typescript
// ❌ No page break control
const html = `
  <div class="contract">
    <h1>Mutual Agreement</h1>
    <p>Long paragraph that might split across pages...</p>
    <section>
      <h2>Terms and Conditions</h2>
      <ol>
        <li>Term 1 that could get cut off...</li>
        <li>Term 2...</li>
      </ol>
    </section>
  </div>
`;

const pdf = await page.pdf({ format: 'A4' });
// Result: Ugly page breaks in middle of sections
```

**Correct approach**:
```typescript
// ✅ Explicit page break control with CSS
const html = `
  <style>
    @media print {
      .page-break { page-break-after: always; }
      .avoid-break { page-break-inside: avoid; }

      h1, h2, h3 {
        page-break-after: avoid;
        page-break-inside: avoid;
      }

      section {
        page-break-inside: avoid;
      }
    }
  </style>

  <div class="contract">
    <section class="avoid-break">
      <h1>Mutual Agreement</h1>
      <p>This entire section stays together...</p>
    </section>

    <div class="page-break"></div>

    <section class="avoid-break">
      <h2>Terms and Conditions</h2>
      <ol>
        <li>Term 1</li>
        <li>Term 2</li>
      </ol>
    </section>
  </div>
`;

const pdf = await page.pdf({
  format: 'A4',
  printBackground: true,
  margin: {
    top: '1in',
    right: '1in',
    bottom: '1in',
    left: '1in'
  }
});
```

**CSS print properties**:
- `page-break-before: always` - Force new page before element
- `page-break-after: always` - Force new page after element
- `page-break-inside: avoid` - Keep element together

---

### Anti-Pattern 4: Not Handling Signature Fields

**Problem**: Signature fields aren't clickable in generated PDFs.

**Wrong approach**:
```typescript
// ❌ Add signature as image (not a real signature field)
const pdfDoc = await PDFDocument.load(existingPdfBytes);

const signatureImage = await pdfDoc.embedPng(signaturePngBytes);
const page = pdfDoc.getPage(0);

page.drawImage(signatureImage, {
  x: 100,
  y: 100,
  width: 200,
  height: 50
});

await pdfDoc.save();
// Not a real signature field - can't be signed digitally
```

**Why wrong**:
- Not legally recognized (just an image)
- Can't use DocuSign/Adobe Sign
- No signature metadata (who, when)

**Correct approach 1**: Create signature field (for DocuSign)
```typescript
// ✅ Create signature field for electronic signing
const pdfDoc = await PDFDocument.load(existingPdfBytes);
const form = pdfDoc.getForm();

// Create signature field
const signatureField = form.createTextField('applicant_signature');
signatureField.addToPage(pdfDoc.getPage(0), {
  x: 100,
  y: 100,
  width: 200,
  height: 50
});

// Mark as signature field (metadata)
signatureField.updateWidgets({
  borderWidth: 1,
  borderColor: { type: 'RGB', red: 0, green: 0, blue: 0 }
});

await pdfDoc.save();
// DocuSign can now detect and fill this field ✅
```

**Correct approach 2**: DocuSign API integration
```typescript
// ✅ Send to DocuSign for e-signature
import { ApiClient, EnvelopesApi } from 'docusign-esign';

async function sendForSignature(pdfBytes: Uint8Array, signerEmail: string) {
  const apiClient = new ApiClient();
  apiClient.setBasePath('https://demo.docusign.net/restapi');

  const envelopesApi = new EnvelopesApi(apiClient);

  const envelope = {
    emailSubject: 'Please sign: Expungement Petition',
    documents: [{
      documentBase64: Buffer.from(pdfBytes).toString('base64'),
      name: 'Petition.pdf',
      fileExtension: 'pdf',
      documentId: '1'
    }],
    recipients: {
      signers: [{
        email: signerEmail,
        name: 'John Doe',
        recipientId: '1',
        tabs: {
          signHereTabs: [{
            documentId: '1',
            pageNumber: '1',
            xPosition: '100',
            yPosition: '100'
          }]
        }
      }]
    },
    status: 'sent'
  };

  return await envelopesApi.createEnvelope(accountId, { envelopeDefinition: envelope });
}
```

---

### Anti-Pattern 5: Storing Filled PDFs Without Encryption

**Problem**: Sensitive legal documents stored in plain text.

**Wrong approach**:
```typescript
// ❌ Save PDF to disk unencrypted
const pdfBytes = await pdfDoc.save();
await fs.writeFile(`./documents/${caseId}.pdf`, pdfBytes);
// Sensitive data accessible to anyone with file system access
```

**Why wrong**:
- Legal/medical data exposed
- HIPAA/GDPR violations
- Data breach liability

**Correct approach 1**: Encrypt at rest
```typescript
// ✅ Encrypt PDF with user password
const pdfBytes = await pdfDoc.save({
  userPassword: generateSecurePassword(),
  ownerPassword: process.env.PDF_OWNER_PASSWORD,
  permissions: {
    printing: 'highResolution',
    modifying: false,
    copying: false,
    annotating: false,
    fillingForms: false,
    contentAccessibility: true,
    documentAssembly: false
  }
});

await fs.writeFile(`./documents/${caseId}.pdf`, pdfBytes);
```

**Correct approach 2**: Store in encrypted storage (S3 with SSE)
```typescript
// ✅ Upload to S3 with server-side encryption
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({ region: 'us-east-1' });

await s3Client.send(new PutObjectCommand({
  Bucket: 'expungement-documents',
  Key: `cases/${caseId}/petition.pdf`,
  Body: pdfBytes,
  ServerSideEncryption: 'AES256',
  Metadata: {
    caseId: caseId,
    documentType: 'petition',
    generatedAt: new Date().toISOString()
  },
  ACL: 'private'  // Not publicly accessible
}));

// Store S3 URL in database (encrypted)
await db.documents.insert({
  case_id: caseId,
  s3_url: encrypt(`s3://expungement-documents/cases/${caseId}/petition.pdf`),
  created_at: new Date()
});
```

**Compliance requirements**:
- HIPAA: Encryption at rest + in transit, access logging
- GDPR: Right to deletion, data minimization
- State bar rules: Attorney-client privilege protection

---

## Production Checklist

```
□ Form fields filled correctly (test with validation)
□ Forms flattened after filling (non-editable)
□ Page breaks controlled (no mid-sentence splits)
□ Signature fields created (for DocuSign/Adobe Sign)
□ PDFs encrypted at rest (S3 SSE or user password)
□ Access logged (who viewed/downloaded)
□ Auto-deletion scheduled (retention policy)
□ Fonts embedded (cross-platform compatibility)
□ File size optimized (&lt;5MB per document)
□ Batch generation tested (1000+ PDFs)
```

---

## When to Use vs Avoid

| Scenario | Appropriate? |
|----------|--------------|
| Fill 50+ government forms | ✅ Yes - automate with pdf-lib |
| Generate invoices from template | ✅ Yes - Puppeteer from HTML |
| Create certificates at scale | ✅ Yes - pdf-lib or LaTeX |
| Assemble multi-doc packets | ✅ Yes - pdf-lib merge |
| View PDFs in browser | ❌ No - use pdf.js or browser |
| Edit PDF by hand | ❌ No - use Adobe Acrobat |
| Extract text with OCR | ❌ No - use Tesseract/Textract |

---

## References

- `/references/pdf-lib-guide.md` - Form filling, field types, flattening, encryption
- `/references/puppeteer-templates.md` - HTML templates, page breaks, styling for print
- `/references/document-assembly.md` - Merging PDFs, packet creation, watermarks

## Scripts

- `scripts/form_filler.ts` - Fill PDF forms from JSON data, batch processing
- `scripts/document_assembler.ts` - Merge multiple PDFs, add cover pages, watermarks

---

**This skill guides**: PDF generation | Form filling | Document automation | Digital signatures | pdf-lib | Puppeteer | LaTeX | DocuSign
