---
name: geiser-chicken
description: Geiser REPL integration for Chicken Scheme with SplitMixTernary 3-coloring and crdt.el sexp patterns.
source: music-topos/skills
license: MIT
---

# Geiser/Chicken Scheme: 3-Coloring Skill

Geiser is the Emacs mode for Scheme REPLs. This skill provides:
- **Chicken Scheme** SplitMix64 implementation
- **3-coloring** via ternary output (-1, 0, +1)
- **crdt.el** sexp manipulation
- **Penrose diagram** ASCII generation

## Chicken Scheme SplitMix64

```scheme
;;; chicken_splitmix.scm

(define GOLDEN #x9E3779B97F4A7C15)
(define MIX1 #xBF58476D1CE4E5B9)
(define MIX2 #x94D049BB133111EB)
(define MASK64 #xFFFFFFFFFFFFFFFF)

(define (make-splitmix64 seed)
  (let ((state (bitwise-and seed MASK64)))
    (lambda ()
      (set! state (bitwise-and (+ state GOLDEN) MASK64))
      (let* ((z state)
             (z (bitwise-and (* (bitwise-xor z (arithmetic-shift z -30)) MIX1) MASK64))
             (z (bitwise-and (* (bitwise-xor z (arithmetic-shift z -27)) MIX2) MASK64)))
        (bitwise-xor z (arithmetic-shift z -31))))))

(define (splitmix-ternary rng)
  ;; Map u64 to {-1, 0, +1}
  (- (modulo (rng) 3) 1))

(define (color-at seed index)
  (let ((rng (make-splitmix64 seed)))
    (do ((i 0 (+ i 1))) ((= i index))
      (rng))
    (let ((h (rng)))
      (list (+ 10 (* (/ (bitwise-and h #xFF) 255.0) 85))          ; L
            (* (/ (bitwise-and (arithmetic-shift h -8) #xFF) 255.0) 100)  ; C
            (* (/ (bitwise-and (arithmetic-shift h -16) #xFFFF) 65535.0) 360))))) ; H
```

## 3-Coloring for Graphs

```scheme
;;; 3-color a graph using SplitMixTernary

(define (graph-3-color vertices edges seed)
  (let ((rng (make-splitmix64 seed))
        (colors (make-hash-table)))
    ;; Assign initial colors
    (for-each
      (lambda (v)
        (hash-table-set! colors v (splitmix-ternary rng)))
      vertices)
    ;; Verify no adjacent same-color (greedy fix)
    (let loop ((changed #t))
      (when changed
        (set! changed #f)
        (for-each
          (lambda (e)
            (let ((c1 (hash-table-ref colors (car e)))
                  (c2 (hash-table-ref colors (cadr e))))
              (when (= c1 c2)
                (hash-table-set! colors (cadr e) (modulo (+ c2 1) 3))
                (set! changed #t))))
          edges)))
    colors))
```

## Geiser REPL Commands

```elisp
;; In Emacs with Geiser

;; Start Chicken REPL
M-x geiser-connect RET chicken RET

;; Load color module
,load chicken_splitmix.scm

;; Generate colors
(color-at #x6761795f636f6c6f 1)
;; => (95.64 75.69 40.58)

;; Get ternary stream
(let ((rng (make-splitmix64 1069)))
  (map (lambda (_) (splitmix-ternary rng)) (iota 10)))
;; => (0 1 -1 0 1 1 -1 0 -1 1)
```

## crdt.el Sexp Patterns

For collaborative editing with crdt.el:

```scheme
;;; Sexp with metadata for crdt.el

(define (sexp-with-meta sexp author timestamp)
  `(,@sexp
    :meta (:author ,author
           :timestamp ,timestamp
           :color ,(color-at (string-hash author) timestamp))))

;;; Damage detection (changed sexps)
(define (sexp-damaged? sexp-old sexp-new)
  (not (equal? sexp-old sexp-new)))

;;; Copy-on-flight: fork sexp with new identity
(define (sexp-fork sexp new-author)
  (let ((old-meta (sexp-meta sexp)))
    (sexp-with-meta (sexp-data sexp)
                    new-author
                    (current-seconds))))
```

## Penrose Diagram Generation

```scheme
;;; ASCII Penrose tiles (P3 rhombus)

(define (penrose-tile type)
  (case type
    ((thin)
     '("  /\\"
       " /  \\"
       "/____\\"))
    ((thick)
     '(" /\\"
       "/  \\"
       "\\  /"
       " \\/"))))

(define (penrose-row n seed)
  (let ((rng (make-splitmix64 seed)))
    (map (lambda (_)
           (if (> (splitmix-ternary rng) 0)
               (penrose-tile 'thin)
               (penrose-tile 'thick)))
         (iota n))))
```

## GF(3) Conservation

```scheme
(define (gf3-conserved? trits)
  ;; Check every window of 3
  (let loop ((ts trits))
    (cond
      ((< (length ts) 3) #t)
      ((not (zero? (modulo (apply + (take ts 3)) 3))) #f)
      (else (loop (cdr ts))))))

(define (enforce-gf3 trits)
  ;; Adjust middle element to conserve GF(3)
  (if (< (length trits) 3)
      trits
      (let* ((a (car trits))
             (b (cadr trits))
             (c (caddr trits))
             (new-b (modulo (- (+ a c)) 3)))
        (cons a (cons (- new-b 1) (enforce-gf3 (cddr trits)))))))
```

## Commands

```bash
just geiser-colors      # Generate color palette in Chicken
just geiser-3color      # 3-color a test graph
just penrose-ascii      # Generate Penrose tiling
```
