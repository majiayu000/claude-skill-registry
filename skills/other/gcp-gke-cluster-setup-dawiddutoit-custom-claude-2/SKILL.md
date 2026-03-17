---
name: gcp-gke-cluster-setup
description: |
  Sets up and configures Google Kubernetes Engine (GKE) clusters for production use. Use when creating new GKE clusters, choosing between Autopilot vs Standard modes, configuring networking (VPC-native, private clusters), setting up node pools, or planning cluster architecture for Spring Boot microservices. Includes regional vs zonal decisions, security hardening, and resource provisioning guidance.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# GKE Cluster Setup

## Purpose

Create production-ready GKE clusters with proper architecture, networking, and security configurations. This skill guides you through cluster creation, mode selection (Autopilot vs Standard), networking setup, and initial resource configuration.

## When to Use

Use this skill when you need to:
- Create a new GKE cluster for production or development
- Choose between Autopilot and Standard cluster modes
- Configure VPC-native networking and private clusters
- Set up node pools with autoscaling
- Enable security features (Workload Identity, private nodes)
- Plan cluster architecture for Spring Boot microservices

Trigger phrases: "create GKE cluster", "set up Kubernetes cluster", "Autopilot vs Standard", "configure GKE networking"

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Decide Between Autopilot and Standard](#step-1-decide-between-autopilot-and-standard)
  - [Step 2: Select Cluster Type](#step-2-select-cluster-type-regional-vs-zonal)
  - [Step 3: Configure Networking](#step-3-configure-networking-vpc-native-required)
  - [Step 4: Enable Security Features](#step-4-enable-security-features)
  - [Step 5: Configure Node Pools](#step-5-configure-node-pools-standard-only)
  - [Step 6: Enable Monitoring and Logging](#step-6-enable-monitoring-and-logging)
  - [Step 7: Get Credentials and Verify](#step-7-get-credentials-and-verify)
- [Examples](#examples)
- [Requirements](#requirements)
- [See Also](#see-also)

## Quick Start

Choose your cluster mode and create it:

```bash
# GKE Autopilot (Recommended for most use cases)
gcloud container clusters create-auto CLUSTER_NAME \
  --region=europe-west2 \
  --enable-ip-alias

# GKE Standard (if you need node control)
gcloud container clusters create CLUSTER_NAME \
  --region=europe-west2 \
  --enable-ip-alias \
  --machine-type=n2-standard-4 \
  --num-nodes=3
```

## Instructions

### Step 1: Decide Between Autopilot and Standard

**Choose Autopilot if:**
- You have Spring Boot microservices (stateless, scalable)
- You want Google to manage nodes and security
- You benefit from per-pod billing (variable workloads)
- Team focuses on application development, not infrastructure
- You need rapid scaling and cost optimization

**Choose Standard if:**
- You need full control over node configuration
- You have specific infrastructure requirements
- You need custom kernel or privileged containers
- You have dedicated Kubernetes operations expertise

**Recommendation:** Use Autopilot for most new GKE deployments. It provides 99.9% SLA, automatic security patching, and cost savings up to 60%.

### Step 2: Select Cluster Type (Regional vs Zonal)

**Regional (Production Recommended):**
```bash
# 99.95% SLA for control plane
# Control plane and nodes distributed across multiple zones
gcloud container clusters create-auto CLUSTER_NAME \
  --region=europe-west2  # Distributes across a, b, c zones
```

**Zonal (Development/Test Only):**
```bash
# 99.5% SLA, single point of failure
# Use only for non-critical environments
gcloud container clusters create-auto CLUSTER_NAME \
  --zone=europe-west2-a
```

### Step 3: Configure Networking (VPC-Native Required)

All production clusters must be VPC-native with proper IP allocation:

```bash
gcloud container clusters create-auto CLUSTER_NAME \
  --region=europe-west2 \
  --network=wtr-vpc \
  --subnetwork=wtr-cluster-subnet \
  --enable-ip-alias \
  --cluster-secondary-range-name=pods \
  --services-secondary-range-name=services
```

**IP Ranges (Example):**
- Primary (Nodes): `10.0.0.0/24`
- Secondary Pods: `10.1.0.0/16`
- Secondary Services: `10.2.0.0/20`

### Step 4: Enable Security Features

```bash
gcloud container clusters create-auto CLUSTER_NAME \
  --region=europe-west2 \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.0/28 \
  --enable-master-authorized-networks \
  --master-authorized-networks=203.0.113.0/24
```

**Security Features:**
- Private nodes (no public IPs)
- Private endpoint (kubectl only from VPC)
- Workload Identity enabled by default
- Shielded nodes enabled by default

### Step 5: Configure Node Pools (Standard Only)

For GKE Standard, create specialized node pools:

```bash
# Production workloads
gcloud container node-pools create production-pool \
  --cluster=CLUSTER_NAME \
  --region=europe-west2 \
  --machine-type=n2-standard-4 \
  --num-nodes=3 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=10

# Batch/non-critical workloads (optional)
gcloud container node-pools create batch-pool \
  --cluster=CLUSTER_NAME \
  --region=europe-west2 \
  --machine-type=n2-standard-2 \
  --spot  # Up to 91% cheaper
```

### Step 6: Enable Monitoring and Logging

```bash
gcloud container clusters update CLUSTER_NAME \
  --region=europe-west2 \
  --logging=SYSTEM,WORKLOAD \
  --monitoring=SYSTEM,WORKLOAD \
  --enable-cloud-logging \
  --enable-cloud-monitoring \
  --enable-managed-prometheus
```

### Step 7: Get Credentials and Verify

```bash
# Get kubectl credentials
gcloud container clusters get-credentials CLUSTER_NAME \
  --region=europe-west2 \
  --project=PROJECT_ID

# Verify cluster access
kubectl cluster-info
kubectl get nodes
```

## Examples

### Example 1: Production Autopilot Cluster

```bash
#!/bin/bash
# Create production-ready Autopilot cluster for Supplier Charges Hub

CLUSTER_NAME="supplier-charges-production"
REGION="europe-west2"
PROJECT_ID="ecp-wtr-supplier-charges-prod"
NETWORK="wtr-vpc"
SUBNET="wtr-prod-subnet"

gcloud container clusters create-auto $CLUSTER_NAME \
  --region=$REGION \
  --project=$PROJECT_ID \
  --network=$NETWORK \
  --subnetwork=$SUBNET \
  --enable-ip-alias \
  --cluster-secondary-range-name=pods \
  --services-secondary-range-name=services \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.0/28 \
  --enable-master-authorized-networks \
  --master-authorized-networks=203.0.113.0/24 \
  --logging=SYSTEM,WORKLOAD \
  --monitoring=SYSTEM,WORKLOAD \
  --release-channel=regular \
  --enable-managed-prometheus

# Get credentials
gcloud container clusters get-credentials $CLUSTER_NAME \
  --region=$REGION \
  --project=$PROJECT_ID

# Verify
kubectl cluster-info
```

### Example 2: Development Zonal Cluster

```bash
# Quick dev/test cluster (lower cost, single zone)
gcloud container clusters create-auto dev-cluster \
  --zone=europe-west2-a \
  --project=ecp-wtr-supplier-charges-labs
```

### Example 3: GKE Standard with Multiple Node Pools

```bash
# Create Standard cluster
gcloud container clusters create managed-cluster \
  --region=europe-west2 \
  --machine-type=n2-standard-4 \
  --num-nodes=3 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=10 \
  --enable-ip-alias \
  --network=wtr-vpc \
  --subnetwork=wtr-cluster-subnet

# Add specialized batch node pool
gcloud container node-pools create batch-pool \
  --cluster=managed-cluster \
  --region=europe-west2 \
  --machine-type=n2-highmem-8 \
  --spot \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=20
```

## Requirements

- `gcloud` CLI configured with appropriate project and permissions
- GCP project with GKE API enabled: `gcloud services enable container.googleapis.com`
- VPC and subnets already created with secondary IP ranges
- For private clusters: authorized networks configured (your office IP range)
- IAM role: `roles/container.admin` or `roles/container.clusterManager`

## See Also

- [gcp-gke-workload-identity](../gcp-gke-workload-identity/SKILL.md) - Set up secure service-to-service authentication
- [gcp-gke-deployment-strategies](../gcp-gke-deployment-strategies/SKILL.md) - Deploy and update applications
- [gcp-gke-troubleshooting](../gcp-gke-troubleshooting/SKILL.md) - Diagnose and fix cluster issues
