---
name: azure-caf-naming-abbreviations
description: Cloud Adoption Framework (CAF) abbreviation reference for Azure resources. Use when naming or validating during code reviews Azure resources in IaC (ex. Terraform, Terragrunt, etc), pipelines, documentation to ensure naming compliance.
---

# CAF Abbreviation recommendations for Azure resources

Bellow are the abbreviation recommendations for many of the resources in Azure, from the Cloud Adoption Framework (CAF). The tables have *abbreviation* mapped to *resource* and *resource provider namespace*.

## AI + machine learning

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| AI Search | `Microsoft.Search/searchServices` | `srch` |
| Azure AI services (multi-service account) | `Microsoft.CognitiveServices/accounts` (kind: `CognitiveServices`) | `ais` |
| Azure AI Foundry account | `Microsoft.CognitiveServices/accounts` (kind: `AIServices`) | `aif` |
| Azure AI Foundry account project | `Microsoft.CognitiveServices/accounts/projects` | `proj` |
| Azure AI Foundry hub | `Microsoft.MachineLearningServices/workspaces` (kind: `Hub`) | `hub` |
| Azure AI Foundry hub project | `Microsoft.MachineLearningServices/workspaces` (kind: `Project`) | `proj` |
| Azure AI Video Indexer | `Microsoft.VideoIndexer/accounts` | `avi` |
| Azure Machine Learning workspace | `Microsoft.MachineLearningServices/workspaces` | `mlw` |
| Azure OpenAI Service | `Microsoft.CognitiveServices/accounts` (kind: `OpenAI`) | `oai` |
| Bot service | `Microsoft.BotService/botServices` (kind: `azurebot`) | `bot` |
| Computer vision | `Microsoft.CognitiveServices/accounts` (kind: `ComputerVision`) | `cv` |
| Content moderator | `Microsoft.CognitiveServices/accounts` (kind: `ContentModerator`) | `cm` |
| Content safety | `Microsoft.CognitiveServices/accounts` (kind: `ContentSafety`) | `cs` |
| Custom vision (prediction) | `Microsoft.CognitiveServices/accounts` (kind: `CustomVision.Prediction`) | `cstv` |
| Custom vision (training) | `Microsoft.CognitiveServices/accounts` (kind: `CustomVision.Training`) | `cstvt` |
| Document intelligence | `Microsoft.CognitiveServices/accounts` (kind: `FormRecognizer`) | `di` |
| Face API | `Microsoft.CognitiveServices/accounts` (kind: `Face`) | `face` |
| Health Insights | `Microsoft.CognitiveServices/accounts` (kind: `HealthInsights`) | `hi` |
| Immersive reader | `Microsoft.CognitiveServices/accounts` (kind: `ImmersiveReader`) | `ir` |
| Language service | `Microsoft.CognitiveServices/accounts` (kind: `TextAnalytics`) | `lang` |
| Speech service | `Microsoft.CognitiveServices/accounts` (kind: `SpeechServices`) | `spch` |
| Translator | `Microsoft.CognitiveServices/accounts` (kind: `TextTranslation`) | `trsl` |

## Analytics and IoT

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| Azure Analysis Services server | `Microsoft.AnalysisServices/servers` | `as` |
| Azure Databricks Access Connector | `Microsoft.Databricks/workspaces/accessConnectors` | `dbac` |
| Azure Databricks workspace | `Microsoft.Databricks/workspaces` | `dbw` |
| Azure Data Explorer cluster | `Microsoft.Kusto/clusters` | `dec` |
| Azure Data Explorer cluster database | `Microsoft.Kusto/clusters/databases` | `dedb` |
| Azure Data Factory | `Microsoft.DataFactory/factories` | `adf` |
| Azure Digital Twin instance | `Microsoft.DigitalTwins/digitalTwinsInstances` | `dt` |
| Azure Stream Analytics | `Microsoft.StreamAnalytics/cluster` | `asa` |
| Azure Synapse Analytics private link hub | `Microsoft.Synapse/privateLinkHubs` | `synplh` |
| Azure Synapse Analytics SQL Dedicated Pool | `Microsoft.Synapse/workspaces/sqlPools` | `syndp` |
| Azure Synapse Analytics Spark Pool | `Microsoft.Synapse/workspaces/bigDataPools` | `synsp` |
| Azure Synapse Analytics workspaces | `Microsoft.Synapse/workspaces` | `synw` |
| Data Lake Store account | `Microsoft.DataLakeStore/accounts` | `dls` |
| Event Hubs namespace | `Microsoft.EventHub/namespaces` | `evhns` |
| Event hub | `Microsoft.EventHub/namespaces/eventHubs` | `evh` |
| Event Grid domain | `Microsoft.EventGrid/domains` | `evgd` |
| Event Grid namespace | `Microsoft.EventGrid/namespaces` | `evgns` |
| Event Grid subscriptions | `Microsoft.EventGrid/eventSubscriptions` | `evgs` |
| Event Grid topic | `Microsoft.EventGrid/domains/topics` | `evgt` |
| Event Grid system topic | `Microsoft.EventGrid/systemTopics` | `egst` |
| Fabric Capacity | `Microsoft.Fabric/capacities` | `fc` |
| HDInsight - Hadoop cluster | `Microsoft.HDInsight/clusters` | `hadoop` |
| HDInsight - HBase cluster | `Microsoft.HDInsight/clusters` | `hbase` |
| HDInsight - Kafka cluster | `Microsoft.HDInsight/clusters` | `kafka` |
| HDInsight - Spark cluster | `Microsoft.HDInsight/clusters` | `spark` |
| HDInsight - Storm cluster | `Microsoft.HDInsight/clusters` | `storm` |
| HDInsight - ML Services cluster | `Microsoft.HDInsight/clusters` | `mls` |
| IoT hub | `Microsoft.Devices/IotHubs` | `iot` |
| Provisioning services | `Microsoft.Devices/provisioningServices` | `provs` |
| Provisioning services certificate | `Microsoft.Devices/provisioningServices/certificates` | `pcert` |
| Power BI Embedded | `Microsoft.PowerBIDedicated/capacities` | `pbi` |
| Time Series Insights environment | `Microsoft.TimeSeriesInsights/environments` | `tsi` |

## Compute and web

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| App Service environment | `Microsoft.Web/hostingEnvironments` | `ase` |
| App Service plan | `Microsoft.Web/serverFarms` | `asp` |
| Azure Load Testing instance | `Microsoft.LoadTestService/loadTests` | `lt` |
| Availability set | `Microsoft.Compute/availabilitySets` | `avail` |
| Azure Arc enabled server | `Microsoft.HybridCompute/machines` | `arcs` |
| Azure Arc enabled Kubernetes cluster | `Microsoft.Kubernetes/connectedClusters` | `arck` |
| Azure Arc private link scope | `Microsoft.HybridCompute/privateLinkScopes` | `pls` |
| Azure Arc gateway | `Microsoft.HybridCompute/gateways` | `arcgw` |
| Batch accounts | `Microsoft.Batch/batchAccounts` | `ba` |
| Cloud service | `Microsoft.Compute/cloudServices` | `cld` |
| Communication Services | `Microsoft.Communication/communicationServices` | `acs` |
| Disk encryption set | `Microsoft.Compute/diskEncryptionSets` | `des` |
| Function app | `Microsoft.Web/sites` | `func` |
| Gallery | `Microsoft.Compute/galleries` | `gal` |
| Hosting environment | `Microsoft.Web/hostingEnvironments` | `host` |
| Image template | `Microsoft.VirtualMachineImages/imageTemplates` | `it` |
| Managed disk (OS) | `Microsoft.Compute/disks` | `osdisk` |
| Managed disk (data) | `Microsoft.Compute/disks` | `disk` |
| Notification Hubs | `Microsoft.NotificationHubs/namespaces/notificationHubs` | `ntf` |
| Notification Hubs namespace | `Microsoft.NotificationHubs/namespaces` | `ntfns` |
| Proximity placement group | `Microsoft.Compute/proximityPlacementGroups` | `ppg` |
| Restore point collection | `Microsoft.Compute/restorePointCollections` | `rpc` |
| Snapshot | `Microsoft.Compute/snapshots` | `snap` |
| Static web app | `Microsoft.Web/staticSites` | `stapp` |
| Virtual machine | `Microsoft.Compute/virtualMachines` | `vm` |
| Virtual machine scale set | `Microsoft.Compute/virtualMachineScaleSets` | `vmss` |
| Virtual machine maintenance configuration | `Microsoft.Maintenance/maintenanceConfigurations` | `mc` |
| VM storage account | `Microsoft.Storage/storageAccounts` | `stvm` |
| Web app | `Microsoft.Web/sites` | `app` |

## Containers

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| AKS cluster | `Microsoft.ContainerService/managedClusters` | `aks` |
| AKS system node pool | `Microsoft.ContainerService/managedClusters/agentPools` (mode: `System`) | `npsystem` |
| AKS user node pool | `Microsoft.ContainerService/managedClusters/agentPools` (mode: `User`) | `np` |
| Container apps | `Microsoft.App/containerApps` | `ca` |
| Container apps environment | `Microsoft.App/managedEnvironments` | `cae` |
| Container apps job | `Microsoft.App/jobs` | `caj` |
| Container registry | `Microsoft.ContainerRegistry/registries` | `cr` |
| Container instance | `Microsoft.ContainerInstance/containerGroups` | `ci` |
| Service Fabric cluster | `Microsoft.ServiceFabric/clusters` | `sf` |
| Service Fabric managed cluster | `Microsoft.ServiceFabric/managedClusters` | `sfmc` |

## Databases

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| Azure Cosmos DB database | `Microsoft.DocumentDB/databaseAccounts/sqlDatabases` | `cosmos` |
| Azure Cosmos DB for Apache Cassandra account | `Microsoft.DocumentDB/databaseAccounts` | `coscas`|
| Azure Cosmos DB for MongoDB account | `Microsoft.DocumentDB/databaseAccounts` | `cosmon`|
| Azure Cosmos DB for NoSQL account | `Microsoft.DocumentDb/databaseAccounts` | `cosno`|
| Azure Cosmos DB for Table account | `Microsoft.DocumentDb/databaseAccounts` |`costab`|
| Azure Cosmos DB for Apache Gremlin account | `Microsoft.DocumentDb/databaseAccounts` | `cosgrm`|
| Azure Cosmos DB PostgreSQL cluster | `Microsoft.DBforPostgreSQL/serverGroupsv2` | `cospos`|
| Azure Cache for Redis instance | `Microsoft.Cache/Redis` | `redis` |
| Azure Managed Redis | `Microsoft.Cache/RedisEnterprise` | `amr` |
| Azure SQL Database server | `Microsoft.Sql/servers` | `sql` |
| Azure SQL database | `Microsoft.Sql/servers/databases` | `sqldb` |
| Azure SQL Elastic Job agent | `Microsoft.Sql/servers/jobAgents` | `sqlja` |
| Azure SQL Elastic Pool | `Microsoft.Sql/servers/elasticpool` | `sqlep` |
| MySQL database | `Microsoft.DBforMySQL/servers` | `mysql` |
| PostgreSQL database | `Microsoft.DBforPostgreSQL/servers` | `psql` |
| SQL Managed Instance | `Microsoft.Sql/managedInstances` | `sqlmi` |

## Developer tools

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| App Configuration store | `Microsoft.AppConfiguration/configurationStores` | `appcs` |
| Maps account | `Microsoft.Maps/accounts` | `map` |
| SignalR | `Microsoft.SignalRService/SignalR` | `sigr` |
| WebPubSub | `Microsoft.SignalRService/webPubSub` | `wps` |

## DevOps

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| Azure Managed Grafana | `Microsoft.Dashboard/grafana` | `amg` |

## Integration

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| API management service instance | `Microsoft.ApiManagement/service` | `apim` |
| Integration account | `Microsoft.Logic/integrationAccounts` | `ia` |
| Logic app | `Microsoft.Logic/workflows` | `logic` |
| Service Bus namespace | `Microsoft.ServiceBus/namespaces` | `sbns` |
| Service Bus queue | `Microsoft.ServiceBus/namespaces/queues` | `sbq` |
| Service Bus topic | `Microsoft.ServiceBus/namespaces/topics` | `sbt` |
| Service Bus topic subscription | `Microsoft.ServiceBus/namespaces/topics/subscriptions` | `sbts` |

## Management and governance

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| Automation account | `Microsoft.Automation/automationAccounts` | `aa` |
| Azure Policy definition | `Microsoft.Authorization/policyDefinitions` | <*descriptive*> |
| Application Insights | `Microsoft.Insights/components` | `appi` |
| Azure Monitor action group | `Microsoft.Insights/actionGroups` | `ag` |
| Azure Monitor data collection rule | `Microsoft.Insights/dataCollectionRules` | `dcr` |
| Azure Monitor alert processing rule | `Microsoft.AlertsManagement/actionRules` | `apr` |
| Data collection endpoint | `Microsoft.Insights/dataCollectionEndpoints` | `dce` |
| Deployment scripts | `Microsoft.Resources/deploymentScripts` | `script` |
| Log Analytics workspace | `Microsoft.OperationalInsights/workspaces` | `log` |
| Log Analytics query packs | `Microsoft.OperationalInsights/querypacks` | `pack` |
| Management group | `Microsoft.Management/managementGroups` | `mg` |
| Microsoft Purview instance | `Microsoft.Purview/accounts` | `pview` |
| Resource group | `Microsoft.Resources/resourceGroups` | `rg` |
| Template specs name | `Microsoft.Resources/templateSpecs` | `ts` |

## Migration

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| Azure Migrate project | `Microsoft.Migrate/assessmentProjects` | `migr` |
| Database Migration Service instance | `Microsoft.DataMigration/services` | `dms` |
| Recovery Services vault | `Microsoft.RecoveryServices/vaults` | `rsv` |

## Networking

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| Application gateway | `Microsoft.Network/applicationGateways` | `agw` |
| Application security group (ASG) | `Microsoft.Network/applicationSecurityGroups` | `asg` |
| CDN profile | `Microsoft.Cdn/profiles` | `cdnp` |
| CDN endpoint | `Microsoft.Cdn/profiles/endpoints` | `cdne` |
| Connections | `Microsoft.Network/connections`| `con` |
| DNS | `Microsoft.Network/dnsZones` | \<*DNS domain name*> |
| DNS forwarding ruleset | `Microsoft.Network/dnsForwardingRulesets` | `dnsfrs` |
| DNS private resolver | `Microsoft.Network/dnsResolvers` | `dnspr` |
| DNS private resolver inbound endpoint | `Microsoft.Network/dnsResolvers/inboundEndpoints` | `in` |
| DNS private resolver outbound endpoint | `Microsoft.Network/dnsResolvers/outboundEndpoints` | `out` |
| DNS zone | `Microsoft.Network/privateDnsZones` | \<*DNS domain name*> |
| Firewall | `Microsoft.Network/azureFirewalls` | `afw` |
| Firewall policy | `Microsoft.Network/firewallPolicies` | `afwp` |
| ExpressRoute circuit | `Microsoft.Network/expressRouteCircuits` | `erc` |
| ExpressRoute direct | `Microsoft.Network/expressRoutePorts` | `erd` |
| ExpressRoute gateway | `Microsoft.Network/virtualNetworkGateways` | `ergw` |
| Front Door (Standard/Premium) profile | `Microsoft.Cdn/profiles` | `afd` |
| Front Door (Standard/Premium) endpoint | `Microsoft.Cdn/profiles/afdEndpoints` | `fde` |
| Front Door firewall policy | `Microsoft.Network/frontdoorWebApplicationFirewallPolicies` | `fdfp`|
| Front Door (classic) | `Microsoft.Network/frontDoors` | `afd` |
| IP group | `Microsoft.Network/ipGroups` | `ipg` |
| Load balancer (internal) | `Microsoft.Network/loadBalancers` | `lbi`|
| Load balancer (external) | `Microsoft.Network/loadBalancers` | `lbe`|
| Load balancer rule | `Microsoft.Network/loadBalancers/inboundNatRules` | `rule`|
| Local network gateway | `Microsoft.Network/localNetworkGateways` | `lgw` |
| NAT gateway | `Microsoft.Network/natGateways` | `ng` |
| Network interface (NIC) | `Microsoft.Network/networkInterfaces` | `nic`|
| Network security perimeter | `Microsoft.Network/networkSecurityPerimeters` | `nsp`|
| Network security group (NSG) | `Microsoft.Network/networkSecurityGroups` | `nsg` |
| Network security group (NSG) security rules | `Microsoft.Network/networkSecurityGroups/securityRules` | `nsgsr` |
| Network Watcher | `Microsoft.Network/networkWatchers` | `nw` |
| Private Link | `Microsoft.Network/privateLinkServices` | `pl` |
| Private endpoint | `Microsoft.Network/privateEndpoints` | `pep` |
| Public IP address | `Microsoft.Network/publicIPAddresses` | `pip`|
| Public IP address prefix | `Microsoft.Network/publicIPPrefixes` | `ippre`|
| Route filter | `Microsoft.Network/routeFilters` | `rf` |
| Route server | `Microsoft.Network/virtualHubs` | `rtserv` |
| Route table | `Microsoft.Network/routeTables` | `rt` |
| Service endpoint policy | `Microsoft.Network/serviceEndPointPolicies` | `se` |
| Traffic Manager profile | `Microsoft.Network/trafficManagerProfiles` | `traf` |
| User defined route (UDR) | `Microsoft.Network/routeTables/routes` | `udr` |
| Virtual network | `Microsoft.Network/virtualNetworks` | `vnet`|
| Virtual network gateway | `Microsoft.Network/virtualNetworkGateways` | `vgw` |
| Virtual network manager | `Microsoft.Network/networkManagers` | `vnm`|
| Virtual network peering | `Microsoft.Network/virtualNetworks/virtualNetworkPeerings` | `peer`|
| Virtual network subnet | `Microsoft.Network/virtualNetworks/subnets` | `snet`|
| Virtual WAN | `Microsoft.Network/virtualWans` | `vwan`|
| Virtual WAN Hub | `Microsoft.Network/virtualHubs` | `vhub`|

## Security

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| Azure Bastion | `Microsoft.Network/bastionHosts` | `bas` |
| Key vault | `Microsoft.KeyVault/vaults` | `kv` |
| Key Vault Managed HSM | `Microsoft.KeyVault/managedHSMs` | `kvmhsm` |
| Managed identity | `Microsoft.ManagedIdentity/userAssignedIdentities` | `id` |
| SSH key | `Microsoft.Compute/sshPublicKeys` | `sshkey` |
| VPN Gateway| `Microsoft.Network/vpnGateways` | `vpng`|
| VPN connection | `Microsoft.Network/vpnGateways/vpnConnections` | `vcn` |
| VPN site | `Microsoft.Network/vpnGateways/vpnSites` | `vst` |
| Web Application Firewall (WAF) policy | `Microsoft.Network/firewallPolicies` | `waf` |
| Web Application Firewall (WAF) policy rule group | `Microsoft.Network/firewallPolicies/ruleGroups` | `wafrg` |

## Storage

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| Backup Vault name | `Microsoft.DataProtection/backupVaults` | `bvault` |
| Backup Vault policy | `Microsoft.DataProtection/backupVaults/backupPolicies` | `bkpol` |
| File share | `Microsoft.Storage/storageAccounts/fileServices/shares` | `share` |
| Storage account | `Microsoft.Storage/storageAccounts` | `st` |
| Storage Sync Service name | `Microsoft.StorageSync/storageSyncServices` | `sss` |

## Virtual desktop infrastructure

| Resource | Resource provider namespace | Abbreviation |
|--|--|--|
| Virtual desktop host pool | `Microsoft.DesktopVirtualization/hostPools` | `vdpool` |
| Virtual desktop application group | `Microsoft.DesktopVirtualization/applicationGroups` | `vdag` |
| Virtual desktop workspace | `Microsoft.DesktopVirtualization/workspaces` | `vdws` |
| Virtual desktop scaling plan | `Microsoft.DesktopVirtualization/scalingPlans` | `vdscaling`|
