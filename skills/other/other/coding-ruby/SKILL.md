---
name: coding-ruby
cluster: coding
description: "Ruby 3.x: blocks/procs/lambdas, metaprogramming, modules, bundler, gems, Rails, RSpec"
tags: ["ruby","rails","coding"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "ruby rails gem bundler metaprogramming blocks modules rspec"
---

# coding-ruby

## Purpose
This skill allows the AI to generate, debug, and optimize Ruby 3.x code, focusing on advanced constructs like blocks, procs, lambdas, metaprogramming, modules, gem management with Bundler, Rails web apps, and RSpec testing.

## When to Use
Use this skill for tasks involving Ruby scripting, such as building web applications with Rails, managing dependencies via Bundler, writing unit tests with RSpec, or applying metaprogramming for dynamic code generation. Apply it when users request code for e-commerce sites, API backends, or custom gems.

## Key Capabilities
- Handle blocks and procs: Define and yield blocks in methods, e.g., for iterators.
- Implement metaprogramming: Use `define_method` or `method_missing` for dynamic class creation.
- Manage modules: Create and include modules for namespacing, like `module MyModule; end`.
- Work with Bundler: Install and manage gems via Gemfiles for dependency resolution.
- Build Rails apps: Generate models, controllers, and routes for MVC architecture.
- Write RSpec tests: Create specs for behavior-driven development, including matchers and mocks.

## Usage Patterns
To accomplish tasks, structure code with Ruby's idioms: use procs for callbacks, modules for reusable code, and metaprogramming for automation. For Rails, follow the MVC pattern; for RSpec, use describe/it blocks. Always check Ruby 3.x syntax, like pattern matching with `case` statements. To define a lambda: `my_lambda = ->(x) { x * 2 }`. Invoke it as `my_lambda.call(5)`. For metaprogramming, add methods dynamically: `class MyClass; define_method(:greet) { puts 'Hello' }; end`. Integrate Bundler by running `bundle install` after editing Gemfiles.

## Common Commands/API
Use these exact commands for Ruby tasks:
- Ruby CLI: Run `ruby -v` to verify version (e.g., 3.2.2), or start IRB with `irb` for interactive testing.
- Bundler: Execute `bundle install --path vendor/bundle` to install gems from a Gemfile; update with `bundle update gem_name`.
- Gems: Add a gem via Gemfile: `gem 'rspec', '~> 3.12'`; then run `bundle install`.
- Rails: Generate a new app with `rails new my_app --database=postgresql`; create a controller: `rails generate controller Users index`.
- RSpec: Run tests with `rspec spec/`, or a specific file: `rspec spec/models/user_spec.rb --format documentation`.
- API endpoints in Rails: Define routes in `config/routes.rb`, e.g., `resources :users`; access via `/users` in code.
Config formats: Use YAML for Rails configs, e.g., in `config/database.yml`: `default: &default adapter: postgresql username: user`. For authentication in gems, set env vars like `$RAILS_MASTER_KEY` for encrypted credentials.

## Integration Notes
Integrate this skill by setting up a Ruby environment first: Install Ruby 3.x via rbenv with `rbenv install 3.2.2` and set it globally with `rbenv global 3.2.2`. For Rails, add to Gemfile and run `bundle exec rails server` to start on port 3000. Use Bundler for gem isolation: Create a new gem set with `bundle init` and require gems in code like `require 'rspec'`. If external APIs are involved (e.g., via gems), handle auth with env vars: Set `$GEM_API_KEY` and access it in code as `ENV['GEM_API_KEY']`. For database integration, configure ActiveRecord in Rails models, e.g., `class User < ApplicationRecord; end`, and migrate with `rails db:migrate`.

## Error Handling
Handle Ruby errors prescriptively: Use begin/rescue blocks for exceptions, e.g.:
```ruby
begin
  File.open('nonexistent.txt')
rescue Errno::ENOENT => e
  puts "File not found: #{e.message}"
end
```
For Rails, check logs in `log/development.log` and use `rescue_from` in controllers for custom errors. In RSpec, expect errors with `expect { code }.to raise_error(SomeError)`. Common issues: Gem conflicts—resolve with `bundle clean --force`; syntax errors in Ruby 3.x—use `ruby -c file.rb` to check. For metaprogramming, catch NoMethodError with `method_missing` to define fallback behavior.

## Graph Relationships
- Related to: coding-python (shares metaprogramming concepts), coding-javascript (both use modules and callbacks).
- Clusters: Linked to "coding" cluster for general programming skills; connects to "web-development" via Rails integration.
- Dependencies: Requires "environment-setup" for Ruby installation; extends "testing-frameworks" through RSpec.
