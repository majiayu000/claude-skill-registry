---
name: Common Lisp Ecosystem
description: This skill should be used when the user asks to "write common lisp", "CLOS", "ASDF", "defpackage", "defsystem", or works with Common Lisp, SBCL, or Coalton. Provides comprehensive Common Lisp ecosystem patterns and best practices.
---

# Common Lisp Ecosystem

## Core Concepts

- **S-expressions**: Homoiconic syntax; code and data share structure, enabling powerful macros
- **CLOS**: Generic functions with multiple dispatch; method combination (`:before`, `:after`, `:around`)
- **Conditions**: `handler-case` for catching, `restart-case` for recovery points; more powerful than exceptions
- **Packages**: Namespace management; use `:import-from` or local-nicknames over bare `:use`

## CLOS

```lisp
;; Define class
(defclass person ()
  ((name :initarg :name :accessor person-name)
   (age :initarg :age :accessor person-age)))

;; Generic function with methods
(defgeneric greet (entity))

(defmethod greet ((p person))
  (format t "Hello, ~a!~%" (person-name p)))

;; Method combination
(defmethod greet :before ((p person))
  (format t "Preparing...~%"))

(defmethod greet :around ((p person))
  (format t "[Start]~%")
  (call-next-method)
  (format t "[End]~%"))
```

## Condition System

```lisp
;; handler-case (like try-catch)
(handler-case
    (/ 1 0)
  (division-by-zero (c)
    (format t "Caught: ~a~%" c)
    0))

;; restart-case (recovery points)
(defun parse-entry (entry)
  (restart-case
      (parse-integer entry)
    (use-value (v)
      :report "Use a different value"
      v)
    (skip-entry ()
      :report "Skip this entry"
      nil)))

;; Custom condition
(define-condition invalid-input (error)
  ((value :initarg :value :reader invalid-input-value))
  (:report (lambda (c stream)
             (format stream "Invalid: ~a" (invalid-input-value c)))))
```

## Packages

```lisp
(defpackage #:my-project
  (:use #:cl)
  (:import-from #:alexandria #:when-let #:if-let)
  (:local-nicknames (#:a #:alexandria)
                    (#:s #:serapeum))
  (:export #:main #:process-data))
```

## ASDF System Definition

```lisp
(defsystem "my-project"
  :description "My project"
  :version "0.1.0"
  :depends-on ("alexandria" "cl-ppcre")
  :components ((:file "package")
               (:file "utils" :depends-on ("package"))
               (:file "main" :depends-on ("utils"))))

;; Package-inferred system (modern)
(defsystem "my-project"
  :class :package-inferred-system
  :depends-on ("my-project/main"))
```

## SBCL

```lisp
;; Create executable
(sb-ext:save-lisp-and-die "my-app"
  :toplevel #'main
  :executable t
  :compression t)

;; Threading
(sb-thread:make-thread (lambda () (work)) :name "worker")
(sb-thread:with-mutex (*lock*) (critical-section))

;; Type declarations for optimization
(defun fast-add (x y)
  (declare (type fixnum x y)
           (optimize (speed 3) (safety 0)))
  (the fixnum (+ x y)))
```

## Coalton (Statically Typed)

```lisp
(coalton-toplevel
  (define-type (Maybe a)
    None
    (Some a))

  (declare safe-div (Integer -> Integer -> (Maybe Integer)))
  (define (safe-div x y)
    (if (== y 0) None (Some (/ x y)))))
```

## Common Patterns

```lisp
;; Resource management with unwind-protect
(defmacro with-open-socket ((var host port) &body body)
  `(let ((,var (make-socket ,host ,port)))
     (unwind-protect (progn ,@body)
       (close-socket ,var))))

;; Loop macro
(loop for item in list
      for i from 0
      when (evenp i)
        collect item)
```

## Naming Conventions

- `*earmuffs*` for special (dynamic) variables
- `+plus-signs+` for constants
- Prefer functional style, minimize mutation

## Anti-Patterns

- **Global mutable state**: Pass state explicitly or use closures
- **Bare :use**: Use `:import-from` for clear dependencies
- **Ignoring conditions**: Handle properly, provide restarts
- **eval in application code**: Use macros or first-class functions

## Tools

- **Qlot**: Per-project dependency manager (`qlot install`, `qlot exec`)
- **Roswell**: Implementation manager and script runner (`ros install sbcl`, `ros build`)

## Context7 Reference

- ASDF: `/websites/asdf_common-lisp_dev`
- SBCL: `/sbcl/sbcl`
- Coalton: `/coalton-lang/coalton`
- FiveAM: `/websites/fiveam_common-lisp_dev`
