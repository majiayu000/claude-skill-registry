---
name: ruby-on-rails-development
description: Rails skills router and knowledge base. Routes your request to the appropriate specialist skill. Contains core Rails principles and conventions. Use when unsure which specialist to choose or for general Rails questions.
---

# Rails Development Router

Welcome! I'll help route your Rails development task to the appropriate specialist.

## 🎯 How This Works

Based on your request, I'll automatically activate the right specialist skill:

| Your Task | Specialist Activated |
|-----------|---------------------|
| Writing tests, TDD | → **rails-testing** |
| UI components, Turbo | → **rails-viewcomponents** |
| Security, encryption | → **rails-security** |
| Business logic, workflows | → **rails-business-logic** |
| Background jobs | → **rails-background-jobs** |
| REST API | → **rails-api** |
| GraphQL | → **rails-graphql** |
| Inertia.js SPA | → **rails-inertia** |
| Docker, deployment | → **rails-devops** |
| Performance, optimization | → **rails-analyst** |
| Documentation | → **rails-technical-writer** |
| Project planning | → **rails-project-manager** |

## 🚀 Quick Start

Just describe what you want to build:

```
✅ "Create User model with email validation"
✅ "Add authentication with Devise"
✅ "Build a dashboard component"
✅ "Setup CI/CD pipeline"
✅ "Optimize slow queries"
```

I'll analyze your request and activate the right specialist!

## 📚 Core Rails Principles

All specialists follow these NON-NEGOTIABLE principles:

### 1. Test-First Development (TDD)

**Every feature MUST follow Red-Green-Refactor:**

```ruby
# 1. RED - Write failing test FIRST
RSpec.describe User do
  it "validates email presence" do
    user = User.new(email: nil)
    expect(user).not_to be_valid
  end
end

# 2. Run test - MUST fail
# 3. GREEN - Write minimal code to pass
# 4. REFACTOR - Improve while tests pass
```

**Rules:**
- ✅ Tests written BEFORE implementation
- ✅ Never commit failing tests
- ✅ Never skip/disable tests to pass builds
- ✅ Red-Green-Refactor cycle strictly enforced

### 2. YAGNI Principle

**You Aren't Gonna Need It - Don't create abstractions until needed.**

```ruby
# ❌ Don't create prematurely
# app/services/      (until pattern emerges)
# app/presenters/    (use decorators instead)
# config/constants.rb (for values used once)

# ✅ Create when actually needed
# app/interactions/  (ActiveInteraction)
# app/components/    (ViewComponents)
```

### 3. Convention Over Configuration

Follow Rails conventions unless compelling reason:

- **Naming**: Models singular, Controllers plural
- **Routes**: RESTful design
- **Structure**: Standard Rails directories
- **Patterns**: Rails way first

### 4. Security by Design

**Always:**
- ✅ Strong parameters in controllers
- ✅ Authorization on all actions (Pundit)
- ✅ Encrypt sensitive data (Lockbox)
- ✅ HTTPS in production
- ✅ Rate limiting on APIs

### 5. Incremental Progress

Each commit should:
- ✅ Compile successfully
- ✅ Pass all tests
- ✅ Be deployable
- ✅ Represent complete feature slice

## 📖 Available Specialists

For detailed information about each specialist, see [SKILLS_REGISTRY.md](../SKILLS_REGISTRY.md)

### 🎯 Coordination
- **rails-project-manager** - Plans features, coordinates specialists

### 💻 Development
- **rails-testing** - RSpec, FactoryBot, TDD
- **rails-viewcomponents** - ViewComponent, Turbo, Stimulus
- **rails-business-logic** - ActiveInteraction, AASM, decorators

### 🌐 API & Frontend
- **rails-api** - REST APIs, JWT, serialization
- **rails-graphql** - GraphQL schemas, mutations
- **rails-inertia** - Inertia.js SPAs

### 🏗️ Infrastructure
- **rails-background-jobs** - Solid Queue, jobs
- **rails-devops** - Docker, CI/CD, deployment
- **rails-security** - Pundit, Lockbox, authentication

### 📊 Analysis
- **rails-analyst** - Performance, optimization
- **rails-technical-writer** - Documentation

## 🔍 Need Help Choosing?

### Ask yourself:

**What am I building?**
- Data/logic → rails-business-logic
- UI component → rails-viewcomponents
- API endpoint → rails-api or rails-graphql
- Background task → rails-background-jobs

**What am I fixing?**
- Slow queries → rails-analyst
- Security issue → rails-security
- Test failure → rails-testing
- Deployment problem → rails-devops

**What am I documenting?**
- README → rails-technical-writer
- Code comments → rails-technical-writer

**What am I planning?**
- Complex feature → rails-project-manager
- Architecture decision → rails-project-manager

## 💡 Example Workflows

### Simple Task (One Specialist)

```
YOU: "Add email validation to User model"

CLAUDE: [Activates rails-testing]
        Writing test first (TDD)...
        Test fails (RED) ✓
        Adding validation...
        Test passes (GREEN) ✓
```

### Complex Task (Multiple Specialists)

```
YOU: "Build comment system for articles"

CLAUDE: [Activates rails-project-manager]
        Analyzing requirements...

        Plan:
        Stage 1: Model & Tests (rails-testing)
        Stage 2: Business Logic (rails-business-logic)
        Stage 3: API (rails-api)
        Stage 4: UI Components (rails-viewcomponents)

        Starting Stage 1...
```

## 🛠️ Tech Stack Reference

Our specialists support:

### Core Framework
- Rails 7.0, 7.1, 7.2, 8.0, 8.1
- Ruby 3.2, 3.3+
- PostgreSQL 14+

### Frontend
- ViewComponent 3.x
- Hotwire (Turbo 8.x, Stimulus 3.x)
- Tailwind CSS
- Inertia.js 1.x

### Backend
- ActiveInteraction 5.x
- AASM 5.x
- Pundit 2.x
- Lockbox 1.x
- Solid Queue (Rails 7.1+)

### DevOps
- Docker
- GitHub Actions / GitLab CI
- Kamal 2.x (Rails 8.0+)

## 📋 Quality Checklist

Before any commit, specialists ensure:

```bash
# All must pass:
bundle exec rspec                    # Tests
bundle exec rubocop                  # Linting
bundle exec erblint --lint-all       # ERB linting
bundle exec brakeman --no-pager      # Security
bundle exec bundle-audit check       # Vulnerabilities
```

## 🔄 Continuous Improvement

This system is:
- ✅ **Extensible** - Easy to add new specialists
- ✅ **Updatable** - Each specialist versioned independently
- ✅ **Open Source** - Community contributions welcome
- ✅ **Documented** - All patterns and practices recorded

See [SKILLS_REGISTRY.md](../SKILLS_REGISTRY.md) for:
- Complete specialist catalog
- Version history
- Extension guide
- Contributing guidelines

---

## 🎬 Ready to Start?

Just tell me what you want to build, and I'll activate the right specialist!

Examples:
- "Create an Article model with validations"
- "Setup authentication system"
- "Build a commenting feature"
- "Optimize slow dashboard queries"
- "Deploy to production with Docker"

Let's build something great! 🚀
