---
name: multi-namespace-deployment-analyzer
description: When the user needs to analyze deployments across multiple Kubernetes namespaces with filtering criteria. This skill discovers namespaces matching patterns, retrieves deployment information from each namespace, extracts metadata and annotations, and performs comparative analysis across namespaces. It handles batch operations and consolidates results from multiple namespace queries. Triggers include 'namespaces starting with', 'across namespaces', 'multiple namespaces', 'deployment analysis', 'namespace pattern', 'batch deployment query', 'cross-namespace comparison'.
---
# Instructions

## Overview
This skill analyzes Kubernetes deployments across multiple namespaces based on filtering criteria. It discovers namespaces matching patterns, retrieves deployment information, extracts metadata/annotations, performs comparative analysis, and can execute batch operations.

## Core Workflow

### 1. Discover Target Namespaces
- Use `k8s-kubectl_get` to list all namespaces
- Filter namespaces based on user criteria (e.g., names starting with 'dev-')
- Store the filtered namespace list for subsequent operations

### 2. Retrieve Deployments from Each Namespace
- For each target namespace, use `k8s-kubectl_get` to list deployments
- Collect deployment metadata: name, namespace, status, creation timestamp
- Handle empty namespaces gracefully

### 3. Extract Detailed Deployment Information
- For each deployment, use `k8s-kubectl_describe` to get detailed information
- Focus on extracting annotations, particularly `app-version-release-date` or similar version metadata
- Note container images, resource limits, and other relevant configuration

### 4. Perform Analysis
- Calculate age of deployments based on release date annotations
- Apply filtering criteria (e.g., "more than 30 days ago")
- Sort results chronologically (oldest to newest)
- Count affected deployments for reporting

### 5. Execute Batch Operations (If Required)
- Based on analysis results, perform actions like scaling deployments to 0 replicas
- Use `k8s-kubectl_scale` for each outdated deployment
- Verify operations completed successfully

### 6. Identify Responsible Personnel
- Search for contact information using multiple approaches:
  - Search emails for relevant keywords ("cluster management", "cluster admin", "kubernetes", "infrastructure")
  - Examine available files and directories for contact information
  - Check PDF documents for organizational charts or responsibility matrices
  - Look for configuration files that might contain contact details

### 7. Generate and Send Report
- Compile results in the specified format
- Include: number of affected deployments, sorted list with namespace/deployment names and days since release
- Use `emails-send_email` to notify the identified responsible party
- Use professional email format with clear subject and body

## Key Considerations

### Error Handling
- Handle cases where no namespaces match the pattern
- Handle deployments without version annotations gracefully
- Provide clear feedback when contact information cannot be found
- Verify email sending was successful

### Performance Optimization
- Batch namespace queries when possible
- Cache results to avoid redundant API calls
- Process deployments in parallel where appropriate

### Output Formatting
- Always sort deployments chronologically from oldest to newest
- Include both namespace and deployment name in listings
- Calculate days accurately based on current date
- Use consistent formatting throughout the report

## Common Patterns
- Namespace filtering: typically prefixes like 'dev-', 'staging-', 'prod-'
- Age filtering: 30, 60, 90 days common thresholds
- Actions: scale to 0, delete, annotate, or just report
- Contacts: cluster admins, team leads, infrastructure managers
