---
name: aws-ec2-deployment
description: Launch, configure, and manage EC2 instances with best practices
sasmp_version: "1.3.0"
bonded_agent: 02-aws-compute
bond_type: PRIMARY_BOND
---

# AWS EC2 Deployment Skill

Deploy and manage EC2 instances with production-ready configurations.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Service | EC2 |
| Complexity | Medium |
| Est. Time | 5-15 min |
| Prerequisites | VPC, Security Group, Key Pair |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| instance_type | string | EC2 instance type | Valid type (m6i.large) |
| ami_id | string | AMI ID | ami-[a-z0-9]{17} |
| subnet_id | string | Target subnet | subnet-[a-z0-9]{17} |
| security_group_ids | array | Security groups | Non-empty array |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| key_name | string | null | SSH key pair name |
| iam_instance_profile | string | null | IAM role ARN |
| user_data | string | null | Base64 startup script |
| ebs_optimized | bool | true | EBS optimization |
| monitoring | bool | true | Detailed monitoring |

## Implementation

### Launch Instance
```bash
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type m6i.large \
  --subnet-id subnet-12345678 \
  --security-group-ids sg-12345678 \
  --key-name my-key \
  --iam-instance-profile Name=MyRole \
  --ebs-optimized \
  --monitoring Enabled=true \
  --metadata-options HttpTokens=required \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyServer}]'
```

### User Data Script
```bash
#!/bin/bash
set -e
yum update -y
yum install -y docker
systemctl enable docker
systemctl start docker
```

## Retry Logic

```python
def launch_with_retry(params, max_retries=3):
    for attempt in range(max_retries):
        try:
            return ec2.run_instances(**params)
        except ec2.exceptions.InsufficientInstanceCapacity:
            params['SubnetId'] = get_alternate_subnet()
            time.sleep(2 ** attempt)
    raise Exception("Failed to launch instance")
```

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| InsufficientInstanceCapacity | AZ full | Try different AZ |
| InvalidAMIID | AMI not in region | Copy AMI |
| Unauthorized | IAM missing | Check permissions |
| Pending forever | ENI issue | Check subnet IPs |

### Debug Checklist
- [ ] AMI exists in target region?
- [ ] Subnet has available IPs?
- [ ] Security group allows traffic?
- [ ] Key pair exists?
- [ ] IMDSv2 configured?

### Instance Selection Guide

| Workload | Family | Key Feature |
|----------|--------|-------------|
| Web/API | M6i, M7g | Balanced |
| Compute | C6i, C7g | High CPU |
| Memory | R6i, X2idn | High memory |
| GPU/ML | P4d, G5 | NVIDIA GPU |

## Cost Optimization

| Strategy | Savings |
|----------|---------|
| Reserved Instances | 30-60% |
| Savings Plans | 30-72% |
| Spot Instances | Up to 90% |
| Right-sizing | 10-50% |

## Test Template

```python
def test_ec2_launch():
    # Arrange
    params = {
        "ImageId": get_latest_amazon_linux_ami(),
        "InstanceType": "t3.micro",
        "MaxCount": 1, "MinCount": 1
    }

    # Act
    response = ec2.run_instances(**params)
    instance_id = response['Instances'][0]['InstanceId']

    # Assert
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])

    # Cleanup
    ec2.terminate_instances(InstanceIds=[instance_id])
```

## Assets

- `assets/ec2-userdata.sh` - Sample user data script

## References

- [EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/)
- [Instance Types](https://aws.amazon.com/ec2/instance-types/)
