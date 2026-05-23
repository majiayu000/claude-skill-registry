---
name: ruby-gems-bundler
description: Use when working with Ruby gems, Bundler for dependency management, creating gemspecs, and publishing gems to RubyGems.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Ruby Gems and Bundler

Master Ruby's package management system with gems and Bundler. Learn to manage dependencies, create gems, and publish to RubyGems.

## Bundler Basics

### Gemfile

```ruby
source 'https://rubygems.org'

# Ruby version
ruby '3.3.0'

# Production gems
gem 'rails', '~> 7.1'
gem 'pg', '>= 1.1'
gem 'puma', '~> 6.0'

# Development and test gems
group :development, :test do
  gem 'rspec-rails'
  gem 'factory_bot_rails'
  gem 'faker'
end

# Development only
group :development do
  gem 'rubocop'
  gem 'rubocop-rails'
end

# Test only
group :test do
  gem 'capybara'
  gem 'selenium-webdriver'
end

# Git source
gem 'my_gem', git: 'https://github.com/user/my_gem.git'

# Local path (for development)
gem 'local_gem', path: '../local_gem'

# Specific branch
gem 'experimental_gem', git: 'https://github.com/user/repo.git', branch: 'develop'

# Require specific file or false to not auto-require
gem 'sidekiq', require: 'sidekiq/web'
gem 'bootsnap', require: false
```

### Version Constraints

```ruby
# Exact version
gem 'rails', '7.1.0'

# Pessimistic operator (allows patch updates)
gem 'rails', '~> 7.1.0'  # >= 7.1.0 and < 7.2.0
gem 'rails', '~> 7.1'    # >= 7.1.0 and < 8.0.0

# Greater than or equal
gem 'pg', '>= 1.1'

# Range
gem 'ruby-version', '>= 1.0', '< 2.0'

# Multiple constraints
gem 'nokogiri', '>= 1.10', '< 2.0'
```

### Bundler Commands

```bash
# Install all gems from Gemfile
bundle install

# Install to specific path
bundle install --path vendor/bundle

# Update all gems
bundle update

# Update specific gem
bundle update rails

# Check for outdated gems
bundle outdated

# Show gem location
bundle show rails

# Execute command with bundled gems
bundle exec rspec

# Open gem in editor
bundle open rails

# Check Gemfile syntax
bundle check

# Remove unused gems
bundle clean

# List all installed gems
bundle list

# Show dependency tree
bundle viz
```

### Gemfile.lock

The `Gemfile.lock` file locks gem versions for consistent installations:

```ruby
# Always commit Gemfile.lock to version control
# This ensures all developers use same gem versions

# Regenerate Gemfile.lock
rm Gemfile.lock
bundle install
```

## Creating Gems

### Gem Structure

```bash
# Create new gem
bundle gem my_gem

# Structure:
my_gem/
├── lib/
│   ├── my_gem/
│   │   └── version.rb
│   └── my_gem.rb
├── spec/
│   ├── my_gem_spec.rb
│   └── spec_helper.rb
├── bin/
│   ├── console
│   └── setup
├── .gitignore
├── Gemfile
├── LICENSE.txt
├── my_gem.gemspec
├── Rakefile
└── README.md
```

### Gemspec

```ruby
# my_gem.gemspec
require_relative 'lib/my_gem/version'

Gem::Specification.new do |spec|
  spec.name          = "my_gem"
  spec.version       = MyGem::VERSION
  spec.authors       = ["Your Name"]
  spec.email         = ["your.email@example.com"]

  spec.summary       = "Short summary of gem"
  spec.description   = "Longer description of what gem does"
  spec.homepage      = "https://github.com/username/my_gem"
  spec.license       = "MIT"

  spec.required_ruby_version = ">= 3.0.0"

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = "https://github.com/username/my_gem"
  spec.metadata["changelog_uri"] = "https://github.com/username/my_gem/CHANGELOG.md"

  # Specify which files should be added to the gem
  spec.files = Dir.chdir(File.expand_path(__dir__)) do
    `git ls-files -z`.split("\x0").reject do |f|
      f.match(%r{\A(?:test|spec|features)/})
    end
  end

  spec.bindir        = "exe"
  spec.executables   = spec.files.grep(%r{\Aexe/}) { |f| File.basename(f) }
  spec.require_paths = ["lib"]

  # Runtime dependencies
  spec.add_dependency "activesupport", "~> 7.0"
  spec.add_dependency "nokogiri", ">= 1.10"

  # Development dependencies
  spec.add_development_dependency "rspec", "~> 3.12"
  spec.add_development_dependency "rubocop", "~> 1.50"
end
```

### Version File

```ruby
# lib/my_gem/version.rb
module MyGem
  VERSION = "0.1.0"
end
```

### Main Library File

```ruby
# lib/my_gem.rb
require_relative "my_gem/version"
require_relative "my_gem/core"
require_relative "my_gem/helpers"

module MyGem
  class Error < StandardError; end

  def self.configure
    yield configuration
  end

  def self.configuration
    @configuration ||= Configuration.new
  end

  class Configuration
    attr_accessor :api_key, :timeout

    def initialize
      @api_key = nil
      @timeout = 30
    end
  end
end
```

## Building and Publishing

### Build Gem

```bash
# Build gem locally
gem build my_gem.gemspec

# This creates my_gem-0.1.0.gem

# Install locally for testing
gem install ./my_gem-0.1.0.gem

# Uninstall
gem uninstall my_gem
```

### Publish to RubyGems

```bash
# First time setup (one-time)
gem push my_gem-0.1.0.gem
# You'll be prompted to log in

# For subsequent pushes
gem push my_gem-0.2.0.gem

# Yank a version (removes from RubyGems)
gem yank my_gem -v 0.1.0

# Unyank a version
gem unyank my_gem -v 0.1.0
```

### Versioning

```ruby
# Semantic Versioning: MAJOR.MINOR.PATCH
# 1.0.0 -> 1.0.1 (patch)
# 1.0.1 -> 1.1.0 (minor)
# 1.1.0 -> 2.0.0 (major)

# lib/my_gem/version.rb
module MyGem
  VERSION = "1.0.0"
end

# Update version, then build and push:
# 1. Edit version.rb
# 2. gem build my_gem.gemspec
# 3. gem push my_gem-1.0.0.gem
```

## RubyGems Commands

```bash
# List installed gems
gem list

# Search for gems
gem search rails

# Show gem info
gem info rails

# List gem dependencies
gem dependency rails

# Update all gems
gem update

# Update specific gem
gem update rails

# Cleanup old versions
gem cleanup

# Show gem environment
gem env

# Install specific version
gem install rails -v 7.1.0

# Install without documentation (faster)
gem install rails --no-document

# Uninstall gem
gem uninstall rails

# Fetch gem but don't install
gem fetch rails
```

## Gem Groups

```ruby
# Define groups
group :development do
  gem 'pry'
end

group :test do
  gem 'rspec'
end

group :development, :test do
  gem 'factory_bot'
end

# Install without specific groups
bundle install --without production

# Require specific groups
Bundler.require(:default, :development)
```

## Gem Sources

```ruby
# Primary source
source 'https://rubygems.org'

# Additional sources
source 'https://gems.example.com' do
  gem 'private_gem'
end

# Git sources
gem 'my_gem', git: 'https://github.com/user/my_gem.git'
gem 'my_gem', git: 'https://github.com/user/my_gem.git', tag: 'v1.0'
gem 'my_gem', git: 'https://github.com/user/my_gem.git', branch: 'main'
gem 'my_gem', git: 'https://github.com/user/my_gem.git', ref: 'abc123'

# GitHub shorthand
gem 'my_gem', github: 'user/my_gem'

# Local path
gem 'my_gem', path: '../my_gem'
```

## Requiring Gems

```ruby
# In code
require 'my_gem'

# Bundler auto-requires gems based on Gemfile
# To disable auto-require:
gem 'my_gem', require: false

# Then manually require where needed:
require 'my_gem'

# Require specific file
gem 'sidekiq', require: 'sidekiq/web'
```

## Platform-Specific Gems

```ruby
# Only install on specific platforms
gem 'pg', platforms: :ruby
gem 'sqlite3', platforms: [:mingw, :mswin, :x64_mingw]

# Multiple platforms
platforms :ruby do
  gem 'pg'
  gem 'nokogiri'
end

platforms :jruby do
  gem 'activerecord-jdbc-adapter'
end
```

## Private Gems

### Using Private Gem Server

```ruby
# Gemfile
source 'https://rubygems.org'

source 'https://gems.mycompany.com' do
  gem 'private_gem'
end
```

### Using Git Credentials

```bash
# .netrc file for private repos
machine github.com
  login your-username
  password your-token
```

## Gem Development

### Using `bundle console`

```bash
# Open IRB with gem loaded
bin/console

# Or
bundle console
```

### Running Tests

```bash
# Using Rake
rake spec

# Or directly
bundle exec rspec
```

### Local Development

```ruby
# In your app's Gemfile, point to local gem
gem 'my_gem', path: '../my_gem'

# Or use bundle config
bundle config local.my_gem ../my_gem
```

## Best Practices

1. **Always commit Gemfile.lock** to version control
2. **Use pessimistic versioning** (~>) for stability
3. **Keep gems updated** but test thoroughly
4. **Use groups** to separate dev/test/production gems
5. **Specify Ruby version** in Gemfile for consistency
6. **Use bundle exec** to ensure correct gem versions
7. **Document gem dependencies** and why they're needed
8. **Test gems locally** before publishing
9. **Follow semantic versioning** for your gems
10. **Keep gemspecs clean** and well-documented

## Anti-Patterns

❌ **Don't commit vendor/bundle** to git (use .gitignore)
❌ **Don't use `require: false` unnecessarily** - adds manual work
❌ **Don't specify exact versions** unless absolutely necessary
❌ **Don't push untested gem versions** to RubyGems
❌ **Don't include unnecessary files** in gem packages
❌ **Don't hardcode credentials** in gemspec or Gemfile

## Troubleshooting

```bash
# Clear bundler cache
bundle clean --force

# Regenerate Gemfile.lock
rm Gemfile.lock && bundle install

# Check for gem conflicts
bundle exec gem dependency

# Verbose output
bundle install --verbose

# Show why a gem is needed
bundle show rails

# List all gem versions
bundle list
```

## Related Skills

- ruby-oop - For structuring gem code
- ruby-metaprogramming - Used in many gems
- ruby-standard-library - Core Ruby functionality
