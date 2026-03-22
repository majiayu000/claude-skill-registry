---
name: arch-cloud
cluster: se-architecture
description: "Cloud: serverless Lambda/CF Workers, edge, CDN, multi-region, HA patterns, IaC Terraform"
tags: ["cloud","serverless","edge","terraform","architecture"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "cloud serverless edge cdn multi-region terraform cost iac lambda"
---

# arch-cloud

## Purpose
This skill helps design and implement cloud architectures focused on serverless technologies (e.g., AWS Lambda, Cloudflare Workers), edge computing, CDNs, multi-region setups for high availability (HA), and Infrastructure as Code (IaC) using Terraform. It ensures scalable, cost-effective solutions by guiding precise configuration and deployment.

## When to Use
Use this skill for applications needing low-latency edge delivery, serverless backends to reduce costs, multi-region redundancy for HA, or IaC automation. Examples include building global APIs, migrating to serverless, or optimizing CDN for media delivery. Avoid for simple monolithic apps or on-prem setups.

## Key Capabilities
- Deploy serverless functions: Create AWS Lambda or Cloudflare Workers for event-driven processing.
- Edge and CDN integration: Configure Cloudflare for edge caching and routing to reduce latency.
- Multi-region HA patterns: Set up auto-failover with AWS Route 53 or Cloudflare load balancers.
- IaC with Terraform: Define and provision cloud resources declaratively for reproducibility.
- Cost optimization: Analyze patterns like using Lambda's reserved concurrency or Terraform's cost modules.

## Usage Patterns
1. **Serverless API Deployment**: Use Terraform to define a Lambda function and API Gateway, then deploy for quick scaling. Ensure multi-region setup by adding Route 53 for failover.
2. **Edge-Computing CDN Setup**: Integrate Cloudflare Workers with a CDN to cache assets and handle requests at the edge, reducing origin server load. Combine with Terraform for automated provisioning across regions.

## Common Commands/API
- **Terraform Commands**: Initialize with `terraform init`; plan changes with `terraform plan -out=plan.tfplan`; apply with `terraform apply plan.tfplan`. Use `-var="region=us-east-1"` for region-specific vars.
- **AWS CLI for Lambda**: Create a function using `aws lambda create-function --function-name myLambda --zip-file fileb://function.zip --handler index.handler --runtime nodejs14.x --role arn:aws:iam::123456789012:role/lambdaRole`. Invoke with `aws lambda invoke --function-name myLambda out.txt`.
- **Cloudflare API Endpoints**: Authenticate with `$CLOUDFLARE_API_KEY` env var. Create a Worker script via POST to `https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts` with JSON body: `{"id": "myWorker", "content": "addEventListener('fetch', event => event.respondWith(new Response('Hello')));"}`.
- **Config Formats**: Use HCL in Terraform files, e.g., `resource "aws_lambda_function" "example" { function_name = "myFunction" runtime = "nodejs14.x" handler = "index.handler" filename = "function.zip" }`. For API keys, set in env vars like `export AWS_ACCESS_KEY_ID=$AWS_API_KEY`.

## Integration Notes
Integrate Terraform with CI/CD by running `terraform plan` in GitHub Actions via a workflow step: `run: terraform plan -out=plan.out`. For serverless, link Lambda to S3 triggers using Terraform: `resource "aws_lambda_permission" "allow_s3" { action = "lambda:InvokeFunction" function_name = aws_lambda_function.example.function_name principal = "s3.amazonaws.com" source_arn = aws_s3_bucket.example.arn }`. Use `$TERRAFORM_STATE_BUCKET` for remote state storage. For edge services, route traffic from Cloudflare to AWS via API Gateway by configuring Cloudflare's origin settings with the Gateway endpoint.

## Error Handling
Handle Terraform errors by checking `terraform plan` output for diffs and running `terraform apply --auto-approve` only after review; common issues include dependency cycles—fix by ordering resources in .tf files. For Lambda, catch invocation errors with `aws lambda invoke --function-name myLambda out.txt` and parse logs via CloudWatch: use `aws logs get-log-events --log-group /aws/lambda/myLambda --log-stream latest`. If Cloudflare API returns 401, verify `$CLOUDFLARE_API_KEY` and retry with exponential backoff. In code, wrap API calls in try-catch: `try { const response = await fetch('https://api.cloudflare.com/...'); } catch (error) { console.error(error.message); }`. Always validate region configs to avoid "region not supported" errors.

## Concrete Usage Examples
1. **Deploy a Multi-Region Serverless Function**: First, set env vars: `export AWS_REGION=us-east-1` and `export AWS_ACCESS_KEY_ID=$AWS_API_KEY`. Create a Terraform file: `resource "aws_lambda_function" "globalFn" { ... } resource "aws_route53_record" "failover" { zone_id = "Z1234567890" name = "api.example.com" type = "A" failover_routing_policy { ... } }`. Run `terraform init && terraform apply` to deploy Lambda in us-east-1 and set up Route 53 for HA.
2. **Set Up Edge CDN with Workers**: Authenticate Cloudflare with `export CLOUDFLARE_API_KEY=your_key`. Use Terraform to provision: `resource "cloudflare_worker_script" "edgeScript" { name = "edgeWorker" content = "addEventListener('fetch', event => { ... }); } resource "cloudflare_zone" "example" { zone = "example.com" }`. Deploy with `terraform apply`, then test by curling the Worker endpoint.

## Graph Relationships
- Related to: se-architecture cluster (e.g., 'design-patterns' for architectural blueprints, 'deployment-strategies' for rollout techniques).
- Connected via tags: 'cloud' links to 'aws-services' skill; 'serverless' to 'lambda-optimizations'; 'terraform' to 'iac-best-practices'.
