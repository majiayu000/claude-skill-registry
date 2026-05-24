---
name: ruby-patterns
description: Ruby development patterns including package manager detection (Bundler), project structure, and idiomatic Ruby practices. Use when writing, reviewing, or debugging Ruby code.
durability: encoded-preference
---

# Ruby Development Patterns

## Package Manager Detection (CRITICAL)

**Before running ANY Ruby commands, detect the package manager:**

| File | Package Manager | Install | Run |
|------|-----------------|---------|-----|
| `Gemfile.lock` | Bundler | `bundle install` | `bundle exec` |
| `Gemfile` (no lock) | Bundler | `bundle install` | `bundle exec` |
| None | gem/ruby | `gem install` | `ruby` |

**NEVER use `gem install` directly when Gemfile exists.**

**Follow the existing project's Gemfile. Always use `bundle exec` to run commands.**

## Project Structure

```
myproject/
├── lib/                # Source code
│   ├── myproject.rb    # Main entry point
│   └── myproject/      # Namespace directory
│       ├── cli.rb
│       └── core.rb
├── spec/               # RSpec tests (preferred)
│   ├── spec_helper.rb
│   └── myproject/
│       └── core_spec.rb
├── bin/                # Executables
├── Gemfile
├── Gemfile.lock
├── Rakefile
└── Makefile
```

## CLI Structure

**Three-layer separation (same principle as Python).**
