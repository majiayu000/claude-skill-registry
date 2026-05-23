---
name: xenodium-elisp
description: "Xenodium's Emacs packages: chatgpt-shell, agent-shell, dwim-shell-command, and ACP integration for modern Emacs development."
source: xenodium + music-topos
license: GPL-3.0
xenomodern: true
total_stars: 2847
ironic_detachment: 0.618  # Golden ratio, naturally
---

# Xenodium Elisp Skill

> *"The best UI is no UI. The second best UI is Emacs."*

## Package Overview

| Package | Stars | Description |
|---------|-------|-------------|
| [chatgpt-shell](https://github.com/xenodium/chatgpt-shell) | 1180⭐ | Multi-LLM Emacs shell (ChatGPT, Claude, DeepSeek, Gemini, Ollama) |
| [agent-shell](https://github.com/xenodium/agent-shell) | 415⭐ | Native Emacs buffer for LLM agents via ACP |
| [dwim-shell-command](https://github.com/xenodium/dwim-shell-command) | 293⭐ | Save and apply shell commands with ease |
| [acp.el](https://github.com/xenodium/acp.el) | 109⭐ | Agent Client Protocol implementation |
| [ob-swiftui](https://github.com/xenodium/ob-swiftui) | 87⭐ | SwiftUI in Org Babel blocks |
| [sqlite-mode-extras](https://github.com/xenodium/sqlite-mode-extras) | 58⭐ | Enhanced sqlite-mode |

## chatgpt-shell: Multi-LLM Interface

```elisp
(use-package chatgpt-shell
  :custom
  (chatgpt-shell-model-version "gpt-4o")
  (chatgpt-shell-anthropic-key (getenv "ANTHROPIC_API_KEY"))
  (chatgpt-shell-openai-key (getenv "OPENAI_API_KEY"))
  :config
  ;; Switch between models
  (setq chatgpt-shell-model-versions
        '("gpt-4o" "gpt-4-turbo" "claude-3-5-sonnet" "gemini-pro")))

;; Key bindings
(global-set-key (kbd "C-c g") 'chatgpt-shell)
(global-set-key (kbd "C-c G") 'chatgpt-shell-send-region)
```

### Shell Commands

| Command | Description |
|---------|-------------|
| `chatgpt-shell` | Open interactive shell |
| `chatgpt-shell-send-region` | Send selected region |
| `chatgpt-shell-describe-code` | Explain code at point |
| `chatgpt-shell-refactor-code` | Refactor with AI |
| `chatgpt-shell-generate-unit-test` | Generate tests |

## agent-shell: ACP-Powered Agents

Agent Client Protocol enables structured agent workflows:

```elisp
(use-package agent-shell
  :after acp
  :config
  (setq agent-shell-default-agent "coding-assistant"))

;; Define custom agent
(acp-define-agent "music-topos-agent"
  :system-prompt "You are a categorical music theory assistant..."
  :tools '((:name "generate-color"
            :description "Generate deterministic color from seed"
            :parameters ((:name "seed" :type "integer")
                        (:name "index" :type "integer")))))
```

## dwim-shell-command: Smart Shell Integration

```elisp
(use-package dwim-shell-command
  :bind (("M-!" . dwim-shell-command)
         ("C-c !" . dwim-shell-command-on-marked-files)))

;; Define reusable commands
(dwim-shell-command-define
 :name "Convert to WebP"
 :command "cwebp -q 80 '<<f>>' -o '<<fne>>.webp'"
 :utils "cwebp")

(dwim-shell-command-define
 :name "FFmpeg to GIF"
 :command "ffmpeg -i '<<f>>' -vf 'fps=10,scale=320:-1' '<<fne>>.gif'"
 :utils "ffmpeg")
```

### Template Variables

| Variable | Meaning |
|----------|---------|
| `<<f>>` | Full file path |
| `<<fne>>` | File path without extension |
| `<<e>>` | File extension |
| `<<*>>` | All marked files |

## acp.el: Agent Client Protocol

```elisp
(use-package acp
  :config
  ;; Register MCP servers
  (acp-register-server
   :name "gay-mcp"
   :command '("julia" "--project=@gay" "-e" "using Gay; Gay.serve_mcp()")
   :env '(("GAY_SEED" . "1069")))
  
  (acp-register-server
   :name "firecrawl"
   :command '("npx" "-y" "firecrawl-mcp")))
```

## sqlite-mode-extras: Enhanced Database UI

```elisp
(use-package sqlite-mode-extras
  :after sqlite-mode
  :hook (sqlite-mode . sqlite-mode-extras-minor-mode)
  :bind (:map sqlite-mode-map
         ("n" . sqlite-mode-extras-next-row)
         ("p" . sqlite-mode-extras-prev-row)
         ("e" . sqlite-mode-extras-edit-cell)
         ("x" . sqlite-mode-extras-execute)))
```

## Integration with Music Topos

### Gay.jl Colors in chatgpt-shell

```elisp
(defun gay/chatgpt-shell-colorize-response ()
  "Colorize chatgpt-shell responses with deterministic colors."
  (let* ((response-count (length chatgpt-shell--conversation))
         (color (gay-color-at gay-seed-default response-count))
         (hex (gay-color-to-hex color)))
    (put-text-property (point-min) (point-max)
                       'face `(:background ,hex))))

(add-hook 'chatgpt-shell-response-hook #'gay/chatgpt-shell-colorize-response)
```

### GF(3) Conservation for Agent Responses

```elisp
(defun gay/agent-response-trit (response)
  "Map agent response to trit based on sentiment/category."
  (let* ((hash (sxhash response))
         (color (gay-color-at gay-seed-default (mod hash 1000)))
         (hue (plist-get color :H)))
    (gay-hue-to-trit hue)))

(defun gay/verify-conversation-gf3 ()
  "Verify GF(3) conservation across conversation."
  (let ((trits (mapcar #'gay/agent-response-trit 
                       chatgpt-shell--conversation)))
    (gay-gf3-conserved-p trits)))
```

## Transient Integration

```elisp
(require 'transient)

(transient-define-prefix gay-transient ()
  "Gay.el color generation commands."
  ["Colors"
   ("p" "Generate palette" gay-generate-palette)
   ("c" "Check GF(3)" gay-check-gf3)
   ("h" "Color at index" gay-color-at-interactive)]
  ["Agents"
   ("s" "Spawn hierarchy" narya/spawn-hierarchy)
   ("d" "Demo" narya/demo)]
  ["Shell"
   ("g" "ChatGPT Shell" chatgpt-shell)
   ("a" "Agent Shell" agent-shell)])

(global-set-key (kbd "C-c C-g") 'gay-transient)
```

## Xenomodern Philosophy

Xenodium's approach embodies xenomodernity through:

1. **Embrace the old** (Emacs) **while pushing forward** (LLM integration)
2. **Ironic distance** from "modern" GUIs while building better UX
3. **DWIM philosophy**: Do What I Mean, not what I said
4. **Composable primitives**: Small packages that combine powerfully

```
                    xenodium
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    Emacs Lisp     Modern LLMs     Unix Tools
    (1976)         (2022+)          (1970s)
        │              │              │
        └──────────────┴──────────────┘
                       │
              Ironic Synthesis
           (chatgpt-shell, acp.el)
```

## Commands

```bash
just xenodium-setup        # Install xenodium packages
just chatgpt-shell-demo    # Run chatgpt-shell demo
just agent-shell-config    # Configure agent-shell with MCP
just dwim-define           # Create custom dwim-shell-command
```

## Resources

- [xenodium.com](https://xenodium.com/) - Blog with Emacs tips
- [YouTube: Xenodium](https://www.youtube.com/@xenodium) - Video tutorials
- [ACP Specification](https://agentclientprotocol.com/) - Agent Client Protocol
