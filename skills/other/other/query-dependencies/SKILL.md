# Query Issue Dependencies

Shows what blocks an issue and what it blocks.

## Usage

When an agent needs to query dependencies:

```bash
gh api graphql -f query='
query {
  repository(owner: "joeczar", name: "code-graph-mcp") {
    issue(number: <issue-number>) {
      number
      title
      state
      blockedBy(first: 20) {
        nodes { number title state }
      }
      blocking(first: 20) {
        nodes { number title state }
      }
    }
  }
}' --jq '.data.repository.issue'
```

## Example

Query dependencies for issue #10:

```bash
gh api graphql -f query='
query {
  repository(owner: "joeczar", name: "code-graph-mcp") {
    issue(number: 10) {
      number
      title
      state
      blockedBy(first: 20) {
        nodes { number title state }
      }
      blocking(first: 20) {
        nodes { number title state }
      }
    }
  }
}' --jq '.data.repository.issue'
```

## Output Example

```json
{
  "number": 10,
  "title": "parse_file tool",
  "state": "OPEN",
  "blockedBy": {
    "nodes": [
      {"number": 12, "title": "AST walker base class", "state": "OPEN"},
      {"number": 13, "title": "TypeScript entity extraction", "state": "OPEN"}
    ]
  },
  "blocking": {
    "nodes": [
      {"number": 11, "title": "parse_directory tool", "state": "OPEN"}
    ]
  }
}
```
