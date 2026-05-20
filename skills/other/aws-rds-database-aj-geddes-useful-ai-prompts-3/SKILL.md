---
name: aws-rds-database
description: Deploy and manage relational databases using RDS with Multi-AZ, read replicas, backups, and encryption. Use for PostgreSQL, MySQL, MariaDB, and Oracle.
---

# AWS RDS Database

## Overview

Amazon RDS simplifies relational database deployment and operations. Support multiple database engines with automated backups, replication, encryption, and high availability through Multi-AZ deployments.

## When to Use

- PostgreSQL and MySQL applications
- Transactional databases and OLTP
- Oracle and Microsoft SQL Server workloads
- Read-heavy applications with replicas
- Development and staging environments
- Data requiring ACID compliance
- Applications needing automatic backups
- Disaster recovery scenarios

## Implementation Examples

### 1. **RDS Instance Creation with AWS CLI**

```bash
# Create DB subnet group
aws rds create-db-subnet-group \
  --db-subnet-group-name app-db-subnet \
  --db-subnet-group-description "App database subnet" \
  --subnet-ids subnet-12345 subnet-67890

# Create security group for RDS
aws ec2 create-security-group \
  --group-name rds-sg \
  --description "RDS security group" \
  --vpc-id vpc-12345

# Allow inbound PostgreSQL
aws ec2 authorize-security-group-ingress \
  --group-id sg-rds123 \
  --protocol tcp \
  --port 5432 \
  --source-security-group-id sg-app123

# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier myapp-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.2 \
  --master-username admin \
  --master-user-password MySecurePassword123! \
  --allocated-storage 100 \
  --storage-type gp3 \
  --db-subnet-group-name app-db-subnet \
  --vpc-security-group-ids sg-rds123 \
  --multi-az \
  --storage-encrypted \
  --kms-key-id arn:aws:kms:region:account:key/id \
  --backup-retention-period 30 \
  --preferred-backup-window "03:00-04:00" \
  --preferred-maintenance-window "mon:04:00-mon:05:00" \
  --enable-clouwatch-logs-exports postgresql \
  --enable-iam-database-authentication

# Create read replica
aws rds create-db-instance-read-replica \
  --db-instance-identifier myapp-db-read \
  --source-db-instance-identifier myapp-db

# Take manual snapshot
aws rds create-db-snapshot \
  --db-snapshot-identifier myapp-db-backup-2024 \
  --db-instance-identifier myapp-db

# Describe RDS instance
aws rds describe-db-instances \
  --db-instance-identifier myapp-db \
  --query 'DBInstances[0].[DBInstanceIdentifier,DBInstanceStatus,Endpoint.Address]'
```

### 2. **Terraform RDS Configuration**

```hcl
# rds.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# DB subnet group
resource "aws_db_subnet_group" "app" {
  name       = "app-db-subnet"
  subnet_ids = [aws_subnet.private1.id, aws_subnet.private2.id]

  tags = { Name = "app-db-subnet" }
}

# Security group
resource "aws_security_group" "rds" {
  name_prefix = "rds-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# KMS key for encryption
resource "aws_kms_key" "rds" {
  description             = "RDS encryption key"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_kms_alias" "rds" {
  name          = "alias/rds-key"
  target_key_id = aws_kms_key.rds.key_id
}

# RDS instance
resource "aws_db_instance" "app" {
  identifier            = "myapp-db"
  engine               = "postgres"
  engine_version       = "15.2"
  instance_class       = "db.t3.micro"
  allocated_storage    = 100
  storage_type         = "gp3"
  storage_encrypted    = true
  kms_key_id           = aws_kms_key.rds.arn

  db_name  = "appdb"
  username = "admin"
  password = random_password.db_password.result

  db_subnet_group_name   = aws_db_subnet_group.app.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  multi_az               = true
  publicly_accessible    = false

  backup_retention_period = 30
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"
  copy_tags_to_snapshot   = true

  enabled_cloudwatch_logs_exports = ["postgresql"]

  enable_iam_database_authentication = true

  deletion_protection = true

  skip_final_snapshot       = false
  final_snapshot_identifier = "myapp-db-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"

  tags = {
    Name = "myapp-db"
  }
}

# Generate random password
resource "random_password" "db_password" {
  length  = 16
  special = true
}

# Store password in Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name_prefix             = "rds/myapp/"
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    username = aws_db_instance.app.username
    password = random_password.db_password.result
    engine   = "postgres"
    host     = aws_db_instance.app.address
    port     = aws_db_instance.app.port
    dbname   = aws_db_instance.app.db_name
  })
}

# Read replica
resource "aws_db_instance" "read_replica" {
  identifier     = "myapp-db-read"
  replicate_source_db = aws_db_instance.app.identifier
  instance_class      = "db.t3.micro"
  publicly_accessible = false

  tags = {
    Name = "myapp-db-read"
  }
}

# Enhanced monitoring role
resource "aws_iam_role" "rds_monitoring" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "monitoring.rds.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# CloudWatch alarms
resource "aws_cloudwatch_metric_alarm" "db_cpu" {
  alarm_name          = "rds-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "Alert when RDS CPU exceeds 80%"

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.app.id
  }
}

resource "aws_cloudwatch_metric_alarm" "db_connections" {
  alarm_name          = "rds-high-connections"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "Alert when database connections exceed 80"

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.app.id
  }
}

# Outputs
output "db_endpoint" {
  value       = aws_db_instance.app.endpoint
  description = "RDS endpoint address"
}

output "db_password_secret" {
  value       = aws_secretsmanager_secret.db_password.arn
  description = "Secret Manager ARN for database credentials"
}
```

### 3. **Database Connection and Configuration**

```bash
# Connect to RDS instance
psql -h myapp-db.xxxx.us-east-1.rds.amazonaws.com \
     -U admin \
     -d appdb \
     -p 5432

# Create database user with IAM authentication
psql -h myapp-db.xxxx.us-east-1.rds.amazonaws.com \
     -U admin \
     -d appdb << EOF
CREATE USER app_user;
GRANT CONNECT ON DATABASE appdb TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
ALTER ROLE app_user WITH PASSWORD 'MySecurePassword123!';
EOF

# Export database
pg_dump -h myapp-db.xxxx.us-east-1.rds.amazonaws.com \
        -U admin \
        appdb > backup.sql

# Import database
psql -h myapp-db.xxxx.us-east-1.rds.amazonaws.com \
     -U admin \
     appdb < backup.sql
```

## Best Practices

### ✅ DO
- Use Multi-AZ for production
- Enable automated backups
- Use encryption at rest and in transit
- Implement IAM database authentication
- Create read replicas for scaling
- Monitor performance metrics
- Set up CloudWatch alarms
- Store credentials in Secrets Manager
- Use parameter groups for configuration

### ❌ DON'T
- Store passwords in code
- Disable encryption
- Use public accessibility in production
- Ignore backup retention
- Skip automated backups
- Create databases without Multi-AZ

## Monitoring

- CloudWatch metrics (CPU, connections, storage)
- Enhanced Monitoring with OS metrics
- RDS Performance Insights
- AWS CloudTrail for API logging
- Custom CloudWatch Logs from applications

## Resources

- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [RDS Best Practices](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)
- [PostgreSQL on RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
