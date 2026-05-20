---
name: data-governance
description: Data lineage, classification (PII/Confidential), and integrity checks (checksums).
role: biz-compliance, eng-data
triggers:
  - data lineage
  - pii masking
  - classification
  - checksum
  - data integrity
  - gdpr
---

# data-governance Skill

Data must be classified, tracked, and verifiable.

## 1. Classification
Before storing any field, tag it:
- **Public**: Safe to release (e.g., Product Descriptions).
- **Internal**: Employee-only (e.g., Org Charts).
- **Confidential**: Business secrets (e.g., Sales Forecasts).
- **Restricted/PII**: SSN, Credit Cards, Medical Records. **Must be Encrypted at Rest**.

## 2. Integrity Patterns
- **Checksums**: Store `md5/sha256` of files to detect bit-rot or tampering.
- **Foreign Keys**: Enforce referential integrity in the DB. No orphans.
- **Versioning**: Never overwrite critical data. Use `v1`, `v2` or Event Sourcing `AppendedOnly`.

## 3. Lineage
- Answer: "Where did this specific value in the dashboard come from?"
- Track: Source System -> ETL Job -> Warehouse -> BI Tool.

## 4. Retention & Deletion (GDPR/CCPA)
- **TTL**: Auto-delete logs after X days.
- **Right to be Forgotten**: Implementation of a `HardDeleteUser` workflow that purges PII from all tables/backups (crypto-shredding).
