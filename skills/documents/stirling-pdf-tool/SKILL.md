---
title: Stirling-PDF Tool
description: A local CLI tool for manipulating PDF files (merge, split, convert) using a Docker-hosted Stirling-PDF instance.
tool_name: stirling-pdf
---

# Stirling-PDF Tool

This tool allows you to perform advanced PDF operations by interfacing with a local Stirling-PDF instance running on Docker.

## Prerequisites
- Docker container `stirling-pdf` must be running on port 8080.
- Python 3 with `requests` installed (`pip install requests`).

## Usage

You can use this tool by running the python script directly.

### Commands

**Check Status**
```bash
python "C:\Users\matts\AI Workspace\custom_tools\stirling_pdf_tool\stirling_client.py" health
```

**Merge PDFs**
```bash
python "C:\Users\matts\AI Workspace\custom_tools\stirling_pdf_tool\stirling_client.py" merge <output_file.pdf> <input1.pdf> <input2.pdf> ...
```

**Split PDF**
```bash
python "C:\Users\matts\AI Workspace\custom_tools\stirling_pdf_tool\stirling_client.py" split <input.pdf> <output_directory>
```

**Convert to PDF**
```bash
python "C:\Users\matts\AI Workspace\custom_tools\stirling_pdf_tool\stirling_client.py" convert <input_file> <output_file.pdf>
```
