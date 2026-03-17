---
name: ipcalc-for-cloud
description: Calculates IP ranges, CIDR blocks, and subnet allocations for cloud networks (Azure, AWS, GCP, Oracle, AliCloud). Supports single VNet/VPC or hub-spoke topologies with automatic AZ distribution. Outputs as info tables, JSON, or IaC templates (Terraform, Bicep, ARM, PowerShell, CloudFormation). Use for network planning, IP calculations, CIDR notation, or infrastructure as code generation.
allowed-tools: Bash(python *), Bash(terraform *), Bash(az *), Bash(aws *)
---

<objective>
Calculate IP ranges, CIDR blocks, and subnet allocations for cloud network planning. This skill:
- Performs CIDR subnet calculations and splitting for cloud providers
- Creates single VNet/VPC with multiple subnets OR hub-spoke topologies
- Validates IP ranges and detects overlaps
- Automatically assigns optimal CIDR blocks or uses custom subnet prefixes
- Distributes subnets across availability zones (AWS, GCP)
- Calculates provider-specific reserved IPs and usable ranges
- Outputs results as formatted tables, JSON, or IaC templates

Supported Cloud Providers:
- **Azure**: VNets with subnets, optional hub-spoke peering
- **AWS**: VPCs with subnets distributed across AZs
- **GCP**: VPCs with subnets (hub-spoke supported)
- **Oracle Cloud**: VCNs with subnets
- **AliCloud**: VPCs with subnets
- **On-Premises**: Basic IP calculations

Output Formats by Provider:
- **Azure**: info, JSON, Terraform, Bicep, ARM, PowerShell, Azure CLI
- **AWS**: info, JSON, Terraform, CloudFormation, AWS CLI
- **GCP**: info, JSON, Terraform, gcloud
- **Oracle**: info, JSON, Terraform, OCI CLI
- **AliCloud**: info, JSON, Terraform, Aliyun CLI
- **On-Premises**: info, JSON

Uses Python for deterministic IP calculations matching the TypeScript CLI implementation.
</objective>

<quick_start>
Basic usage - calculate subnets for a single VNet/VPC:

**Show network information**:
```
/ipcalc-for-cloud "azure, 10.0.0.0/16, 4 subnets"
```

**Generate Terraform for AWS**:
```
/ipcalc-for-cloud "aws, 10.0.0.0/16, 3 subnets, output: terraform"
```

**Custom subnet prefix** (to avoid filling entire network):
```
/ipcalc-for-cloud "azure, 172.16.1.0/24, 4 subnets, prefix: /26"
```

**Hub-spoke topology for Azure**:
```
/ipcalc-for-cloud "azure, 10.0.0.0/16, 2 subnets, spokes: 10.1.0.0/16,10.2.0.0/16, spoke-subnets: 2,2, output: terraform"
```

The skill will:
- Calculate optimal CIDR splits based on provider constraints
- Distribute subnets across availability zones (AWS/GCP)
- Apply provider-specific reserved IP calculations
- Validate IP allocations
- Output in requested format
</quick_start>

<workflow>
## Step 1: Parse Input Specifications

Accept user input specifying:
- **Cloud provider**: azure, aws, gcp, oracle, alicloud, onpremises
- **Base CIDR**: Network CIDR block (e.g., "10.0.0.0/16")
- **Number of subnets**: How many subnets to create (1-256)
- **Output format**: info (default), json, terraform, bicep, arm, powershell, cloudformation, cli, gcloud, oci, aliyun
- **Optional - Custom prefix**: Desired subnet prefix (e.g., /26) to override auto-calculation
- **Optional - Hub-spoke**: Spoke network CIDRs and subnet counts for hub-spoke topology

Extract:
- Cloud provider selection
- Base IP range (CIDR notation)
- Number of subnets for primary network
- Output format
- Custom subnet prefix (if specified)
- Spoke network specifications (if hub-spoke topology)

## Step 2: Run IP Calculations

Execute the IP calculation script with cloud provider configuration:

```bash
python ~/.claude/skills/ipcalc-for-cloud/scripts/ipcalc.py \
  --provider azure \
  --cidr "10.0.0.0/16" \
  --subnets 4 \
  --output terraform
```

**With custom subnet prefix**:
```bash
python ~/.claude/skills/ipcalc-for-cloud/scripts/ipcalc.py \
  --provider azure \
  --cidr "172.16.1.0/24" \
  --subnets 4 \
  --prefix 26 \
  --output info
```

**With hub-spoke topology**:
```bash
python ~/.claude/skills/ipcalc-for-cloud/scripts/ipcalc.py \
  --provider azure \
  --cidr "10.0.0.0/16" \
  --subnets 2 \
  --spoke-cidrs "10.1.0.0/16,10.2.0.0/16,10.3.0.0/16" \
  --spoke-subnets "2,2,2" \
  --output terraform
```

The script will:
- Validate base CIDR against provider constraints
- Calculate optimal subnet prefix OR use custom prefix
- Check capacity (can the network accommodate requested subnets?)
- Generate subnet CIDR assignments
- Distribute subnets across availability zones (AWS, GCP)
- Calculate provider-specific reserved IPs (Azure: 5, AWS: 5, GCP: 4, Oracle: 3)
- Calculate usable IP ranges
- Detect any overlaps or invalid ranges
- For hub-spoke: Calculate spoke networks and configure peering
- Output structured data for template rendering

## Step 3: Output Results

Based on requested output format and provider:

**Info format** (default):
- Human-readable formatted table
- Network details (CIDR, total IPs, address range)
- Subnet details with availability zones
- Reserved and usable IP information
- Provider-specific formatting

**JSON format**:
- Structured JSON data
- Complete network and subnet information
- Availability zone assignments
- Reserved IP lists
- Machine-readable for integration

**Terraform format**:
Generate HCL code with:
- Provider configuration (azurerm, aws, google, etc.)
- Variables for customization
- Network resource (VNet/VPC)
- Subnet resources with AZ distribution
- Outputs for resource IDs
- Hub-spoke peering resources (if applicable)
- Comments with IP allocation table

**Other IaC formats**:
- **Bicep**: Azure Bicep template with inline subnets
- **ARM**: Azure Resource Manager JSON template
- **PowerShell**: Azure PowerShell script with cmdlets
- **CloudFormation**: AWS YAML template with intrinsic functions
- **CLI Scripts**: Bash scripts with az/aws/gcloud commands

## Step 4: Validate Output

Run validation checks:
- IP range validation (no overlaps, proper nesting)
- Provider constraint validation (prefix limits)
- Capacity validation (requested subnets fit in network)
- For Terraform: syntax validation (if terraform CLI available)
- For hub-spoke: peering configuration correctness
</workflow>

<examples>
<example number="1">
<input>
User: "Calculate IP allocation for Azure with 10.0.0.0/16 and 4 subnets"
</input>
<process>
1. Parse: provider=azure, cidr=10.0.0.0/16, subnets=4, output=info (default)
2. Calculate:
   - VNet: 10.0.0.0/16 (65,536 IPs)
   - Auto-calculate subnet prefix: /18 (4 subnets need 2 bits)
   - Subnet 1: 10.0.0.0/18 (16,384 IPs, Azure AZ 1)
   - Subnet 2: 10.0.64.0/18 (16,384 IPs, Azure AZ 2)
   - Subnet 3: 10.0.128.0/18 (16,384 IPs, Azure AZ 3)
   - Subnet 4: 10.0.192.0/18 (16,384 IPs, Azure AZ 1)
   - Apply Azure reserved IPs (5 per subnet)
3. Display formatted table with network info and subnet details
</process>
<output>
Formatted table showing:
- Network address, CIDR, total IPs
- Each subnet with CIDR, network, mask, usable IPs, usable range, AZ, reserved IPs
</output>
</example>

<example number="2">
<input>
User: "Generate Terraform for AWS with 172.16.0.0/12, 6 subnets"
</input>
<process>
1. Parse: provider=aws, cidr=172.16.0.0/12, subnets=6, output=terraform
2. Calculate:
   - VPC: 172.16.0.0/12 (1,048,576 IPs)
   - Auto-calculate subnet prefix: /15 (6 subnets need 3 bits = /15)
   - Generate 6 subnets distributed round-robin across AWS AZs
   - Apply AWS reserved IPs (5 per subnet)
3. Generate Terraform code with AWS provider, VPC, subnets with AZ distribution, outputs
</process>
<output>
Terraform file with:
- AWS provider ~> 5.0
- VPC resource with DNS enabled
- 6 subnet resources, each with availability_zone from round-robin distribution
- Internet gateway and route table
- Output blocks for VPC ID and subnet IDs
- IP allocation table in comments
</output>
</example>

<example number="3">
<input>
User: "Azure hub-spoke with hub 10.0.0.0/16 (2 subnets), spokes 10.1.0.0/16 and 10.2.0.0/16 (2 subnets each), Terraform output"
</input>
<process>
1. Parse: provider=azure, hub_cidr=10.0.0.0/16, hub_subnets=2, spoke_cidrs=[10.1.0.0/16, 10.2.0.0/16], spoke_subnets=[2,2], output=terraform
2. Calculate hub network:
   - Hub VNet: 10.0.0.0/16
   - 2 subnets (/17 each)
3. Calculate spoke networks:
   - Spoke 1: 10.1.0.0/16 with 2 subnets (/17 each)
   - Spoke 2: 10.2.0.0/16 with 2 subnets (/17 each)
4. Generate Terraform with peering configuration
</process>
<output>
Terraform file with:
- Hub VNet and subnets
- Spoke VNet resources
- Spoke subnet resources
- Bidirectional peering: hub-to-spoke1, spoke1-to-hub, hub-to-spoke2, spoke2-to-hub
- Peering properties: allowVirtualNetworkAccess, allowForwardedTraffic
- Outputs for all network and peering IDs
</output>
</example>

<example number="4">
<input>
User: "Calculate 172.16.1.0/24 with 4 subnets using /26 prefix for Azure"
</input>
<process>
1. Parse: provider=azure, cidr=172.16.1.0/24, subnets=4, prefix=26
2. Validate:
   - /24 network can fit 4 × /26 subnets? Yes (256 IPs ÷ 64 IPs = 4)
   - /26 meets Azure minimum (/29)? Yes
3. Calculate using /26 prefix:
   - Subnet 1: 172.16.1.0/26 (64 IPs)
   - Subnet 2: 172.16.1.64/26 (64 IPs)
   - Subnet 3: 172.16.1.128/26 (64 IPs)
   - Subnet 4: 172.16.1.192/26 (64 IPs)
   - This uses exactly the full /24 network
4. Display info
</process>
<output>
Formatted table showing 4 subnets with /26 prefix, each with 59 usable IPs (64 - 5 Azure reserved)
</output>
</example>
</examples>

<validation>
For all output formats:

1. **IP Range Validation**:
   - Verify all subnets fit within parent network
   - Confirm no overlapping ranges
   - Validate CIDR notation
   - Check provider constraints (min/max prefix)

2. **Provider Constraint Validation**:
   - Azure: /8 to /29
   - AWS: /16 to /28
   - GCP: /8 to /29
   - Oracle: /16 to /30
   - AliCloud: /8 to /29

3. **Capacity Validation**:
   - Requested subnets fit in network
   - Custom prefix (if specified) allows requested subnet count
   - No address space exhaustion

4. **Manual Review Checklist**:
   - [ ] Subnets properly sized for intended use
   - [ ] Availability zone distribution is appropriate
   - [ ] Reserved IPs calculated correctly for provider
   - [ ] Usable IP counts are accurate
   - [ ] Hub-spoke peering configured correctly (if applicable)

**Additional validation for IaC output**:

5. **Syntax Validation** (if CLI tools available):
   ```bash
   # Terraform
   terraform init && terraform validate

   # Azure Bicep
   az bicep build --file output.bicep

   # AWS CloudFormation
   aws cloudformation validate-template --template-body file://output.yaml
   ```

6. **IaC Checklist**:
   - [ ] Provider configuration present and correct version
   - [ ] Resource naming follows conventions
   - [ ] Variables defined for customization
   - [ ] Output variables defined for resource IDs
   - [ ] Hub-spoke peering resources complete (if applicable)
   - [ ] IP allocation documented in comments
</validation>

<advanced_features>
**Custom Subnet Prefix**:
Specify exact subnet size instead of auto-calculation:
```
/ipcalc-for-cloud "azure, 172.16.1.0/24, 4 subnets, prefix: /26"
```
Use case: Avoid filling entire network, leave room for future expansion

**Hub-Spoke Topology** (Azure, GCP):
Create centralized hub network with multiple spoke networks:
```
/ipcalc-for-cloud "azure, 10.0.0.0/16, 2 subnets, spokes: 10.1.0.0/16,10.2.0.0/16,10.3.0.0/16, spoke-subnets: 2,3,2, output: terraform"
```
Generates bidirectional peering between hub and each spoke

**Multi-Provider Support**:
Same IP calculations work across all cloud providers with provider-specific adjustments:
- Reserved IP counts
- CIDR prefix constraints
- Availability zone naming
- Output format availability

**Availability Zone Distribution** (AWS, GCP):
Automatic round-robin distribution of subnets across AZs for high availability

**Legacy Compatibility**:
Old command-line options still supported for backward compatibility:
```bash
python ipcalc.py --base-cidr "10.0.0.0/16" --vnets 3 --subnets-per-vnet 4
```
(Creates multiple VNets instead of single VNet with subnets)
</advanced_features>

<scripts_reference>
## scripts/ipcalc.py

Main IP calculator script supporting multiple cloud providers and output formats.

**Key Functions**:
- `calculate_subnets(cidr, num_subnets, provider, desired_prefix)` - Calculate subnet allocations
- `generate_hub_spoke_topology(hub_cidr, hub_subnets, spoke_cidrs, spoke_subnets, provider)` - Hub-spoke networks
- `calculate_network_info(network, provider_config)` - Detailed network information
- `format_network_info(cidr, subnets, provider)` - Human-readable output

**Usage**:
```bash
python scripts/ipcalc.py --provider PROVIDER --cidr CIDR --subnets N [OPTIONS]
```

**Options**:
- `--provider`: Cloud provider (azure, aws, gcp, oracle, alicloud, onpremises)
- `--cidr`: Network CIDR block
- `--subnets`: Number of subnets (1-256)
- `--prefix`: Optional custom subnet prefix
- `--output`: Output format (info, json, terraform, bicep, arm, powershell, cloudformation, cli, gcloud, oci, aliyun)
- `--file`: Write output to file
- `--spoke-cidrs`: Comma-separated spoke VNet/VPC CIDRs
- `--spoke-subnets`: Comma-separated subnet counts per spoke

**Output Format** (JSON):
```json
{
  "vnetCidr": "10.0.0.0/16",
  "provider": "azure",
  "subnets": [
    {
      "name": "subnet1",
      "cidr": "10.0.0.0/18",
      "network": "10.0.0.0",
      "mask": "255.255.192.0",
      "total_ips": 16384,
      "usable_ips": 16379,
      "usable_range": "10.0.0.3 - 10.0.63.253",
      "availabilityZone": "1",
      "reserved": ["10.0.0.0", "10.0.0.1", "10.0.0.2", "10.0.63.254", "10.0.63.255"]
    }
  ],
  "peeringEnabled": false
}
```

## scripts/cloud_provider_config.py

Cloud provider configuration module defining provider-specific settings.

**Configurations**:
- Reserved IP counts (Azure: 5, AWS: 5, GCP: 4, Oracle: 3, etc.)
- CIDR prefix limits (min/max)
- Availability zone lists
- Supported output formats

**Functions**:
- `get_cloud_provider_config(provider)` - Get provider configuration
- `validate_output_format(provider, output_format)` - Validate output format support
- `get_availability_zone(provider, index)` - Get AZ for subnet index (round-robin)

## scripts/ipcalc_legacy.py

Legacy version supporting old multi-VNet split behavior. Use for backward compatibility:
```bash
python scripts/ipcalc_legacy.py --base-cidr "10.0.0.0/16" --vnets 3 --subnets-per-vnet 4
```
Creates 3 separate VNets instead of 1 VNet with subnets.
</scripts_reference>

<templates_reference>
## Template Architecture

Templates are organized by provider and format:
```
templates/
├── azure/
│   ├── terraform.template.tf
│   ├── bicep.template.bicep
│   ├── arm.template.json
│   ├── powershell.template.ps1
│   └── cli.template.sh
├── aws/
│   ├── terraform.template.tf
│   ├── cloudformation.template.yaml
│   └── cli.template.sh
└── ...
```

**Template Placeholders**:
Common across all templates:
- `{{vnetCidr}}` / `{{vpcCidr}}` - Network CIDR
- `{{subnetVariables}}` - Subnet variable declarations
- `{{subnetResources}}` - Subnet resource definitions
- `{{subnetOutputs}}` - Output definitions
- `{{spokeVnetResources}}` / `{{spokeVpcResources}}` - Spoke network resources
- `{{vnetPeeringResources}}` / `{{vpcPeeringResources}}` - Peering configurations

**Template Processor**:
The template processor module (`template_processor.py`) generates placeholder content:
- Variable/parameter declarations
- Resource definitions with proper syntax
- Hub-spoke peering logic
- Provider-specific formatting

Templates use simple string replacement for placeholders, maintaining exact output compatibility with TypeScript CLI.
</templates_reference>

<anti_patterns>
<pitfall name="filling_entire_network">
❌ Auto-calculating subnet size fills entire network, no room for growth
✅ Use `--prefix` option to specify smaller subnets, leave address space for future
</pitfall>

<pitfall name="ignoring_provider_constraints">
❌ Requesting /30 subnets in AWS (minimum is /28)
✅ Check provider min/max CIDR prefixes before planning
</pitfall>

<pitfall name="uneven_az_distribution">
❌ All subnets in single availability zone
✅ Use automatic AZ distribution (AWS, GCP) for high availability
</pitfall>

<pitfall name="incorrect_reserved_ips">
❌ Assuming standard 2 reserved IPs (network + broadcast)
✅ Use provider-specific reserved counts (Azure: 5, AWS: 5, GCP: 4)
</pitfall>

<pitfall name="missing_hub_spoke_peering">
❌ Creating hub and spoke VNets without peering configuration
✅ Use `--spoke-cidrs` option to automatically generate peering
</pitfall>

<pitfall name="hardcoded_values">
❌ Generated IaC templates with hardcoded names and regions
✅ Templates include variables for customization
</pitfall>
</anti_patterns>

<success_criteria>
The skill successfully completes when:

**For all providers and outputs**:
- [ ] IP calculations are mathematically correct and deterministic
- [ ] Provider constraints are enforced (CIDR prefix limits)
- [ ] Reserved IPs calculated correctly for provider
- [ ] Subnets fit within parent network
- [ ] No CIDR blocks overlap
- [ ] Multiple invocations with same input produce identical output
- [ ] Output format matches user request

**For AWS and GCP**:
- [ ] Subnets distributed across availability zones using round-robin
- [ ] AZ names match provider conventions

**For hub-spoke topologies**:
- [ ] Hub network calculated correctly
- [ ] All spoke networks calculated correctly
- [ ] Bidirectional peering configured for each spoke
- [ ] No overlapping CIDRs between hub and spokes or between spokes

**For IaC template outputs**:
- [ ] Generated code passes syntax validation
- [ ] Provider configuration is present and correct
- [ ] Resource naming follows cloud provider conventions
- [ ] Variables defined for customization
- [ ] Outputs defined for resource IDs
- [ ] Documentation included (IP allocation table in comments)
- [ ] Hub-spoke peering resources complete (if applicable)

**Compatibility**:
- [ ] Output matches TypeScript CLI output for same inputs
- [ ] Legacy compatibility maintained via `ipcalc_legacy.py`
</success_criteria>
