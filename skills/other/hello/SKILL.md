---
name: hello
argument-hint: "[--help|-h] [--lang|-l=(en|de|fr|it)] [<subject>]"
description: >
    Show a nice greeting message with a timestamp.
    Use this, when the user wants to greet or say hello,
    optionally to a certain subject <subject> and in a certain language <language>.
user-invocable: true
disable-model-invocation: false
allowed-tools:
    - "Bash(date)"
    - "Bash(ase meta *)"
---

!`ase meta control skill getopt`

<skill name="hello">
    Hello World
</skill>

<expand name="getopt" arg1="foo">
    $ARGUMENTS
</expand>

<flow>

1.  <step id="STEP 1: Determine Parameters">

    1.  Set <subject><getopt-arguments/></subject>
        Set <language><getopt-lang/></language>

    2.  <if condition="<subject/> is empty">
            Set <subject>World</subject>
        </if>

    3.  The current time <time/> is set by capturing the
        output of the `Bash` tool command `date '+%Y-%m-%d %H:%M:%S'`

    4.  The greeting format in Markdown is exactly:
        `[<time/>]: *Hello*, **<subject/>**, nice to meet you!`

    </step>

2.  <step id="STEP 2: Product Output">

    1.  Create the greeting string, based on the greeting format.

    2.  Translate the greeting string into the target language <language/>.

    3.  Output the greeting string verbatim.
        Do not output anything else.

    </step>

</flow>

