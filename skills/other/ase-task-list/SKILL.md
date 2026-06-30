---
name: ase-task-list
argument-hint: "[--help|-h] [--verbose|-v]"
description: >
    List all available task ids.
    Use when user wants to see all tasks.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-task-list">
List Task Plans
</skill>

<expand name="getopt"
    arg1="ase-task-list"
    arg2="--verbose|-v">
    $ARGUMENTS
</expand>

<objective>
*List* all available *task plans* of the current project.
</objective>

1.  Call the `ase_task_list(verbose: <getopt-option-verbose/>)` tool from
    the `ase` MCP server. The result is a structured object with a
    `tasks` array where each entry has an `id` field, and -- if
    <getopt-option-verbose/> is `true` -- additionally an `mtime` field
    (formatted as `YYYY-MM-DD HH:MM`).

2.  If the `tasks` array is empty, output the following <template/>:

    <template>
    ⧉ **ASE**: ◉ tasks: *(none)*
    </template>

    Else, dispatch on <getopt-option-verbose/>:

    -   If <getopt-option-verbose/> is `true`, output the list of tasks
        with the following <template/>, where each <id/> and <mtime/>
        correspond to an entry in the task list:

        <template>
        ⧉ **ASE**: ◉ tasks:

        | *Task Id* | *Last Modified*    |
        |-----------|--------------------|
        | **<id/>** | `<mtime/>`         |
        | [...]     | [...]              |

        </template>

    -   If <getopt-option-verbose/> is `false`, output the list of tasks
        with the following <template/>, where each <id/> corresponds to
        an entry in the task list:

        <template>
        ⧉ **ASE**: ◉ tasks:

        | *Task Id* |
        |-----------|
        | **<id/>** |
        | [...]     |

        </template>

