---
name: File Path Traversal Testing
description: This skill should be used when the user asks to "test for directory traversal", "exploit path traversal vulnerabilities", "read arbitrary files through web applications", "find LFI vulnerabilities", or "access files outside web root". It provides comprehensive file path traversal attack and testing methodologies.
metadata:
  author: zebbern
  version: 4.1.0-fractal
---

# File Path Traversal Testing

## Purpose

Identify and exploit file path traversal (directory traversal) vulnerabilities that allow attackers to read arbitrary files on the server, potentially including sensitive configuration files, credentials, and source code. This vulnerability occurs when user-controllable input is passed to filesystem APIs without proper validation.

## Prerequisites

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Required Tools](./sub-skills/required-tools.md)
### 2. [Required Knowledge](./sub-skills/required-knowledge.md)
### 3. [Phase 1: Understanding Path Traversal](./sub-skills/phase-1-understanding-path-traversal.md)
### 4. [Phase 2: Identifying Traversal Points](./sub-skills/phase-2-identifying-traversal-points.md)
### 5. [Phase 3: Basic Exploitation Techniques](./sub-skills/phase-3-basic-exploitation-techniques.md)
### 6. [Phase 4: Bypass Techniques](./sub-skills/phase-4-bypass-techniques.md)
### 7. [Phase 5: Linux Target Files](./sub-skills/phase-5-linux-target-files.md)
### 8. [Phase 6: Windows Target Files](./sub-skills/phase-6-windows-target-files.md)
### 9. [Phase 7: Automated Testing](./sub-skills/phase-7-automated-testing.md)
### 10. [Phase 8: LFI to RCE Escalation](./sub-skills/phase-8-lfi-to-rce-escalation.md)
### 11. [Phase 9: Testing Methodology](./sub-skills/phase-9-testing-methodology.md)
### 12. [Phase 10: Prevention Measures](./sub-skills/phase-10-prevention-measures.md)
### 13. [Common Payloads](./sub-skills/common-payloads.md)
### 14. [Target Files](./sub-skills/target-files.md)
### 15. [Encoding Variants](./sub-skills/encoding-variants.md)
### 16. [Permission Restrictions](./sub-skills/permission-restrictions.md)
### 17. [Application Restrictions](./sub-skills/application-restrictions.md)
### 18. [Testing Considerations](./sub-skills/testing-considerations.md)
