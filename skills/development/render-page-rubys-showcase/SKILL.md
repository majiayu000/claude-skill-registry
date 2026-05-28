---
name: render-page
description: Use this skill to inspect what a Rails page currently displays, extract HTML content, or verify rendering WITHOUT starting a dev server. Useful for understanding page output before making changes, debugging views, searching for content, or testing that pages work correctly. Provides scripts/render.rb for quick page inspection and HTML extraction.
---

# Render Pages Without Starting a Server

Use the `scripts/render.rb` tool to verify page rendering, extract HTML, or search content in rendered pages.

### Basic Usage

The script accepts the database either as an argument or via RAILS_APP_DB environment variable:

```bash
# Pass database as argument
scripts/render.rb db/2025-alexandria-80-s-neon-nights.sqlite3 /people

# Or just the database name
scripts/render.rb 2025-alexandria-80-s-neon-nights /people

# Or use environment variable
RAILS_APP_DB=2025-alexandria-80-s-neon-nights scripts/render.rb /people
```

Common operations:

```bash
# Check if pages render successfully
scripts/render.rb 2025-alexandria-80-s-neon-nights --check /people /heats /solos

# Show summary with page sizes
scripts/render.rb 2025-alexandria-80-s-neon-nights /people /heats

# Get full HTML output (single page only)
scripts/render.rb 2025-alexandria-80-s-neon-nights --html /solos

# Search for specific content in rendered pages
scripts/render.rb 2025-alexandria-80-s-neon-nights --search "Solos" /solos
```

### Script Options

- `--check` - Only check if page renders (exit 0 on success, 1 on failure)
- `--html` - Output full HTML content (works with single path only)
- `--search TEXT` - Search for specific text in rendered output
- `--verbose, -v` - Show detailed information
- `--help, -h` - Show help message

## Common Workflows

### 1. Verify Pages Render Successfully

Test multiple pages at once and see their sizes:

```bash
scripts/render.rb db/DATABASE.sqlite3 /people /heats /solos
```

For CI/CD pipelines, use `--check` mode (silent, exit code indicates success):

```bash
scripts/render.rb db/DATABASE.sqlite3 --check /people /heats /solos
echo $?  # 0 = all succeeded, 1 = at least one failed
```

### 2. Search for Content in Rendered Pages

Verify specific content appears in a page:

```bash
scripts/render.rb db/DATABASE.sqlite3 --search "Rhythm Solos" /solos
# Output: ✓ /solos - 'Rhythm Solos' found
```

### 3. Extract HTML for Analysis

Save rendered HTML to a file for inspection:

```bash
scripts/render.rb db/DATABASE.sqlite3 --html /heats > heats.html
```

## Advanced: Custom Scripts with Rails API

For complex custom logic, write a Ruby script using Rails' routing API directly:

```ruby
# custom_test.rb
env = { "PATH_INFO" => '/heats', "REQUEST_METHOD" => "GET" }
code, headers, response = Rails.application.routes.call(env)

if code == 200
  html = response.body.force_encoding('utf-8')
  puts "Success: #{html.length} bytes"
else
  puts "Error: #{code}"
  exit 1
end
```

Run with `bin/run db/DATABASE.sqlite3 custom_test.rb`

See `lib/tasks/prerender.rake` for a production example of this technique.
