---
name: pdf-automation-gotenberg
description: |
  GotenbergでPDF変換・帳票出力を自動化。HTML/Office→PDF対応。
  Use when: (1) user says「PDF変換」「帳票生成」「HTML→PDF」,
  (2) user wants automated PDF generation,
  (3) user mentions「請求書PDF」「レポートPDF化」「Gotenberg」.
  Do NOT use for: PDF読み取り（pdf-processingを使用）、
  ドキュメント変換（doc-convert-pandocを使用）。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# PDF Automation (Gotenberg)

## Instructions

- 入力（HTML/Office/URL）と品質要件（余白/ヘッダ/フォント）を確認
- 変換APIを確定し、失敗時の再試行と保存先を設計

