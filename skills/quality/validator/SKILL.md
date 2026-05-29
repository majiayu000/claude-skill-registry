---
name: agnosticv:validator
description: Validate AgnosticV catalog configurations against best practices and deployment requirements
---

---
context: main
model: sonnet
---

# Skill: agnosticv-validator

**Name:** AgnosticV Catalog Validator
**Description:** Validate AgnosticV configurations against best practices and deployment requirements
**Version:** 1.0.0
**Last Updated:** 2026-01-22

---

## Purpose

Comprehensive validation of AgnosticV catalog configurations before deployment. Checks UUID format, YAML syntax, workload dependencies, category correctness, and best practices to prevent deployment failures.

## Workflow Diagram

![Workflow](workflow.svg)

## What You'll Need Before Starting

Have these ready before running this skill:

**Required:**
- 📁 **Path to catalog directory** - Location of the catalog you want to validate
  - Example: `~/work/code/agnosticv/agd_v2/my-workshop`
  - Example: `/path/to/agnosticv/catalogs/my-demo`
  - Can be relative path if you're in the AgV repo

**The catalog should have:**
- ✅ **common.yaml** (minimum requirement)
- 📋 Optional: dev.yaml, prod.yaml, description.adoc

**Access needed:**
- ✅ Read permissions to the catalog directory
- ✅ Read permissions to AgnosticV repository

**What gets validated:**
- UUID format and uniqueness
- YAML syntax (common.yaml, dev.yaml, prod.yaml)
- Workload dependencies and availability
- Category correctness and structure
- Infrastructure recommendations
- Best practices compliance
- Asset metadata completeness

**Good to know:**
- Validation produces errors (must fix), warnings (should fix), and suggestions (nice to have)
- Best run BEFORE creating a PR
- Can run multiple times as you fix issues

---

## When to Use This Skill

Use `/agnosticv-validator` when you need to:

- Validate a new catalog before creating PR
- Troubleshoot catalog deployment failures
- Check catalog quality before testing in RHDP
- Verify updates to existing catalogs
- Ensure best practices compliance

**Prerequisites:**
- AgnosticV repository cloned locally
- Catalog files exist (common.yaml minimum)
- Git configured and repository accessible

---

## Skill Workflow Overview

```
Step 1: Path Detection (Auto-detect or ask)
  ↓
Step 2: Validation Scope Selection
  ↓
Step 3: Run Validation Checks
  ↓
Step 4: Generate Report (Errors/Warnings/Suggestions)
  ↓
Step 5: Offer Follow-up Actions
```

---

## Configuration Detection

### Get AgnosticV Repository Path (For Full Repo Validation)

**Check configuration files for AgV repository path:**

Checks these locations in order:
1. `~/CLAUDE.md`
2. `~/claude/*.md`
3. `~/.claude/*.md`

```bash
# Check configuration files for AgV path (multiple locations)
agv_repo_path=""

# Check ~/CLAUDE.md first
if [[ -f ~/CLAUDE.md ]]; then
  agv_repo_path=$(grep -E "agnosticv.*:" ~/CLAUDE.md | grep -oE '(~|/)[^ ]+' | head -1)
fi

# Check ~/claude/*.md if not found
if [[ -z "$agv_repo_path" ]]; then
  for file in ~/claude/*.md; do
    [[ -f "$file" ]] && agv_repo_path=$(grep -E "agnosticv.*:" "$file" | grep -oE '(~|/)[^ ]+' | head -1)
    [[ -n "$agv_repo_path" ]] && break
  done
fi

# Check ~/.claude/*.md if still not found
if [[ -z "$agv_repo_path" ]]; then
  for file in ~/.claude/*.md; do
    [[ -f "$file" ]] && agv_repo_path=$(grep -E "agnosticv.*:" "$file" | grep -oE '(~|/)[^ ]+' | head -1)
    [[ -n "$agv_repo_path" ]] && break
  done
fi

# Expand tilde if present
[[ "$agv_repo_path" =~ ^~ ]] && agv_repo_path="${agv_repo_path/#\~/$HOME}"
```

**If found in configuration:**
```
✓ Found AgV repository path: [path from configuration]
```

**If NOT found, will ask when needed for full repository validation.**

---

## Step 1: Smart Path Detection (FIRST)

### Auto-detect Catalog Location

**Check current directory for AgV catalog structure:**

```bash
# Look for common.yaml in current directory or parent
if [ -f "common.yaml" ]; then
  CATALOG_PATH=$(pwd)
elif [ -f "../common.yaml" ]; then
  CATALOG_PATH=$(cd .. && pwd)
elif [ -f "../../common.yaml" ]; then
  CATALOG_PATH=$(cd ../.. && pwd)
fi

# Verify it's an AgV catalog
if [ -f "$CATALOG_PATH/common.yaml" ]; then
  # Extract catalog slug from path
  CATALOG_SLUG=$(basename $CATALOG_PATH)
  CATALOG_DIR=$(basename $(dirname $CATALOG_PATH))
fi
```

### Ask User

```
🔍 AgnosticV Catalog Validator

I'll validate your AgnosticV catalog configuration.

Current directory: {{ current_directory }}

{% if common_yaml_detected %}
✅ Detected catalog:
   Path: {{ detected_catalog_path }}
   Directory: {{ catalog_dir }}/{{ catalog_slug }}

Use this catalog? [Yes/No/Specify different path]
{% else %}
No catalog detected in current directory.

Options:
1. Specify catalog path (e.g., ~/work/code/agnosticv/agd_v2/my-catalog)
2. Validate entire AgnosticV repository (all catalogs)
3. Exit

Your choice: [1/2/3]
{% endif %}
```

### Path Validation

```python
import os

if os.path.exists(catalog_path):
  if os.path.isfile(f"{catalog_path}/common.yaml"):
    ✅ Valid catalog path
    Path: {{ catalog_path }}
    
    # Extract catalog information
    catalog_slug = os.path.basename(catalog_path)
    catalog_dir = os.path.basename(os.path.dirname(catalog_path))
    
    Files found:
    ✓ common.yaml
    {{ '✓ description.adoc' if os.path.exists(f"{catalog_path}/description.adoc") else '⚠ description.adoc (missing)' }}
    {{ '✓ dev.yaml' if os.path.exists(f"{catalog_path}/dev.yaml") else 'ℹ dev.yaml (optional, not found)' }}
    
  else:
    ❌ Path exists but no common.yaml found
    
    Expected file: {{ catalog_path }}/common.yaml
    
    Is this an AgV catalog directory? [Yes - Continue anyway / No - Try different path]
else:
  ❌ Path not found: {{ catalog_path }}
  
  Try again? [Yes/No]
```

**Store validated path** for validation checks.

---

## Step 2: Validation Scope Selection

```
Q: What level of validation do you want?

1. ⚡ Quick check (file structure, UUID, basic YAML)
   Duration: ~5 seconds
   Checks: Essential blocking issues only
   
2. ✅ Standard validation (recommended)
   Duration: ~15-30 seconds
   Checks: Files, UUID, YAML, workloads, schema, best practices
   
3. 🔬 Full validation (everything + GitHub API)
   Duration: ~30-60 seconds
   Checks: Standard + GitHub tag/branch validation, collection URLs

Recommended: 2 (Standard)

Your choice: [1/2/3]
```

**Set validation scope:**

```python
if choice == 1:
  validation_scope = "quick"
  checks_to_run = ["file_structure", "uuid", "yaml_syntax"]
  
elif choice == 2:
  validation_scope = "standard"
  checks_to_run = ["file_structure", "uuid", "yaml_syntax", "category",
                   "workloads", "authentication", "showroom", "infrastructure",
                   "stage_files", "multiuser", "bastion", "collections",
                   "deployer", "reporting_labels", "components", "asciidoc",
                   "best_practices"]

elif choice == 3:
  validation_scope = "full"
  checks_to_run = ["file_structure", "uuid", "yaml_syntax", "category",
                   "workloads", "authentication", "showroom", "infrastructure",
                   "stage_files", "multiuser", "bastion", "collections",
                   "deployer", "reporting_labels", "components", "asciidoc",
                   "best_practices", "github_api", "collection_urls", "scm_refs"]
```

---

## Step 3: Run Validation Checks

### Initialize Error Collection

```python
errors = []         # ERRORS (must fix) - Block deployment
warnings = []       # WARNINGS (should fix) - May cause issues  
suggestions = []    # SUGGESTIONS (nice to have) - Best practices
passed_checks = []  # Passed checks for summary
```

### Check 1: File Structure

```python
def check_file_structure(catalog_path):
  """Required files validation"""
  
  required_files = ["common.yaml"]
  recommended_files = ["description.adoc", "dev.yaml"]
  
  # Check required
  for file in required_files:
    filepath = f"{catalog_path}/{file}"
    if os.path.exists(filepath):
      passed_checks.append(f"✓ Required file present: {file}")
    else:
      errors.append({
        'check': 'file_structure',
        'severity': 'ERROR',
        'message': f'Missing required file: {file}',
        'location': catalog_path,
        'fix': f'Create {file} in catalog directory'
      })
  
  # Check recommended
  for file in recommended_files:
    filepath = f"{catalog_path}/{file}"
    if not os.path.exists(filepath):
      warnings.append({
        'check': 'file_structure',
        'severity': 'WARNING',
        'message': f'Recommended file missing: {file}',
        'location': catalog_path,
        'fix': f'Create {file} for better catalog quality'
      })
```

### Check 2: UUID Format and Uniqueness

```python
import re
import yaml

def check_uuid(catalog_path, agv_repo_path):
  """UUID validation - CRITICAL"""
  
  # Load common.yaml
  with open(f"{catalog_path}/common.yaml") as f:
    config = yaml.safe_load(f)
  
  # Check if UUID exists
  if '__meta__' not in config:
    errors.append({
      'check': 'uuid',
      'severity': 'ERROR',
      'message': 'Missing __meta__ section',
      'location': 'common.yaml',
      'fix': 'Add __meta__ section with asset_uuid'
    })
    return
  
  if 'asset_uuid' not in config['__meta__']:
    errors.append({
      'check': 'uuid',
      'severity': 'ERROR',
      'message': 'Missing __meta__.asset_uuid',
      'location': 'common.yaml:__meta__',
      'fix': 'Generate UUID with: uuidgen'
    })
    return
  
  uuid = config['__meta__']['asset_uuid']
  
  # Validate UUID format (RFC 4122)
  uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
  
  if not re.match(uuid_pattern, str(uuid).lower()):
    errors.append({
      'check': 'uuid',
      'severity': 'ERROR',
      'message': f'Invalid UUID format: {uuid}',
      'location': 'common.yaml:__meta__.asset_uuid',
      'fix': 'Generate proper UUID with: uuidgen',
      'example': '5ac92190-6f0d-4c0e-a9bd-3b20dd3c816f'
    })
    return
  
  # Check for UUID collision
  collision = search_uuid_in_repo(uuid, agv_repo_path, current_catalog=catalog_path)
  
  if collision:
    errors.append({
      'check': 'uuid',
      'severity': 'ERROR',
      'message': f'UUID collision detected',
      'location': 'common.yaml:__meta__.asset_uuid',
      'details': f'UUID {uuid} already used in: {collision["path"]}',
      'catalog': collision["name"],
      'fix': 'Generate new unique UUID with: uuidgen'
    })
    return
  
  passed_checks.append(f"✓ UUID format valid: {uuid}")
  passed_checks.append(f"✓ UUID is unique")

def search_uuid_in_repo(uuid, repo_path, current_catalog):
  """Search for UUID in all catalogs"""
  import glob
  
  for catalog in glob.glob(f"{repo_path}/**/common.yaml", recursive=True):
    if os.path.dirname(catalog) == current_catalog:
      continue  # Skip current catalog
    
    with open(catalog) as f:
      try:
        config = yaml.safe_load(f)
        if config.get('__meta__', {}).get('asset_uuid') == uuid:
          return {
            'path': catalog,
            'name': config.get('__meta__', {}).get('catalog', {}).get('display_name', 'Unknown')
          }
      except:
        continue
  
  return None
```

### Check 3: Category Validation

```python
def check_category(config):
  """Category correctness validation"""

  valid_categories = ["Workshops", "Demos", "Sandboxes", "Labs", "Brand_Events"]

  if '__meta__' not in config or 'catalog' not in config['__meta__']:
    errors.append({
      'check': 'category',
      'severity': 'ERROR',
      'message': 'Missing __meta__.catalog section',
      'location': 'common.yaml',
      'fix': 'Add __meta__.catalog section with category'
    })
    return

  category = config['__meta__']['catalog'].get('category')

  if not category:
    errors.append({
      'check': 'category',
      'severity': 'ERROR',
      'message': 'Missing __meta__.catalog.category',
      'location': 'common.yaml:__meta__.catalog',
      'fix': f'Add category: {valid_categories}'
    })
    return

  if category not in valid_categories:
    errors.append({
      'check': 'category',
      'severity': 'ERROR',
      'message': f'Invalid category: "{category}"',
      'location': 'common.yaml:__meta__.catalog.category',
      'current': category,
      'valid_options': valid_categories,
      'fix': f'Use one of: {", ".join(valid_categories)} (case-sensitive)'
    })
    return

  passed_checks.append(f"✓ Category valid: {category}")

  # Validate category alignment with configuration
  multiuser = config['__meta__']['catalog'].get('multiuser', False)

  if category in ["Workshops", "Brand_Events"] and not multiuser:
    warnings.append({
      'check': 'category',
      'severity': 'WARNING',
      'message': f'Category "{category}" typically requires multiuser: true',
      'location': 'common.yaml:__meta__.catalog',
      'recommendation': 'Set multiuser: true for workshop/event catalogs'
    })

  if category == "Demos" and multiuser:
    errors.append({
      'check': 'category',
      'severity': 'ERROR',
      'message': 'Category "Demos" should not be multi-user',
      'location': 'common.yaml:__meta__.catalog',
      'current': 'multiuser: true',
      'expected': 'multiuser: false',
      'fix': 'Set multiuser: false for demos'
    })

  # Check workshopLabUiRedirect - should NOT be enabled for demos
  workshop_ui_redirect = config['__meta__']['catalog'].get('workshopLabUiRedirect', False)

  if category == "Demos" and workshop_ui_redirect:
    errors.append({
      'check': 'category',
      'severity': 'ERROR',
      'message': 'Demos should not have workshopLabUiRedirect enabled',
      'location': 'common.yaml:__meta__.catalog',
      'current': 'workshopLabUiRedirect: true',
      'fix': 'Remove workshopLabUiRedirect or set to false for demos'
    })
```

### Check 4: YAML Syntax

```python
def check_yaml_syntax(catalog_path):
  """YAML syntax validation"""
  
  files_to_check = ["common.yaml", "dev.yaml"]
  
  for filename in files_to_check:
    filepath = f"{catalog_path}/{filename}"
    
    if not os.path.exists(filepath):
      continue
    
    try:
      with open(filepath) as f:
        yaml.safe_load(f)
      passed_checks.append(f"✓ {filename} syntax valid")
    except yaml.YAMLError as e:
      errors.append({
        'check': 'yaml_syntax',
        'severity': 'ERROR',
        'message': f'YAML syntax error in {filename}',
        'location': f'{filename}:line {e.problem_mark.line if hasattr(e, "problem_mark") else "?"}',
        'details': str(e),
        'fix': 'Fix YAML syntax errors'
      })
```

### Check 5: Workload Dependencies

```python
def check_workload_dependencies(config):
  """Workload and collection dependency validation"""
  
  if 'workloads' not in config:
    errors.append({
      'check': 'workloads',
      'severity': 'ERROR',
      'message': 'No workloads defined',
      'location': 'common.yaml',
      'fix': 'Add workloads list'
    })
    return
  
  workloads = config.get('workloads', [])
  collections = config.get('requirements_content', {}).get('collections', [])
  
  # Extract collection names
  collection_names = []
  for coll in collections:
    if 'name' in coll:
      # Extract org/repo from GitHub URL or collection name
      if 'github.com' in coll['name']:
        # https://github.com/agnosticd/core_workloads.git → core_workloads
        repo_name = coll['name'].split('/')[-1].replace('.git', '')
        collection_names.append(repo_name)
      else:
        collection_names.append(coll['name'])
  
  # Check each workload format and dependencies
  for workload in workloads:
    # Validate format: namespace.collection.role
    parts = workload.split('.')
    
    if len(parts) < 3:
      errors.append({
        'check': 'workloads',
        'severity': 'ERROR',
        'message': f'Invalid workload format: {workload}',
        'location': 'common.yaml:workloads',
        'expected': 'namespace.collection.role_name',
        'example': 'agnosticd.core_workloads.ocp4_workload_authentication_htpasswd',
        'fix': 'Use fully qualified workload name'
      })
      continue
    
    namespace, collection, role = parts[0], parts[1], '.'.join(parts[2:])
    
    # Check if collection is in requirements
    if collection not in collection_names and collection not in ['showroom']:
      warnings.append({
        'check': 'workloads',
        'severity': 'WARNING',
        'message': f'Workload "{workload}" requires collection "{collection}"',
        'location': 'common.yaml:requirements_content.collections',
        'fix': f'Add collection to requirements_content.collections',
        'example': f'''
requirements_content:
  collections:
  - name: https://github.com/{namespace}/{collection}.git
    type: git
    version: main
'''
      })
  
  if workloads:
    passed_checks.append(f"✓ Workload format correct ({len(workloads)} workloads)")
```

### Check 6: Infrastructure Recommendations

```python
def check_infrastructure(config):
  """Infrastructure type validation and recommendations"""
  
  workloads = config.get('workloads', [])
  components = config.get('__meta__', {}).get('components', [])
  
  # Detect infrastructure type
  cluster_component = next((c for c in components if 'openshift' in c.get('name', '').lower()), None)
  
  if not cluster_component:
    warnings.append({
      'check': 'infrastructure',
      'severity': 'WARNING',
      'message': 'No OpenShift cluster component found',
      'location': 'common.yaml:__meta__.components',
      'recommendation': 'Add cluster component if OpenShift-based'
    })
    return
  
  cluster_item = cluster_component.get('item', '')
  cluster_size = cluster_component.get('parameter_values', {}).get('cluster_size', '')
  
  # Check GPU workloads on non-AWS
  gpu_workloads = [w for w in workloads if 'gpu' in w.lower() or 'nvidia' in w.lower()]
  
  if gpu_workloads and 'aws' not in cluster_item.lower():
    warnings.append({
      'check': 'infrastructure',
      'severity': 'WARNING',
      'message': 'GPU workloads detected but not using AWS infrastructure',
      'workloads': gpu_workloads,
      'current_infrastructure': cluster_item,
      'recommendation': 'GPU workloads require AWS with g6.4xlarge instances',
      'fix': 'Change to AWS infrastructure or remove GPU workloads'
    })
  
  # Check heavy workloads on SNO
  if cluster_size == 'sno':
    heavy_workloads = [w for w in workloads if any(tech in w for tech in ['openshift_ai', 'acs', 'service_mesh'])]
    
    if len(workloads) > 5 or heavy_workloads:
      warnings.append({
        'check': 'infrastructure',
        'severity': 'WARNING',
        'message': 'Heavy workloads on SNO (Single Node OpenShift)',
        'workloads': heavy_workloads if heavy_workloads else f'{len(workloads)} workloads',
        'recommendation': 'SNO best for lightweight demos, consider CNV multi-node',
        'resource_concern': 'SNO has limited resources (32Gi RAM, 16 cores)'
      })
  
  # Multi-user on SNO
  multiuser = config.get('__meta__', {}).get('catalog', {}).get('multiuser', False)
  
  if multiuser and cluster_size == 'sno':
    errors.append({
      'check': 'infrastructure',
      'severity': 'ERROR',
      'message': 'Multi-user enabled on SNO infrastructure',
      'location': 'common.yaml',
      'issue': 'SNO cannot support multiple concurrent users',
      'fix': 'Change to CNV multi-node or set multiuser: false'
    })
  
  passed_checks.append(f"✓ Infrastructure type: {cluster_size}")
```

### Check 7: Authentication Configuration

```python
def check_authentication(config):
  """Authentication workload validation"""
  
  workloads = config.get('workloads', [])
  
  auth_workloads = [w for w in workloads if 'authentication' in w]
  
  if not auth_workloads:
    errors.append({
      'check': 'authentication',
      'severity': 'ERROR',
      'message': 'No authentication workload configured',
      'location': 'common.yaml:workloads',
      'fix': 'Add authentication workload (htpasswd or keycloak)',
      'examples': [
        'agnosticd.core_workloads.ocp4_workload_authentication_htpasswd',
        'agnosticd.core_workloads.ocp4_workload_authentication_keycloak'
      ]
    })
    return
  
  if len(auth_workloads) > 1:
    warnings.append({
      'check': 'authentication',
      'severity': 'WARNING',
      'message': 'Multiple authentication workloads detected',
      'workloads': auth_workloads,
      'recommendation': 'Usually only one authentication method is needed'
    })
  
  # Check authentication variables
  if 'htpasswd' in auth_workloads[0]:
    required_vars = [
      'ocp4_workload_authentication_htpasswd_admin_user',
      'ocp4_workload_authentication_htpasswd_admin_password',
      'ocp4_workload_authentication_htpasswd_user_count'
    ]
    
    for var in required_vars:
      if var not in config:
        warnings.append({
          'check': 'authentication',
          'severity': 'WARNING',
          'message': f'Missing htpasswd variable: {var}',
          'location': 'common.yaml',
          'fix': f'Add {var} configuration'
        })
  
  passed_checks.append(f"✓ Authentication configured: {auth_workloads[0].split('.')[-1]}")
```

### Check 8: Showroom Integration

```python
def check_showroom(config):
  """Showroom workload and configuration validation"""
  
  workloads = config.get('workloads', [])
  
  showroom_workloads = [w for w in workloads if 'showroom' in w]
  
  if showroom_workloads:
    # Check for showroom repo configuration
    showroom_vars = [k for k in config.keys() if 'showroom_content_git_repo' in k]
    
    if not showroom_vars:
      errors.append({
        'check': 'showroom',
        'severity': 'ERROR',
        'message': 'Showroom workload present but no git repository configured',
        'location': 'common.yaml',
        'fix': 'Add ocp4_workload_showroom_content_git_repo variable',
        'example': 'ocp4_workload_showroom_content_git_repo: https://github.com/rhpds/repo.git'
      })
    else:
      repo_url = config.get(showroom_vars[0], '')
      
      # Check for SSH format (should be HTTPS)
      if repo_url.startswith('git@github.com:'):
        warnings.append({
          'check': 'showroom',
          'severity': 'WARNING',
          'message': 'Showroom git repository uses SSH format',
          'location': f'common.yaml:{showroom_vars[0]}',
          'current': repo_url,
          'recommendation': 'Use HTTPS format for user cloning',
          'suggested': repo_url.replace('git@github.com:', 'https://github.com/').replace('.git', '.git')
        })
      
      passed_checks.append(f"✓ Showroom integration configured")
```

### Check 9: Best Practices

```python
def check_best_practices(config):
  """Best practice recommendations"""
  
  # Check for display_name
  display_name = config.get('__meta__', {}).get('catalog', {}).get('display_name', '')
  
  if len(display_name) > 60:
    suggestions.append({
      'check': 'best_practices',
      'message': 'Display name is quite long',
      'current_length': len(display_name),
      'recommendation': 'Keep display names under 60 characters for better UX'
    })
  
  # Check for keywords
  keywords = config.get('__meta__', {}).get('catalog', {}).get('keywords', [])
  
  if len(keywords) < 3:
    suggestions.append({
      'check': 'best_practices',
      'message': 'Few keywords defined',
      'current': len(keywords),
      'recommendation': 'Add 3-5 keywords for better discoverability'
    })
  
  # Check for abstract
  if 'abstract' not in config.get('__meta__', {}).get('catalog', {}):
    suggestions.append({
      'check': 'best_practices',
      'message': 'No abstract defined in catalog metadata',
      'recommendation': 'Add abstract for catalog description'
    })
  
  # Check for owners/maintainers
  if 'owners' not in config.get('__meta__', {}):
    suggestions.append({
      'check': 'best_practices',
      'message': 'No maintainer/owner defined',
      'recommendation': 'Add __meta__.owners.maintainer for accountability'
    })
```

### Check 10: Stage Files Validation

```python
def check_stage_files(catalog_path):
  """Validate stage-specific override files"""

  stage_files = {
    'dev.yaml': {
      'required': True,
      'expected_purpose': 'development'
    },
    'event.yaml': {
      'required': False,
      'expected_purpose': 'events'
    },
    'prod.yaml': {
      'required': False,
      'expected_purpose': 'production'
    }
  }

  for filename, requirements in stage_files.items():
    filepath = f"{catalog_path}/{filename}"

    if os.path.exists(filepath):
      try:
        with open(filepath) as f:
          stage_config = yaml.safe_load(f)

        # Check purpose field
        if 'purpose' in stage_config:
          purpose = stage_config['purpose']
          expected = requirements['expected_purpose']

          if purpose != expected:
            warnings.append({
              'check': 'stage_files',
              'severity': 'WARNING',
              'message': f'{filename} has unexpected purpose value',
              'location': f'{filename}:purpose',
              'current': purpose,
              'expected': expected,
              'recommendation': f'Set purpose: {expected}'
            })
          else:
            passed_checks.append(f"✓ {filename} purpose correct: {purpose}")

        # Check scm_ref differentiation for event/prod
        if filename in ['event.yaml', 'prod.yaml']:
          scm_ref = stage_config.get('__meta__', {}).get('deployer', {}).get('scm_ref')

          if scm_ref == 'main':
            suggestions.append({
              'check': 'stage_files',
              'message': f'{filename} uses scm_ref: main',
              'recommendation': 'Consider using tagged release (e.g., catalog-name-1.0.0) for production stability'
            })

      except yaml.YAMLError:
        # YAML syntax errors handled elsewhere
        pass

    elif requirements['required']:
      warnings.append({
        'check': 'stage_files',
        'severity': 'WARNING',
        'message': f'Missing {filename}',
        'location': catalog_path,
        'fix': f'Create {filename} with purpose: {requirements["expected_purpose"]}'
      })
```

### Check 11: Multi-User Configuration

```python
def check_multiuser_config(config):
  """Multi-user specific validation"""

  multiuser = config.get('__meta__', {}).get('catalog', {}).get('multiuser', False)

  if not multiuser:
    return  # Skip checks for single-user catalogs

  # Check num_users parameter exists
  parameters = config.get('__meta__', {}).get('catalog', {}).get('parameters', [])
  num_users_param = next((p for p in parameters if p.get('name') == 'num_users'), None)

  if not num_users_param:
    errors.append({
      'check': 'multiuser',
      'severity': 'ERROR',
      'message': 'Multi-user catalog missing num_users parameter',
      'location': 'common.yaml:__meta__.catalog.parameters',
      'fix': 'Add num_users parameter with min/max values'
    })
    return

  # Validate num_users schema
  schema = num_users_param.get('openAPIV3Schema', {})

  if not schema:
    errors.append({
      'check': 'multiuser',
      'severity': 'ERROR',
      'message': 'num_users parameter missing openAPIV3Schema',
      'location': 'common.yaml:__meta__.catalog.parameters',
      'fix': 'Add openAPIV3Schema with type: integer, default, minimum, maximum'
    })
    return

  # Check for worker scaling configuration
  if 'worker_instance_count' in config:
    worker_formula = str(config['worker_instance_count'])

    if 'num_users' not in worker_formula:
      warnings.append({
        'check': 'multiuser',
        'severity': 'WARNING',
        'message': 'worker_instance_count does not scale with num_users',
        'location': 'common.yaml:worker_instance_count',
        'current': config['worker_instance_count'],
        'recommendation': 'Use formula based on num_users for multi-user scaling'
      })
    else:
      passed_checks.append(f"✓ Worker scaling formula includes num_users")

  # Check SalesforceID for large deployments
  max_users = schema.get('maximum', 0)

  if max_users > 10:
    salesforce_params = [p for p in parameters if 'salesforce' in p.get('name', '').lower()]

    if not salesforce_params:
      suggestions.append({
        'check': 'multiuser',
        'message': f'Large deployment (max {max_users} users) without SalesforceID parameter',
        'recommendation': 'Add SalesforceID parameter for tracking large deployments'
      })

  # Check workshopLabUiRedirect for multi-user workshops
  catalog = config.get('__meta__', {}).get('catalog', {})
  category = catalog.get('category', '')
  workshop_ui_redirect = catalog.get('workshopLabUiRedirect', False)

  if category in ['Workshops', 'Brand_Events'] and multiuser and not workshop_ui_redirect:
    warnings.append({
      'check': 'multiuser',
      'severity': 'WARNING',
      'message': 'Multi-user workshop without workshopLabUiRedirect enabled',
      'location': 'common.yaml:__meta__.catalog',
      'recommendation': 'Set workshopLabUiRedirect: true for multi-user workshops',
      'fix': 'Add workshopLabUiRedirect: true to enable lab UI routing per user'
    })

  passed_checks.append(f"✓ Multi-user configuration present (max {max_users} users)")
```

### Check 12: Bastion Configuration

```python
def check_bastion_config(config):
  """Bastion instance validation for CNV/AWS catalogs"""

  cloud_provider = config.get('cloud_provider', '')

  # Only check bastion for CNV and AWS
  if cloud_provider not in ['openshift_cnv', 'aws', 'none']:
    return

  # Check bastion image
  bastion_image = config.get('bastion_instance_image', config.get('default_instance_image', ''))

  if bastion_image:
    valid_images = ['rhel-9.4', 'rhel-9.5', 'rhel-9.6', 'rhel-10.0', 'RHEL-10.0-GOLD-latest']

    if not any(img in bastion_image for img in valid_images):
      warnings.append({
        'check': 'bastion',
        'severity': 'WARNING',
        'message': f'Unusual bastion image: {bastion_image}',
        'location': 'common.yaml:bastion_instance_image',
        'valid_images': valid_images,
        'recommendation': 'Use supported RHEL 9.x or 10.x images'
      })
    else:
      passed_checks.append(f"✓ Bastion image valid: {bastion_image}")

  # Check bastion resources
  bastion_cores = config.get('bastion_cores')
  bastion_memory = config.get('bastion_memory')

  if bastion_cores and int(str(bastion_cores).replace('G', '').replace('i', '')) < 2:
    warnings.append({
      'check': 'bastion',
      'severity': 'WARNING',
      'message': f'Bastion has low CPU: {bastion_cores}',
      'location': 'common.yaml:bastion_cores',
      'recommendation': 'Minimum 2 cores recommended for bastion'
    })

  if bastion_memory and int(str(bastion_memory).replace('G', '').replace('i', '')) < 4:
    warnings.append({
      'check': 'bastion',
      'severity': 'WARNING',
      'message': f'Bastion has low memory: {bastion_memory}',
      'location': 'common.yaml:bastion_memory',
      'recommendation': 'Minimum 4Gi recommended for bastion'
    })
```

### Check 13: Collection Versions

```python
def check_collection_versions(config):
  """Validate git collection versions are specified"""

  collections = config.get('requirements_content', {}).get('collections', [])

  if not collections:
    warnings.append({
      'check': 'collections',
      'severity': 'WARNING',
      'message': 'No collections defined',
      'location': 'common.yaml:requirements_content.collections',
      'recommendation': 'Add required collections for workloads'
    })
    return

  for coll in collections:
    coll_name = coll.get('name', '')
    coll_type = coll.get('type', '')
    coll_version = coll.get('version', '')

    if coll_type == 'git' or 'github.com' in coll_name:
      if not coll_version:
        errors.append({
          'check': 'collections',
          'severity': 'ERROR',
          'message': f'Git collection missing version: {coll_name}',
          'location': 'common.yaml:requirements_content.collections',
          'fix': 'Add version: main (or specific tag/commit)'
        })
      elif coll_version == 'HEAD':
        warnings.append({
          'check': 'collections',
          'severity': 'WARNING',
          'message': f'Collection uses HEAD: {coll_name}',
          'location': 'common.yaml:requirements_content.collections',
          'recommendation': 'Use specific branch or tag for reproducibility'
        })

  passed_checks.append(f"✓ Collections defined ({len(collections)} collections)")
```

### Check 14: Deployer Configuration

```python
def check_deployer_config(config):
  """Validate deployer configuration"""

  deployer = config.get('__meta__', {}).get('deployer', {})

  if not deployer:
    errors.append({
      'check': 'deployer',
      'severity': 'ERROR',
      'message': 'Missing __meta__.deployer section',
      'location': 'common.yaml:__meta__',
      'fix': 'Add deployer section with scm_url, scm_ref, execution_environment'
    })
    return

  # Check required fields
  required_fields = {
    'scm_url': 'https://github.com/agnosticd/agnosticd-v2',
    'scm_ref': 'main',
    'execution_environment': {'image': 'quay.io/agnosticd/ee-multicloud:*'}
  }

  for field, example in required_fields.items():
    if field not in deployer:
      errors.append({
        'check': 'deployer',
        'severity': 'ERROR',
        'message': f'Missing deployer.{field}',
        'location': 'common.yaml:__meta__.deployer',
        'fix': f'Add {field}',
        'example': example
      })

  # Validate EE image
  ee_image = deployer.get('execution_environment', {}).get('image', '')

  if ee_image:
    if not ee_image.startswith('quay.io/agnosticd/ee-multicloud:'):
      warnings.append({
        'check': 'deployer',
        'severity': 'WARNING',
        'message': 'Non-standard execution environment image',
        'location': 'common.yaml:__meta__.deployer.execution_environment.image',
        'current': ee_image,
        'recommendation': 'Use quay.io/agnosticd/ee-multicloud:chained-YYYY-MM-DD'
      })
    else:
      passed_checks.append(f"✓ Execution environment image valid")

  passed_checks.append(f"✓ Deployer configuration present")
```

### Check 14a: Reporting Labels (Critical)

```python
def check_reporting_labels(config):
  """Validate reporting labels for business unit tracking"""

  catalog = config.get('__meta__', {}).get('catalog', {})
  reporting_labels = catalog.get('reportingLabels', {})

  if not reporting_labels:
    warnings.append({
      'check': 'reporting_labels',
      'severity': 'WARNING',
      'message': 'Missing reportingLabels section',
      'location': 'common.yaml:__meta__.catalog',
      'recommendation': 'Add reportingLabels with primaryBU for tracking/reporting'
    })
    return

  # Check for primaryBU (very important for reporting)
  primary_bu = reporting_labels.get('primaryBU')

  if not primary_bu:
    errors.append({
      'check': 'reporting_labels',
      'severity': 'ERROR',
      'message': 'Missing reportingLabels.primaryBU',
      'location': 'common.yaml:__meta__.catalog.reportingLabels',
      'fix': 'Add primaryBU field for business unit tracking',
      'example': 'primaryBU: Hybrid_Platforms'
    })
    return

  # Validate primaryBU value (common values)
  valid_bus = [
    'Hybrid_Platforms',
    'Application_Services',
    'Ansible',
    'RHEL',
    'Middleware',
    'Cloud_Services'
  ]

  if primary_bu not in valid_bus:
    warnings.append({
      'check': 'reporting_labels',
      'severity': 'WARNING',
      'message': f'Unusual primaryBU value: {primary_bu}',
      'location': 'common.yaml:__meta__.catalog.reportingLabels.primaryBU',
      'current': primary_bu,
      'common_values': valid_bus,
      'recommendation': 'Verify primaryBU is correct business unit for tracking'
    })

  passed_checks.append(f"✓ Reporting labels configured: primaryBU={primary_bu}")
```

### Check 15: Component Propagation

```python
def check_component_propagation(config):
  """Validate multi-stage catalog component data propagation"""

  components = config.get('__meta__', {}).get('components', [])

  if not components:
    return  # Not a multi-stage catalog

  for component in components:
    comp_name = component.get('name', 'unknown')
    propagate_data = component.get('propagate_provision_data', [])

    if not propagate_data:
      warnings.append({
        'check': 'components',
        'severity': 'WARNING',
        'message': f'Component "{comp_name}" has no propagate_provision_data',
        'location': 'common.yaml:__meta__.components',
        'recommendation': 'Add propagate_provision_data to pass info between stages'
      })
      continue

    # Common required propagations for OpenShift components
    if 'openshift' in comp_name.lower():
      required_propagations = [
        'openshift_api_url',
        'openshift_cluster_admin_token',
        'bastion_public_hostname'
      ]

      for req in required_propagations:
        if not any(p.get('name') == req for p in propagate_data):
          warnings.append({
            'check': 'components',
            'severity': 'WARNING',
            'message': f'Component "{comp_name}" missing common propagation: {req}',
            'location': 'common.yaml:__meta__.components',
            'recommendation': f'Add {req} to propagate_provision_data'
          })

  passed_checks.append(f"✓ Multi-stage catalog with {len(components)} component(s)")
```

### Check 16: AsciiDoc Templates

```python
def check_asciidoc_templates(catalog_path):
  """Validate AsciiDoc template files"""

  templates = {
    'description.adoc': True,  # Required
    'info-message-template.adoc': True,  # Required
    'user-message-template.adoc': False  # Optional but recommended for multi-user
  }

  for template, required in templates.items():
    filepath = f"{catalog_path}/{template}"

    if os.path.exists(filepath):
      try:
        with open(filepath) as f:
          content = f.read()

        # Check for variable substitution syntax
        if template.endswith('-template.adoc'):
          if '{' not in content and '}' not in content:
            warnings.append({
              'check': 'asciidoc',
              'severity': 'WARNING',
              'message': f'{template} has no variable substitutions',
              'location': template,
              'recommendation': 'Add UserInfo variables like {bastion_public_hostname}'
            })
          else:
            passed_checks.append(f"✓ {template} has variable substitutions")

      except Exception as e:
        warnings.append({
          'check': 'asciidoc',
          'severity': 'WARNING',
          'message': f'Cannot read {template}: {e}',
          'location': template
        })

    elif required:
      warnings.append({
        'check': 'asciidoc',
        'severity': 'WARNING',
        'message': f'Missing {template}',
        'location': catalog_path,
        'fix': f'Create {template} for catalog documentation'
      })
```

---

## Step 4: Generate Validation Report

### Interactive Report Format

```
╔═══════════════════════════════════════════════════════════╗
║         AgV Catalog Validation Report                     ║
╚═══════════════════════════════════════════════════════════╝

Catalog: {{ catalog_display_name }}
Location: {{ catalog_path }}
Validation Level: {{ validation_scope }}
Timestamp: {{ current_timestamp }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{% if errors %}
ERRORS (must fix before deployment):

{% for error in errors %}
❌ {{ error.message }}
   Location: {{ error.location }}
   {% if error.current %}Current: {{ error.current }}{% endif %}
   {% if error.fix %}Fix: {{ error.fix }}{% endif %}
   {% if error.example %}Example: {{ error.example }}{% endif %}

{% endfor %}
{% endif %}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{% if warnings %}
WARNINGS (should fix to avoid issues):

{% for warning in warnings %}
⚠️  {{ warning.message }}
   Location: {{ warning.location }}
   {% if warning.recommendation %}Recommendation: {{ warning.recommendation }}{% endif %}
   {% if warning.fix %}Fix: {{ warning.fix }}{% endif %}

{% endfor %}
{% endif %}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{% if suggestions %}
SUGGESTIONS (nice to have):

{% for suggestion in suggestions %}
💡 {{ suggestion.message }}
   {% if suggestion.recommendation %}Why: {{ suggestion.recommendation }}{% endif %}

{% endfor %}
{% endif %}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PASSED ({{ passed_checks|length }} checks):

{% for check in passed_checks %}
{{ check }}
{% endfor %}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY:
  {% if errors %}❌ {{ errors|length }} error(s) (must fix){% endif %}
  {% if warnings %}⚠️  {{ warnings|length }} warning(s) (should fix){% endif %}
  {% if suggestions %}💡 {{ suggestions|length }} suggestion(s) (nice to have){% endif %}
  ✓ {{ passed_checks|length }} check(s) passed

STATUS: {% if errors %}❌ FAILED - Fix errors before deploying to RHDP{% elif warnings %}⚠️ PASSED WITH WARNINGS{% else %}✅ PASSED{% endif %}

Next steps:
{% if errors %}
1. Fix the {{ errors|length }} error(s) listed above
2. Run validation again: /agnosticv-validator
3. Address warnings for better quality
4. Test in RHDP Integration environment
{% elif warnings %}
1. Review and address warnings for better quality
2. Test in RHDP Integration environment
3. Create PR when ready
{% else %}
1. Catalog looks good! Test in RHDP Integration
2. Create PR for review
3. Request merge after successful testing
{% endif %}
```

---

## Step 5: Follow-up Actions

```
Would you like me to:

1. 💾 Create validation report file (validation-report.txt)
2. 🔧 Show detailed fix instructions for errors
3. 🔄 Re-run validation after you fix issues
4. 📋 Generate checklist for manual review
5. ❌ Exit

Your choice: [1/2/3/4/5]
```

### Option 1: Create Report File

```bash
cat > {{ catalog_path }}/validation-report.txt << 'EOF'
{{ full_validation_report }}
EOF

✅ Validation report saved

File: {{ catalog_path }}/validation-report.txt

You can:
- Review offline
- Share with team
- Attach to PR
- Track fixes over time
```

### Option 2: Detailed Fix Instructions

```
🔧 Detailed Fix Instructions

{% for i, error in enumerate(errors) %}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Error {{ i+1 }}: {{ error.message }}

Location: {{ error.location }}

Problem:
{{ error.details if error.details else error.message }}

How to fix:

1. Open file: {{ error.location.split(':')[0] }}

2. {% if 'UUID' in error.message %}
   Generate new UUID:
   $ uuidgen
   
   Update common.yaml:
   __meta__:
     asset_uuid: <paste-uuid-here>

{% elif 'category' in error.message %}
   Update category to valid option:
   __meta__:
     catalog:
       category: {{ error.valid_options[0] if error.valid_options else 'Workshops' }}
   
   Valid options: {{ error.valid_options|join(', ') }}

{% elif 'workload' in error.message %}
   Add missing collection:
   requirements_content:
     collections:
     - name: {{ error.example if error.example else 'https://github.com/agnosticd/collection.git' }}
       type: git
       version: main

{% else %}
   {{ error.fix }}
{% endif %}

3. Save file

4. Re-run validation: /agnosticv-validator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% endfor %}
```

### Option 3: Re-validation Loop

```
Re-run validation now? [Yes/No]

{% if Yes %}
🔄 Re-validating catalog...

(Re-run all validation checks from Step 3)

{% endif %}
```

### Option 4: Manual Review Checklist

```
📋 Manual Review Checklist

Save this checklist for comprehensive review:

## Catalog Information
- [ ] Display name is clear and descriptive
- [ ] Abstract explains purpose (starts with product name)
- [ ] Category is correct (Workshops/Demos/Sandboxes)
- [ ] Keywords are relevant (3-5 keywords)
- [ ] UUID is unique and valid format

## Infrastructure
- [ ] Infrastructure type matches requirements (CNV/SNO/AWS)
- [ ] Cluster size appropriate for workload
- [ ] GPU configuration if needed (AWS only)
- [ ] Multi-user setting aligns with category

## Workloads
- [ ] All required workloads included
- [ ] Authentication workload present
- [ ] Showroom workload for content delivery
- [ ] Technology-specific workloads match abstract
- [ ] All workload collections in requirements

## Configuration
- [ ] Showroom git repository URL is HTTPS format
- [ ] All workload variables defined
- [ ] No hardcoded values (use variables)
- [ ] dev.yaml exists for development overrides

## Testing
- [ ] Tested in RHDP Integration
- [ ] All workloads provision successfully
- [ ] Showroom content loads correctly
- [ ] UserInfo variables available
- [ ] Exercises work as documented

## Documentation
- [ ] description.adoc explains catalog purpose
- [ ] Prerequisites listed
- [ ] Learning outcomes defined
- [ ] Environment details specified
- [ ] User access instructions (if multi-user)

## Git & PR
- [ ] Branch created (no feature/ prefix)
- [ ] Files committed with clear message
- [ ] PR created with test plan
- [ ] PR description includes test results
- [ ] Ready for RHDP team review
```

---

## Error Handling

### Catalog Not Found

```
❌ Catalog Validation Failed

I couldn't find an AgnosticV catalog at: {{ provided_path }}

Common issues:
- Wrong path provided
- Not in an AgV catalog directory
- Missing common.yaml file

Try:
1. Navigate to catalog directory: cd {{ agv_path }}/agd_v2/<catalog-name>
2. Verify common.yaml exists: ls -la
3. Run validator again: /agnosticv-validator

Exit or try again? [Try again/Exit]
```

### YAML Parse Error

```
❌ Cannot Parse YAML

File: {{ file_path }}

Error: {{ yaml_error_message }}

This usually means:
- Incorrect indentation
- Missing colons or quotes
- Invalid YAML syntax

Recommendations:
1. Use YAML validator online
2. Check indentation (spaces, not tabs)
3. Validate quotes and special characters

Continue validation anyway (will skip YAML checks)? [Yes/No]
```

### Repository Access Error

```
⚠️  Cannot Access Full Repository

I can validate this catalog but cannot check UUID uniqueness across all catalogs.

Reason: {{ access_error }}

Validation will continue with reduced scope.

Limited checks:
✓ File structure
✓ YAML syntax (local catalog only)
✓ Workload format
✓ Category validation

Skipped checks:
⊘ UUID uniqueness across repository
⊘ Collection URL validation

Continue? [Yes/No]
```

---

## Skill Exit

```
{% if errors %}
❌ Validation Complete - ERRORS FOUND

You have {{ errors|length }} error(s) that must be fixed before deployment.

Next steps:
1. Review errors above
2. Fix issues in catalog files
3. Run /agnosticv-validator again
4. Repeat until all errors resolved

{% elif warnings %}
⚠️  Validation Complete - WARNINGS FOUND

Catalog will deploy but has {{ warnings|length }} warning(s).

Recommended:
1. Review warnings for quality improvements
2. Fix what makes sense
3. Test in RHDP Integration

{% else %}
✅ Validation Complete - ALL CHECKS PASSED

Catalog is ready for deployment!

Next steps:
1. Commit changes (if any)
2. Test in RHDP Integration
3. Create PR with test results
4. Request merge after successful testing

{% endif %}

👋 Exiting /agnosticv-validator
```

---

## References

- [babylon_checks.py](https://github.com/rhpds/agnosticv/blob/main/.tests/babylon_checks.py) - Validation patterns
- [Workload Mappings](../../docs/workload-mappings.md) - Technology to workload reference
- [Infrastructure Guide](../../docs/infrastructure-guide.md) - CNV/SNO/AWS decision tree

---

**Last Updated:** 2026-01-22
**Maintained By:** RHDP Team
**Version:** 1.0.0
