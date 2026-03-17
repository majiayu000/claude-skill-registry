---
name: aws-cli
description: AWS CLI 操作
version: 1.0.0
author: terminal-skills
tags: [cloud, aws, cli, ec2, s3, iam]
---

# AWS CLI 操作

## 概述
EC2、S3、IAM、Lambda 等 AWS 服务的命令行操作技能。

## 配置与认证

```bash
# 配置凭证
aws configure
aws configure --profile myprofile

# 查看配置
aws configure list
aws configure list --profile myprofile

# 配置文件位置
~/.aws/credentials
~/.aws/config

# 使用环境变量
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_DEFAULT_REGION=us-east-1

# 使用 profile
export AWS_PROFILE=myprofile
aws s3 ls --profile myprofile

# 获取当前身份
aws sts get-caller-identity
```

## EC2 实例

### 实例管理
```bash
# 列出实例
aws ec2 describe-instances
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]' --output table

# 启动/停止实例
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0

# 终止实例
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# 创建实例
aws ec2 run-instances \
    --image-id ami-12345678 \
    --instance-type t3.micro \
    --key-name my-key \
    --security-group-ids sg-12345678 \
    --subnet-id subnet-12345678 \
    --count 1
```

### 安全组
```bash
# 列出安全组
aws ec2 describe-security-groups
aws ec2 describe-security-groups --group-ids sg-12345678

# 创建安全组
aws ec2 create-security-group \
    --group-name my-sg \
    --description "My security group" \
    --vpc-id vpc-12345678

# 添加入站规则
aws ec2 authorize-security-group-ingress \
    --group-id sg-12345678 \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# 删除规则
aws ec2 revoke-security-group-ingress \
    --group-id sg-12345678 \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0
```

## S3 存储

### 基础操作
```bash
# 列出桶
aws s3 ls

# 列出对象
aws s3 ls s3://bucket-name/
aws s3 ls s3://bucket-name/prefix/ --recursive

# 创建桶
aws s3 mb s3://bucket-name
aws s3 mb s3://bucket-name --region us-west-2

# 删除桶
aws s3 rb s3://bucket-name
aws s3 rb s3://bucket-name --force    # 包括内容
```

### 文件操作
```bash
# 上传文件
aws s3 cp file.txt s3://bucket-name/
aws s3 cp file.txt s3://bucket-name/path/file.txt

# 下载文件
aws s3 cp s3://bucket-name/file.txt ./
aws s3 cp s3://bucket-name/path/ ./ --recursive

# 同步目录
aws s3 sync ./local-dir s3://bucket-name/prefix/
aws s3 sync s3://bucket-name/prefix/ ./local-dir
aws s3 sync ./local-dir s3://bucket-name/ --delete    # 删除目标多余文件

# 删除对象
aws s3 rm s3://bucket-name/file.txt
aws s3 rm s3://bucket-name/prefix/ --recursive

# 移动/重命名
aws s3 mv s3://bucket-name/old.txt s3://bucket-name/new.txt
```

### 高级操作
```bash
# 预签名 URL
aws s3 presign s3://bucket-name/file.txt --expires-in 3600

# 设置公开访问
aws s3api put-object-acl --bucket bucket-name --key file.txt --acl public-read

# 查看桶策略
aws s3api get-bucket-policy --bucket bucket-name

# 设置生命周期
aws s3api put-bucket-lifecycle-configuration \
    --bucket bucket-name \
    --lifecycle-configuration file://lifecycle.json
```

## IAM 管理

```bash
# 列出用户
aws iam list-users

# 创建用户
aws iam create-user --user-name myuser

# 创建访问密钥
aws iam create-access-key --user-name myuser

# 附加策略
aws iam attach-user-policy \
    --user-name myuser \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# 列出角色
aws iam list-roles

# 获取角色
aws iam get-role --role-name myrole
```

## Lambda 函数

```bash
# 列出函数
aws lambda list-functions

# 调用函数
aws lambda invoke \
    --function-name my-function \
    --payload '{"key": "value"}' \
    output.json

# 查看函数配置
aws lambda get-function --function-name my-function

# 更新函数代码
aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://function.zip

# 查看日志
aws logs filter-log-events \
    --log-group-name /aws/lambda/my-function \
    --start-time $(date -d '1 hour ago' +%s)000
```

## EKS 集群

```bash
# 列出集群
aws eks list-clusters

# 获取集群信息
aws eks describe-cluster --name my-cluster

# 更新 kubeconfig
aws eks update-kubeconfig --name my-cluster --region us-east-1

# 列出节点组
aws eks list-nodegroups --cluster-name my-cluster
```

## 常见场景

### 场景 1：批量操作实例
```bash
# 获取所有运行中实例 ID
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running" \
    --query 'Reservations[*].Instances[*].InstanceId' \
    --output text

# 批量停止
aws ec2 stop-instances --instance-ids $(aws ec2 describe-instances \
    --filters "Name=tag:Environment,Values=dev" \
    --query 'Reservations[*].Instances[*].InstanceId' \
    --output text)
```

### 场景 2：S3 大文件传输
```bash
# 多部分上传（自动）
aws s3 cp large-file.zip s3://bucket-name/ \
    --storage-class STANDARD_IA

# 配置传输加速
aws s3api put-bucket-accelerate-configuration \
    --bucket bucket-name \
    --accelerate-configuration Status=Enabled
```

### 场景 3：查询 CloudWatch 日志
```bash
# 查询日志
aws logs filter-log-events \
    --log-group-name /aws/lambda/my-function \
    --filter-pattern "ERROR" \
    --start-time $(date -d '1 hour ago' +%s)000

# 实时跟踪
aws logs tail /aws/lambda/my-function --follow
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 认证失败 | `aws sts get-caller-identity` |
| 权限不足 | 检查 IAM 策略 |
| 区域错误 | 检查 `--region` 参数 |
| 超时 | 检查网络、增加超时设置 |

```bash
# 调试模式
aws s3 ls --debug

# 检查配置
aws configure list
```
