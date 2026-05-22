---
name: aliyun-cli
description: 阿里云 CLI 操作
version: 1.0.0
author: terminal-skills
tags: [cloud, aliyun, cli, ecs, oss, rds]
---

# 阿里云 CLI 操作

## 概述
阿里云 ECS、OSS、RDS 等服务的命令行操作技能。

## 配置与认证

```bash
# 配置凭证
aliyun configure
aliyun configure --profile myprofile

# 交互式配置
# Access Key ID: xxx
# Access Key Secret: xxx
# Default Region Id: cn-hangzhou
# Default Output Format: json

# 查看配置
aliyun configure list

# 使用 profile
aliyun ecs DescribeInstances --profile myprofile

# 环境变量
export ALICLOUD_ACCESS_KEY=xxx
export ALICLOUD_SECRET_KEY=xxx
export ALICLOUD_REGION=cn-hangzhou
```

## ECS 实例

### 实例管理
```bash
# 列出实例
aliyun ecs DescribeInstances
aliyun ecs DescribeInstances --RegionId cn-hangzhou

# 按状态过滤
aliyun ecs DescribeInstances --Status Running

# 查看实例详情
aliyun ecs DescribeInstanceAttribute --InstanceId i-xxx

# 启动实例
aliyun ecs StartInstance --InstanceId i-xxx

# 停止实例
aliyun ecs StopInstance --InstanceId i-xxx
aliyun ecs StopInstance --InstanceId i-xxx --ForceStop true

# 重启实例
aliyun ecs RebootInstance --InstanceId i-xxx

# 删除实例
aliyun ecs DeleteInstance --InstanceId i-xxx --Force true
```

### 创建实例
```bash
# 创建实例
aliyun ecs CreateInstance \
    --RegionId cn-hangzhou \
    --ImageId ubuntu_22_04_x64_20G_alibase_20230907.vhd \
    --InstanceType ecs.t6-c1m1.large \
    --SecurityGroupId sg-xxx \
    --VSwitchId vsw-xxx \
    --InstanceName my-instance \
    --InternetChargeType PayByTraffic \
    --InternetMaxBandwidthOut 5

# 分配公网 IP
aliyun ecs AllocatePublicIpAddress --InstanceId i-xxx
```

### 安全组
```bash
# 列出安全组
aliyun ecs DescribeSecurityGroups --RegionId cn-hangzhou

# 创建安全组
aliyun ecs CreateSecurityGroup \
    --RegionId cn-hangzhou \
    --VpcId vpc-xxx \
    --SecurityGroupName my-sg

# 添加入方向规则
aliyun ecs AuthorizeSecurityGroup \
    --SecurityGroupId sg-xxx \
    --IpProtocol tcp \
    --PortRange 22/22 \
    --SourceCidrIp 0.0.0.0/0

# 删除规则
aliyun ecs RevokeSecurityGroup \
    --SecurityGroupId sg-xxx \
    --IpProtocol tcp \
    --PortRange 22/22 \
    --SourceCidrIp 0.0.0.0/0
```

## OSS 存储

### ossutil 工具
```bash
# 配置
ossutil config

# 列出桶
ossutil ls

# 创建桶
ossutil mb oss://my-bucket

# 上传文件
ossutil cp file.txt oss://my-bucket/
ossutil cp -r ./dir oss://my-bucket/dir/

# 下载文件
ossutil cp oss://my-bucket/file.txt ./
ossutil cp -r oss://my-bucket/dir/ ./dir/

# 同步目录
ossutil sync ./local-dir oss://my-bucket/prefix/
ossutil sync oss://my-bucket/prefix/ ./local-dir

# 删除文件
ossutil rm oss://my-bucket/file.txt
ossutil rm -r oss://my-bucket/dir/

# 删除桶
ossutil rb oss://my-bucket

# 生成签名 URL
ossutil sign oss://my-bucket/file.txt --timeout 3600
```

### OSS API
```bash
# 列出桶
aliyun oss ListBuckets

# 列出对象
aliyun oss ListObjects --BucketName my-bucket

# 获取桶信息
aliyun oss GetBucketInfo --BucketName my-bucket
```

## RDS 数据库

```bash
# 列出实例
aliyun rds DescribeDBInstances --RegionId cn-hangzhou

# 查看实例详情
aliyun rds DescribeDBInstanceAttribute --DBInstanceId rm-xxx

# 创建实例
aliyun rds CreateDBInstance \
    --RegionId cn-hangzhou \
    --Engine MySQL \
    --EngineVersion 8.0 \
    --DBInstanceClass rds.mysql.s2.large \
    --DBInstanceStorage 100 \
    --DBInstanceNetType Intranet \
    --PayType Postpaid

# 创建数据库
aliyun rds CreateDatabase \
    --DBInstanceId rm-xxx \
    --DBName mydb \
    --CharacterSetName utf8mb4

# 创建账号
aliyun rds CreateAccount \
    --DBInstanceId rm-xxx \
    --AccountName admin \
    --AccountPassword 'MyPassword123!' \
    --AccountType Super

# 重启实例
aliyun rds RestartDBInstance --DBInstanceId rm-xxx
```

## ACK 容器服务

```bash
# 列出集群
aliyun cs DescribeClusters

# 获取集群详情
aliyun cs DescribeClusterDetail --ClusterId c-xxx

# 获取 kubeconfig
aliyun cs DescribeClusterUserKubeconfig --ClusterId c-xxx

# 扩容节点
aliyun cs ScaleCluster \
    --ClusterId c-xxx \
    --size 5
```

## SLB 负载均衡

```bash
# 列出实例
aliyun slb DescribeLoadBalancers --RegionId cn-hangzhou

# 创建实例
aliyun slb CreateLoadBalancer \
    --RegionId cn-hangzhou \
    --LoadBalancerName my-slb \
    --AddressType internet \
    --LoadBalancerSpec slb.s1.small

# 添加后端服务器
aliyun slb AddBackendServers \
    --LoadBalancerId lb-xxx \
    --BackendServers '[{"ServerId":"i-xxx","Weight":"100"}]'

# 创建监听
aliyun slb CreateLoadBalancerTCPListener \
    --LoadBalancerId lb-xxx \
    --ListenerPort 80 \
    --BackendServerPort 80 \
    --Bandwidth -1
```

## 常见场景

### 场景 1：批量操作实例
```bash
# 获取所有运行中实例
aliyun ecs DescribeInstances --Status Running \
    --output cols=InstanceId rows=Instances.Instance[]

# 批量停止
for id in $(aliyun ecs DescribeInstances --Status Running \
    --output cols=InstanceId rows=Instances.Instance[] | tail -n +2); do
    aliyun ecs StopInstance --InstanceId $id
done
```

### 场景 2：监控数据查询
```bash
# 查询 CPU 使用率
aliyun cms DescribeMetricLast \
    --Namespace acs_ecs_dashboard \
    --MetricName CPUUtilization \
    --Dimensions '[{"instanceId":"i-xxx"}]'
```

### 场景 3：日志查询
```bash
# 查询 SLS 日志
aliyun sls GetLogs \
    --project my-project \
    --logstore my-logstore \
    --from $(date -d '1 hour ago' +%s) \
    --to $(date +%s) \
    --query "* | select *"
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 认证失败 | 检查 AccessKey 配置 |
| 权限不足 | 检查 RAM 策略 |
| 区域错误 | 检查 RegionId |
| 配额超限 | 查看配额管理 |

```bash
# 调试模式
aliyun ecs DescribeInstances --debug

# 查看帮助
aliyun help
aliyun ecs DescribeInstances help
```
