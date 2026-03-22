---
name: aws-ecr
description: "Manage AWS ECR container image repositories."
metadata: {"thinkfleetbot":{"emoji":"🐋","requires":{"bins":["aws","jq"],"env":["AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"]}}}
---

# AWS ECR

Manage Elastic Container Registry repositories and images.

## List repositories

```bash
aws ecr describe-repositories --query 'repositories[].{Name:repositoryName,Uri:repositoryUri,Created:createdAt}' --output table
```

## List images

```bash
aws ecr list-images --repository-name my-repo --query 'imageIds[].{Tag:imageTag,Digest:imageDigest}' --output table | head -20
```

## Describe images (with size/push date)

```bash
aws ecr describe-images --repository-name my-repo --query 'imageDetails | sort_by(@, &imagePushedAt) | reverse(@)[:10].{Tags:imageTags[0],Size:imageSizeInBytes,Pushed:imagePushedAt}' --output table
```

## Get login token (for docker push/pull)

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
```

## Delete image

```bash
aws ecr batch-delete-image --repository-name my-repo --image-ids imageTag=old-tag | jq '{Deleted: .imageIds, Failures: .failures}'
```

## Get lifecycle policy

```bash
aws ecr get-lifecycle-policy --repository-name my-repo | jq '.lifecyclePolicyText | fromjson'
```

## Notes

- Login tokens expire after 12 hours.
- Use lifecycle policies to auto-clean old images.
- Confirm before deleting images.
