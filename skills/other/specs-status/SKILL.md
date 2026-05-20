---
name: specs-status
description: 현재 프로젝트의 EARS 스펙 상태 현황 표시
user-invocable: true
---

# /specs-status [project|all]

현재 프로젝트 또는 지정된 프로젝트의 스펙 상태를 표시합니다.

## Arguments

- **无参数** - 현재 디렉토리명을 프로젝트명으로 사용
- **project-name** - 지정된 프로젝트의 스펙만 표시
- **all** - 모든 프로젝트의 스펙을 표시

## Implementation

```bash
specs-status() {
    local SPECS_DIR="$HOME/.claude/specs"
    local target_project="$1"
    local projects=()

    # Determine which projects to show
    if [[ -z "$target_project" ]]; then
        # No argument: use current directory basename
        target_project="$(basename "$PWD")"
        projects=("$target_project")
    elif [[ "$target_project" == "all" ]]; then
        # Show all projects
        if [[ ! -d "$SPECS_DIR" ]]; then
            echo "No specs directory found"
            return 0
        fi
        # Get all subdirectories in specs directory
        while IFS= read -r -d '' dir; do
            projects+=("$(basename "$dir")")
        done < <(find "$SPECS_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
    else
        # Specific project
        projects=("$target_project")
    fi

    # Exit if no projects found
    if [[ ${#projects[@]} -eq 0 ]]; then
        echo "No projects found"
        return 0
    fi

    # Process each project
    for project in "${projects[@]}"; do
        local project_dir="$SPECS_DIR/$project"

        echo ""
        echo "## Specs Status: $project"
        echo ""

        # Check if project directory exists
        if [[ ! -d "$project_dir" ]]; then
            echo "No specs found for project $project"
            continue
        fi

        # Track counts
        local pending_count=0 doing_count=0 done_count=0
        local pending_specs=() doing_specs=() done_specs=()

        # Process each status directory
        for status in pending doing done; do
            local status_dir="$project_dir/$status"

            if [[ ! -d "$status_dir" ]]; then
                continue
            fi

            # Find all .ears.md files in status directory
            while IFS= read -r -d '' spec_file; do
                local spec_id
                spec_id="$(basename "$spec_file" .ears.md)"
                local title="" priority="" created=""

                # Parse metadata from file using grep for safety
                # Extract title (first line with # SPEC-ID: format, e.g., "# 001: Title")
                title="$(grep -m1 "^# *[0-9]*: " "$spec_file" 2>/dev/null | sed 's/^# *[0-9]*: //')"
                # Extract created date
                created="$(grep '^-' "$spec_file" 2>/dev/null | grep 'created:' | sed 's/.*created: *//' | head -1)"
                # Extract priority
                priority="$(grep '^-' "$spec_file" 2>/dev/null | grep 'priority:' | sed 's/.*priority: *//' | head -1)"

                # Default values if not found
                [[ -z "$title" ]] && title="(no title)"
                [[ -z "$priority" ]] && priority="medium"
                [[ -z "$created" ]] && created="(unknown)"

                case "$status" in
                    pending)
                        ((pending_count++))
                        pending_specs+=("$spec_id|$title|$priority|$created")
                        ;;
                    doing)
                        ((doing_count++))
                        doing_specs+=("$spec_id|$title|$priority|$created")
                        ;;
                    done)
                        ((done_count++))
                        done_specs+=("$spec_id|$title|$priority|$created")
                        ;;
                esac
            done < <(find "$status_dir" -maxdepth 1 -type f -name "*.ears.md" -print0 | sort -z)
        done

        # Display summary table
        echo "| Status  | Count |"
        echo "|---------|-------|"
        echo "| Pending | $pending_count     |"
        echo "| Doing   | $doing_count     |"
        echo "| Done    | $done_count     |"
        echo ""

        # Check if any specs found
        if [[ $pending_count -eq 0 && $doing_count -eq 0 && $done_count -eq 0 ]]; then
            echo "No specs found for project $project"
            continue
        fi

        # Display pending specs
        if [[ $pending_count -gt 0 ]]; then
            echo "### Pending"
            for spec in "${pending_specs[@]}"; do
                IFS='|' read -r spec_id spec_title spec_priority spec_created <<< "$spec"
                echo "- **$spec_id**: $spec_title ($spec_priority) - created: $spec_created"
            done
            echo ""
        fi

        # Display doing specs
        if [[ $doing_count -gt 0 ]]; then
            echo "### Doing"
            for spec in "${doing_specs[@]}"; do
                IFS='|' read -r spec_id spec_title spec_priority spec_created <<< "$spec"
                echo "- **$spec_id**: $spec_title ($spec_priority) - created: $spec_created"
            done
            echo ""
        fi

        # Display done specs
        if [[ $done_count -gt 0 ]]; then
            echo "### Done"
            for spec in "${done_specs[@]}"; do
                IFS='|' read -r spec_id spec_title spec_priority spec_created <<< "$spec"
                echo "- **$spec_id**: $spec_title ($spec_priority) - created: $spec_created"
            done
            echo ""
        fi
    done
}

specs-status "$@"
```
