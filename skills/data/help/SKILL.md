---
name: help
description: Show available skills, common workflows, and quick reference
model: claude-haiku-4-5-20251001
allowed-tools: []
---

## bitwize-music Plugin Help

Display this help information to the user in a clear, organized format.

---

### Getting Started

**New to the plugin?**
- `/bitwize-music:tutorial` - Interactive guided album creation
- `/bitwize-music:configure` - Set up configuration file
- `/bitwize-music:about` - About bitwize and this plugin

**Resume existing work:**
- `/bitwize-music:resume <album-name>` - Find an album and see status/next steps

---

### Skills by Category

**Album & Track Creation**
- `/bitwize-music:album-ideas` - Track and manage album ideas
- `/bitwize-music:new-album` - Create new album with directory structure
- `/bitwize-music:album-conceptualizer` - Album concepts and tracklist architecture
- `/bitwize-music:lyric-writer` - Write/review lyrics, fix prosody
- `/bitwize-music:suno-engineer` - Technical Suno prompting and genre selection

**Research & Sources**
- `/bitwize-music:researcher` - Main research coordinator, fact-checking
- `/bitwize-music:document-hunter` - Automated document search/download
- `/bitwize-music:researchers-legal` - Court documents, indictments
- `/bitwize-music:researchers-gov` - DOJ/FBI/SEC releases
- `/bitwize-music:researchers-tech` - Project histories, changelogs
- `/bitwize-music:researchers-journalism` - Investigative articles
- `/bitwize-music:researchers-security` - Malware analysis, CVEs
- `/bitwize-music:researchers-financial` - SEC filings, market data
- `/bitwize-music:researchers-historical` - Archives, timelines
- `/bitwize-music:researchers-biographical` - Personal backgrounds
- `/bitwize-music:researchers-primary-source` - Tweets, blogs, forums
- `/bitwize-music:researchers-verifier` - Quality control, citation validation

**Quality Control**
- `/bitwize-music:lyric-reviewer` - Pre-generation QC gate (9-point checklist)
- `/bitwize-music:pronunciation-specialist` - Scan for pronunciation risks
- `/bitwize-music:explicit-checker` - Verify explicit content flags
- `/bitwize-music:validate-album` - Validate album structure and paths

**Production & Release**
- `/bitwize-music:album-art-director` - Visual concepts and AI art prompts
- `/bitwize-music:mastering-engineer` - Audio mastering guidance
- `/bitwize-music:promo-director` - Generate promo videos for social media
- `/bitwize-music:cloud-uploader` - Upload promo videos to Cloudflare R2 or AWS S3
- `/bitwize-music:sheet-music-publisher` - Convert audio to sheet music
- `/bitwize-music:release-director` - Release coordination and distribution

**File Management**
- `/bitwize-music:import-track` - Move track .md files to album location
- `/bitwize-music:import-audio` - Move audio files to album location
- `/bitwize-music:import-art` - Place album art in correct locations
- `/bitwize-music:clipboard` - Copy track lyrics/prompts to clipboard

**System & Maintenance**
- `/bitwize-music:configure` - Edit plugin configuration
- `/bitwize-music:test` - Run automated tests
- `/bitwize-music:skill-model-updater` - Update model references in skills
- `/bitwize-music:help` - Show this help (you are here!)
- `/bitwize-music:about` - About bitwize and the plugin

---

### Common Workflows

**Creating a New Album:**
1. `/bitwize-music:new-album <name> <genre>` - Create structure
2. Answer the 7 planning phases (concept, sonic direction, etc.)
3. Write lyrics for each track
4. Run `/bitwize-music:lyric-reviewer` before generation
5. Generate in Suno, log results
6. Master audio with `/bitwize-music:mastering-engineer`
7. [Optional] Generate promo videos with `/bitwize-music:promo-director`
8. [Optional] Upload to cloud with `/bitwize-music:cloud-uploader`
9. Release with `/bitwize-music:release-director`

**True-Story Albums (with research):**
1. Use researcher skills to gather sources
2. All sources must be verified by human before production
3. Update track status from `❌ Pending` to `✅ Verified (DATE)`
4. Then proceed with lyric writing and generation

**Resume Existing Work:**
1. `/bitwize-music:resume <album-name>` - Get detailed status
2. Follow the recommended next steps

---

### Quick Tips

- **Config file:** `~/.bitwize-music/config.yaml` (always read this for paths)
- **Pronunciation:** Use phonetic spelling for tricky words (see pronunciation guide)
- **Explicit content:** Use flag for: fuck, shit, bitch, cunt, cock, dick, pussy, etc.
- **Mastering target:** -14 LUFS, -1.0 dBTP for streaming platforms
- **Promo videos:** Generate after mastering, 15s vertical (9:16) for social media
- **Track status flow:** Not Started → In Progress → Generated → Final
- **Album status flow:** Concept → In Progress → Complete → Released

---

### Key Documentation

- **CLAUDE.md** - Main workflow instructions
- **README.md** - Project overview
- `/reference/suno/` - Suno V5 guides, pronunciation, tips
- `/reference/workflows/` - Detailed workflow procedures
- `/reference/mastering/` - Audio mastering documentation
- `/templates/` - Templates for new content
- `/skills/[skill-name]/SKILL.md` - Individual skill documentation

---

### Getting Help

- Use this skill anytime: `/bitwize-music:help`
- For tutorial: `/bitwize-music:tutorial`
- For status: `/bitwize-music:resume <album-name>`
- Ask Claude: "What should I do next?" for guidance
