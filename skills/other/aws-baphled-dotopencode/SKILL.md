---
name: aws
description: AWS cloud infrastructure, managed services, security best practices, and Go SDK integration
category: DevOps Operations
---

# Skill: aws

## What I do

I provide expertise in AWS cloud services. I design and implement scalable, reliable, and secure cloud-native architectures using managed services, Infrastructure as Code (Terraform), and Go SDK integration.

## When to use me

- Deploying applications to scalable cloud infrastructure
- Implementing serverless architectures (Lambda, Fargate)
- Managing databases with automated backups (RDS, DynamoDB)
- Securing cloud environments using IAM least privilege
- Optimising cloud costs through auto-scaling and right-sizing
- Integrating AWS services with Go applications

## Core principles

1. **Managed Services First** — Prefer AWS managed services (RDS, ECS) over self-managed EC2
2. **Multi-AZ Availability** — Deploy across multiple Availability Zones for high availability
3. **IAM Least Privilege** — Grant minimum required permissions; use service roles
4. **Auto-Scaling** — Design for horizontal scalability based on demand
5. **Security by Design** — Enable encryption at rest and in transit (KMS, TLS)
6. **Infrastructure as Code** — Manage all resources through Terraform or CloudFormation

## Patterns & examples

**Infrastructure as Code (Terraform - RDS):**
```hcl
resource "aws_db_instance" "postgres" {
  engine         = "postgres"
  instance_class = "db.t3.medium"
  multi_az       = true
  allocated_storage = 100
  storage_encrypted = true
  db_subnet_group_name = aws_db_subnet_group.main.name
  password = data.aws_secretsmanager_secret_version.db_pass.secret_string
}
```

**Go SDK - S3 Upload (v2):**
```go
func (s *S3Client) Upload(ctx context.Context, key string, body io.Reader) error {
    _, err := s.client.PutObject(ctx, &s3.PutObjectInput{
        Bucket:               aws.String(s.bucket),
        Key:                  aws.String(key),
        Body:                 body,
        ServerSideEncryption: types.ServerSideEncryptionAes256,
    })
    return err
}
```

**Lambda Handler (Go):**
```go
func handler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
    return events.APIGatewayProxyResponse{
        StatusCode: 200,
        Body:       `{"status":"ok"}`,
    }, nil
}
func main() { lambda.Start(handler) }
```

## Anti-patterns to avoid

- ❌ **Public S3 Buckets** — Use CloudFront with OAC for static content serving
- ❌ **Hardcoded Credentials** — Use IAM Roles for services and Secrets Manager for keys
- ❌ **Single AZ Production** — Creates single point of failure; always use Multi-AZ
- ❌ **Root Account Usage** — Never use root for daily ops; create granular IAM users
- ❌ **No Cost Monitoring** — Enable budgets and cost allocation tags to avoid bill shock


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/DevOps-Operations/AWS.md`

## Related skills

- `infrastructure-as-code` - Terraform and CloudFormation patterns
- `docker` - Containerisation for ECS/Fargate
- `devops` - CI/CD and operational excellence
- `security` - IAM and encryption standards
- `go-expert` - Advanced SDK integration patterns
