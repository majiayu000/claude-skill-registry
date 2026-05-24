---
name: aws-drawio-architecture-diagrams
description: Creates professional AWS architecture diagrams in draw.io XML format (.drawio files) using official AWS Architecture Icons (aws4 library). Use when the user asks for AWS diagrams, VPC layouts, multi-tier architectures, serverless designs, network topology, or draw.io exports involving Lambda, EC2, RDS, or other AWS services.
allowed-tools: Read, Write, Bash
---

# AWS Architecture Diagram Creation with Draw.io

## Overview

Creates pixel-perfect AWS architecture diagrams in draw.io XML format using official AWS4 shape library. Generates production-ready `.drawio` files for [diagrams.net](https://app.diagrams.net/?libs=aws4).

## When to Use

- AWS cloud architecture diagrams (VPC, subnets, services)
- Multi-tier application architectures on AWS
- Serverless designs (Lambda, API Gateway, DynamoDB)
- Network topology diagrams with security groups
- Infrastructure documentation for Well-Architected reviews

## Instructions

### File Structure

Every `.drawio` file follows this XML structure:

```xml
<mxfile host="app.diagrams.net" agent="Claude" version="24.7.17">
  <diagram id="aws-arch-1" name="AWS Architecture">
    <mxGraphModel dx="1434" dy="759" grid="1" gridSize="10" guides="1"
      tooltips="1" connect="1" arrows="1" fold="1" page="1"
      pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- AWS shapes and connectors -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Key rules:**
- IDs "0" and "1" are reserved for root cells
- Use sequential integer IDs starting from "2"
- Landscape orientation (`pageWidth="1169" pageHeight="827"`)
- All coordinates positive and aligned to grid (multiples of 10)

### AWS4 Group Containers

Groups use `container=1` with child shapes referencing via `parent="groupId"`.

**AWS Cloud (top-level boundary):**
```xml
<mxCell id="2" value="AWS Cloud" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="1">
  <mxGeometry x="100" y="40" width="1000" height="700" as="geometry" />
</mxCell>
```

**Region:**
```xml
<mxCell id="3" value="us-east-1" style="...grIcon=mxgraph.aws4.group_region;strokeColor=#00A4A6;fontColor=#147EBA;dashed=1;..." vertex="1" parent="2">
  <mxGeometry x="20" y="40" width="960" height="640" as="geometry" />
</mxCell>
```

**VPC:**
```xml
<mxCell id="4" value="VPC (10.0.0.0/16)" style="...grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;fontColor=#AAB7B8;..." vertex="1" parent="3">
  <mxGeometry x="20" y="40" width="920" height="580" as="geometry" />
</mxCell>
```

**Subnet styles:**
- Public: `strokeColor=#7AA116;fillColor=#E9F3D2;fontColor=#248814`
- Private: `strokeColor=#00A4A6;fillColor=#E6F6F7;fontColor=#147EBA`

### AWS4 Service Icons

Service icons use `shape=mxgraph.aws4.resourceIcon` with `resIcon` property.

**CRITICAL: `strokeColor=#ffffff` is required** for `resourceIcon` shapes to render white icon glyphs on colored backgrounds.

**Standard service icon:**
```xml
<mxCell id="10" value="Amazon S3" style="...gradientColor=#60A337;gradientDirection=north;fillColor=#277116;strokeColor=#ffffff;...shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="60" height="60" as="geometry" />
</mxCell>
```

**Dedicated shapes (Lambda, ALB, Users) use `strokeColor=none`.** See `references/aws-shape-reference.md` for complete shape catalog.

### Service Color Codes

Each AWS service category uses official colors. All `resourceIcon` shapes must use `strokeColor=#ffffff` and `gradientDirection=north`. See `references/aws-shape-reference.md` for full color table.

Quick reference:
| Category | fillColor | gradientColor | Services |
|----------|-----------|---------------|----------|
| Compute | `#D05C17` | `#F78E04` | EC2, ECS, EKS, Fargate |
| Storage | `#277116` | `#60A337` | S3, EBS, EFS, Glacier |
| Database | `#3334B9` | `#4D72F3` | RDS, DynamoDB, Aurora, Redshift |
| Networking | `#5A30B5` | `#945DF2` | CloudFront, Route 53, API GW |
| Security | `#C7131F` | `#F54749` | IAM, Cognito, KMS, WAF |
| App Integration | `#BC1356` | `#F54749` | SQS, SNS, EventBridge |

### Connector Styles

**Standard data flow:**
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=open;endFill=0;strokeColor=#545B64;strokeWidth=2;
```

**Encrypted connection:**
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeColor=#DD344C;strokeWidth=2;dashed=1;dashPattern=5 5;
```

**Async/event flow:**
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=open;endFill=0;strokeColor=#E7157B;strokeWidth=2;dashed=1;
```

### Layout Best Practices

1. **Hierarchy**: External → Internet → AWS Cloud → Region → VPC → Subnets → Services
2. **Flow**: Left-to-right for user traffic, top-to-bottom for tiers
3. **Sizes**: Service icons 60x60, grid-aligned coordinates
4. **Spacing**: 30-40px between icons, 20px padding inside containers
5. **Labels**: Place below icons (`verticalLabelPosition=bottom`)

## Examples

### Three-Tier Architecture

**User Request:** "Create AWS three-tier architecture with VPC, public ALB, private EC2, RDS across 2 AZs."

**Generated Output:**
```xml
<mxfile host="app.diagrams.net" agent="Claude" version="24.7.17">
  <diagram id="three-tier-1" name="Three-Tier Web App">
    <mxGraphModel dx="1434" dy="759" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="2" value="Users" style="...shape=mxgraph.aws4.users;fillColor=#232F3E;..." vertex="1" parent="1">
          <mxGeometry x="40" y="340" width="60" height="60" as="geometry" />
        </mxCell>
        <mxCell id="3" value="AWS Cloud" style="...shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;..." vertex="1" parent="1">
          <mxGeometry x="160" y="40" width="960" height="720" as="geometry" />
        </mxCell>
        <mxCell id="4" value="us-east-1" style="...grIcon=mxgraph.aws4.group_region;strokeColor=#00A4A6;dashed=1;..." vertex="1" parent="3">
          <mxGeometry x="20" y="40" width="920" height="660" as="geometry" />
        </mxCell>
        <mxCell id="5" value="VPC (10.0.0.0/16)" style="...grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;..." vertex="1" parent="4">
          <mxGeometry x="20" y="40" width="880" height="600" as="geometry" />
        </mxCell>
        <mxCell id="6" value="Public Subnet" style="...grIcon=mxgraph.aws4.group_security_group;strokeColor=#7AA116;fillColor=#E9F3D2;..." vertex="1" parent="5">
          <mxGeometry x="20" y="40" width="400" height="160" as="geometry" />
        </mxCell>
        <mxCell id="7" value="Private Subnet" style="...grIcon=mxgraph.aws4.group_security_group;strokeColor=#00A4A6;fillColor=#E6F6F7;..." vertex="1" parent="5">
          <mxGeometry x="20" y="230" width="400" height="160" as="geometry" />
        </mxCell>
        <mxCell id="8" value="Data Subnet" style="...grIcon=mxgraph.aws4.group_security_group;strokeColor=#00A4A6;fillColor=#E6F6F7;..." vertex="1" parent="5">
          <mxGeometry x="20" y="420" width="400" height="160" as="geometry" />
        </mxCell>
        <mxCell id="12" value="Application&lt;br&gt;Load Balancer" style="...fillColor=#8C4FFF;shape=mxgraph.aws4.applicationLoadBalancer;" vertex="1" parent="6">
          <mxGeometry x="170" y="50" width="60" height="60" as="geometry" />
        </mxCell>
        <mxCell id="13" value="EC2 Instance" style="...gradientColor=#F78E04;fillColor=#D05C17;strokeColor=#ffffff;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;" vertex="1" parent="7">
          <mxGeometry x="170" y="50" width="60" height="60" as="geometry" />
        </mxCell>
        <mxCell id="15" value="RDS Primary" style="...gradientColor=#4D72F3;fillColor=#3334B9;strokeColor=#ffffff;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;" vertex="1" parent="8">
          <mxGeometry x="170" y="50" width="60" height="60" as="geometry" />
        </mxCell>
        <mxCell id="20" style="...endArrow=open;strokeColor=#545B64;strokeWidth=2;" edge="1" parent="1" source="2" target="12">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="21" value="HTTPS" style="...endArrow=open;strokeColor=#545B64;strokeWidth=2;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="12" target="13">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="23" value="TCP 5432" style="...endArrow=open;strokeColor=#545B64;strokeWidth=2;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="13" target="15">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Opening Instructions:**
```
Open in draw.io with AWS libraries enabled:
https://app.diagrams.net/?libs=aws4
```

### Serverless API Architecture

**User Request:** "Create serverless architecture with API Gateway, Lambda, DynamoDB, S3 for REST API."

**Generated Output:** XML with API Gateway (violet), Lambda (orange), DynamoDB (blue), S3 (green). See `references/aws-architecture-templates.md` for complete template.

### Reference Files

See `references/` directory:
- `aws-shape-reference.md` - Complete AWS4 shape catalog with styles for 50+ services
- `aws-architecture-templates.md` - Ready-to-use templates (3-tier, serverless, data pipeline)

## Constraints and Warnings

### Validation Workflow

Always follow this validation checklist before saving:

1. **Generate XML** - Create complete `.drawio` file structure
2. **Validate ID uniqueness** - Ensure all IDs are unique integers (0, 1 reserved)
3. **Check parent references** - Verify all `parent` attributes reference existing cells
4. **Verify XML well-formedness** - Close all tags, escape special chars (`&`→`&amp;`, `<`→`&lt;`)
5. **Test in draw.io** - Open at `https://app.diagrams.net/?libs=aws4`
6. **Fix rendering issues** - Adjust positions if elements overlap or render incorrectly

### Critical Constraints

1. **XML well-formed**: Invalid XML fails to open. Close all tags, escape special characters, use `&lt;br&gt;` for line breaks.

2. **ID uniqueness mandatory**: IDs "0" and "1" reserved. All others must be unique integers from "2". Duplicates cause loading failures.

3. **Coordinate system**: All coordinates positive integers, multiples of 10 for grid alignment.

4. **AWS4 library only**: Use official `mxgraph.aws4.*` shapes. Legacy `mxgraph.aws3.*` not supported.

5. **Valid parent references**: Parent must reference existing cell ID. Invalid refs cause elements to disappear.

### Limitations

- No dynamic layouts - Manual adjustment may be needed for complex diagrams
- Single page only - Multi-page requires multiple `<diagram>` elements
- No auto-routing - Rearranging elements requires manual edge adjustment

### Security Considerations

- No sensitive data - Avoid real IPs, ARNs, or resource IDs in labels
- Review before sharing - XML exposes architecture details
- Validate templates - Review XML before production documentation

## Best Practices

1. Use official AWS4 shapes (`mxgraph.aws4.*`)
2. Follow AWS service category colors
3. Nest properly: AWS Cloud → Region → VPC → Subnet → Services
4. Label services, CIDR blocks, ports, protocols
5. Show data flow direction with labeled arrows
6. Include external actors (users, corporate DC)
7. Keep diagrams focused (15-20 icons max)
8. Add annotations for important notes ("Multi-AZ", "Auto Scaling")
9. Validate all IDs unique and parent references exist
