---
name: pulumi-code-review
description: Master Pulumi Infrastructure as Code review patterns including naming conventions, secrets management, resource protection, component design, and configuration. Use PROACTIVELY when reviewing Pulumi PRs.
---

# Pulumi Code Review

Comprehensive code review checklist and patterns for Pulumi Infrastructure as Code, focusing on resource management, security, and IaC best practices.

## When to Use This Skill

- Reviewing Pulumi pull requests
- Establishing IaC code review standards
- Training reviewers on Pulumi-specific issues
- Catching security and configuration issues
- Ensuring proper infrastructure patterns

## Quick Checklist

```markdown
## Pulumi Review Checklist

- [ ] Consistent naming convention across all resources
- [ ] Tags applied to all resources
- [ ] Secrets use pulumi.Config.requireSecret()
- [ ] Component Resources for reusable patterns
- [ ] No hardcoded values (use Config)
- [ ] Critical resources have Protect: true
- [ ] Stack outputs defined for needed values
- [ ] Explicit dependencies where auto-inference fails
```

## Review Severity Labels

```
🔴 [blocking]  - Must fix before merge (bugs, security, breaking)
🟡 [important] - Should fix, but discuss if you disagree
🟢 [nit]       - Nice to have, not blocking
💡 [suggestion]- Alternative approach to consider
```

---

## Naming Conventions

### Inconsistent Naming

```python
# ❌ Inconsistent naming - hard to identify resources
vpc = aws.ec2.Vpc("my-vpc", ...)
subnet = aws.ec2.Subnet("subnet1", ...)
instance = aws.ec2.Instance("WebServer", ...)
db = aws.rds.Instance("production-database", ...)

# ✅ Consistent naming convention: {project}-{env}-{type}-{name}
naming = NamingConvention.from_context()

vpc = aws.ec2.Vpc(naming.resource("vpc", "main"), ...)
subnet = aws.ec2.Subnet(naming.resource("sn", "public-01"), ...)
instance = aws.ec2.Instance(naming.resource("ec2", "web-01"), ...)
db = aws.rds.Instance(naming.resource("rds", "primary"), ...)
```

```go
// Go example
naming := NewNamingConvention(ctx)

vpc, _ := ec2.NewVpc(ctx, naming.Resource("vpc", "main"), ...)
subnet, _ := ec2.NewSubnet(ctx, naming.Resource("sn", "public-01"), ...)
instance, _ := ec2.NewInstance(ctx, naming.Resource("ec2", "web-01"), ...)
```

### Naming Convention Reference

| Resource Type  | Abbreviation | Example Name              |
| -------------- | ------------ | ------------------------- |
| VPC            | `vpc`        | `myapp-prod-vpc-main`     |
| Subnet         | `sn`         | `myapp-prod-sn-public-01` |
| Security Group | `sg`         | `myapp-prod-sg-web`       |
| EC2 Instance   | `ec2`        | `myapp-prod-ec2-app-01`   |
| RDS            | `rds`        | `myapp-prod-rds-primary`  |
| S3 Bucket      | `s3`         | `myapp-prod-usw2-s3-data` |
| Lambda         | `fn`         | `myapp-prod-fn-processor` |
| IAM Role       | `role`       | `myapp-prod-role-lambda`  |

---

## Secrets Management

### Hardcoded Secrets

```python
# ❌ Hardcoded secrets - stored in plain text in state!
db_password = "super_secret_password"

db = aws.rds.Instance(
    "database",
    password=db_password,  # EXPOSED in state file!
)

# ✅ Use secret config
config = pulumi.Config()
db_password = config.require_secret("dbPassword")

db = aws.rds.Instance(
    "database",
    password=db_password,  # Encrypted in state
)
```

```go
// Go example
cfg := config.New(ctx, "")
dbPassword := cfg.RequireSecret("dbPassword")

db, err := rds.NewInstance(ctx, "database", &rds.InstanceArgs{
    Password: dbPassword,
})
```

### Secrets in Outputs

```python
# ❌ Secret exposed in plain text output
pulumi.export("db_password", db_password)  # EXPOSED!

# ✅ Export as secret
pulumi.export("db_password", pulumi.Output.secret(db_password))
```

```go
// Go example
ctx.Export("dbPassword", pulumi.ToSecret(dbPassword))
```

### Logging Secrets

```python
# ❌ Logging secrets
db_password.apply(lambda pwd: print(f"Password: {pwd}"))  # EXPOSED in logs!

# ✅ Never log secrets
db_password.apply(lambda pwd: print("Password configured successfully"))
```

---

## Resource Protection

### Critical Resources Unprotected

```python
# ❌ Production database unprotected - can be accidentally deleted!
db = aws.rds.Instance(
    "production-db",
    instance_class="db.r5.large",
    allocated_storage=100,
    # No protection!
)

# ✅ Protect critical resources
db = aws.rds.Instance(
    "production-db",
    instance_class="db.r5.large",
    allocated_storage=100,
    opts=pulumi.ResourceOptions(protect=True),
)
```

```go
// Go example
db, err := rds.NewInstance(ctx, "production-db", &rds.InstanceArgs{
    InstanceClass:    pulumi.String("db.r5.large"),
    AllocatedStorage: pulumi.Int(100),
}, pulumi.Protect(true))
```

### Resources to Protect

Always protect:

- Production databases
- S3 buckets with important data
- KMS keys
- VPCs and core networking
- DNS zones
- Secrets Manager secrets

```python
# ✅ Protect all critical resources
for critical_resource in [production_db, data_bucket, encryption_key]:
    pulumi.ResourceOptions(protect=True)
```

---

## Component Resources

### Duplicate Infrastructure Code

```python
# ❌ Duplicate infrastructure code - hard to maintain
def create_web_stack_prod():
    vpc = aws.ec2.Vpc("prod-vpc", ...)
    subnet = aws.ec2.Subnet("prod-subnet", ...)
    alb = aws.lb.LoadBalancer("prod-alb", ...)
    # ... 50 more resources, copy-pasted

def create_web_stack_staging():
    vpc = aws.ec2.Vpc("staging-vpc", ...)  # Copy-pasted!
    subnet = aws.ec2.Subnet("staging-subnet", ...)
    alb = aws.lb.LoadBalancer("staging-alb", ...)
    # ... 50 more resources

# ✅ Reusable Component Resource
class WebStack(pulumi.ComponentResource):
    def __init__(self, name: str, args: WebStackArgs,
                 opts: pulumi.ResourceOptions = None):
        super().__init__("custom:app:WebStack", name, None, opts)

        self.vpc = aws.ec2.Vpc(
            f"{name}-vpc",
            cidr_block=args.vpc_cidr,
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.subnet = aws.ec2.Subnet(
            f"{name}-subnet",
            vpc_id=self.vpc.id,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Register outputs
        self.register_outputs({
            "vpc_id": self.vpc.id,
            "subnet_id": self.subnet.id,
        })

# Usage - clean and reusable
prod_stack = WebStack("prod", WebStackArgs(environment="prod", vpc_cidr="10.0.0.0/16"))
staging_stack = WebStack("staging", WebStackArgs(environment="staging", vpc_cidr="10.1.0.0/16"))
```

```go
// Go Component Resource example
type WebStack struct {
    pulumi.ResourceState

    VpcId    pulumi.StringOutput `pulumi:"vpcId"`
    SubnetId pulumi.StringOutput `pulumi:"subnetId"`
}

func NewWebStack(ctx *pulumi.Context, name string, args *WebStackArgs,
    opts ...pulumi.ResourceOption) (*WebStack, error) {

    component := &WebStack{}
    err := ctx.RegisterComponentResource("custom:app:WebStack", name, component, opts...)
    if err != nil {
        return nil, err
    }

    vpc, err := ec2.NewVpc(ctx, name+"-vpc", &ec2.VpcArgs{
        CidrBlock: pulumi.String(args.VpcCidr),
    }, pulumi.Parent(component))

    // ... more resources

    component.VpcId = vpc.ID()
    return component, nil
}
```

---

## Configuration

### Hardcoded Values

```python
# ❌ Hardcoded values - same for all environments
instance = aws.ec2.Instance(
    "web",
    instance_type="t3.large",  # Same for dev and prod!
    ami="ami-12345678",        # Hardcoded AMI!
)

# ✅ Environment-specific config
config = pulumi.Config()

instance = aws.ec2.Instance(
    "web",
    instance_type=config.get("instanceType") or "t3.medium",
    ami=config.require("ami"),
)
```

Stack config files:

```yaml
# Pulumi.dev.yaml
config:
  myapp:instanceType: t3.small
  myapp:ami: ami-dev123

# Pulumi.prod.yaml
config:
  myapp:instanceType: t3.large
  myapp:ami: ami-prod456
```

### Missing Default Values

```python
# ❌ No defaults - config required even for optional values
instance_type = config.require("instanceType")  # Fails if not set

# ✅ Provide sensible defaults
instance_type = config.get("instanceType") or "t3.medium"
enable_monitoring = config.get_bool("enableMonitoring") or True
replica_count = config.get_int("replicaCount") or 2
```

---

## Dependencies

### Missing Explicit Dependencies

```python
# ❌ Implicit dependencies may not work for all cases
role = aws.iam.Role("lambda-role", ...)

policy = aws.iam.RolePolicy("lambda-policy",
    role=role.name,
    policy=policy_document,
)

function = aws.lambda_.Function("my-function",
    role=role.arn,
    # Policy might not be attached yet!
)

# ✅ Explicit dependencies when needed
function = aws.lambda_.Function("my-function",
    role=role.arn,
    opts=pulumi.ResourceOptions(depends_on=[policy]),
)
```

### Circular Dependencies

```python
# ❌ Circular dependency - will fail
security_group_a = aws.ec2.SecurityGroup("sg-a",
    ingress=[{
        "security_groups": [security_group_b.id],  # B doesn't exist yet!
    }],
)

security_group_b = aws.ec2.SecurityGroup("sg-b",
    ingress=[{
        "security_groups": [security_group_a.id],
    }],
)

# ✅ Use separate security group rules
security_group_a = aws.ec2.SecurityGroup("sg-a")
security_group_b = aws.ec2.SecurityGroup("sg-b")

rule_a_to_b = aws.ec2.SecurityGroupRule("a-to-b",
    type="ingress",
    security_group_id=security_group_a.id,
    source_security_group_id=security_group_b.id,
    protocol="tcp",
    from_port=443,
    to_port=443,
)
```

---

## Tags and Organization

### Missing Tags

```python
# ❌ No tags - hard to manage and track costs
instance = aws.ec2.Instance("web",
    instance_type="t3.medium",
    # No tags!
)

# ✅ Consistent tags on all resources
def get_tags(name: str, additional: dict = None) -> dict:
    tags = {
        "Name": name,
        "Environment": pulumi.get_stack(),
        "Project": pulumi.get_project(),
        "ManagedBy": "pulumi",
    }
    if additional:
        tags.update(additional)
    return tags

instance = aws.ec2.Instance("web",
    instance_type="t3.medium",
    tags=get_tags("web-server", {"Role": "frontend"}),
)
```

### AWS Provider Default Tags (Best Practice)

```python
# ✅ Set default tags at provider level
aws_provider = aws.Provider("aws",
    region="us-west-2",
    default_tags=aws.ProviderDefaultTagsArgs(
        tags={
            "Environment": pulumi.get_stack(),
            "Project": pulumi.get_project(),
            "ManagedBy": "pulumi",
        },
    ),
)

# All resources using this provider get these tags automatically
instance = aws.ec2.Instance("web",
    instance_type="t3.medium",
    opts=pulumi.ResourceOptions(provider=aws_provider),
)
```

---

## Stack Outputs

### Missing Important Outputs

```python
# ❌ No outputs - hard to use stack values elsewhere
vpc = aws.ec2.Vpc("main", cidr_block="10.0.0.0/16")
alb = aws.lb.LoadBalancer("web", ...)

# Stack has no accessible outputs!

# ✅ Export important values
vpc = aws.ec2.Vpc("main", cidr_block="10.0.0.0/16")
alb = aws.lb.LoadBalancer("web", ...)

pulumi.export("vpc_id", vpc.id)
pulumi.export("alb_dns_name", alb.dns_name)
pulumi.export("alb_zone_id", alb.zone_id)
```

### Sensitive Outputs

```python
# ❌ Sensitive data in plain output
pulumi.export("db_connection_string", connection_string)

# ✅ Mark sensitive outputs as secrets
pulumi.export("db_connection_string", pulumi.Output.secret(connection_string))
```

---

## Resource Refactoring

### Renaming Without Aliases

```python
# ❌ Renaming resource - causes delete and recreate!
# Before:
instance = aws.ec2.Instance("old-name", ...)
# After:
instance = aws.ec2.Instance("new-name", ...)  # Deletes old, creates new!

# ✅ Use aliases to preserve resource
instance = aws.ec2.Instance("new-name",
    instance_type="t3.medium",
    opts=pulumi.ResourceOptions(
        aliases=[pulumi.Alias(name="old-name")],
    ),
)
```

```go
// Go example
instance, err := ec2.NewInstance(ctx, "new-name", &ec2.InstanceArgs{
    InstanceType: pulumi.String("t3.medium"),
}, pulumi.Aliases([]pulumi.Alias{
    {Name: pulumi.String("old-name")},
}))
```

---

## Testing

### No Infrastructure Tests

```python
# ❌ No tests for infrastructure

# ✅ Add unit tests with mocks
import unittest
import pulumi

class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [f"{args.name}_id", args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}

pulumi.runtime.set_mocks(MyMocks())

class TestInfrastructure(unittest.TestCase):
    @pulumi.runtime.test
    def test_vpc_has_correct_cidr(self):
        import infra  # Your Pulumi code

        def check_cidr(cidr):
            self.assertEqual(cidr, "10.0.0.0/16")

        infra.vpc.cidr_block.apply(check_cidr)
```

---

## Common Pitfalls

| Pitfall             | Problem                | Solution                 |
| ------------------- | ---------------------- | ------------------------ |
| Hardcoded secrets   | Exposed in state       | Use `require_secret()`   |
| No protection       | Accidental deletion    | Use `protect=True`       |
| Inconsistent naming | Hard to identify       | Naming convention module |
| Duplicate code      | Hard to maintain       | Component Resources      |
| Hardcoded values    | Same for all envs      | Use Config               |
| Missing outputs     | Can't reference values | Export important values  |
| Missing tags        | Cost tracking issues   | Tag all resources        |

## Best Practices Summary

1. **Consistent Naming** - Use naming convention module
2. **Encrypt Secrets** - `require_secret()` for sensitive values
3. **Protect Critical** - `protect=True` for production resources
4. **Component Resources** - For reusable infrastructure patterns
5. **Use Config** - Never hardcode environment-specific values
6. **Tag Everything** - For cost tracking and management
7. **Export Outputs** - For cross-stack references
8. **Test Infrastructure** - Unit tests with mocks


## Parent Hub
- [_devops-cloud-mastery](../_devops-cloud-mastery/SKILL.md)
