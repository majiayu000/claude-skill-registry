---
name: linear
cluster: community
description: "Linear: issue tracking, cycles, projects, roadmaps, Git integration, SLA tracking, API"
tags: ["linear","issues","engineering","project"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "linear issue cycle project roadmap git sla api engineering"
---

# linear

## Purpose
This skill enables the AI to interact with Linear's API for issue tracking, cycle management, project roadmaps, Git integrations, SLA monitoring, and API-driven workflows, specifically for engineering teams.

## When to Use
Use this skill when automating engineering workflows, such as creating issues from code changes, updating project roadmaps, tracking SLAs for tickets, or syncing Git commits with Linear issues. Apply it in scenarios involving team collaboration, like querying issues during sprint planning or integrating with CI/CD pipelines.

## Key Capabilities
- **Issue Management**: Create, update, and query issues using Linear's GraphQL API at https://api.linear.app/graphql.
- **Cycle and Project Handling**: Manage cycles via mutations like `cycleCreate` and projects with queries for roadmaps.
- **Git Integration**: Link Git commits to issues using webhooks or API; for example, associate a commit SHA with an issue ID.
- **SLA Tracking**: Monitor service level agreements by querying issue states and timestamps.
- **API Access**: Authenticate with a personal API key and perform operations like fetching issues with filters (e.g., state: "todo").
- **Config Formats**: Store API keys in environment variables like `$LINEAR_API_KEY`; use JSON for payload structures in requests.

## Usage Patterns
To accomplish tasks, always authenticate first by setting `$LINEAR_API_KEY` in your environment. For querying data, use GraphQL queries; for mutations, provide input objects. Pattern for issue creation: Authenticate → Prepare mutation payload → Send request → Handle response. For integrations, combine with Git tools by parsing commit messages and mapping to Linear issues. Always validate inputs, like ensuring issue titles are under 255 characters, before sending requests.

## Common Commands/API
- **Query Issues**: Use this GraphQL query to fetch open issues:
  ```
  query { issues(filter: { state: { name: { eq: "todo" } } }) { nodes { id title } } }
  ```
  Send via curl: `curl -H "Authorization: Bearer $LINEAR_API_KEY" -X POST https://api.linear.app/graphql -d '{"query": "above query"}'`
- **Create an Issue**: Execute this mutation to add a new issue:
  ```
  mutation { issueCreate(input: { title: "Fix bug in login", description: "Details here" }) { issue { id } } }
  ```
  Command: `curl -H "Authorization: Bearer $LINEAR_API_KEY" -X POST https://api.linear.app/graphql -d '{"query": "above mutation"}'`
- **Update Project Roadmap**: Query projects first, then mutate: `mutation { projectUpdate(id: "proj_123", name: "Updated Roadmap") { project { id } } }`
- **Git Integration Command**: To link a Git commit, use: `git log --format="%H %s" | awk '{print $1}' | xargs -I {} curl -H "Authorization: Bearer $LINEAR_API_KEY" -X POST https://api.linear.app/graphql -d '{"query": "mutation { issueUpdate(id: \"iss_456\", branch: \"{}\") { issue { id } } }"}'`
- **SLA Check**: Query: `query { issues(filter: { createdAt: { gt: "2023-01-01" } }) { nodes { id slaViolated } } }`

## Integration Notes
Set up authentication by exporting `$LINEAR_API_KEY` from your Linear account settings. For Git integration, configure webhooks in Linear to trigger on issue updates and parse payloads in scripts (e.g., using Python's requests library). Config format: Use a .env file with `LINEAR_API_KEY=your_key_here`, then load it in scripts via `os.environ.get('LINEAR_API_KEY')`. To integrate with other tools, chain API calls; for example, after a Git push, run a script that queries Linear issues and updates them. Ensure rate limits (e.g., 100 requests/min) are respected by adding delays in loops.

## Error Handling
Check for authentication errors (e.g., 401 status) by verifying `$LINEAR_API_KEY` before requests; if failed, prompt user to set the env var. For GraphQL errors, parse the "errors" field in responses (e.g., if "message" contains "Invalid input", validate payloads like ensuring required fields are present). Handle network issues with retries: Use a loop with exponential backoff, like `for i in 1..3; do curl ...; if [ $? -ne 0 ]; then sleep $((2**i)); fi; done`. For SLA violations, catch query errors by checking if issues return null values and log them. Always wrap API calls in try-catch blocks in code, e.g.:
  ```
  try { response = requests.post('https://api.linear.app/graphql', headers={'Authorization': f'Bearer {os.environ["LINEAR_API_KEY"]}'}, json={'query': '...'}) } catch e { print(f'Error: {e}') }
  ```

## Concrete Usage Examples
1. **Automate Issue Creation from Code Review**: When a pull request is opened in GitHub, use this script to create a Linear issue: Set `$LINEAR_API_KEY`, then run `curl -H "Authorization: Bearer $LINEAR_API_KEY" -X POST https://api.linear.app/graphql -d '{"query": "mutation { issueCreate(input: { title: \"Review PR #123\", description: \"Fixes in branch main\" }) { issue { id } } }"}'`. This links the PR to a new issue for tracking.
2. **Track SLA for Overdue Issues**: Query and notify on SLA breaches: First, export `$LINEAR_API_KEY`, then execute `curl -H "Authorization: Bearer $LINEAR_API_KEY" -X POST https://api.linear.app/graphql -d '{"query": "query { issues(filter: { slaViolated: true }) { nodes { id title } } }"}' | jq '.data.issues.nodes' > overdue_issues.json`. Process the JSON to send alerts, ensuring issues older than 48 hours are flagged.

## Graph Relationships
- Related to: "git" (for commit integrations), "issues" (for tracking workflows), "engineering" (for team management), "project" (for roadmap syncing).
- Connections: This skill can chain with "git" skills via API calls for automated linking; integrates with "engineering" for broader tool ecosystems.
