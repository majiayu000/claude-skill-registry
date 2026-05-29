---
name: agent-exporter
description: Upload tailored resume to cloud or attach to user session. Handles final formatting and delivery.
---

# Exporter Agent

## Overview

The Exporter Agent handles the final stage of the pipeline: converting the tailored data into a document and delivering it.

## Workflow Definition

1.  **Input**: Tailored Resume JSON.
2.  **Formatting**: Call `resume-format` to generate Markdown/Text.
3.  **Conversion**: (Future) Convert Markdown to PDF/DOCX.
4.  **Upload**: Call `upload-drive` to save to Google Drive (if configured).
5.  **Output**: Final download link or file path.
