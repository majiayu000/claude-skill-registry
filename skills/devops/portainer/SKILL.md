---
name: portainer
description: Manage Portainer deployments - create stacks from Git repos, check deployment status, redeploy, view logs. Use when user asks about deploying to Portainer, checking stack status, or managing Docker deployments.
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion
---

# Portainer Deployment Management

Manage Docker stack deployments via Portainer API.

## Configuration

Before using, ensure these are available:
- **PORTAINER_URL**: Portainer instance URL (e.g., `https://portainer.example.com`)
- **PORTAINER_TOKEN**: API token from Portainer (User Settings > Access Tokens)

Store sensitive config in environment or prompt user when needed.

## Available Operations

### 1. List All Stacks

```bash
curl -s -X GET "$PORTAINER_URL/api/stacks" \
  -H "X-API-Key: $PORTAINER_TOKEN" | jq '.[] | {Id, Name, Status, CreationDate}'
```

Status codes: `1` = active, `2` = inactive

### 2. Check Stack Status

```bash
# Get specific stack by name
STACK_NAME="my-stack"
curl -s -X GET "$PORTAINER_URL/api/stacks" \
  -H "X-API-Key: $PORTAINER_TOKEN" | jq ".[] | select(.Name==\"$STACK_NAME\")"
```

### 3. Get Stack Containers/Services

```bash
STACK_ID=24
ENDPOINT_ID=1
curl -s -X GET "$PORTAINER_URL/api/endpoints/$ENDPOINT_ID/docker/containers/json?all=true" \
  -H "X-API-Key: $PORTAINER_TOKEN" | jq '.[] | select(.Labels["com.docker.compose.project"]=="STACK_NAME") | {Id: .Id[:12], Name: .Names[0], State, Status}'
```

### 4. Create Stack from Git Repository

Required parameters:
- `name`: Stack name (lowercase, hyphens allowed)
- `repositoryURL`: Git repo URL
- `repositoryReferenceName`: Branch (e.g., `refs/heads/main`)
- `composeFile`: Path to compose file in repo
- `env`: Array of environment variables

```bash
ENDPOINT_ID=$(curl -s "$PORTAINER_URL/api/endpoints" -H "X-API-Key: $PORTAINER_TOKEN" | jq '.[0].Id')

curl -X POST "$PORTAINER_URL/api/stacks/create/standalone/repository?endpointId=$ENDPOINT_ID" \
  -H "X-API-Key: $PORTAINER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-stack",
    "repositoryURL": "https://github.com/user/repo.git",
    "repositoryReferenceName": "refs/heads/main",
    "composeFile": "docker-compose.yml",
    "repositoryAuthentication": true,
    "repositoryUsername": "USERNAME",
    "repositoryPassword": "GITHUB_TOKEN",
    "env": [
      {"name": "VAR_NAME", "value": "value"}
    ],
    "autoUpdate": {
      "interval": "5m"
    }
  }'
```

For private repos, set `repositoryAuthentication: true` and provide credentials.
Get GitHub token via: `gh auth token`

### 5. Redeploy/Update Stack

```bash
STACK_ID=24
ENDPOINT_ID=1
curl -X PUT "$PORTAINER_URL/api/stacks/$STACK_ID/git/redeploy?endpointId=$ENDPOINT_ID" \
  -H "X-API-Key: $PORTAINER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pullImage": true, "prune": false}'
```

### 6. Delete Stack

```bash
STACK_ID=24
ENDPOINT_ID=1
curl -X DELETE "$PORTAINER_URL/api/stacks/$STACK_ID?endpointId=$ENDPOINT_ID" \
  -H "X-API-Key: $PORTAINER_TOKEN"
```

### 7. View Container Logs

```bash
CONTAINER_ID="abc123"
ENDPOINT_ID=1
curl -s "$PORTAINER_URL/api/endpoints/$ENDPOINT_ID/docker/containers/$CONTAINER_ID/logs?stdout=true&stderr=true&tail=100" \
  -H "X-API-Key: $PORTAINER_TOKEN"
```

## Workflow Instructions

### When user asks to deploy to Portainer:

1. **Gather requirements**:
   - Portainer URL and API token
   - Git repository URL
   - Compose file path
   - Environment variables needed
   - Target branch

2. **Check if repo is private**:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" https://github.com/USER/REPO
   ```
   If 404, need GitHub credentials.

3. **Get endpoint ID**:
   ```bash
   curl -s "$PORTAINER_URL/api/endpoints" -H "X-API-Key: $TOKEN" | jq '.[0].Id'
   ```

4. **Check for existing stack**:
   ```bash
   curl -s "$PORTAINER_URL/api/stacks" -H "X-API-Key: $TOKEN" | jq -r '.[] | select(.Name=="STACK_NAME") | .Id'
   ```

5. **Create or update** based on whether stack exists.

6. **Verify deployment** by checking stack status after creation.

### When user asks about deployment status:

1. List all stacks or get specific stack by name
2. Get container status for the stack
3. Check container health/logs if issues detected
4. Report status in a clear table format

### Status Response Format

Present status in a clear format:

```
| Stack | Status | Containers | Last Updated |
|-------|--------|------------|--------------|
| my-app | Active | 3/3 running | 2 hours ago |
```

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `authentication failed` | Private repo without credentials | Add `repositoryAuthentication`, username, password |
| `Invalid request payload` | Malformed JSON | Check JSON syntax, especially nested objects |
| `stack already exists` | Duplicate name | Use update/redeploy instead of create |
| `endpoint not found` | Wrong endpoint ID | Query `/api/endpoints` first |

## Security Notes

- Never commit API tokens or passwords to version control
- Use `gh auth token` for GitHub credentials (auto-refreshes)
- Portainer tokens should be stored securely or prompted at runtime
- Consider using environment variables for sensitive values

## Example: Full Deployment Script

See `scripts/deploy-portainer.sh` in this repository for a complete example.
