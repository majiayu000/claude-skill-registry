---
name: contacts
description: Manage Google Contacts with full CRUD operations via Ruby scripts. This skill should be used when searching, viewing, creating, updating, or deleting contacts in Google Contacts. Supports contact lookup, batch operations, and comprehensive contact field management including names, emails, phones, addresses, birthdays, organizations, and notes.
---

# Google Contacts Management Skill

## Overview

Provide comprehensive Google Contacts management capabilities through Ruby-based scripts with shared authentication. Enable full CRUD operations (Create, Read, Update, Delete) on Google Contacts with support for all standard contact fields.

## When to Use This Skill

Use this skill for ANY Google Contacts operations:

- **Search & Lookup**: Find contacts by name, email, or other fields
- **View Details**: Get complete contact information including all fields
- **Create Contacts**: Add new contacts with any combination of fields
- **Update Contacts**: Modify existing contact information
- **Delete Contacts**: Remove contacts from Google Contacts
- **List & Browse**: View all contacts with pagination support
- **Batch Operations**: Manage multiple contacts efficiently

## Authentication

This skill shares authentication with the calendar skill via `~/.claude/.google/token.json`. Both skills use the same OAuth token with scopes:
- `https://www.googleapis.com/auth/calendar` (Calendar access)
- `https://www.googleapis.com/auth/contacts` (Contacts read/write access)

When either skill refreshes the token, both skills benefit from the updated authentication.

### First-Time Setup

If not already configured:

1. Ensure `~/.claude/.google/client_secret.json` exists with OAuth credentials
2. Run any contacts operation - the script will prompt for authorization
3. The token will be stored and shared with calendar skill

### Re-authorization for New Scope

Since the contacts scope has been updated from readonly to full access, you'll need to re-authorize once:

```bash
# Delete the existing token to force re-authorization
rm ~/.claude/.google/token.json

# Run any contacts operation to trigger OAuth flow
~/.claude/skills/contacts/scripts/contacts_manager.rb --list
```

Follow the authorization URL and enter the code when prompted.

## Core Script: contacts_manager.rb

Location: `scripts/contacts_manager.rb`

Comprehensive Ruby script providing all Google Contacts operations through the People API v1.

### Search Contacts

Find contacts by name or other search criteria:

```bash
# Search by name
contacts_manager.rb --search "John Smith"

# Search by partial name
contacts_manager.rb --search "John"
```

Returns JSON with matching contacts including all available fields.

### Get Contact Details

Retrieve complete information for a specific contact:

```bash
# Get by resource name (from search results)
contacts_manager.rb --get "people/c1234567890"
```

Returns full contact details including names, emails, phones, addresses, birthdays, organizations, notes, and URLs.

### List All Contacts

Browse contacts with pagination support:

```bash
# List first 100 contacts
contacts_manager.rb --list

# List with custom page size
contacts_manager.rb --list --page-size 50

# Get next page using token from previous response
contacts_manager.rb --list --page-token "NEXT_PAGE_TOKEN"
```

Returns array of contacts with `next_page_token` for pagination.

### Create New Contact

Add a new contact with any combination of fields:

```bash
# Minimal contact (name and email)
contacts_manager.rb --create '{
  "name": {
    "given_name": "John",
    "family_name": "Doe",
    "display_name": "John Doe"
  },
  "emails": [
    {"value": "john@example.com", "type": "home"}
  ]
}'

# Complete contact with all fields
contacts_manager.rb --create '{
  "name": {
    "given_name": "Jane",
    "family_name": "Smith",
    "display_name": "Jane Smith"
  },
  "emails": [
    {"value": "jane@work.com", "type": "work"},
    {"value": "jane@personal.com", "type": "home"}
  ],
  "phones": [
    {"value": "555-1234", "type": "mobile"},
    {"value": "555-5678", "type": "work"}
  ],
  "organization": {
    "name": "Acme Corp",
    "title": "Senior Engineer"
  },
  "birthday": {
    "year": 1990,
    "month": 5,
    "day": 15
  },
  "addresses": [
    {
      "street": "123 Main St",
      "city": "Springfield",
      "state": "IL",
      "zip": "62701",
      "country": "US",
      "type": "home"
    }
  ],
  "notes": "Met at conference 2024"
}'
```

### Update Existing Contact

Modify contact information using resource name:

```bash
# Update phone number
contacts_manager.rb --update "people/c1234567890" \
  --update-data '{"phones":[{"value":"555-9999","type":"mobile"}]}' \
  --update-mask "phoneNumbers"

# Update email addresses
contacts_manager.rb --update "people/c1234567890" \
  --update-data '{"emails":[{"value":"newemail@example.com","type":"work"}]}' \
  --update-mask "emailAddresses"

# Update multiple fields
contacts_manager.rb --update "people/c1234567890" \
  --update-data '{
    "phones":[{"value":"555-1111","type":"mobile"}],
    "organization":{"name":"New Company","title":"Director"}
  }' \
  --update-mask "phoneNumbers,organizations"
```

**Update Mask Fields**: Specify which fields to update (comma-separated):
- `names` - Name fields
- `emailAddresses` - Email addresses
- `phoneNumbers` - Phone numbers
- `organizations` - Organization/company info
- `birthdays` - Birthday information
- `addresses` - Physical addresses
- `biographies` - Notes/biography

### Delete Contact

Remove a contact permanently:

```bash
contacts_manager.rb --delete "people/c1234567890"
```

**Warning**: This permanently deletes the contact. There is no undo.

## Contact Field Reference

See `references/contact_fields.md` for comprehensive documentation of all available contact fields and their data structures.

### Common Fields

- **Names**: `given_name`, `family_name`, `display_name`
- **Emails**: `value`, `type` (home, work, other)
- **Phones**: `value`, `type` (mobile, home, work, other)
- **Organizations**: `name`, `title`
- **Birthdays**: `year`, `month`, `day`
- **Addresses**: `street`, `city`, `state`, `zip`, `country`, `type`
- **Notes**: Free-form text for additional information
- **URLs**: Website URLs with type classification

## Workflow Patterns

### Finding Contact Information

```bash
# 1. Search for contact
SEARCH_RESULT=$(contacts_manager.rb --search "John Smith")

# 2. Extract resource name from results
RESOURCE_NAME=$(echo $SEARCH_RESULT | jq -r '.contacts[0].resource_name')

# 3. Get full details
contacts_manager.rb --get "$RESOURCE_NAME"
```

### Creating Contact from Name

When user provides just a name, create minimal contact:

```bash
contacts_manager.rb --create '{
  "name": {
    "given_name": "FirstName",
    "family_name": "LastName",
    "display_name": "FirstName LastName"
  }
}'
```

Then update with additional information as provided.

### Bulk Updates

For updating multiple contacts, search first, then update each:

```bash
# Find all contacts at company
contacts_manager.rb --search "Acme Corp" > contacts.json

# Process each contact (example in shell)
cat contacts.json | jq -r '.contacts[].resource_name' | while read resource; do
  contacts_manager.rb --update "$resource" \
    --update-data '{"organization":{"name":"Acme Corporation"}}' \
    --update-mask "organizations"
done
```

### Integration with Calendar Skill

Since both skills share authentication, they work seamlessly together:

```bash
# Use calendar skill to find meeting attendees
calendar_manager.rb --list-events

# Add attendee to contacts
contacts_manager.rb --create '{"name":{...}, "emails":[...]}'

# Update contact with meeting notes
contacts_manager.rb --update "people/c123" \
  --update-data '{"notes":"Met at Q1 planning meeting"}' \
  --update-mask "biographies"
```

## Error Handling

The script returns JSON with status and error details:

```json
{
  "status": "error",
  "code": "AUTH_ERROR|API_ERROR|INVALID_ARGS",
  "message": "Detailed error message"
}
```

**Exit Codes**:
- `0` - Success
- `1` - Operation failed
- `2` - Authentication error
- `3` - API error
- `4` - Invalid arguments

## Common Use Cases

### Email Skill Integration

The contacts skill complements the email skill by providing contact lookup:

```bash
# Find contact email
EMAIL=$(contacts_manager.rb --search "Rob" | jq -r '.contacts[0].emails[0].value')

# Use with email skill
~/.claude/skills/email/SKILL.md "Send Rob a message about the project"
```

### Contact Deduplication

```bash
# List all contacts
contacts_manager.rb --list > all_contacts.json

# Process to find duplicates (requires custom logic)
# Then delete duplicates
contacts_manager.rb --delete "people/c123"
```

### Birthday Reminders

```bash
# Search contacts with birthdays
contacts_manager.rb --list | jq '.contacts[] | select(.birthday != null)'

# Add birthday to contact
contacts_manager.rb --update "people/c123" \
  --update-data '{"birthday":{"month":5,"day":15}}' \
  --update-mask "birthdays"
```

## Best Practices

1. **Search Before Create**: Always search to avoid duplicates
2. **Use Resource Names**: Store resource names for quick access to frequently used contacts
3. **Minimal Creates**: Create contacts with minimal info, update with details later
4. **Careful Deletes**: Double-check before deleting - it's permanent
5. **Batch Operations**: Use pagination for large contact lists
6. **Update Masks**: Always specify update mask to avoid overwriting unintended fields
7. **Error Handling**: Check JSON status field before processing results

## Troubleshooting

### Authentication Issues

```bash
# Re-authorize if token invalid
rm ~/.claude/.google/token.json
contacts_manager.rb --list
```

### Scope Errors

If you see scope-related errors, ensure the token has the full contacts scope:

```bash
# Check current scopes
cat ~/.claude/.google/token.json | jq -r '.default' | jq -r '.scope'

# Should include: https://www.googleapis.com/auth/contacts
```

### API Quota Limits

Google Contacts API has rate limits. If you hit quota:
- Wait a few minutes before retrying
- Reduce page size for list operations
- Batch updates efficiently

## Script Version

Current version: 1.0.0

Run `contacts_manager.rb --version` to check installed version.
