---
name: file-placement
description: Enforces ZERO TOLERANCE file placement rules for documentation and scripts. Use when (1) Creating any .md file, (2) Creating any .sh script, (3) Organizing documentation, (4) Writing guides or reports, (5) Adding utility scripts. CRITICAL RULES - NEVER create .md files in root directories (except README.md, CLAUDE.md), NEVER create .sh scripts in backend (except start.sh), ALL documentation goes in docs/ subfolders, ALL scripts go in scripts/ folder.
---

# File Placement Rules

## 🚨 ZERO TOLERANCE FILE PLACEMENT 🚨

### STRICT RULES

* ❌ **FORBIDDEN:** Creating .md files in `/Users/aideveloper/core/` (except README.md, CLAUDE.md)
* ❌ **FORBIDDEN:** Creating .md files in `/Users/aideveloper/core/src/backend/` (except README.md)
* ❌ **FORBIDDEN:** Creating .md files in `/Users/aideveloper/core/AINative-website/` (except README.md, CLAUDE.md)
* ❌ **FORBIDDEN:** Creating scripts (.sh) in `/Users/aideveloper/core/src/backend/` (except start.sh)

### REQUIRED LOCATIONS

## Backend Documentation → `/Users/aideveloper/core/docs/`

* **Issues/Bugs:** `docs/issues/ISSUE_*.md`, `docs/issues/BUG_*.md`, `docs/issues/ROOT_CAUSE_*.md`
* **Testing/QA:** `docs/testing/*_TEST*.md`, `docs/testing/QA_*.md`
* **Agent Swarm:** `docs/agent-swarm/AGENT_SWARM_*.md`, `docs/agent-swarm/WORKFLOW_*.md`, `docs/agent-swarm/STAGE_*.md`
* **API Documentation:** `docs/api/API_*.md`, `docs/api/*_ENDPOINTS*.md`
* **Implementation Reports:** `docs/reports/*_IMPLEMENTATION*.md`, `docs/reports/*_SUMMARY.md`
* **Deployment:** `docs/deployment/DEPLOYMENT_*.md`, `docs/deployment/RAILWAY_*.md`
* **Quick References:** `docs/quick-reference/*_QUICK_*.md`, `docs/quick-reference/*_REFERENCE.md`, `docs/quick-reference/STEPS_*.md`
* **Backend Features:** `docs/backend/RLHF_*.md`, `docs/backend/MEMORY_*.md`, `docs/backend/SECURITY_*.md`
* **Development Guides:** `docs/development-guides/CODING_*.md`, `docs/development-guides/*_GUIDE.md`, `docs/guides/*_INSTRUCTIONS.md`
* **Planning:** `docs/planning/PRD_*.md`, `docs/planning/BACKLOG*.md`

## Frontend Documentation → `/Users/aideveloper/core/AINative-website/docs/`

* **Frontend Features:** `AINative-website/docs/features/`
* **Frontend Testing:** `AINative-website/docs/testing/`
* **Frontend Implementation:** `AINative-website/docs/implementation/`
* **Frontend Issues:** `AINative-website/docs/issues/`
* **Frontend Deployment:** `AINative-website/docs/deployment/`
* **Frontend Reports:** `AINative-website/docs/reports/`

## Scripts → `/Users/aideveloper/core/scripts/`

* **ALL test scripts:** `scripts/test_*.sh`
* **ALL migration scripts:** `scripts/*_migration.sh`
* **ALL monitoring scripts:** `scripts/monitor_*.sh`
* **ALL utility scripts:** `scripts/*.sh`

## ENFORCEMENT WORKFLOW

Before creating ANY .md file or .sh script, you MUST:

1. ✅ Check if you're creating it in a root directory
2. ✅ If yes, STOP and use the appropriate docs/ or scripts/ subfolder
3. ✅ Choose the correct category based on filename patterns above
4. ✅ Create in the correct location FIRST TIME, not in root then move later

## VIOLATION CONSEQUENCES

Creating documentation in root directories causes:

* Project clutter and disorganization
* Wasted time reorganizing files
* Inconsistent documentation structure
* Developer frustration
* Loss of findability for important docs

**THIS IS A ZERO-TOLERANCE RULE. ALWAYS use docs/ or scripts/ subfolders.**

## Reference Files

See `references/directory-mapping.md` for complete mapping table of filename patterns to required directory locations.
