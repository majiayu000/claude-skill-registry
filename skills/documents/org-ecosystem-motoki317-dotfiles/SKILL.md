---
name: Org Ecosystem
description: This skill should be used when the user asks to "write org", "org-mode", "org file", ".org file", "org syntax", "org document", "org babel", "org export", "org agenda", "org capture", "GTD", "literate programming", "org publishing", or "org-mode workflow". Provides comprehensive Org-mode patterns and best practices.
---

<purpose>
  Provide comprehensive patterns for Org-mode document creation, GTD workflow, literate programming with Babel, and export/publishing.
</purpose>

<org_syntax>
  <fundamentals>
    <concept name="headings">
      <description>Hierarchical outline structure with stars</description>
      <example>
        - Top-level heading
        ** Second-level heading \*** Third-level heading
      </example>
    </concept>

    <concept name="properties">
      <description>Key-value metadata attached to headings</description>
      <example>
        * Task
        :PROPERTIES:
        :CATEGORY: work
        :EFFORT:   2h
        :END:
      </example>
    </concept>

    <concept name="drawers">
      <description>Hidden content blocks</description>
      <example>
        :LOGBOOK:
        CLOCK: [2024-01-15 Mon 10:00]--[2024-01-15 Mon 12:00] =>  2:00
        :END:
      </example>
    </concept>

    <concept name="timestamps">
      <description>Date and time specifications</description>
      <example>
        <2024-01-15 Mon>           ; active timestamp
        [2024-01-15 Mon]           ; inactive timestamp
        <2024-01-15 Mon 10:00>     ; with time
        <2024-01-15 Mon +1w>       ; repeating weekly
        <2024-01-15 Mon .+1d>      ; restart from completion
      </example>
    </concept>

    <decision_tree name="timestamp_type_selection">
      <question>What is the purpose of this timestamp?</question>
      <branch condition="Schedule task, show in agenda">&lt;active timestamp&gt;</branch>
      <branch condition="Record date without agenda visibility">[inactive timestamp]</branch>
      <branch condition="Task repeats on fixed schedule">+1d/+1w/+1m repeater</branch>
      <branch condition="Task repeats from today when done">.+1d reset repeater</branch>
      <branch condition="Shift to future, catching up missed">++1d cumulative repeater</branch>
    </decision_tree>
  </fundamentals>

  <patterns>
    <pattern name="lists">
      <description>Ordered and unordered lists</description>
      <example>
        - Unordered item
        - Another item
        - Nested item

        1. First ordered item
        2. Second ordered item

        - [ ] Checkbox item
        - [x] Completed checkbox
      </example>
    </pattern>

    <pattern name="tables">
      <description>Spreadsheet-like tables with formulas</description>
      <example>
        | Name  | Quantity | Price |  Total |
        |-------+----------+-------+--------|
        | Item1 |        2 |  10.0 |   20.0 |
        | Item2 |        3 |  15.0 |   45.0 |
        |-------+----------+-------+--------|
        | Total |          |       |   65.0 |
        #+TBLFM: $4=$2*$3::@>$4=vsum(@2..@-1)
      </example>
      <note>C-c C-c to recalculate, C-c | to create table from region</note>
    </pattern>

    <pattern name="links">
      <description>Internal and external hyperlinks</description>
      <example>
        [[https://orgmode.org][Org website]]
        [[file:./other.org][Local file]]
        [[file:./image.png]]
        [[*Heading][Internal link]]
        [[id:unique-id][ID link]]
        &lt;&lt;target&gt;&gt; and [[target]]
      </example>
    </pattern>

    <decision_tree name="link_type_selection">
      <question>What are you linking to?</question>
      <branch condition="External URL">[[https://...][description]]</branch>
      <branch condition="Local file in project">[[file:./path][description]]</branch>
      <branch condition="Heading in same file">[[*Heading Name][description]]</branch>
      <branch condition="Stable cross-file reference">[[id:uuid][description]] with org-id</branch>
      <branch condition="Named target in document">&lt;&lt;target&gt;&gt; and [[target]]</branch>
    </decision_tree>

    <pattern name="blocks">
      <description>Special content blocks</description>
      <example>
        #+BEGIN_QUOTE
        Quoted text here.
        #+END_QUOTE

        #+BEGIN_EXAMPLE
        Verbatim text, no markup processing.
        #+END_EXAMPLE

        #+BEGIN_CENTER
        Centered text.
        #+END_CENTER

        #+BEGIN_VERSE
        Poetry or
        formatted text.
        #+END_VERSE
      </example>
    </pattern>

    <pattern name="markup">
      <description>Text formatting markup</description>
      <example>
        *bold*
        /italic/
        _underline_
        =verbatim=
        ~code~
        +strikethrough+
      </example>
    </pattern>

    <pattern name="footnotes">
      <description>Reference notes</description>
      <example>
        Text with footnote[fn:1].

        [fn:1] Footnote definition.

        Or inline[fn:: inline footnote definition].
      </example>
    </pattern>
  </patterns>
</org_syntax>

<gtd_workflow>
  <concept name="todo_states">
    <description>Task state workflow configuration</description>
    <example>
      #+TODO: TODO(t) NEXT(n) WAITING(w@/!) | DONE(d!) CANCELLED(c@)

      - TODO Buy groceries
      - NEXT Write report
      - WAITING Review from team :@john:
      - DONE Complete project
      - CANCELLED Obsolete task
    </example>
    <note>@ prompts for note, ! records timestamp, | separates active from done states</note>
  </concept>

  <patterns>
    <pattern name="capture">
      <description>Quick capture templates</description>
      <example>
        (setq org-capture-templates
        '(("t" "Todo" entry (file+headline "~/org/inbox.org" "Tasks")
        "* TODO %?\n  %i\n  %a")
        ("n" "Note" entry (file "~/org/notes.org")
        "* %? :note:\n  %U\n  %i")
        ("j" "Journal" entry (file+datetree "~/org/journal.org")
        "* %?\n  %U")
        ("m" "Meeting" entry (file+headline "~/org/work.org" "Meetings")
        "* MEETING %? :meeting:\n  %T")))
      </example>
      <note>%? cursor position, %i active region, %a annotation, %U inactive timestamp, %T active timestamp</note>
    </pattern>

    <decision_tree name="capture_template_type">
      <question>What type of content are you capturing?</question>
      <branch condition="Action item or task">entry with TODO state to inbox</branch>
      <branch condition="Reference note or information">entry to notes file</branch>
      <branch condition="Daily journal or log">entry with file+datetree</branch>
      <branch condition="Meeting notes">entry with timestamp to meetings section</branch>
      <branch condition="Add item to existing list">item or checkitem type</branch>
    </decision_tree>

    <pattern name="agenda">
      <description>Agenda views and custom commands</description>
      <example>
        (setq org-agenda-files '("~/org/"))

        (setq org-agenda-custom-commands
        '(("d" "Dashboard"
        ((agenda "" ((org-agenda-span 7)))
        (todo "NEXT"
        ((org-agenda-overriding-header "Next Actions")))
        (todo "WAITING"
        ((org-agenda-overriding-header "Waiting For")))))
        ("w" "Weekly Review"
        ((agenda "" ((org-agenda-span 7)
        (org-agenda-start-on-weekday 1)))
        (stuck "")
        (todo "TODO")))))
      </example>
    </pattern>

    <pattern name="refile">
      <description>Task refiling configuration</description>
      <example>
        (setq org-refile-targets
        '((nil :maxlevel . 3)
        (org-agenda-files :maxlevel . 2)))

        (setq org-refile-use-outline-path 'file)
        (setq org-outline-path-complete-in-steps nil)
        (setq org-refile-allow-creating-parent-nodes 'confirm)
      </example>
      <note>C-c C-w to refile entry, C-u C-c C-w to jump to target</note>
    </pattern>

    <pattern name="clocking">
      <description>Time tracking with clock</description>
      <example>
        * Task with time tracking
        :LOGBOOK:
        CLOCK: [2024-01-15 Mon 10:00]--[2024-01-15 Mon 12:30] =>  2:30
        CLOCK: [2024-01-14 Sun 14:00]--[2024-01-14 Sun 15:00] =>  1:00
        :END:

        (setq org-clock-persist t)
        (setq org-clock-in-resume t)
        (setq org-clock-out-remove-zero-time-clocks t)
        (setq org-clock-report-include-clocking-task t)
      </example>
      <note>C-c C-x C-i clock in, C-c C-x C-o clock out, C-c C-x C-r insert clock report</note>
    </pattern>

    <pattern name="tags">
      <description>Tag-based organization</description>
      <example>
        #+TAGS: @home(h) @work(w) @phone(p) @computer(c)
        #+TAGS: urgent(u) important(i)

        - TODO Call dentist :@phone:urgent:

        (setq org-tag-alist
        '((:startgroup)
        ("@home" . ?h)
        ("@work" . ?w)
        (:endgroup)
        ("urgent" . ?u)
        ("important" . ?i)))
      </example>
    </pattern>

    <pattern name="archiving">
      <description>Archive completed tasks</description>
      <example>
        (setq org-archive-location "~/org/archive.org::datetree/")

        (setq org-archive-subtree-save-file-p t)
      </example>
      <note>C-c C-x C-a archive subtree, C-c C-x C-s archive sibling</note>
    </pattern>
  </patterns>

  <decision_tree name="task_state_selection">
    <question>What is the current status of the task?</question>
    <branch condition="Not yet started, actionable">TODO</branch>
    <branch condition="Next physical action to take">NEXT</branch>
    <branch condition="Blocked, waiting for someone/something">WAITING</branch>
    <branch condition="Successfully completed">DONE</branch>
    <branch condition="Will not be done">CANCELLED</branch>
  </decision_tree>
</gtd_workflow>

<babel>
  <concept name="code_blocks">
    <description>Executable source code blocks</description>
    <example>
      #+NAME: example-block
      #+BEGIN_SRC python :results output :exports both
      print("Hello from Python")
      for i in range(3):
      print(f"  Item {i}")
      #+END_SRC

      #+RESULTS: example-block
      : Hello from Python
      : Item 0
      : Item 1
      : Item 2
    </example>
  </concept>

  <patterns>
    <pattern name="header_args">
      <description>Common header arguments for code blocks</description>
      <example>
        #+BEGIN_SRC elisp :var x=5 :results value
        (* x x)
        #+END_SRC

        #+BEGIN_SRC shell :dir /tmp :results silent
        ls -la
        #+END_SRC

        #+BEGIN_SRC python :session py :results output

        # Persistent session across blocks

        import sys
        print(sys.version)
        #+END_SRC
      </example>
      <note>
        Header arguments:

        - :results (value, output, silent, replace, append)
        - :exports (code, results, both, none)
        - :var (variable binding)
        - :dir (working directory)
        - :session (persistent session)
        - :tangle (file to tangle to)
        - :noweb (noweb reference expansion)
      </note>
    </pattern>

    <pattern name="tangle">
      <description>Extract source code to files</description>
      <example>
        #+PROPERTY: header-args :tangle yes

        #+BEGIN_SRC python :tangle ./script.py :shebang "#!/usr/bin/env python3"
        def main():
        print("Generated from org file")

        if **name** == "**main**":
        main()
        #+END_SRC

        #+BEGIN_SRC nix :tangle ./default.nix :mkdirp yes
        { pkgs ? import &lt;nixpkgs&gt; {} }:
        pkgs.hello
        #+END_SRC
      </example>
      <note>C-c C-v t to tangle current file, :mkdirp yes to create directories</note>
    </pattern>

    <pattern name="noweb">
      <description>Literate programming with named blocks</description>
      <example>
        #+NAME: imports
        #+BEGIN_SRC python :noweb-ref imports
        import os
        import sys
        #+END_SRC

        #+NAME: main-function
        #+BEGIN_SRC python :noweb-ref main
        def main():
        print("Running main")
        #+END_SRC

        #+BEGIN_SRC python :tangle ./program.py :noweb yes
        &lt;&lt;imports&gt;&gt;

        &lt;&lt;main&gt;&gt;

        if **name** == "**main**":
        main()
        #+END_SRC
      </example>
    </pattern>

    <pattern name="results">
      <description>Result handling options</description>
      <example>
        #+BEGIN_SRC elisp :results value
        (+ 1 2 3)
        #+END_SRC

        #+RESULTS:
        : 6

        #+BEGIN_SRC python :results output
        print("line 1")
        print("line 2")
        #+END_SRC

        #+RESULTS:
        : line 1
        : line 2

        #+BEGIN_SRC elisp :results table
        '(("Name" "Age") ("Alice" 30) ("Bob" 25))
        #+END_SRC

        #+RESULTS:
        | Name | Age |
        | Alice | 30 |
        | Bob | 25 |
      </example>
    </pattern>

    <pattern name="language_specific">
      <description>Language-specific configurations</description>
      <example>
        (org-babel-do-load-languages
        'org-babel-load-languages
        '((emacs-lisp . t)
        (python . t)
        (shell . t)
        (js . t)
        (sql . t)
        (plantuml . t)))

        (setq org-confirm-babel-evaluate nil)
        (setq org-src-preserve-indentation t)
        (setq org-src-tab-acts-natively t)
        (setq org-edit-src-content-indentation 0)
      </example>
    </pattern>

    <pattern name="inline_code">
      <description>Inline source code evaluation</description>
      <example>
        The result is src_python{return 2 + 2} {{{results(=4=)}}}.

        Today is src_elisp{(format-time-string "%Y-%m-%d")}.
      </example>
    </pattern>
  </patterns>

  <decision_tree name="results_type">
    <question>What kind of output do you need?</question>
    <branch condition="Return value of expression">:results value</branch>
    <branch condition="Stdout/printed output">:results output</branch>
    <branch condition="Tabular data">:results table</branch>
    <branch condition="Raw org markup">:results raw</branch>
    <branch condition="No output needed">:results silent</branch>
  </decision_tree>
</babel>

<export>
  <concept name="export_basics">
    <description>Document export fundamentals</description>
    <example>
      #+TITLE: Document Title
      #+AUTHOR: Author Name
      #+DATE: 2024-01-15
      #+OPTIONS: toc:2 num:t author:t

      #+SETUPFILE: ./theme.setup
    </example>
  </concept>

  <patterns>
    <pattern name="html_export">
      <description>HTML export configuration</description>
      <example>
        #+OPTIONS: html-postamble:nil html-preamble:nil
        #+HTML_HEAD: &lt;link rel="stylesheet" type="text/css" href="style.css"/&gt;
        #+HTML_HEAD_EXTRA: &lt;script src="script.js"&gt;&lt;/script&gt;

        (setq org-html-validation-link nil)
        (setq org-html-head-include-scripts nil)
        (setq org-html-head-include-default-style nil)
        (setq org-html-doctype "html5")
        (setq org-html-html5-fancy t)
      </example>
      <note>C-c C-e h h to export to HTML file</note>
    </pattern>

    <pattern name="latex_export">
      <description>LaTeX/PDF export configuration</description>
      <example>
        #+LATEX_CLASS: article
        #+LATEX_CLASS_OPTIONS: [a4paper,11pt]
        #+LATEX_HEADER: \usepackage{geometry}
        #+LATEX_HEADER: \geometry{margin=1in}

        (setq org-latex-pdf-process
        '("latexmk -pdf -shell-escape %f"))

        (add-to-list 'org-latex-classes
        '("report"
        "\\documentclass{report}"
        ("\\chapter{%s}" . "\\chapter*{%s}")
        ("\\section{%s}" . "\\section*{%s}")))
      </example>
      <note>C-c C-e l p to export to PDF via LaTeX</note>
    </pattern>

    <pattern name="beamer">
      <description>Presentation slides with Beamer</description>
      <example>
        #+TITLE: Presentation Title
        #+AUTHOR: Presenter
        #+OPTIONS: H:2 toc:nil
        #+BEAMER_THEME: Madrid
        #+BEAMER_COLOR_THEME: default

        - Introduction
        \*\* First Slide

        * Point one
        * Point two

        \*\* Second Slide
        #+ATTR_BEAMER: :overlay &lt;+->

        - Appears first
        - Appears second
        - Appears third

        * Conclusion
        \*\* Summary
        Key takeaways here.
      </example>
      <note>H:2 means level-2 headings become frames</note>
    </pattern>

    <pattern name="markdown_export">
      <description>Markdown export for GitHub/GitLab</description>
      <example>
        #+OPTIONS: toc:nil

        (require 'ox-md)
        (require 'ox-gfm) ; GitHub Flavored Markdown
      </example>
      <note>C-c C-e m m to export to Markdown</note>
    </pattern>

    <pattern name="publishing">
      <description>Multi-file publishing projects</description>
      <example>
        (setq org-publish-project-alist
        '(("org-notes"
        :base-directory "~/org/notes/"
        :base-extension "org"
        :publishing-directory "~/public_html/"
        :recursive t
        :publishing-function org-html-publish-to-html
        :headline-levels 4
        :auto-preamble t)
        ("org-static"
        :base-directory "~/org/notes/"
        :base-extension "css\\|js\\|png\\|jpg\\|gif"
        :publishing-directory "~/public_html/"
        :recursive t
        :publishing-function org-publish-attachment)
        ("org" :components ("org-notes" "org-static"))))
      </example>
      <note>C-c C-e P p to publish project</note>
    </pattern>

    <pattern name="selective_export">
      <description>Control what gets exported</description>
      <example>
        * Exported heading

        - Not exported :noexport:

        #+BEGIN_COMMENT
        This entire block is not exported.
        #+END_COMMENT

        Text for export only. @@html:&lt;br&gt;@@ continues.

        #+BEGIN_EXPORT html
        &lt;div class="custom"&gt;Raw HTML here&lt;/div&gt;
        #+END_EXPORT
      </example>
    </pattern>
  </patterns>

  <decision_tree name="export_backend">
    <question>What is the target format?</question>
    <branch condition="Web page">HTML (ox-html)</branch>
    <branch condition="Print document">PDF via LaTeX (ox-latex)</branch>
    <branch condition="Presentation slides">Beamer (ox-beamer)</branch>
    <branch condition="README/docs">Markdown (ox-md, ox-gfm)</branch>
    <branch condition="Word document">ODT (ox-odt)</branch>
  </decision_tree>
</export>

<tools>
  <tool name="org-capture">
    <description>Quick capture notes and tasks</description>
    <use_case>Capturing ideas without interrupting current work</use_case>
  </tool>

  <tool name="org-agenda">
    <description>Unified view of scheduled items and TODOs</description>
    <use_case>Daily/weekly planning and review</use_case>
  </tool>

  <tool name="org-refile">
    <description>Move entries to different locations</description>
    <use_case>Organizing captured items into proper locations</use_case>
  </tool>

  <tool name="org-babel">
    <description>Execute code blocks in documents</description>
    <use_case>Literate programming, reproducible research</use_case>
  </tool>

  <tool name="org-export">
    <description>Export to various formats</description>
    <use_case>Publishing documents, creating presentations</use_case>
  </tool>

  <tool name="org-clock">
    <description>Time tracking within org files</description>
    <use_case>Project time tracking, productivity analysis</use_case>
  </tool>
</tools>

<best_practices>
  <practice priority="critical">Use one file per major project or area of responsibility</practice>
  <practice priority="critical">Keep inbox.org for quick captures, refile regularly</practice>
  <practice priority="high">Use consistent TODO state workflow across all files</practice>
  <practice priority="high">Add SCHEDULED or DEADLINE to time-sensitive tasks</practice>
  <practice priority="high">Use tags for context (@home, @work, @phone) not categories</practice>
  <practice priority="high">Archive completed subtrees periodically</practice>
  <practice priority="medium">Use org-id for stable cross-file links</practice>
  <practice priority="medium">Set :EFFORT: property for time estimation</practice>
  <practice priority="medium">Use column view for project overviews</practice>
  <practice priority="medium">Configure org-agenda-custom-commands for common views</practice>
</best_practices>

<anti_patterns>
  <avoid name="single_giant_file">
    <description>Putting everything in one org file</description>
    <instead>Split by project, area, or topic; use org-agenda-files</instead>
  </avoid>

  <avoid name="deep_nesting">
    <description>Excessive heading depth (beyond 4-5 levels)</description>
    <instead>Refactor into separate files or flatten structure</instead>
  </avoid>

  <avoid name="no_refile">
    <description>Never refiling captured items</description>
    <instead>Regular inbox processing (daily or at least weekly)</instead>
  </avoid>

  <avoid name="overcomplex_templates">
    <description>Capture templates with too many fields</description>
    <instead>Capture quickly with minimal fields, refine later</instead>
  </avoid>

  <avoid name="babel_side_effects">
    <description>Code blocks that modify external state unexpectedly</description>
    <instead>Use :results silent for side-effect blocks, document clearly</instead>
  </avoid>

  <avoid name="hardcoded_paths">
    <description>Absolute paths in org files</description>
    <instead>Use relative paths or org-directory variable</instead>
  </avoid>
</anti_patterns>

<workflow>
  <phase name="analyze">
    <objective>Understand org document requirements</objective>
    <step>1. Identify document type: notes, project, literate program, publication</step>
    <step>2. Determine required features: GTD, babel, export</step>
    <step>3. Check existing org patterns in project</step>
  </phase>
  <phase name="implement">
    <objective>Create or modify org document</objective>
    <step>1. Set up document header with appropriate options</step>
    <step>2. Structure content with appropriate heading levels</step>
    <step>3. Add metadata (properties, tags, timestamps) as needed</step>
    <step>4. Configure babel blocks for executable content</step>
  </phase>
  <phase name="validate">
    <objective>Verify org document correctness</objective>
    <step>1. Check syntax with org-lint</step>
    <step>2. Test babel blocks execute correctly</step>
    <step>3. Verify export produces expected output</step>
  </phase>
</workflow>

<rules priority="critical">
  <rule>Use appropriate heading levels (do not skip levels)</rule>
  <rule>Close all drawers and blocks properly</rule>
  <rule>Use consistent timestamp format throughout document</rule>
</rules>

<rules priority="standard">
  <rule>Add :PROPERTIES: drawer after heading, not before</rule>
  <rule>Use #+NAME: before code blocks that are referenced</rule>
  <rule>Set document-wide header-args with #+PROPERTY:</rule>
  <rule>Use :noexport: tag for internal notes</rule>
</rules>

<error_escalation>
  <level severity="low">
    <example>Minor formatting inconsistency</example>
    <action>Fix and continue</action>
  </level>
  <level severity="medium">
    <example>Babel block execution error</example>
    <action>Debug block, check language support</action>
  </level>
  <level severity="high">
    <example>Export failure or corrupted output</example>
    <action>Check document structure, present options to user</action>
  </level>
  <level severity="critical">
    <example>Data loss from failed tangle or corrupted file</example>
    <action>Block operation, require explicit user acknowledgment</action>
  </level>
</error_escalation>

<related_agents>
  <agent name="execute">Implementation of org document structures and babel configurations</agent>
  <agent name="docs">Documentation generation from org files</agent>
  <agent name="design">Architecture for complex org-based systems</agent>
</related_agents>

<related_skills>
  <skill name="emacs-ecosystem">Emacs Lisp configuration for org-mode customization</skill>
  <skill name="serena-usage">Symbol operations for navigating org structures</skill>
  <skill name="context7-usage">Fetch latest org-mode documentation</skill>
  <skill name="technical-documentation">Documentation patterns applicable to org export</skill>
</related_skills>

<constraints>
  <must>Use consistent heading structure (do not skip levels)</must>
  <must>Close all blocks and drawers properly</must>
  <must>Use relative paths for portability</must>
  <avoid>Excessive nesting beyond 4-5 levels</avoid>
  <avoid>Side effects in babel blocks without clear documentation</avoid>
  <avoid>Hardcoded absolute paths in documents</avoid>
</constraints>
