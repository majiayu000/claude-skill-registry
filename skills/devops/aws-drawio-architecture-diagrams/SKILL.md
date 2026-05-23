---
name: aws-drawio-architecture-diagrams
description: Provides professional AWS architecture diagram creation in draw.io XML format (.drawio files) using official AWS Architecture Icons (aws4 library). Use when creating AWS cloud architecture diagrams, infrastructure diagrams, network topology diagrams, serverless architectures, multi-tier application diagrams, VPC layouts, or any AWS visual diagram in draw.io format.
category: aws
tags: [aws, drawio, architecture, diagrams, infrastructure, cloud, visualization]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS Architecture Diagram Creation with Draw.io

## Overview

Create professional, pixel-perfect AWS architecture diagrams in draw.io's native XML format using the official AWS Architecture Icons (aws4 shape library). This skill enables generation of production-ready `.drawio` files that can be opened directly in [diagrams.net](https://app.diagrams.net/?libs=aws4).

## When to Use

Use this skill when:
- Creating AWS cloud architecture diagrams (VPC, subnets, services)
- Designing multi-tier application architectures on AWS
- Drawing serverless architecture diagrams (Lambda, API Gateway, DynamoDB)
- Visualizing network topologies with VPCs, subnets, and security groups
- Creating infrastructure diagrams for AWS Well-Architected reviews
- Documenting existing AWS infrastructure as visual diagrams
- Building deployment architecture diagrams with ECS, EKS, or EC2
- Designing data pipeline architectures (Kinesis, S3, Glue, Redshift)
- Creating disaster recovery and multi-region architecture diagrams

## Instructions

### Draw.io File Structure

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
        <!-- AWS shapes and connectors here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Key rules:**
- IDs "0" and "1" are reserved for root cells
- Use sequential integer IDs starting from "2"
- Use landscape orientation (`pageWidth="1169" pageHeight="827"`) for architecture diagrams
- All coordinates must be positive and aligned to grid (multiples of 10)

### AWS4 Group Containers

Groups are containers that visually organize AWS resources. They use `container=1` and child shapes reference the group via `parent="groupId"`.

**AWS Cloud (top-level boundary):**
```xml
<mxCell id="2" value="AWS Cloud" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="1">
  <mxGeometry x="100" y="40" width="1000" height="700" as="geometry" />
</mxCell>
```

**Region:**
```xml
<mxCell id="3" value="us-east-1" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor=#00A4A6;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=1;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="2">
  <mxGeometry x="20" y="40" width="960" height="640" as="geometry" />
</mxCell>
```

**VPC:**
```xml
<mxCell id="4" value="VPC (10.0.0.0/16)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#AAB7B8;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="3">
  <mxGeometry x="20" y="40" width="920" height="580" as="geometry" />
</mxCell>
```

**Public Subnet:**
```xml
style="points=[[...same points...]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;strokeColor=#7AA116;fillColor=#E9F3D2;verticalAlign=top;align=left;spacingLeft=30;fontColor=#248814;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
```

**Private Subnet:**
```xml
style="points=[[...same points...]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
```

### AWS4 Service Icons

Service icons use the `shape=mxgraph.aws4.resourceIcon` pattern with `resIcon` for the specific service, or dedicated shape names.

**CRITICAL: `strokeColor=#ffffff` is required** for all `resourceIcon` shapes. This makes the icon glyph render as **white** on the colored background. Using `strokeColor=none` causes the icon to render as black.

**Standard service icon pattern:**
```xml
<mxCell id="10" value="Amazon S3" style="sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;gradientColor=#60A337;gradientDirection=north;fillColor=#277116;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="60" height="60" as="geometry" />
</mxCell>
```

**Note:** Dedicated shapes like `lambda_function`, `applicationLoadBalancer`, `users` do NOT use `resourceIcon` and should keep `strokeColor=none`.

### AWS Service Color Codes

Each AWS service category uses official colors with gradients for `resourceIcon` shapes. All `resourceIcon` shapes **must** use `strokeColor=#ffffff` and `gradientDirection=north`.

| Category | fillColor | gradientColor | strokeColor | Services |
|----------|-----------|---------------|-------------|----------|
| **Compute** | `#D05C17` | `#F78E04` | `#ffffff` | EC2, ECS, EKS, Fargate |
| **Compute (dedicated shapes)** | `#ED7100` | none | none | Lambda (`lambda_function`), ALB (`applicationLoadBalancer`) |
| **Storage** | `#277116` | `#60A337` | `#ffffff` | S3, EBS, EFS, Glacier |
| **Database** | `#3334B9` | `#4D72F3` | `#ffffff` | RDS, DynamoDB, ElastiCache, Aurora, Redshift |
| **Networking** | `#5A30B5` | `#945DF2` | `#ffffff` | CloudFront, Route 53, ELB, API Gateway, NAT GW, IGW |
| **Security** | `#C7131F` | `#F54749` | `#ffffff` | IAM, Cognito, KMS, WAF, Shield, Pinpoint |
| **Analytics** | `#5A30B5` | `#945DF2` | `#ffffff` | Kinesis, Athena, Glue, EMR, Lake Formation |
| **Application Integration** | `#BC1356` | `#F54749` | `#ffffff` | SQS, SNS, EventBridge, Step Functions |
| **Management** | `#BC1356` | `#F54749` | `#ffffff` | CloudWatch, CloudFormation, Systems Manager |
| **Machine Learning** | `#116D5B` | `#4AB29A` | `#ffffff` | SageMaker, Bedrock, Comprehend, Lex, Rekognition |
| **Developer Tools** | `#5A30B5` | `#945DF2` | `#ffffff` | CodePipeline, CodeBuild, CodeDeploy |
| **General / External** | `#232F3E` | none | none | Users, Mobile Client, Corporate DC (dedicated shapes) |

### Connector Styles for AWS Diagrams

**Standard data flow:**
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=open;endFill=0;strokeColor=#545B64;strokeWidth=2;
```

**Secure/encrypted connection:**
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeColor=#DD344C;strokeWidth=2;dashed=1;dashPattern=5 5;
```

**Async/event-driven flow:**
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=open;endFill=0;strokeColor=#E7157B;strokeWidth=2;dashed=1;
```

### Layout Best Practices for AWS Diagrams

1. **Hierarchy**: External users → Internet → AWS Cloud → Region → VPC → Subnets → Services
2. **Left-to-right flow**: User traffic enters from the left, data flows right
3. **Top-to-bottom tiers**: Public tier on top, private tier in middle, data tier at bottom
4. **Standard sizes**: Service icons 60x60, group containers follow nesting
5. **Spacing**: 30-40px between service icons, 20px padding inside containers
6. **Grid alignment**: All coordinates in multiples of 10
7. **Labels**: Place below icons (`verticalLabelPosition=bottom;verticalAlign=top;`)

### Opening Diagrams with AWS Libraries

Always include this instruction when generating a `.drawio` file:

```
Open in draw.io with AWS libraries enabled:
https://app.diagrams.net/?libs=aws4
```

## Examples

### Example 1: Generate a Three-Tier Architecture Diagram

**User Request:**
"Create an AWS architecture diagram for a three-tier web application with VPC, public subnets for ALB, private subnets for EC2, and RDS in data subnets across two AZs."

**Generated Output (three-tier-architecture.drawio):**

```xml
<mxfile host="app.diagrams.net" agent="Claude" version="24.7.17">
  <diagram id="three-tier-1" name="Three-Tier Web App">
    <mxGraphModel dx="1434" dy="759" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="2" value="Users" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#232F3E;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.users;" vertex="1" parent="1">
          <mxGeometry x="40" y="340" width="60" height="60" as="geometry" />
        </mxCell>
        <mxCell id="3" value="AWS Cloud" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="1">
          <mxGeometry x="160" y="40" width="960" height="720" as="geometry" />
        </mxCell>
        <mxCell id="4" value="us-east-1" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor=#00A4A6;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=1;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="3">
          <mxGeometry x="20" y="40" width="920" height="660" as="geometry" />
        </mxCell>
        <mxCell id="5" value="VPC (10.0.0.0/16)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#AAB7B8;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="4">
          <mxGeometry x="20" y="40" width="880" height="600" as="geometry" />
        </mxCell>
        <mxCell id="6" value="Public Subnet (10.0.1.0/24)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;strokeColor=#7AA116;fillColor=#E9F3D2;verticalAlign=top;align=left;spacingLeft=30;fontColor=#248814;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="5">
          <mxGeometry x="20" y="40" width="400" height="160" as="geometry" />
        </mxCell>
        <mxCell id="7" value="Private Subnet (10.0.3.0/24)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="5">
          <mxGeometry x="20" y="230" width="400" height="160" as="geometry" />
        </mxCell>
        <mxCell id="8" value="Data Subnet (10.0.5.0/24)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;labelBackgroundColor=none;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;" vertex="1" parent="5">
          <mxGeometry x="20" y="420" width="400" height="160" as="geometry" />
        </mxCell>
        <mxCell id="12" value="Application&lt;br&gt;Load Balancer" style="sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;fillColor=#8C4FFF;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.applicationLoadBalancer;" vertex="1" parent="6">
          <mxGeometry x="170" y="50" width="60" height="60" as="geometry" />
        </mxCell>
        <mxCell id="13" value="EC2 Instance" style="sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;gradientColor=#F78E04;gradientDirection=north;fillColor=#D05C17;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;" vertex="1" parent="7">
          <mxGeometry x="170" y="50" width="60" height="60" as="geometry" />
        </mxCell>
        <mxCell id="15" value="RDS Primary" style="sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;gradientColor=#4D72F3;gradientDirection=north;fillColor=#3334B9;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;" vertex="1" parent="8">
          <mxGeometry x="170" y="50" width="60" height="60" as="geometry" />
        </mxCell>
        <mxCell id="20" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=open;endFill=0;strokeColor=#545B64;strokeWidth=2;" edge="1" parent="1" source="2" target="12">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="21" value="HTTPS" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=open;endFill=0;strokeColor=#545B64;strokeWidth=2;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="12" target="13">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="23" value="TCP 5432" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=open;endFill=0;strokeColor=#545B64;strokeWidth=2;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="13" target="15">
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

---

### Example 2: Serverless API Architecture

**User Request:**
"Create a serverless architecture diagram with API Gateway, Lambda functions, DynamoDB, and S3 for a REST API."

**Generated Output:** XML file con API Gateway (violet #E7157B), Lambda functions (orange #ED7100), DynamoDB (pink #C925D1), S3 (green #3F8624). See `references/aws-architecture-templates.md` for the complete template.

---

### Reference Files

See the `references/` directory for:
- `aws-shape-reference.md` - Complete AWS4 shape catalog with styles for 50+ AWS services
- `aws-architecture-templates.md` - Ready-to-use architecture templates (3-tier, serverless, data pipeline)

## Constraints and Warnings

### Critical Constraints

1. **XML must be well-formed**: Invalid XML will fail to open in draw.io. Always:
   - Close all tags properly (`<mxCell ... />` or `<mxCell>...</mxCell>`)
   - Escape special characters in attributes: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`
   - Use proper XML entities for labels (e.g., `&lt;br&gt;` for line breaks)

2. **ID uniqueness is mandatory**:
   - IDs "0" and "1" are reserved for root cells
   - All other IDs must be unique integers starting from "2"
   - Duplicate IDs will cause the diagram to fail loading

3. **Coordinate system constraints**:
   - All coordinates must be positive integers (x ≥ 0, y ≥ 0)
   - Use multiples of 10 for grid alignment (e.g., x="100" not x="105")
   - Negative coordinates will place elements outside the visible canvas

4. **AWS4 library only**:
   - This skill only supports official AWS4 shapes (`mxgraph.aws4.*`)
   - Legacy AWS shapes (`mxgraph.aws3.*`) are not supported
   - Generic shapes should use `fillColor=#232F3E` (AWS gray)

5. **Parent references must be valid**:
   - The `parent` attribute must reference an existing cell ID
   - Groups with `container=1` must be referenced correctly by child elements
   - Invalid parent references will cause elements to disappear or render incorrectly

### Limitations

- **No dynamic layouts**: Generated XML has fixed positions; manual adjustment in draw.io may be needed for complex diagrams
- **Single page only**: Multi-page diagrams require multiple `<diagram>` elements (advanced feature)
- **No custom styling beyond AWS colors**: Deviating from official AWS colors reduces diagram professionalism
- **No auto-routing**: Connection paths are fixed; rearranging elements requires manual edge adjustment

### Security Considerations

- **No sensitive data in diagrams**: Avoid including real IP addresses, ARNs, or resource IDs in labels
- **Review before sharing**: XML files contain plain text that may expose internal architecture details
- **Validate downloaded templates**: When using `references/aws-architecture-templates.md`, review the XML before deploying to production documentation

## Best Practices

1. **Always use official AWS4 shapes** - Use `mxgraph.aws4.*` shapes for professional look
2. **Follow AWS color codes** - Use official AWS service category colors
3. **Use proper nesting** - AWS Cloud → Region → VPC → Subnet → Services
4. **Label everything** - Service names, CIDR blocks, ports, protocols
5. **Show data flow direction** - Use labeled arrows with protocols (HTTPS, gRPC)
6. **Include external actors** - Users, corporate data centers, third-party services
7. **Keep diagrams focused** - Max 15-20 service icons per diagram
8. **Use multi-page** - Separate overview, network, and detail diagrams into pages
9. **Add annotations** - Use text labels for important notes (e.g., "Multi-AZ", "Auto Scaling")
10. **Validate XML** - Ensure all IDs are unique, all source/target references exist
