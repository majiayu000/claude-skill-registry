---
name: azure-cli
description: Azure CLI 操作
version: 1.0.0
author: terminal-skills
tags: [cloud, azure, cli, vm, storage, aks]
---

# Azure CLI 操作

## 概述
Azure 资源管理、AKS、存储操作等技能。

## 配置与认证

```bash
# 登录
az login
az login --use-device-code          # 设备代码登录
az login --service-principal -u <app-id> -p <password> --tenant <tenant-id>

# 查看账户
az account show
az account list --output table

# 切换订阅
az account set --subscription "subscription-name"
az account set --subscription "subscription-id"

# 查看当前配置
az configure --list-defaults

# 设置默认值
az configure --defaults group=myResourceGroup location=eastus
```

## 资源组

```bash
# 列出资源组
az group list --output table

# 创建资源组
az group create --name myResourceGroup --location eastus

# 删除资源组
az group delete --name myResourceGroup --yes --no-wait

# 查看资源组中的资源
az resource list --resource-group myResourceGroup --output table
```

## 虚拟机

### VM 管理
```bash
# 列出 VM
az vm list --output table
az vm list --resource-group myResourceGroup --output table

# 创建 VM
az vm create \
    --resource-group myResourceGroup \
    --name myVM \
    --image Ubuntu2204 \
    --admin-username azureuser \
    --generate-ssh-keys \
    --size Standard_B2s

# 启动/停止 VM
az vm start --resource-group myResourceGroup --name myVM
az vm stop --resource-group myResourceGroup --name myVM
az vm deallocate --resource-group myResourceGroup --name myVM
az vm restart --resource-group myResourceGroup --name myVM

# 删除 VM
az vm delete --resource-group myResourceGroup --name myVM --yes

# 查看 VM 详情
az vm show --resource-group myResourceGroup --name myVM
az vm get-instance-view --resource-group myResourceGroup --name myVM
```

### VM 操作
```bash
# 获取公网 IP
az vm list-ip-addresses --resource-group myResourceGroup --name myVM --output table

# 打开端口
az vm open-port --resource-group myResourceGroup --name myVM --port 80

# 调整大小
az vm resize --resource-group myResourceGroup --name myVM --size Standard_D4s_v3

# 运行命令
az vm run-command invoke \
    --resource-group myResourceGroup \
    --name myVM \
    --command-id RunShellScript \
    --scripts "apt-get update && apt-get install -y nginx"
```

## 存储账户

### 账户管理
```bash
# 列出存储账户
az storage account list --output table

# 创建存储账户
az storage account create \
    --name mystorageaccount \
    --resource-group myResourceGroup \
    --location eastus \
    --sku Standard_LRS

# 获取连接字符串
az storage account show-connection-string \
    --name mystorageaccount \
    --resource-group myResourceGroup

# 获取密钥
az storage account keys list \
    --account-name mystorageaccount \
    --resource-group myResourceGroup
```

### Blob 操作
```bash
# 设置环境变量
export AZURE_STORAGE_CONNECTION_STRING="..."

# 创建容器
az storage container create --name mycontainer

# 列出容器
az storage container list --output table

# 上传文件
az storage blob upload \
    --container-name mycontainer \
    --name myblob \
    --file ./local-file.txt

# 下载文件
az storage blob download \
    --container-name mycontainer \
    --name myblob \
    --file ./downloaded-file.txt

# 列出 blob
az storage blob list --container-name mycontainer --output table

# 删除 blob
az storage blob delete --container-name mycontainer --name myblob

# 生成 SAS URL
az storage blob generate-sas \
    --container-name mycontainer \
    --name myblob \
    --permissions r \
    --expiry 2024-12-31 \
    --full-uri
```

## AKS 集群

```bash
# 列出集群
az aks list --output table

# 创建集群
az aks create \
    --resource-group myResourceGroup \
    --name myAKSCluster \
    --node-count 3 \
    --node-vm-size Standard_D2s_v3 \
    --generate-ssh-keys

# 获取凭证
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

# 查看集群
az aks show --resource-group myResourceGroup --name myAKSCluster

# 扩缩节点
az aks scale \
    --resource-group myResourceGroup \
    --name myAKSCluster \
    --node-count 5

# 升级集群
az aks get-upgrades --resource-group myResourceGroup --name myAKSCluster
az aks upgrade --resource-group myResourceGroup --name myAKSCluster --kubernetes-version 1.28.0

# 删除集群
az aks delete --resource-group myResourceGroup --name myAKSCluster --yes
```

## App Service

```bash
# 列出 App Service 计划
az appservice plan list --output table

# 创建 App Service 计划
az appservice plan create \
    --name myAppServicePlan \
    --resource-group myResourceGroup \
    --sku B1 \
    --is-linux

# 创建 Web App
az webapp create \
    --resource-group myResourceGroup \
    --plan myAppServicePlan \
    --name myWebApp \
    --runtime "NODE:18-lts"

# 部署代码
az webapp deployment source config-zip \
    --resource-group myResourceGroup \
    --name myWebApp \
    --src app.zip

# 查看日志
az webapp log tail --resource-group myResourceGroup --name myWebApp
```

## 常见场景

### 场景 1：批量操作资源
```bash
# 列出所有 VM 并停止
az vm list --query "[].{name:name, rg:resourceGroup}" -o tsv | \
while read name rg; do
    az vm deallocate --resource-group "$rg" --name "$name" --no-wait
done
```

### 场景 2：导出资源模板
```bash
# 导出资源组模板
az group export --name myResourceGroup > template.json

# 部署模板
az deployment group create \
    --resource-group myResourceGroup \
    --template-file template.json \
    --parameters @parameters.json
```

### 场景 3：监控与日志
```bash
# 查看活动日志
az monitor activity-log list \
    --resource-group myResourceGroup \
    --start-time 2024-01-01 \
    --output table

# 查看指标
az monitor metrics list \
    --resource /subscriptions/.../resourceGroups/.../providers/Microsoft.Compute/virtualMachines/myVM \
    --metric "Percentage CPU" \
    --interval PT1H
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 登录失败 | `az login --use-device-code` |
| 权限不足 | 检查 RBAC 角色分配 |
| 资源找不到 | 检查订阅、资源组 |
| 配额超限 | `az vm list-usage --location eastus` |

```bash
# 调试模式
az vm list --debug

# 查看帮助
az vm --help
az vm create --help
```
