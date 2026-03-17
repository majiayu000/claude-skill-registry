# ☁️ Skill: AWS Backend Deployment

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-aws` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `aws`, `eks`, `rds`, `s3`, `lambda`, `cloud` |
| **Referencia** | [AWS Docs](https://docs.aws.amazon.com/) |

## 🔑 Keywords para Invocación

- `aws`
- `eks`
- `rds`
- `s3`
- `lambda`
- `@skill:aws`

## 📖 Descripción

AWS proporciona servicios cloud para backends de Flutter: EKS para containers, RDS para databases, S3 para storage, Lambda para serverless, API Gateway y más.

## 💻 Servicios Principales para Backend Flutter

### 1. EKS (Elastic Kubernetes Service)

```bash
# Crear cluster con eksctl
eksctl create cluster \
  --name myapp-prod \
  --version 1.28 \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 10 \
  --managed

# Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name myapp-prod
```

### 2. RDS (Relational Database Service)

```bash
# Crear PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier myapp-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.4 \
  --master-username admin \
  --master-user-password SecurePassword123! \
  --allocated-storage 20 \
  --storage-type gp3 \
  --storage-encrypted \
  --multi-az \
  --backup-retention-period 7
```

### 3. S3 (Storage)

```bash
# Crear bucket
aws s3 mb s3://myapp-storage-prod

# Configurar CORS para Flutter app
aws s3api put-bucket-cors --bucket myapp-storage-prod --cors-configuration '{
  "CORSRules": [{
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3000
  }]
}'

# Configurar lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket myapp-storage-prod \
  --lifecycle-configuration file://lifecycle.json
```

### 4. Lambda + API Gateway (Serverless Backend)

```javascript
// handler.js
exports.handler = async (event) => {
  const body = JSON.parse(event.body);

  // Your business logic
  const response = {
    message: 'Hello from Lambda!',
    input: body
  };

  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    },
    body: JSON.stringify(response)
  };
};
```

```bash
# Deploy Lambda
zip function.zip handler.js
aws lambda create-function \
  --function-name myapp-api \
  --runtime nodejs20.x \
  --handler handler.handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::123456789012:role/lambda-execution
```

### 5. ElastiCache (Redis)

```bash
# Crear Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id myapp-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --engine-version 7.0 \
  --num-cache-nodes 1 \
  --cache-subnet-group-name myapp-subnet-group
```

### 6. Secrets Manager

```bash
# Store database credentials
aws secretsmanager create-secret \
  --name prod/database/credentials \
  --secret-string '{
    "username": "admin",
    "password": "SecurePassword123!",
    "host": "myapp-db.xxxxx.us-east-1.rds.amazonaws.com",
    "port": 5432,
    "database": "myapp_prod"
  }'

# Retrieve secret
aws secretsmanager get-secret-value \
  --secret-id prod/database/credentials \
  --query SecretString \
  --output text
```

### 7. CloudWatch (Monitoring)

```bash
# Create log group
aws logs create-log-group --log-group-name /aws/backend/myapp

# Put metric
aws cloudwatch put-metric-data \
  --namespace MyApp \
  --metric-name RequestCount \
  --value 1 \
  --dimensions Environment=production
```

### 8. IAM Roles for Backend

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::myapp-storage-prod/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:*:*:secret:prod/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

### 9. AWS CDK (Infrastructure as Code)

```typescript
// lib/backend-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as eks from 'aws-cdk-lib/aws-eks';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class BackendStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // EKS Cluster
    const cluster = new eks.Cluster(this, 'MyAppCluster', {
      version: eks.KubernetesVersion.V1_28,
      defaultCapacity: 3,
      defaultCapacityInstance: cdk.aws_ec2.InstanceType.of(
        cdk.aws_ec2.InstanceClass.T3,
        cdk.aws_ec2.InstanceSize.MEDIUM
      ),
    });

    // RDS Database
    const database = new rds.DatabaseInstance(this, 'MyAppDB', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_15_4,
      }),
      instanceType: cdk.aws_ec2.InstanceType.of(
        cdk.aws_ec2.InstanceClass.T3,
        cdk.aws_ec2.InstanceSize.MICRO
      ),
      vpc: cluster.vpc,
      multiAz: true,
      allocatedStorage: 20,
      maxAllocatedStorage: 100,
      backupRetention: cdk.Duration.days(7),
    });

    // S3 Bucket
    const bucket = new s3.Bucket(this, 'MyAppStorage', {
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
      cors: [{
        allowedMethods: [s3.HttpMethods.GET, s3.HttpMethods.PUT],
        allowedOrigins: ['*'],
        allowedHeaders: ['*'],
      }],
    });
  }
}
```

## 🎯 Mejores Prácticas

1. **Use VPC** para aislamiento de red
2. **Enable encryption** en rest y en tránsito
3. **Tag resources** para cost tracking
4. **Use Secrets Manager** para credentials
5. **Enable CloudWatch** logging y monitoring
6. **Use IAM roles** en lugar de access keys
7. **Enable MFA** para usuarios críticos
8. **Regular backups** con RDS automated backups

## 📚 Recursos

- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

## 🔗 Skills Relacionados

- [Terraform](../terraform/SKILL.md)
- [EKS](../kubernetes/SKILL.md)
- [ArgoCD](../argocd/SKILL.md)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
