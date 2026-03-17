---
name: pdf-processor
description: Extracts text and tables from PDF documents. Use when working with PDF files or when the user needs document analysis.
---

# PDF Processor

## Overview

Process PDF documents to extract text, tables, and metadata.

## Instructions

1. Validate the PDF file exists and is readable
2. Extract text content using appropriate parser
3. Identify and extract tabular data
4. Return structured output

## Examples

Input: "Extract the text from report.pdf"
Output: Plain text content of the document

Input: "Get all tables from financial-report.pdf"
Output: CSV-formatted table data

## Error Handling

If the PDF is encrypted, inform the user that a password may be required.
If the file is corrupted, return an appropriate error message.
