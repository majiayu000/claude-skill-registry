---
name: template-mason-brick
description: Guide for creating, updating, or removing Mason bricks with corresponding tests and CI workflow (project)
---

# Mason Brick Development Skill

This skill guides the creation, modification, and removal of Mason bricks, ensuring test coverage and CI workflow integration.

## When to Use

Trigger this skill when:
- Creating a new Mason brick template
- Updating an existing brick's structure or variables
- Removing a brick from the project
- User asks to "create a brick", "add a mason template", "update brick", or "remove brick"

## Project Structure

Bricks are organized in three locations:

```
bricks/                    # Mason template definitions
├── brick_name/
│   ├── brick.yaml         # Brick configuration and variables
│   ├── __brick__/         # Template files with Mustache syntax
│   └── hooks/             # Optional pre/post generation hooks

test_bricks/               # Brick tests (one folder per brick)
├── brick_name/
│   └── brick_name_test.dart

.github/workflows/
└── brick-test.yml         # Parallel CI jobs for each brick
```

## Creating a New Brick

### Step 1: Create Brick Directory

```bash
mkdir -p bricks/new_brick/__brick__
```

### Step 2: Create brick.yaml

```yaml
name: new_brick
description: Description of what this brick generates
version: 0.1.0+1

environment:
  mason: ^0.1.1

vars:
  name:
    type: string
    description: The name for the generated component
    prompt: What is the name?

  # Add more variables as needed
  optional_var:
    type: boolean
    description: Optional feature flag
    default: true
```

### Step 3: Create Template Files

In `__brick__/`, create files using Mustache syntax:

```
__brick__/
├── {{name.snakeCase()}}/
│   ├── lib/
│   │   └── {{name.snakeCase()}}.dart
│   ├── pubspec.yaml
│   └── README.md
```

Use these Mustache helpers:
- `{{name}}` - raw value
- `{{name.snakeCase()}}` - snake_case
- `{{name.pascalCase()}}` - PascalCase
- `{{name.camelCase()}}` - camelCase
- `{{name.paramCase()}}` - param-case
- `{{#flag}}...{{/flag}}` - conditional block
- `{{^flag}}...{{/flag}}` - inverted conditional

### Step 4: Create Brick Test

Create `test_bricks/new_brick/new_brick_test.dart`:

```dart
import 'dart:io';
import 'package:mason/mason.dart';
import 'package:path/path.dart' as path;
import 'package:test/test.dart';

void main() {
  group('New Brick Tests', () {
    late Directory tempDir;

    setUp(() async {
      tempDir = await Directory.systemTemp.createTemp('new_brick_test_');
    });

    tearDown(() async {
      if (await tempDir.exists()) {
        await tempDir.delete(recursive: true);
      }
    });

    test('generates correct structure', () async {
      final brick = Brick.path(path.join('..', '..', 'bricks', 'new_brick'));

      final generator = await MasonGenerator.fromBrick(brick);
      await generator.generate(
        DirectoryGeneratorTarget(tempDir),
        vars: {'name': 'test_name'},
      );

      // Verify generated files exist
      final file = File(path.join(tempDir.path, 'test_name', 'pubspec.yaml'));
      expect(await file.exists(), isTrue);
    });

    // Add more tests for different variable combinations
  });
}
```

### Step 5: Add Workflow Job

Add a new job to `.github/workflows/brick-test.yml`:

```yaml
  new-brick:
    name: Test new_brick
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - uses: flutter-actions/setup-flutter@v4

      - name: Cache dependencies
        uses: actions/cache@v5
        with:
          path: |
            ~/.pub-cache
            .dart_tool
          key: ${{ runner.os }}-pub-${{ hashFiles('**/pubspec.lock') }}
          restore-keys: ${{ runner.os }}-pub-

      - name: Install tools
        run: dart pub global activate melos

      - name: Prepare project
        run: |
          melos run prepare
          mason get

      - name: Test new_brick brick
        run: dart run test_bricks/new_brick/new_brick_test.dart
```

### Step 6: Register Brick

Add to root `mason.yaml`:

```yaml
bricks:
  new_brick:
    path: bricks/new_brick
```

Then run `mason get` to register.

## Updating an Existing Brick

When modifying a brick:

1. Update `brick.yaml` if adding/removing variables
2. Update template files in `__brick__/`
3. **Update tests** in `test_bricks/brick_name/` to cover changes
4. Run test locally: `dart run test_bricks/brick_name/brick_name_test.dart`
5. Increment version in `brick.yaml`

## Removing a Brick

When removing a brick, update all three locations:

1. Remove brick directory: `rm -rf bricks/brick_name`
2. Remove test directory: `rm -rf test_bricks/brick_name`
3. Remove workflow job from `.github/workflows/brick-test.yml`
4. Remove from `mason.yaml`
5. Update CLAUDE.md if the brick was documented

## Testing Locally

```bash
# Register bricks
mason get

# Test a specific brick
dart run test_bricks/brick_name/brick_name_test.dart

# Test brick generation manually
mason make brick_name -o /tmp/test_output --var1=value1
```

## Existing Bricks Reference

| Brick | Purpose | Key Variables |
|-------|---------|---------------|
| `screen` | Flutter screen with routing | `name`, `folder`, `has_adaptive_scaffold` |
| `widget` | Reusable widget | `name`, `type`, `folder` |
| `simple_bloc` | Basic BLoC package | `name` |
| `list_bloc` | List management BLoC | `name` |
| `form_bloc` | Form validation BLoC | `name`, `field_names` |
| `repository` | Data repository | `name` |
| `api_client` | API client package | `package_name` |
| `native_federation_plugin` | Federated native plugin | `name`, `package_prefix`, `support_*` |

## Checklist

When creating/updating a brick:

- [ ] `brick.yaml` has name, description, version, and vars
- [ ] Template files use correct Mustache syntax
- [ ] Test file exists in `test_bricks/brick_name/`
- [ ] Tests cover main generation paths
- [ ] Workflow job added/updated in `brick-test.yml`
- [ ] Brick registered in `mason.yaml`
- [ ] Run `mason get` to verify registration
- [ ] Run test locally before committing
