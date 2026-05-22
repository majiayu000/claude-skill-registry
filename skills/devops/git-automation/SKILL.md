---
name: git-automation
description: Advanced Git operations automation including intelligent branching, commit optimization, release workflows, and repository health management
version: 1.0.0
---

## Overview

Comprehensive Git automation skill that provides intelligent repository management, advanced branching strategies, automated commit optimization, and sophisticated release workflows with continuous learning from repository patterns.

## Git Repository Intelligence

### Repository Analysis
```bash
# Analyze repository structure and patterns
analyze_repository() {
  local repo_path=$1

  # Repository metrics
  local total_commits=$(git rev-list --count HEAD)
  local total_branches=$(git branch -a | wc -l)
  local total_tags=$(git tag -l | wc -l)
  local repo_size=$(du -sh .git 2>/dev/null | cut -f1)

  # Activity metrics
  local recent_commits=$(git log --since="1 month ago" --oneline | wc -l)
  local active_contributors=$(git log --since="3 months ago" --format='%ae' | sort -u | wc -l)

  # Quality metrics
  local merge_conflicts=$(git log --grep="conflict" --oneline | wc -l)
  local large_files=$(git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sed -n 's/^blob //p' | sort -nr | head -10 | wc -l)

  echo "Repository Analysis for $repo_path:"
  echo "  Total Commits: $total_commits"
  echo "  Total Branches: $total_branches"
  echo "  Total Tags: $total_tags"
  echo "  Repository Size: $repo_size"
  echo "  Recent Commits (1mo): $recent_commits"
  echo "  Active Contributors (3mo): $active_contributors"
  echo "  Merge Conflicts: $merge_conflicts"
  echo "  Large Files (>1MB): $large_files"
}
```

### Branching Strategy Detection
```bash
# Detect current branching strategy
detect_branching_strategy() {
  local main_branch=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
  local develop_branch=$(git branch -r | grep -E "origin/develop|origin/dev" | head -1 | sed 's@origin/@@')
  local release_branches=$(git branch -r | grep -E "origin/release|origin/rel" | wc -l)
  local feature_branches=$(git branch -r | grep -E "origin/feat|origin/feature" | wc -l)

  if [[ -n "$develop_branch" ]] && [[ $release_branches -gt 0 ]]; then
    echo "GitFlow"
  elif [[ -z "$develop_branch" ]] && [[ $feature_branches -gt 0 ]]; then
    echo "GitHub Flow"
  elif [[ $feature_branches -eq 0 ]] && [[ $release_branches -eq 0 ]]; then
    echo "Trunk-Based Development"
  else
    echo "Custom Strategy"
  fi
}
```

## Intelligent Commit Management

### Semantic Commit Analysis
```bash
# Analyze commits for semantic versioning impact
analyze_commit_impact() {
  local commit_range=$1

  # Count commit types
  local breaking_changes=$(git log --oneline $commit_range | grep -c "BREAKING\|breaking")
  local features=$(git log --oneline $commit_range | grep -c "feat:")
  local fixes=$(git log --oneline $commit_range | grep -c "fix:")
  local performance=$(git log --oneline $commit_range | grep -c "perf:")
  local refactors=$(git log --oneline $commit_range | grep -c "refactor:")

  # Determine version bump
  if [[ $breaking_changes -gt 0 ]]; then
    echo "major ($breaking_changes breaking changes)"
  elif [[ $features -gt 0 ]]; then
    echo "minor ($features features added)"
  else
    echo "patch ($fixes fixes, $performance improvements)"
  fi
}

# Generate intelligent commit messages
generate_commit_message() {
  local changes=$(git diff --cached --name-only)
  local commit_type=""
  local scope=""
  local description=""

  # Analyze changed files to determine commit type
  if echo "$changes" | grep -q "test\|spec"; then
    commit_type="test"
  elif echo "$changes" | grep -q "doc\|readme\|md"; then
    commit_type="docs"
  elif echo "$changes" | grep -q "package\|requirements\|setup"; then
    commit_type="chore"
  elif echo "$changes" | grep -q "\.py\|\.js\|\.ts\|\.java\|\.cpp"; then
    commit_type="feat"  # Default to feature for code changes
  fi

  # Extract scope from file paths
  scope=$(echo "$changes" | head -1 | cut -d'/' -f1)

  # Generate description from file changes
  description=$(echo "$changes" | head -3 | tr '\n' ', ' | sed 's/,$//')

  echo "$commit_type($scope): $description"
}
```

### Automated Commit Optimization
```bash
# Optimize commit history
optimize_commit_history() {
  local target_branch=$1
  local since_date=${2:-"1 month ago"}

  # Identify fixup commits
  local fixup_commits=$(git log --since="$since_date" --oneline --grep="fixup!" --grep="squash!" | wc -l)

  if [[ $fixup_commits -gt 0 ]]; then
    echo "Found $fixup_commits fixup/squash commits"

    # Interactive rebase to squash fixups
    local base_commit=$(git merge-base $target_branch HEAD)
    git rebase -i --autosquash $base_commit
  fi

  # Remove empty commits
  git filter-branch --commit-filter '
    if git rev-parse --verify HEAD^1 >/dev/null 2>&1 &&
       [ "$(git diff-tree --no-commit-id --root -r --name-only HEAD | wc -l)" = 0 ]; then
      skip_commit "$@";
    else
      git commit-tree "$@";
    fi
  ' HEAD~50..HEAD
}
```

## Advanced Release Automation

### Intelligent Version Bumping
```bash
# Smart version bump based on changes
smart_version_bump() {
  local current_version=$(get_current_version)
  local commit_range=$(get_last_release_range)
  local version_impact=$(analyze_commit_impact "$commit_range")

  echo "Current version: $current_version"
  echo "Version impact: $version_impact"

  case $version_impact in
    major*)
      local new_version=$(bump_version "$current_version" major)
      ;;
    minor*)
      local new_version=$(bump_version "$current_version" minor)
      ;;
    patch*)
      local new_version=$(bump_version "$current_version" patch)
      ;;
  esac

  echo "New version: $new_version"
  update_version_files "$new_version"
}

# Update version across all files
update_version_files() {
  local new_version=$1

  # Common version files
  local version_files=(
    "package.json"
    "setup.py"
    "pyproject.toml"
    "Cargo.toml"
    "composer.json"
    "pom.xml"
    "__init__.py"
    "version.py"
    "Dockerfile"
  )

  for file in "${version_files[@]}"; do
    if [[ -f "$file" ]]; then
      case "$file" in
        "package.json")
          npm version $new_version --no-git-tag-version
          ;;
        "setup.py"|"pyproject.toml")
          bump2version $new_version --allow-dirty
          ;;
        "Cargo.toml")
          cargo bump $new_version
          ;;
        *)
          # Generic version update
          sed -i "s/version\s*=\s*[\"'][0-9]\+\.[0-9]\+\.[0-9]\+[\"']/version = \"$new_version\"/" "$file"
          ;;
      esac
    fi
  done
}
```

### Release Workflow Automation
```bash
# Complete release workflow
execute_release_workflow() {
  local new_version=$1
  local release_notes_file=$2

  echo "Starting release workflow for v$new_version"

  # 1. Pre-release validation
  validate_release_readiness || exit 1

  # 2. Update version files
  update_version_files "$new_version"

  # 3. Generate changelog
  generate_changelog "$new_version" > CHANGELOG.md.tmp
  cat CHANGELOG.md.tmp >> CHANGELOG.md
  rm CHANGELOG.md.tmp

  # 4. Commit version changes
  git add .
  git commit -m "chore(release): v$new_version"

  # 5. Create release branch/tag
  git checkout -b "release/v$new_version"
  git tag -a "v$new_version" -m "Release v$new_version"

  # 6. Merge to main
  git checkout main
  git merge "release/v$new_version" --no-ff

  # 7. Push changes
  git push origin main
  git push origin "v$new_version"

  # 8. Create GitHub release
  if command -v gh >/dev/null 2>&1; then
    if [[ -f "$release_notes_file" ]]; then
      gh release create "v$new_version" --title "Release v$new_version" --notes-file "$release_notes_file"
    else
      gh release create "v$new_version" --title "Release v$new_version" --generate-notes
    fi
  fi

  # 9. Cleanup
  git branch -d "release/v$new_version"

  echo "Release v$new_version completed successfully!"
}

# Pre-release validation
validate_release_readiness() {
  local errors=0

  # Check working directory is clean
  if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Working directory is not clean"
    ((errors++))
  fi

  # Run tests
  if command -v npm >/dev/null 2>&1; then
    npm test || ((errors++))
  elif command -v pytest >/dev/null 2>&1; then
    pytest || ((errors++))
  fi

  # Check for linting issues
  if command -v npm >/dev/null 2>&1; then
    npm run lint || ((errors++))
  elif command -v flake8 >/dev/null 2>&1; then
    flake8 . || ((errors++))
  fi

  # Security scan
  if command -v npm >/dev/null 2>&1; then
    npm audit --audit-level high || ((errors++))
  fi

  if [[ $errors -gt 0 ]]; then
    echo "❌ Pre-release validation failed with $errors errors"
    return 1
  fi

  echo "✅ Pre-release validation passed"
  return 0
}
```

## Multi-Platform Integration

### GitHub Integration
```bash
# GitHub operations automation
github_operations() {
  local operation=$1
  local repo_name=$2

  case $operation in
    "create-pr")
      local title=$3
      local body=$4
      local head_branch=$5
      local base_branch=${6:-"main"}

      gh pr create \
        --title "$title" \
        --body "$body" \
        --head "$head_branch" \
        --base "$base_branch"
      ;;

    "merge-pr")
      local pr_number=$2
      local merge_method=${3:-"merge"}

      gh pr merge "$pr_number" --"$merge_method" --delete-branch
      ;;

    "create-release")
      local tag=$2
      local title=$3
      local notes_file=$4

      if [[ -f "$notes_file" ]]; then
        gh release create "$tag" --title "$title" --notes-file "$notes_file"
      else
        gh release create "$tag" --title "$title" --generate-notes
      fi
      ;;

    "update-repo-info")
      local description=$2
      local homepage=$3
      local topics=$4

      gh repo edit \
        --description "$description" \
        --homepage "$homepage" \
        --add-topic $topics
      ;;
  esac
}
```

### GitLab Integration
```bash
# GitLab operations automation
gitlab_operations() {
  local operation=$1

  case $operation in
    "create-mr")
      local title=$2
      local description=$3
      local source_branch=$4
      local target_branch=${5:-"main"}

      glab mr create \
        --title "$title" \
        --description "$description" \
        --source-branch "$source_branch" \
        --target-branch "$target_branch"
      ;;

    "create-release")
      local tag=$2
      local name=$3
      local description=$4

      glab release create "$tag" \
        --name "$name" \
        --description "$description"
      ;;
  esac
}
```

## Repository Health Management

### Repository Cleanup
```bash
# Cleanup repository for better performance
cleanup_repository() {
  echo "Cleaning up repository..."

  # Remove unreachable objects
  git prune --expire=now

  # Compress repository
  git gc --aggressive --prune=now

  # Remove stale references
  git remote prune origin

  # Clean up large files (requires git-filter-repo)
  if command -v git-filter-repo >/dev/null 2>&1; then
    git-filter-repo --strip-blobs-bigger-than 10M
  fi

  # Check for sensitive data
  if command -v git-secrets >/dev/null 2>&1; then
    git-secrets --scan-history
  fi

  echo "Repository cleanup completed"
}

# Analyze repository health
analyze_repository_health() {
  local issues=0

  echo "Repository Health Analysis:"

  # Check for large files
  local large_files=$(git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sed -n 's/^blob //p' | awk '$2 > 1048576 { print $2, $3 }')
  if [[ -n "$large_files" ]]; then
    echo "⚠️  Found large files in repository:"
    echo "$large_files"
    ((issues++))
  fi

  # Check for many small commits
  local small_commits=$(git log --stat --oneline | awk '{if($2 < 10) count++} END {print count+0}')
  if [[ $small_commits -gt 50 ]]; then
    echo "⚠️  High number of small commits ($small_commits). Consider squashing."
    ((issues++))
  fi

  # Check for old branches
  local old_branches=$(git branch -r | while read branch; do
    local last_commit=$(git log -1 --format='%ci' "$branch" 2>/dev/null)
    if [[ -n "$last_commit" ]]; then
      local days_old=$(( ($(date +%s) - $(date -d "$last_commit" +%s)) / 86400 ))
      if [[ $days_old -gt 90 ]]; then
        echo "$branch ($days_old days old)"
      fi
    fi
  done)

  if [[ -n "$old_branches" ]]; then
    echo "⚠️  Found old branches:"
    echo "$old_branches"
    ((issues++))
  fi

  if [[ $issues -eq 0 ]]; then
    echo "✅ Repository is healthy"
  else
    echo "❌ Found $issues health issues"
  fi
}
```

## Integration Patterns

### Continuous Learning Integration
```json
{
  "git_patterns": {
    "commit_frequency": {
      "average": 5.2,
      "peak_day": "friday",
      "peak_time": "14:00 UTC"
    },
    "branch_strategy": "github_flow",
    "release_cadence": "bi_weekly",
    "common_issues": [
      "merge_conflicts",
      "version_inconsistencies",
      "documentation_drift"
    ],
    "optimization_opportunities": [
      "automated_changelog_generation",
      "pre_commit_validation",
      "automated_dependency_updates"
    ]
  },
  "automation_success_rates": {
    "release_automation": 0.95,
    "version_bumping": 0.98,
    "branch_creation": 0.99,
    "commit_optimization": 0.87
  }
}
```

### Error Recovery Patterns
```bash
# Handle common Git operation failures
handle_git_failure() {
  local operation=$1
  local error_code=$2

  case $operation in
    "merge")
      if [[ $error_code -eq 1 ]]; then
        echo "Merge conflict detected. Attempting resolution..."
        git merge --abort
        # Analyze conflicts and suggest resolution strategy
      fi
      ;;
    "push")
      if [[ $error_code -eq 1 ]]; then
        echo "Push failed. Checking for issues..."
        # Check if remote is ahead
        git fetch origin
        local behind=$(git rev-list --count HEAD..origin/$(git branch --show-current))
        if [[ $behind -gt 0 ]]; then
          echo "Local branch is $behind commits behind. Pulling first..."
          git pull origin $(git branch --show-current)
        fi
      fi
      ;;
  esac
}
```

## When to Apply

Use Git Automation when:
- Managing complex branching strategies and release workflows
- Need to standardize commit messages and version bumping
- Automating GitHub/GitLab operations and releases
- Optimizing repository performance and health
- Implementing continuous deployment pipelines
- Coordinating multi-platform repository operations

The Git Automation skill provides comprehensive repository management with intelligent automation, learning capabilities, and seamless integration with modern development workflows.