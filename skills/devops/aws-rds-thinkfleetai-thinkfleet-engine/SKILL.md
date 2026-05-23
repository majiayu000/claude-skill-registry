---
name: aws-rds
description: "Manage AWS RDS database instances, snapshots, and clusters."
metadata: {"thinkfleetbot":{"emoji":"🗄️","requires":{"bins":["aws","jq"],"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"]}}}
---

# AWS RDS

Manage relational database instances and clusters.

## List instances

```bash
aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,Engine:Engine,Version:EngineVersion,Status:DBInstanceStatus,Class:DBInstanceClass,Storage:AllocatedStorage}' --output table
```

## Get instance details

```bash
aws rds describe-db-instances --db-instance-identifier my-db | jq '.DBInstances[0] | {Id: .DBInstanceIdentifier, Engine, Status: .DBInstanceStatus, Endpoint: .Endpoint.Address, Port: .Endpoint.Port, MultiAZ, StorageType, AllocatedStorage}'
```

## List Aurora clusters

```bash
aws rds describe-db-clusters --query 'DBClusters[].{Id:DBClusterIdentifier,Engine:Engine,Status:Status,Endpoint:Endpoint,ReaderEndpoint:ReaderEndpoint}' --output table
```

## Create snapshot

```bash
aws rds create-db-snapshot --db-instance-identifier my-db \
  --db-snapshot-identifier my-db-snap-$(date +%Y%m%d) | jq '{SnapshotId: .DBSnapshot.DBSnapshotIdentifier, Status: .DBSnapshot.Status}'
```

## List snapshots

```bash
aws rds describe-db-snapshots --db-instance-identifier my-db --query 'DBSnapshots[].{Id:DBSnapshotIdentifier,Status:Status,Created:SnapshotCreateTime,Size:AllocatedStorage}' --output table
```

## Stop instance

```bash
aws rds stop-db-instance --db-instance-identifier my-db | jq '{Id: .DBInstance.DBInstanceIdentifier, Status: .DBInstance.DBInstanceStatus}'
```

## Start instance

```bash
aws rds start-db-instance --db-instance-identifier my-db | jq '{Id: .DBInstance.DBInstanceIdentifier, Status: .DBInstance.DBInstanceStatus}'
```

## Recent events

```bash
aws rds describe-events --source-identifier my-db --source-type db-instance --duration 1440 --query 'Events[].{Date:Date,Message:Message}' --output table
```

## Notes

- Stop/start is not available for Aurora clusters (use scaling to 0 ACUs instead).
- Snapshots are region-specific; copy cross-region for DR.
- Always confirm before stopping, deleting, or modifying instances.
