---
name: pulumi-best-practice
description: Master comprehensive Pulumi Infrastructure as Code best practices covering project structure, stack management, component resources, naming conventions, secrets, multi-cloud patterns, testing, and CI/CD integration using Go and Python. Use PROACTIVELY for Pulumi development, IaC review, or establishing infrastructure standards.
---

# Pulumi Best Practices

Master comprehensive Pulumi Infrastructure as Code (IaC) practices for building maintainable, secure, and scalable cloud infrastructure using Go and Python (2024-2026).

## When to Use This Skill

- Designing new Pulumi projects and stacks
- Reviewing infrastructure code for quality
- Establishing team IaC standards
- Managing multi-environment deployments
- Implementing multi-cloud infrastructure
- Writing testable infrastructure code
- Setting up CI/CD for infrastructure
- Migrating from Terraform or CloudFormation

## Core Concepts

### 1. Project Structure

**Go Project Structure:**

```
infrastructure/
├── Pulumi.yaml                 # Project definition
├── Pulumi.dev.yaml            # Dev stack configuration
├── Pulumi.staging.yaml        # Staging stack configuration
├── Pulumi.prod.yaml           # Production stack configuration
├── main.go                    # Main entry point
├── config/                    # Configuration loading
│   └── config.go
├── components/                # Reusable component resources
│   ├── vpc.go
│   ├── cluster.go
│   └── database.go
├── naming/                    # Naming conventions
│   └── naming.go
├── stacks/                    # Stack-specific configurations
│   ├── networking.go
│   ├── compute.go
│   └── storage.go
├── tests/                     # Infrastructure tests
│   └── components_test.go
├── go.mod
├── go.sum
└── README.md
```

**Python Project Structure:**

```
infrastructure/
├── Pulumi.yaml                 # Project definition
├── Pulumi.dev.yaml            # Dev stack configuration
├── Pulumi.staging.yaml        # Staging stack configuration
├── Pulumi.prod.yaml           # Production stack configuration
├── __main__.py                # Main entry point
├── config.py                  # Configuration loading
├── components/                # Reusable component resources
│   ├── __init__.py
│   ├── vpc.py
│   ├── cluster.py
│   └── database.py
├── naming.py                  # Naming conventions
├── stacks/                    # Stack-specific configurations
│   ├── __init__.py
│   ├── networking.py
│   ├── compute.py
│   └── storage.py
├── tests/                     # Infrastructure tests
│   └── test_components.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

**Pulumi.yaml (Project Definition):**

```yaml
name: my-infrastructure
runtime:
  name: go # or python
description: Production infrastructure for my-app
config:
  pulumi:tags:
    value:
      pulumi:template: ""
```

### 2. Resource Naming Conventions

Establish consistent naming across all resources.

**Go Naming Module:**

```go
// naming/naming.go
package naming

import (
    "fmt"
    "strings"

    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

// Convention defines the naming convention for resources
type Convention struct {
    Project     string
    Environment string
    Region      string
}

// NewConvention creates a new naming convention from Pulumi context
func NewConvention(ctx *pulumi.Context) *Convention {
    return &Convention{
        Project:     ctx.Project(),
        Environment: ctx.Stack(),
        Region:      "usw2", // Abbreviate regions
    }
}

// Resource generates a resource name following the pattern:
// {project}-{environment}-{resource_type}-{name}
// Example: myapp-prod-vpc-main
func (c *Convention) Resource(resourceType, name string) string {
    return fmt.Sprintf("%s-%s-%s-%s",
        c.sanitize(c.Project),
        c.sanitize(c.Environment),
        c.sanitize(resourceType),
        c.sanitize(name),
    )
}

// ResourceWithRegion includes region for multi-region resources:
// {project}-{environment}-{region}-{resource_type}-{name}
// Example: myapp-prod-usw2-s3-data
func (c *Convention) ResourceWithRegion(resourceType, name string) string {
    return fmt.Sprintf("%s-%s-%s-%s-%s",
        c.sanitize(c.Project),
        c.sanitize(c.Environment),
        c.sanitize(c.Region),
        c.sanitize(resourceType),
        c.sanitize(name),
    )
}

// Short generates a short name for resources with length limits:
// {project_abbr}{env_abbr}{type_abbr}{name}
// Example: maprdbs01 (my-app + prod + rds + 01)
func (c *Convention) Short(resourceType, name string, maxLen int) string {
    abbr := fmt.Sprintf("%s%s%s%s",
        c.abbreviate(c.Project, 2),
        c.abbreviate(c.Environment, 2),
        c.abbreviate(resourceType, 3),
        name,
    )
    if len(abbr) > maxLen {
        return abbr[:maxLen]
    }
    return abbr
}

// Tags returns standard tags for all resources
func (c *Convention) Tags(additionalTags map[string]string) pulumi.StringMap {
    tags := pulumi.StringMap{
        "Project":     pulumi.String(c.Project),
        "Environment": pulumi.String(c.Environment),
        "ManagedBy":   pulumi.String("pulumi"),
    }
    for k, v := range additionalTags {
        tags[k] = pulumi.String(v)
    }
    return tags
}

func (c *Convention) sanitize(s string) string {
    return strings.ToLower(strings.ReplaceAll(s, "_", "-"))
}

func (c *Convention) abbreviate(s string, length int) string {
    s = strings.ToLower(s)
    if len(s) <= length {
        return s
    }
    return s[:length]
}

// Usage example:
// naming := naming.NewConvention(ctx)
// vpcName := naming.Resource("vpc", "main")        // myapp-prod-vpc-main
// bucketName := naming.ResourceWithRegion("s3", "data")  // myapp-prod-usw2-s3-data
// rdsName := naming.Short("rds", "01", 63)         // maprdbs01
```

**Python Naming Module:**

```python
# naming.py
from dataclasses import dataclass
from typing import Optional
import pulumi


@dataclass
class NamingConvention:
    """Naming convention for all infrastructure resources."""

    project: str
    environment: str
    region: str = "usw2"

    @classmethod
    def from_context(cls) -> "NamingConvention":
        """Create naming convention from Pulumi context."""
        return cls(
            project=pulumi.get_project(),
            environment=pulumi.get_stack(),
        )

    def resource(self, resource_type: str, name: str) -> str:
        """Generate resource name: {project}-{env}-{type}-{name}.

        Example: myapp-prod-vpc-main
        """
        return f"{self._sanitize(self.project)}-{self._sanitize(self.environment)}-{self._sanitize(resource_type)}-{self._sanitize(name)}"

    def resource_with_region(self, resource_type: str, name: str) -> str:
        """Generate name with region: {project}-{env}-{region}-{type}-{name}.

        Example: myapp-prod-usw2-s3-data
        """
        return f"{self._sanitize(self.project)}-{self._sanitize(self.environment)}-{self._sanitize(self.region)}-{self._sanitize(resource_type)}-{self._sanitize(name)}"

    def short(self, resource_type: str, name: str, max_len: int = 63) -> str:
        """Generate short name for resources with length limits.

        Pattern: {project_abbr}{env_abbr}{type_abbr}{name}
        Example: maprdbs01
        """
        abbr = (
            self._abbreviate(self.project, 2) +
            self._abbreviate(self.environment, 2) +
            self._abbreviate(resource_type, 3) +
            name
        )
        return abbr[:max_len]

    def tags(self, **additional_tags: str) -> dict[str, str]:
        """Return standard tags for all resources."""
        tags = {
            "Project": self.project,
            "Environment": self.environment,
            "ManagedBy": "pulumi",
        }
        tags.update(additional_tags)
        return tags

    def _sanitize(self, s: str) -> str:
        return s.lower().replace("_", "-")

    def _abbreviate(self, s: str, length: int) -> str:
        s = s.lower()
        return s[:length] if len(s) > length else s


# Usage example:
# naming = NamingConvention.from_context()
# vpc_name = naming.resource("vpc", "main")              # myapp-prod-vpc-main
# bucket_name = naming.resource_with_region("s3", "data")  # myapp-prod-usw2-s3-data
# rds_name = naming.short("rds", "01", max_len=63)       # maprdbs01
```

**Naming Convention Reference:**

| Resource Type  | Abbreviation | Example Name                  | Notes                           |
| -------------- | ------------ | ----------------------------- | ------------------------------- |
| VPC            | `vpc`        | `myapp-prod-vpc-main`         |                                 |
| Subnet         | `sn`         | `myapp-prod-sn-public-01`     | Include type (public/private)   |
| Security Group | `sg`         | `myapp-prod-sg-web`           |                                 |
| EC2 Instance   | `ec2`        | `myapp-prod-ec2-app-01`       | Include instance number         |
| RDS            | `rds`        | `myapp-prod-rds-primary`      |                                 |
| S3 Bucket      | `s3`         | `myapp-prod-usw2-s3-data`     | Globally unique, include region |
| Lambda         | `fn`         | `myapp-prod-fn-processor`     |                                 |
| EKS Cluster    | `eks`        | `myapp-prod-eks-main`         |                                 |
| IAM Role       | `role`       | `myapp-prod-role-lambda-exec` |                                 |
| CloudWatch Log | `log`        | `/myapp/prod/app`             | Use path format                 |

### 3. Component Resources

**Go Component Resource:**

```go
// components/vpc.go
package components

import (
    "fmt"

    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/ec2"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
    "myproject/naming"
)

// VpcArgs defines the arguments for creating a VPC
type VpcArgs struct {
    CidrBlock        string
    AzCount          int
    EnableNatGateway bool
    Tags             map[string]string
}

// Vpc is a component resource that creates a complete VPC setup
type Vpc struct {
    pulumi.ResourceState

    VpcId            pulumi.StringOutput   `pulumi:"vpcId"`
    PublicSubnetIds  pulumi.StringArrayOutput `pulumi:"publicSubnetIds"`
    PrivateSubnetIds pulumi.StringArrayOutput `pulumi:"privateSubnetIds"`
}

// NewVpc creates a new VPC component resource
func NewVpc(ctx *pulumi.Context, name string, args *VpcArgs, opts ...pulumi.ResourceOption) (*Vpc, error) {
    component := &Vpc{}

    err := ctx.RegisterComponentResource("custom:network:Vpc", name, component, opts...)
    if err != nil {
        return nil, err
    }

    n := naming.NewConvention(ctx)

    // Create VPC
    vpc, err := ec2.NewVpc(ctx, n.Resource("vpc", name), &ec2.VpcArgs{
        CidrBlock:          pulumi.String(args.CidrBlock),
        EnableDnsHostnames: pulumi.Bool(true),
        EnableDnsSupport:   pulumi.Bool(true),
        Tags:               n.Tags(args.Tags),
    }, pulumi.Parent(component))
    if err != nil {
        return nil, err
    }

    // Get availability zones
    azs, err := ec2.GetAvailabilityZones(ctx, &ec2.GetAvailabilityZonesArgs{
        State: pulumi.StringRef("available"),
    })
    if err != nil {
        return nil, err
    }

    // Create Internet Gateway
    igw, err := ec2.NewInternetGateway(ctx, n.Resource("igw", name), &ec2.InternetGatewayArgs{
        VpcId: vpc.ID(),
        Tags:  n.Tags(map[string]string{"Name": n.Resource("igw", name)}),
    }, pulumi.Parent(component))
    if err != nil {
        return nil, err
    }

    var publicSubnetIds pulumi.StringArray
    var privateSubnetIds pulumi.StringArray

    for i := 0; i < args.AzCount && i < len(azs.Names); i++ {
        azName := azs.Names[i]

        // Public subnet
        publicSubnet, err := ec2.NewSubnet(ctx, n.Resource("sn", fmt.Sprintf("public-%d", i)), &ec2.SubnetArgs{
            VpcId:               vpc.ID(),
            CidrBlock:           pulumi.Sprintf("10.0.%d.0/24", i),
            AvailabilityZone:    pulumi.String(azName),
            MapPublicIpOnLaunch: pulumi.Bool(true),
            Tags: n.Tags(map[string]string{
                "Name": n.Resource("sn", fmt.Sprintf("public-%d", i)),
                "Type": "public",
            }),
        }, pulumi.Parent(component))
        if err != nil {
            return nil, err
        }
        publicSubnetIds = append(publicSubnetIds, publicSubnet.ID())

        // Private subnet
        privateSubnet, err := ec2.NewSubnet(ctx, n.Resource("sn", fmt.Sprintf("private-%d", i)), &ec2.SubnetArgs{
            VpcId:            vpc.ID(),
            CidrBlock:        pulumi.Sprintf("10.0.%d.0/24", i+100),
            AvailabilityZone: pulumi.String(azName),
            Tags: n.Tags(map[string]string{
                "Name": n.Resource("sn", fmt.Sprintf("private-%d", i)),
                "Type": "private",
            }),
        }, pulumi.Parent(component))
        if err != nil {
            return nil, err
        }
        privateSubnetIds = append(privateSubnetIds, privateSubnet.ID())
    }

    component.VpcId = vpc.ID()
    component.PublicSubnetIds = publicSubnetIds.ToStringArrayOutput()
    component.PrivateSubnetIds = privateSubnetIds.ToStringArrayOutput()

    ctx.RegisterResourceOutputs(component, pulumi.Map{
        "vpcId":            vpc.ID(),
        "publicSubnetIds":  publicSubnetIds,
        "privateSubnetIds": privateSubnetIds,
    })

    return component, nil
}
```

**Python Component Resource:**

```python
# components/vpc.py
from dataclasses import dataclass
from typing import Optional

import pulumi
from pulumi import ComponentResource, ResourceOptions, Output
import pulumi_aws as aws

from naming import NamingConvention


@dataclass
class VpcArgs:
    """Arguments for creating a VPC."""
    cidr_block: str
    az_count: int
    enable_nat_gateway: bool = True
    tags: dict[str, str] | None = None


class Vpc(ComponentResource):
    """VPC component that creates a complete network setup."""

    vpc_id: Output[str]
    public_subnet_ids: Output[list[str]]
    private_subnet_ids: Output[list[str]]

    def __init__(
        self,
        name: str,
        args: VpcArgs,
        opts: ResourceOptions | None = None,
    ) -> None:
        super().__init__("custom:network:Vpc", name, None, opts)

        naming = NamingConvention.from_context()
        default_tags = naming.tags(**(args.tags or {}))

        # Create VPC
        vpc = aws.ec2.Vpc(
            naming.resource("vpc", name),
            cidr_block=args.cidr_block,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags={**default_tags, "Name": naming.resource("vpc", name)},
            opts=ResourceOptions(parent=self),
        )

        # Get availability zones
        azs = aws.get_availability_zones(state="available")

        # Create Internet Gateway
        igw = aws.ec2.InternetGateway(
            naming.resource("igw", name),
            vpc_id=vpc.id,
            tags={**default_tags, "Name": naming.resource("igw", name)},
            opts=ResourceOptions(parent=self),
        )

        public_subnets: list[aws.ec2.Subnet] = []
        private_subnets: list[aws.ec2.Subnet] = []

        for i in range(min(args.az_count, len(azs.names))):
            az_name = azs.names[i]

            # Public subnet
            public_subnet = aws.ec2.Subnet(
                naming.resource("sn", f"public-{i}"),
                vpc_id=vpc.id,
                cidr_block=f"10.0.{i}.0/24",
                availability_zone=az_name,
                map_public_ip_on_launch=True,
                tags={
                    **default_tags,
                    "Name": naming.resource("sn", f"public-{i}"),
                    "Type": "public",
                },
                opts=ResourceOptions(parent=self),
            )
            public_subnets.append(public_subnet)

            # Private subnet
            private_subnet = aws.ec2.Subnet(
                naming.resource("sn", f"private-{i}"),
                vpc_id=vpc.id,
                cidr_block=f"10.0.{i + 100}.0/24",
                availability_zone=az_name,
                tags={
                    **default_tags,
                    "Name": naming.resource("sn", f"private-{i}"),
                    "Type": "private",
                },
                opts=ResourceOptions(parent=self),
            )
            private_subnets.append(private_subnet)

        # Set outputs
        self.vpc_id = vpc.id
        self.public_subnet_ids = Output.all([s.id for s in public_subnets])
        self.private_subnet_ids = Output.all([s.id for s in private_subnets])

        self.register_outputs({
            "vpc_id": self.vpc_id,
            "public_subnet_ids": self.public_subnet_ids,
            "private_subnet_ids": self.private_subnet_ids,
        })


# Usage example:
# vpc = Vpc("main", VpcArgs(
#     cidr_block="10.0.0.0/16",
#     az_count=3,
#     enable_nat_gateway=True,
#     tags={"Team": "platform"},
# ))
```

### 4. Stack Management

**Go Configuration:**

```go
// config/config.go
package config

import (
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

// AppConfig holds all application configuration
type AppConfig struct {
    Environment      string
    Region           string
    VpcCidr          string
    EnableNatGateway bool
    InstanceType     string
    MinNodes         int
    MaxNodes         int
    DbInstanceClass  string
    AlertEmail       string
}

// Load loads configuration from Pulumi config
func Load(ctx *pulumi.Context) *AppConfig {
    cfg := config.New(ctx, "")
    awsCfg := config.New(ctx, "aws")

    return &AppConfig{
        Environment:      ctx.Stack(),
        Region:           awsCfg.Require("region"),
        VpcCidr:          cfg.Require("vpcCidr"),
        EnableNatGateway: cfg.GetBool("enableNatGateway"),
        InstanceType:     cfg.Get("instanceType"),
        MinNodes:         cfg.GetInt("minNodes"),
        MaxNodes:         cfg.GetInt("maxNodes"),
        DbInstanceClass:  cfg.Get("dbInstanceClass"),
        AlertEmail:       cfg.Get("alertEmail"),
    }
}
```

**Python Configuration:**

```python
# config.py
from dataclasses import dataclass
from typing import Literal

import pulumi


@dataclass
class AppConfig:
    """Application configuration from Pulumi config."""

    environment: Literal["dev", "staging", "prod"]
    region: str
    vpc_cidr: str
    enable_nat_gateway: bool
    instance_type: str
    min_nodes: int
    max_nodes: int
    db_instance_class: str
    alert_email: str | None

    @classmethod
    def load(cls) -> "AppConfig":
        """Load configuration from Pulumi config."""
        config = pulumi.Config()
        aws_config = pulumi.Config("aws")

        return cls(
            environment=pulumi.get_stack(),  # type: ignore
            region=aws_config.require("region"),
            vpc_cidr=config.require("vpcCidr"),
            enable_nat_gateway=config.get_bool("enableNatGateway") or True,
            instance_type=config.get("instanceType") or "t3.medium",
            min_nodes=config.get_int("minNodes") or 2,
            max_nodes=config.get_int("maxNodes") or 10,
            db_instance_class=config.get("dbInstanceClass") or "db.t3.medium",
            alert_email=config.get("alertEmail"),
        )
```

**Stack Configuration Files:**

```yaml
# Pulumi.dev.yaml
config:
  aws:region: us-west-2
  my-infra:vpcCidr: "10.0.0.0/16"
  my-infra:enableNatGateway: false
  my-infra:instanceType: t3.small
  my-infra:minNodes: 1
  my-infra:maxNodes: 3

# Pulumi.prod.yaml
config:
  aws:region: us-east-1
  my-infra:vpcCidr: "10.100.0.0/16"
  my-infra:enableNatGateway: true
  my-infra:instanceType: t3.large
  my-infra:minNodes: 3
  my-infra:maxNodes: 20
  my-infra:dbInstanceClass: db.r5.large
  my-infra:alertEmail:
    secure: AAABAxxxxxxx  # Encrypted secret
```

### 5. Secrets Management

**Go Secrets:**

```go
// main.go
package main

import (
    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/rds"
    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/secretsmanager"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
    "myproject/naming"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        cfg := config.New(ctx, "")
        n := naming.NewConvention(ctx)

        // Get secret from config (encrypted in state)
        dbPassword := cfg.RequireSecret("dbPassword")

        // Create secret in AWS Secrets Manager
        dbSecret, err := secretsmanager.NewSecret(ctx, n.Resource("secret", "db-creds"), &secretsmanager.SecretArgs{
            Name:        pulumi.Sprintf("/%s/%s/database/credentials", n.Project, n.Environment),
            Description: pulumi.String("Database credentials"),
        })
        if err != nil {
            return err
        }

        // Store secret value
        _, err = secretsmanager.NewSecretVersion(ctx, n.Resource("secret-v", "db-creds"), &secretsmanager.SecretVersionArgs{
            SecretId: dbSecret.ID(),
            SecretString: pulumi.Sprintf(`{"username": "admin", "password": "%s"}`, dbPassword),
        })
        if err != nil {
            return err
        }

        // Use secret in RDS
        _, err = rds.NewInstance(ctx, n.Resource("rds", "primary"), &rds.InstanceArgs{
            // ... other config
            Password: dbPassword,
        })

        // ✅ CORRECT: Export as secret
        ctx.Export("databasePassword", pulumi.ToSecret(dbPassword))

        return nil
    })
}
```

**Python Secrets:**

```python
# __main__.py
import pulumi
from pulumi import Config, Output
import pulumi_aws as aws

from naming import NamingConvention

config = Config()
naming = NamingConvention.from_context()

# Get secret from config (encrypted in state)
db_password = config.require_secret("dbPassword")

# Create secret in AWS Secrets Manager
db_secret = aws.secretsmanager.Secret(
    naming.resource("secret", "db-creds"),
    name=f"/{naming.project}/{naming.environment}/database/credentials",
    description="Database credentials",
)

# Store secret value
db_secret_version = aws.secretsmanager.SecretVersion(
    naming.resource("secret-v", "db-creds"),
    secret_id=db_secret.id,
    secret_string=db_password.apply(
        lambda pwd: f'{{"username": "admin", "password": "{pwd}"}}'
    ),
)

# Use secret in RDS
db_instance = aws.rds.Instance(
    naming.resource("rds", "primary"),
    # ... other config
    password=db_password,
)

# ✅ CORRECT: Export as secret
pulumi.export("database_password", Output.secret(db_password))
```

### 6. Testing Infrastructure

**Go Tests:**

```go
// tests/components_test.go
package tests

import (
    "testing"

    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
    "github.com/stretchr/testify/assert"
)

type mocks int

func (mocks) NewResource(args pulumi.MockResourceArgs) (string, resource.PropertyMap, error) {
    return args.Name + "_id", args.Inputs, nil
}

func (mocks) Call(args pulumi.MockCallArgs) (resource.PropertyMap, error) {
    if args.Token == "aws:index/getAvailabilityZones:getAvailabilityZones" {
        return resource.PropertyMap{
            "names": resource.NewArrayProperty([]resource.PropertyValue{
                resource.NewStringProperty("us-west-2a"),
                resource.NewStringProperty("us-west-2b"),
            }),
        }, nil
    }
    return resource.PropertyMap{}, nil
}

func TestVpcComponent(t *testing.T) {
    err := pulumi.RunErr(func(ctx *pulumi.Context) error {
        vpc, err := components.NewVpc(ctx, "test", &components.VpcArgs{
            CidrBlock:        "10.0.0.0/16",
            AzCount:          2,
            EnableNatGateway: true,
        })
        assert.NoError(t, err)

        // Test outputs
        pulumi.All(vpc.PublicSubnetIds, vpc.PrivateSubnetIds).ApplyT(
            func(args []interface{}) error {
                publicIds := args[0].([]string)
                privateIds := args[1].([]string)

                assert.Len(t, publicIds, 2, "should have 2 public subnets")
                assert.Len(t, privateIds, 2, "should have 2 private subnets")
                return nil
            },
        )

        return nil
    }, pulumi.WithMocks("project", "stack", mocks(0)))

    assert.NoError(t, err)
}
```

**Python Tests:**

```python
# tests/test_components.py
import unittest
from unittest.mock import Mock, patch

import pulumi


class MyMocks(pulumi.runtime.Mocks):
    """Mock Pulumi runtime for testing."""

    def new_resource(
        self, args: pulumi.runtime.MockResourceArgs
    ) -> tuple[str, dict]:
        return f"{args.name}_id", args.inputs

    def call(self, args: pulumi.runtime.MockCallArgs) -> tuple[dict, None]:
        if args.token == "aws:index/getAvailabilityZones:getAvailabilityZones":
            return {"names": ["us-west-2a", "us-west-2b"]}, None
        return {}, None


pulumi.runtime.set_mocks(MyMocks())


class TestVpcComponent(unittest.TestCase):
    """Test VPC component resource."""

    @pulumi.runtime.test
    def test_vpc_creates_correct_subnets(self):
        """Test that VPC creates correct number of subnets."""
        from components.vpc import Vpc, VpcArgs

        vpc = Vpc("test", VpcArgs(
            cidr_block="10.0.0.0/16",
            az_count=2,
            enable_nat_gateway=True,
        ))

        def check_subnets(subnet_ids):
            self.assertEqual(len(subnet_ids), 2)

        vpc.public_subnet_ids.apply(check_subnets)
        vpc.private_subnet_ids.apply(check_subnets)

    @pulumi.runtime.test
    def test_vpc_applies_tags(self):
        """Test that VPC applies correct tags."""
        from components.vpc import Vpc, VpcArgs

        vpc = Vpc("test", VpcArgs(
            cidr_block="10.0.0.0/16",
            az_count=1,
            tags={"Team": "platform"},
        ))

        # Verify tags are applied
        # (implementation depends on how you expose tags)


if __name__ == "__main__":
    unittest.main()
```

### 7. CI/CD Integration

```yaml
# .github/workflows/pulumi.yaml
name: Pulumi Infrastructure

on:
  push:
    branches: [main]
    paths:
      - "infrastructure/**"
  pull_request:
    branches: [main]
    paths:
      - "infrastructure/**"

env:
  PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}

jobs:
  preview:
    name: Preview
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      # For Go
      - uses: actions/setup-go@v5
        with:
          go-version: "1.22"
          cache-dependency-path: infrastructure/go.sum

      # Or for Python
      # - uses: actions/setup-python@v5
      #   with:
      #     python-version: '3.12'
      #     cache: 'pip'

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2

      - uses: pulumi/actions@v5
        with:
          command: preview
          stack-name: org-name/my-infra/dev
          work-dir: infrastructure
          comment-on-pr: true
          github-token: ${{ secrets.GITHUB_TOKEN }}

  deploy-dev:
    name: Deploy to Dev
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: development
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: "1.22"

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2

      - uses: pulumi/actions@v5
        with:
          command: up
          stack-name: org-name/my-infra/dev
          work-dir: infrastructure
```

### 8. Best Practices Patterns

**Go Resource Protection and Transformations:**

```go
package main

import (
    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/rds"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
    "myproject/naming"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        n := naming.NewConvention(ctx)

        // ✅ CORRECT: Protect critical resources
        _, err := rds.NewInstance(ctx, n.Resource("rds", "primary"), &rds.InstanceArgs{
            // ... config
        }, pulumi.Protect(true))

        // ✅ CORRECT: Use aliases for resource refactoring
        _, err = ec2.NewInstance(ctx, n.Resource("ec2", "new-name"), &ec2.InstanceArgs{
            // ... config
        }, pulumi.Aliases([]pulumi.Alias{
            {Name: pulumi.String(n.Resource("ec2", "old-name"))},
        }))

        // ✅ CORRECT: Explicit dependencies when needed
        dbSubnetGroup, _ := rds.NewSubnetGroup(ctx, n.Resource("rds-sng", "main"), &rds.SubnetGroupArgs{
            SubnetIds: vpc.PrivateSubnetIds,
        })

        _, err = rds.NewInstance(ctx, n.Resource("rds", "primary"), &rds.InstanceArgs{
            DbSubnetGroupName: dbSubnetGroup.Name,
        }, pulumi.DependsOn([]pulumi.Resource{dbSubnetGroup}))

        return nil
    })
}
```

**Python Resource Protection:**

```python
import pulumi
from pulumi import ResourceOptions
import pulumi_aws as aws

from naming import NamingConvention

naming = NamingConvention.from_context()

# ✅ CORRECT: Protect critical resources
db = aws.rds.Instance(
    naming.resource("rds", "primary"),
    # ... config
    opts=ResourceOptions(protect=True),
)

# ✅ CORRECT: Use aliases for resource refactoring
instance = aws.ec2.Instance(
    naming.resource("ec2", "new-name"),
    # ... config
    opts=ResourceOptions(
        aliases=[pulumi.Alias(name=naming.resource("ec2", "old-name"))],
    ),
)

# ✅ CORRECT: Explicit dependencies
db_subnet_group = aws.rds.SubnetGroup(
    naming.resource("rds-sng", "main"),
    subnet_ids=vpc.private_subnet_ids,
)

db = aws.rds.Instance(
    naming.resource("rds", "primary"),
    db_subnet_group_name=db_subnet_group.name,
    opts=ResourceOptions(depends_on=[db_subnet_group]),
)
```

## Quick Reference

### Pulumi CLI Commands

| Command                      | Description               |
| ---------------------------- | ------------------------- |
| `pulumi new go`              | Create new Go project     |
| `pulumi new python`          | Create new Python project |
| `pulumi stack init`          | Create new stack          |
| `pulumi stack select`        | Switch stacks             |
| `pulumi preview`             | Preview changes           |
| `pulumi up`                  | Deploy changes            |
| `pulumi destroy`             | Tear down resources       |
| `pulumi config set --secret` | Set encrypted config      |
| `pulumi refresh`             | Sync state with cloud     |
| `pulumi import`              | Import existing resources |

### Resource Options

| Option                | Description              |
| --------------------- | ------------------------ |
| `Parent`              | Set parent resource      |
| `DependsOn`           | Explicit dependencies    |
| `Protect`             | Prevent deletion         |
| `IgnoreChanges`       | Ignore property changes  |
| `Provider`            | Use specific provider    |
| `Aliases`             | Handle renames           |
| `Import`              | Import existing resource |
| `DeleteBeforeReplace` | Force replace order      |

## Common Pitfalls

| Pitfall              | Problem                     | Solution                                   |
| -------------------- | --------------------------- | ------------------------------------------ |
| Inconsistent naming  | Hard to identify resources  | Use naming convention module               |
| Hardcoded values     | Environment-specific config | Use Config and stack files                 |
| No protection        | Accidental deletion         | Use `Protect: true` for critical resources |
| Giant stacks         | Slow operations             | Split into micro-stacks                    |
| Secrets in outputs   | Exposed credentials         | Use `ToSecret()` or `Output.secret()`      |
| Missing dependencies | Race conditions             | Use explicit `DependsOn`                   |

## Best Practices Summary

### DO

1. Use consistent naming conventions across all resources
2. Use Component Resources for reusable infrastructure
3. Split large projects into micro-stacks
4. Encrypt secrets with `pulumi config set --secret`
5. Protect production resources with `Protect: true`
6. Tag all resources for cost allocation and management
7. Test infrastructure with unit tests
8. Version lock provider dependencies
9. Document component interfaces
10. Use type-safe configuration loading

### DON'T

1. Store secrets in plain text config
2. Create monolithic stacks with all resources
3. Hardcode environment-specific values
4. Skip preview before deployment
5. Use inconsistent resource names
6. Allow direct production deployments without review
7. Use `pulumi up --yes` without review in CI
8. Forget to register component outputs
9. Mix multiple concerns in one component
10. Ignore state drift (run refresh regularly)


## Parent Hub
- [_devops-cloud-mastery](../_devops-cloud-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
