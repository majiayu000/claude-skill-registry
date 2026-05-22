---
name: jenkins
description: "Manage Jenkins jobs, builds, and pipelines via the REST API."
metadata: {"thinkfleetbot":{"emoji":"🏗️","requires":{"bins":["curl","jq"],"env":["JENKINS_URL","JENKINS_USER","JENKINS_TOKEN"]}}}
---

# Jenkins

Manage Jenkins jobs, builds, and pipelines via the REST API.

## Environment Variables

- `JENKINS_URL` - Jenkins server URL (e.g. `https://jenkins.example.com`)
- `JENKINS_USER` - Jenkins username
- `JENKINS_TOKEN` - API token (generate from user profile > Configure > API Token)

## List jobs

```bash
curl -s -u "$JENKINS_USER:$JENKINS_TOKEN" \
  "$JENKINS_URL/api/json?tree=jobs[name,color,url]" | jq '.jobs[] | {name, color, url}'
```

## Get job info

```bash
curl -s -u "$JENKINS_USER:$JENKINS_TOKEN" \
  "$JENKINS_URL/job/my-pipeline/api/json?tree=name,color,lastBuild[number,result,timestamp]" | jq .
```

## Trigger build

```bash
curl -s -X POST -u "$JENKINS_USER:$JENKINS_TOKEN" \
  "$JENKINS_URL/job/my-pipeline/build"
echo "Build triggered"
```

## Trigger build with parameters

```bash
curl -s -X POST -u "$JENKINS_USER:$JENKINS_TOKEN" \
  "$JENKINS_URL/job/my-pipeline/buildWithParameters" \
  --data-urlencode "BRANCH=main" \
  --data-urlencode "ENV=staging"
echo "Parameterized build triggered"
```

## Get build status

```bash
curl -s -u "$JENKINS_USER:$JENKINS_TOKEN" \
  "$JENKINS_URL/job/my-pipeline/lastBuild/api/json?tree=number,result,duration,timestamp,building" | jq .
```

## Get build console output

```bash
curl -s -u "$JENKINS_USER:$JENKINS_TOKEN" \
  "$JENKINS_URL/job/my-pipeline/lastBuild/consoleText" | tail -50
```

## List build queue

```bash
curl -s -u "$JENKINS_USER:$JENKINS_TOKEN" \
  "$JENKINS_URL/queue/api/json?tree=items[task[name],why,inQueueSince]" | jq '.items[] | {job: .task.name, why, since: .inQueueSince}'
```

## Get pipeline stages (Blue Ocean)

```bash
curl -s -u "$JENKINS_USER:$JENKINS_TOKEN" \
  "$JENKINS_URL/blue/rest/organizations/jenkins/pipelines/my-pipeline/runs/1/nodes/" | jq '.[] | {displayName, result, durationInMillis}'
```

## Notes

- Jenkins uses crumb-based CSRF protection; if enabled, fetch crumb first.
- Use `buildWithParameters` for parameterized jobs, `build` for simple jobs.
- API token is preferred over password for authentication.
- Always confirm before triggering builds.
