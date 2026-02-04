---
name: agnosticv:catalog-builder
description: Create or update AgnosticV catalog files (common.yaml, dev.yaml, description.adoc, info-message-template.adoc)
---

---
context: main
model: sonnet
---

# Skill: agnosticv-catalog-builder

**Name:** AgnosticV Catalog Builder
**Description:** Create or update AgnosticV catalog files for RHDP deployments
**Version:** 2.1.0
**Last Updated:** 2026-02-03

---

## ⚠️ CRITICAL: Keep Questions Simple and Direct

**When asking for paths, URLs, or locations:**
- Just ask for the path or URL directly
- DO NOT ask about GitHub organizations, root folders, subdirectories, or try to find/detect them
- DO NOT offer multiple options to search or auto-detect
- Accept exactly what the user provides - don't try to be smart about it

**Example of what NOT to do:**
```
❌ Which GitHub organization? (rhpds / redhat-scholars / Other)
❌ Should I auto-detect your catalog directory? [Y/n]
❌ Which subdirectory should I use?
```

**Example of what TO do:**
```
✅ What is the URL or path to your Showroom repository?
✅ What is the path to the catalog/CI directory?
```

Just ask, use what they give you, move on. Users know their paths - trust them.

---

## Purpose

Unified skill for creating and updating AgnosticV catalog configurations. Handles everything from full catalog creation to updating individual files like description.adoc or info-message-template.adoc.

## Workflow Diagram

![Workflow](workflow.svg)

## What You'll Need Before Starting

Have these ready before running this skill:

**Choose your mode first:**
1. **Full Catalog** - Creating complete new catalog
2. **Description Only** - Just updating description.adoc
3. **Info Message Template** - Creating info-message-template.adoc
4. **Virtual CI** - Creating published/ Virtual CI

**For Full Catalog mode:**
- 📁 **AgnosticV repo path** - Where your local AgnosticV repository is (e.g., `~/work/code/agnosticv`)
- 🏢 **Catalog details**:
  - Display name (appears in RHDP UI)
  - Short name (directory name, lowercase with hyphens)
  - Brief description (1-2 sentences)
  - Category (workshop, demo, integration, etc.)
- 🔧 **Infrastructure choices**:
  - Cloud provider (AWS, Azure, OpenShift CNV, None)
  - Sandbox architecture (single-node, multi-node)
  - Workloads needed (which ocp4_workload_* roles)
- 🔗 **Showroom URL** (optional) - Link to your workshop/demo repository

**For Description Only mode:**
- 📁 **Showroom path or URL** - Where your workshop content is
- 📁 **Catalog directory path** - Where to save description.adoc
- 📋 **Module content** - Completed Showroom modules to extract from

**For Info Message Template:**
- 📁 **Catalog path** - Path to existing AgV catalog
- 📊 **User data keys** - List of data your workload shares via agnosticd_user_info

**For Virtual CI:**
- 📁 **Base component path** - Existing component to create Virtual CI from
- 🏷️ **Naming** - Virtual CI folder name (must be unique)

**Access needed:**
- ✅ Write permissions to AgnosticV repository
- ✅ Git configured with SSH access to GitHub
- ✅ RHDP account with AgnosticV repository access

---

## When to Use This Skill

Use `/agnosticv-catalog-builder` when you need to:

- Create a complete new RHDP catalog item
- Generate just description.adoc from Showroom content
- Create info-message-template.adoc for user data display
- Update catalog files after Showroom content changes
- Set up infrastructure provisioning for workshops/demos

**Prerequisites:**
- RHDP account with AgnosticV repository access
- AgnosticV repository cloned locally (e.g., `~/work/code/agnosticv` or `~/devel/git/agnosticv`)
- Git configured with SSH access to GitHub
- For description generation: Showroom content in `content/modules/ROOT/pages/`

---

## Skill Workflow Overview

```
Step 0: Prerequisites & Scope Selection
  ↓
  ├─ Full Catalog → Steps 1-10 (infrastructure + all files)
  ├─ Description Only → Steps 1-3 (extract from Showroom)
  └─ Info Message Template → Steps 1-2 (user data template)
```

---

## Step 0: Prerequisites & Scope Selection (FIRST)

**CRITICAL:** Start by asking what the user wants to generate.

### Ask for Scope

```
🏗️  AgnosticV Catalog Builder

What would you like to create or update?

1. Full Catalog (common.yaml, dev.yaml, description.adoc, info-message-template.adoc)
   └─ For: New catalog from scratch with infrastructure setup

2. Description Only (description.adoc)
   └─ For: Generate/update description from Showroom content

3. Info Message Template (info-message-template.adoc)
   └─ For: Display user data from your workload CI

4. Create Virtual CI (published/ folder)
   └─ For: Create Virtual CI from existing base component

Your choice [1-4]:
```

### Get AgnosticV Repository Path

**Option C: Read from configuration files if present, otherwise ask**

Checks these locations in order:
1. `~/CLAUDE.md`
2. `~/claude/*.md`
3. `~/.claude/*.md`

```bash
# Check configuration files for AgV path (multiple locations)
agv_path=""

# Check ~/CLAUDE.md first
if [[ -f ~/CLAUDE.md ]]; then
  agv_path=$(grep -E "agnosticv.*:" ~/CLAUDE.md | grep -oE '(~|/)[^ ]+' | head -1)
fi

# Check ~/claude/*.md if not found
if [[ -z "$agv_path" ]]; then
  for file in ~/claude/*.md; do
    [[ -f "$file" ]] && agv_path=$(grep -E "agnosticv.*:" "$file" | grep -oE '(~|/)[^ ]+' | head -1)
    [[ -n "$agv_path" ]] && break
  done
fi

# Check ~/.claude/*.md if still not found
if [[ -z "$agv_path" ]]; then
  for file in ~/.claude/*.md; do
    [[ -f "$file" ]] && agv_path=$(grep -E "agnosticv.*:" "$file" | grep -oE '(~|/)[^ ]+' | head -1)
    [[ -n "$agv_path" ]] && break
  done
fi

# Expand tilde if present
[[ "$agv_path" =~ ^~ ]] && agv_path="${agv_path/#\~/$HOME}"
```

**If found in configuration:**
```
✓ Found AgV path in configuration: [path from configuration]

Proceeding with this path.
```

**If NOT found, ask:**
```
📂 AgnosticV Repository

Q: What is your AgnosticV repository directory path?
   (e.g., ~/work/code/agnosticv or ~/devel/git/agnosticv)

Your path:
```

**Validate path exists:**
```bash
# Expand tilde if present
[[ "$agv_path" =~ ^~ ]] && agv_path="${agv_path/#\~/$HOME}"

# Check directory exists
if [[ ! -d "$agv_path" ]]; then
  echo "✗ Directory not found: $agv_path"
  exit 1
fi

# Check if it's a git repo (warning only)
if [[ ! -d "$agv_path/.git" ]]; then
  echo "⚠️  Warning: Not a git repository"
fi

echo "✓ Using: $agv_path"
```

### Git Branch Selection

```bash
cd "$agv_path"

# Show current branch
current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
```

**Ask about branch:**
```
📍 I see you are working on branch: $current_branch

Q: Do you want to use this branch or should I create a new one?

1. Use current branch: $current_branch
2. Create new branch

Choice [1/2]:
```

**If user chooses 1 (Use current branch):**
```
✓ Using your current branch: $current_branch
```

**If user chooses 2 (Create new branch):**
```
Q: New branch name (e.g., add-my-catalog or update-description):
   (no 'feature/' prefix needed)

Branch name:
```

```bash
# Strip feature/ prefix if user added it
branch_name="${branch_name#feature/}"

# Create and switch to new branch
git checkout -b "$branch_name"

echo "✓ Created and switched to branch: $branch_name"
```

---

## MODE 1: Full Catalog Creation

**When selected:** User chose option 1 (Full Catalog)

### Step 1: Catalog Discovery (Search Existing)

Search for similar catalogs to learn from or use as reference.

```
📖 Catalog Discovery

Let me search for existing catalogs to help you.

Q: What keywords describe your catalog?
   (Examples: ansible, openshift ai, pipelines, gitops)

Keywords:
```

**Search logic:**
```bash
cd $AGV_PATH

# Search by keywords in:
# - Directory names
# - common.yaml display names
# - description.adoc content

find . -type f -name "common.yaml" | while read file; do
  dir=$(dirname "$file")
  name=$(grep "^name:" "$file" | cut -d':' -f2-)
  echo "$dir: $name"
done | grep -i "$keywords"
```

**Present results and ask:**
```
Found similar catalogs:

1. agd_v2/ansible-aap-workshop/
   └─ Ansible Automation Platform Self-Service

2. agd_v2/openshift-gitops-intro/
   └─ OpenShift GitOps Introduction

Do you want to:
A. Create new catalog from scratch
B. Use one as reference (copy structure)
C. Just browse and continue

Choice [A/B/C]:
```

### Step 2: Category Selection (REQUIRED)

```
📂 Category Selection

RHDP catalogs MUST have exactly one category:

1. Workshops - Multi-user hands-on learning with exercises
2. Demos - Single-user presenter-led demonstrations
3. Labs - General learning environments
4. Sandboxes - Self-service playground environments
5. Brand_Events - Events like Red Hat Summit, Red Hat One

Q: Which category? [1-5]:
```

**Validate:** Must be one of: `Workshops`, `Demos`, `Labs`, `Sandboxes`, `Brand_Events` (exact match)

**Important validation rules:**
- Workshops/Brand_Events → Must set multiuser: true
- Demos → Must set multiuser: false (single-user only)

### Step 3: UUID Generation (REQUIRED)

```
🔑 UUID Generation

Every catalog needs a unique RFC 4122 compliant UUID.

Generating UUID...
```

**Generate and validate:**
```bash
# Generate lowercase UUID
new_uuid=$(uuidgen | tr '[:upper:]' '[:lower:]')

# Check for collisions
echo "Generated: $new_uuid"
echo "Checking for collisions..."

# Search all common.yaml files
grep -r "asset_uuid: $new_uuid" $AGV_PATH/ --exclude-dir=.git

if [[ $? -eq 0 ]]; then
  echo "⚠️  Collision detected! Regenerating..."
  # Regenerate until unique
fi
```

### Step 4: Infrastructure Selection

```
🏗️  Infrastructure Selection

Choose your OpenShift deployment type:

1. CNV Multi-Node (Standard - Recommended for most)
   └─ Full OpenShift cluster on CNV pools
   └─ Best for: Multi-user workshops, complex workloads
   └─ Component: agd-v2/ocp-cluster-cnv-pools/prod

2. SNO (Single Node OpenShift)
   └─ Single-node cluster for lightweight demos
   └─ Best for: Quick demos, single-user environments, edge demos
   └─ Component: agd-v2/ocp-cluster-cnv-pools/prod (cluster_size: sno)

3. AWS (Cloud-based VMs)
   └─ VM-based deployment on AWS
   └─ Best for: GPU workloads, AWS-specific features, bastion-only demos
   └─ Component: Custom (requires bastion + instances configuration)

4. CNV VMs (Cloud VMs on CNV)
   └─ Virtual machines on CNV infrastructure
   └─ Best for: RHEL demos, edge appliances, non-OpenShift workloads
   └─ Component: Custom (cloud_provider: openshift_cnv, config: cloud-vms-base)

Q: Infrastructure choice [1-4]:
```

**Set configuration based on choice:**

1. **CNV Multi-Node:**
```yaml
config: openshift-workloads
cloud_provider: none
clusters:
  - default:
      api_url: "{{ openshift_api_url }}"
      api_token: "{{ openshift_cluster_admin_token }}"

__meta__:
  components:
    - name: openshift
      display_name: OpenShift Cluster
      item: agd-v2/ocp-cluster-cnv-pools/prod
      parameter_values:
        cluster_size: multinode
        host_ocp4_installer_version: "4.20"
        ocp4_fips_enable: false
        num_users: "{{ num_users }}"
```

2. **SNO:**
```yaml
config: openshift-workloads
cloud_provider: none
clusters:
  - default:
      api_url: "{{ openshift_api_url }}"
      api_token: "{{ openshift_cluster_admin_token }}"

__meta__:
  components:
    - name: openshift
      display_name: OpenShift Cluster
      item: agd-v2/ocp-cluster-cnv-pools/prod
      parameter_values:
        cluster_size: sno
        host_ocp4_installer_version: "4.20"
        ocp4_fips_enable: false
```

3. **AWS:**
```yaml
cloud_provider: aws
config: cloud-vms-base

# Define security groups and instances
security_groups:
  - name: BastionSG
    rules:
      - name: SSH
        from_port: 22
        to_port: 22
        protocol: tcp
        cidr: "0.0.0.0/0"
        rule_type: Ingress

instances:
  - name: bastion
    count: 1
    image: RHEL-10.0-GOLD-latest
    flavor:
      ec2: t3a.large
    security_groups:
      - BastionSG
```

4. **CNV VMs:**
```yaml
cloud_provider: openshift_cnv
config: cloud-vms-base

instances:
  - name: bastion
    count: 1
    image: rhel-9.6
    cores: 8
    memory: 16G
    image_size: 200Gi
```

### Step 5: Authentication Setup

```
🔐 Authentication Method

How should users authenticate to OpenShift?

1. htpasswd (Simple username/password - Most common)
   └─ Workload: agnosticd.core_workloads.ocp4_workload_authentication_htpasswd

2. Keycloak SSO (Enterprise authentication - For AAP/complex setups)
   └─ Workload: agnosticd.core_workloads.ocp4_workload_authentication_keycloak

Q: Authentication method [1-2]:
```

**Set workload based on choice:**

1. **htpasswd:**
```yaml
workloads:
  - agnosticd.core_workloads.ocp4_workload_authentication_htpasswd
  # ... other workloads

# htpasswd configuration
common_password: "{{ (guid[:5] | hash('md5') | int(base=16) | b64encode)[:8] }}"
ocp4_workload_authentication_htpasswd_admin_user: admin
ocp4_workload_authentication_htpasswd_admin_password: "{{ common_password }}"
ocp4_workload_authentication_htpasswd_user_base: user
ocp4_workload_authentication_htpasswd_user_password: "{{ common_password }}"
ocp4_workload_authentication_htpasswd_user_count: "{{ num_users | default('1') }}"
ocp4_workload_authentication_htpasswd_remove_kubeadmin: true
```

2. **Keycloak:**
```yaml
workloads:
  - agnosticd.core_workloads.ocp4_workload_authentication_keycloak
  # ... other workloads

# Keycloak configuration
common_password: "{{ (guid[:5] | hash('md5') | int(base=16) | b64encode)[:8] }}"
ocp4_workload_authentication_keycloak_namespace: keycloak
ocp4_workload_authentication_keycloak_channel: stable-v26.2
ocp4_workload_authentication_keycloak_admin_username: admin
ocp4_workload_authentication_keycloak_admin_password: "{{ common_password }}"
ocp4_workload_authentication_keycloak_num_users: "{{ num_users }}"
ocp4_workload_authentication_keycloak_user_username_base: user
ocp4_workload_authentication_keycloak_user_password: "{{ common_password }}"
ocp4_workload_authentication_keycloak_remove_kubeadmin: true
```

### Step 6: Workload Selection

```
🧩 Workload Selection

I'll recommend workloads based on your catalog.

Q: What technologies will users learn? (comma-separated)
   Examples: ansible aap, openshift ai, gitops, pipelines

Technologies:
```

**Workload recommendation engine:**

Based on keywords, suggest from workload-mappings.md:
- `ansible` or `aap` → `rhpds.aap25.ocp4_workload_aap25`
- `ai` or `gpu` → `rhpds.nvidia_gpu.ocp4_workload_nvidia_gpu`
- `gitops` or `argocd` → `rhpds.openshift_gitops.ocp4_workload_openshift_gitops`
- `pipelines` → `rhpds.openshift_pipelines.ocp4_workload_openshift_pipelines`
- `showroom` → `rhpds.showroom.ocp4_workload_showroom` (always recommended)

**Present recommendations:**
```
Recommended workloads:

✓ rhpds.ocp4_workload_authentication.ocp4_workload_authentication (selected - auth)
✓ rhpds.showroom.ocp4_workload_showroom (recommended - guide)
  rhpds.aap25.ocp4_workload_aap25 (suggested - ansible)
  rhpds.openshift_gitops.ocp4_workload_openshift_gitops (suggested - gitops)

Select workloads (comma-separated numbers, or 'all'):
```

### Step 7: Showroom Repository Detection

**Ask directly for the Showroom URL or path. DO NOT ask about GitHub org, root folders, or try to find it yourself:**

```
📚 Showroom Content

Q: Do you have a Showroom repository for this catalog? [Y/n]
```

**If YES:**
```
Q: What is the URL or path to your Showroom repository?

   Just provide the URL or path - I'll use it as-is.

   Examples:
   - https://github.com/rhpds/showroom-ansible-ai
   - /path/to/local/showroom

URL or path:
```

**If NO:**
```
ℹ️  You can add the Showroom URL later in common.yaml
```

### Step 8: Catalog Details

```
📝 Catalog Details

Q: Display name (appears in RHDP UI):
   Example: Ansible Automation Platform with OpenShift AI

Name:

Q: Short name (lowercase, hyphens, descriptive):
   Example: ansible-aap-ai-workshop

Short name:

Q: Brief description (1-2 sentences):
   This appears in the catalog listing.

Description:
```

**Validate directory doesn't exist across entire repo:**
```bash
# Check if directory name exists anywhere in AgV repo
if find "$AGV_PATH" -maxdepth 2 -type d -name "$short_name" 2>/dev/null | grep -q .; then
  echo "⚠️  Directory '$short_name' already exists in AgnosticV repo"
  echo "Choose a different name."
  exit 1
fi
```

### Step 8a: Repository Setup

```
📦 Repository Configuration
```

**Ask about Showroom repository:**
```
Q: Do you have a Showroom repository created for this catalog? [Y/n]
```

**If NO:**
```
📚 Create Showroom Repository

Use the Showroom Nookbag template to create your repository:

Repository: https://github.com/rhpds/showroom_template_nookbag

Instructions:
1. Visit: https://github.com/rhpds/showroom_template_nookbag
2. Follow the README to generate your showroom repository
3. Recommended naming: {short-name}-showroom
4. Create in: github.com/rhpds organization

Example:
  Use the nookbag template to create your repository:
  https://github.com/rhpds/showroom_template_nookbag

Once created, come back and re-run this skill with the repository URL.

⏸️  Pausing - Create your Showroom repository first.
```

**If YES:**
```
Q: What is the URL or path to your Showroom repository?

   Examples:
   - https://github.com/rhpds/ansible-aap-ai-showroom
   - /path/to/local/showroom

Showroom URL or path:
```

**Ask about custom Ansible collection:**
```
Q: Will this catalog use a custom Ansible collection? [Y/n]

ℹ️  Custom collections are needed when:
   - Creating new workloads specific to this catalog
   - Sharing workload logic across multiple catalogs
   - Building reusable automation components
```

**If YES:**
```
Collection naming: rhpds.{short-name}
Repository: https://github.com/rhpds/rhpds.{short-name}

Note:
- Collection must be created in github.com/rhpds organization
- Will be added to requirements_content in common.yaml
- Use this for catalog-specific workloads

Example structure:
  rhpds.{short-name}/
  ├── galaxy.yml
  ├── roles/
  │   └── ocp4_workload_{catalog_feature}/
  └── README.md
```

**If NO:**
```
✓ Using standard collections only (agnosticd.core_workloads, agnosticd.showroom, etc.)
```

### Step 9: Multi-User Configuration

```
👥 Multi-User Setup
```

**Auto-set based on category:**
- **Workshops / Brand_Events:** Multiuser REQUIRED
- **Demos:** Single-user only (multiuser: false)
- **Labs / Sandboxes:** Ask user

**If multi-user (Workshops/Brand_Events):**
```
Q: How many concurrent users (maximum)?
   Typical range: 10-60
   Default: 30

Max users [default: 30]:
```

**Set in common.yaml:**
```yaml
__meta__:
  catalog:
    multiuser: true
    workshopLabUiRedirect: true  # Auto-enable for workshops
    parameters:
      - name: num_users
        description: Number of users to provision within the environment
        formLabel: User Count
        openAPIV3Schema:
          type: integer
          default: 3
          minimum: 3
          maximum: 60
```

**Worker scaling formula (if CNV/SNO):**
```yaml
# Auto-scale workers based on num_users
openshift_cnv_scale_cluster: "{{ (num_users | int) > 3 }}"

# Per-user resource calculation
# Example: 1 worker per 5 users (adjust based on workload)
worker_instance_count: "{{ [(num_users | int / 5) | round(0, 'ceil') | int, 1] | max if (num_users | int) > 3 else 0 }}"

ai_workers_cores: 32
ai_workers_memory: 128Gi
```

**If single-user (Demos):**
```yaml
__meta__:
  catalog:
    multiuser: false  # Demos are always single-user
    # NO workshopLabUiRedirect for demos
```

### Step 10: Generate Files

Now generate all four files:

#### 10.1: Generate common.yaml

**Modern catalog structure (2026+):**

```yaml
---
#include /includes/agd-v2-mapping.yaml
#include /includes/sandbox-api.yaml
#include /includes/catalog-icon-openshift.yaml  # or catalog-icon-project-dance, catalog-icon-rh-ai-2025
#include /includes/terms-of-service.yaml
#include /includes/access-restriction-rh1-2026-devs.yaml  # Optional - for restricted catalogs

#include /includes/parameters/purpose.yaml
#include /includes/parameters/salesforce-id.yaml
#include /includes/parameters/num-users-salesforce.yaml  # If multi-user

#include /includes/secrets/ocp4_ai_offline_token.yaml
#include /includes/secrets/s3-rhpds-private-bucket.yaml

# -------------------------------------------------------------------
# --- Catalog Item: <Display Name>
# -------------------------------------------------------------------

# ===================================================================
# Repository Tag
# Tag for all repositories that are used in this config.
# ===================================================================
tag: main  # Override in prod.yaml, event.yaml with specific tag (e.g., <short-name>-1.0.0)

# -------------------------------------------------------------------
# Mandatory Variables
# -------------------------------------------------------------------
config: openshift-workloads
cloud_provider: none
software_to_deploy: none
openshift_cnv_scale_cluster: true
clusters:
  - default:
      api_url: "{{ openshift_api_url }}"
      api_token: "{{ openshift_cluster_admin_token }}"

# -------------------------------------------------------------------
# Platform
# -------------------------------------------------------------------
platform: rhpds

# -------------------------------------------------------------------
# CNV Specific (if using CNV pools)
# -------------------------------------------------------------------
bastion_instance_image: rhel-9.6
bastion_cores: 2
bastion_memory: 4Gi

# Worker scaling formula
worker_instance_count: "{{ [2, ((num_users | int / 5.0) | round(0, 'ceil') | int) + 1] | max }}"
ai_workers_cores: 32
ai_workers_memory: 128Gi

# -------------------------------------------------------------------
# Common Password
# -------------------------------------------------------------------
common_password: "{{ (guid[:5] | hash('md5') | int(base=16) | b64encode)[:8] }}"

# -------------------------------------------------------------------
# Student User on Bastion (if needed)
# -------------------------------------------------------------------
install_student_user: true
student_name: lab-user
student_sudo: true

# -------------------------------------------------------------------
# Custom collections for this environment
# -------------------------------------------------------------------
requirements_content:
  collections:
    - name: https://github.com/agnosticd/core_workloads.git
      type: git
      version: main
    - name: https://github.com/agnosticd/showroom.git
      type: git
      version: v1.3.9
    # Add other collections as needed

# -------------------------------------------------------------------
# Workloads
# -------------------------------------------------------------------
workloads:
  - agnosticd.core_workloads.ocp4_workload_authentication_htpasswd
  - agnosticd.showroom.ocp4_workload_showroom_ocp_integration
  - agnosticd.showroom.ocp4_workload_showroom
  # Add technology-specific workloads

# ===================================================================
# Workload: ocp4_workload_authentication_htpasswd
# ===================================================================
ocp4_workload_authentication_htpasswd_admin_user: admin
ocp4_workload_authentication_htpasswd_admin_password: "{{ common_password }}"
ocp4_workload_authentication_htpasswd_user_base: user
ocp4_workload_authentication_htpasswd_user_password: "{{ common_password }}"
ocp4_workload_authentication_htpasswd_user_count: "{{ num_users | default('1') }}"
ocp4_workload_authentication_htpasswd_remove_kubeadmin: true

# ===================================================================
# Workload: ocp4_workload_showroom
# ===================================================================
ocp4_workload_showroom_content_git_repo: https://github.com/rhpds/showroom-repo.git
ocp4_workload_showroom_content_git_repo_ref: main

# -------------------------------------------------------------------
# Metadata
# -------------------------------------------------------------------
__meta__:
  asset_uuid: <generated-uuid>
  anarchy:
    namespace: babylon-anarchy-7
  components:
    - name: openshift
      display_name: OpenShift Cluster
      item: agd-v2/ocp-cluster-cnv-pools/prod
      parameter_values:
        cluster_size: multinode  # or sno
        host_ocp4_installer_version: "4.20"
        ocp4_fips_enable: false
        num_users: "{{ num_users }}"
      propagate_provision_data:
        - name: sandbox_openshift_api_key
          var: sandbox_openshift_api_key
        - name: sandbox_openshift_api_url
          var: sandbox_openshift_api_url
        - name: sandbox_openshift_namespace
          var: sandbox_openshift_namespace
        - name: openshift_cluster_admin_token
          var: openshift_cluster_admin_token
        - name: openshift_api_url
          var: openshift_api_url
        - name: bastion_public_hostname
          var: bastion_ansible_host
        - name: bastion_ssh_user_name
          var: bastion_ansible_user
        - name: bastion_ssh_password
          var: bastion_ansible_ssh_pass
        - name: bastion_ssh_port
          var: bastion_ansible_port
  catalog:
    namespace: babylon-catalog-{{ stage | default('?') }}
    display_name: "<Display Name>"
    category: <Workshops|Demos|Labs|Sandboxes|Brand_Events>
    multiuser: true  # or false for demos
    workshopLabUiRedirect: true  # Only for workshops
    parameters:
      - name: num_users
        description: Number of users to provision within the environment
        formLabel: User Count
        openAPIV3Schema:
          type: integer
          default: 3
          minimum: 3
          maximum: 60
    keywords:
      - <keyword1>
      - <keyword2>
    labels:
      Provider: RHDP
      Product: <Product_Name>
      Product_Family: <Product_Family>
      # Brand_Event: Red_Hat_One_2026  # If Brand_Events
    reportingLabels:
      primaryBU: Hybrid_Platforms  # CRITICAL: For business unit tracking/reporting (Hybrid_Platforms, Application_Services, Ansible, RHEL, etc.)
  owners:
    maintainer:
      - email: <email>
        name: <Name>
    sme:
      - email: <sme-email>
        name: <SME Name>
  tower:
    timeout: 14400  # 4 hours - adjust based on complexity
  deployer:
    scm_url: https://github.com/agnosticd/agnosticd-v2
    scm_ref: main
    execution_environment:
      image: quay.io/agnosticd/ee-multicloud:chained-2025-12-17
      pull: missing
```

#### 10.2: Generate dev.yaml

```yaml
---
# -------------------------------------------------------------------
# Purpose - Cost tag. One of development, ilt, production, event
# -------------------------------------------------------------------
purpose: development
__meta__:
  deployer:
    scm_ref: main
    scm_type: git
```

**Note:** dev.yaml is minimal - only overrides scm_ref and sets purpose tag for cost tracking.

#### 10.3: Generate description.adoc

**Ask for description content:**
```
📄 Description Generation

I can extract description content from your Showroom, or you can provide it manually.

Q: Do you want me to extract from Showroom content? [Y/n]
```

**If YES and Showroom URL provided:**
```bash
# Clone showroom temporarily
temp_dir=$(mktemp -d)
git clone <showroom-url> "$temp_dir"

# Extract modules
find "$temp_dir/content/modules/ROOT/pages" -name "*.adoc" | sort

# Read module titles
grep "^= " "$temp_dir/content/modules/ROOT/pages"/*.adoc
```

**Generate description.adoc (following RHDP structure - Nate's format):**
```asciidoc
<Brief overview: 3-4 sentences max>
<Sentence 1: Start with product/technology name - what is this thing showing or doing?>
<Sentence 2-3: What is the intended use? Real-world scenario or business context>
<Do NOT mention the catalog name or generic info - get straight to the point>

[IMPORTANT]
====
<Add warnings AFTER overview if needed: GPU availability, beta/alpha release, limited support, high memory, etc.>
<For RH1 labs: "This Red Hat One lab is being released as-is with little change from the version delivered in person at the event. There is limited support for these labs and only those with regular usage will be retained in the RHDP catalog. A 30 day advance notice will be posted for any labs that get scheduled for removal.">
====

== Lab Guide

You can find a preview version of the link:<github-pages-url>[lab guide^] here.

== Featured Technology and Products

<List ONLY the products that matter or are the focus - max 6-7 for complex labs>
<Include major versions extracted from AgnosticV>
<List all significant products - e.g., for RHADS include RHTAS, RHTPA, RHACS, etc.>

* <Red Hat Product Name> <Major Version>
* <Red Hat Product Name> <Major Version>
* <Related Technology> <Major Version>

== Detailed Overview

* *<Module 1 Title>*
** <Key learning point 1>
** <Key learning point 2>
** <Key learning point 3>

* *<Module 2 Title>*
** <Key learning point 1>
** <Key learning point 2>
** <Key learning point 3>

* *<Module 3 Title>*
** <Key learning point 1>
** <Key learning point 2>

== Authors

<Retrieve all names from __meta__.owners in common.yaml - names only, NO emails>

* <Author Name>
* <Author Name>

== Support

For help with instructions or functionality, contact lab authors.

For problems with provisioning or environment stability:

* Open an RHDP link:https://red.ht/rhdp-ticket[Support Ticket^]
* Post a message in Slack channel: link:https://redhat.enterprise.slack.com/archives/C06QWD4A5TE[#forum-demo-redhat-com^]
```

**Example (Demo):**
```asciidoc
vLLM Playground demonstrates deploying and managing vLLM inference servers using containers with features like structured outputs, tool calling, and MCP integration. This demo uses the ACME Corporation customer support scenario to show how Red Hat AI Inference Server modernizes AI-powered infrastructure. Learners deploy vLLM servers, configure structured outputs for system integration, and implement agentic workflows with performance benchmarking.

[IMPORTANT]
====
GPU-enabled nodes recommended for optimal performance. CPU-only mode available but slower.
====

== Lab Guide

You can find a preview version of the link:https://rhpds.github.io/showroom-vllm-playground[lab guide^] here.

== Featured Technology and Products

* Red Hat Enterprise Linux 10
* vLLM Playground 0.1.1
* Red Hat AI

== Detailed Overview

* *Introduction to vLLM Playground*
** Overview of vLLM architecture and container-based deployment
** ACME Corp use case: modernizing customer support with AI
** Deploy first vLLM server instance

* *Structured Outputs Configuration*
** Configure JSON schema validation for reliable outputs
** Integrate with downstream systems using structured data
** Test output consistency across multiple requests

* *Tool Calling and MCP Integration*
** Implement function calling to extend AI capabilities
** Enable Model Context Protocol for agentic workflows
** Build human-in-the-loop approval system

* *Performance Benchmarking*
** Run load tests against vLLM deployments
** Compare CPU vs GPU performance metrics
** Validate production readiness criteria

== Authors

* Michael Tao
* Jane Developer

== Support

For help with instructions or functionality, contact lab authors.

For problems with provisioning or environment stability:

* Open an RHDP link:https://red.ht/rhdp-ticket[Support Ticket^]
* Post a message in Slack channel: link:https://redhat.enterprise.slack.com/archives/C06QWD4A5TE[#forum-demo-redhat-com^]
```

**Example (Workshop - Real from Nate's PR):**
```asciidoc
Red Hat Advanced Developer Suite (RHADS) scales platform engineering teams to increase developer productivity and reduce software supply chain risk in hybrid and multicloud environments. This hands-on workshop goes deep into the architecture and implementation of RHADS, built for solutions architects, consultants, and technical sellers. Learners deploy and configure core RHADS components, explore real-world integration patterns, and see how RHADS improves developer experience while strengthening software supply chain security.

[IMPORTANT]
====
This Red Hat One lab is being released as-is with little change from the version delivered in person at the event.
There is limited support for these labs and only those with regular usage will be retained in the RHDP catalog.
A 30 day advance notice will be posted for any labs that get scheduled for removal.
====

== Lab Guide

You can find a preview version of the link:https://rhpds.github.io/build-secured-dev-workflows-showroom[lab guide^] here.

== Featured Technology and Products

* Red Hat Advanced Developer Suite (RHADS)
* Red Hat Trusted Artifact Signer (RHTAS)
* Red Hat Trusted Profile Analyzer (RHTPA)
* Red Hat Developer Hub (RHDH)
* Red Hat Advanced Cluster Security (RHACS)
* Red Hat OpenShift Pipelines
* Jenkins

== Detailed Overview

* *Module 1: Establish Software Composition Trust with SBOMs*
** Configure identity and access management using Red Hat Build of Keycloak (RHBK)
** Deploy Red Hat Trusted Profile Analyzer (RHTPA) using an operator
** Ingest SBOMs and analyze software composition to gain visibility into vulnerabilities

* *Sign and Verify All Artifacts With RHTAS*
** Deploy Red Hat Trusted Artifact Signer (RHTAS) for cryptographic signing and verification
** Integrate RHTAS with Tekton Chains to automate keyless artifact signing
** Establish immutable provenance tracking with Fulcio, Rekor, and Trillian

* *Developer Workflow Without Developer Friction*
** Configure Red Hat Developer Hub (RHDH) with SSO authentication and dynamic plugins
** Set up catalog auto-discovery using GitOps and Configuration as Code
** Enable OIDC-based commit signing with GitSign and Red Hat DevSpaces

* *Enforce Policy and Promote Safely*
** Configure Red Hat Advanced Cluster Security (RHACS) integration with Quay for image scanning
** Execute end-to-end trusted software supply chain pipelines
** Enforce Enterprise Contract (EC) policies and promote only verified, compliant images

== Authors

* Tyrell Reddy
* Prakhar Srivastava
* Ramy El Essawy

== Support

For help with instructions or functionality, contact lab authors.

For problems with provisioning or environment stability:

* Open an RHDP link:https://red.ht/rhdp-ticket[Support Ticket^]
* Post a message in Slack channel: link:https://redhat.enterprise.slack.com/archives/C06QWD4A5TE[#forum-demo-redhat-com^]
```

**Key Guidelines (Nate's Format):**
- Brief overview: 3-4 sentences max - start with product name, what it shows, intended use, NO catalog name
- Warnings AFTER overview using `[IMPORTANT]` blocks (GPU, beta/alpha, limited support, etc.)
- Lab Guide section: "You can find a preview version of the link:url[lab guide^] here."
- Featured Products: 6-7 max for complex labs, include all significant products with major versions
- Detailed Overview: Use `**` (double asterisks) for sub-bullets under module titles, NOT numbered lists
- Do not create more than 3 sub-bullets for each module
- Module titles can use `*` for top-level bullets (like `* *Module 1: Title*`)
- Authors: names only from __meta__.owners in common.yaml - NO emails
- Support: Simple format - "For help with instructions or functionality, contact lab authors." then "For problems with provisioning or environment stability:" with RHDP ticket + Slack links

#### 10.4: Generate info-message-template.adoc

```
📧 Info Message Template

This template displays user data after deployment.

Q: Does your catalog use agnosticd_user_info to share data? [Y/n]
```

**If YES:**
```
Q: What data keys does your workload share via agnosticd_user_info.data?

Examples:
  - litellm_api_base_url
  - litellm_virtual_key
  - grafana_admin_password

Data keys (comma-separated):
```

**Generate info-message-template.adoc:**
```asciidoc
= Environment Provisioned

Your <catalog-name> environment has been provisioned successfully!

== Access Information

* *Console URL*: {openshift_console_url}
* *Username*: {openshift_cluster_admin_username}
* *Password*: {openshift_cluster_admin_password}

== Guide

Access your workshop guide:

* link:{openshift_cluster_console_url}/showroom[Workshop Guide^]

== Additional Information

=== <Service Name>

* *API URL*: {<data_key_1>}
* *API Key*: {<data_key_2>}

NOTE: The data above comes from `agnosticd_user_info.data` in your workload.

== Support

Questions? Reach out in Slack: [#forum-demo-developers](https://redhat.enterprise.slack.com/archives/C04MLMA15MX)
```

**Explain agnosticd_user_info:**
```
ℹ️  How to share data from your workload:

In your workload tasks/workload.yml:

- name: Save user data for info message
  agnosticd.core.agnosticd_user_info:
    data:
      my_api_url: "{{ api_base_url }}"
      my_api_key: "{{ virtual_key }}"

Then use in info-message-template.adoc:

* API URL: {my_api_url}
* API Key: {my_api_key}

The template renders when users receive their environment.
```

**If NO user data:**
```asciidoc
= Environment Provisioned

Your <catalog-name> environment is ready!

== Access Information

* *Console URL*: {openshift_console_url}
* *Username*: {openshift_cluster_admin_username}
* *Password*: {openshift_cluster_admin_password}

== Workshop Guide

link:{openshift_cluster_console_url}/showroom[Open Guide^]

== Support

Questions? [#forum-demo-developers](https://redhat.enterprise.slack.com/archives/C04MLMA15MX)
```

### Step 11: Determine Catalog Directory Path

```
📂 Catalog Directory Path

Q: Which subdirectory should I create the catalog in?

Common options:
- agd_v2 (standard catalogs)
- openshift_cnv (CNV-based catalogs)
- sandboxes-gpte (sandbox catalogs)
- published (Virtual CIs)
- custom path

Enter subdirectory (e.g., agd_v2):
```

**Build the path:**
```bash
# User enters subdirectory (e.g., "agd_v2")
catalog_path="$AGV_PATH/$subdirectory/$directory_name"
```

**Validate doesn't exist:**
```bash
if [[ -d "$catalog_path" ]]; then
  echo "⚠️  Directory already exists: $catalog_path"
  echo "Choose a different name or location."
  exit 1
fi
```

### Step 12: Write Files

```
💾 Writing Files

Creating catalog directory: $catalog_path

Writing:
  ✓ common.yaml
  ✓ dev.yaml
  ✓ description.adoc
  ✓ info-message-template.adoc
```

**Execute:**
```bash
mkdir -p "$catalog_path"

# Write all four files
cat > "$catalog_path/common.yaml" <<'EOF'
<generated-content>
EOF

cat > "$catalog_path/dev.yaml" <<'EOF'
<generated-content>
EOF

cat > "$catalog_path/description.adoc" <<'EOF'
<generated-content>
EOF

cat > "$catalog_path/info-message-template.adoc" <<'EOF'
<generated-content>
EOF
```

### Step 13: Git Commit (Optional)

```
🚀 Ready to Commit

Files created in: $catalog_path

Q: Commit these changes? [Y/n]
```

**If YES:**
```bash
# Get relative path from AgV root for commit message
rel_path="${catalog_path#$AGV_PATH/}"

cd "$AGV_PATH"

git add "$rel_path/"

git commit -m "Add $directory_name catalog

- Category: $category
- Infrastructure: $cloud_provider ($sandbox_architecture)
- Workloads: $num_workloads selected
- UUID: $asset_uuid
- Path: $rel_path"

current_branch=$(git rev-parse --abbrev-ref HEAD)
echo "✓ Committed to branch: $current_branch"
echo ""
echo "Next steps:"
echo "  1. Test locally: cd $rel_path && agnosticv_cli dev.yaml"
echo "  2. Run validator: /agnosticv-validator"
echo "  3. Create PR: git push origin $current_branch && gh pr create --fill"
```

---

## MODE 2: Description Only

**When selected:** User chose option 2 (Description Only)

**Simplified workflow - just extract from Showroom and generate description.adoc**

### Step 1: Locate Showroom

**Ask directly for the path. DO NOT ask about GitHub org or try to find it yourself:**

```
📚 Showroom Content

Q: What is the path to your Showroom repository?

   Just provide the path or URL - I'll use it as-is.
   Press Enter to use current directory.

   Examples:
   - /Users/you/work/my-workshop-showroom
   - https://github.com/rhpds/my-workshop-showroom
   - . (current directory)

Path:
```

**Validate:**
```bash
if [[ -d "$path/content/modules/ROOT/pages" ]]; then
  echo "✓ Found Showroom content"
  HAS_SHOWROOM=true
else
  echo "✗ No Showroom content found at: $path/content/modules/ROOT/pages"
  HAS_SHOWROOM=false
fi
```

**If no Showroom found, offer manual entry:**
```
⚠️  No Showroom Content Found

Mode 2 works best when you have Showroom content to extract from.

Options:
1. Enter description details manually (I'll ask you questions)
2. Create Showroom content first and come back
3. Exit and use Mode 1 (Full Catalog) instead

Your choice [1/2/3]:
```

**If option 2 (Create Showroom first):**
```
📚 Create Showroom Content First

Use the /create-lab or /create-demo skills to generate Showroom content:

For workshops:
  /create-lab

For demos:
  /create-demo

Once you have Showroom content, run this skill again with Mode 2.

⏸️  Exiting - Create Showroom content first.
```

**If option 3 (Use Mode 1):**
```
ℹ️  Mode 1 (Full Catalog) creates everything including description.adoc

Re-run this skill and select Mode 1 at the beginning.

⏸️  Exiting
```

**If option 1 (Manual entry), continue to Step 1a**

---

### Step 1a: Manual Entry (When No Showroom)

**Only run this step if HAS_SHOWROOM=false and user chose manual entry**

```
📝 Manual Description Entry (RHDP Structure)

Since you don't have Showroom content, I'll ask for all the details needed for description.adoc.
```

**1. Brief Overview (3-4 sentences max):**
```
Q: Brief overview (3-4 sentences):
   - Sentence 1: What is this showing or doing?
   - Sentence 2-3: What is the intended use? Business context?
   - Sentence 4: What do learners do/deploy?
   - Do NOT mention catalog name or generic info

   Example: "vLLM Playground demonstrates deploying and managing vLLM inference servers using containers with features like structured outputs and tool calling. This demo uses the ACME Corporation customer support scenario to show how Red Hat AI Inference Server modernizes AI-powered infrastructure. Learners deploy vLLM servers, configure structured outputs, and implement agentic workflows with performance benchmarking."

Overview:
```

**2. Warnings (optional):**
```
Q: Any warnings or special requirements? (optional)
   Examples: "GPU-enabled nodes recommended for optimal performance"
             "Beta release - features subject to change"
             "High memory usage - 32GB RAM minimum"

Warnings [press Enter to skip]:
```

**3. Guide Link:**
```
Q: Lab/Demo Guide URL:
   - Link to rendered Showroom (preferred)
   - Or link to repo/document if no Showroom yet

   Example: https://rhpds.github.io/my-workshop-showroom

Guide URL:
```

**4. Featured Products (max 3-4):**
```
Q: Featured Technology and Products (max 3-4, ONLY what matters):
   List the products that are the FOCUS of this asset with major versions.
   Do NOT list every product - only what matters.

   Example: "Red Hat Enterprise Linux 10, vLLM Playground 0.1.1, Red Hat AI"

Products [comma-separated with versions]:
```

**5. Module Details:**
```
Q: How many modules/chapters are in this lab/demo?

Module count:
```

**For each module, ask:**
```bash
for ((i=1; i<=module_count; i++)); do
  echo ""
  echo "=== Module $i Details ==="
  echo ""
  echo "Q: Module $i title:"
  read module_title

  echo ""
  echo "Q: Module $i details (2-3 bullets max, what do learners do?):"
  echo "   Enter bullets one per line, press Enter twice when done"
  echo ""

  bullets=()
  while IFS= read -r line; do
    [[ -z "$line" ]] && break
    bullets+=("$line")
  done

  # Store module data
  module_data["$i"]="$module_title|${bullets[*]}"
done
```

**6. Authors:**
```
Q: Lab/Demo authors (from __meta__.owners or manual entry):
   If this catalog has a common.yaml, I'll extract from __meta__.owners.
   Otherwise, enter author names (one per line, press Enter twice when done):

Authors:
```

**Capture authors:**
```bash
authors=()
while IFS= read -r line; do
  [[ -z "$line" ]] && break
  authors+=("$line")
done
```

**7. Support Information:**
```
Q: Content support Slack channel (where users get help with instructions):
   Example: #my-lab-support

Content Slack channel:

Q: Author Slack handle (to tag for content questions):
   Example: @john-smith

Author Slack handle:

Q: Author email (alternative to Slack):
   Example: jsmith@redhat.com

Author email [optional]:
```

**Set variables for Step 3:**
```bash
# For manual entry, set these variables
brief_overview="$overview_input"
warnings="$warnings_input"
guide_url="$guide_url_input"
featured_products="$products_input"
module_details=("${module_data[@]}")
authors=("${authors[@]}")
content_slack_channel="$content_slack_input"
author_slack_handle="$author_slack_handle_input"
author_email="$author_email_input"

# Skip Step 2 (extraction) and go directly to Step 3 (generate)
```

### Step 2: Extract Content from Showroom

**Only run this step if HAS_SHOWROOM=true (skip if manual entry)**

**Read ALL modules and extract comprehensive information:**
```bash
# Get ALL modules (ensure we don't miss any)
modules=$(find "$path/content/modules/ROOT/pages" -type f -name "*.adoc" \
  -not -name "index.adoc" \
  -not -name "*nav.adoc" \
  -not -name "workshop-overview.adoc" | sort)

# Count modules
module_count=$(echo "$modules" | grep -c "\.adoc$")

# Extract and display all module titles
echo "📚 Reading $module_count modules:"
module_titles=()
while IFS= read -r module; do
  if [[ -f "$module" ]]; then
    title=$(grep "^= " "$module" | head -1 | sed 's/^= //')
    echo "  * $title ($(basename "$module"))"
    module_titles+=("$title")
  fi
done <<< "$modules"

# Read ALL modules for comprehensive content extraction
echo ""
echo "📖 Analyzing all module content..."

# Combine all module content (excluding index/nav)
all_content=$(cat "$path/content/modules/ROOT/pages"/*.adoc 2>/dev/null | grep -v "^include::" | grep -v "^::")

# Extract overview from index.adoc first
if [[ -f "$path/content/modules/ROOT/pages/index.adoc" ]]; then
  index_overview=$(awk '
    /^= / { in_content=1; next }
    in_content && /^:/ { next }
    in_content && /^$/ { next }
    in_content && /^[A-Z]/ {
      print;
      for(i=1; i<=3; i++) {
        getline;
        if ($0 != "") print;
      }
      exit
    }
  ' "$path/content/modules/ROOT/pages/index.adoc" 2>/dev/null)
fi

# Extract key learning objectives from all modules
learning_objectives=$(echo "$all_content" | grep -E "learn|understand|configure|deploy|create|build|integrate|automate" | grep -v "^#" | head -10)

# Detect Red Hat product names across ALL modules
detected_products=$(echo "$all_content" | grep -hoE '(Red Hat )?OpenShift (Container Platform|Virtualization|AI|GitOps|Pipelines|Data Foundation)?|Ansible Automation Platform|(Red Hat )?Ansible( AI)?|Red Hat Enterprise Linux|RHEL [0-9.]+|Red Hat Device Edge|Red Hat Insights|Advanced Cluster Management|ACM|Red Hat Quay|Red Hat OpenShift Service Mesh|Red Hat AMQ|Red Hat Integration|Red Hat build of Keycloak|Red Hat OpenShift Data Foundation|Red Hat Advanced Cluster Security' 2>/dev/null | sort -u | head -15)

# Extract version numbers mentioned across ALL modules
version_info=$(echo "$all_content" | grep -hoE '(OpenShift|Ansible|RHEL|AAP|Kubernetes) [0-9]+\.[0-9]+|version [0-9]+\.[0-9]+' 2>/dev/null | sort -u | head -8)

# Detect key technical topics across ALL modules
technical_topics=$(echo "$all_content" | grep -hoE 'GitOps|CI/CD|Kubernetes|Operators|Helm|Service Mesh|Serverless|Tekton|ArgoCD|Prometheus|Grafana|Storage|Networking|Security|Multi-cluster' 2>/dev/null | sort -u | head -10)

# Get git author
author=$(git -C "$path" config user.name 2>/dev/null || echo "Unknown")

# Get GitHub Pages URL from remote
remote=$(git -C "$path" remote get-url origin 2>/dev/null)
if [[ -n "$remote" ]]; then
  github_pages_url=$(echo "$remote" | sed 's|git@github.com:|https://|' | sed 's|\.git$|/|' | sed 's|github.com/|rhpds.github.io/|')
else
  github_pages_url=""
fi

echo ""
echo "📊 Extracted from ALL modules:"
echo "  ✓ Modules analyzed: $module_count"
echo "  ✓ Module titles:"
for title in "${module_titles[@]}"; do
  echo "    - $title"
done
echo "  ✓ Author: $author"
echo "  ✓ GitHub Pages: $github_pages_url"
echo "  ✓ Red Hat Products detected:"
echo "$detected_products" | while read product; do
  [[ -n "$product" ]] && echo "    - $product"
done
if [[ -n "$version_info" ]]; then
  echo "  ✓ Versions found:"
  echo "$version_info" | while read version; do
    [[ -n "$version" ]] && echo "    - $version"
  done
fi
if [[ -n "$technical_topics" ]]; then
  echo "  ✓ Technical topics:"
  echo "$technical_topics" | while read topic; do
    [[ -n "$topic" ]] && echo "    - $topic"
  done
fi
```

### Step 3: Generate Description

**If HAS_SHOWROOM=true (extracted from Showroom):**

**Review comprehensive extracted content from ALL modules:**
```
📝 Description Content Review

I've read ALL $module_count modules and extracted the following:

Module Structure:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${module_titles[@]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overview (from index.adoc):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$index_overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Red Hat Products Detected (from all modules):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$detected_products
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Versions Found (from all modules):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$version_info
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Technical Topics (from all modules):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$technical_topics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: Is the extracted overview accurate? [Y to use as-is / N to provide custom]:

If N:
Q: Provide a brief overview (2-3 sentences, starting with product name):
   Base it on the module titles and content above.

Custom overview:

Q: Are the detected products/technologies/versions correct? [Y to use / N to customize]:

If N:
Q: Featured technologies (comma-separated with versions):
   Example: OpenShift 4.14, Ansible Automation Platform 2.5, Red Hat Enterprise Linux 9

   Detected: $detected_products $version_info

Custom technologies:

Q: Any warnings or special requirements? (optional)
   Examples: "Requires GPU nodes", "High memory usage", "Network-intensive"
   Based on: $technical_topics

Warnings [optional]:
```

**IMPORTANT:**
- ALL modules have been read and analyzed, not just index.adoc
- If user says Yes to extracted content, use it directly. Don't ask again!
- Show comprehensive data from all modules so user can make informed decisions
- Module titles, products, versions, and topics are extracted from the entire workshop content

---

**If HAS_SHOWROOM=false (manual entry):**

**Review manually entered content:**
```
📝 Description Content Review

You entered the following information:

Display Name:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$display_name
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overview:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$index_overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Technologies:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$detected_products
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Modules ($module_count):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${module_titles[@]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Author: $author
GitHub Pages: ${github_pages_url:-"Not provided"}
Warnings: ${warnings:-"None"}

Q: Is this information correct? [Y to proceed / N to edit]:

If N, allow editing:
  Q: What would you like to edit?
     1. Overview
     2. Technologies
     3. Modules
     4. All of the above

  Choice [1-4]:
```

**After confirmation, proceed to generate description.adoc**

---

**Generate and write description.adoc** (same format as Mode 1, Step 10.3)

### Step 4: Locate Output Directory

**Ask directly for the path. DO NOT try to auto-detect, search, or ask about subdirectories:**

```
📂 Output Location

Q: What is the path to the catalog/CI directory where I should save description.adoc?

   Just provide the full path - I'll save the file there directly.

   Examples:
   - ~/work/code/agnosticv/agd_v2/my-workshop
   - /Users/you/code/agnosticv/catalogs/demo-catalog
   - agd_v2/my-catalog (relative to AgV repo)

Path:
```

**Write file and optionally commit** (same as Mode 1, Step 12)

---

## MODE 3: Info Message Template Only

**When selected:** User chose option 3 (Info Message Template)

### Step 1: Locate Catalog

**Ask directly for the path. DO NOT try to find it or ask about subdirectories:**

```
📂 Catalog Location

Q: What is the path to your AgV catalog directory?

   Examples:
   - ~/work/code/agnosticv/agd_v2/my-catalog
   - /path/to/agnosticv/catalogs/demo-catalog

Path:
```

### Step 2: User Data Configuration

```
📧 Info Message Template

This template uses data from agnosticd_user_info.

Q: Does your workload share data via agnosticd_user_info? [Y/n]
```

**If YES:**
```
Q: List the data keys your workload shares (comma-separated):

Examples:
  - litellm_api_base_url, litellm_virtual_key
  - grafana_url, grafana_password
  - custom_service_url, custom_api_key

Data keys:
```

**Generate template** (same as Mode 1, Step 10.4)

**Write file and optionally commit**

---

## MODE 4: Create Virtual CI

**When selected:** User chose option 4 (Create Virtual CI)

Create a Virtual CI in the `published/` folder based on an existing base component.

**What this mode does:**
- Creates Virtual CI in `published/<name>/` with common.yaml, dev.yaml, prod.yaml, description.adoc
- Copies description.adoc and templates from base component
- Adds dev restriction (`#include /includes/access-restriction-devs-only.yaml`) to base component
- Adds warning to base component's description.adoc
- Creates/updates base component's prod.yaml with scm_ref version (for production stability)
- Ensures `reportingLabels.primaryBU` is set on both Virtual CI and base component

**Bulk usage:** The user may provide multiple base component paths. Process each one sequentially.

### Step 1: Get Base Component Path

If not provided as argument, ask:

```
Q: What is the path to the base component?
   (Relative to AgV root, e.g., openshift_cnv/kafka-developer-workshop-cnv)

   You can provide multiple paths separated by spaces for bulk processing.

Path(s):
```

### Step 2: Locate and Read Base Component

For each base component path:

1. Path is relative to `$AGV_PATH` (detected from configuration files or user input)
2. Read `<base-component-path>/common.yaml`
3. If file doesn't exist, report error and skip (or stop if single component)

### Step 3: Derive Virtual CI Name

1. Take last segment of base component path (e.g., `kafka-developer-workshop-cnv`)
2. Check for known provider suffixes: `-cnv`, `-aws`, `-azure`, `-gcp`, `-sandbox`, `-pool`
3. If suffix exists, strip it to get Virtual CI name (e.g., `kafka-developer-workshop`)

**If no recognizable suffix:**
- Base component name doesn't have provider suffix
- **Cannot reuse base component folder name** — names must be unique across AgnosticV
- Ask: "The base component `<name>` doesn't have a provider suffix. What should the Virtual CI folder be named? (Must be unique across all of AgnosticV)"

**Uniqueness Check (CRITICAL):**

Folder names must be unique across **entire AgnosticV repository**.

**ALWAYS run this check:**
```bash
find "$AGV_PATH" -type d -name "<proposed-name>" 2>/dev/null
```

**If name already exists:**
- In `published/`: Ask if user wants to add to existing Virtual CI (multi-component)
- Elsewhere (agd_v2/, openshift_cnv/, etc.): Cannot use name, ask for alternative
- User can also skip this base component

### Step 4: Extract Information from Base Component

From base component's `common.yaml`, extract **only what exists** — do NOT invent values:

| Field | Action |
|-------|--------|
| `#include` statements | Copy icon include (e.g., `#include /includes/catalog-icon-*.yaml`) |
| `__meta__.asset_uuid` | Note it (Virtual CI needs NEW UUID) |
| `__meta__.owners` | Copy exactly as-is |
| `__meta__.catalog` | Copy exactly, modify `display_name` |
| `__meta__.catalog.display_name` | Remove provider suffix (e.g., "(CNV)", "(AWS)") |
| `__meta__.catalog.parameters` | Copy, update component references |

**IMPORTANT:** Do not generate missing fields. If required field missing, ask user.

**Special handling for `catalog.reportingLabels.primaryBU`:**

This field is **required** for reporting and must always be verified.

Known valid values (Feb 2026):
- Application_Developer
- Artificial_Intelligence
- Automation
- DEMO_Platform
- Edge
- Hybrid_Platforms
- RHDP
- RHEL

**Verification process:**

When asking about `primaryBU`, **always include base component path** (important for bulk processing):

1. **If present in base component:**
   - Ask: "For `<base-component-path>`: The base component has `primaryBU: <value>`. Is this correct, or should it be changed to one of: [list above]?"

2. **If NOT present:**
   - Ask: "For `<base-component-path>`: Missing `primaryBU`. What business unit should this be? Options: [list above]"
   - Add answer to **BOTH** Virtual CI **AND** base component's `common.yaml`

**When processing multiple base components:** Ask about each one separately with base component path in question.

**Icon include:** Look for `#include /includes/catalog-icon-*.yaml` in base component. Use same icon in Virtual CI. If not found, ask user.

### Step 5: Generate New UUID

```bash
uuidgen | tr '[:upper:]' '[:lower:]'
```

### Step 6: Determine Component Name

Component name in `__meta__.components`:
- Use last segment from base component path (e.g., `kafka-developer-workshop-cnv`)
- Becomes both `name` and used in `item` path

### Step 7: Create Virtual CI Files

Create folder: `$AGV_PATH/published/<virtual-ci-name>/`

#### common.yaml

```yaml
---
#include /includes/<icon-from-base-component>.yaml
#include /includes/terms-of-service.yaml
#include /includes/lifetime-standard.yaml

#include /includes/parameters/salesforce-id.yaml
#include /includes/parameters/purpose.yaml

# -------------------------------------------------------------------
#
# --- Catalog Item: <Display Name>
#
# No changes should be made to this CI, other than __meta__
# All changes to the functional CI should be made to the component(s)
#
# <base-component-path>
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# Babylon meta variables
# -------------------------------------------------------------------
__meta__:
  asset_uuid: <generated-uuid>
  owners:
    # Copy exactly from base component — do not modify or add fields
    maintainer:
    - name: <name>
      email: <email>

  catalog:
    # Copy exactly from base component, only modify display_name
    # Do NOT add fields that don't exist in base component
    namespace: babylon-catalog-{{ stage | default('?') }}
    display_name: "<clean-name-without-provider-suffix>"
    # ... copy remaining catalog fields exactly as they appear

  components:
  - name: <component-name>
    display_name: <Display Name with Provider>
    item: <base-component-path>

  deployer:
    type: null
```

#### dev.yaml

```yaml
# No config required
# See dev.yaml in component CI for details
```

#### prod.yaml

```yaml
# No config required
# See prod.yaml in component CI for details
```

#### test.yaml (only if base component has one)

```yaml
# No config required
# See test.yaml in component CI for details
```

#### description.adoc (REQUIRED)

Copy from base component exactly as-is:

```bash
cp "$AGV_PATH/<base-component-path>/description.adoc" \
   "$AGV_PATH/published/<virtual-ci-name>/description.adoc"
```

#### info-message-template.adoc (if exists)

```bash
cp "$AGV_PATH/<base-component-path>/info-message-template.adoc" \
   "$AGV_PATH/published/<virtual-ci-name>/info-message-template.adoc"
```

#### user-message-template.adoc (if exists)

```bash
cp "$AGV_PATH/<base-component-path>/user-message-template.adoc" \
   "$AGV_PATH/published/<virtual-ci-name>/user-message-template.adoc"
```

### Step 8: Update Base Component Files

#### 8a: Add dev restriction to common.yaml

Add to **top** of base component's `common.yaml` (after initial `---`):

```yaml
# This item is restricted to devs only!
# It should be ordered by regular users using the Virtual CI
# in the `published` directory.
#include /includes/access-restriction-devs-only.yaml
```

**Note:** If include already exists, skip.

#### 8b: Add warning to description.adoc

Add to **beginning** of base component's `description.adoc`:

```asciidoc
[WARNING]
====
Do not order this item unless you are a developer and are working on the CI.
Order the parent CI instead, which can be found link:https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/published.<virtual-ci-name>.prod[here^].
====

```

Replace `<virtual-ci-name>` with actual Virtual CI folder name.

#### 8c: Create/Update prod.yaml with scm_ref version

**IMPORTANT:** For production stability, base components should pin `scm_ref` to a specific version.

**Ask user:**
```
📌 Production Version Pinning

Q: What scm_ref version should be used for production?
   (e.g., demyst-1.0.1, ocp-adv-1.0.0, build-secure-dev-0.0.1)

   Enter version tag (or press Enter to skip):
```

**If user provides version:**

Create or update `<base-component-path>/prod.yaml`:

```yaml
---
# -------------------------------------------------------------------
# Babylon meta variables
# -------------------------------------------------------------------
__meta__:
  deployer:
    scm_ref: <user-provided-version>
```

**If prod.yaml already exists:**
- Read existing file
- Check if `__meta__.deployer.scm_ref` exists
- If exists and different, ask: "prod.yaml already has scm_ref: <existing>. Replace with <new-version>? [Y/n]"
- Update only the scm_ref value, preserve other settings

**If user skips:**
- No prod.yaml created/updated
- Continue to next step

### Step 9: Handle Multiple Components

If adding to existing Virtual CI (multi-component):

1. Read existing Virtual CI's `common.yaml`
2. Add new base component to `__meta__.components` list
3. If `__meta__.catalog.parameters` has `components` arrays, add new component name
4. **Check conflicts:** If owners or catalog settings differ, ask for clarification

### Step 10: Validation

After creating files:

1. Verify YAML syntax is valid
2. Validate `__meta__` against schema at `$AGV_PATH/.schemas/babylon.yaml`
   - Ensure required fields present (e.g., `asset_uuid`)
   - Verify field types match schema
   - Check no unknown properties (`additionalProperties: false`)
3. Confirm `item` path points to existing base component
4. Verify `description.adoc` copied to Virtual CI
5. Verify dev restriction added to base component's `common.yaml`
6. Verify warning added to base component's `description.adoc`
7. Verify prod.yaml created/updated in base component (if version was provided)
8. Report what was created

### Output Format

```
Created Virtual CI: published/<name>
  - Base component: <base-component-path>
  - UUID: <generated-uuid>
  - Display name: "<clean-display-name>"
  - Icon: <icon-include-used>
  - Files created: common.yaml, dev.yaml, prod.yaml, description.adoc
  - Optional files copied: info-message-template.adoc, user-message-template.adoc (if existed)
  - Base component updated:
    - Added dev restriction to common.yaml
    - Added warning to description.adoc
    - Created/Updated prod.yaml with scm_ref: <version> (if provided)
```

### Error Handling

| Error | Action |
|-------|--------|
| No base component path | Ask user |
| Base component not found | Report path, suggest alternatives if similar exist |
| No provider suffix | Ask user for Virtual CI folder name (cannot reuse base name) |
| Name matches base component | Cannot use — ask alternative |
| Name exists in `published/` | Ask preference (add component, rename, skip) |
| Name exists elsewhere | Cannot use — ask alternative |
| No icon include | Ask user which icon |
| Missing `__meta__` in base | Report error, cannot create Virtual CI |
| Missing required field | Ask user — do not invent |
| Conflicting metadata (multi-component) | Ask which values to use |
| No description.adoc | Report error — required |

---

## Common Git Workflow (All Modes)

After generating files, always offer to commit:

```
🚀 Commit Changes

Branch: <branch-name>
Files modified:
  - agd_v2/<catalog-name>/...

Q: Commit these changes? [Y/n]
```

**If YES:**
```bash
cd "$AGV_PATH"

git add <files>

git commit -m "<appropriate-message>"

echo "✓ Committed to branch: $branch_name"
echo ""
echo "Next steps:"
echo "  1. Push: git push origin $branch_name"
echo "  2. Create PR: gh pr create --fill"
echo "  3. Validate: /agnosticv-validator"
```

---

## Validation & Testing

After file generation, guide users to validate:

```
✅ Next Steps

Your catalog files are ready!

Recommended actions:

1. Validate configuration:
   /agnosticv-validator

2. Test locally (if you have agnosticd-cli):
   cd agd_v2/<catalog-name>
   agnosticd_cli dev.yaml

3. Create pull request:
   git push origin <branch-name>
   gh pr create --fill

4. Request review in [#forum-demo-developers](https://redhat.enterprise.slack.com/archives/C04MLMA15MX)
```

---

## Error Handling

**UUID collision:**
```
⚠️  UUID collision detected!

The generated UUID already exists in:
  <path-to-existing-catalog>

Regenerating new UUID...
```

**Invalid category:**
```
⚠️  Category must be exactly one of:
  - Workshops
  - Demos
  - Sandboxes

(Case-sensitive, plural form)
```

**Showroom not found:**
```
⚠️  Showroom content not found at: <path>

Expected structure:
  content/modules/ROOT/pages/*.adoc

Please check the path and try again.
```

**Branch name with feature/:**
```
⚠️  Branch names should NOT include 'feature/' prefix.

Instead of: feature/add-workshop
Use: add-workshop

Please provide a branch name without 'feature/':
```

---

## Smart Features

### Auto-Detection
- Showroom module structure
- GitHub Pages URL from git remote
- Author name from git config
- Technology keywords in content
- Existing catalog directories

### Recommendations
- Workloads based on technology keywords
- Infrastructure based on catalog type
- Multi-user settings based on category

### Validation
- UUID uniqueness
- Category exact match
- Directory name conflicts
- Branch naming conventions
- Showroom content structure

---

## Best Practices

1. **Always pull main before starting** - Ensures latest catalog patterns
2. **Use descriptive branch names** - No feature/ prefix, just: add-catalog-name
3. **Validate before PR** - Use /agnosticv-validator
4. **Test in dev first** - Use dev.yaml for testing
5. **Document user data** - Clear info-message-template.adoc
6. **Start with product name** - Description overview must start with product, not "This workshop"

---

## Example Sessions

### Example 1: Full Catalog Creation

```
User: /agnosticv-catalog-builder
Skill: 🏗️  AgnosticV Catalog Builder

What would you like to create or update?

1. Full Catalog (common.yaml, dev.yaml, description.adoc, info-message-template.adoc)
2. Description Only (description.adoc)
3. Info Message Template (info-message-template.adoc)

Your choice [1-3]: 1

Q: AgnosticV repository path: [your_agv_path]

🔧 Git Workflow Setup

Current branch: main
📥 Pulling latest changes from main...
Already up to date.

Q: Branch name (without feature/): add-ansible-ai-workshop

🌿 Creating branch: add-ansible-ai-workshop
Switched to a new branch 'add-ansible-ai-workshop'

📖 Catalog Discovery

Q: Keywords for search: ansible ai

Found similar catalogs:
1. ansible-aap-workshop (Ansible Automation Platform Self-Service)
2. ansible-automation-mesh (Ansible Automation Mesh on OpenShift)

Choice: A (Create new from scratch)

📂 Category: 1 (Workshops)

🔑 UUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890 (validated)

🏗️  Infrastructure: 1 (CNV Multi-Node)

🔐 Authentication: 1 (htpasswd)

🧩 Workload Selection

Technologies: ansible aap, openshift ai

Recommended workloads:
✓ rhpds.ocp4_workload_authentication.ocp4_workload_authentication
✓ rhpds.showroom.ocp4_workload_showroom
✓ rhpds.aap25.ocp4_workload_aap25
✓ rhpds.openshift_ai.ocp4_workload_openshift_ai

📚 Showroom: https://github.com/rhpds/showroom-ansible-ai

📝 Display name: Ansible Automation with OpenShift AI
📝 Description: Learn to build intelligent automation using Ansible and OpenShift AI
📝 Directory: ansible-ai-workshop

👥 Multi-user: Y (30 users)

📄 Extract description from Showroom: Y

💾 Writing files to: agd_v2/ansible-ai-workshop/
  ✓ common.yaml
  ✓ dev.yaml  
  ✓ description.adoc
  ✓ info-message-template.adoc

🚀 Commit: Y

✓ Committed to branch: add-ansible-ai-workshop

Next steps:
  1. Validate: /agnosticv-validator
  2. Push: git push origin add-ansible-ai-workshop
  3. Create PR: gh pr create --fill
```

### Example 2: Description Only

```
User: /agnosticv-catalog-builder

What would you like to create or update?
Your choice [1-3]: 2

Q: AgnosticV repository path: [your_agv_path]

🔧 Git Workflow Setup
Current branch: update-ocp-pipelines
⚠️  You're on: update-ocp-pipelines
Switch to main? Y

📥 Pulling main...
Q: Branch name: update-ocp-pipelines-description

📚 Showroom path: ~/work/code/showroom-ocp-pipelines

✓ Found 5 modules

Auto-extracted:
  ✓ Modules: Introduction, Deploy App, Create Pipeline, Add Tests, Deploy to Prod
  ✓ Author: Prakhar Srivastava
  ✓ Guide: https://rhpds.github.io/showroom-ocp-pipelines

Q: Overview: OpenShift Pipelines enables cloud-native CI/CD using Tekton...

Q: Technologies: OpenShift 4.17, OpenShift Pipelines 1.15

Q: Warnings: [none]

📂 Output location: 1 (Auto-detect)

Found: agd_v2/openshift-pipelines-intro/

💾 Writing description.adoc

🚀 Commit: Y

✓ Updated description.adoc
```

### Example 3: Info Message Template Only

```
User: /agnosticv-catalog-builder

Your choice [1-3]: 3

Q: AgnosticV repository path: [your_agv_path]

🔧 Git Workflow Setup
Q: Branch name: add-litellm-info-message

📂 Catalog: [your_agv_path]/agd_v2/litellm-virtual-keys/

📧 Info Message Template

Q: Uses agnosticd_user_info? Y

Q: Data keys: litellm_api_base_url, litellm_virtual_key, litellm_available_models_list

ℹ️  How to share data from your workload:

In tasks/workload.yml:
- name: Save LiteMaaS credentials
  agnosticd.core.agnosticd_user_info:
    data:
      litellm_api_base_url: "{{ litellm_api_base_url }}"
      litellm_virtual_key: "{{ litellm_virtual_key }}"
      litellm_available_models_list: "{{ litellm_available_models | join(', ') }}"

Template usage:
* API URL: {litellm_api_base_url}
* API Key: {litellm_virtual_key}
* Models: {litellm_available_models_list}

💾 Writing info-message-template.adoc

🚀 Commit: Y

✓ Created info-message-template.adoc
```

---

## References

### Related Skills
- `/agnosticv-validator` - Validate catalog configuration
- `/create-lab` - Create Showroom workshop content
- `/ftl` - Create graders/solvers for workshop testing

### Documentation
- `~/.claude/docs/workload-mappings.md` - Technology to workload mapping
- `~/.claude/docs/infrastructure-guide.md` - Infrastructure selection guide

### Key Files Generated

**common.yaml** - Main catalog configuration
```yaml
asset_uuid: <uuid>
name: Display Name
description: Brief description
category: Workshops|Demos|Sandboxes
cloud_provider: equinix_metal|ec2
sandbox_architecture: standard|single-node
num_users: <number>
student_guide_url: <github-pages>
workloads:
  - namespace.collection.role
```

**dev.yaml** - Development overrides
```yaml
cloud_provider: "{{ cloud_provider }}"
sandbox_architecture: "{{ sandbox_architecture }}"
num_users: 1
```

**description.adoc** - UI catalog description
```asciidoc
= Display Name

== Overview
Product description starting with product name...

== Guide
link:url[Open Guide]

== Featured Products
* Product Version

== Agenda
* Module titles

== Authors
* Name - contact
```

**info-message-template.adoc** - User notification template
```asciidoc
= Environment Provisioned

== Access Information
* Console: {openshift_console_url}
* Username: {openshift_cluster_admin_username}

== Additional Data
* Service URL: {custom_data_key}

Variables come from agnosticd_user_info.data
```

---

## Troubleshooting

### Branch Creation Fails

**Problem:** `fatal: A branch named 'X' already exists`

**Solution:**
```bash
# List branches
git branch -a

# Delete local branch if needed
git branch -D old-branch-name

# Or use different name
```

### UUID Collision

**Problem:** Generated UUID already exists

**Solution:** Skill auto-regenerates. If persistent, check for corrupted catalogs.

### Showroom Not Detected

**Problem:** Cannot find `content/modules/ROOT/pages/`

**Solution:**
```bash
# Verify structure
ls -la ~/path/to/showroom/content/modules/ROOT/pages/

# Should contain .adoc files
```

### Git Not Clean

**Problem:** Uncommitted changes prevent branch creation

**Solution:**
```bash
# Stash changes
git stash

# Or commit them first
git add .
git commit -m "WIP"
```

### Workload Not Found

**Problem:** Selected workload doesn't exist in collections

**Solution:** Check `~/.claude/docs/workload-mappings.md` for correct namespace.collection.role format

---

## Important Reminders

### ⚠️ Branch Naming
- **NO** `feature/` prefix
- **YES** descriptive names: `add-catalog-name`, `update-description`

### ⚠️ Description Overview
- **NO** starting with "This workshop/demo/lab..."
- **YES** starting with product name: "OpenShift Pipelines enables..."

### ⚠️ Category Values
- Must be **exact match**: `Workshops`, `Demos`, or `Sandboxes`
- Plural form required
- Case-sensitive

### ⚠️ Info Message Variables
- List/array variables from Ansible don't render in AsciiDoc
- Convert to strings: `{{ my_list | join(', ') }}`
- Example: `litellm_available_models_list: "{{ litellm_available_models | join(', ') }}"`

### ⚠️ Git Workflow
- Always pull main first
- Create new branch for each catalog
- Commit with descriptive messages
- Test before creating PR

---

## Success Criteria

After using this skill, you should have:

**For Full Catalog:**
- ✅ Clean git branch (pulled main, no feature/ prefix)
- ✅ Four files created (common.yaml, dev.yaml, description.adoc, info-message-template.adoc)
- ✅ Valid UUID (lowercase, RFC 4122, unique)
- ✅ Correct category (exact match)
- ✅ Appropriate workloads for technologies
- ✅ Showroom integration configured
- ✅ Ready for validation and PR

**For Description Only:**
- ✅ Clean git branch
- ✅ description.adoc with extracted content
- ✅ Overview starts with product name
- ✅ Module agenda from Showroom
- ✅ Author and contact info
- ✅ GitHub Pages link

**For Info Message Template:**
- ✅ Clean git branch
- ✅ info-message-template.adoc with user data placeholders
- ✅ Documented how to use agnosticd_user_info
- ✅ String formatting for lists/arrays
- ✅ Clear variable names

---

## Version History

- **2.1.0** (2026-02-03) - UX improvements: respect CLAUDE.md config, optional git workflow, no agd_v2/ assumption
- **2.0.0** (2026-01-22) - Unified skill combining agv-generator and generate-agv-description
- **1.0.0** (2026-01-15) - Initial separate skills (deprecated)

---

**End of Skill Documentation**
