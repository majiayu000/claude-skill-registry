---
name: pulumi-components
description: Use when building reusable infrastructure components with Pulumi for modular, composable cloud resources.
allowed-tools: [Bash, Read]
---

# Pulumi Components

Build reusable infrastructure components with Pulumi to create modular, composable, and maintainable infrastructure.

## Overview

Pulumi ComponentResources allow you to create higher-level abstractions that encapsulate multiple cloud resources into logical units. This enables code reuse, better organization, and more maintainable infrastructure code.

## Basic ComponentResource

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface WebServerArgs {
    instanceType?: pulumi.Input<string>;
    ami?: pulumi.Input<string>;
    subnetId: pulumi.Input<string>;
    vpcId: pulumi.Input<string>;
}

export class WebServer extends pulumi.ComponentResource {
    public readonly instance: aws.ec2.Instance;
    public readonly securityGroup: aws.ec2.SecurityGroup;
    public readonly publicIp: pulumi.Output<string>;

    constructor(name: string, args: WebServerArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:infrastructure:WebServer", name, {}, opts);

        const defaultOpts = { parent: this };

        // Create security group
        this.securityGroup = new aws.ec2.SecurityGroup(`${name}-sg`, {
            vpcId: args.vpcId,
            description: "Security group for web server",
            ingress: [
                {
                    protocol: "tcp",
                    fromPort: 80,
                    toPort: 80,
                    cidrBlocks: ["0.0.0.0/0"],
                },
                {
                    protocol: "tcp",
                    fromPort: 443,
                    toPort: 443,
                    cidrBlocks: ["0.0.0.0/0"],
                },
            ],
            egress: [{
                protocol: "-1",
                fromPort: 0,
                toPort: 0,
                cidrBlocks: ["0.0.0.0/0"],
            }],
            tags: {
                Name: `${name}-sg`,
            },
        }, defaultOpts);

        // Create EC2 instance
        this.instance = new aws.ec2.Instance(`${name}-instance`, {
            instanceType: args.instanceType || "t3.micro",
            ami: args.ami,
            subnetId: args.subnetId,
            vpcSecurityGroupIds: [this.securityGroup.id],
            tags: {
                Name: `${name}-instance`,
            },
        }, defaultOpts);

        this.publicIp = this.instance.publicIp;

        this.registerOutputs({
            instance: this.instance,
            securityGroup: this.securityGroup,
            publicIp: this.publicIp,
        });
    }
}
```

## Advanced VPC Component

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface VpcNetworkArgs {
    cidrBlock?: string;
    availabilityZones?: string[];
    enableNatGateway?: boolean;
    enableVpnGateway?: boolean;
    enableDnsHostnames?: boolean;
    enableDnsSupport?: boolean;
    privateSubnetCidrs?: string[];
    publicSubnetCidrs?: string[];
    tags?: { [key: string]: string };
}

export class VpcNetwork extends pulumi.ComponentResource {
    public readonly vpc: aws.ec2.Vpc;
    public readonly publicSubnets: aws.ec2.Subnet[];
    public readonly privateSubnets: aws.ec2.Subnet[];
    public readonly internetGateway: aws.ec2.InternetGateway;
    public readonly natGateways?: aws.ec2.NatGateway[];
    public readonly publicRouteTable: aws.ec2.RouteTable;
    public readonly privateRouteTables: aws.ec2.RouteTable[];
    public readonly vpcId: pulumi.Output<string>;

    constructor(name: string, args: VpcNetworkArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:network:VpcNetwork", name, {}, opts);

        const defaultOpts = { parent: this };
        const cidrBlock = args.cidrBlock || "10.0.0.0/16";
        const azs = args.availabilityZones || ["us-east-1a", "us-east-1b"];
        const publicCidrs = args.publicSubnetCidrs || ["10.0.1.0/24", "10.0.2.0/24"];
        const privateCidrs = args.privateSubnetCidrs || ["10.0.101.0/24", "10.0.102.0/24"];

        // Create VPC
        this.vpc = new aws.ec2.Vpc(`${name}-vpc`, {
            cidrBlock: cidrBlock,
            enableDnsHostnames: args.enableDnsHostnames !== false,
            enableDnsSupport: args.enableDnsSupport !== false,
            tags: {
                Name: `${name}-vpc`,
                ...args.tags,
            },
        }, defaultOpts);

        this.vpcId = this.vpc.id;

        // Create Internet Gateway
        this.internetGateway = new aws.ec2.InternetGateway(`${name}-igw`, {
            vpcId: this.vpc.id,
            tags: {
                Name: `${name}-igw`,
                ...args.tags,
            },
        }, defaultOpts);

        // Create public subnets
        this.publicSubnets = [];
        for (let i = 0; i < azs.length; i++) {
            const subnet = new aws.ec2.Subnet(`${name}-public-${i}`, {
                vpcId: this.vpc.id,
                cidrBlock: publicCidrs[i],
                availabilityZone: azs[i],
                mapPublicIpOnLaunch: true,
                tags: {
                    Name: `${name}-public-${azs[i]}`,
                    Type: "public",
                    ...args.tags,
                },
            }, defaultOpts);
            this.publicSubnets.push(subnet);
        }

        // Create private subnets
        this.privateSubnets = [];
        for (let i = 0; i < azs.length; i++) {
            const subnet = new aws.ec2.Subnet(`${name}-private-${i}`, {
                vpcId: this.vpc.id,
                cidrBlock: privateCidrs[i],
                availabilityZone: azs[i],
                tags: {
                    Name: `${name}-private-${azs[i]}`,
                    Type: "private",
                    ...args.tags,
                },
            }, defaultOpts);
            this.privateSubnets.push(subnet);
        }

        // Create public route table
        this.publicRouteTable = new aws.ec2.RouteTable(`${name}-public-rt`, {
            vpcId: this.vpc.id,
            tags: {
                Name: `${name}-public-rt`,
                ...args.tags,
            },
        }, defaultOpts);

        // Create route to Internet Gateway
        new aws.ec2.Route(`${name}-public-route`, {
            routeTableId: this.publicRouteTable.id,
            destinationCidrBlock: "0.0.0.0/0",
            gatewayId: this.internetGateway.id,
        }, defaultOpts);

        // Associate public subnets with public route table
        this.publicSubnets.forEach((subnet, i) => {
            new aws.ec2.RouteTableAssociation(`${name}-public-rta-${i}`, {
                subnetId: subnet.id,
                routeTableId: this.publicRouteTable.id,
            }, defaultOpts);
        });

        // Create NAT Gateways if enabled
        if (args.enableNatGateway !== false) {
            this.natGateways = [];
            this.publicSubnets.forEach((subnet, i) => {
                const eip = new aws.ec2.Eip(`${name}-nat-eip-${i}`, {
                    vpc: true,
                    tags: {
                        Name: `${name}-nat-eip-${i}`,
                        ...args.tags,
                    },
                }, defaultOpts);

                const natGw = new aws.ec2.NatGateway(`${name}-nat-${i}`, {
                    subnetId: subnet.id,
                    allocationId: eip.id,
                    tags: {
                        Name: `${name}-nat-${i}`,
                        ...args.tags,
                    },
                }, defaultOpts);
                this.natGateways.push(natGw);
            });
        }

        // Create private route tables
        this.privateRouteTables = [];
        this.privateSubnets.forEach((subnet, i) => {
            const rt = new aws.ec2.RouteTable(`${name}-private-rt-${i}`, {
                vpcId: this.vpc.id,
                tags: {
                    Name: `${name}-private-rt-${i}`,
                    ...args.tags,
                },
            }, defaultOpts);

            // Add NAT Gateway route if enabled
            if (this.natGateways && this.natGateways[i]) {
                new aws.ec2.Route(`${name}-private-route-${i}`, {
                    routeTableId: rt.id,
                    destinationCidrBlock: "0.0.0.0/0",
                    natGatewayId: this.natGateways[i].id,
                }, defaultOpts);
            }

            new aws.ec2.RouteTableAssociation(`${name}-private-rta-${i}`, {
                subnetId: subnet.id,
                routeTableId: rt.id,
            }, defaultOpts);

            this.privateRouteTables.push(rt);
        });

        this.registerOutputs({
            vpcId: this.vpcId,
            vpc: this.vpc,
            publicSubnets: this.publicSubnets,
            privateSubnets: this.privateSubnets,
            internetGateway: this.internetGateway,
            natGateways: this.natGateways,
        });
    }
}
```

## Database Component with RDS

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface DatabaseArgs {
    engine: "postgres" | "mysql" | "mariadb";
    engineVersion: string;
    instanceClass?: string;
    allocatedStorage?: number;
    databaseName: string;
    username: string;
    password: pulumi.Input<string>;
    vpcId: pulumi.Input<string>;
    subnetIds: pulumi.Input<string>[];
    backupRetentionPeriod?: number;
    multiAz?: boolean;
    allowedSecurityGroupIds?: pulumi.Input<string>[];
    allowedCidrBlocks?: string[];
}

export class Database extends pulumi.ComponentResource {
    public readonly instance: aws.rds.Instance;
    public readonly subnetGroup: aws.rds.SubnetGroup;
    public readonly securityGroup: aws.ec2.SecurityGroup;
    public readonly endpoint: pulumi.Output<string>;
    public readonly port: pulumi.Output<number>;

    constructor(name: string, args: DatabaseArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:database:Database", name, {}, opts);

        const defaultOpts = { parent: this };

        // Create DB subnet group
        this.subnetGroup = new aws.rds.SubnetGroup(`${name}-subnet-group`, {
            subnetIds: args.subnetIds,
            tags: {
                Name: `${name}-subnet-group`,
            },
        }, defaultOpts);

        // Create security group
        this.securityGroup = new aws.ec2.SecurityGroup(`${name}-sg`, {
            vpcId: args.vpcId,
            description: `Security group for ${name} database`,
            tags: {
                Name: `${name}-sg`,
            },
        }, defaultOpts);

        // Get port based on engine
        const portMap = {
            postgres: 5432,
            mysql: 3306,
            mariadb: 3306,
        };
        const dbPort = portMap[args.engine];

        // Add ingress rules for security groups
        if (args.allowedSecurityGroupIds) {
            args.allowedSecurityGroupIds.forEach((sgId, i) => {
                new aws.ec2.SecurityGroupRule(`${name}-sg-rule-${i}`, {
                    type: "ingress",
                    fromPort: dbPort,
                    toPort: dbPort,
                    protocol: "tcp",
                    sourceSecurityGroupId: sgId,
                    securityGroupId: this.securityGroup.id,
                }, defaultOpts);
            });
        }

        // Add ingress rules for CIDR blocks
        if (args.allowedCidrBlocks) {
            new aws.ec2.SecurityGroupRule(`${name}-sg-cidr-rule`, {
                type: "ingress",
                fromPort: dbPort,
                toPort: dbPort,
                protocol: "tcp",
                cidrBlocks: args.allowedCidrBlocks,
                securityGroupId: this.securityGroup.id,
            }, defaultOpts);
        }

        // Create RDS instance
        this.instance = new aws.rds.Instance(`${name}-instance`, {
            engine: args.engine,
            engineVersion: args.engineVersion,
            instanceClass: args.instanceClass || "db.t3.micro",
            allocatedStorage: args.allocatedStorage || 20,
            dbName: args.databaseName,
            username: args.username,
            password: args.password,
            dbSubnetGroupName: this.subnetGroup.name,
            vpcSecurityGroupIds: [this.securityGroup.id],
            backupRetentionPeriod: args.backupRetentionPeriod || 7,
            multiAz: args.multiAz || false,
            skipFinalSnapshot: true,
            tags: {
                Name: `${name}-instance`,
            },
        }, defaultOpts);

        this.endpoint = this.instance.endpoint;
        this.port = this.instance.port;

        this.registerOutputs({
            endpoint: this.endpoint,
            port: this.port,
            instance: this.instance,
        });
    }
}
```

## Container Application Component (ECS)

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface ContainerAppArgs {
    vpcId: pulumi.Input<string>;
    publicSubnetIds: pulumi.Input<string>[];
    privateSubnetIds: pulumi.Input<string>[];
    containerImage: string;
    containerPort: number;
    cpu?: number;
    memory?: number;
    desiredCount?: number;
    environment?: { [key: string]: string };
    secrets?: { [key: string]: pulumi.Input<string> };
}

export class ContainerApp extends pulumi.ComponentResource {
    public readonly cluster: aws.ecs.Cluster;
    public readonly taskDefinition: aws.ecs.TaskDefinition;
    public readonly service: aws.ecs.Service;
    public readonly loadBalancer: aws.lb.LoadBalancer;
    public readonly targetGroup: aws.lb.TargetGroup;
    public readonly dnsName: pulumi.Output<string>;

    constructor(name: string, args: ContainerAppArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:container:ContainerApp", name, {}, opts);

        const defaultOpts = { parent: this };

        // Create ECS cluster
        this.cluster = new aws.ecs.Cluster(`${name}-cluster`, {
            tags: {
                Name: `${name}-cluster`,
            },
        }, defaultOpts);

        // Create ALB security group
        const albSg = new aws.ec2.SecurityGroup(`${name}-alb-sg`, {
            vpcId: args.vpcId,
            description: "Security group for ALB",
            ingress: [
                {
                    protocol: "tcp",
                    fromPort: 80,
                    toPort: 80,
                    cidrBlocks: ["0.0.0.0/0"],
                },
                {
                    protocol: "tcp",
                    fromPort: 443,
                    toPort: 443,
                    cidrBlocks: ["0.0.0.0/0"],
                },
            ],
            egress: [{
                protocol: "-1",
                fromPort: 0,
                toPort: 0,
                cidrBlocks: ["0.0.0.0/0"],
            }],
            tags: {
                Name: `${name}-alb-sg`,
            },
        }, defaultOpts);

        // Create Application Load Balancer
        this.loadBalancer = new aws.lb.LoadBalancer(`${name}-alb`, {
            internal: false,
            loadBalancerType: "application",
            securityGroups: [albSg.id],
            subnets: args.publicSubnetIds,
            tags: {
                Name: `${name}-alb`,
            },
        }, defaultOpts);

        // Create target group
        this.targetGroup = new aws.lb.TargetGroup(`${name}-tg`, {
            port: args.containerPort,
            protocol: "HTTP",
            vpcId: args.vpcId,
            targetType: "ip",
            healthCheck: {
                enabled: true,
                path: "/health",
                interval: 30,
                timeout: 5,
                healthyThreshold: 2,
                unhealthyThreshold: 2,
            },
            tags: {
                Name: `${name}-tg`,
            },
        }, defaultOpts);

        // Create ALB listener
        new aws.lb.Listener(`${name}-listener`, {
            loadBalancerArn: this.loadBalancer.arn,
            port: 80,
            protocol: "HTTP",
            defaultActions: [{
                type: "forward",
                targetGroupArn: this.targetGroup.arn,
            }],
        }, defaultOpts);

        // Create task execution role
        const taskExecRole = new aws.iam.Role(`${name}-task-exec-role`, {
            assumeRolePolicy: aws.iam.assumeRolePolicyForPrincipal({
                Service: "ecs-tasks.amazonaws.com",
            }),
            tags: {
                Name: `${name}-task-exec-role`,
            },
        }, defaultOpts);

        new aws.iam.RolePolicyAttachment(`${name}-task-exec-policy`, {
            role: taskExecRole.name,
            policyArn: "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
        }, defaultOpts);

        // Build environment variables
        const envVars = Object.entries(args.environment || {}).map(([name, value]) => ({
            name,
            value,
        }));

        // Build secrets
        const secretVars = Object.entries(args.secrets || {}).map(([name, valueFrom]) => ({
            name,
            valueFrom,
        }));

        // Create task definition
        const containerDef = pulumi.all([
            pulumi.output(args.containerImage),
            pulumi.output(args.containerPort),
        ]).apply(([image, port]) => JSON.stringify([{
            name: `${name}-container`,
            image: image,
            cpu: args.cpu || 256,
            memory: args.memory || 512,
            essential: true,
            portMappings: [{
                containerPort: port,
                protocol: "tcp",
            }],
            environment: envVars,
            secrets: secretVars.length > 0 ? secretVars : undefined,
            logConfiguration: {
                logDriver: "awslogs",
                options: {
                    "awslogs-group": `/ecs/${name}`,
                    "awslogs-region": aws.getRegion().then(r => r.name),
                    "awslogs-stream-prefix": "ecs",
                },
            },
        }]));

        // Create CloudWatch log group
        new aws.cloudwatch.LogGroup(`${name}-logs`, {
            name: `/ecs/${name}`,
            retentionInDays: 7,
            tags: {
                Name: `${name}-logs`,
            },
        }, defaultOpts);

        this.taskDefinition = new aws.ecs.TaskDefinition(`${name}-task`, {
            family: name,
            cpu: String(args.cpu || 256),
            memory: String(args.memory || 512),
            networkMode: "awsvpc",
            requiresCompatibilities: ["FARGATE"],
            executionRoleArn: taskExecRole.arn,
            containerDefinitions: containerDef,
            tags: {
                Name: `${name}-task`,
            },
        }, defaultOpts);

        // Create service security group
        const serviceSg = new aws.ec2.SecurityGroup(`${name}-service-sg`, {
            vpcId: args.vpcId,
            description: "Security group for ECS service",
            ingress: [{
                protocol: "tcp",
                fromPort: args.containerPort,
                toPort: args.containerPort,
                securityGroups: [albSg.id],
            }],
            egress: [{
                protocol: "-1",
                fromPort: 0,
                toPort: 0,
                cidrBlocks: ["0.0.0.0/0"],
            }],
            tags: {
                Name: `${name}-service-sg`,
            },
        }, defaultOpts);

        // Create ECS service
        this.service = new aws.ecs.Service(`${name}-service`, {
            cluster: this.cluster.arn,
            taskDefinition: this.taskDefinition.arn,
            desiredCount: args.desiredCount || 2,
            launchType: "FARGATE",
            networkConfiguration: {
                subnets: args.privateSubnetIds,
                securityGroups: [serviceSg.id],
                assignPublicIp: false,
            },
            loadBalancers: [{
                targetGroupArn: this.targetGroup.arn,
                containerName: `${name}-container`,
                containerPort: args.containerPort,
            }],
            tags: {
                Name: `${name}-service`,
            },
        }, defaultOpts);

        this.dnsName = this.loadBalancer.dnsName;

        this.registerOutputs({
            dnsName: this.dnsName,
            cluster: this.cluster,
            service: this.service,
        });
    }
}
```

## S3 Static Website Component

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface StaticWebsiteArgs {
    domainName?: string;
    indexDocument?: string;
    errorDocument?: string;
    enableCdn?: boolean;
    certificateArn?: pulumi.Input<string>;
}

export class StaticWebsite extends pulumi.ComponentResource {
    public readonly bucket: aws.s3.Bucket;
    public readonly bucketPolicy: aws.s3.BucketPolicy;
    public readonly distribution?: aws.cloudfront.Distribution;
    public readonly websiteUrl: pulumi.Output<string>;

    constructor(name: string, args: StaticWebsiteArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:web:StaticWebsite", name, {}, opts);

        const defaultOpts = { parent: this };

        // Create S3 bucket
        this.bucket = new aws.s3.Bucket(`${name}-bucket`, {
            bucket: args.domainName || undefined,
            website: {
                indexDocument: args.indexDocument || "index.html",
                errorDocument: args.errorDocument || "error.html",
            },
            tags: {
                Name: `${name}-bucket`,
            },
        }, defaultOpts);

        // Block public access settings
        new aws.s3.BucketPublicAccessBlock(`${name}-public-access-block`, {
            bucket: this.bucket.id,
            blockPublicAcls: args.enableCdn !== false,
            blockPublicPolicy: args.enableCdn !== false,
            ignorePublicAcls: args.enableCdn !== false,
            restrictPublicBuckets: args.enableCdn !== false,
        }, defaultOpts);

        if (args.enableCdn !== false) {
            // Create CloudFront OAI
            const oai = new aws.cloudfront.OriginAccessIdentity(`${name}-oai`, {
                comment: `OAI for ${name}`,
            }, defaultOpts);

            // Bucket policy for CloudFront
            this.bucketPolicy = new aws.s3.BucketPolicy(`${name}-bucket-policy`, {
                bucket: this.bucket.id,
                policy: pulumi.all([this.bucket.arn, oai.iamArn]).apply(([bucketArn, oaiArn]) =>
                    JSON.stringify({
                        Version: "2012-10-17",
                        Statement: [{
                            Effect: "Allow",
                            Principal: {
                                AWS: oaiArn,
                            },
                            Action: "s3:GetObject",
                            Resource: `${bucketArn}/*`,
                        }],
                    })
                ),
            }, defaultOpts);

            // Create CloudFront distribution
            this.distribution = new aws.cloudfront.Distribution(`${name}-cdn`, {
                enabled: true,
                defaultRootObject: args.indexDocument || "index.html",
                origins: [{
                    originId: "s3Origin",
                    domainName: this.bucket.bucketRegionalDomainName,
                    s3OriginConfig: {
                        originAccessIdentity: oai.cloudfrontAccessIdentityPath,
                    },
                }],
                defaultCacheBehavior: {
                    targetOriginId: "s3Origin",
                    viewerProtocolPolicy: "redirect-to-https",
                    allowedMethods: ["GET", "HEAD", "OPTIONS"],
                    cachedMethods: ["GET", "HEAD"],
                    compress: true,
                    forwardedValues: {
                        queryString: false,
                        cookies: {
                            forward: "none",
                        },
                    },
                    minTtl: 0,
                    defaultTtl: 3600,
                    maxTtl: 86400,
                },
                restrictions: {
                    geoRestriction: {
                        restrictionType: "none",
                    },
                },
                viewerCertificate: args.certificateArn ? {
                    acmCertificateArn: args.certificateArn,
                    sslSupportMethod: "sni-only",
                    minimumProtocolVersion: "TLSv1.2_2021",
                } : {
                    cloudfrontDefaultCertificate: true,
                },
                aliases: args.domainName ? [args.domainName] : undefined,
                customErrorResponses: [{
                    errorCode: 404,
                    responseCode: 200,
                    responsePagePath: `/${args.errorDocument || "error.html"}`,
                }],
                tags: {
                    Name: `${name}-cdn`,
                },
            }, defaultOpts);

            this.websiteUrl = this.distribution.domainName.apply(d => `https://${d}`);
        } else {
            // Public bucket policy
            this.bucketPolicy = new aws.s3.BucketPolicy(`${name}-bucket-policy`, {
                bucket: this.bucket.id,
                policy: this.bucket.arn.apply(bucketArn =>
                    JSON.stringify({
                        Version: "2012-10-17",
                        Statement: [{
                            Effect: "Allow",
                            Principal: "*",
                            Action: "s3:GetObject",
                            Resource: `${bucketArn}/*`,
                        }],
                    })
                ),
            }, defaultOpts);

            this.websiteUrl = this.bucket.websiteEndpoint.apply(e => `http://${e}`);
        }

        this.registerOutputs({
            websiteUrl: this.websiteUrl,
            bucket: this.bucket,
            distribution: this.distribution,
        });
    }
}
```

## Kubernetes Application Component

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as k8s from "@pulumi/kubernetes";

export interface K8sAppArgs {
    namespace?: string;
    image: string;
    replicas?: number;
    port: number;
    resources?: {
        requests?: {
            memory?: string;
            cpu?: string;
        };
        limits?: {
            memory?: string;
            cpu?: string;
        };
    };
    environment?: { [key: string]: string };
    secrets?: { [key: string]: string };
    enableIngress?: boolean;
    ingressHost?: string;
}

export class K8sApp extends pulumi.ComponentResource {
    public readonly namespace: k8s.core.v1.Namespace;
    public readonly deployment: k8s.apps.v1.Deployment;
    public readonly service: k8s.core.v1.Service;
    public readonly ingress?: k8s.networking.v1.Ingress;
    public readonly configMap?: k8s.core.v1.ConfigMap;
    public readonly secret?: k8s.core.v1.Secret;

    constructor(name: string, args: K8sAppArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:k8s:K8sApp", name, {}, opts);

        const defaultOpts = { parent: this };
        const ns = args.namespace || "default";

        // Create namespace if specified
        if (args.namespace && args.namespace !== "default") {
            this.namespace = new k8s.core.v1.Namespace(`${name}-ns`, {
                metadata: {
                    name: args.namespace,
                },
            }, defaultOpts);
        }

        // Create ConfigMap for environment variables
        if (args.environment && Object.keys(args.environment).length > 0) {
            this.configMap = new k8s.core.v1.ConfigMap(`${name}-config`, {
                metadata: {
                    name: `${name}-config`,
                    namespace: ns,
                },
                data: args.environment,
            }, defaultOpts);
        }

        // Create Secret
        if (args.secrets && Object.keys(args.secrets).length > 0) {
            this.secret = new k8s.core.v1.Secret(`${name}-secret`, {
                metadata: {
                    name: `${name}-secret`,
                    namespace: ns,
                },
                stringData: args.secrets,
            }, defaultOpts);
        }

        // Build environment variables
        const envVars: any[] = [];

        if (this.configMap) {
            Object.keys(args.environment || {}).forEach(key => {
                envVars.push({
                    name: key,
                    valueFrom: {
                        configMapKeyRef: {
                            name: `${name}-config`,
                            key: key,
                        },
                    },
                });
            });
        }

        if (this.secret) {
            Object.keys(args.secrets || {}).forEach(key => {
                envVars.push({
                    name: key,
                    valueFrom: {
                        secretKeyRef: {
                            name: `${name}-secret`,
                            key: key,
                        },
                    },
                });
            });
        }

        // Create Deployment
        this.deployment = new k8s.apps.v1.Deployment(`${name}-deployment`, {
            metadata: {
                name: `${name}-deployment`,
                namespace: ns,
                labels: {
                    app: name,
                },
            },
            spec: {
                replicas: args.replicas || 3,
                selector: {
                    matchLabels: {
                        app: name,
                    },
                },
                template: {
                    metadata: {
                        labels: {
                            app: name,
                        },
                    },
                    spec: {
                        containers: [{
                            name: name,
                            image: args.image,
                            ports: [{
                                containerPort: args.port,
                            }],
                            env: envVars.length > 0 ? envVars : undefined,
                            resources: args.resources,
                            livenessProbe: {
                                httpGet: {
                                    path: "/health",
                                    port: args.port,
                                },
                                initialDelaySeconds: 30,
                                periodSeconds: 10,
                            },
                            readinessProbe: {
                                httpGet: {
                                    path: "/ready",
                                    port: args.port,
                                },
                                initialDelaySeconds: 10,
                                periodSeconds: 5,
                            },
                        }],
                    },
                },
            },
        }, defaultOpts);

        // Create Service
        this.service = new k8s.core.v1.Service(`${name}-service`, {
            metadata: {
                name: `${name}-service`,
                namespace: ns,
                labels: {
                    app: name,
                },
            },
            spec: {
                selector: {
                    app: name,
                },
                ports: [{
                    port: 80,
                    targetPort: args.port,
                    protocol: "TCP",
                }],
                type: args.enableIngress ? "ClusterIP" : "LoadBalancer",
            },
        }, defaultOpts);

        // Create Ingress if enabled
        if (args.enableIngress && args.ingressHost) {
            this.ingress = new k8s.networking.v1.Ingress(`${name}-ingress`, {
                metadata: {
                    name: `${name}-ingress`,
                    namespace: ns,
                    annotations: {
                        "kubernetes.io/ingress.class": "nginx",
                        "cert-manager.io/cluster-issuer": "letsencrypt-prod",
                    },
                },
                spec: {
                    tls: [{
                        hosts: [args.ingressHost],
                        secretName: `${name}-tls`,
                    }],
                    rules: [{
                        host: args.ingressHost,
                        http: {
                            paths: [{
                                path: "/",
                                pathType: "Prefix",
                                backend: {
                                    service: {
                                        name: `${name}-service`,
                                        port: {
                                            number: 80,
                                        },
                                    },
                                },
                            }],
                        },
                    }],
                },
            }, defaultOpts);
        }

        this.registerOutputs({
            deployment: this.deployment,
            service: this.service,
            ingress: this.ingress,
        });
    }
}
```

## Lambda Function Component

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface LambdaFunctionArgs {
    runtime: aws.lambda.Runtime;
    handler: string;
    code: pulumi.asset.AssetArchive | pulumi.asset.FileArchive;
    environment?: { [key: string]: string };
    timeout?: number;
    memorySize?: number;
    vpcConfig?: {
        subnetIds: pulumi.Input<string>[];
        securityGroupIds: pulumi.Input<string>[];
    };
    policies?: pulumi.Input<string>[];
    layers?: pulumi.Input<string>[];
}

export class LambdaFunction extends pulumi.ComponentResource {
    public readonly function: aws.lambda.Function;
    public readonly role: aws.iam.Role;
    public readonly logGroup: aws.cloudwatch.LogGroup;
    public readonly arn: pulumi.Output<string>;

    constructor(name: string, args: LambdaFunctionArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:serverless:LambdaFunction", name, {}, opts);

        const defaultOpts = { parent: this };

        // Create IAM role
        this.role = new aws.iam.Role(`${name}-role`, {
            assumeRolePolicy: aws.iam.assumeRolePolicyForPrincipal({
                Service: "lambda.amazonaws.com",
            }),
            tags: {
                Name: `${name}-role`,
            },
        }, defaultOpts);

        // Attach basic Lambda execution policy
        new aws.iam.RolePolicyAttachment(`${name}-basic-policy`, {
            role: this.role.name,
            policyArn: "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
        }, defaultOpts);

        // Attach VPC execution policy if VPC config provided
        if (args.vpcConfig) {
            new aws.iam.RolePolicyAttachment(`${name}-vpc-policy`, {
                role: this.role.name,
                policyArn: "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole",
            }, defaultOpts);
        }

        // Attach additional policies
        if (args.policies) {
            args.policies.forEach((policyArn, i) => {
                new aws.iam.RolePolicyAttachment(`${name}-policy-${i}`, {
                    role: this.role.name,
                    policyArn: policyArn,
                }, defaultOpts);
            });
        }

        // Create CloudWatch log group
        this.logGroup = new aws.cloudwatch.LogGroup(`${name}-logs`, {
            name: `/aws/lambda/${name}`,
            retentionInDays: 14,
            tags: {
                Name: `${name}-logs`,
            },
        }, defaultOpts);

        // Create Lambda function
        this.function = new aws.lambda.Function(`${name}-function`, {
            runtime: args.runtime,
            handler: args.handler,
            code: args.code,
            role: this.role.arn,
            timeout: args.timeout || 30,
            memorySize: args.memorySize || 256,
            environment: args.environment ? {
                variables: args.environment,
            } : undefined,
            vpcConfig: args.vpcConfig,
            layers: args.layers,
            tags: {
                Name: `${name}-function`,
            },
        }, defaultOpts);

        this.arn = this.function.arn;

        this.registerOutputs({
            arn: this.arn,
            function: this.function,
        });
    }
}
```

## When to Use This Skill

Use the `pulumi-components` skill when you need to:

- Create reusable infrastructure abstractions
- Encapsulate multiple resources into logical units
- Build infrastructure libraries for your organization
- Implement complex multi-resource patterns
- Ensure consistent resource configurations
- Create higher-level infrastructure APIs
- Share infrastructure code across projects
- Build opinionated infrastructure templates
- Manage resource relationships and dependencies
- Create self-contained infrastructure modules

## Best Practices

1. **Use Parent Relationships**: Always set `{ parent: this }` when creating child resources to maintain proper resource hierarchy
2. **Register Outputs**: Call `registerOutputs()` at the end of constructor to expose component properties
3. **Type Safety**: Use TypeScript interfaces for component arguments with clear types
4. **Input Types**: Use `pulumi.Input<T>` for arguments that can be outputs from other resources
5. **Naming Convention**: Prefix child resource names with the component name for clarity
6. **Default Options**: Create a `defaultOpts` object with parent set for all child resources
7. **Documentation**: Add JSDoc comments explaining component purpose and usage
8. **Composition Over Inheritance**: Favor creating components that compose other components
9. **Single Responsibility**: Each component should encapsulate a single logical infrastructure unit
10. **Explicit Dependencies**: Don't rely on implicit dependencies; make them explicit in code
11. **Resource Groups**: Use tags consistently across all resources in a component
12. **Error Handling**: Validate inputs in the constructor before creating resources
13. **Immutability**: Avoid modifying component state after construction
14. **Export Typed Outputs**: Export strongly-typed outputs for use by consumers
15. **Provider Configuration**: Allow provider configuration to be passed through opts

## Common Pitfalls

1. **Missing Parent**: Forgetting to set `parent: this` breaks resource hierarchy and prevents proper deletion
2. **Not Registering Outputs**: Forgetting `registerOutputs()` prevents output tracking
3. **Incorrect Type URN**: Using wrong format for component type (should be `category:subcategory:Name`)
4. **Circular Dependencies**: Creating circular references between components
5. **Improper Output Handling**: Not using `pulumi.Output.apply()` for dependent values
6. **Hardcoded Values**: Hardcoding values that should be configurable arguments
7. **Missing Resource Names**: Not prefixing child resource names can cause name conflicts
8. **Inconsistent Tagging**: Not applying consistent tags across all component resources
9. **Overly Complex Components**: Creating components that do too much
10. **Poor Abstraction Level**: Creating components at wrong abstraction level (too high or too low)
11. **Missing Validation**: Not validating required arguments before resource creation
12. **State Mutations**: Mutating component state after construction
13. **Implicit Dependencies**: Relying on Pulumi to figure out dependencies instead of being explicit
14. **Missing Error Messages**: Not providing helpful error messages for invalid configurations
15. **Tight Coupling**: Creating components that are too tightly coupled to specific implementations

## Resources

- [Pulumi ComponentResource Documentation](https://www.pulumi.com/docs/intro/concepts/resources/components/)
- [Pulumi Resource Options](https://www.pulumi.com/docs/intro/concepts/resources/options/)
- [Pulumi Best Practices](https://www.pulumi.com/docs/guides/best-practices/)
- [Component Resource Examples](https://github.com/pulumi/examples)
- [Pulumi TypeScript API](https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/pulumi/)
