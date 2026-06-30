---
name: ase-meta-compat
description: >
    Self-test the LLM's ability to execute ASE's core interpreter
    machinery (control flow, XML placeholders, regex matching,
    arithmetic) and report an overall compatibility rating. Use when
    the user wants to check how well the current model/harness is
    compatible with ASE, or asks to "test ASE compatibility" or "check
    ASE compatibility".
user-invocable: true
disable-model-invocation: true
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md

Self-Test ASE Compatibility
===========================

Objective
---------

*Self-test* how faithfully the current LLM (and its harness) executes the
four *core interpreter primitives* that every ASE skill silently relies
on -- *control flow*, *XML placeholders*, *regex matching*, and
*arithmetic* -- and report an overall **0%…100% compatibility** rating.

This skill is unusual: it is both the *test definition* and the *system
under test*. Each *probe* is a pure ASE construct that you execute and
record its *actual* result. You *MUST NOT* compare against any expected
value until STEP 6. Do not fabricate passes: a probe whose actual result
differs from its expected result *MUST* be recorded as a *fail*.

Notice that this skill intentionally does not strictly follow the ASE
skill format, especially it does not include any meta skill information,
etc.

Procedure
---------

1.  STEP 1: Initialize Self-Test

    Initialize the running map of actual probe results <actuals></actuals>
    (set to empty) -- every probe in STEPs 2-5 stores its result here as
    a `<category/>/<probe-name/>` entry with its *actual* computed value.

    Initialize the running list of failed probes <failures></failures>
    (set to empty) -- this is populated only in STEP 6 after comparing
    actuals against the expected values.

2.  STEP 2: Probe XML Placeholders

    Execute *all* of the following XML-placeholder probes (in the given
    order). For each probe, record the *actual* result in <actuals/>
    under the key `xml-placeholders/<probe-name/>`. Do *not* compare to
    any expected value here.

    1.  *get-and-set*: Set <v>42</v>, then get <v/>.
        Record actual result for `xml-placeholders/get-and-set`.

    2.  *self-ref*: Set <v>42</v>, then set `<v>pre_<v/></v>`, then get <v/>.
        Record actual result for `xml-placeholders/self-ref`.

    3.  *overwrite*: Set <v>42</v>, then set `<v>99</v>`, then get <v/>.
        Record actual result for `xml-placeholders/overwrite`.

    4.  *indexed*: Set `<eval-1-2>+1</eval-1-2>` and `<eval-2-1>-1</eval-2-1>`,
        then get <eval-1-2/> and <eval-2-1/> via `<eval-1-2/>,<eval-2-1/>`.
        Record actual result for `xml-placeholders/indexed`.

    5.  *nested-attr*: With <w>20</w>, build the value of an XML attribute
        `width="<w/>"` and read the attribute `width` back.
        Record actual result for `xml-placeholders/nested-attr`.

    6.  *entity*: Evaluate the XML entity `&#x29BF;` and get the rendered
        Unicode character.
        Record actual result for `xml-placeholders/entity`.

    Set <xml-total/> to the number of XML-placeholder probes above.

3.  STEP 3: Probe Control Flow

    Execute *all* of the following control-flow probes (in the given
    order). For each probe, record the *actual* result in <actuals/>
    under the key `control-flow/<probe-name/>`. Do *not* compare to any
    expected value here.

    1.  *branch*: Set <a>3</a>, then evaluate
        `<if condition="<a/> is greater than 5">big</if>
        <elseif condition="<a/> is greater than 2">mid</elseif>
        <else>small</else>`.
        Record actual result for `control-flow/branch`.

    2.  *while-sum*: Set <s>0</s> and <i>1</i>, then evaluate
        `<while condition="<i/> is less than or equal to 5">
        set <s/> to <s/> + <i/>,
        set <i/> to <i/> + 1
        </while>`.
        Record <s/> as actual result for `control-flow/while-sum`.

    3.  *for-order*: Set <s></s>, then evaluate
        `<for items="x y z"><s><s/>-<item/></for>`.
        Record <s/> as actual result for `control-flow/for-order`.

    4.  *while-break*: Set <i>1</i> and <hit></hit>, then evaluate
        `<while condition="<i/> is less than or equal to 9">
        if <i/> equals 4 set <hit/> to <i/> and <break/>,
        else set <i/> to <i/> + 1
        </while>`.
        Record <hit/> as actual result for `control-flow/while-break`.

    5.  *step-skip*: A `<step condition="[...]">[...]</step>` either expands
        to its body (if condition evaluates to true) or to the empty string,
        so what does `<step condition="42 is greater than 7">X</step>` expands into?
        Record the result of this construct for `control-flow/step-skip`.

    6.  *expand-subst*: With `<define name="foo">[<arg1/>:<content/>]</define>`,
        evaluate `<expand name="foo" arg1="K">V</expand>`.
        Record actual result for `control-flow/expand-subst`.

    Set <cf-total/> to the number of control-flow probes above.

4.  STEP 4: Probe Regex Matching

    Execute *all* of the following regex probes (in the given order).
    For each probe, record the *actual* result in <actuals/> under the
    key `regex/<probe-name/>`. Do *not* compare to any expected value
    here.

    1.  *getopt-dash*: Does the string `-l foo` match the regexp `(^|\s)-`?
        Record `yes` or `no` as actual result for `regex/getopt-dash`.

    2.  *getopt-nodash*: Does the string `foo` match the regexp `(^|\s)-`?
        Record `yes` or `no` as actual result for `regex/getopt-nodash`.

    3.  *anchored-int*: Does `123` fully match `^\d+$`, and does `12a` fully
        match `^\d+$`? Report as `<yes-or-no/>,<yes-or-no/>`.
        Record actual result for `regex/anchored-int`.

    4.  *alternation*: Does `thorough` match `^(basic|standard|thorough)$`?
        Record `yes` or `no` as actual result for `regex/alternation`.

    5.  *capture*: Apply `^--(\w+).+` to `--foo-bar-quux`.
        Record the first capture group as actual result for `regex/capture`.

    6.  *whitespace*: Does ` -x` (leading space then dash) match `(^|\s)-`
        (the `\s` alternative)?
        Record `yes` or `no` as actual result for `regex/whitespace`.

    7.  *complex*: Does  `--level=(low|high)...` match
        `^--([A-Za-z][A-Za-z0-9-]*)(?:\|-([A-Za-z]))?(?:=(\((.*)\)(\.\.\.)?|.*))?$`?
        Record `yes` or `no` as actual result for `regex/complex`.

    Set <re-total/> to the number of regex probes above.

5.  STEP 5: Probe Arithmetic

    Execute *all* of the following arithmetic probes (in the given
    order). For each probe, record the *actual* result in <actuals/>
    under the key `arithmetic/<probe-name/>`. Do *not* compare to any
    expected value here.

    1.  *increment*: With <n>7</n>, compute <n/> + 2.
        Record actual result for `arithmetic/increment`.

    2.  *product-sum*: Compute `4.00 * 1.00 + 2.00 * 0.50`.
        Record actual result (as `X.XX`) for `arithmetic/product-sum`.

    3.  *percentage*: Compute `3 / 7` rounded to 2 decimal places.
        Record actual result (as `0.XX`) for `arithmetic/percentage`.

    4.  *bar-width*: With <title-len>13</title-len>, compute `67 - <title-len/>`.
        Record actual result for `arithmetic/bar-width`.

    5.  *threshold*: Is `0.095` less than `0.10`?
        Record `yes` or `no` as actual result for `arithmetic/threshold`.

    6.  *round-half*: Round `2.5` to the nearest integer (round half up).
        Record actual result for `arithmetic/round-half`.

    Set <arith-total/> to the number of arithmetic probes above.

6.  STEP 6: Fetch Expected Values and Score

    Call the `ase_compat()` tool of the `ase` MCP server with an
    *internal* *programmatic* MCP tool call (and *NOT* with an external
    shell command) and set <compat-output/> to the `text` content of the
    response.

    Parse <compat-output/> into a map <expected/> by splitting on
    newlines; for each non-empty line of the form `<id/>: <value/>`, set
    `<expected[<id/>]>` to `<value/>` (value may be empty for probes
    whose correct answer is an empty string).

    For each probe in <actuals/>, compare the actual result to
    `<expected[<id/>]>` using an exact-match comparison:

    -   If they match, count the probe as *pass*.
    -   If they differ, count the probe as *fail* and append `<id/>`
        to <failures/>.

    Tally pass counts per category:

    -   Set <xml-pass/>   to the number of `xml-placeholders/*` probes that passed.
    -   Set <cf-pass/>    to the number of `control-flow/*`     probes that passed.
    -   Set <re-pass/>    to the number of `regex/*`            probes that passed.
    -   Set <arith-pass/> to the number of `arithmetic/*`       probes that passed.

7.  STEP 7: Compute and Report Compatibility

    Compute each category's *pass-rate* (a value in 0.0…1.0) by dividing
    its passes by its total:

    set <xml-rate/>   to <xml-pass/>   / <xml-total/>,
    set <cf-rate/>    to <cf-pass/>    / <cf-total/>,
    set <re-rate/>    to <re-pass/>    / <re-total/>,
    set <arith-rate/> to <arith-pass/> / <arith-total/>.

    Compute the overall compatibility as a *weighted average* of the
    four pass-rates, where *XML placeholders* carry weight `4.00` (the
    backbone of every skill), *control flow* carries weight `3.00`,
    *regex matching* carries weight `2.00`, and *arithmetic* carries
    weight `1.00`. Use the `ase_decision_matrix` MCP tool with a single
    "compatibility" alternative column, one matrix row per category of
    the form `[ <weight/>, <rate/> ]`:

    Call...

    `ase_decision_matrix(matrix: [
        [ 4.00, <xml-rate/>   ],
        [ 3.00, <cf-rate/>    ],
        [ 2.00, <re-rate/>    ],
        [ 1.00, <arith-rate/> ]
    ])`

    ...of the `ase` MCP server with an *internal* *programmatic* MCP
    tool call (and *NOT* with an external shell command) and set
    <product-sum/> to the *single* numerical value of the returned
    array.

    The product-sum is the sum over the four rows of `<weight/> *
    <rate/>`, so dividing by the sum of weights (4.00 + 3.00 + 2.00 +
    1.00 = 10.00) yields the weighted-average compatibility on 0.0…1.0:

    Set <overall/> to <product-sum/> / 10.00.
    Set <overall-pct/> to round(<overall/> * 100) (an integer percentage).

    Also compute each category's display percentage:

    Set <cf-pct/> to round(<cf-rate/> * 100), and
    likewise <xml-pct/>, <re-pct/>, <arith-pct/>.

    Determine the <verdict/> from <overall-pct/>:

    1.  If <overall-pct/> is greater than or equal to 90:
        Set <verdict>✓ *FULLY COMPATIBLE*</verdict>.

    2.  Else if <overall-pct/> is greater than or equal to 60:
        Set <verdict>⚠ *PARTIALLY COMPATIBLE*</verdict>.

    3.  Else:
        Set <verdict>✘ *INCOMPATIBLE*</verdict>.

    4.  If <failures/> is not empty:
        Append to <verdict/> the suffix ` (failed: <failures/>)`.

    Finally, output the compatibility report:

    **RESULTS**:

    | ⦿ *Capability*       | ⚖ *Weight*  | ✓ *Passed*                   | ⚑ *Rate*            |
    | :------------------- | ----------: | ---------------------------: | ------------------: |
    | XML Placeholders     |        4.00 | <xml-pass/>/<xml-total/>     | <xml-pct/>%         |
    | Control Flow         |        3.00 | <cf-pass/>/<cf-total/>       | <cf-pct/>%          |
    | Regex Matching       |        2.00 | <re-pass/>/<re-total/>       | <re-pct/>%          |
    | Arithmetic           |        1.00 | <arith-pass/>/<arith-total/> | <arith-pct/>%       |
    | **OVERALL**          |             |                              | **<overall-pct/>%** |

    **VERDICT**: <verdict/>
