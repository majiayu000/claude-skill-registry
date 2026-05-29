---
name: project-templates
description: "Curated project templates that guide feature-dev Phase 3 questions with research-backed technology choices. Provides standardized options for common project types (SaaS API, ML Service, CLI Tool, Full-Stack). Use when starting new projects or when feature-dev needs structured decision guidance. Do NOT use for existing projects with established stacks - analyze existing code instead."
version: 1.0.0
---

# Project Templates Skill

Provides curated, research-backed project templates for `/popkit:dev full` Phase 3 (Questions).

## Purpose

Instead of dynamically generating technology options (which can miss relevant choices or suggest unfamiliar stacks), this skill provides:

1. **Curated templates** for common project types
2. **Research-backed options** with pros/cons/when-to-use
3. **Consistent question flow** across similar projects
4. **Extensibility** for custom project types

## Available Templates

| Template            | Use Case                       | Key Decisions                            |
| ------------------- | ------------------------------ | ---------------------------------------- |
| `saas-api`          | Backend APIs for SaaS products | Runtime, Database, Auth, Billing         |
| `ml-service`        | ML/AI inference APIs           | Runtime, Model Serving, Inference Engine |
| `cli-tool`          | Command-line applications      | Language, Distribution, Config Format    |
| `fullstack`         | Full-stack web applications    | Frontend, Backend, Database, Hosting     |
| `browser-extension` | Browser extensions             | Manifest Version, Framework, Storage     |
| `mobile-backend`    | Mobile app backends            | Runtime, Push Notifications, Real-time   |

## Template Schema

Each template is a JSON file with this structure:

```json
{
  "id": "saas-api",
  "name": "SaaS Backend API",
  "description": "Backend API for SaaS products with auth, billing, multi-tenancy",
  "icon": "cloud",
  "questions": [
    {
      "id": "runtime",
      "header": "Runtime",
      "question": "Which runtime/framework should we use for the API server?",
      "multiSelect": false,
      "options": [
        {
          "value": "node-fastify",
          "label": "Node.js + Fastify",
          "description": "Fast, TypeScript-native, great for APIs",
          "pros": [
            "Fastest Node framework",
            "First-class TypeScript",
            "Schema validation built-in"
          ],
          "cons": ["Smaller ecosystem than Express", "Less middleware available"],
          "when": "Performance critical, TypeScript preferred, API-focused",
          "popularity": { "npm_weekly": 2000000, "github_stars": 28000 }
        }
      ],
      "default": "node-fastify",
      "research_sources": ["npm trends", "TechEmpower benchmarks", "State of JS 2024"]
    }
  ],
  "agents": {
    "primary": ["api-designer", "code-architect"],
    "supporting": ["security-auditor", "test-writer-fixer"]
  },
  "quality_gates": ["typescript", "lint", "test", "security-scan"],
  "scaffolding": {
    "directories": ["src", "src/routes", "src/services", "tests"],
    "files": ["package.json", "tsconfig.json", ".env.example"]
  }
}
```

## Usage in feature-dev

### Phase 3 Integration

When `/popkit:dev full` reaches Phase 3 (Questions):

1. **Template Selection** - First question asks project type:

   ```
   What type of project is this?
   - SaaS Backend API
   - ML/AI Service
   - CLI Tool
   - Full-Stack Web App
   - Custom (dynamic questions)
   ```

2. **Load Template** - Based on selection, load the corresponding template

3. **Ask Template Questions** - Use `AskUserQuestion` with template-defined options:

   ```
   Use AskUserQuestion tool with:
   - questions: template.questions (converted to AskUserQuestion format)
   - Each question has curated options with descriptions
   ```

4. **Store Decisions** - Save answers for Phase 4 (Architecture)

### Example Flow

```markdown
## Phase 3: Questions

Based on your PRODUCT-SPEC.md, this looks like a **SaaS API** project.

[AskUserQuestion: Project Type confirmation]

Loading SaaS API template...

[AskUserQuestion: Runtime - Node.js+Fastify / Python+FastAPI / Go+Fiber / Bun+Hono]
[AskUserQuestion: Database - PostgreSQL / MySQL / MongoDB / SQLite]
[AskUserQuestion: Auth - Clerk / Auth0 / Supabase Auth / Custom JWT]
[AskUserQuestion: Billing - Stripe / Paddle / LemonSqueezy / None]

Decisions captured. Moving to Phase 4: Architecture...
```

## Adding Custom Templates

To add a project-specific template:

1. Create `templates/my-template.json` following the schema
2. Add entry to `templates/index.json`
3. Template will appear in project type selection

## Research Methodology

Each template option should include:

- **Popularity metrics**: npm downloads, GitHub stars, survey data
- **Performance data**: Benchmarks where relevant
- **Ecosystem size**: Available plugins, middleware, tools
- **Production usage**: Companies using it at scale
- **Maintenance status**: Last release, contributor activity

Sources:

- npm trends (https://npmtrends.com)
- State of JS/Python/Go surveys
- TechEmpower benchmarks
- GitHub star history
- Developer surveys (Stack Overflow, JetBrains)

## Process

1. **Detect Project Type**: Analyze PRODUCT-SPEC.md or ask user
2. **Load Template**: Read from `templates/<type>.json`
3. **Present Questions**: Use AskUserQuestion with template options
4. **Capture Decisions**: Store for architecture phase
5. **Generate Scaffolding**: Optional project structure setup
