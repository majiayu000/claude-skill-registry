---
name: aws-architecture-diagram
description: Generate Draw.io XML architecture diagrams with accurate AWS service icons. Use when the user asks to create, update, or visualize an AWS architecture diagram, or mentions Draw.io diagrams for AWS infrastructure.
user-invocable: true
argument-hint: "describe the AWS architecture to diagram"
---

# AWS Architecture Diagram Skill

Generate Draw.io XML architecture diagrams with accurate AWS service icons.

## When to use

When the user asks to create, update, or generate an AWS architecture diagram in Draw.io format.

## Workflow

### 1. Understand the request and confirm preferences

- Identify which AWS services are needed
- Determine the architecture pattern (three-tier, event-driven, data pipeline, RAG, etc.)
- **Assess the audience**: technical (detailed labels, protocol names) vs non-technical (step numbers, simplified descriptions)
- **Ask the user** (using AskUserQuestion) for:
  - **Language**: English or 日本語 for all labels, titles, and the companion guide
  - Any other preferences not already clear from the request

### 2. Look up icons

Read the relevant reference files to get exact shape names and colors:

- `references/aws-icons-compute.md` — EC2, Lambda, ECS, EKS, Fargate, ELB
- `references/aws-icons-storage-database.md` — S3, EBS, RDS, DynamoDB, Aurora, ElastiCache
- `references/aws-icons-networking.md` — VPC, CloudFront, Route 53, API Gateway, Direct Connect
- `references/aws-icons-app-integration.md` — SNS, SQS, EventBridge, Step Functions, CloudWatch, CloudFormation
- `references/aws-icons-analytics-ml.md` — Athena, Glue, Kinesis, OpenSearch, Bedrock, SageMaker
- `references/aws-icons-security.md` — IAM, Cognito, WAF, Shield, KMS, GuardDuty
- `references/aws-icons-common.md` — Users, servers, internet, groups, arrows

**CRITICAL**: Always look up icons before generating XML. Never guess icon names.

### 3. Plan the layout

Read `references/layout-guidelines.md` for spacing, nesting, and style rules.

Key layout decisions:
- Group nesting: AWS Cloud → Region → VPC → Subnet
- Primary flow direction (usually left-to-right)
- Where to place auxiliary services

### 4. Generate the Draw.io XML

Use `templates/base.drawio.xml` as the skeleton. Build XML with these patterns:

#### Service icon (colored background, white glyph)

```xml
<mxCell id="svc-lambda" value="Lambda" style="sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;fillColor=#ED7100;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;" vertex="1" parent="grp-subnet">
  <mxGeometry x="100" y="50" width="48" height="48" as="geometry" />
</mxCell>
```

**MANDATORY**: `strokeColor=#ffffff` for resourceIcon pattern. This makes the glyph white.

#### Dedicated shape (dark silhouette)

```xml
<mxCell id="res-lambda-fn" value="Lambda Function" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#ED7100;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.lambda_function;" vertex="1" parent="grp-subnet">
  <mxGeometry x="100" y="50" width="48" height="48" as="geometry" />
</mxCell>
```

#### Group container

```xml
<mxCell id="grp-vpc" value="VPC" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fontStyle=0;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc2;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#AAB7B8;dashed=0;" vertex="1" parent="grp-region">
  <mxGeometry x="30" y="40" width="800" height="400" as="geometry" />
</mxCell>
```

#### Edge (arrow)

```xml
<mxCell id="edge-1" value="HTTPS" style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;elbow=vertical;startArrow=none;endFill=1;strokeColor=#545B64;rounded=0;fontSize=10;fontColor=#545B64;" edge="1" source="svc-cloudfront" target="svc-apigw" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 5. Output

Choose a **descriptive kebab-case slug** that best describes the diagram content (e.g., `realtime-data-pipeline`, `event-driven-orders`, `multi-tier-web-app`). Use this slug for both output files.

#### 5a. Write the Draw.io file

- Write to `docs/<slug>.drawio` (e.g., `docs/realtime-data-pipeline.drawio`)

#### 5b. Write the companion guide

- Write to `docs/<slug>.md`
- This Markdown file helps readers understand the diagram. Include:
  - **Overview**: 1-2 sentence summary of what the architecture does
  - **Components**: Table of each AWS service in the diagram, its role, and why it was chosen
  - **Data flows**: Step-by-step explanation of each flow (matching the step numbers in the diagram if using Non-Technical Audience Mode)
  - **Key design decisions**: Brief notes on architectural choices (e.g., why serverless, why this database, why this region setup)
  - **Cost/scaling notes** (optional): Anything helpful for planning — e.g., "Lambda scales automatically", "OpenSearch Serverless has a minimum baseline cost"
- Write the guide in the same language the user chose for the diagram
- Tell the user both file paths and suggest opening the `.drawio` in Draw.io to verify

## Rules

1. **Always look up icons** in reference files before generating XML
2. **Use `strokeColor=#ffffff`** for all resourceIcon patterns (service-level icons)
3. **Use `strokeColor=none`** for all dedicated shapes (resource-level icons)
4. **Match fillColor to category** — never mix colors across categories
5. **Ask the user for language** (English or 日本語) — use consistently across diagram labels, titles, legend, and companion guide
6. **No HTML in labels** — plain text only
7. **Max 15-20 icons** per diagram for readability
8. **Edge color**: `#545B64` (AWS default gray)
9. **Font**: 12px for icon labels, 10px for edge labels
10. **Icon size**: 48×48 for both service and resource icons
11. **Single AWS Cloud group** — use one AWS Cloud group spanning the full diagram, not multiple
12. **Full-coverage background** — add a light `#F5F5F5` rounded rect behind everything (title, lanes, legend) so PNG export has a clean background instead of black

## Non-Technical Audience Mode

When the diagram targets non-technical viewers (managers, stakeholders, end users):

### Step-numbered edges
Replace technical labels (HTTPS, REST API, etc.) with circled step numbers:
- Flow A: ① ② ③ ④ (white circled)
- Flow B: ❶ ❷ ❸ ❹ (black circled)
- Use different circle styles per flow for visual distinction

### Simplified labels
- Use plain Japanese descriptions instead of technical terms
- Examples: "チケット取得" not "REST API call", "AI学習用に変換" not "チャンク分割・埋め込み", "検索データベース" not "k-NNベクトルインデックス"
- Drop technical qualifiers: "OpenSearch" not "OpenSearch Serverless", "VPN接続" not "Site-to-Site VPN"

### Lane layout with flow summaries
When a diagram has multiple flows (e.g., data processing + search), use swim lanes:
- Add a step-by-step summary in each lane header: e.g., `"① チケット取得 → ② データ保存 → ③ AI変換 → ④ 索引化"`
- Use a dashed vertical line to separate lanes instead of separate colored blocks
- Place the legend outside colored lanes for visibility

### Background and legend
- One big `#F5F5F5` rounded rect behind everything (title + lanes + legend)
- Legend text: `fontColor=#232F3E` (not gray) for readability on any export background
- Legend maps step numbers to short descriptions

## Managed Services and VPC Endpoints Pattern

When a diagram includes AWS managed services (S3, Bedrock, OpenSearch, etc.) accessed from within a VPC:

### Two-box layout
- **VPC box** (left): Contains user-deployed resources (EC2, Lambda, NAT Gateway, etc.)
- **Managed Services box** (right): A plain rounded-rect group containing AWS managed services that live outside the VPC (S3, Bedrock KB, OpenSearch, Bedrock Claude, etc.)
- **VPC Endpoints icon**: Placed on the boundary between the two boxes — visually sitting between VPC and Managed Services to communicate "this is the bridge"
- Both boxes sit inside the single AWS Cloud group

### Managed Services group style
```
rounded=1;whiteSpace=wrap;fillColor=none;strokeColor=#879196;strokeWidth=1;dashed=1;dashPattern=4 4;fontColor=#232F3E;fontSize=12;fontStyle=1;verticalAlign=top;align=left;spacingLeft=10;spacingTop=8;container=1;collapsible=0;
```

### Arrow routing
- Arrows go **directly** from source to target (e.g., Lambda → S3, EC2 → Bedrock KB) — do NOT route arrows through the VPC Endpoints icon
- The visual separation (two boxes + icon between them) already communicates that connections cross the VPC boundary via VPC Endpoints
- The companion guide explains the VPC Endpoint detail

### When to use this pattern
- The architecture uses a VPC with VPC Endpoints for private connectivity
- Multiple managed services are accessed from within the VPC
- The audience benefits from seeing a clear boundary between "your infrastructure" and "AWS managed services"

## Category Color Reference

| Category | fillColor |
|---|---|
| Compute & Containers | `#ED7100` |
| Storage | `#7AA116` |
| Database | `#C925D1` |
| Networking & CDN | `#8C4FFF` |
| Analytics | `#8C4FFF` |
| App Integration & Mgmt | `#E7157B` |
| AI / Machine Learning | `#01A88D` |
| Security | `#DD344C` |
| General | `#232F3E` |
