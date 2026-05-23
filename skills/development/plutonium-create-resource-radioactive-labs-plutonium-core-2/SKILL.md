---
name: plutonium-create-resource
description: Generate Plutonium resources with models, migrations, controllers, policies, and definitions
---

# Create Resource Skill

Use the `pu:res:scaffold` generator to create complete resources in Plutonium applications.

## Command Syntax

```bash
rails g pu:res:scaffold MODEL_NAME \
    field1:type \
    field2:type \
    --dest=DESTINATION
```

**IMPORTANT**: Always specify `--dest` to avoid interactive prompts:
- `--dest=main_app` for resources in the main application
- `--dest=package_name` for resources in a feature package

**IMPORTANT**: Quote fields containing `?` or `{}` to prevent shell expansion:
```bash
'field:type?'              # Nullable - must quote
'field:decimal{10,2}'      # Options - must quote
'field:decimal?{10,2}'     # Both - must quote
```

## From Existing Models

For existing Rails projects with models you want to convert to Plutonium resources:

### Option 1: Model already includes Plutonium::Resource::Record

```bash
rails g pu:res:scaffold Post --no-migration --dest=main_app
```

This generates only the definition, policy, and controller - leaving your model unchanged.

### Option 2: Let the generator update the model

```bash
rails g pu:res:scaffold Post --dest=main_app
```

Run without attributes to auto-import fields from `model.content_columns`. This regenerates the model file, so review changes carefully.

### Don't forget to include the module

Your model must include `Plutonium::Resource::Record` (directly or via inheritance):

```ruby
class Post < ApplicationRecord
  include Plutonium::Resource::Record
end

# Or inherit from a base class
class Post < ResourceRecord
end
```

## Field Type Syntax

Format: `name:type:index_type`

### Basic Types

| Syntax | Result |
|--------|--------|
| `name:string` | Required string |
| `'name:string?'` | Nullable string |
| `age:integer` | Required integer |
| `'age:integer?'` | Nullable integer |
| `active:boolean` | Required boolean |
| `'active:boolean?'` | Nullable boolean |
| `content:text` | Required text |
| `'content:text?'` | Nullable text |
| `birth_date:date` | Required date |
| `'anniversary:date?'` | Nullable date |
| `starts_at:datetime` | Required datetime |
| `'ends_at:datetime?'` | Nullable datetime |
| `alarm_time:time` | Required time |
| `'reminder_time:time?'` | Nullable time |
| `metadata:json` | JSON field |
| `settings:jsonb` | JSONB (PostgreSQL) |
| `external_id:uuid` | UUID field |

### PostgreSQL-Specific Types

These types work in both PostgreSQL and SQLite (automatically mapped):

| Type | PostgreSQL | SQLite |
|------|------------|--------|
| `jsonb` | `jsonb` | `json` |
| `hstore` | `hstore` | `json` |
| `uuid` | `uuid` | `string` |
| `inet` | `inet` | `string` |
| `cidr` | `cidr` | `string` |
| `macaddr` | `macaddr` | `string` |
| `ltree` | `ltree` | `string` |

### Default Values

Use `{default:value}` syntax for default values:

```bash
'status:string{default:draft}'           # String default
'active:boolean{default:true}'           # Boolean default (true/false/yes/1)
'priority:integer{default:0}'            # Integer default
'rating:float{default:4.5}'              # Float default
'status:string?{default:pending}'        # Nullable with default
```

### JSON/JSONB Default Values

Supports nested braces for structured defaults:

```bash
'metadata:jsonb{default:{}}'             # Empty hash
'tags:jsonb{default:[]}'                 # Empty array
'settings:jsonb{default:{"theme":"dark"}}' # Object with values
'config:jsonb?{default:{}}'              # Nullable with empty hash default
```

Default values are parsed as JSON first. If JSON parsing fails, the value is treated as a string (or coerced based on column type for integers, floats, and booleans).

### Decimal with Precision and Default

```bash
'amount:decimal{10,2}'                   # precision: 10, scale: 2
'price:decimal{10,2,default:0}'          # with default value
'balance:decimal?{15,2,default:0}'       # nullable with precision and default
```

### References/Associations

```bash
company:belongs_to                 # Required foreign key
'parent:belongs_to?'               # Nullable (null: true + optional: true)
user:references                    # Same as belongs_to
blogging/post:belongs_to           # Cross-package reference
'author:belongs_to{class_name:User}'     # Custom class_name (author_id -> User)
'reviewer:belongs_to?{class_name:User}'  # Nullable with class_name
```

Nullable references generate:
- Migration: `null: true`
- Model: `belongs_to :parent, optional: true`

### Index Types (third segment)

```bash
email:string:index                 # Regular index
email:string:uniq                  # Unique index
```

### Special Types

```bash
password_digest                    # has_secure_password
auth_token:token                   # has_secure_token (auto unique index)
content:rich_text                  # has_rich_text
avatar:attachment                  # has_one_attached
photos:attachments                 # has_many_attached
price_cents:integer                # has_cents (money field)
```

Token fields automatically get a unique index in the migration.

## Generator Options

- `--dest=DESTINATION` - Target destination (**always required** to avoid prompts)
  - `main_app` for main application resources
  - `package_name` for feature package resources
- `--no-model` - Skip model generation (keeps existing model)
- `--no-migration` - Skip migration generation (use with `--no-model` for existing models)

## What Gets Generated

For **main_app** resources:
1. **Model** - `app/models/model_name.rb`
2. **Migration** - `db/migrate/xxx_create_model_names.rb`
3. **Controller** - `app/controllers/model_names_controller.rb`
4. **Policy** - `app/policies/model_name_policy.rb`
5. **Definition** - `app/definitions/model_name_definition.rb`

For **packaged** resources:
1. **Model** - `app/models/package_name/model_name.rb`
2. **Migration** - `db/migrate/xxx_create_package_name_model_names.rb`
3. **Controller** - `packages/package_name/app/controllers/package_name/model_names_controller.rb`
4. **Policy** - `packages/package_name/app/policies/package_name/model_name_policy.rb`
5. **Definition** - `packages/package_name/app/definitions/package_name/model_name_definition.rb`

## Migration Customizations

The generator creates basic migrations. **Always review and customize** the migration before running:

### Inline Indexes (preferred)

```ruby
create_table :model_names do |t|
  t.belongs_to :parent, null: false, foreign_key: true
  t.string :name, null: false

  t.timestamps

  t.index :name
  t.index [:parent_id, :name], unique: true
end
```

### Cascade Delete

```ruby
t.belongs_to :parent, null: false, foreign_key: {on_delete: :cascade}
```

### Default Values

Default values can be set directly in the generator using `{default:value}` syntax (see Field Type Syntax above). For more complex defaults or expressions, edit the migration:

```ruby
t.boolean :is_active, default: true
t.integer :status, default: 0
t.datetime :published_at, default: -> { "CURRENT_TIMESTAMP" }
```

## Examples

### Main App Resource

```bash
rails g pu:res:scaffold Post \
    user:belongs_to \
    title:string \
    'content:text?' \
    'published_at:datetime?' \
    --dest=main_app
```

### Resource with Precision and Indexes

```bash
rails g pu:res:scaffold Property \
    company:belongs_to \
    code:string:uniq \
    'latitude:decimal{11,8}' \
    'longitude:decimal?{11,8}' \
    'value:decimal?{15,2}' \
    'notes:text?' \
    --dest=main_app
```

### Optional Association

```bash
rails g pu:res:scaffold Comment \
    user:belongs_to \
    'parent:belongs_to?' \
    body:text \
    --dest=blogging
```

### Cross-Package Reference

```bash
rails g pu:res:scaffold Comment \
    user:belongs_to \
    blogging/post:belongs_to \
    body:text \
    --dest=comments
```

## After Generation

1. **Review and customize the migration** (add cascade delete, defaults, composite indexes)
2. Run `rails db:migrate`
3. Connect resource to portal: `rails g pu:res:conn Post --dest=admin_portal`
4. Customize policy permissions as needed
5. Add definition customizations for UI behavior
