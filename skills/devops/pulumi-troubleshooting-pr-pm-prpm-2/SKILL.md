---
name: pulumi-troubleshooting
description: Comprehensive guide to troubleshooting Pulumi TypeScript errors, infrastructure issues, and best practices - covers common errors, Outputs handling, AWS Beanstalk deployment, and cost optimization
---

# Pulumi Infrastructure Troubleshooting Skill

## Common Pulumi TypeScript Errors and Solutions

### 1. "This expression is not callable. Type 'never' has no call signatures"

**Cause**: TypeScript infers a type as `never` when working with Pulumi Outputs, especially with arrays.

**Solution**: Wrap the value in `pulumi.output()` and properly type the callback:
```typescript
// ❌ Bad - TypeScript can't infer the type
value: pulumi.all(config.vpc.publicSubnets.map((s: any) => s.id))

// ✅ Good - Explicitly wrap and type
value: pulumi.output(config.vpc.publicSubnets).apply((subnets: any[]) =>
  pulumi.all(subnets.map((s: any) => s.id)).apply(ids => ids.join(","))
)
```

### 2. "Modifiers cannot appear here" (export in conditional blocks)

**Cause**: TypeScript doesn't allow `export` statements inside `if` blocks.

**Solution**: Use optional chaining for conditional exports:
```typescript
// ❌ Bad
if (opensearch) {
  export const opensearchEndpoint = opensearch.endpoint;
}

// ✅ Good
export const opensearchEndpoint = opensearch?.endpoint;
```

### 3. "Configuration key 'aws:region' is not namespaced by the project"

**Cause**: Pulumi.yaml config with namespaced keys (e.g., `aws:region`) cannot use `default` attribute.

**Solution**: Remove the config section or don't set defaults for provider configs:
```yaml
# ❌ Bad
config:
  aws:region:
    description: AWS region
    default: us-east-1

# ✅ Good - set via workflow/CLI instead
config:
  app:domainName:
    description: Domain name
```

### 4. Stack Not Found Errors

**Cause**: Pulumi stack doesn't exist yet in new environments.

**Solution**: Use `||` operator to create if not exists:
```bash
pulumi stack select $STACK || pulumi stack init $STACK
```

### 5. Working with Pulumi Outputs

**Key Concepts**:
- `pulumi.Output<T>` is a promise-like wrapper for async values
- Use `.apply()` to transform Output values
- Use `pulumi.all([...])` to combine multiple Outputs
- Use `pulumi.output(value)` to wrap plain values as Outputs

**Common Patterns**:
```typescript
// Transforming a single Output
const url = endpoint.apply(e => `https://${e}`);

// Combining multiple Outputs
const connectionString = pulumi.all([host, port, db]).apply(
  ([h, p, d]) => `postgres://${h}:${p}/${d}`
);

// Interpolating Outputs
const message = pulumi.interpolate`Server at ${endpoint}:${port}`;
```

**Nested Outputs** (Properties that are themselves Outputs):
```typescript
// ❌ Bad - resource.property might be an Output<string>
const endpoint = instance.apply(i => i.endpoint.split(":")[0]); // ERROR: Property 'split' does not exist

// ✅ Good - unwrap nested Output with pulumi.output()
const endpoint = instance.apply(i =>
  pulumi.output(i.endpoint).apply(e => e.split(":")[0])
);

// ✅ Alternative - use pulumi.all to flatten
const endpoint = pulumi.all([instance]).apply(([inst]) =>
  pulumi.output(inst.endpoint).apply(e => e.split(":")[0])
);
```

### 6. Beanstalk Environment Variables

**Issue**: Complex objects or arrays need to be serialized.

**Solution**: Use JSON.stringify for complex values:
```typescript
{
  namespace: "aws:elasticbeanstalk:application:environment",
  name: "ALLOWED_ORIGINS",
  value: allowedOrigins.apply(origins => JSON.stringify(origins)),
}
```

### 7. ACM Certificate Validation

**Issue**: Certificate validation hangs or times out.

**Solution**: Ensure DNS records are created and wait for validation:
```typescript
// 1. Create certificate
const cert = new aws.acm.Certificate(...);

// 2. Create DNS validation record
const validationRecord = new aws.route53.Record(..., {
  name: cert.domainValidationOptions[0].resourceRecordName,
  type: cert.domainValidationOptions[0].resourceRecordType,
  records: [cert.domainValidationOptions[0].resourceRecordValue],
});

// 3. Wait for validation to complete
const validation = new aws.acm.CertificateValidation(..., {
  certificateArn: cert.arn,
  validationRecordFqdns: [validationRecord.fqdn],
});
```

### 8. GitHub Actions Pulumi Setup

**Best Practices**:
```yaml
- name: Setup Pulumi
  uses: pulumi/actions@v5

- name: Configure Stack
  run: |
    STACK="${{ inputs.stack || 'prod' }}"
    pulumi stack select $STACK || pulumi stack init $STACK
    pulumi config set aws:region ${{ env.AWS_REGION }}
    # Set other non-secret configs here

- name: Pulumi Up
  run: pulumi up --yes --non-interactive
  env:
    PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
    PULUMI_CONFIG_PASSPHRASE: ${{ secrets.PULUMI_CONFIG_PASSPHRASE }}
```

### 9. Debugging TypeScript Compilation

**Quick checks**:
1. Run `npm run build` in the infra package locally
2. Check for conditional exports inside blocks
3. Verify all Pulumi Outputs are properly typed
4. Look for `.map()` calls on potentially undefined arrays
5. Ensure all imports are correct

### 10. Cost Optimization Tips

**Beanstalk vs ECS Fargate**:
- Beanstalk with t3.micro: ~$32/month
- ECS Fargate: ~$126/month
- Key difference: Beanstalk runs on EC2 instances you control
- Use public subnets to avoid NAT Gateway costs ($32/month)

## Checklist Before Deploying

- [ ] Run `npm run build` locally to catch TypeScript errors
- [ ] Test with `pulumi preview` before `pulumi up`
- [ ] Verify all secrets are in GitHub Secrets (not hardcoded)
- [ ] Check stack name matches environment (dev/staging/prod)
- [ ] Ensure domain/DNS is configured if using custom domains
- [ ] Verify VPC/subnets exist if using existing infrastructure
- [ ] Check that all required extensions/providers are installed

## Common Environment Variables to Set

```typescript
// Database
DATABASE_URL: pulumi.interpolate`postgres://${user}:${pass}@${host}:5432/${db}`

// Redis
REDIS_URL: redisEndpoint.apply(e => `redis://${e}:6379`)

// S3
S3_BUCKET: bucketName
S3_REGION: region

// Auth
GITHUB_CLIENT_ID: clientId
GITHUB_CLIENT_SECRET: clientSecret

// App Config
NODE_ENV: "production"
PORT: "8080"
LOG_LEVEL: "info"
```

## Resources

- [Pulumi TypeScript Docs](https://www.pulumi.com/docs/languages-sdks/javascript/)
- [AWS Provider Docs](https://www.pulumi.com/registry/packages/aws/)
- [Pulumi Outputs Guide](https://www.pulumi.com/docs/concepts/inputs-outputs/)
