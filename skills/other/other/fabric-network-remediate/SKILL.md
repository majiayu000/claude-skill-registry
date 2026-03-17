---
name: fabric-network-remediate
description: Diagnose and resolve Microsoft Fabric network performance issues including connectivity failures, latency, private endpoints, managed VNets, outbound access protection, gateway diagnostics, OneLake endpoint routing, service tag configuration, firewall allowlisting, DNS resolution, and Spark session startup delays. Use when remediate Fabric networking, slow Spark jobs, connection timeouts, private link errors, managed private endpoint approval, or capacity throttling.
license: Complete terms in LICENSE.txt
---
# Microsoft Fabric Network Performance remediate

Systematic toolkit for diagnosing and resolving network performance issues across Microsoft Fabric workloads including Spark, OneLake, Data Warehouse, Pipelines, and Dataflows.

## When to Use This Skill

- Fabric Spark sessions take longer than expected to start (>10 seconds)
- Connection timeouts to external data sources from notebooks or pipelines
- Managed private endpoint status shows Pending or Failed
- DNS resolution returns public IPs instead of private IPs
- Outbound access protection blocks required dependencies (PyPI, Conda)
- On-premises data gateway connectivity failures
- OneLake API calls returning 403 or timeout errors
- Capacity throttling errors (HTTP 430)
- Dataflow Gen2 staging failures behind firewalls
- Cross-workspace environment attachment failures due to network mismatch

## Prerequisites

- PowerShell 7+ with Az module installed (`Install-Module Az -Scope CurrentUser`)
- Fabric Admin or Workspace Admin role for network configuration changes
- Azure portal access for Private Link Service and DNS zone management
- Network access to run `nslookup`, `Test-NetConnection`, and `Resolve-DnsName`

## Step-by-Step Workflows

### Workflow 1: Diagnose Spark Session Startup Delays

Spark startup times vary based on networking configuration. Consult the reference table:

| Scenario                                | Typical Startup Time    |
| --------------------------------------- | ----------------------- |
| Default settings, no libraries          | 5-10 seconds            |
| Default settings + library dependencies | 5-10 sec + 30 sec-5 min |
| High traffic in region, no libraries    | 2-5 minutes             |
| High traffic + library dependencies     | 2-5 min + 30 sec-5 min  |
| Network security (Private Links/VNet)   | 2-5 minutes             |
| Network security + library dependencies | 2-5 min + 30 sec-5 min  |

Run the [diagnostic script](./scripts/Test-FabricNetworkHealth.ps1) for automated assessment:

```powershell
.\scripts\Test-FabricNetworkHealth.ps1 -WorkspaceId "<workspace-id>" -CheckType SparkStartup
```

When Private Links or Managed VNets are enabled, Starter Pools are unavailable and Fabric must create clusters on demand, adding 2-5 minutes to session start time.

### Workflow 2: Validate Managed Private Endpoint Connectivity

1. Navigate to Fabric workspace **Settings > Network security**
2. Under **Managed private endpoints**, verify Status shows **Approved**
3. If Pending or Failed, see [private-endpoint-remediate.md](./references/private-endpoint-remediate.md)
4. Validate DNS routing from a Fabric Notebook:

```bash
nslookup sqlserver.corp.contoso.com
```

Confirm the returned IP is a private range (10.x.x.x or 172.x.x.x), not public.

5. Run the automated validation:

```powershell
.\scripts\Test-FabricNetworkHealth.ps1 -WorkspaceId "<workspace-id>" -CheckType PrivateEndpoint
```

### Workflow 3: Configure Firewall Allowlisting

Fabric requires specific endpoints and service tags. Run the [firewall audit script](./scripts/Test-FabricNetworkHealth.ps1):

```powershell
.\scripts\Test-FabricNetworkHealth.ps1 -CheckType FirewallEndpoints
```

For the complete endpoint reference, see [firewall-endpoints.md](./references/firewall-endpoints.md).

Key service tags for Azure Firewall / NSG rules:

| Tag              | Purpose                | Direction |
| ---------------- | ---------------------- | --------- |
| Power BI         | Fabric core services   | Both      |
| DataFactory      | Pipeline operations    | Both      |
| PowerQueryOnline | Dataflow processing    | Both      |
| SQL              | Warehouse connectivity | Outbound  |
| EventHub         | Real-Time Analytics    | Outbound  |
| KustoAnalytics   | Real-Time Analytics    | Both      |

### Workflow 4: Troubleshoot Outbound Access Protection

When outbound access protection is enabled, public repositories (PyPI, Conda) are blocked. To install libraries in secured environments:

1. Prepare a `requirements.txt` on a machine with internet access
2. Download packages and dependencies using pip:

```bash
pip download -r requirements.txt -d ./packages
```

3. Upload packages as custom libraries in the Fabric Environment
4. See [outbound-access-guide.md](./references/outbound-access-guide.md) for detailed steps

### Workflow 5: Resolve Capacity Throttling (HTTP 430)

When all Spark VCores are consumed, new jobs receive HTTP 430 errors. Formula: **1 Capacity Unit = 2 Spark VCores**.

1. Check current utilization in the Monitoring Hub
2. Cancel idle or stuck Spark sessions
3. Consider upgrading capacity SKU if sustained
4. Enable queueing for pipeline and Spark Job Definition workloads

For queue limits by SKU, see [capacity-throttling.md](./references/capacity-throttling.md).

## remediate Quick Reference

| Symptom                       | Likely Cause                    | First Action                            |
| ----------------------------- | ------------------------------- | --------------------------------------- |
| Spark startup >2 min          | Private Link/VNet enabled       | Expected; Starter Pools unavailable     |
| Connection timeout from Spark | Firewall blocking Fabric subnet | Open required ports (1433 for SQL)      |
| DNS resolves to public IP     | Private DNS zone not linked     | Add A record pointing to private IP     |
| MPE status = Failed           | PLS rejected or deleted         | Re-create MPE, verify PLS exists        |
| HTTP 430 error                | Capacity VCores exhausted       | Cancel jobs or upgrade SKU              |
| PyPI install blocked          | Outbound access protection      | Upload packages as custom libraries     |
| Cross-workspace env fails     | Network settings mismatch       | Ensure same capacity and network config |
| OneLake API 403               | Endpoint URL validation         | Use `*.dfs.fabric.microsoft.com`      |

## References

- [Private Endpoint remediate](./references/private-endpoint-remediate.md)
- [Firewall Endpoints and Allowlist](./references/firewall-endpoints.md)
- [Outbound Access Protection Guide](./references/outbound-access-guide.md)
- [Capacity Throttling and Queue Limits](./references/capacity-throttling.md)
- [Diagnostic Report Template](./templates/network-diagnostic-report.md)
