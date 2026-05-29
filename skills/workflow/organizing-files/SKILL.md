---
name: organizing-files
description: Organizes macOS files across Desktop, Documents, Downloads, and iCloud Drive into a consistent structure. Use when the user asks to organize files, clean up folders, sort downloads, declutter desktop, tidy up documents, or structure their filesystem. Triggers on "organize", "clean up", "sort files", "declutter", "file mess", "tidy", or any request about file/folder structure on macOS.
---

# Organizing Files

## Overview

**Every file has a home. Find it, move it, never delete it.** This skill enforces a consistent macOS file organization structure across Desktop, Documents, Downloads, and iCloud Drive — optimized for software engineers who also have personal documents, media, and credentials scattered around.

## Principles

1. **No deletions** — move files, never remove them
2. **iCloud Documents = central hub** — organized subfolders, backed up automatically
3. **Desktop = clean workspace** — only actively-used files
4. **Downloads = temporary inbox** — local-only, clear regularly into Documents
5. **Git repos stay local** — `~/dev/` must never be inside iCloud (sync breaks `.git`, `node_modules`)
6. **Sensitive files get isolated** — credentials, recovery codes, identity docs in dedicated folders
7. **Inspect before sorting** — read images, check EXIF/metadata, understand content before categorizing

## Phase 1: Explore

Before moving anything, understand what exists. Launch parallel exploration agents:

| Agent | Target | Purpose |
|-------|--------|---------|
| 1 | `~/Desktop/` | File types, sizes, screen recordings vs docs |
| 2 | `~/Documents/` | Current structure, migration folders, images |
| 3 | `~/Downloads/` | File type breakdown, duplicates, installers |
| 4 | iCloud Drive root | Loose files, subfolders, empty folders |
| 5 | `~/dev/` | Confirm git repos are local, not in iCloud |

Check iCloud sync status:
- `stat ~/Desktop` and `stat ~/Documents` — check if symlinked to iCloud
- `brctl status` — check iCloud sync daemon
- Look for migration folders (`Desktop - <Mac Name>`, `Documents - <Mac Name>`)

**iCloud path mapping:** When iCloud Desktop & Documents is enabled, `~/Desktop` and `~/Documents` point to iCloud Drive. The iCloud Drive root is at `~/Library/Mobile Documents/com~apple~CloudDocs/`. Files at that root are separate from Desktop/Documents — they're loose files in the drive itself.

## Phase 2: Inspect Content

**Don't sort by filename alone.** Inspect actual content. Each exploration agent must visually read images and check metadata:

| File Type | Inspection Method |
|-----------|-------------------|
| Images (.jpg, .png, .heic) | **Read the image file visually** (Claude can see images) to understand what it shows — is it a headshot, org chart, screenshot, meme, stock photo, or personal photo? Then `mdls` for EXIF (camera, GPS, dimensions, date) |
| PDFs | `mdls` for author, page count, title, creation date, security/encryption. Read small PDFs to understand content. |
| Spreadsheets (.xlsx, .csv) | `head -2` for CSV headers, `mdls` for author/dates |
| Code files (.ts, .tsx, .py) | `head -10` to understand purpose |
| Videos (.mov, .mp4) | `mdls` for duration, resolution, codec, creation date |
| Audio (.mp3, .m4a) | `mdls` for title, artist, duration |
| Hidden files (.*) | Check for dotfiles — config files, secrets, system files. Include in exploration. |

**Visual image inspection is critical.** Filenames like `IMG_6284.jpg` or `20991151.jpg` tell you nothing. Reading the image reveals whether it's a wedding invitation, a stock photo for a website, an office selfie, or a screenshot of credentials. Always read images with the Read tool.

**Flag these immediately:**
- Files with GPS coordinates embedded (privacy risk)
- Credential files (AWS keys, recovery codes, passwords)
- Password-protected/encrypted documents
- Identity documents (ID cards, driver's licenses, passports)
- Symlinks pointing to external drives or other locations — don't move these, note them

## Phase 3: Plan the Structure

### Target Folder Tree

```
~/Documents/                          # iCloud-synced central hub
├── Personal/
│   ├── Identity/                     # ID docs, driver's license, passports
│   ├── Financial/                    # Tax, salary, stock, receipts, invoices
│   ├── Legal/                        # Contracts, agreements, leases
│   ├── Medical/                      # Health records, insurance
│   ├── Travel/                       # Bookings, itineraries, travel insurance
│   ├── Orders/                       # Online order receipts
│   └── Resumes/
│       ├── Mine/                     # Own resume versions
│       └── Others/                   # Candidates' CVs
│
├── Work/
│   ├── <Company>/                    # Primary company folder
│   │   ├── Exports/                  # Data exports, reports
│   │   ├── Analytics/                # Query results, usage data
│   │   ├── Screenshots/              # App screenshots, org charts
│   │   ├── Feature Demos/            # Named demo videos
│   │   └── HR/                       # HR surveys, research
│   ├── <Previous Company>/           # Old employer docs
│   ├── Documentation/                # Technical docs, blog posts, meeting notes
│   └── Job Descriptions/             # JDs for hiring
│
├── Media/
│   ├── Photos/
│   │   ├── Headshots/                # Professional photos + variants
│   │   ├── DSLR/                     # Camera photos by shoot
│   │   └── Personal/                 # Phone photos, misc images
│   ├── Logos & Branding/             # Company logos, SVGs, design assets
│   ├── AI Generated/                 # Midjourney, DALL-E, Gemini outputs
│   ├── GIFs & Memes/                 # Animated GIFs, reaction images, slackmojis
│   ├── Audio/                        # Music, voice recordings
│   ├── Screen Recordings/            # Generic recordings, by month
│   │   ├── YYYY-MM/                  # Organized by year-month
│   │   └── ...
│   └── Videos/                       # Other video files
│
├── Technical/
│   ├── 3D Printing/                  # GCODE, STEP, STL files
│   ├── Code Snippets/                # Loose .ts, .tsx, .py files
│   ├── Config Backups/               # TablePlus, keybindings, dotfiles
│   └── Design Files/                 # PSD, Figma exports
│
├── Sensitive/                        # Credentials and recovery files
│   ├── Recovery Codes/               # Browser, VPN, 2FA recovery
│   └── Cloud Credentials/            # AWS, GCP, etc.
│
└── Archive/
    ├── Installers/                   # DMG, PKG, ZIP app installers
    ├── Old Backups/                  # Device backups, PST archives
    ├── Old Firmware/                 # Router firmware, device updates
    └── Misc/                         # UUID-named files, unknown docs, logs
```

### Desktop — Keep Empty

Move everything off Desktop into the structure above. Desktop is a workspace, not storage.

### Downloads — Clear Into Documents

Everything in Downloads should be sorted into `~/Documents/` subfolders. Downloads is a temporary landing zone.

### iCloud Root — No Loose Files

All loose files at iCloud Drive root move into `~/Documents/` subfolders. Only system symlinks (Desktop, Documents) should remain at root.

## Phase 4: Execute

### Execution Order

1. Create all target directories with `mkdir -p`
2. Move iCloud root loose files → Documents subfolders
3. Move iCloud subfolder contents → Documents subfolders
4. Flatten migration folders (`Desktop - <Mac Name>`, `Documents - <Mac Name>`) → Documents
5. Move Downloads files → Documents subfolders
6. Handle duplicates — keep both, rename with date suffix: `file (2025-12-15).ext`
7. Verify all moves completed

### Duplicate Handling

When the same filename exists in multiple locations:

```bash
# Keep both, rename the duplicate with its modification date
mv "duplicate.pdf" "duplicate (2025-12-15).pdf"
```

Never overwrite. Never delete. Always preserve both copies.

### Sensitive Files

After moving credentials to `Sensitive/`, remind the user:
- AWS keys should live in a password manager, not the filesystem
- Recovery code images should be encrypted or vault-stored
- GPS-tagged photos should be stripped before sharing publicly

## Phase 5: Verify

After all moves:

1. `ls ~/Desktop/` — should be empty or near-empty
2. `ls ~/Downloads/` — should be empty (existing files moved)
3. `find ~/Documents/ -maxdepth 2 -type d | sort` — verify folder tree
4. Check for any files left behind in iCloud root
5. Count files per category — sanity check totals match original counts

## Red Flags — STOP

| Thought | Action |
|---------|--------|
| "I'll sort by extension/filename" | INSPECT CONTENT — read images visually, check metadata, peek at CSVs. A .pdf could be financial or junk. |
| "I'll delete these old installers" | NO DELETIONS — move to Archive/Installers/ |
| "Git repos should be in Documents" | NEVER — ~/dev stays local, outside iCloud |
| "I'll merge these duplicates" | KEEP BOTH — rename with date suffix |
| "Credentials are fine in Documents" | ISOLATE in Sensitive/ folder, warn user |
| "I'll organize Downloads later" | DO IT NOW — Downloads is the biggest mess |
| "Desktop needs some files on it" | EMPTY IT — Desktop is a workspace, not storage |

## Anti-Patterns

**Extension-only sorting:** Moving all `.pdf` to one folder ignores that PDFs span financial docs, identity docs, resumes, and junk. Always inspect content.

**Flat category folders:** Don't dump 50 spreadsheets into one folder. Use subcategories (`Exports/`, `Analytics/`, `HR/`).

**Ignoring iCloud root:** Users forget iCloud Drive root has its own loose files separate from Desktop/Documents. Always check it.

**Skipping metadata:** EXIF data reveals GPS coordinates (privacy risk), camera models (helps identify photo sources), and creation dates (helps determine if files are current or archival).

**Moving git repos to iCloud:** iCloud sync corrupts `.git` directories and creates conflicts with `node_modules`, `__pycache__`, and other generated files. Development repos must stay local.
