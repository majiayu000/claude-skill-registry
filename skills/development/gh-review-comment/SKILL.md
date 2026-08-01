---
name: gh-review-comment
description: '`gh` コマンドを用いて GitHub の PR レビューコメントを操作します。レビューコメントへの返信（Reply）や解決（Resolve）するときに必ず使用してください。'
---

---
name: gh-review-comment
description: `gh` コマンドを用いて GitHub の PR レビューコメントを操作します。レビューコメントへの返信（Reply）や解決（Resolve）するときに必ず使用してください。
---

# gh コマンドを用いた GitHub の PR レビューコメントの操作

## 返信（Reply）

```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments/COMMENT_ID/replies -X POST \
  -f body="BODY"
```

## 解決（Resolve）

```bash
# スレッドIDを取得
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 10) {
        nodes {
          id
          comments(first: 1) {
            nodes {
              databaseId
            }
          }
        }
      }
    }
  }
}'

# スレッドを解決
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "THREAD_ID"}) {
    thread {
      id
      isResolved
    }
  }
}'
```

### 参考リンク

- [GitHub REST API - Review comments](https://docs.github.com/rest/pulls/comments)
- [GitHub GraphQL API - resolveReviewThread](https://docs.github.com/graphql/reference/mutations#resolvereviewthread)
