---
name: universal-templating
description: Master all templating formats - Handlebars, Cookiecutter, Copier, Maven, and Harness - with format selection matrix, generation workflows, and best practices
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, WebSearch]
dependencies: [harness-expert, project-scaffolding]
triggers: [template format, generate template, template design, template workflow]
---

# Universal Templating Skill

Comprehensive guide to template format selection, design patterns, generation workflows, and best practices across Handlebars, Cookiecutter, Copier, Maven, and Harness templates.

## Template Format Matrix

### Handlebars

**Use Cases:**
- Simple variable substitution
- Email templates
- Document generation
- Configuration files
- Quick string templating

**Syntax:**
```handlebars
Hello {{name}},
{{#if premium}}Welcome to premium!{{/if}}
{{#each items}}- {{this}}{{/each}}
```

**Strengths:**
- Minimal learning curve
- Fast execution
- Great for config files
- Small file size
- No external dependencies

**Weaknesses:**
- Limited logic capabilities
- No native loops/conditionals
- Requires helpers for complex operations

**Best For:** Configuration file templating, simple document generation

---

### Cookiecutter

**Use Cases:**
- Interactive project scaffolding
- Multi-step wizard templates
- Python package templates
- Post-generation hooks

**Syntax:**
```json
{
  "project_name": "{{ cookiecutter.project_name }}",
  "author": "{{ cookiecutter.author_name }}"
}
```

**Strengths:**
- Interactive CLI prompts
- Python ecosystem integration
- Post-generation hooks
- Conditional rendering
- JSON-based config

**Weaknesses:**
- Python dependency required
- Jinja2 templates (verbose)
- Less flexible validation
- Community templates vary in quality

**Best For:** Python projects, quick prototypes, community templates

---

### Copier

**Use Cases:**
- Modern project scaffolding
- Template versioning and updates
- Multi-template composition
- Complex validation rules

**Syntax:**
```yaml
_templates_suffix: .jinja
_copy_without_render:
  - "*.png"
  - "*.jpg"

project_name:
  type: str
  help: What is your project name?
  default: my_project
```

**Strengths:**
- Powerful Jinja2 templating
- Template versioning
- Update existing projects
- Composite templates
- Advanced validation
- Excellent documentation

**Weaknesses:**
- Python dependency
- Steeper learning curve
- Larger footprint
- Development active (API changes possible)

**Best For:** Enterprise templates, versioned scaffolding, complex projects

---

### Maven

**Use Cases:**
- Java/JVM project archetypes
- Enterprise Java scaffolding
- Build system integration
- Dependency management

**Syntax:**
```xml
<archetype>
  <groupId>org.apache.maven.archetypes</groupId>
  <artifactId>maven-archetype-quickstart</artifactId>
</archetype>
```

**Strengths:**
- Native Maven integration
- Build tool awareness
- Dependency management
- Enterprise adoption
- IDEs have built-in support

**Weaknesses:**
- Java/JVM only
- XML-heavy
- Complex archetype internals
- Verbose setup

**Best For:** Java/JVM projects, Maven-based builds

---

### Harness Templates

**Use Cases:**
- CI/CD pipeline steps
- Reusable stage definitions
- Pipeline patterns
- Deployment strategies

**Syntax:**
```yaml
template:
  name: Deploy Service
  type: StepGroup
  spec:
    steps:
      - step:
          name: Deploy K8s
          identifier: deploy_k8s
          type: K8sDeploy
          spec:
            service: <+input>
```

**Strengths:**
- Native Harness integration
- Expression language support
- Runtime inputs
- Pipeline-aware
- Built-in approval flows

**Weaknesses:**
- Harness-specific only
- YAML complexity
- Requires Harness setup
- Limited reusability outside Harness

**Best For:** Harness pipelines, deployment templates

---

## Format Selection Decision Tree

```
START: Need to generate what?
│
├─ Configuration files
│  ├─ Simple substitution → Handlebars
│  └─ Complex validation → Copier
│
├─ Project scaffold
│  ├─ Python project → Cookiecutter
│  ├─ Enterprise/versioned → Copier
│  └─ Java/JVM → Maven
│
├─ CI/CD pipeline
│  ├─ Harness platform → Harness Templates
│  └─ Other CI → Handlebars + custom
│
├─ Document/email
│  └─ Handlebars
│
└─ Reusable components
   ├─ Code snippets → Handlebars
   └─ Full modules → Copier
```

---

## Generation Workflow Steps

### Step 1: Template Planning

**Inputs:**
- Target audience (users, developers, automation)
- Use cases and scenarios
- Complexity level (simple, moderate, advanced)
- Maintenance burden tolerance
- Integration requirements

**Deliverables:**
- Template specification document
- Format selection justification
- Variable naming convention document
- Example instantiation

**Questions to Answer:**
1. What will be generated?
2. Who uses it (users, scripts, tools)?
3. How often will it change?
4. Will it need versioning?
5. What validation is needed?

---

### Step 2: Variable Definition

**Essential Variables:**
```
project_name         - Primary identifier
author_name         - Creator/maintainer
organization        - Company/org name
description         - Brief description
license             - License type (MIT, Apache, etc.)
target_framework    - Framework/language version
```

**Optional Variables (by use case):**
```
// Python projects
python_version      - Target Python version
package_name        - PyPI package name
django_version      - Django version (if applicable)

// Java projects
java_version        - JDK version
groupId            - Maven group ID
artifactId         - Maven artifact ID

// Cloud projects
aws_region         - AWS region
kubernetes_cluster - K8s cluster name
docker_registry    - Container registry
```

---

### Step 3: Variable Naming Conventions

**Naming Rules:**

1. **Format:** `snake_case` (all formats support this)
2. **Prefixes:**
   - `generated_*` - Files/content created by template
   - `input_*` - User input required
   - `computed_*` - Derived from other variables
   - `optional_*` - Optional user input

3. **Examples:**
   ```
   ✓ project_name
   ✓ author_email
   ✓ generated_version
   ✓ target_framework
   ✗ ProjectName (avoid PascalCase)
   ✗ PROJECT_NAME (avoid SCREAMING_SNAKE_CASE)
   ```

---

### Step 4: Content Structure Design

**Standard Project Structure:**
```
{project_name}/
├── README.md              # Template instructions
├── {project_name}/        # Main package/app
│   ├── __init__.py        # (if applicable)
│   ├── main.py
│   └── config.py
├── tests/                 # Test directory
│   ├── __init__.py
│   └── test_main.py
├── docs/                  # Documentation
│   └── API.md
├── .gitignore
├── LICENSE
├── requirements.txt       # (Python)
├── setup.py              # (Python)
├── package.json          # (Node.js)
└── {{cookiecutter.var}}/ # Template variables
```

---

### Step 5: Conditional Rendering

**When to Use:**
- Optional features
- Different project types
- Target-specific configurations
- License-based files

**Handlebars Example:**
```handlebars
{{#if include_docker}}
FROM python:3.11
COPY . /app
{{/if}}
```

**Cookiecutter/Copier Example:**
```yaml
{%- if use_docker %}
# Docker configuration
{%- endif %}
```

---

### Step 6: Validation & Constraints

**Input Validation:**
- Email format checking
- Version number validation
- Project name uniqueness checks
- Path validation

**Copier Example:**
```yaml
project_name:
  type: str
  help: Project name (lowercase, alphanumeric + underscore)
  regex: "^[a-z_][a-z0-9_]*$"

python_version:
  type: str
  default: "3.11"
  help: Python version (3.9, 3.10, 3.11, 3.12)
  choices:
    - "3.9"
    - "3.10"
    - "3.11"
    - "3.12"
```

---

### Step 7: Post-Generation Hooks

**Cookiecutter/Copier Hooks:**
```python
# hooks/post_gen_project.py
import os
from pathlib import Path

# Initialize git repository
os.system("git init")

# Create virtual environment
os.system("python -m venv venv")

# Install dependencies
os.system("pip install -r requirements.txt")

# Generate API docs
os.system("python generate_docs.py")
```

---

### Step 8: Documentation

**Required Documentation:**
1. **README.md** - How to use template
2. **VARIABLES.md** - All available variables
3. **EXAMPLES.md** - Example instantiations
4. **TROUBLESHOOTING.md** - Common issues

---

## Best Practices for Template Design

### 1. Variable Defaults

**Good Defaults:**
```yaml
# Clear, sensible defaults
author_name: "Your Name"
license: "MIT"
python_version: "3.11"  # Latest stable
include_docker: false   # Opt-in for complexity
include_tests: true     # Always good to start with tests
```

**Bad Defaults:**
```yaml
# Unclear or empty
author_name: ""
unknown_var: "???"
version: "1.0.0"  # Should be context-aware
```

---

### 2. DRY Principle (Don't Repeat Yourself)

**Template Variables Once:**
```
Define: project_name = "my_project"
Use in:
  - Directory name
  - README title
  - Setup.py name
  - Docker image name
```

---

### 3. File Organization

**Group Related Files:**
```
template/
├── [project_name]/        # Project source (stays as-is)
├── [project_name]_docs/   # Docs structure
├── [project_name]_config/ # Config templates
└── tests/                 # Test templates
```

---

### 4. Template Readability

**Use Clear Comments:**
```jinja
{# This file is generated from {{template_name}} #}
{# Last updated: {{generated_date}} #}
{# For questions, see: {{docs_url}} #}
```

---

### 5. Version Management

**Template Versioning:**
```yaml
# In template metadata
version: "1.0.0"
harness_compatibility: "1.4+"
minimum_python: "3.9"
```

---

### 6. Error Handling

**Clear Error Messages:**
```python
# Instead of: ValueError
# Use:
if not re.match(r"^[a-z_][a-z0-9_]*$", project_name):
    raise ValueError(
        f"Project name '{project_name}' is invalid.\n"
        f"Must start with lowercase letter or underscore,\n"
        f"followed by lowercase letters, numbers, or underscores."
    )
```

---

## Template Generation Workflow

### End-to-End Generation Process

```
1. USER SELECTION
   ├─ Choose template
   ├─ Select format (if flexible)
   └─ Provide variables

2. VALIDATION
   ├─ Validate all inputs
   ├─ Check constraints
   └─ Generate variable report

3. PRE-PROCESSING
   ├─ Compute derived variables
   ├─ Expand conditionals
   └─ Build file tree

4. GENERATION
   ├─ Render templates
   ├─ Copy static files
   ├─ Create directory structure
   └─ Handle special files

5. POST-PROCESSING
   ├─ Run hooks
   ├─ Initialize git/vcs
   ├─ Install dependencies
   └─ Generate documentation

6. VALIDATION
   ├─ Check generated files
   ├─ Verify structure
   ├─ Test basic functionality
   └─ Generate report

7. OUTPUT
   ├─ Display summary
   ├─ Provide next steps
   └─ Save manifest
```

---

## Harness Expression Language in Templates

### Available Context Variables

```
Harness Expressions:
├─ <+input.VARIABLE_NAME>        # Inputs
├─ <+pipeline.PROPERTY>          # Pipeline-level
├─ <+stage.PROPERTY>             # Stage-level
├─ <+steps.STEP_ID.PROPERTY>     # Step outputs
├─ <+env.PROPERTY>               # Environment variables
├─ <+secrets.getValue("NAME")>   # Secret references
└─ <+execution.PROPERTY>         # Execution context
```

### Template Examples with Expressions

```yaml
template:
  name: Deploy Service
  type: Step
  spec:
    service:
      name: <+input.service_name>
    environment:
      name: <+input.environment>
    variables:
      version: <+input.artifact_version>
      deploy_timeout: <+input.timeout_minutes>
      approval_required: <+input.requires_approval>
```

---

## Related Documentation

- [Handlebars.js](https://handlebarsjs.com/)
- [Cookiecutter](https://cookiecutter.readthedocs.io/)
- [Copier](https://copier.readthedocs.io/)
- [Maven Archetypes](https://maven.apache.org/guides/introduction/introduction-to-archetypes.html)
- [Harness Templates](https://developer.harness.io/docs/platform/templates)
