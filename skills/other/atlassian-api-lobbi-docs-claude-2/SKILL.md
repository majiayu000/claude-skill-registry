---
name: atlassianapi
description: Atlassian API integration for Jira and Confluence automation. Activate for Atlassian REST APIs, webhooks, and platform integration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Atlassian API Skill

Provides comprehensive Atlassian API integration capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Jira REST API integration
- Confluence REST API integration
- Atlassian webhooks
- Automation and scripting
- Cross-platform synchronization

## Authentication

### API Token (Cloud)
\`\`\`python
import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('email@example.com', 'API_TOKEN')
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

base_url = 'https://your-domain.atlassian.net'
\`\`\`

### Python Client Library
\`\`\`python
from atlassian import Jira, Confluence

jira = Jira(
    url='https://your-domain.atlassian.net',
    username='email@example.com',
    password='API_TOKEN',
    cloud=True
)

confluence = Confluence(
    url='https://your-domain.atlassian.net',
    username='email@example.com',
    password='API_TOKEN',
    cloud=True
)
\`\`\`

## Jira REST API

### Issues
\`\`\`python
# Create issue
response = requests.post(
    f'{base_url}/rest/api/3/issue',
    auth=auth,
    headers=headers,
    json={
        'fields': {
            'project': {'key': 'GA'},
            'summary': 'Implement agent monitoring',
            'description': {
                'type': 'doc',
                'version': 1,
                'content': [
                    {
                        'type': 'paragraph',
                        'content': [
                            {'type': 'text', 'text': 'Description text'}
                        ]
                    }
                ]
            },
            'issuetype': {'name': 'Story'},
            'priority': {'name': 'High'},
            'labels': ['backend', 'monitoring']
        }
    }
)

# Get issue
response = requests.get(
    f'{base_url}/rest/api/3/issue/GA-123',
    auth=auth,
    headers=headers
)
issue = response.json()

# Update issue
response = requests.put(
    f'{base_url}/rest/api/3/issue/GA-123',
    auth=auth,
    headers=headers,
    json={
        'fields': {
            'summary': 'Updated summary'
        }
    }
)

# Transition issue
# First, get available transitions
transitions = requests.get(
    f'{base_url}/rest/api/3/issue/GA-123/transitions',
    auth=auth,
    headers=headers
).json()

# Then transition
requests.post(
    f'{base_url}/rest/api/3/issue/GA-123/transitions',
    auth=auth,
    headers=headers,
    json={'transition': {'id': '31'}}  # ID from available transitions
)

# Add comment
requests.post(
    f'{base_url}/rest/api/3/issue/GA-123/comment',
    auth=auth,
    headers=headers,
    json={
        'body': {
            'type': 'doc',
            'version': 1,
            'content': [
                {
                    'type': 'paragraph',
                    'content': [
                        {'type': 'text', 'text': 'Comment text'}
                    ]
                }
            ]
        }
    }
)
\`\`\`

### JQL Search
\`\`\`python
# Search issues
jql = 'project = GA AND status = "In Progress" ORDER BY created DESC'
response = requests.get(
    f'{base_url}/rest/api/3/search',
    auth=auth,
    headers=headers,
    params={
        'jql': jql,
        'maxResults': 50,
        'fields': 'summary,status,assignee,priority'
    }
)
results = response.json()

for issue in results['issues']:
    print(f"{issue['key']}: {issue['fields']['summary']}")
\`\`\`

### Sprints and Boards
\`\`\`python
# Get boards
boards = requests.get(
    f'{base_url}/rest/agile/1.0/board',
    auth=auth,
    headers=headers
).json()

# Get sprints for a board
board_id = 1
sprints = requests.get(
    f'{base_url}/rest/agile/1.0/board/{board_id}/sprint',
    auth=auth,
    headers=headers
).json()

# Get issues in sprint
sprint_id = 10
issues = requests.get(
    f'{base_url}/rest/agile/1.0/sprint/{sprint_id}/issue',
    auth=auth,
    headers=headers
).json()

# Move issues to sprint
requests.post(
    f'{base_url}/rest/agile/1.0/sprint/{sprint_id}/issue',
    auth=auth,
    headers=headers,
    json={'issues': ['GA-123', 'GA-124']}
)
\`\`\`

## Confluence REST API

### Pages
\`\`\`python
# Create page
response = requests.post(
    f'{base_url}/wiki/rest/api/content',
    auth=auth,
    headers=headers,
    json={
        'type': 'page',
        'title': 'Agent Architecture',
        'space': {'key': 'GA'},
        'body': {
            'storage': {
                'value': '<h1>Overview</h1><p>Content here...</p>',
                'representation': 'storage'
            }
        }
    }
)

# Get page
page = requests.get(
    f'{base_url}/wiki/rest/api/content/12345',
    auth=auth,
    headers=headers,
    params={'expand': 'body.storage,version'}
).json()

# Update page
requests.put(
    f'{base_url}/wiki/rest/api/content/12345',
    auth=auth,
    headers=headers,
    json={
        'type': 'page',
        'title': 'Updated Title',
        'body': {
            'storage': {
                'value': '<h1>Updated Content</h1>',
                'representation': 'storage'
            }
        },
        'version': {'number': page['version']['number'] + 1}
    }
)

# Search pages
results = requests.get(
    f'{base_url}/wiki/rest/api/content/search',
    auth=auth,
    headers=headers,
    params={'cql': 'space = GA AND text ~ "agent"'}
).json()
\`\`\`

## Webhooks

### Jira Webhook Handler
\`\`\`python
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhooks/jira', methods=['POST'])
def handle_jira_webhook():
    event = request.json
    event_type = event.get('webhookEvent')

    if event_type == 'jira:issue_created':
        issue = event['issue']
        handle_issue_created(issue)
    elif event_type == 'jira:issue_updated':
        issue = event['issue']
        changelog = event.get('changelog', {})
        handle_issue_updated(issue, changelog)
    elif event_type == 'sprint_started':
        sprint = event['sprint']
        handle_sprint_started(sprint)

    return {'status': 'ok'}

def handle_issue_created(issue):
    print(f"Issue created: {issue['key']}")

def handle_issue_updated(issue, changelog):
    for item in changelog.get('items', []):
        if item['field'] == 'status':
            print(f"Issue {issue['key']} status changed: {item['fromString']} -> {item['toString']}")
\`\`\`

### Register Webhook
\`\`\`python
# Register Jira webhook
webhook = requests.post(
    f'{base_url}/rest/webhooks/1.0/webhook',
    auth=auth,
    headers=headers,
    json={
        'name': 'Golden Armada Integration',
        'url': 'https://your-app.com/webhooks/jira',
        'events': [
            'jira:issue_created',
            'jira:issue_updated',
            'sprint_started',
            'sprint_closed'
        ],
        'filters': {
            'issue-related-events-section': 'project = GA'
        }
    }
)
\`\`\`

## Automation Recipes

### Sync GitHub PR to Jira
\`\`\`python
async def sync_pr_to_jira(pr_data: dict):
    # Extract Jira issue key from branch name (e.g., feature/GA-123-add-feature)
    branch = pr_data['head']['ref']
    match = re.search(r'(GA-\d+)', branch)
    if not match:
        return

    issue_key = match.group(1)

    # Add comment with PR link
    jira.add_comment(
        issue_key,
        f"PR opened: [{pr_data['title']}]({pr_data['html_url']})"
    )

    # Transition to "In Review" if PR is ready
    if not pr_data.get('draft'):
        jira.transition_issue(issue_key, 'In Review')
\`\`\`

### Auto-create Release Notes
\`\`\`python
def generate_release_notes(version: str, project_key: str = 'GA'):
    # Get all issues in the release
    jql = f'project = {project_key} AND fixVersion = "{version}" ORDER BY issuetype'
    issues = jira.jql(jql)['issues']

    # Group by type
    features = [i for i in issues if i['fields']['issuetype']['name'] == 'Story']
    bugs = [i for i in issues if i['fields']['issuetype']['name'] == 'Bug']

    # Generate markdown
    notes = f"# Release {version}\n\n"
    notes += "## Features\n"
    for issue in features:
        notes += f"- [{issue['key']}] {issue['fields']['summary']}\n"
    notes += "\n## Bug Fixes\n"
    for issue in bugs:
        notes += f"- [{issue['key']}] {issue['fields']['summary']}\n"

    # Create Confluence page
    confluence.create_page(
        space='GA',
        title=f'Release Notes - {version}',
        body=markdown_to_confluence(notes),
        parent_id=RELEASE_NOTES_PARENT_ID
    )
\`\`\`

## Golden Armada Commands

\`\`\`bash
# Sync with Atlassian
/atlassian-sync --jira --confluence

# Create Jira issue from template
/jira-create --type story --template agent-feature

# Update Confluence docs from code
/confluence-publish --from docs/ --space GA
\`\`\`
