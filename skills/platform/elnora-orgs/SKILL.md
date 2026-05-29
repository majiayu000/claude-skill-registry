---
name: elnora-orgs
description: >
  Use this skill when the user asks about "Elnora organizations", "org members",
  "org billing", "org invitations", "shared library", "library folders",
  "org settings", or any task involving Elnora organization management.
  Covers org CRUD, membership, invitations, billing, and the shared library.
---

# Elnora Organizations

Manage organizations, members, invitations, billing, and the shared org library
via Elnora MCP tools.

## Core Concepts

- **Organizations** are the top-level container. They hold projects, members, and a shared library.
- **Members** have roles (owner, admin, member). Use the **membership ID** (not user ID) for role updates and removals.
- **Invitations** are sent by email with a role. They can be cancelled before acceptance.
- **Billing** is per-org. Query it to check plan, usage, and limits.
- **Shared Library** stores org-wide files and folders accessible to all members.

## Tools Reference

### Organization CRUD

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_list_orgs` | List all orgs the user belongs to | — |
| `elnora_get_org` | Get org details | `org_id` |
| `elnora_create_org` | Create a new org | `name` |
| `elnora_update_org` | Update org settings | `org_id`, fields to update |

### Membership

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_list_org_members` | List members of an org | `org_id` |
| `elnora_update_org_member_role` | Change a member's role | `org_id`, `membership_id`, `role` |
| `elnora_remove_org_member` | Remove a member from org | `org_id`, `membership_id` |

**Important**: `elnora_update_org_member_role` and `elnora_remove_org_member` require the
**membership ID**, not the user ID. Get it from `elnora_list_org_members` first.

### Invitations

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_invite_org_member` | Invite someone by email | `org_id`, `email`, `role` |
| `elnora_list_org_invitations` | List pending invitations | `org_id` |
| `elnora_cancel_org_invitation` | Cancel a pending invitation | `org_id`, `invitation_id` |

### Billing

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_get_org_billing` | Get billing/plan info | `org_id` |

### Shared Library

The shared library provides org-wide file and folder storage.

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_list_library_files` | List files in the shared library | `org_id`, optional `folder_id` |
| `elnora_list_library_folders` | List library folders | `org_id` |
| `elnora_create_library_folder` | Create a library folder | `org_id`, `name` |
| `elnora_rename_library_folder` | Rename a library folder | `org_id`, `folder_id`, `name` |
| `elnora_delete_library_folder` | Delete a library folder | `org_id`, `folder_id` |

**Warning**: `elnora_delete_library_folder` is destructive. Confirm with the user before deleting.

## Common Workflows

### List orgs and inspect one

1. `elnora_list_orgs` to get all orgs
2. `elnora_get_org` with the chosen `org_id` for details

### Invite a new member

1. `elnora_invite_org_member` with `org_id`, `email`, and `role`
2. `elnora_list_org_invitations` to confirm the invitation was sent

### Change a member's role

1. `elnora_list_org_members` with `org_id` to find the `membership_id`
2. `elnora_update_org_member_role` with `org_id`, `membership_id`, and new `role`

### Manage the shared library

1. `elnora_list_library_folders` to see existing folders
2. `elnora_create_library_folder` to add a new folder
3. `elnora_list_library_files` with optional `folder_id` to browse contents

### Check billing

1. `elnora_list_orgs` to get the `org_id`
2. `elnora_get_org_billing` to view plan, usage, and limits

## ID Format

All IDs are UUIDs (e.g., `bfdc6fbd-40ed-4042-9ea7-c79a5ec90085`).
