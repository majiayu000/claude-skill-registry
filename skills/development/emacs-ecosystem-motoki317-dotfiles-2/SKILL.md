---
name: Emacs Ecosystem
description: This skill should be used when the user asks to "write elisp", "emacs config", "init.el", "use-package", ".el file", "emacs lisp", or "magit". Provides comprehensive Emacs ecosystem patterns and best practices. For org-mode, use org-ecosystem skill.
---

# Elisp Fundamentals

S-expressions as code and data (homoiconicity). Prefix notation for all operations.

## Data Types
- **symbol**: `'foo`, `:keyword`
- **cons cell**: `(cons 1 2)` => `(1 . 2)`
- **list**: `'(1 2 3)`
- **vector**: `[1 2 3]`
- **hash-table**: `(make-hash-table)`
- **string**: `"hello"`
- **number**: `42`, `3.14`

## Core Patterns

**defun**:
```elisp
(defun my-function (arg1 arg2)
  "Docstring describing the function."
  (+ arg1 arg2))
```

**let binding**:
```elisp
(let ((x 1) (y 2)) (+ x y))
(let* ((x 1) (y (+ x 1))) y)  ; y can reference x
```

**Conditionals**: `if`, `when`, `unless`, `cond`, `pcase`

**Iteration**:
```elisp
(dolist (item list) (process item))
(dotimes (i 10) (process i))
(cl-loop for item in list collect (transform item))
(seq-map #'transform sequence)
```

**Lambda**: `(lambda (x) (* x 2))`

**Macros**: Use backquote for templates, comma for evaluation.
```elisp
(defmacro with-temp-message (msg &rest body)
  `(progn (message "%s" ,msg) ,@body))
```

# Configuration Patterns

## init.el Structure
```elisp
;;; init.el --- Emacs configuration -*- lexical-binding: t; -*-
(require 'package)
(setq package-archives
      '(("melpa" . "https://melpa.org/packages/")
        ("gnu" . "https://elpa.gnu.org/packages/")))
(package-initialize)

(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))
(eval-when-compile (require 'use-package))
;; Configuration...
(provide 'init)
;;; init.el ends here
```

## use-package
```elisp
(use-package company
  :ensure t
  :defer t
  :hook (prog-mode . company-mode)
  :bind (:map company-active-map
              ("C-n" . company-select-next)
              ("C-p" . company-select-previous))
  :custom
  (company-idle-delay 0.2)
  (company-minimum-prefix-length 2)
  :config
  (setq company-backends '(company-capf)))
```

Keywords: `:ensure` (install), `:defer` (lazy load), `:hook`, `:bind`, `:custom`, `:init` (before load), `:config` (after load), `:commands` (autoload), `:after`, `:if`/`:when`/`:unless`.

## Keybindings
```elisp
(global-set-key (kbd "C-c l") #'org-store-link)
(define-key emacs-lisp-mode-map (kbd "C-c C-e") #'eval-last-sexp)
;; With use-package
(use-package magit :bind (("C-x g" . magit-status)))
```

## Hooks
```elisp
(add-hook 'prog-mode-hook #'display-line-numbers-mode)
;; With use-package
(use-package flycheck :hook (prog-mode . flycheck-mode))
```

## Advice
```elisp
(defun my-after-save-message (orig-fun &rest args)
  (apply orig-fun args)
  (message "Saved at %s" (current-time-string)))
(advice-add 'save-buffer :around #'my-after-save-message)
```

## Custom Variables
```elisp
(defgroup my-package nil "My package customization." :group 'convenience)
(defcustom my-package-option t "Enable option." :type 'boolean :group 'my-package)
```

# Package Managers

- **package.el**: Built-in, `package-install`, `package-refresh-contents`
- **straight.el**: Functional with Git integration
- **elpaca**: Modern async package manager

# Magit

```elisp
(use-package magit
  :ensure t
  :bind (("C-x g" . magit-status)
         ("C-x M-g" . magit-dispatch)))
```

Status buffer keys: `s` stage, `u` unstage, `c c` commit, `P p` push, `F p` pull, `b b` checkout, `l l` log.

**Forge** for GitHub/GitLab: `(use-package forge :after magit)`

# LSP Integration

## eglot (Built-in, Emacs 29+)
```elisp
(use-package eglot
  :ensure nil
  :hook ((python-mode . eglot-ensure)
         (rust-mode . eglot-ensure))
  :config
  (setq eglot-autoshutdown t))
```

## lsp-mode (Feature-rich)
```elisp
(use-package lsp-mode
  :hook (python-mode . lsp-deferred)
  :custom
  (lsp-keymap-prefix "C-c l")
  (lsp-idle-delay 0.5))
(use-package lsp-ui :hook (lsp-mode . lsp-ui-mode))
```

## Completion
```elisp
;; corfu (modern)
(use-package corfu :custom (corfu-auto t) :init (global-corfu-mode))
;; company (traditional)
(use-package company :hook (after-init . global-company-mode))
```

# Modern Packages

## Vertico Stack
```elisp
(use-package vertico :init (vertico-mode))
(use-package orderless :custom (completion-styles '(orderless basic)))
(use-package marginalia :init (marginalia-mode))
(use-package consult
  :bind (("C-s" . consult-line)
         ("C-x b" . consult-buffer)))
```

## Tree-sitter (Emacs 29+)
```elisp
(setq treesit-language-source-alist
      '((python "https://github.com/tree-sitter/tree-sitter-python")))
(setq major-mode-remap-alist '((python-mode . python-ts-mode)))
```

## which-key
```elisp
(use-package which-key :diminish :init (which-key-mode))
```

# Context7 Integration
- Emacs Docs: `/websites/emacsdocs`

# Best Practices
- Enable lexical-binding in all files: `-*- lexical-binding: t; -*-`
- Use `#'function-name` for function references
- Document functions with docstrings
- Namespace all symbols with package prefix
- Prefer `seq.el` functions for sequence operations
- Use `pcase` for complex pattern matching
- Use `defcustom` for user-configurable options
- Use `provide` at end of file
- Prefer `:custom` over `setq` in use-package
- Use `:hook` instead of `add-hook` in use-package
- Lazy load packages with `:defer`, `:commands`, or `:hook`
- Use native-compilation when available (Emacs 28+)
- Prefer eglot for LSP (built-in, simpler)
- Use tree-sitter modes when available (Emacs 29+)

# Anti-patterns
- Dynamic binding without justification - Add `lexical-binding: t`
- Hardcoded paths - Use `expand-file-name`, `user-emacs-directory`
- Unconditional `require` at top level - Use autoload, `:defer`
- Modifying global state without restoration - Use `let`, `save-excursion`
- Lambdas in hooks (hard to remove) - Define named functions
- `setq` for defcustom variables - Use `customize-set-variable` or `:custom`
- Deprecated `cl` library - Use `cl-lib` with `cl-` prefixes
- `eval-after-load` with string - Use `with-eval-after-load` or `:config`

# Related Skills
- **org-ecosystem**: Org-mode document creation, GTD workflow, Babel, export patterns
