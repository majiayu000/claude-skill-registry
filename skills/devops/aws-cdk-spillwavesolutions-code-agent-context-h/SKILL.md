# AWS CDK Skill

This skill provides guidance for AWS CDK development.

## Best Practices

1. Use TypeScript for type safety
2. Follow the construct hierarchy: App > Stack > Construct
3. Use environment-specific configurations
4. Implement proper tagging strategies

## Common Patterns

- Use `cdk.CfnOutput` for stack outputs
- Leverage `cdk.Aspects` for cross-cutting concerns
- Use `cdk.Tags` for resource tagging
