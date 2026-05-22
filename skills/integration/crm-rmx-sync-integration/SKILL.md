---
name: crm-rmx-sync-integration
description: Create or update CRM to RMX syncing integrations. Use when adding a new synced entity, mapping, EF Core model/migration, or CrmSyncingInboxService logic for CRM to RMX (and optional RMX to CRM live sync/outbox). Produces a repeatable step-by-step plan and implements the integration.
---

# CRM RMX Sync Integration

## Overview
Create a repeatable plan and implement new CRM <-> RMX sync integrations (inbox, optional outbox/live sync). Ask for missing decisions, inspect schemas via crm_dbhub and dbhub, then update CRM PHP sync pipeline and RMX .NET/EF Core models, mappers, and CrmSyncingInboxService.

## Workflow (Plan + Implement)

### 1) Intake questions (ask only if not already answered)
- Which CRM table is the source? Provide schema and table name.
- Which CRM fields must be synced (and any transforms/defaults)?
- Does RMX need a new table/model (EF Core) or map into an existing RMX entity?
- Is there RMX -> CRM live syncing or outbox syncing for this entity? If yes, what events/fields?
- Any dependencies (parent entities that must exist first)?
- Desired ID strategy (CRM id, external id, GUID mapping)?

### 2) Gather context and schema
- Read `references/rmx-syncing-guide.md`.
- Open the initial CRM doc at `/mnt/wsl/yourcrm/public/includes/logical/rmx-sync/UptimeRMX-CRM-Integration-Instructions.md`.
- Use `crm_dbhub` to inspect CRM table columns and sample data shape.
- Use `dbhub` to check RMX DB `UptimeRmxBackend` schema for existing tables/fields.
- Locate the closest existing mapper/entity pair for pattern matching.

### 3) Produce the step-by-step plan
Include explicit file paths and ordered steps for:
- CRM changes (triggers, DTO, payload, RmxSynchronizer)
- RMX changes (JsonModels, InboxMappers, EF Core model/migration, CrmSyncingInboxService)
- Optional live sync/outbox work
- Testing, verification, and rollback notes

### 4) Implement CRM (inbox / CRM -> RMX)
- Add triggers/migrations for `sync_outbox` if the table is new to syncing.
- Add SyncTables enum constant.
- Create or extend CRM DTO model in `/mnt/wsl/yourcrm/public/includes/logical/rmx-sync/Models`.
- Update `RmxSynchronizer.php` to collect entity data, map to payload field, and include deletions if needed.
- Update payload model/serializer if required.

### 5) Implement RMX (inbox / CRM -> RMX)
- Add JSON model in `UptimeRMX.Service/CrmSyncing/JsonModels`.
- Add mapper in `UptimeRMX.Service/CrmSyncing/InboxMappers`.
- Update `UptimeRMX.Service/CrmSyncing/SyncingInboxPayload.cs` to include the new collection.
- If a new table is needed: add EF Core model in `UptimeRMX/Models/DefaultContextModels/...`, add DbSet in `UptimeRMX/Models/Context/DefaultContext.cs`, and create a migration in `UptimeRMX.Migrations`.
- Update `UptimeRMX.Service/CrmSyncing/CrmSyncingInboxService.cs` to upsert into RMX DB using existing `SyncChunks` and dictionary helpers (add to `CrmSyncDatabaseDictionaryHelper` if needed).
- Preserve dependency ordering (parents before children).

### 6) Optional RMX -> CRM live sync / outbox
- Add models and payload types used by live sync/outbox flows.
- Update RMX outbox service to publish, update CRM API handlers to apply changes.
- Document any new endpoints and required auth keys.

### 7) Validate
- Ensure payload serialization matches expected JSON casing.
- Run migrations (if any).
- Test with a sample payload or `SyncCrmFromFiles`.
- Verify `sync_outbox` status and RMX logs.

## Output expectations
- Provide a concrete plan with numbered steps.
- Call out files to edit and why.
- Ask clarifying questions inline if info is missing.
