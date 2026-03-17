---
name: "AWS Cloud Infrastructure"
description: "Deploy Node.js applications on AWS using EC2, RDS, and managed services with security best practices. Apply when setting up AWS infrastructure, configuring databases, managing security, or optimizing costs."
allowed-tools: Read, Write, Edit, Bash
version: 1.1.0
updated: 2026-01-15
compatibility: Claude Opus 4.5, Claude Code v2.x
---

# AWS Cloud Infrastructure

Systematic AWS deployment for Node.js applications ensuring scalability, security, and cost efficiency.

## Overview

This Skill enforces:
- EC2 instance configuration and security
- RDS (Relational Database Service) setup
- IAM roles and least-privilege access
- Environment variable and secrets management
- Auto-scaling and load balancing
- Security group and network configuration
- CloudWatch monitoring

Apply when deploying to AWS, configuring databases, or managing cloud infrastructure.

## Deployment Workflow

**Every AWS deployment follows this process**:

```
Step 1: Create EC2 Instance
  ↓
Step 2: Configure Security Groups
  ↓
Step 3: Install Node.js and dependencies
  ↓
Step 4: Deploy application with PM2
  ↓
Step 5: Set up RDS database
  ↓
Step 6: Configure environment variables
  ↓
Step 7: Set up monitoring and scaling
```

## Step 1: EC2 Instance Setup

### Launch EC2 Instance

```bash
# Using AWS CLI
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name your-key-pair \
  --security-groups your-security-group
```

### Instance Types by Use Case

- **Development**: t3.micro (free tier eligible)
- **Production**: m5.large or c5.xlarge (more CPU/memory)
- **High-traffic**: c6i.2xlarge or m6i.2xlarge

### SSH into Instance

```bash
ssh -i "your-key.pem" ubuntu@<ec2-public-ip>
```

### Install Node.js and Dependencies

```bash
sudo apt update
sudo apt install nodejs npm nginx git curl -y

# Install NVM for Node version management
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Load NVM
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"

# Install Node 20 (LTS)
nvm install 20
nvm use 20
```

## Step 2: Security Groups Configuration

### Configure Security Group Rules

```
Inbound Rules:
- SSH (port 22): Only from your IP
- HTTP (port 80): From 0.0.0.0/0
- HTTPS (port 443): From 0.0.0.0/0
- Custom TCP (your app port): From Load Balancer

Outbound Rules:
- Allow all traffic
```

### Using AWS CLI

```bash
# Allow SSH from specific IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP/32

# Allow HTTP
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Allow HTTPS
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

## Step 3: Deploy Application

### Clone Repository and Install Dependencies

```bash
git clone https://github.com/your-repo/project.git
cd project

npm ci  # Install exact versions from package-lock.json
```

### Setup Environment Variables

```bash
# Create .env file
cat > .env << EOF
NODE_ENV=production
DATABASE_URL=postgresql://user:password@your-rds-endpoint:5432/dbname
PORT=3000
EOF

# Verify .env is not committed
cat .gitignore | grep .env
```

### Install PM2 Process Manager

```bash
npm install -g pm2

# Start application
pm2 start npm --name "myapp" -- start

# Save PM2 process list to restart on reboot
pm2 startup
pm2 save
```

### Verify Application Running

```bash
curl http://localhost:3000
```

## Step 4: Set Up Nginx Reverse Proxy

### Configure Nginx

```nginx
# /etc/nginx/sites-available/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable and Test Nginx

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
sudo nginx -t  # Test configuration
```

## Step 5: RDS Database Setup

### Create RDS Instance

```bash
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourPasswordHere \
  --allocated-storage 20 \
  --publicly-accessible false
```

### Configure RDS Security Group

```bash
# Allow EC2 to access RDS
aws ec2 authorize-security-group-ingress \
  --group-id sg-rds-xxxxx \
  --protocol tcp \
  --port 5432 \
  --source-security-group-id sg-ec2-xxxxx
```

### Get RDS Endpoint

```bash
aws rds describe-db-instances \
  --db-instance-identifier mydb \
  --query 'DBInstances[0].Endpoint.Address'
```

### Connect to RDS

```bash
psql -h mydb.xxxxxx.us-east-1.rds.amazonaws.com \
     -U admin \
     -d postgres
```

## Step 6: Secrets Management

### MUST NOT: Hardcode Secrets

Use AWS Secrets Manager or Parameter Store:

```bash
# Store in Secrets Manager
aws secretsmanager create-secret \
  --name prod/database/password \
  --secret-string YourSecurePassword

# Retrieve secret
aws secretsmanager get-secret-value \
  --secret-id prod/database/password
```

### Environment Variable Best Practices

```ts
// ✅ GOOD: Use environment variables
const dbPassword = process.env.DATABASE_PASSWORD;
const apiKey = process.env.API_KEY;

// ❌ BAD: Hardcoded secrets
const dbPassword = 'MyPassword123';
const apiKey = 'sk-1234567890';
```

### IAM Role for EC2

```bash
# Create IAM role with least privilege
aws iam create-role \
  --role-name EC2-App-Role \
  --assume-role-policy-document file://trust-policy.json

# Attach policy to access RDS and Secrets Manager
aws iam attach-role-policy \
  --role-name EC2-App-Role \
  --policy-arn arn:aws:iam::aws:policy/AmazonRDSReadOnlyAccess
```

## Step 7: Monitoring and Logging

### CloudWatch Configuration

```bash
# View application logs
pm2 logs myapp

# Configure CloudWatch Logs
sudo apt install awslogs -y

# Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time 2025-11-13T00:00:00Z \
  --end-time 2025-11-13T01:00:00Z \
  --period 300 \
  --statistics Average
```

## Auto-Scaling and Load Balancing

### Create Load Balancer

```bash
aws elbv2 create-load-balancer \
  --name my-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx
```

### Auto Scaling Group

```bash
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name myapp-asg \
  --launch-configuration-name myapp-lc \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 2 \
  --load-balancer-names my-lb
```

## HTTPS with Let's Encrypt

### Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renew setup
sudo systemctl enable certbot.timer
```

### Configure Nginx for HTTPS

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        # ... proxy settings ...
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## Anti-Patterns

```bash
# ❌ BAD: SSH access from anywhere
--cidr 0.0.0.0/0  # Port 22 open to world

# ❌ BAD: Hardcoded credentials
DATABASE_URL=postgresql://user:password@host:5432/db

# ❌ BAD: Public RDS instance
--publicly-accessible true

# ❌ BAD: No backup configuration
# No automated snapshots enabled

# ❌ BAD: Single instance (no redundancy)
# No load balancing or auto-scaling

# ❌ BAD: No monitoring
# No CloudWatch alarms or logging
```

## Verification Before Production

- [ ] EC2 instance launched and accessible
- [ ] Security groups configured (SSH limited, HTTP/HTTPS open)
- [ ] Node.js installed and application running with PM2
- [ ] Nginx reverse proxy working
- [ ] RDS instance created and accessible from EC2
- [ ] Environment variables configured (not hardcoded)
- [ ] Secrets in AWS Secrets Manager or Parameter Store
- [ ] IAM roles with least-privilege access
- [ ] SSL/TLS certificate installed
- [ ] CloudWatch monitoring enabled
- [ ] Backups configured
- [ ] Auto-scaling groups set up
- [ ] Load balancer distributing traffic

## Common Commands

```bash
# Check application status
pm2 status

# View application logs
pm2 logs myapp

# Restart application
pm2 restart myapp

# Stop application
pm2 stop myapp

# Reload (graceful restart)
pm2 reload myapp

# Monitor resources
pm2 monit

# Check nginx status
sudo systemctl status nginx

# Reload nginx configuration
sudo systemctl reload nginx

# Monitor system resources
htop
```

## Integration with Project Standards

Enforces security best practices:
- S-5: Secrets in environment variables
- S-1: Encryption in transit (HTTPS)
- No hardcoded credentials
- IAM least-privilege access
- Security group whitelisting
- Monitoring and logging

## Resources

- AWS EC2: https://docs.aws.amazon.com/ec2
- AWS RDS: https://docs.aws.amazon.com/rds
- PM2 Documentation: https://pm2.keymetrics.io
- Nginx Reverse Proxy: https://nginx.org/en/docs

---

**Last Updated:** January 15, 2026
**Version:** 1.1.0
**Status:** Production Ready ✅

> **January 2026 Note:** This skill has been updated for compatibility with Claude Code v2.x and Claude Opus 4.5. For complex infrastructure planning, use Claude Opus 4.5 with `effort: high` to get comprehensive deployment strategies.
