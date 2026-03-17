---
name: wget-reader
description: Fetch data from URLs. Use when asked to download content, fetch remote files, or read web data.
version: 1.0.0
---

# Wget URL Reader

## Overview

Fetches content from URLs using wget command-line tool. Supports downloading files, reading web pages, and retrieving API responses.

## Instructions

1. When user provides a URL to read or fetch:
   - Validate the URL format
   - Use wget with appropriate flags based on content type

2. For reading content to stdout (display):
   ```bash
   wget -qO- "<URL>"
   ```

3. For downloading files:
   ```bash
   wget -O "<filename>" "<URL>"
   ```

4. For JSON API responses:
   ```bash
   wget -qO- --header="Accept: application/json" "<URL>"
   ```

5. Common wget flags:
   - `-q`: Quiet mode (no progress output)
   - `-O-`: Output to stdout
   - `-O <file>`: Output to specific file
   - `--header`: Add custom HTTP header
   - `--timeout=<seconds>`: Set timeout
   - `--tries=<n>`: Number of retries
   - `--user-agent=<agent>`: Set user agent

## Examples

### Example: Read webpage content
**Input:** "Read the content from https://example.com"
**Command:**
```bash
wget -qO- "https://example.com"
```

### Example: Download a file
**Input:** "Download the file from https://example.com/data.json"
**Command:**
```bash
wget -O "data.json" "https://example.com/data.json"
```

### Example: Fetch API with headers
**Input:** "Fetch JSON from https://api.example.com/data"
**Command:**
```bash
wget -qO- --header="Accept: application/json" "https://api.example.com/data"
```

### Example: Download with timeout and retries
**Input:** "Download with 30 second timeout"
**Command:**
```bash
wget --timeout=30 --tries=3 -O "output.txt" "<URL>"
```

## Guidelines

### Do
- Always quote URLs to handle special characters
- Use `-q` flag to suppress progress bars in scripts
- Add `--timeout` for unreliable endpoints
- Respect robots.txt and rate limits

### Don't
- Use `--no-check-certificate` unless necessary
- Fetch URLs without validating format first
- Ignore HTTP error codes in responses
- Store credentials in command history
