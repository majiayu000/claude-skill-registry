---
name: Common Lisp Ecosystem
description: This skill should be used when the user asks to "write common lisp", "CLOS", "ASDF", "defpackage", "defsystem", or works with Common Lisp, SBCL, or Coalton. Provides comprehensive Common Lisp ecosystem patterns and best practices.
---

<purpose>
  Provide comprehensive patterns for Common Lisp, CLOS, ASDF system definition, SBCL-specific features, and Coalton integration.
</purpose>

<tools>
  <tool>Read - Analyze ASDF system definitions and Lisp source files</tool>
  <tool>Edit - Modify Common Lisp code and system definitions</tool>
  <tool>Bash - Run SBCL, Roswell, Qlot commands</tool>
  <tool>mcp__context7__get-library-docs - Fetch ASDF, SBCL, and library documentation</tool>
</tools>

<concepts>
  <concept name="s_expressions">Homoiconic syntax: code and data share the same structure, enabling powerful macro systems</concept>
  <concept name="clos">Generic functions with multiple dispatch; method combination (:before, :after, :around)</concept>
  <concept name="conditions">Handler-case for catching, restart-case for recovery points; more powerful than exceptions</concept>
  <concept name="packages">Namespace management with defpackage; use :import-from or local-nicknames over bare :use</concept>
</concepts>

<common_lisp_fundamentals>
  <concept name="s_expressions">
    <description>Code and data share the same syntax (homoiconicity). Enables powerful macro systems for code transformation.</description>
  </concept>

  <concept name="symbols">
    <description>First-class named objects used for identifiers. Interned in packages, can have value, function, and property list.</description>
  </concept>

  <concept name="multiple_values">
    <description>Functions can return multiple values using values, multiple-value-bind, multiple-value-list.</description>
  </concept>

  <concept name="dynamic_binding">
    <description>Special variables with dynamic scope using defvar/defparameter. Convention: *earmuffs* for special variables.</description>
  </concept>
</common_lisp_fundamentals>

<clos>
  <description>Common Lisp Object System - Generic functions and multiple dispatch</description>

  <pattern name="defclass">
    <description>Define a class with slots. Slot options: :initarg, :initform, :accessor, :reader, :writer, :type, :documentation.</description>
    <example>
      (defclass person ()
        ((name :initarg :name :accessor person-name)
         (age :initarg :age :accessor person-age))
        (:documentation "Represents a person."))
    </example>
  </pattern>

  <pattern name="defgeneric_defmethod">
    <description>Define generic functions with multiple method implementations.</description>
    <example>
      (defgeneric greet (entity)
        (:documentation "Greet an entity."))

      (defmethod greet ((p person))
        (format t "Hello, ~a!~%" (person-name p)))
    </example>
    <decision_tree name="when_to_use">
      <question>Do you need polymorphic behavior based on multiple types?</question>
      <if_yes>Use defgeneric and defmethod for multiple dispatch</if_yes>
      <if_no>Use regular functions for single implementation</if_no>
    </decision_tree>
  </pattern>

  <pattern name="method_combination">
    <description>Method qualifiers (:before, :after, :around) for aspect-oriented programming.</description>
    <example>
      (defmethod greet :before ((p person))
        (format t "Preparing to greet...~%"))

      (defmethod greet :around ((p person))
        (format t "[Start]~%")
        (call-next-method)
        (format t "[End]~%"))
    </example>
  </pattern>

  <pattern name="multiple_inheritance">
    <description>Classes can inherit from multiple parent classes. Uses C3 linearization for method resolution order.</description>
    <example>
      (defclass employee (person job-holder)
        ((employee-id :initarg :id :accessor employee-id)))
    </example>
  </pattern>
</clos>

<conditions>
  <description>Common Lisp condition system - Restarts and handlers</description>

  <pattern name="handler_case">
    <description>Handle conditions similar to try-catch</description>
    <example>
      (handler-case
          (/ 1 0)
        (division-by-zero (c)
          (format t "Caught: ~a~%" c)
          0))
    </example>
  </pattern>

  <pattern name="handler_bind">
    <description>Handle conditions without unwinding stack</description>
    <example>
      (handler-bind
          ((error #'(lambda (c)
                      (format t "Error occurred: ~a~%" c)
                      (invoke-restart 'use-value 0))))
        (restart-case
            (error "Something went wrong")
          (use-value (v) v)))
    </example>
  </pattern>

  <pattern name="restart_case">
    <description>Define recovery points</description>
    <example>
      (defun parse-entry (entry)
        (restart-case
            (parse-integer entry)
          (use-value (v)
            :report "Use a different value"
            :interactive (lambda () (list (read)))
            v)
          (skip-entry ()
            :report "Skip this entry"
            nil)))
    </example>
    <decision_tree name="when_to_use">
      <question>Can the error be recovered interactively or programmatically?</question>
      <if_yes>Provide restarts for different recovery strategies</if_yes>
      <if_no>Use handler-case for simple error handling</if_no>
    </decision_tree>
  </pattern>

  <pattern name="define_condition">
    <description>Define custom condition types for structured error handling.</description>
    <example>
      (define-condition invalid-input (error)
        ((value :initarg :value :reader invalid-input-value))
        (:report (lambda (c stream)
                   (format stream "Invalid input: ~a"
                           (invalid-input-value c)))))
    </example>
  </pattern>
</conditions>

<packages>
  <pattern name="defpackage">
    <description>Define packages with explicit dependencies and exports.</description>
    <example>
      (defpackage #:my-project
        (:use #:cl)
        (:import-from #:alexandria #:when-let #:if-let)
        (:export #:main
                 #:process-data))
    </example>
  </pattern>

  <pattern name="package_local_nicknames">
    <description>Define local package nicknames for shorter, clearer references.</description>
    <example>
      (defpackage #:my-project
        (:use #:cl)
        (:local-nicknames (#:a #:alexandria)
                          (#:s #:serapeum)))
    </example>
  </pattern>
</packages>

<asdf>
  <description>Another System Definition Facility - Build system for Common Lisp</description>

  <pattern name="basic_defsystem">
    <description>Basic ASDF system definition with metadata and component dependencies.</description>
    <example>
      (defsystem "my-project"
        :description "My project description"
        :version "0.1.0"
        :author "Author Name"
        :license "MIT"
        :depends-on ("alexandria" "cl-ppcre")
        :components ((:file "package")
                     (:file "utils" :depends-on ("package"))
                     (:file "main" :depends-on ("utils"))))
    </example>
  </pattern>

  <pattern name="module_organization">
    <description>Organize system components into modules for better structure.</description>
    <example>
      (defsystem "my-project"
        :components
        ((:module "src"
          :components ((:file "package")
                       (:file "core" :depends-on ("package"))))
         (:module "tests"
          :depends-on ("src")
          :components ((:file "test-suite")))))
    </example>
  </pattern>

  <pattern name="package_inferred_system">
    <description>Infer dependencies from defpackage forms for modern, maintainable systems.</description>
    <example>
      (defsystem "my-project"
        :class :package-inferred-system
        :depends-on ("my-project/main"))

      ;; In my-project/main.lisp:
      (defpackage #:my-project/main
        (:use #:cl)
        (:import-from #:my-project/utils #:helper))
    </example>
    <decision_tree name="when_to_use">
      <question>Do you want automatic dependency inference from package definitions?</question>
      <if_yes>Use package-inferred-system for modern projects</if_yes>
      <if_no>Use traditional defsystem with explicit component dependencies</if_no>
    </decision_tree>
  </pattern>

  <pattern name="test_system">
    <description>Define test system with automatic test execution using test-op.</description>
    <example>
      (defsystem "my-project/test"
        :depends-on ("my-project" "fiveam")
        :components ((:file "tests"))
        :perform (test-op (o s)
                   (uiop:symbol-call :fiveam '#:run!
                     (uiop:find-symbol* '#:my-test-suite :my-project/test))))
    </example>
  </pattern>

  <pattern name="project_structure">
    <description>Recommended directory layout for Common Lisp projects.</description>
    <example>
      my-project/
      ├── my-project.asd
      ├── src/
      │   ├── package.lisp
      │   ├── utils.lisp
      │   └── main.lisp
      └── tests/
          └── test-suite.lisp
    </example>
  </pattern>
</asdf>

<sbcl>
  <description>Steel Bank Common Lisp - High-performance implementation</description>

  <pattern name="save_executable">
    <description>Create standalone executable with SBCL.</description>
    <example>
      (defun main ()
        (format t "Hello, World!~%")
        (sb-ext:exit :code 0))

      (sb-ext:save-lisp-and-die "my-app"
        :toplevel #'main
        :executable t
        :compression t)
    </example>
  </pattern>

  <pattern name="threading">
    <description>SBCL threading support with make-thread and mutex synchronization.</description>
    <example>
      (defvar *result* nil)

      (let ((thread (sb-thread:make-thread
                      (lambda ()
                        (setf _result_ (heavy-computation)))
                      :name "worker")))
        (sb-thread:join-thread thread))

      ;; Mutex
      (defvar _lock_ (sb-thread:make-mutex))
      (sb-thread:with-mutex (_lock_)
        (critical-section))
    </example>
  </pattern>

  <pattern name="foreign_function">
    <description>Call C functions from SBCL using sb-alien interface.</description>
    <example>
      (sb-alien:define-alien-routine "strlen" sb-alien:int
        (str sb-alien:c-string))

      (strlen "hello") ; => 5
    </example>
  </pattern>

  <pattern name="optimization">
    <description>Use declarations for type information and optimization settings. Options: type, ftype, inline, optimize.</description>
    <example>
      (defun fast-add (x y)
        (declare (type fixnum x y)
                 (optimize (speed 3) (safety 0)))
        (the fixnum (+ x y)))
    </example>
  </pattern>

  <pattern name="sbcl_extensions">
    <description>SBCL-specific extensions for system interaction and performance tuning.</description>
    <example>
      ;; Command-line arguments
      sb-ext:*posix-argv*

      ;; Execute external programs
      (sb-ext:run-program "/bin/ls" '("-l"))

      ;; Trigger garbage collection
      (sb-ext:gc)

      ;; POSIX interface: sb-posix
      ;; Network sockets: sb-bsd-sockets
    </example>
  </pattern>
</sbcl>

<coalton>
  <description>Statically typed functional programming on Common Lisp</description>

  <pattern name="basic_types">
    <description>Define algebraic data types in Coalton with type-safe operations.</description>
    <example>
      (coalton-toplevel
        (define-type (Maybe a)
          None
          (Some a))

        (declare safe-div (Integer -> Integer -> (Maybe Integer)))
        (define (safe-div x y)
          (if (== y 0)
              None
              (Some (/ x y)))))
    </example>
  </pattern>

  <pattern name="type_classes">
    <description>Define type classes for polymorphic behavior in Coalton.</description>
    <example>
      (coalton-toplevel
        (define-class (Printable a)
          (print-it (a -> String)))

        (define-instance (Printable Integer)
          (define (print-it x)
            (into x))))
    </example>
  </pattern>

  <pattern name="coalton_integration">
    <description>Coalton compiles to efficient Common Lisp code and is interoperable with regular CL.</description>
    <note>Use coalton-toplevel for type-safe code sections</note>
    <note>Coalton functions can call CL functions and vice versa</note>
    <note>Provides Hindley-Milner type inference with type classes</note>
  </pattern>
</coalton>

<context7_libraries>
  <description>Available Context7 documentation libraries for Common Lisp ecosystem.</description>

  <tool name="context7_common_lisp_docs">
    <description>Common Lisp Docs - General Common Lisp documentation</description>
    <param name="library_id">/lisp-docs/lisp-docs.github.io</param>
    <param name="trust_score">4.7</param>
    <param name="snippets">580</param>
  </tool>

  <tool name="context7_asdf">
    <description>ASDF - Another System Definition Facility documentation</description>
    <param name="library_id">/websites/asdf_common-lisp_dev</param>
    <param name="trust_score">7.5</param>
    <param name="snippets">190</param>
  </tool>

  <tool name="context7_sbcl">
    <description>SBCL - Steel Bank Common Lisp documentation</description>
    <param name="library_id">/sbcl/sbcl</param>
    <param name="trust_score">8.0</param>
    <param name="snippets">86</param>
  </tool>

  <tool name="context7_cffi">
    <description>CFFI - Common Foreign Function Interface documentation</description>
    <param name="library_id">/websites/cffi_common-lisp_dev</param>
    <param name="trust_score">7.5</param>
    <param name="snippets">198</param>
  </tool>

  <tool name="context7_fiveam">
    <description>FiveAM - Testing framework documentation</description>
    <param name="library_id">/websites/fiveam_common-lisp_dev</param>
    <param name="trust_score">7.5</param>
    <param name="snippets">164</param>
  </tool>

  <tool name="context7_coalton">
    <description>Coalton - Statically typed functional programming documentation</description>
    <param name="library_id">/coalton-lang/coalton</param>
    <param name="trust_score">6.6</param>
    <param name="snippets">568</param>
  </tool>

  <pattern name="retrieve_documentation">
    <description>Use resolve-library-id then get-library-docs for latest documentation.</description>
    <example>
      ;; Get ASDF documentation
      mcp__context7__get-library-docs
        context7CompatibleLibraryID="/websites/asdf_common-lisp_dev"
        topic="defsystem"
    </example>
  </pattern>
</context7_libraries>

<common_patterns>
  <pattern name="with_macro">
    <description>Resource management with unwind-protect for cleanup.</description>
    <example>
      (defmacro with-open-socket ((var host port) &body body)
        `(let ((,var (make-socket ,host ,port)))
           (unwind-protect
               (progn ,@body)
             (close-socket ,var))))
    </example>
  </pattern>

  <pattern name="loop_macro">
    <description>Loop macro for iteration with collection, filtering, and accumulation.</description>
    <example>
      (loop for item in list
            for i from 0
            when (evenp i)
              collect item into evens
            finally (return evens))
    </example>
  </pattern>

  <pattern name="format_directives">
    <description>Common format directives: ~a (aesthetic), ~s (standard), ~d (decimal), ~f (float), ~% (newline), ~{~} (iteration), ~[~] (conditional).</description>
    <example>
      (format t "~a is ~d years old~%" name age)
    </example>
  </pattern>

  <pattern name="documentation">
    <description>Document functions with docstrings explaining purpose and parameters.</description>
    <example>
      (defun my-function (arg)
        "Docstring describing the function.
         ARG is the argument description."
        (process arg))
    </example>
  </pattern>
</common_patterns>

<best_practices>
  <practice priority="high">Use `*earmuffs*` for special variables</practice>
  <practice priority="high">Use +plus-signs+ for constants</practice>
  <practice priority="high">Prefer functional style, minimize mutation</practice>
  <practice priority="high">Provide restarts for recoverable situations</practice>
  <practice priority="high">Document exported symbols</practice>
  <practice priority="medium">Use appropriate condition types, not just error</practice>
  <practice priority="medium">Use check-type for argument validation</practice>
  <practice priority="medium">Prefer ASDF package-inferred-system for new projects</practice>
  <practice priority="medium">Consider Qlot for per-project dependency management</practice>
  <practice priority="medium">Use Roswell for portable script execution</practice>
</best_practices>

<rules priority="critical">
  <rule>Use ASDF for all system definitions; never load files directly</rule>
  <rule>Provide restarts for recoverable error conditions</rule>
  <rule>Document all exported symbols with docstrings</rule>
</rules>

<rules priority="standard">
  <rule>Use *earmuffs* for special variables, +plus-signs+ for constants</rule>
  <rule>Prefer :import-from over bare :use for clear dependencies</rule>
  <rule>Use check-type for argument validation at function boundaries</rule>
  <rule>Consider package-inferred-system for new projects</rule>
</rules>

<modern_tooling>
  <tool name="qlot">
    <description>Per-project dependency manager (like bundler/npm)</description>
    <use_case>Install dependencies from qlfile</use_case>
    <use_case>Run commands with project dependencies</use_case>
    <example>
      qlot install
      qlot exec ros run
    </example>
  </tool>

  <tool name="roswell">
    <description>Lisp implementation manager and script runner</description>
    <use_case>Install Lisp implementations or libraries</use_case>
    <use_case>Start REPL with specified implementation</use_case>
    <use_case>Build standalone executable</use_case>
    <example>
      ros install sbcl
      ros run
      ros build myapp.ros
    </example>
  </tool>
</modern_tooling>

<anti_patterns>
  <avoid name="global_state">
    <description>Global mutable state makes code harder to test and reason about.</description>
    <instead>Pass state explicitly or use closures to encapsulate mutable state.</instead>
  </avoid>

  <avoid name="bare_use">
    <description>Using :use for packages other than :cl creates namespace pollution.</description>
    <instead>Use :import-from or package-local-nicknames for clearer dependencies.</instead>
  </avoid>

  <avoid name="ignore_conditions">
    <description>Ignoring conditions loses error context and recovery opportunities.</description>
    <instead>Handle conditions with handler-case or handler-bind, and provide appropriate restarts.</instead>
  </avoid>

  <avoid name="deep_nesting">
    <description>Deeply nested code reduces readability and maintainability.</description>
    <instead>Extract helper functions and use early returns to reduce nesting depth.</instead>
  </avoid>

  <avoid name="eval_usage">
    <description>Using eval in application code is slow and defeats compile-time optimization.</description>
    <instead>Use macros for compile-time code generation or first-class functions for runtime dispatch.</instead>
  </avoid>

  <avoid name="read_macros_overuse">
    <description>Custom reader macros make code harder to read for others.</description>
    <instead>Use reader macros sparingly and document them clearly when necessary.</instead>
  </avoid>
</anti_patterns>

<workflow>
  <phase name="analyze">
    <objective>Understand Lisp code requirements</objective>
    <step>1. Check ASDF system definition</step>
    <step>2. Review existing macros and patterns</step>
    <step>3. Identify CLOS class hierarchies</step>
  </phase>
  <phase name="implement">
    <objective>Write idiomatic Common Lisp code</objective>
    <step>1. Use appropriate abstraction level</step>
    <step>2. Follow condition system for errors</step>
    <step>3. Design reusable macros carefully</step>
  </phase>
  <phase name="validate">
    <objective>Verify Lisp code correctness</objective>
    <step>1. Load system with ASDF</step>
    <step>2. Run tests with appropriate framework</step>
    <step>3. Check for compilation warnings</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Style inconsistency</example>
    <action>Fix formatting, follow project conventions</action>
  </level>
  <level severity="medium">
    <example>Compilation warning or type error</example>
    <action>Fix issue, add type declarations if needed</action>
  </level>
  <level severity="high">
    <example>Macro expansion error</example>
    <action>Debug with macroexpand, present options to user</action>
  </level>
  <level severity="critical">
    <example>Reader macro conflict</example>
    <action>Block operation, require careful namespace management</action>
  </level>
</error_escalation>

<constraints>
  <must>Use ASDF for system definition</must>
  <must>Follow condition system for error handling</must>
  <must>Document macros with clear examples</must>
  <avoid>Overly complex macros without documentation</avoid>
  <avoid>Global state without clear lifecycle</avoid>
  <avoid>Reader macros without namespace isolation</avoid>
</constraints>

<related_agents>
  <agent name="design">CLOS hierarchy design, system architecture, and package structure planning</agent>
  <agent name="execute">Common Lisp implementation with proper condition handling and ASDF systems</agent>
  <agent name="code-quality">Ensure idiomatic Common Lisp patterns and proper documentation</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Navigate CLOS hierarchies, generic functions, and symbol definitions</skill>
  <skill name="context7-usage">Access ASDF, SBCL, and Common Lisp library documentation</skill>
  <skill name="investigation-patterns">Debug condition handling, macro expansion, and SBCL-specific issues</skill>
</related_skills>
