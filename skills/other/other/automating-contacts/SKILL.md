---
name: automating-contacts
description: Automates macOS Contacts via JXA with AppleScript dictionary discovery. Use when asked to "automate contacts", "JXA contacts automation", "macOS address book scripting", "AppleScript contacts", or "Contacts app automation". Covers querying, CRUD, multi-value fields, groups, images, and ObjC bridge fallbacks.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Contacts (JXA-first, AppleScript discovery)

## Relationship to Other Skills
- **Standalone for Contacts:** Use this skill for Contacts-specific operations (querying, CRUD, groups).
- **Reuse `automating-mac-apps` for:** TCC permissions setup, shell command helpers, UI scripting fallbacks, and ObjC bridge patterns.
- **Integration:** Load both skills when combining Contacts automation with broader macOS scripting.
- **PyXA Installation:** To use PyXA examples in this skill, see the installation instructions in `automating-mac-apps` skill (PyXA Installation section).

## Core Framing
- Contacts dictionary is AppleScript-first; discover there, implement in JXA
- Object specifiers: read with methods (`name()`, `emails()`), write with assignments
- Multi-value fields (emails, phones, addresses) are elements; use constructor + `.push()`
- Group membership: `add ... to` command or `.people.push`; handle duplicates defensively
- TCC permissions required: running host must have Contacts access

## Workflow (default)
1) Inspect the Contacts dictionary in Script Editor (JavaScript view).
2) Prototype minimal AppleScript to validate verbs; port to JXA with specifier reads/writes.
3) Use `.whose` for coarse filtering; fall back to hybrid (coarse filter + JS refine) when needed.
4) Create records with proxy + `make`, then assign primitives and push multi-values; `Contacts.save()` to persist.
5) Verify persistence: check `person.id()` exists after save; handle TCC permission errors.
6) Manage groups after person creation; guard against duplicate membership with existence checks.
7) For photos or broken bridges, use ObjC/clipboard fallback; for heavy queries, batch read or pre-filter.
8) Test operations: run→check results→fix errors in iterative loop.

### Validation Checklist
- [ ] Contacts permissions granted (System Settings > Privacy & Security > Contacts)
- [ ] Dictionary inspected and verbs validated in Script Editor
- [ ] AppleScript prototype runs without errors
- [ ] JXA port handles specifiers correctly
- [ ] Multi-value fields pushed to arrays properly
- [ ] Groups existence checked before creation
- [ ] Operations saved and verified with `.id()` checks
- [ ] Error handling wraps all operations

## Quickstart (upsert + group)
```javascript
const Contacts = Application("Contacts");
const email = "ada@example.com";
try {
  const existing = Contacts.people.whose({ emails: { value: { _equals: email } } })();
  const person = existing.length ? existing[0] : Contacts.Person().make();
  person.firstName = "Ada";
  person.lastName = "Lovelace";
  
  // Handle multi-value email
  const work = Contacts.Email({ label: "Work", value: email });
  person.emails.push(work);
  Contacts.save();
  
  // Handle groups with error checking
  let grp;
  try { 
    grp = Contacts.groups.byName("VIP"); 
    grp.name(); // Verify exists
  } catch (e) {
    grp = Contacts.Group().make(); 
    grp.name = "VIP";
  }
  Contacts.add(person, { to: grp });
  Contacts.save();
  console.log("Contact upserted successfully");
} catch (error) {
  console.error("Contacts operation failed:", error);
}
```

## Pitfalls
- **TCC Permissions**: Photos/attachments require TCC + Accessibility; use clipboard fallback if blocked
- **Yearless birthdays**: Not cleanly scriptable; use full dates
- **Advanced triggers**: Delegate geofencing to Shortcuts app
- **Heavy queries**: Batch read or pre-filter to avoid timeouts

## When Not to Use
- Non-macOS platforms (use platform-specific APIs)
- Simple AppleScript-only solutions (skip JXA complexity)
- iCloud sync operations (use native Contacts framework)
- User-facing apps (use native Contacts framework)
- Cross-platform contact management (use CardDAV or vCard APIs)

## What to load
- JXA basics & specifiers: `automating-contacts/references/contacts-basics.md`
- Recipes (query, create, multi-values, groups): `automating-contacts/references/contacts-recipes.md`
- Advanced (hybrid filters, clipboard image, TCC, date pitfalls): `automating-contacts/references/contacts-advanced.md`
- Dictionary & type map: `automating-contacts/references/contacts-dictionary.md`
- **PyXA API Reference** (complete class/method docs): `automating-contacts/references/contacts-pyxa-api-reference.md`