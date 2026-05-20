---
name: gcloud
description: Google Cloud CLI 操作
version: 1.0.0
author: terminal-skills
tags: [cloud, gcp, gcloud, gke, compute]
---

# Google Cloud CLI 操作

## 概述
GCP 资源管理、GKE、Cloud Functions 等技能。

## 配置与认证

```bash
# 初始化配置
gcloud init

# 登录
gcloud auth login
gcloud auth application-default login    # 应用默认凭证

# 服务账号认证
gcloud auth activate-service-account --key-file=key.json

# 查看配置
gcloud config list
gcloud config configurations list

# 设置项目
gcloud config set project my-project

# 设置区域
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# 创建配置
gcloud config configurations create my-config
gcloud config configurations activate my-config
```

## Compute Engine

### 实例管理
```bash
# 列出实例
gcloud compute instances list

# 创建实例
gcloud compute instances create my-instance \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB

# 启动/停止实例
gcloud compute instances start my-instance --zone=us-central1-a
gcloud compute instances stop my-instance --zone=us-central1-a

# 删除实例
gcloud compute instances delete my-instance --zone=us-central1-a

# SSH 连接
gcloud compute ssh my-instance --zone=us-central1-a

# 执行命令
gcloud compute ssh my-instance --zone=us-central1-a --command="uptime"
```

### 磁盘管理
```bash
# 列出磁盘
gcloud compute disks list

# 创建磁盘
gcloud compute disks create my-disk \
    --zone=us-central1-a \
    --size=100GB \
    --type=pd-ssd

# 附加磁盘
gcloud compute instances attach-disk my-instance \
    --disk=my-disk \
    --zone=us-central1-a

# 创建快照
gcloud compute disks snapshot my-disk \
    --zone=us-central1-a \
    --snapshot-names=my-snapshot
```

### 防火墙
```bash
# 列出防火墙规则
gcloud compute firewall-rules list

# 创建规则
gcloud compute firewall-rules create allow-http \
    --allow=tcp:80 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server

# 删除规则
gcloud compute firewall-rules delete allow-http
```

## Cloud Storage

```bash
# 列出桶
gsutil ls

# 创建桶
gsutil mb gs://my-bucket
gsutil mb -l us-central1 gs://my-bucket

# 上传文件
gsutil cp file.txt gs://my-bucket/
gsutil cp -r ./dir gs://my-bucket/

# 下载文件
gsutil cp gs://my-bucket/file.txt ./
gsutil cp -r gs://my-bucket/dir ./

# 同步目录
gsutil rsync -r ./local-dir gs://my-bucket/prefix/
gsutil rsync -d -r ./local-dir gs://my-bucket/prefix/    # 删除多余文件

# 删除
gsutil rm gs://my-bucket/file.txt
gsutil rm -r gs://my-bucket/dir/

# 删除桶
gsutil rb gs://my-bucket

# 设置公开访问
gsutil acl ch -u AllUsers:R gs://my-bucket/file.txt

# 生成签名 URL
gsutil signurl -d 1h key.json gs://my-bucket/file.txt
```

## GKE 集群

```bash
# 列出集群
gcloud container clusters list

# 创建集群
gcloud container clusters create my-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --machine-type=e2-medium

# 获取凭证
gcloud container clusters get-credentials my-cluster --zone=us-central1-a

# 调整节点数
gcloud container clusters resize my-cluster \
    --zone=us-central1-a \
    --num-nodes=5

# 升级集群
gcloud container clusters upgrade my-cluster \
    --zone=us-central1-a \
    --master

# 删除集群
gcloud container clusters delete my-cluster --zone=us-central1-a
```

## Cloud Functions

```bash
# 列出函数
gcloud functions list

# 部署函数
gcloud functions deploy my-function \
    --runtime=nodejs18 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point=handler \
    --source=./

# 调用函数
gcloud functions call my-function --data='{"name":"World"}'

# 查看日志
gcloud functions logs read my-function

# 删除函数
gcloud functions delete my-function
```

## Cloud Run

```bash
# 部署服务
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image \
    --platform=managed \
    --region=us-central1 \
    --allow-unauthenticated

# 列出服务
gcloud run services list

# 查看服务
gcloud run services describe my-service --region=us-central1

# 更新服务
gcloud run services update my-service \
    --region=us-central1 \
    --memory=512Mi \
    --concurrency=80

# 删除服务
gcloud run services delete my-service --region=us-central1
```

## IAM 管理

```bash
# 列出服务账号
gcloud iam service-accounts list

# 创建服务账号
gcloud iam service-accounts create my-sa \
    --display-name="My Service Account"

# 创建密钥
gcloud iam service-accounts keys create key.json \
    --iam-account=my-sa@my-project.iam.gserviceaccount.com

# 添加角色
gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:my-sa@my-project.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# 查看 IAM 策略
gcloud projects get-iam-policy my-project
```

## 常见场景

### 场景 1：批量操作实例
```bash
# 停止所有实例
gcloud compute instances list --format="value(name,zone)" | \
while read name zone; do
    gcloud compute instances stop "$name" --zone="$zone" --async
done
```

### 场景 2：日志查询
```bash
# 查看日志
gcloud logging read "resource.type=gce_instance" --limit=100

# 按时间范围
gcloud logging read "timestamp>=\"2024-01-01T00:00:00Z\"" --limit=100

# 按严重级别
gcloud logging read "severity>=ERROR" --limit=100
```

### 场景 3：导出计费数据
```bash
# 设置计费导出
gcloud beta billing accounts describe BILLING_ACCOUNT_ID

# 查看预算
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 认证失败 | `gcloud auth list` |
| 权限不足 | 检查 IAM 角色 |
| 配额超限 | `gcloud compute project-info describe` |
| API 未启用 | `gcloud services enable compute.googleapis.com` |

```bash
# 调试模式
gcloud compute instances list --verbosity=debug

# 查看帮助
gcloud help
gcloud compute instances create --help
```
