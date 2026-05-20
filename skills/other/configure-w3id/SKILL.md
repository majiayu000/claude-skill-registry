---
description: A skill that will register a new w3id for a new github project.
---

For context See https://github.com/linkml/linkml-project-copier/issues/127

First, it will be necessary to create a fork of https://github.com/perma-id/w3id.org

This might be in ~/repos/w3id.org - be sure it is up to date

make a PR with a new folder ./{{ project_name }}/

This will have two files:

.htaccess:

```
Options +FollowSymLinks
RewriteEngine on

# vocab/ end point
RewriteRule ^vocab$ https://github.{{ github_org }}.io/{{ project_name }}/$1
RewriteRule ^vocab\/(.*)$ https://github.{{ github_org }}.io/{{ project_name }}/$1 [R=301,L]

# schema submodules
RewriteRule ^schema\/(.*)$ https://raw.githubusercontent.com/{{ github_org }}/{{ project_name }}/main/src/{{ project_name }}/$1 [R=301,L]

# Schema artefacts use raw Github URLs
# if suffix is yaml, redirect to LinkML YAML schema
RewriteRule ^{{ project_name }}.yaml$ https://raw.githubusercontent.com/{{ github_org }}/{{ project_name }}/main/src/{{ project_name }}/merged/merged_hierarchy.yaml [R=302,L]

# if suffix is schema.json, redirect to JSON Schema
RewriteRule ^{{ project_name }}.schema.json$ https://raw.githubusercontent.com/{{ github_org }}/{{ project_name }}/main/project/jsonschema/{{ project_name }}.schema.json [R=302,L]

# if suffix is owl, redirect to OWL
RewriteRule ^{{ project_name }}.owl.ttl$ https://raw.githubusercontent.com/{{ github_org }}/{{ project_name }}/main/project/owl/{{ project_name }}.owl.ttl [R=302,L]


# Schema elements use Github Pages
# Rewrite Base URL
RewriteRule ^(.*)$ https://github.{{ github_org }}.io/{{ project_name }}/elements/$1 [R=302,L]
```

a README.md that contains homepages (ie github), documentation links, plus contacts
