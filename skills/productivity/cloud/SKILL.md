---
name: Cloud
description: "Choose, organize, sync, share, and back up personal files across iCloud, Google Drive, Dropbox, and OneDrive."
---

## Triggers

Activate on: iCloud full, cloud storage, backup photos, sync between devices, share folder, Google Drive help, Dropbox issues, "where are my files", storage plan comparison.

## Scope

This skill covers **consumer cloud storage** — the services regular people use for photos, documents, and backups.

**Not this skill:** AWS, Azure, S3 buckets, VPS, Docker, APIs → use `infrastructure`, `s3`, or `server`.

## Quick Service Picker

| Your devices | Best fit | Why |
|--------------|----------|-----|
| iPhone + Mac | iCloud | Native integration, seamless |
| Android + Chrome | Google Drive | Included with Gmail, auto photo backup |
| Windows PC | OneDrive | Built into Windows, Office integration |
| Mixed devices | Dropbox | Works equally well everywhere |

For detailed pricing and features, see `services.md`.

## Common Confusions

| What you think | What's actually happening |
|----------------|---------------------------|
| "I deleted it from my phone and now it's gone from my laptop" | Sync works as designed — one file, everywhere |
| "iCloud storage full but my phone has space" | Phone storage ≠ iCloud storage |
| "My photos are duplicated everywhere" | Multiple services backing up the same camera roll |
| "I pay for 3 cloud services" | Pick one primary, cancel the rest |

## Storage Full — What to Do

1. **Check what's using space** — Photos usually dominate
2. **Empty trash** — Deleted files count until trash is emptied
3. **Disable duplicate backups** — Pick one photo backup service
4. **Offload old files** — Move archives to external drive

For service-specific cleanup steps, see `cleanup.md`.

## Backup Strategy

- **3-2-1 rule:** 3 copies, 2 different media, 1 offsite
- **Cloud counts as offsite** — but also keep a local backup
- **Check backup status monthly** — don't assume it's working

What to back up and what NOT to store in cloud: see `backup.md`.

## Sharing Files

| Need | Method |
|------|--------|
| Quick share with anyone | Link (set expiration) |
| Ongoing family access | Shared folder |
| Sensitive documents | Don't use cloud, or encrypt first |

Step-by-step per service: see `sharing.md`.

## Security Basics

- **Enable 2FA** on all cloud accounts
- **Review shared links** quarterly — revoke old ones
- **Don't store unencrypted:** passwords, IDs, financial documents
