---
name: ash-framework
description: "Ash Framework — resources, actions, policies, aggregates, calculations, AshPhoenix.Form, LiveView, migrations. Use when generating resources via mix ash.codegen, editing changes, checks, types, validations, or domain code interfaces."
effort: medium
user-invocable: false
---

# Ash Framework Reference

Reference for Ash Framework in Phoenix/LiveView projects.
Ash complements Phoenix/Ecto — LiveView, security, and OTP Iron Laws still apply.
Only data access patterns shift toward Ash actions and domain code interfaces.

## Iron Laws

1. **USE DOMAIN CODE INTERFACES** — Never call `Ash.create/Ash.read` directly in LiveViews or Controllers; use domain code interfaces: `MyApp.Accounts.register_user()` not `Ash.create(User, attrs)`
2. **SET ACTOR/SCOPE AT QUERY PREP, NOT EXECUTION** — Pass `actor:` or `scope:` to
   `for_read/for_create/for_action` (prep), NOT to `Ash.read!/Ash.create!` (execution);
   execution-level actor bypasses row-level policy evaluation. If project uses `Ash.Scope`,
   pass `scope:` consistently instead of bare `actor:` — do not mix styles
3. **GENERATORS FIRST** — Before writing Ash code manually, run `mix ash.gen.resource` or `mix ash.gen.domain` with `--yes`; check `mix help ash.gen.<task>` for options
4. **CODEGEN AFTER RESOURCE CHANGES** — Always run `mix ash.codegen` after modifying resources; this generates migrations from resource snapshots — never write AshPostgres migrations by hand
5. **ACTIONS OVER FUNCTIONS** — Put business logic in named actions, not domain functions; expose via code interfaces defined on the domain
6. **NEVER EDIT RESOURCE SNAPSHOTS** — `priv/resource_snapshots/` is owned exclusively by `mix ash.codegen`; manual edits corrupt migration tracking
7. **NO DIRECT `Repo.*` IN ASH PROJECTS** — `Repo.all/get/insert` bypass Ash policies and notifications; use domain code interfaces. Any `Repo` call in an Ash project is an escape hatch and must be documented

## Quick Reference

### Domain Code Interface Pattern

```elixir
# Domain definition
defmodule MyApp.Accounts do
  use Ash.Domain

  resources do
    resource MyApp.Accounts.User do
      define :register_user, action: :create, args: [:email, :password]
      define :get_user_by_email, action: :read, get_by: [:email]
    end
  end
end

# In LiveView/Controller — always via domain, never Ash.create directly
{:ok, user} = MyApp.Accounts.register_user(email, password, actor: nil)
user = MyApp.Accounts.get_user_by_email!(email, actor: current_user)
```

### Authorization — Actor/Scope at Query Prep

```elixir
# CORRECT — actor at query prep, policies evaluated per-row
MyApp.Post
|> Ash.Query.for_read(:list_published, %{}, actor: current_user)
|> Ash.read!()

# CORRECT with Ash.Scope (carries actor + tenant + context; use if project adopts it)
MyApp.Post
|> Ash.Query.for_read(:list_published, %{}, scope: scope)
|> Ash.read!()

# WRONG — actor at execution bypasses row-level policy evaluation
MyApp.Post
|> Ash.Query.for_read(:list_published)
|> Ash.read!(actor: current_user)
```

### Ash.Scope — When the Project Uses It

`Ash.Scope` bundles `actor + tenant + context` into a single struct passed through actions.
Implement `Ash.Scope.ToOpts` on a project-defined scope struct:

```elixir
defimpl Ash.Scope.ToOpts, for: MyApp.Scope do
  def get_actor(%{current_user: u}), do: {:ok, u}
  def get_tenant(%{current_tenant: t}), do: {:ok, t}
  def get_context(%{locale: l}), do: {:ok, %{shared: %{locale: l}}}
  def get_tracer(_), do: :error
  def get_authorize?(_), do: :error
end
```

**Detection**: if the project has a `Scope` module implementing `Ash.Scope.ToOpts`, use
`scope:` everywhere instead of bare `actor:`. Do NOT mix the two styles in the same codebase.
See `mix usage_rules.docs Ash.Scope` for full protocol spec.

### File Conventions (from `mix ash.gen.*`)

| File           | Location                          | Behaviour                     |
| -------------- | --------------------------------- | ----------------------------- |
| Changes        | `lib/app/ctx/changes/name.ex`     | `use Ash.Resource.Change`     |
| Policy Checks  | `lib/app/ctx/checks/name.ex`      | `use Ash.Policy.Check`        |
| Custom Actions | `lib/app/ctx/actions/name.ex`     | generic action logic          |
| Custom Types   | `lib/app/ctx/types/name.ex`       | `use Ash.Type`                |
| Validations    | `lib/app/ctx/validations/name.ex` | `use Ash.Resource.Validation` |

### Generator Workflow

```bash
mix ash.gen.resource MyApp.Accounts.User --yes
mix ash.gen.domain MyApp.Accounts --yes
mix ash.codegen        # reads resource snapshots → generates migration
mix ash.migrate
```

## Research

Prefer the highest-fidelity source available:

1. **Tidewave** (exact version from `mix.lock`):

   ```
   mcp__tidewave__get_docs(module: "Ash.Resource")
   mcp__tidewave__get_docs(module: "AshPhoenix.Form")
   ```

2. **usage_rules** (project-synced to your installed ash_* dep versions):

   ```bash
   mix usage_rules.search_docs "<topic>" -p ash -p ash_phoenix -p ash_postgres -p ash_authentication -p ash_oban
   mix usage_rules.docs Ash.Resource
   ```

3. **WebFetch hexdocs.pm** (fallback when neither is available):

   ```
   WebFetch(url: "https://hexdocs.pm/ash/Ash.Resource.html", prompt: "Extract module docs.")
   ```

If `usage_rules` is not configured, the SessionStart hook suggests how to install it.
