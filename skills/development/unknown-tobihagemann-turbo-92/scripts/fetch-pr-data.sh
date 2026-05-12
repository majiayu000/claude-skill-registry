#!/usr/bin/env bash
# Fetch all review threads, reviews, issue comments, and metadata for a GitHub PR.
# Emits a single merged JSON document on stdout:
#   {
#     "meta":          { title, url, headRefName, baseRefName },
#     "reviewThreads": [ ... ],
#     "reviews":       [ ... ],
#     "issueComments": [ ... ]    # PR conversation comments (non-review); author, body, createdAt, url
#   }
#
# Paginates reviewThreads, reviews, and issue comments to avoid silent drops on long
# PRs. For any thread whose inner comments exceed the initial page, walks the
# remaining comments via node(id:) and merges them back into the thread.
#
# Usage: fetch-pr-data.sh <owner> <repo> <pr_number>

set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <owner> <repo> <pr_number>" >&2
  exit 2
fi

owner="$1"
repo="$2"
pr="$3"

meta_query=$(cat <<'GRAPHQL'
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) { title url headRefName baseRefName }
  }
}
GRAPHQL
)

threads_query=$(cat <<'GRAPHQL'
query($owner: String!, $repo: String!, $pr: Int!, $endCursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes { author { login } body path line originalLine diffHunk }
          }
        }
      }
    }
  }
}
GRAPHQL
)

reviews_query=$(cat <<'GRAPHQL'
query($owner: String!, $repo: String!, $pr: Int!, $endCursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviews(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes { author { login } body state }
      }
    }
  }
}
GRAPHQL
)

issue_comments_query=$(cat <<'GRAPHQL'
query($owner: String!, $repo: String!, $pr: Int!, $endCursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      comments(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes { author { login } body createdAt url }
      }
    }
  }
}
GRAPHQL
)

thread_tail_query=$(cat <<'GRAPHQL'
query($thread_id: ID!, $cursor: String!) {
  node(id: $thread_id) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { author { login } body path line originalLine diffHunk }
      }
    }
  }
}
GRAPHQL
)

meta=$(gh api graphql \
  -f query="$meta_query" \
  -f owner="$owner" -f repo="$repo" -F pr="$pr" \
  --jq '.data.repository.pullRequest')

threads=$(gh api graphql --paginate \
  -f query="$threads_query" \
  -f owner="$owner" -f repo="$repo" -F pr="$pr" \
  --jq '.data.repository.pullRequest.reviewThreads.nodes[]' \
  | jq -s '.')

threads=$(jq -c '.[]' <<<"$threads" | while IFS= read -r thread; do
  has_next=$(jq -r '.comments.pageInfo.hasNextPage' <<<"$thread")
  if [ "$has_next" != "true" ]; then
    printf '%s\n' "$thread"
    continue
  fi
  thread_id=$(jq -r '.id' <<<"$thread")
  cursor=$(jq -r '.comments.pageInfo.endCursor' <<<"$thread")
  nodes=$(jq '.comments.nodes' <<<"$thread")
  while [ "$has_next" = "true" ]; do
    page=$(gh api graphql \
      -f query="$thread_tail_query" \
      -f thread_id="$thread_id" -f cursor="$cursor" \
      --jq '.data.node.comments')
    page_nodes=$(jq '.nodes' <<<"$page")
    nodes=$(jq -n --argjson a "$nodes" --argjson b "$page_nodes" '$a + $b')
    has_next=$(jq -r '.pageInfo.hasNextPage' <<<"$page")
    cursor=$(jq -r '.pageInfo.endCursor // ""' <<<"$page")
  done
  jq --argjson nodes "$nodes" '
    .comments.nodes = $nodes
    | .comments.pageInfo.hasNextPage = false
    | .comments.pageInfo.endCursor = null
  ' <<<"$thread"
done | jq -s '.')

reviews=$(gh api graphql --paginate \
  -f query="$reviews_query" \
  -f owner="$owner" -f repo="$repo" -F pr="$pr" \
  --jq '.data.repository.pullRequest.reviews.nodes[]' \
  | jq -s '.')

issue_comments=$(gh api graphql --paginate \
  -f query="$issue_comments_query" \
  -f owner="$owner" -f repo="$repo" -F pr="$pr" \
  --jq '.data.repository.pullRequest.comments.nodes[]' \
  | jq -s '.')

jq -n \
  --argjson meta "$meta" \
  --argjson threads "$threads" \
  --argjson reviews "$reviews" \
  --argjson issueComments "$issue_comments" \
  '{meta: $meta, reviewThreads: $threads, reviews: $reviews, issueComments: $issueComments}'
