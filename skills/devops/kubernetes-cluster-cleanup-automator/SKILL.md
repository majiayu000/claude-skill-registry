---
name: kubernetes-cluster-cleanup-automator
description: Identifies and cleans up outdated Kubernetes deployments based on namespace patterns and application version age. Discovers deployments, analyzes release dates from annotations, performs cleanup actions, and notifies stakeholders.
---
# Instructions

## Primary Objective
Automatically identify Kubernetes deployments in target namespaces that are running application versions older than a specified threshold, stop those deployments, and notify the responsible cluster administrator.

## Core Workflow

### 1. Discover Target Namespaces
- Use `k8s-kubectl_get` to list all namespaces
- Filter namespaces by name pattern (default: names starting with 'dev-')
- Store the filtered namespace list for subsequent operations

### 2. Discover Deployments in Target Namespaces
- For each target namespace, use `k8s-kubectl_get` to list all deployments
- Collect deployment metadata including name, namespace, and creation timestamp

### 3. Analyze Deployment Version Information
- For each discovered deployment, use `k8s-kubectl_describe` to get detailed information
- Extract the `app-version-release-date` annotation (expected format: ISO 8601 timestamp)
- Calculate the age of the version relative to current date
- Flag deployments where version age exceeds threshold (default: 30 days)

### 4. Identify Cluster Administrator Contact
- Search for contact information using multiple approaches:
  - Search emails for relevant keywords: "cluster management", "cluster admin", "kubernetes", "infrastructure"
  - Examine local filesystem for contact documents or configuration files
  - Check PDF documents for team contact information (look for "Cluster & Computing Resources" or similar sections)
- Extract email address of responsible person (typically found in team contact tables)

### 5. Perform Cleanup Actions
- For each outdated deployment, use `k8s-kubectl_scale` to set replicas to 0
- This effectively "stops" the deployment without deleting it
- Verify each scale operation completes successfully

### 6. Compile and Send Notification
- Sort outdated deployments chronologically from oldest to newest release date
- Calculate exact number of days since each version was released
- Format email according to specified template
- Use `emails-send_email` to notify the identified cluster administrator
- Include count of cleaned deployments and detailed list with namespace/deployment names and version ages

## Key Parameters & Configuration
- **Namespace Pattern**: Default 'dev-*' (configurable via user input)
- **Age Threshold**: Default 30 days (configurable via user input)
- **Date Annotation**: Looks for `app-version-release-date` annotation on deployments
- **Contact Search**: Multiple fallback strategies for finding cluster admin

## Error Handling & Edge Cases
- If no namespaces match the pattern, report this and exit gracefully
- If deployments lack the version annotation, skip them with a note
- If cluster admin contact cannot be found, pause and request guidance
- If scale operations fail, log the error but continue with others
- Always verify email was sent successfully

## Output Format
The final email must follow this exact format:
