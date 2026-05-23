---
name: gitbook
version: 1.0.0
description: Publish documentation and books with GitBook including spaces, collections, variants, Git sync, collaboration, and API integration
author: workspace-hub
category: documentation
type: skill
capabilities:
  - Documentation publishing
  - Spaces and collections management
  - Content variants (versions)
  - Git synchronization
  - Team collaboration
  - API integration
  - Custom domains
  - Search optimization
  - Analytics
  - Visitor authentication
tools:
  - gitbook-api
  - git
  - curl
  - python-requests
tags: [gitbook, documentation, publishing, books, git-sync, collaboration, api, markdown, spaces, collections]
platforms: [web, api, git]
related_skills:
  - mkdocs
  - docusaurus
  - sphinx
  - pandoc
---

# GitBook Documentation Skill

Master GitBook for publishing professional documentation and books with spaces, collections, content variants, Git synchronization, team collaboration, and API integration. Build beautiful, searchable documentation sites with powerful collaboration features.

## When to Use This Skill

### USE GitBook when:
- **Team documentation** - Collaborative docs with multiple editors
- **Product documentation** - User guides, API docs, tutorials
- **Knowledge bases** - Internal wikis and knowledge management
- **Multi-version docs** - Maintain docs for different product versions
- **Git-based workflow** - Sync docs with GitHub/GitLab
- **Custom branding** - Need custom domains and styling
- **Access control** - Restrict docs to authenticated users
- **Quick setup** - Need docs fast without build systems

### DON'T USE GitBook when:
- **Complex code docs** - Use Sphinx for Python API docs
- **Static site control** - Use MkDocs or Docusaurus
- **Offline-first** - GitBook is primarily cloud-hosted
- **Self-hosted required** - GitBook is SaaS (legacy self-hosted deprecated)
- **Free unlimited** - Free tier has limitations

## Prerequisites

### GitBook Account Setup

```bash
# 1. Sign up at https://www.gitbook.com/
# 2. Create an organization (or use personal space)
# 3. Generate API token at:
#    https://app.gitbook.com/account/developer

# Set environment variable
export GITBOOK_API_TOKEN="gb_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Verify authentication
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "https://api.gitbook.com/v1/user" | jq '.id, .displayName'
```

### Git Sync Setup

```bash
# In your GitBook space settings:
# 1. Go to Integrations > Git Sync
# 2. Connect GitHub/GitLab account
# 3. Select repository and branch

# Repository structure
docs-repo/
├── README.md           # Main page (or SUMMARY.md)
├── SUMMARY.md          # Table of contents
├── chapter-1/
│   ├── README.md       # Chapter intro
│   ├── page-1.md
│   └── page-2.md
├── chapter-2/
│   └── ...
└── .gitbook.yaml       # GitBook config (optional)
```

### Python Setup

```bash
# Install dependencies
pip install requests python-dateutil

# Using uv
uv pip install requests python-dateutil

# Verify
python -c "import requests; print('Ready for GitBook integration!')"
```

## Core Capabilities

### 1. API Authentication

**REST API Basics:**
```bash
# GitBook API base URL
API_BASE="https://api.gitbook.com/v1"

# Get current user
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/user" | jq

# List organizations
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/orgs" | jq

# Get organization details
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/orgs/ORG_ID" | jq
```

**Python API Client:**
```python
import requests
from datetime import datetime
import os

class GitBookClient:
    """GitBook API client."""

    BASE_URL = "https://api.gitbook.com/v1"

    def __init__(self, api_token=None):
        self.api_token = api_token or os.environ.get("GITBOOK_API_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def _request(self, method, endpoint, data=None, params=None):
        """Make API request."""
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(
            method,
            url,
            headers=self.headers,
            json=data,
            params=params
        )
        response.raise_for_status()
        return response.json() if response.text else None

    def get_user(self):
        """Get current user."""
        return self._request("GET", "/user")

    def list_organizations(self):
        """List all organizations."""
        return self._request("GET", "/orgs")

    def get_organization(self, org_id):
        """Get organization details."""
        return self._request("GET", f"/orgs/{org_id}")


# Example usage
if __name__ == "__main__":
    client = GitBookClient()

    user = client.get_user()
    print(f"User: {user['displayName']}")

    orgs = client.list_organizations()
    for org in orgs.get("items", []):
        print(f"Org: {org['title']}")
```

### 2. Spaces Management

**REST API - Spaces:**
```bash
# List spaces in organization
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/orgs/ORG_ID/spaces" | jq

# Get space details
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID" | jq

# Create space
curl -s -X POST -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    -H "Content-Type: application/json" \
    "$API_BASE/orgs/ORG_ID/spaces" \
    -d '{
        "title": "API Documentation",
        "visibility": "public"
    }' | jq

# Update space
curl -s -X PATCH -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    -H "Content-Type: application/json" \
    "$API_BASE/spaces/SPACE_ID" \
    -d '{
        "title": "Updated API Documentation",
        "visibility": "private"
    }' | jq

# Delete space
curl -s -X DELETE -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID"

# Get space content (pages)
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/content" | jq
```

**Python - Spaces:**
```python
class GitBookClient:
    # ... previous methods ...

    def list_spaces(self, org_id):
        """List all spaces in organization."""
        return self._request("GET", f"/orgs/{org_id}/spaces")

    def get_space(self, space_id):
        """Get space details."""
        return self._request("GET", f"/spaces/{space_id}")

    def create_space(self, org_id, title, visibility="public"):
        """Create a new space."""
        return self._request(
            "POST",
            f"/orgs/{org_id}/spaces",
            data={"title": title, "visibility": visibility}
        )

    def update_space(self, space_id, **kwargs):
        """Update space settings."""
        return self._request(
            "PATCH",
            f"/spaces/{space_id}",
            data=kwargs
        )

    def delete_space(self, space_id):
        """Delete a space."""
        return self._request("DELETE", f"/spaces/{space_id}")

    def get_space_content(self, space_id):
        """Get space content structure."""
        return self._request("GET", f"/spaces/{space_id}/content")


# Example usage
spaces = client.list_spaces("org_xxxxx")
for space in spaces.get("items", []):
    print(f"Space: {space['title']} ({space['visibility']})")

# Create new space
new_space = client.create_space(
    org_id="org_xxxxx",
    title="Developer Guide",
    visibility="public"
)
print(f"Created: {new_space['id']}")
```

### 3. Content Management

**REST API - Content:**
```bash
# Get page content
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/content/page/PAGE_ID" | jq

# List pages in space
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/content" | jq '.pages'

# Import content from Git
curl -s -X POST -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    -H "Content-Type: application/json" \
    "$API_BASE/spaces/SPACE_ID/content/import/git" \
    -d '{
        "url": "https://github.com/user/docs-repo",
        "ref": "main"
    }' | jq

# Export content
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/content/export" \
    -o content-export.zip

# Search content
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/search?query=installation" | jq
```

**Python - Content:**
```python
class GitBookClient:
    # ... previous methods ...

    def get_page(self, space_id, page_id):
        """Get page content."""
        return self._request(
            "GET",
            f"/spaces/{space_id}/content/page/{page_id}"
        )

    def list_pages(self, space_id):
        """List all pages in space."""
        content = self.get_space_content(space_id)
        return content.get("pages", [])

    def search_content(self, space_id, query):
        """Search content in space."""
        return self._request(
            "GET",
            f"/spaces/{space_id}/search",
            params={"query": query}
        )

    def import_from_git(self, space_id, repo_url, ref="main"):
        """Import content from Git repository."""
        return self._request(
            "POST",
            f"/spaces/{space_id}/content/import/git",
            data={"url": repo_url, "ref": ref}
        )


# Search example
results = client.search_content("space_xxxxx", "getting started")
for result in results.get("items", []):
    print(f"Found: {result['title']} - {result['path']}")
```

### 4. Collections Management

**REST API - Collections:**
```bash
# List collections
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/orgs/ORG_ID/collections" | jq

# Get collection
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/collections/COLLECTION_ID" | jq

# Create collection
curl -s -X POST -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    -H "Content-Type: application/json" \
    "$API_BASE/orgs/ORG_ID/collections" \
    -d '{
        "title": "Product Documentation",
        "description": "All product-related documentation"
    }' | jq

# Add space to collection
curl -s -X POST -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/collections/COLLECTION_ID/spaces/SPACE_ID" | jq

# Remove space from collection
curl -s -X DELETE -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/collections/COLLECTION_ID/spaces/SPACE_ID"

# List spaces in collection
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/collections/COLLECTION_ID/spaces" | jq
```

**Python - Collections:**
```python
class GitBookClient:
    # ... previous methods ...

    def list_collections(self, org_id):
        """List all collections in organization."""
        return self._request("GET", f"/orgs/{org_id}/collections")

    def get_collection(self, collection_id):
        """Get collection details."""
        return self._request("GET", f"/collections/{collection_id}")

    def create_collection(self, org_id, title, description=None):
        """Create a new collection."""
        data = {"title": title}
        if description:
            data["description"] = description

        return self._request(
            "POST",
            f"/orgs/{org_id}/collections",
            data=data
        )

    def add_space_to_collection(self, collection_id, space_id):
        """Add space to collection."""
        return self._request(
            "POST",
            f"/collections/{collection_id}/spaces/{space_id}"
        )

    def list_collection_spaces(self, collection_id):
        """List spaces in collection."""
        return self._request(
            "GET",
            f"/collections/{collection_id}/spaces"
        )


# Create collection and add spaces
collection = client.create_collection(
    org_id="org_xxxxx",
    title="API Reference",
    description="All API documentation"
)

client.add_space_to_collection(collection["id"], "space_xxxxx")
```

### 5. Content Variants (Versions)

**REST API - Variants:**
```bash
# List variants for space
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/variants" | jq

# Create variant
curl -s -X POST -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    -H "Content-Type: application/json" \
    "$API_BASE/spaces/SPACE_ID/variants" \
    -d '{
        "title": "v2.0",
        "slug": "v2"
    }' | jq

# Get variant content
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/variants/VARIANT_ID/content" | jq

# Set primary variant
curl -s -X PUT -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/variants/VARIANT_ID/primary" | jq

# Delete variant
curl -s -X DELETE -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/variants/VARIANT_ID"
```

**Python - Variants:**
```python
class GitBookClient:
    # ... previous methods ...

    def list_variants(self, space_id):
        """List all variants for space."""
        return self._request("GET", f"/spaces/{space_id}/variants")

    def create_variant(self, space_id, title, slug):
        """Create a new variant."""
        return self._request(
            "POST",
            f"/spaces/{space_id}/variants",
            data={"title": title, "slug": slug}
        )

    def get_variant_content(self, space_id, variant_id):
        """Get variant content."""
        return self._request(
            "GET",
            f"/spaces/{space_id}/variants/{variant_id}/content"
        )

    def set_primary_variant(self, space_id, variant_id):
        """Set variant as primary."""
        return self._request(
            "PUT",
            f"/spaces/{space_id}/variants/{variant_id}/primary"
        )


# Create version variants
client.create_variant("space_xxxxx", "Version 1.0", "v1")
client.create_variant("space_xxxxx", "Version 2.0", "v2")
client.set_primary_variant("space_xxxxx", "variant_v2")
```

### 6. Git Synchronization

**GitBook YAML Configuration:**
```yaml
# .gitbook.yaml - Repository configuration

# Root path for documentation
root: ./docs/

# Structure file (table of contents)
structure:
  readme: README.md
  summary: SUMMARY.md

# Redirects for moved pages
redirects:
  old-page: new-page.md
  moved/page: new-location/page.md
```

**SUMMARY.md Structure:**
```markdown
# Summary

## Getting Started

* [Introduction](README.md)
* [Installation](getting-started/installation.md)
* [Quick Start](getting-started/quickstart.md)
* [Configuration](getting-started/configuration.md)

## User Guide

* [Overview](user-guide/overview.md)
* [Basic Usage](user-guide/basic-usage.md)
* [Advanced Topics](user-guide/advanced/README.md)
  * [Topic 1](user-guide/advanced/topic-1.md)
  * [Topic 2](user-guide/advanced/topic-2.md)

## API Reference

* [REST API](api/rest.md)
* [SDKs](api/sdks.md)
* [Webhooks](api/webhooks.md)

## Resources

* [FAQ](resources/faq.md)
* [Troubleshooting](resources/troubleshooting.md)
* [Changelog](CHANGELOG.md)
```

**Git Workflow Script:**
```python
#!/usr/bin/env python3
"""gitbook_sync.py - GitBook Git synchronization helper"""

import subprocess
import os
from pathlib import Path

class GitBookSyncHelper:
    """Helper for GitBook Git synchronization."""

    def __init__(self, repo_path, docs_path="docs"):
        self.repo_path = Path(repo_path)
        self.docs_path = self.repo_path / docs_path

    def validate_structure(self):
        """Validate GitBook structure."""
        issues = []

        # Check for SUMMARY.md
        summary_path = self.docs_path / "SUMMARY.md"
        if not summary_path.exists():
            issues.append("Missing SUMMARY.md")

        # Check for README.md
        readme_path = self.docs_path / "README.md"
        if not readme_path.exists():
            issues.append("Missing README.md")

        # Validate SUMMARY.md links
        if summary_path.exists():
            with open(summary_path) as f:
                content = f.read()

            import re
            links = re.findall(r'\[.*?\]\((.*?\.md)\)', content)

            for link in links:
                file_path = self.docs_path / link
                if not file_path.exists():
                    issues.append(f"Broken link: {link}")

        return issues

    def generate_summary(self, exclude_patterns=None):
        """Auto-generate SUMMARY.md from directory structure."""
        exclude_patterns = exclude_patterns or ["_*", ".*"]

        lines = ["# Summary\n"]

        def process_dir(dir_path, indent=0):
            items = sorted(dir_path.iterdir())

            for item in items:
                # Skip excluded patterns
                if any(item.match(p) for p in exclude_patterns):
                    continue

                relative_path = item.relative_to(self.docs_path)

                if item.is_dir():
                    # Check for README.md in directory
                    readme = item / "README.md"
                    if readme.exists():
                        title = self._get_title(readme) or item.name
                        lines.append(
                            f"{'  ' * indent}* [{title}]({relative_path}/README.md)"
                        )
                    else:
                        lines.append(f"\n{'  ' * indent}## {item.name}\n")

                    process_dir(item, indent + 1)

                elif item.suffix == ".md" and item.name != "README.md":
                    title = self._get_title(item) or item.stem
                    lines.append(
                        f"{'  ' * indent}* [{title}]({relative_path})"
                    )

        process_dir(self.docs_path)
        return "\n".join(lines)

    def _get_title(self, md_path):
        """Extract title from markdown file."""
        with open(md_path) as f:
            for line in f:
                if line.startswith("# "):
                    return line[2:].strip()
        return None

    def sync_to_git(self, message="Update documentation"):
        """Commit and push changes."""
        os.chdir(self.repo_path)

        subprocess.run(["git", "add", "-A"])
        subprocess.run(["git", "commit", "-m", message])
        subprocess.run(["git", "push"])


# Example usage
if __name__ == "__main__":
    helper = GitBookSyncHelper("./my-docs-repo", "docs")

    # Validate
    issues = helper.validate_structure()
    if issues:
        print("Structure issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Structure valid!")

    # Generate SUMMARY.md
    summary = helper.generate_summary()
    print("\nGenerated SUMMARY.md:")
    print(summary)
```

### 7. Team Collaboration

**REST API - Members:**
```bash
# List organization members
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/orgs/ORG_ID/members" | jq

# Invite member
curl -s -X POST -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    -H "Content-Type: application/json" \
    "$API_BASE/orgs/ORG_ID/invites" \
    -d '{
        "email": "user@example.com",
        "role": "editor"
    }' | jq

# Update member role
curl -s -X PATCH -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    -H "Content-Type: application/json" \
    "$API_BASE/orgs/ORG_ID/members/MEMBER_ID" \
    -d '{
        "role": "admin"
    }' | jq

# Remove member
curl -s -X DELETE -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/orgs/ORG_ID/members/MEMBER_ID"

# List pending invites
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/orgs/ORG_ID/invites" | jq
```

**Python - Collaboration:**
```python
class GitBookClient:
    # ... previous methods ...

    def list_members(self, org_id):
        """List organization members."""
        return self._request("GET", f"/orgs/{org_id}/members")

    def invite_member(self, org_id, email, role="editor"):
        """Invite member to organization."""
        return self._request(
            "POST",
            f"/orgs/{org_id}/invites",
            data={"email": email, "role": role}
        )

    def update_member_role(self, org_id, member_id, role):
        """Update member's role."""
        return self._request(
            "PATCH",
            f"/orgs/{org_id}/members/{member_id}",
            data={"role": role}
        )

    def remove_member(self, org_id, member_id):
        """Remove member from organization."""
        return self._request(
            "DELETE",
            f"/orgs/{org_id}/members/{member_id}"
        )


# Roles: "admin", "creator", "editor", "reviewer", "reader"
client.invite_member("org_xxxxx", "newuser@example.com", role="editor")
```

### 8. Custom Domains and Branding

**REST API - Customization:**
```bash
# Get space customization
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/publishing/customization" | jq

# Update customization
curl -s -X PATCH -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    -H "Content-Type: application/json" \
    "$API_BASE/spaces/SPACE_ID/publishing/customization" \
    -d '{
        "favicon": "https://example.com/favicon.ico",
        "logo": {
            "light": "https://example.com/logo-light.png",
            "dark": "https://example.com/logo-dark.png"
        },
        "themes": {
            "default": "light",
            "toggeable": true
        },
        "styling": {
            "primaryColor": "#0066FF",
            "font": "Inter"
        }
    }' | jq

# Get custom domain settings
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "$API_BASE/spaces/SPACE_ID/publishing/customization/hostname" | jq

# Set custom domain
curl -s -X PUT -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    -H "Content-Type: application/json" \
    "$API_BASE/spaces/SPACE_ID/publishing/customization/hostname" \
    -d '{
        "hostname": "docs.example.com"
    }' | jq
```

**Python - Customization:**
```python
class GitBookClient:
    # ... previous methods ...

    def get_customization(self, space_id):
        """Get space customization settings."""
        return self._request(
            "GET",
            f"/spaces/{space_id}/publishing/customization"
        )

    def update_customization(self, space_id, settings):
        """Update space customization."""
        return self._request(
            "PATCH",
            f"/spaces/{space_id}/publishing/customization",
            data=settings
        )

    def set_custom_domain(self, space_id, hostname):
        """Set custom domain for space."""
        return self._request(
            "PUT",
            f"/spaces/{space_id}/publishing/customization/hostname",
            data={"hostname": hostname}
        )


# Update branding
client.update_customization("space_xxxxx", {
    "styling": {
        "primaryColor": "#6366F1",
        "font": "Inter"
    },
    "themes": {
        "default": "light",
        "toggeable": True
    }
})
```

## Complete Examples

### Example 1: Documentation Site Builder

```python
#!/usr/bin/env python3
"""docs_site_builder.py - Build complete documentation site"""

import os
from datetime import datetime
import json

class DocsSiteBuilder:
    """Build and manage GitBook documentation sites."""

    def __init__(self, api_token, org_id):
        self.client = GitBookClient(api_token)
        self.org_id = org_id

    def create_docs_site(
        self,
        title,
        description=None,
        visibility="public",
        custom_domain=None,
        branding=None
    ):
        """
        Create complete documentation site.

        Args:
            title: Site title
            description: Site description
            visibility: "public" or "private"
            custom_domain: Custom domain name
            branding: Branding settings dict

        Returns:
            Space details
        """
        # Create space
        space = self.client.create_space(
            org_id=self.org_id,
            title=title,
            visibility=visibility
        )

        space_id = space["id"]
        print(f"Created space: {space_id}")

        # Apply customization
        if branding:
            self.client.update_customization(space_id, branding)
            print("Applied branding")

        # Set custom domain
        if custom_domain:
            self.client.set_custom_domain(space_id, custom_domain)
            print(f"Set custom domain: {custom_domain}")

        return space

    def setup_versioned_docs(self, space_id, versions):
        """
        Set up version variants for documentation.

        Args:
            space_id: Space ID
            versions: List of version dicts with title and slug
        """
        for version in versions:
            variant = self.client.create_variant(
                space_id,
                title=version["title"],
                slug=version["slug"]
            )
            print(f"Created variant: {version['title']}")

            if version.get("primary"):
                self.client.set_primary_variant(space_id, variant["id"])
                print(f"Set {version['title']} as primary")

    def create_docs_collection(self, title, space_ids):
        """
        Create collection and add spaces.

        Args:
            title: Collection title
            space_ids: List of space IDs to add
        """
        collection = self.client.create_collection(
            org_id=self.org_id,
            title=title
        )

        for space_id in space_ids:
            self.client.add_space_to_collection(collection["id"], space_id)

        print(f"Created collection '{title}' with {len(space_ids)} spaces")
        return collection


# Example usage
if __name__ == "__main__":
    builder = DocsSiteBuilder(
        api_token=os.environ["GITBOOK_API_TOKEN"],
        org_id="org_xxxxx"
    )

    # Create main docs site
    space = builder.create_docs_site(
        title="Product Documentation",
        description="Complete product documentation",
        visibility="public",
        branding={
            "styling": {
                "primaryColor": "#0066FF",
                "font": "Inter"
            },
            "themes": {
                "default": "light",
                "toggeable": True
            }
        }
    )

    # Set up versions
    builder.setup_versioned_docs(space["id"], [
        {"title": "v1.0", "slug": "v1"},
        {"title": "v2.0", "slug": "v2", "primary": True},
        {"title": "Latest", "slug": "latest"}
    ])
```

### Example 2: Content Migration Tool

```python
#!/usr/bin/env python3
"""content_migration.py - Migrate content to GitBook"""

import os
from pathlib import Path
import re
import shutil

class ContentMigrator:
    """Migrate content from various formats to GitBook."""

    def __init__(self, source_path, output_path):
        self.source_path = Path(source_path)
        self.output_path = Path(output_path)

    def migrate_mkdocs(self):
        """
        Migrate MkDocs project to GitBook format.
        """
        # Copy markdown files
        docs_src = self.source_path / "docs"
        if not docs_src.exists():
            docs_src = self.source_path

        shutil.copytree(docs_src, self.output_path, dirs_exist_ok=True)

        # Convert mkdocs.yml nav to SUMMARY.md
        mkdocs_config = self.source_path / "mkdocs.yml"
        if mkdocs_config.exists():
            summary = self._convert_mkdocs_nav(mkdocs_config)
            (self.output_path / "SUMMARY.md").write_text(summary)

        # Create .gitbook.yaml
        gitbook_config = """
root: ./

structure:
  readme: README.md
  summary: SUMMARY.md
"""
        (self.output_path / ".gitbook.yaml").write_text(gitbook_config)

        print(f"Migrated MkDocs project to: {self.output_path}")

    def _convert_mkdocs_nav(self, mkdocs_path):
        """Convert MkDocs nav to SUMMARY.md format."""
        import yaml

        with open(mkdocs_path) as f:
            config = yaml.safe_load(f)

        nav = config.get("nav", [])
        lines = ["# Summary\n"]

        def process_nav(items, indent=0):
            for item in items:
                if isinstance(item, dict):
                    for title, value in item.items():
                        if isinstance(value, str):
                            lines.append(f"{'  ' * indent}* [{title}]({value})")
                        elif isinstance(value, list):
                            lines.append(f"\n{'  ' * indent}## {title}\n")
                            process_nav(value, indent + 1)
                elif isinstance(item, str):
                    lines.append(f"{'  ' * indent}* [{item}]({item})")

        process_nav(nav)
        return "\n".join(lines)

    def migrate_docusaurus(self):
        """Migrate Docusaurus project to GitBook format."""
        docs_src = self.source_path / "docs"

        # Copy docs
        shutil.copytree(docs_src, self.output_path, dirs_exist_ok=True)

        # Convert sidebars.js to SUMMARY.md
        sidebars = self.source_path / "sidebars.js"
        if sidebars.exists():
            # Basic conversion (would need proper JS parsing for complex sidebars)
            summary = self._generate_summary_from_files()
            (self.output_path / "SUMMARY.md").write_text(summary)

        # Create .gitbook.yaml
        (self.output_path / ".gitbook.yaml").write_text("""
root: ./

structure:
  readme: intro.md
  summary: SUMMARY.md
""")

        print(f"Migrated Docusaurus project to: {self.output_path}")

    def _generate_summary_from_files(self):
        """Generate SUMMARY.md from file structure."""
        lines = ["# Summary\n"]

        for md_file in sorted(self.output_path.rglob("*.md")):
            if md_file.name == "SUMMARY.md":
                continue

            relative = md_file.relative_to(self.output_path)
            title = self._extract_title(md_file) or md_file.stem

            depth = len(relative.parts) - 1
            lines.append(f"{'  ' * depth}* [{title}]({relative})")

        return "\n".join(lines)

    def _extract_title(self, md_path):
        """Extract title from markdown file."""
        content = md_path.read_text()

        # Check for frontmatter title
        if content.startswith("---"):
            match = re.search(r"title:\s*[\"']?(.+?)[\"']?\n", content)
            if match:
                return match.group(1)

        # Check for H1
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1)

        return None

    def fix_links(self):
        """Fix relative links for GitBook."""
        for md_file in self.output_path.rglob("*.md"):
            content = md_file.read_text()

            # Fix relative links without .md extension
            content = re.sub(
                r'\[([^\]]+)\]\((?!http)([^)]+)(?<!\.md)\)',
                r'[\1](\2.md)',
                content
            )

            # Fix image paths
            content = re.sub(
                r'!\[([^\]]*)\]\((?!http)\.\./',
                r'![\1](/',
                content
            )

            md_file.write_text(content)

        print("Fixed links in all markdown files")


# Example usage
if __name__ == "__main__":
    migrator = ContentMigrator(
        source_path="./mkdocs-project",
        output_path="./gitbook-docs"
    )

    migrator.migrate_mkdocs()
    migrator.fix_links()
```

### Example 3: Documentation Analytics

```python
#!/usr/bin/env python3
"""docs_analytics.py - GitBook documentation analytics"""

import os
from datetime import datetime, timedelta
import json

class DocsAnalytics:
    """Analyze GitBook documentation usage."""

    def __init__(self, api_token):
        self.client = GitBookClient(api_token)

    def get_space_stats(self, space_id):
        """Get statistics for a space."""
        space = self.client.get_space(space_id)
        content = self.client.get_space_content(space_id)

        # Count pages
        def count_pages(pages):
            count = len(pages)
            for page in pages:
                if "pages" in page:
                    count += count_pages(page["pages"])
            return count

        page_count = count_pages(content.get("pages", []))

        # Get variants
        variants = self.client.list_variants(space_id)

        return {
            "space_id": space_id,
            "title": space.get("title"),
            "visibility": space.get("visibility"),
            "page_count": page_count,
            "variant_count": len(variants.get("items", [])),
            "created_at": space.get("createdAt"),
            "updated_at": space.get("updatedAt")
        }

    def audit_content(self, space_id):
        """Audit content for issues."""
        content = self.client.get_space_content(space_id)
        issues = []

        def check_pages(pages, path=""):
            for page in pages:
                page_path = f"{path}/{page.get('slug', 'unknown')}"

                # Check for missing titles
                if not page.get("title"):
                    issues.append({
                        "type": "missing_title",
                        "path": page_path
                    })

                # Check for empty pages
                if not page.get("document"):
                    issues.append({
                        "type": "empty_page",
                        "path": page_path
                    })

                # Recurse into child pages
                if "pages" in page:
                    check_pages(page["pages"], page_path)

        check_pages(content.get("pages", []))
        return issues

    def generate_report(self, org_id):
        """Generate analytics report for organization."""
        spaces = self.client.list_spaces(org_id)

        report = {
            "generated_at": datetime.now().isoformat(),
            "org_id": org_id,
            "summary": {
                "total_spaces": 0,
                "total_pages": 0,
                "public_spaces": 0,
                "private_spaces": 0
            },
            "spaces": []
        }

        for space in spaces.get("items", []):
            stats = self.get_space_stats(space["id"])
            report["spaces"].append(stats)

            report["summary"]["total_spaces"] += 1
            report["summary"]["total_pages"] += stats["page_count"]

            if stats["visibility"] == "public":
                report["summary"]["public_spaces"] += 1
            else:
                report["summary"]["private_spaces"] += 1

        return report


# Example usage
if __name__ == "__main__":
    analytics = DocsAnalytics(os.environ["GITBOOK_API_TOKEN"])

    # Get org report
    report = analytics.generate_report("org_xxxxx")

    print(f"Documentation Analytics Report")
    print(f"{'='*50}")
    print(f"Total Spaces: {report['summary']['total_spaces']}")
    print(f"Total Pages: {report['summary']['total_pages']}")
    print(f"Public: {report['summary']['public_spaces']}")
    print(f"Private: {report['summary']['private_spaces']}")

    print(f"\nSpaces:")
    for space in report["spaces"]:
        print(f"  - {space['title']}: {space['page_count']} pages")

    # Save report
    with open("docs_report.json", "w") as f:
        json.dump(report, f, indent=2)
```

## Integration Examples

### GitHub Actions for Git Sync

```yaml
# .github/workflows/gitbook-sync.yml
name: Sync to GitBook

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'SUMMARY.md'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Validate Structure
        run: |
          # Check required files exist
          test -f docs/README.md || echo "Missing docs/README.md"
          test -f docs/SUMMARY.md || echo "Missing docs/SUMMARY.md"

          # Check for broken links
          python3 << 'EOF'
          import re
          from pathlib import Path

          summary = Path("docs/SUMMARY.md").read_text()
          links = re.findall(r'\[.*?\]\((.*?\.md)\)', summary)

          for link in links:
              path = Path("docs") / link
              if not path.exists():
                  print(f"Broken link: {link}")
                  exit(1)

          print("All links valid!")
          EOF

      - name: Notify on Success
        if: success()
        run: |
          echo "Documentation synced successfully!"
          # GitBook automatically pulls from connected repo
```

### Slack Notification for Updates

```python
#!/usr/bin/env python3
"""slack_notify.py - Notify Slack of GitBook updates"""

import os
import requests
from datetime import datetime, timedelta

def notify_docs_update(space_title, update_type, details):
    """Send Slack notification for docs update."""
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"Documentation Update: {space_title}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Type:*\n{update_type}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:*\n{datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Details:*\n{details}"
                }
            }
        ]
    }

    response = requests.post(webhook_url, json=message)
    return response.status_code == 200
```

## Best Practices

### 1. Structure Content Properly

```markdown
# Good structure
docs/
├── README.md           # Landing page
├── SUMMARY.md          # Navigation
├── getting-started/
│   ├── README.md       # Section intro
│   ├── installation.md
│   └── quickstart.md
└── guides/
    ├── README.md
    └── ...
```

### 2. Use Meaningful Slugs

```markdown
# SUMMARY.md - Good slugs
* [Installation Guide](getting-started/installation.md)
* [API Reference](api/reference.md)

# Avoid
* [Page 1](page1.md)
* [Untitled](untitled-1.md)
```

### 3. Maintain Version Consistency

```python
# Use consistent version naming
versions = [
    {"title": "v1.0", "slug": "v1"},
    {"title": "v2.0", "slug": "v2"},
    {"title": "Latest", "slug": "latest"}
]
```

### 4. Validate Before Publish

```python
def validate_docs(docs_path):
    """Validate docs before publishing."""
    issues = []

    # Check SUMMARY.md exists
    if not (docs_path / "SUMMARY.md").exists():
        issues.append("Missing SUMMARY.md")

    # Check all linked files exist
    # Check for broken internal links
    # Check image paths

    return issues
```

## Troubleshooting

### Common Issues

**Issue: 401 Unauthorized**
```bash
# Verify token
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "https://api.gitbook.com/v1/user"

# Regenerate token at:
# https://app.gitbook.com/account/developer
```

**Issue: Git sync not updating**
```bash
# Check Git connection in GitBook space settings
# Verify branch name matches
# Check for merge conflicts

# Force resync via API
curl -s -X POST -H "Authorization: Bearer $GITBOOK_API_TOKEN" \
    "https://api.gitbook.com/v1/spaces/SPACE_ID/git/sync"
```

**Issue: Broken links after migration**
```python
# Fix relative links
import re

content = path.read_text()
# Add .md extension to links
content = re.sub(
    r'\[([^\]]+)\]\((?!http)([^)]+)(?<!\.md)\)',
    r'[\1](\2.md)',
    content
)
```

**Issue: Images not displaying**
```markdown
<!-- Use absolute paths from root -->
![Image](/assets/image.png)

<!-- Or relative from current file -->
![Image](./images/image.png)
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Spaces management API
  - Collections and variants
  - Git synchronization
  - Team collaboration
  - Custom domains and branding
  - Content migration tools
  - Analytics and reporting
  - GitHub Actions integration
  - Best practices and troubleshooting

## Resources

- **GitBook Documentation**: https://docs.gitbook.com/
- **GitBook API Reference**: https://developer.gitbook.com/
- **Git Sync Guide**: https://docs.gitbook.com/integrations/git-sync
- **Custom Domains**: https://docs.gitbook.com/published-documentation/custom-domain

---

**Publish beautiful documentation with GitBook - spaces, collections, and seamless Git integration!**
