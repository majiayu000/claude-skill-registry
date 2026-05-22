---
name: AWS Ecosystem
description: This skill should be used when the user asks to "aws cli", "aws configure", "aws sso", "aws sts", "terraform aws", or works with AWS CLI and Terraform AWS Provider patterns. Provides comprehensive AWS ecosystem patterns and best practices.
---

<purpose>
  Provide comprehensive patterns for AWS CLI configuration, authentication, common operations, and Terraform AWS Provider infrastructure as code.
</purpose>

<cli_configuration>
  <config_files>
    <file name="~/.aws/config">
      <description>AWS CLI configuration file</description>
      <example>
        [default]
        region = ap-northeast-1
        output = json

        [profile dev]
        region = ap-northeast-1
        output = json

        [profile prod]
        region = ap-northeast-1
        output = json
      </example>
    </file>

    <file name="~/.aws/credentials">
      <description>AWS credentials file (avoid storing long-term credentials)</description>
      <example>
        [default]
        aws_access_key_id = AKIA...
        aws_secret_access_key = ...
      </example>
      <warning>Prefer SSO or IAM roles over long-term credentials</warning>
    </file>
  </config_files>

  <environment_variables>
    <var name="AWS_PROFILE">Active profile name</var>
    <var name="AWS_REGION">Override region</var>
    <var name="AWS_DEFAULT_REGION">Default region</var>
    <var name="AWS_ACCESS_KEY_ID">Access key (avoid in production)</var>
    <var name="AWS_SECRET_ACCESS_KEY">Secret key (avoid in production)</var>
    <var name="AWS_SESSION_TOKEN">Session token for temporary credentials</var>
    <var name="AWS_CONFIG_FILE">Custom config file path</var>
    <var name="AWS_SHARED_CREDENTIALS_FILE">Custom credentials file path</var>
  </environment_variables>

  <profile_switching>
    <pattern name="environment_variable">
      <description>Set profile via environment variable</description>
      <example>export AWS_PROFILE=dev</example>
    </pattern>
    <pattern name="inline">
      <description>Set profile inline with command</description>
      <example>aws s3 ls --profile prod</example>
    </pattern>
  </profile_switching>
</cli_configuration>

<authentication>
  <decision_tree name="when_to_use">
    <question>Are you authenticating for human access or programmatic access?</question>
    <if_yes>Human: Use SSO for temporary credentials; Programmatic: Use IAM roles or OIDC federation</if_yes>
    <if_no>Never use long-term access keys in production</if_no>
  </decision_tree>

  <sso>
    <description>AWS IAM Identity Center (SSO) authentication (2025 recommended)</description>
    <example>
      [profile sso-dev]
      sso_session = my-sso
      sso_account_id = 123456789012
      sso_role_name = DeveloperAccess
      region = ap-northeast-1
      output = json

      [sso-session my-sso]
      sso_start_url = https://example.awsapps.com/start
      sso_region = ap-northeast-1
      sso_registration_scopes = sso:account:access
    </example>
    <commands>
      <command name="login">aws sso login --sso-session my-sso</command>
      <command name="logout">aws sso logout --sso-session my-sso</command>
    </commands>
    <concept name="pkce_authorization">
      <description>PKCE authorization (default since AWS CLI v2.22.0)</description>
      <note>Recommended for desktop/mobile access; provides secure OAuth 2.0 flow</note>
    </concept>
    <concept name="token_refresh">
      <description>Automatic token refresh without re-authentication</description>
      <note>Requires AWS CLI v2.9.0+ or v1.27.10+; sso-session configuration enables token refresh support</note>
    </concept>
    <note>Use SSO with sso-session for human users; use IAM roles for services</note>
  </sso>

  <assume_role>
    <description>Cross-account or elevated access via role assumption</description>
    <example>
      [profile cross-account]
      role_arn = arn:aws:iam::987654321098:role/CrossAccountRole
      source_profile = default
      region = ap-northeast-1
    </example>
    <example>
      aws sts assume-role --role-arn arn:aws:iam::123456789012:role/MyRole --role-session-name session1
    </example>
    <concept name="chained_roles">
      <description>Assume role from another assumed role</description>
      <example>
        [profile chained]
        role_arn = arn:aws:iam::111111111111:role/FinalRole
        source_profile = cross-account
      </example>
    </concept>
  </assume_role>

  <mfa>
    <description>Multi-factor authentication for CLI</description>
    <example>
      [profile mfa-required]
      role_arn = arn:aws:iam::123456789012:role/AdminRole
      source_profile = default
      mfa_serial = arn:aws:iam::123456789012:mfa/username
    </example>
    <example>
      aws sts get-session-token --serial-number arn:aws:iam::123456789012:mfa/username --token-code 123456
    </example>
  </mfa>

  <credential_process>
    <description>External credential provider</description>
    <example>
      [profile external]
      credential_process = /path/to/credential-provider
    </example>
    <note>Integration with 1Password, Vault, or custom providers</note>
  </credential_process>

  <oidc_federation>
    <description>OIDC federation for CI/CD (2025 best practice)</description>
    <note>Use cases: GitHub Actions, GitLab CI, Azure DevOps with OIDC</note>
    <example>

      <file_reference>.github/workflows/deploy.yml</file_reference>

      permissions:
      id-token: write
      contents: read

      jobs:
      deploy:
      runs-on: ubuntu-latest
      steps: - uses: aws-actions/configure-aws-credentials@v4
      with:
      role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
      aws-region: ap-northeast-1
    </example>
    <note>No long-term credentials stored in CI/CD; temporary credentials via STS</note>
    <warning>Validate OIDC thumbprints and restrict ClientIDList to prevent misconfiguration</warning>
  </oidc_federation>

  <verification>
    <description>Verify current AWS identity</description>
    <example>
      aws sts get-caller-identity
    </example>
    <example>
      {
      "UserId": "AIDAEXAMPLE",
      "Account": "123456789012",
      "Arn": "arn:aws:iam::123456789012:user/username"
      }
    </example>
  </verification>
</authentication>

<output_filtering>
  <decision_tree name="when_to_use">
    <question>Do you need to filter or transform AWS CLI output?</question>
    <if_yes>Use --query for AWS-native filtering or pipe to jq for complex transformations</if_yes>
    <if_no>Use default JSON output for full response data</if_no>
  </decision_tree>

  <output_formats>
    <format name="json">Default, machine-readable (--output json)</format>
    <format name="text">Tab-delimited, scriptable (--output text)</format>
    <format name="table">Human-readable (--output table)</format>
    <format name="yaml">YAML format (--output yaml)</format>
  </output_formats>

  <query_examples>
    <pattern name="single_value">
      <description>Extract single value from query</description>
      <example>aws ec2 describe-instances --query 'Reservations[0].Instances[0].InstanceId' --output text</example>
    </pattern>

    <pattern name="list">
      <description>Extract list of values</description>
      <example>aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --output text</example>
    </pattern>

    <pattern name="filtered">
      <description>Filter results by condition</description>
      <example>aws ec2 describe-instances --query 'Reservations[].Instances[?State.Name==`running`].InstanceId' --output text</example>
    </pattern>

    <pattern name="projection">
      <description>Project multiple fields with custom formatting</description>
      <example>aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table</example>
    </pattern>

    <pattern name="sorting">
      <description>Sort results by field</description>
      <example>aws ec2 describe-instances --query 'sort_by(Reservations[].Instances[], &amp;LaunchTime)[].InstanceId'</example>
    </pattern>
  </query_examples>

  <jq_integration>
    <pattern name="basic">
      <description>Basic jq filtering</description>
      <example>aws ec2 describe-instances | jq '.Reservations[].Instances[].InstanceId'</example>
    </pattern>
    <pattern name="complex">
      <description>Complex jq transformation with TSV output</description>
      <example>aws ec2 describe-instances | jq -r '.Reservations[].Instances[] | [.InstanceId, .State.Name] | @tsv'</example>
    </pattern>
  </jq_integration>
</output_filtering>

<common_commands>
  <s3>
    <command name="list_buckets">aws s3 ls</command>
    <command name="list_objects">aws s3 ls s3://bucket-name/prefix/</command>
    <command name="copy">aws s3 cp file.txt s3://bucket-name/</command>
    <command name="sync">aws s3 sync ./local-dir s3://bucket-name/prefix/</command>
    <command name="presign">aws s3 presign s3://bucket-name/object-key --expires-in 3600</command>
  </s3>

  <ec2>
    <command name="list_instances">aws ec2 describe-instances</command>
    <command name="start">aws ec2 start-instances --instance-ids i-1234567890abcdef0</command>
    <command name="stop">aws ec2 stop-instances --instance-ids i-1234567890abcdef0</command>
    <command name="terminate">aws ec2 terminate-instances --instance-ids i-1234567890abcdef0</command>
  </ec2>

  <iam>
    <command name="list_users">aws iam list-users</command>
    <command name="list_roles">aws iam list-roles</command>
    <command name="get_policy">aws iam get-policy --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess</command>
  </iam>

  <lambda>
    <command name="list_functions">aws lambda list-functions</command>
    <command name="invoke">aws lambda invoke --function-name my-function --payload '{"key": "value"}' response.json</command>
    <command name="logs">aws logs tail /aws/lambda/my-function --follow</command>
  </lambda>

  <ecs>
    <command name="list_clusters">aws ecs list-clusters</command>
    <command name="list_services">aws ecs list-services --cluster cluster-name</command>
    <command name="describe_tasks">aws ecs describe-tasks --cluster cluster-name --tasks task-arn</command>
    <command name="exec">aws ecs execute-command --cluster cluster-name --task task-id --container container-name --interactive --command "/bin/sh"</command>
  </ecs>

  <cloudwatch>
    <command name="tail_logs">aws logs tail /aws/lambda/function-name --follow</command>
    <command name="filter_logs">aws logs filter-log-events --log-group-name /aws/lambda/function-name --filter-pattern "ERROR"</command>
    <command name="get_metrics">aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=i-1234567890abcdef0 --start-time 2024-01-01T00:00:00Z --end-time 2024-01-02T00:00:00Z --period 3600 --statistics Average</command>
  </cloudwatch>

  <ssm>
    <command name="get_parameter">aws ssm get-parameter --name /path/to/param --with-decryption</command>
    <command name="put_parameter">aws ssm put-parameter --name /path/to/param --value "secret" --type SecureString</command>
    <command name="start_session">aws ssm start-session --target i-1234567890abcdef0</command>
  </ssm>

  <secrets_manager>
    <command name="get_secret">aws secretsmanager get-secret-value --secret-id my-secret --query SecretString --output text</command>
    <command name="create_secret">aws secretsmanager create-secret --name my-secret --secret-string '{"key":"value"}'</command>
  </secrets_manager>
</common_commands>

<scripting_patterns>
  <wait_commands>
    <pattern name="instance_running">
      <description>Wait for EC2 instance to reach running state</description>
      <example>aws ec2 wait instance-running --instance-ids i-1234567890abcdef0</example>
    </pattern>
    <pattern name="stack_complete">
      <description>Wait for CloudFormation stack creation</description>
      <example>aws cloudformation wait stack-create-complete --stack-name my-stack</example>
    </pattern>
  </wait_commands>

  <pagination>
    <pattern name="manual">
      <description>Manual pagination with token</description>
      <example>aws s3api list-objects-v2 --bucket bucket-name --max-items 100 --starting-token TOKEN</example>
    </pattern>
    <pattern name="automatic">
      <description>Automatic pagination with query</description>
      <example>aws s3api list-objects-v2 --bucket bucket-name --query 'Contents[].Key' --output text</example>
    </pattern>
  </pagination>

  <pattern name="dry_run">
    <description>Test commands without execution</description>
    <example>aws ec2 run-instances --dry-run --image-id ami-12345678 --instance-type t3.micro</example>
  </pattern>

  <batch_operations>
    <pattern name="loop">
      <description>Batch operations using shell loop</description>
      <example>
        for id in $(aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --output text); do
        aws ec2 create-tags --resources "$id" --tags Key=Environment,Value=Dev
        done
      </example>
    </pattern>

    <pattern name="xargs">
      <description>Batch operations using xargs</description>
      <example>
        aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --output text | \
        xargs -I {} aws ec2 create-tags --resources {} --tags Key=Backup,Value=true
      </example>
    </pattern>
  </batch_operations>
</scripting_patterns>

<anti_patterns>
  <avoid name="hardcoded_credentials">
    <description>Never hardcode credentials in scripts or config</description>
    <instead>Use IAM roles, SSO, or credential_process</instead>
  </avoid>

  <avoid name="long_term_credentials">
    <description>Avoid using long-term access keys</description>
    <instead>Use temporary credentials via SSO or AssumeRole</instead>
  </avoid>

  <avoid name="root_account">
    <description>Never use root account credentials for CLI</description>
    <instead>Create IAM users or use SSO with appropriate permissions</instead>
  </avoid>

  <avoid name="shared_credentials">
    <description>Do not share credentials between team members</description>
    <instead>Each user should have their own SSO access or IAM user</instead>
  </avoid>

  <avoid name="credentials_in_env">
    <description>Avoid exporting credentials in shell history</description>
    <instead>Use aws configure or credential files with proper permissions</instead>
  </avoid>

  <avoid name="wildcard_permissions">
    <description>Avoid policies with Resource: "*" and Action: "*"</description>
    <instead>Follow least privilege principle</instead>
  </avoid>
</anti_patterns>

<best_practices>
  <practice priority="critical">Eliminate long-term access keys; use SSO or IAM roles instead</practice>
  <practice priority="critical">Use sso-session configuration for token refresh support (CLI v2.9.0+)</practice>
  <practice priority="critical">Use OIDC federation for CI/CD (GitHub Actions, GitLab CI)</practice>
  <practice priority="critical">Use Instance Profiles for EC2, EKS Service Accounts for K8s, Lambda Execution Roles for serverless</practice>
  <practice priority="high">Enable MFA for all human users</practice>
  <practice priority="high">Follow least privilege principle; avoid wildcard permissions</practice>
  <practice priority="high">Enable CloudTrail for CLI activity monitoring</practice>
  <practice>Use --query for filtering instead of jq when possible</practice>
  <practice>Set default region in config to avoid specifying every time</practice>
  <practice>Use named profiles for different environments</practice>
  <practice>Use aws sts get-caller-identity to verify current identity</practice>
  <practice>Enable CLI auto-prompt: export AWS_CLI_AUTO_PROMPT=on-partial</practice>
  <practice>Use --dry-run for destructive operations first</practice>
  <practice>Use wait commands in scripts for async operations</practice>
  <practice>Store credentials file with 600 permissions</practice>
</best_practices>

<terraform>
  <decision_tree name="when_to_use">
    <question>Are you managing AWS infrastructure as code?</question>
    <if_yes>Use Terraform for declarative, version-controlled infrastructure</if_yes>
    <if_no>Use AWS CLI for one-off operations or AWS Console for exploration</if_no>
  </decision_tree>

  <provider_configuration>
    <pattern name="basic">
      <description>Basic AWS provider configuration</description>
      <example>
        terraform {
        required_providers {
        aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
        }
        }
        }

        provider "aws" {
        region = "ap-northeast-1"
        }
      </example>
    </pattern>

    <pattern name="with_profile">
      <description>Using AWS CLI profile</description>
      <example>
        provider "aws" {
        region  = "ap-northeast-1"
        profile = "dev"
        }
      </example>
    </pattern>

    <pattern name="with_assume_role">
      <description>Cross-account access with assume role</description>
      <example>
        provider "aws" {
        region = "ap-northeast-1"

        assume_role {
        role_arn = "arn:aws:iam::987654321098:role/TerraformRole"
        session_name = "terraform-session"
        external_id = "unique-external-id"
        }
        }
      </example>
    </pattern>

    <pattern name="multi_region">
      <description>Multiple region configuration with aliases</description>
      <example>
        provider "aws" {
        region = "ap-northeast-1"
        alias  = "tokyo"
        }

        provider "aws" {
        region = "us-east-1"
        alias = "virginia"
        }

        resource "aws_s3_bucket" "tokyo_bucket" {
        provider = aws.tokyo
        bucket = "my-tokyo-bucket"
        }

        resource "aws_s3_bucket" "virginia_bucket" {
        provider = aws.virginia
        bucket = "my-virginia-bucket"
        }
      </example>
    </pattern>

    <pattern name="default_tags">
      <description>Apply default tags to all resources</description>
      <example>
        provider "aws" {
        region = "ap-northeast-1"

        default_tags {
        tags = {
        Environment = "dev"
        ManagedBy = "terraform"
        Project = "my-project"
        }
        }
        }
      </example>
    </pattern>
  </provider_configuration>

  <backend_configuration>
    <pattern name="s3_backend">
      <description>Remote state with S3 and DynamoDB locking</description>
      <example>
        terraform {
        backend "s3" {
        bucket = "my-terraform-state"
        key = "env/dev/terraform.tfstate"
        region = "ap-northeast-1"
        encrypt = true
        dynamodb_table = "terraform-locks"
        }
        }
      </example>
    </pattern>

    <pattern name="state_locking">
      <description>DynamoDB table for state locking</description>
      <example>
        resource "aws_dynamodb_table" "terraform_locks" {
        name         = "terraform-locks"
        billing_mode = "PAY_PER_REQUEST"
        hash_key     = "LockID"

        attribute {
        name = "LockID"
        type = "S"
        }
        }
      </example>
    </pattern>
  </backend_configuration>

  <common_resources>
    <pattern name="vpc">
      <description>VPC with subnets and internet gateway</description>
      <example>
        resource "aws_vpc" "main" {
        cidr_block = "10.0.0.0/16"
        enable_dns_hostnames = true
        enable_dns_support = true

        tags = {
        Name = "main-vpc"
        }
        }

        resource "aws_subnet" "public" {
        count = 2
        vpc_id = aws_vpc.main.id
        cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
        availability_zone = data.aws_availability_zones.available.names[count.index]
        map_public_ip_on_launch = true

        tags = {
        Name = "public-subnet-${count.index + 1}"
        }
        }

        resource "aws_internet_gateway" "main" {
        vpc_id = aws_vpc.main.id
        }
      </example>
    </pattern>

    <pattern name="security_group">
      <description>Security group with ingress and egress rules</description>
      <example>
        resource "aws_security_group" "web" {
        name        = "web-sg"
        description = "Security group for web servers"
        vpc_id      = aws_vpc.main.id

        ingress {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
        }

        egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
        }
        }
      </example>
    </pattern>

    <pattern name="iam_role">
      <description>IAM role with policy attachment</description>
      <example>
        resource "aws_iam_role" "lambda_role" {
        name = "lambda-execution-role"

        assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
        Service = "lambda.amazonaws.com"
        }
        }
        ]
        })
        }

        resource "aws_iam_role_policy_attachment" "lambda_basic" {
        role = aws_iam_role.lambda_role.name
        policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
        }
      </example>
    </pattern>

    <pattern name="oidc_provider">
      <description>OIDC provider for GitHub Actions (2025 recommended)</description>
      <example>
        resource "aws_iam_openid_connect_provider" "github" {
        url = "https://token.actions.githubusercontent.com"

        client_id_list = ["sts.amazonaws.com"]

        thumbprint_list = ["ffffffffffffffffffffffffffffffffffffffff"]
        }

        resource "aws_iam_role" "github_actions" {
        name = "github-actions-role"

        assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
        Effect = "Allow"
        Principal = {
        Federated = aws_iam_openid_connect_provider.github.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
        StringEquals = {
        "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
        "token.actions.githubusercontent.com:sub" = "repo:org/repo:*"
        }
        }
        }
        ]
        })
        }
      </example>
      <note>Always restrict sub claim to specific repos/branches</note>
    </pattern>

    <pattern name="sts_preferences">
      <description>STS global endpoint token version (2025 security)</description>
      <example>
        resource "aws_iam_security_token_service_preferences" "main" {
        global_endpoint_token_version = "v2Token"
        }
      </example>
      <note>v2Token provides regional STS tokens for improved security</note>
    </pattern>

    <pattern name="s3_bucket">
      <description>S3 bucket with versioning, encryption, and public access block</description>
      <example>
        resource "aws_s3_bucket" "main" {
        bucket = "my-unique-bucket-name"
        }

        resource "aws_s3_bucket_versioning" "main" {
        bucket = aws_s3_bucket.main.id
        versioning_configuration {
        status = "Enabled"
        }
        }

        resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
        bucket = aws_s3_bucket.main.id

        rule {
        apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
        }
        }
        }

        resource "aws_s3_bucket_public_access_block" "main" {
        bucket = aws_s3_bucket.main.id

        block_public_acls = true
        block_public_policy = true
        ignore_public_acls = true
        restrict_public_buckets = true
        }
      </example>
    </pattern>

    <pattern name="lambda">
      <description>Lambda function with environment variables</description>
      <example>
        resource "aws_lambda_function" "main" {
        function_name = "my-function"
        role          = aws_iam_role.lambda_role.arn
        handler       = "index.handler"
        runtime       = "nodejs20.x"  # or "nodejs22.x" (Node.js 22 LTS)
        timeout       = 30
        memory_size   = 256

        filename = "lambda.zip"
        source_code_hash = filebase64sha256("lambda.zip")

        environment {
        variables = {
        ENV = "production"
        }
        }
        }
      </example>
    </pattern>

    <pattern name="ecs">
      <description>ECS cluster with Fargate task definition</description>
      <example>
        resource "aws_ecs_cluster" "main" {
        name = "my-cluster"

        setting {
        name = "containerInsights"
        value = "enabled"
        }
        }

        resource "aws_ecs_task_definition" "app" {
        family = "my-app"
        network_mode = "awsvpc"
        requires_compatibilities = ["FARGATE"]
        cpu = "256"
        memory = "512"
        execution_role_arn = aws_iam_role.ecs_execution.arn
        task_role_arn = aws_iam_role.ecs_task.arn

        container_definitions = jsonencode([
        {
        name = "app"
        image = "nginx:latest"
        portMappings = [
        {
        containerPort = 80
        hostPort = 80
        }
        ]
        }
        ])
        }
      </example>
    </pattern>

    <pattern name="rds">
      <description>RDS PostgreSQL instance with encryption and backups</description>
      <example>
        resource "aws_db_instance" "main" {
        identifier           = "my-database"
        engine               = "postgres"
        engine_version       = "15"
        instance_class       = "db.t3.micro"
        allocated_storage    = 20
        storage_encrypted    = true

        db_name = "mydb"
        username = "admin"
        password = var.db_password

        vpc_security_group_ids = [aws_security_group.rds.id]
        db_subnet_group_name = aws_db_subnet_group.main.name

        backup_retention_period = 7
        skip_final_snapshot = false
        final_snapshot_identifier = "my-database-final"

        tags = {
        Name = "my-database"
        }
        }
      </example>
    </pattern>
  </common_resources>

  <data_sources>
    <pattern name="availability_zones">
      <description>Get available availability zones</description>
      <example>
        data "aws_availability_zones" "available" {
        state = "available"
        }
      </example>
    </pattern>

    <pattern name="caller_identity">
      <description>Get current AWS account ID and ARN</description>
      <example>
        data "aws_caller_identity" "current" {}

        output "account_id" {
        value = data.aws_caller_identity.current.account_id
        }
      </example>
    </pattern>

    <pattern name="region">
      <description>Get current AWS region</description>
      <example>
        data "aws_region" "current" {}

        output "region" {
        value = data.aws_region.current.name
        }
      </example>
    </pattern>

    <pattern name="ami">
      <description>Find latest Amazon Linux AMI</description>
      <example>
        data "aws_ami" "amazon_linux" {
        most_recent = true
        owners      = ["amazon"]

        filter {
        name = "name"
        values = ["al2023-ami-*-x86_64"]
        }
        }
      </example>
    </pattern>
  </data_sources>

  <modules>
    <pattern name="local_module">
      <description>Local module reference</description>
      <example>
        module "vpc" {
        source = "./modules/vpc"

        cidr_block = "10.0.0.0/16"
        name = "main"
        }
      </example>
    </pattern>

    <pattern name="registry_module">
      <description>Terraform Registry module</description>
      <example>
        module "vpc" {
        source  = "terraform-aws-modules/vpc/aws"
        version = "5.0.0"

        name = "my-vpc"
        cidr = "10.0.0.0/16"

        azs = ["ap-northeast-1a", "ap-northeast-1c"]
        private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
        public_subnets = ["10.0.101.0/24", "10.0.102.0/24"]

        enable_nat_gateway = true
        single_nat_gateway = true
        }
      </example>
    </pattern>
  </modules>

  <terraform_commands>
    <command name="init">terraform init</command>
    <command name="plan">terraform plan -out=tfplan</command>
    <command name="apply">terraform apply tfplan</command>
    <command name="destroy">terraform destroy</command>
    <command name="fmt">terraform fmt -recursive</command>
    <command name="validate">terraform validate</command>
    <command name="state_list">terraform state list</command>
    <command name="state_show">terraform state show aws_instance.example</command>
    <command name="import">terraform import aws_instance.example i-1234567890abcdef0</command>
    <command name="refresh">terraform refresh</command>
    <command name="output">terraform output -json</command>
  </terraform_commands>

  <terraform_anti_patterns>
    <avoid name="hardcoded_credentials">
      <description>Never hardcode AWS credentials in Terraform files</description>
      <instead>Use environment variables, AWS CLI profiles, or IAM roles</instead>
    </avoid>

    <avoid name="hardcoded_secrets">
      <description>Never store secrets in terraform.tfvars or state</description>
      <instead>Use AWS Secrets Manager, SSM Parameter Store, or external secret management</instead>
    </avoid>

    <avoid name="no_state_locking">
      <description>Running Terraform without state locking in teams</description>
      <instead>Use DynamoDB table for S3 backend locking</instead>
    </avoid>

    <avoid name="wildcard_permissions">
      <description>Using "*" for resources and actions in IAM policies</description>
      <instead>Follow least privilege principle with specific resources</instead>
    </avoid>

    <avoid name="unencrypted_state">
      <description>Storing state without encryption</description>
      <instead>Enable encryption for S3 backend state</instead>
    </avoid>

    <avoid name="no_versioning">
      <description>Not versioning provider and module versions</description>
      <instead>Pin versions with ~> or exact versions</instead>
    </avoid>
  </terraform_anti_patterns>

  <terraform_best_practices>
    <practice priority="critical">Use remote state with S3 backend and DynamoDB locking</practice>
    <practice priority="critical">Enable state encryption with encrypt = true</practice>
    <practice priority="critical">Pin provider versions to avoid breaking changes</practice>
    <practice priority="high">Use default_tags for consistent resource tagging</practice>
    <practice priority="high">Separate environments using workspaces or directory structure</practice>
    <practice priority="high">Run terraform plan before apply to review changes</practice>
    <practice priority="medium">Use terraform fmt before committing code</practice>
    <practice priority="medium">Use data sources instead of hardcoding ARNs</practice>
    <practice priority="medium">Store sensitive variables in environment or secret managers</practice>
    <practice priority="medium">Use modules for reusable infrastructure components</practice>
    <practice priority="medium">Enable versioning on S3 state bucket</practice>
    <practice priority="medium">Use lifecycle rules to prevent accidental deletion</practice>
  </terraform_best_practices>

  <context7_integration>
    <tool name="resolve-library-id">
      <description>Library ID is already known: /hashicorp/terraform-provider-aws (trust score 9.8, 31100 snippets)</description>
    </tool>

    <tool name="get-library-docs">
      <description>Fetch documentation with specific topic</description>
      <use_case>VPC and networking resources (topic: vpc)</use_case>
      <use_case>IAM roles and policies (topic: iam)</use_case>
      <use_case>Lambda function configuration (topic: lambda)</use_case>
      <use_case>ECS cluster and task definitions (topic: ecs)</use_case>
      <use_case>S3 bucket configuration (topic: s3)</use_case>
    </tool>
  </context7_integration>
</terraform>

<workflow>
  <phase name="analyze">
    <objective>Understand AWS infrastructure requirements</objective>
    <step>1. Identify target AWS services and regions</step>
    <step>2. Review existing infrastructure patterns</step>
    <step>3. Check IAM permissions and policies</step>
  </phase>
  <phase name="implement">
    <objective>Implement AWS resources safely</objective>
    <step>1. Use Terraform for infrastructure as code</step>
    <step>2. Follow least-privilege IAM principles</step>
    <step>3. Tag resources appropriately</step>
  </phase>
  <phase name="validate">
    <objective>Verify AWS configuration correctness</objective>
    <step>1. Run terraform plan to preview changes</step>
    <step>2. Verify security group rules</step>
    <step>3. Test access and connectivity</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Minor tagging inconsistency</example>
    <action>Fix tags, follow naming conventions</action>
  </level>
  <level severity="medium">
    <example>IAM policy too permissive</example>
    <action>Restrict permissions, apply least privilege</action>
  </level>
  <level severity="high">
    <example>Security group allows unrestricted access</example>
    <action>Stop, require security review before proceeding</action>
  </level>
  <level severity="critical">
    <example>Potential data exposure or credential leak</example>
    <action>Block operation, require immediate remediation</action>
  </level>
</error_escalation>

<constraints>
  <must>Use Terraform for infrastructure management</must>
  <must>Follow least-privilege IAM principles</must>
  <must>Enable encryption at rest and in transit</must>
  <avoid>Hardcoding credentials in code</avoid>
  <avoid>Overly permissive security groups</avoid>
  <avoid>Untagged resources</avoid>
</constraints>

<related_agents>
  <agent name="design">Architecture design for AWS infrastructure and service integration</agent>
  <agent name="docs">CloudFormation and Terraform documentation generation</agent>
  <agent name="execute">AWS CLI operations and Terraform deployment tasks</agent>
  <agent name="bug">Debugging AWS API errors and Terraform state issues</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Symbol operations for Terraform code navigation</skill>
  <skill name="context7-usage">Terraform AWS Provider documentation via /hashicorp/terraform-provider-aws</skill>
  <skill name="investigation-patterns">Debugging authentication failures and service quota issues</skill>
  <skill name="technical-documentation">Creating infrastructure documentation and runbooks</skill>
</related_skills>
