# Document Processing (PDF)

Gemini processes PDFs using native vision to understand entire document contexts including text, images, diagrams, charts, and tables.

## Table of Contents

- [Capabilities](#capabilities)
- [Inline PDF Data](#inline-pdf-data)
- [Files API (Large PDFs)](#files-api-large-pdfs)
- [Multiple PDFs](#multiple-pdfs)
- [Technical Details](#technical-details)
- [Best Practices](#best-practices)

---

## Capabilities

- Analyze up to 1000 pages per document
- Extract information into structured output formats
- Summarize and answer questions from visual and textual elements
- Transcribe content preserving layouts and formatting

**Note:** Non-PDF documents are treated as plain text, losing visual context like charts or formatting.

---

## Inline PDF Data

Best for smaller documents or temporary processing.

### From URL

```python
from google import genai
from google.genai import types
import io
import httpx

client = genai.Client()

doc_url = "https://example.com/document.pdf"
doc_data = io.BytesIO(httpx.get(doc_url).content)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        types.Part.from_bytes(data=doc_data.read(), mime_type='application/pdf'),
        "Summarize this document"
    ]
)
print(response.text)
```

```javascript
const pdfResp = await fetch('https://example.com/document.pdf')
    .then((response) => response.arrayBuffer());

const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: [
        { text: "Summarize this document" },
        {
            inlineData: {
                mimeType: 'application/pdf',
                data: Buffer.from(pdfResp).toString("base64")
            }
        }
    ]
});
```

### From Local File

```python
import pathlib

filepath = pathlib.Path('file.pdf')

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        types.Part.from_bytes(
            data=filepath.read_bytes(),
            mime_type='application/pdf',
        ),
        "Summarize this document"
    ]
)
```

```javascript
import * as fs from 'fs';

const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: [
        { text: "Summarize this document" },
        {
            inlineData: {
                mimeType: 'application/pdf',
                data: Buffer.from(fs.readFileSync("file.pdf")).toString("base64")
            }
        }
    ]
});
```

---

## Files API (Large PDFs)

Recommended for larger files or reusing documents across multiple requests. Files are stored for 48 hours.

### Upload from URL

```python
import io
import httpx

pdf_url = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"
doc_data = io.BytesIO(httpx.get(pdf_url).content)

uploaded_file = client.files.upload(
    file=doc_data,
    config=dict(mime_type='application/pdf')
)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[uploaded_file, "Summarize this document"]
)
```

```javascript
import { createPartFromUri, GoogleGenAI } from "@google/genai";

const pdfBuffer = await fetch(pdfUrl).then((r) => r.arrayBuffer());
const fileBlob = new Blob([pdfBuffer], { type: 'application/pdf' });

const file = await ai.files.upload({
    file: fileBlob,
    config: { displayName: 'document.pdf' },
});

// Wait for processing
let getFile = await ai.files.get({ name: file.name });
while (getFile.state === 'PROCESSING') {
    await new Promise((resolve) => setTimeout(resolve, 5000));
    getFile = await ai.files.get({ name: file.name });
}

const response = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: [
        'Summarize this document',
        createPartFromUri(file.uri, file.mimeType),
    ],
});
```

### Upload from Local File

```python
import pathlib

file_path = pathlib.Path('large_file.pdf')

uploaded_file = client.files.upload(file=file_path)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[uploaded_file, "Summarize this document"]
)
```

```javascript
const file = await ai.files.upload({
    file: 'path/to/file.pdf',
    config: { displayName: 'document.pdf' },
});

// Wait for processing...
```

### Check File Status

```python
file_info = client.files.get(name=uploaded_file.name)
print(file_info.model_dump_json(indent=4))
```

---

## Multiple PDFs

Process multiple documents (up to 1000 pages combined) in a single request.

```python
import io
import httpx

doc_url_1 = "https://arxiv.org/pdf/2312.11805"
doc_url_2 = "https://arxiv.org/pdf/2403.05530"

pdf_1 = client.files.upload(
    file=io.BytesIO(httpx.get(doc_url_1).content),
    config=dict(mime_type='application/pdf')
)
pdf_2 = client.files.upload(
    file=io.BytesIO(httpx.get(doc_url_2).content),
    config=dict(mime_type='application/pdf')
)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        pdf_1,
        pdf_2,
        "Compare the main benchmarks between these papers in a table."
    ]
)
```

```javascript
// Upload both files, wait for processing...

const response = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: [
        'Compare the main benchmarks between these papers in a table.',
        createPartFromUri(file1.uri, file1.mimeType),
        createPartFromUri(file2.uri, file2.mimeType),
    ],
});
```

---

## Technical Details

| Property | Value |
|----------|-------|
| Max file size | 50MB |
| Max pages | 1000 |
| Tokens per page | ~258 |
| Max resolution | 3072 x 3072 (scaled down) |
| Min resolution | 768 x 768 (scaled up) |

### Gemini 3 Enhancements

- `media_resolution` parameter: control vision processing (low, medium, high)
- Native text extraction: embedded PDF text is extracted separately
- Token billing: image tokens counted under `IMAGE` modality

### Supported Document Types

PDF is the only format with full visual understanding. Other formats (TXT, Markdown, HTML, XML) are extracted as plain text only.

---

## Best Practices

- Rotate pages to correct orientation before uploading
- Avoid blurry pages
- For single-page documents, place the text prompt after the page
- Use Files API for documents you'll reference multiple times
- Use structured outputs for data extraction tasks

---

## Resources

- [Document Processing Guide](https://ai.google.dev/gemini-api/docs/document-processing)
- [Media Resolution Guide](https://ai.google.dev/gemini-api/docs/media-resolution)
- [File Input Methods](https://ai.google.dev/gemini-api/docs/file-input-methods)
