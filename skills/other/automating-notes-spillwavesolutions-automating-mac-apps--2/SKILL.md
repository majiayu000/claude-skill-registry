---
name: automating-notes
description: Automates Apple Notes via JXA. Use when asked to "create notes programmatically", "automate Notes app", "JXA notes scripting", or "organize notes with automation". Covers accounts/folders/notes, HTML bodies, queries, moves, and Objective-C/UI fallbacks for Notes.app automation on macOS.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Apple Notes (JXA-first, AppleScript discovery)

## Relationship to the macOS automation skill
- Standalone for Notes; reuse `automating-mac-apps` for permissions, shell, and Objective-C/UI scripting patterns.
- **PyXA Installation:** To use PyXA examples in this skill, see the installation instructions in `automating-mac-apps` skill (PyXA Installation section).

## Core framing
- Notes uses an AEOM hierarchy: Application → Accounts → Folders → Notes (with nested folders).
- **Load:** `automating-notes/references/notes-basics.md` for complete specifier reference.

## Workflow (default)
1) Resolve account/folder explicitly (iCloud vs On My Mac); validate existence and permissions.
2) Ensure target path exists (create folders if needed); handle creation failures gracefully.
3) Create notes with explicit `name` and HTML `body`; verify creation success.
4) Query/update with `.whose` filters; batch delete/move as needed; check counts before/after operations.
5) For checklists/attachments, use clipboard/Objective-C scripting if dictionary support is insufficient; test fallbacks.
6) For meeting/people workflows, file notes under `meetings/<company>/<date>-<meeting-title>` and `people/<first>-<last>/...`; validate final structure.

## Quickstart (ensure path + create)

**JXA (Legacy):**
```javascript
const Notes = Application("Notes");

// Ensure folder path exists, creating intermediate folders as needed
function ensurePath(acc, path) {
  const parts = path.split("/").filter(Boolean);
  let container = acc;
  parts.forEach(seg => {
    let f; try {
      f = container.folders.byName(seg);
      f.name(); // Verify access
    } catch (e) {
      // Folder doesn't exist, create it
      f = Notes.Folder({ name: seg });
      container.folders.push(f);
    }
    container = f;
  });
  return container;
}

try {
  // Get iCloud account and ensure meeting folder exists
  const acc = Notes.accounts.byName("iCloud");
  const folder = ensurePath(acc, "meetings/Acme/2024-07-01-Review");

  // Create new note in the folder
  folder.notes.push(Notes.Note({
    name: "Client Review",
    body: "<h1>Client Review</h1><div>Agenda...</div>"
  }));
  console.log("Note created successfully");
} catch (e) {
  console.error("Failed to create note: " + e.message);
}
```

**PyXA (Recommended Modern Approach):**
```python
import PyXA

notes = PyXA.Notes()

def ensure_path(account, path):
    """Ensure folder path exists, creating intermediate folders as needed"""
    parts = [p for p in path.split("/") if p]  # Filter empty parts
    container = account

    for part in parts:
        try:
            # Try to find existing folder
            folder = container.folders().by_name(part)
            folder.name()  # Verify access
        except:
            # Folder doesn't exist, create it
            folder = notes.make("folder", {"name": part})
            container.folders().push(folder)

        container = folder

    return container

try:
    # Get iCloud account
    account = notes.accounts().by_name("iCloud")

    # Ensure meeting folder exists
    folder = ensure_path(account, "meetings/Acme/2024-07-01-Review")

    # Create new note in the folder
    note = folder.notes().push({
        "name": "Client Review",
        "body": "<h1>Client Review</h1><div>Agenda...</div>"
    })

    print("Note created successfully")

except Exception as e:
    print(f"Failed to create note: {e}")
```

**PyObjC with Scripting Bridge:**
```python
from ScriptingBridge import SBApplication

notes = SBApplication.applicationWithBundleIdentifier_("com.apple.Notes")

def ensure_path(account, path):
    """Ensure folder path exists, creating intermediate folders as needed"""
    parts = [p for p in path.split("/") if p]
    container = account

    for part in parts:
        try:
            folder = container.folders().objectWithName_(part)
            folder.name()  # Verify access
        except:
            # Create new folder
            folder = notes.classForScriptingClass_("folder").alloc().init()
            folder.setName_(part)
            container.folders().addObject_(folder)

        container = folder

    return container

try:
    # Get iCloud account
    accounts = notes.accounts()
    account = None
    for acc in accounts:
        if acc.name() == "iCloud":
            account = acc
            break

    if account:
        # Ensure meeting folder exists
        folder = ensure_path(account, "meetings/Acme/2024-07-01-Review")

        # Create new note
        note = notes.classForScriptingClass_("note").alloc().init()
        note.setName_("Client Review")
        note.setBody_("<h1>Client Review</h1><div>Agenda...</div>")

        folder.notes().addObject_(note)

        print("Note created successfully")
    else:
        print("iCloud account not found")

except Exception as e:
    print(f"Failed to create note: {e}")
```

## Validation Checklist
- [ ] Account access works (iCloud vs On My Mac)
- [ ] Folder creation and path resolution succeeds
- [ ] Note creation with valid HTML body completes
- [ ] Note appears in Notes UI
- [ ] `.whose` queries return expected results
- [ ] Error handling covers missing accounts/folders

## HTML & fallbacks
- Allowed tags: `<h1>-<h3>`, `<b>`, `<i>`, `<u>`, `<ul>/<ol>/<li>`, `<div>/<p>/<br>`, `<a>`.
- **Security:** Always sanitize HTML input; avoid `<script>`, `<style>`, or event handlers to prevent XSS in rendered notes.
- Checklists/attachments: Objective-C/clipboard fallback (Cmd+Shift+L for checklist, paste image via NSPasteboard + System Events).
- Append helper: replace `</body>` with extra HTML, or append when missing; validate HTML structure post-modification.

## When Not to Use
- Cross-platform note taking (use Notion API, Obsidian, or Markdown files)
- iCloud sync operations requiring status feedback (limited API support)
- Non-macOS platforms
- Rich formatting beyond supported HTML tags
- Collaborative editing workflows (no multi-user support)

## What to load
- Basics & specifiers: `automating-notes/references/notes-basics.md`
- Recipes (create/move/query/ensure path/checklists): `automating-notes/references/notes-recipes.md`
- Advanced (HTML body rules, attachments/UI, JSON import/export, ObjC bridge): `automating-notes/references/notes-advanced.md`
- Dictionary/type map: `automating-notes/references/notes-dictionary.md`
- **PyXA API Reference** (complete class/method docs): `automating-notes/references/notes-pyxa-api-reference.md`