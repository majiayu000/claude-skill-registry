---
name: flutter-pub
description: "[Flutter] pub.dev package search skill. Quick package search, info lookup, version check, and dependency analysis. (project)"
---

# Flutter pub.dev Package Finder

> Quick search and lookup for Flutter/Dart packages on pub.dev

---

## When to Use

Use this skill when:
- "Find ~~ package"
- "Search pub.dev for ~~"
- "Tell me about ~~ library"
- Need to check latest version, score, or dependencies

---

## pub.dev API Reference

### Package Search

```
GET https://pub.dev/api/search?q={query}
```

| Parameter | Description | Example |
|-----------|-------------|---------|
| `q` | Search query | `state management` |
| `page` | Page number | `1`, `2`, ... |

### Package Details

```
GET https://pub.dev/api/packages/{package_name}
```

**Response Fields:**
- `name` - Package name
- `latest.version` - Latest version
- `latest.pubspec` - pubspec.yaml contents
- `versions` - All version list

### Package Score

```
GET https://pub.dev/api/packages/{package_name}/score
```

**Response Fields:**
- `likeCount` - Number of likes
- `downloadCount30Days` - 30-day download count
- `maxPoints` - Maximum points
- `grantedPoints` - Granted points
- `tags` - Platform tags (sdk:flutter, platform:android, etc.)

### Publisher Info

```
GET https://pub.dev/api/packages/{package_name}/publisher
```

---

## Workflow

### 1. Package Search

When user asks to find packages:

1. **Call search API via WebFetch**
   ```
   https://pub.dev/api/search?q={query}
   ```

2. **Extract top 5 packages**
   - Package name
   - Latest version

3. **Present as table**
   | Package | Version | Description |
   |---------|---------|-------------|
   | provider | 6.1.1 | State management |

### 2. Package Details Lookup

When specific package info requested:

1. **Call package info API**
   ```
   https://pub.dev/api/packages/{package_name}
   ```

2. **Call score API**
   ```
   https://pub.dev/api/packages/{package_name}/score
   ```

3. **Summarize info**
   - Latest version
   - Dependencies list
   - Platform support
   - Likes/Downloads
   - pub.dev link

### 3. pubspec.yaml Addition Guide

When package installation requested:

```yaml
dependencies:
  {package_name}: ^{version}
```

---

## Output Format

### Search Results

```markdown
## pub.dev Search: "{query}"

| Package | Version | Score | Description |
|---------|---------|-------|-------------|
| package1 | 1.0.0 | 140 | Description1 |
| package2 | 2.0.0 | 130 | Description2 |

> [See more on pub.dev](https://pub.dev/packages?q={query})
```

### Package Details

```markdown
## {package_name}

- **Version**: {version}
- **Publisher**: {publisher}
- **Likes**: {likes} | **Downloads (30d)**: {downloads}
- **Score**: {points}/{maxPoints}
- **Platforms**: Android, iOS, Web, ...

### Installation
\`\`\`yaml
dependencies:
  {package_name}: ^{version}
\`\`\`

### Dependencies
- dep1: ^1.0.0
- dep2: ^2.0.0

> [pub.dev](https://pub.dev/packages/{package_name}) | [API Docs](https://pub.dev/documentation/{package_name}/latest/)
```

---

## Examples

### Search Example

**Input**: "Find state management packages"

**AI Actions**:
1. WebFetch `https://pub.dev/api/search?q=state+management`
2. Parse results and create table
3. Explain recommended packages

### Detail Lookup Example

**Input**: "Tell me about riverpod"

**AI Actions**:
1. WebFetch `https://pub.dev/api/packages/flutter_riverpod`
2. WebFetch `https://pub.dev/api/packages/flutter_riverpod/score`
3. Format detailed info

---

## Notes

- Consider API rate limits, avoid rapid successive calls
- URL encode search queries
- Package names are case-insensitive
- Flutter packages often have `flutter_` prefix

---

## Related Links

- [pub.dev](https://pub.dev/)
- [pub.dev API Docs](https://pub.dev/help/api)
- [Dart Packages](https://pub.dev/packages)
