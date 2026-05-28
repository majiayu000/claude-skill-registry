---
name: generate-convention-skill
description: 規約・ガイドラインからConvention Skillを生成する
---

# Generate Convention Skill

## 概要

このコマンドは、ユーザーが提供する規約・ガイドラインの内容から、Convention Skillのマークダウンファイルを生成する。引数でファイルパスが指定された場合はそのファイルの内容を解析し、引数がない場合は対話を通じて規約内容を収集する。既存のConvention Skillとの重複を確認し、標準化されたスキルドキュメントを作成する。

## 使用するエージェント

- **plugin-development-agent:** プラグイン要素の作成全体を管理し、ユーザーと対話しながら要素を設計・生成する

## 使用するスキル

1. **convention-skill-generator:** ユーザーの規約・ガイドラインから、Convention Skillのマークダウンファイルを生成する
2. **documentation-standards:** Markdownドキュメントの記述標準に従う
3. **interaction-guidelines:** ユーザーとの効果的な対話パターンに従う
4. **element-definition-convention:** プラグイン要素の定義ルールに従う
5. **plugin-architecture-convention:** プラグイン全体のアーキテクチャ設計原則に従う

## 実行フロー

1. plugin-development-agentが以下のスキルを使用して、既存のConvention Skillを確認し、重複を避ける
   - convention-skill-generator（スキル確認）
   - plugin-architecture-convention（アーキテクチャ規約遵守）

2. plugin-development-agentが以下のスキルを使用して、引数でファイルパスが指定された場合はそのファイルを読み込み、内容を解析する
   - convention-skill-generator（ファイル解析）
   - interaction-guidelines（対話パターン）

3. plugin-development-agentが以下のスキルを使用して、引数がない場合は対話を通じて情報を収集する
   - convention-skill-generator（情報収集）
   - interaction-guidelines（対話パターン）

4. plugin-development-agentが以下のスキルを使用して、コンテンツを生成する
   - convention-skill-generator（コンテンツ生成）
   - element-definition-convention（定義ルール遵守）

5. plugin-development-agentが以下のスキルを使用して、markdownlint検証を実施する
   - convention-skill-generator（検証実施）
   - documentation-standards（記述標準遵守）

6. plugin-development-agentがユーザーからのフィードバックを収集して必要に応じて修正する

## 成果物

**出力先:**

- `[プラグインディレクトリ]/skills/[スキル名]/SKILL.md`

**ファイル内容:**

- フロントマター（name, description）
- 役割セクション
- 規約・ガイドライン内容
- 適用範囲と除外範囲
- チェックリストや検証項目
- 具体例やサンプル（必要に応じて）

## チェックリスト

### コマンド実行前

- [ ] 規約・ガイドラインの内容が明確である（ファイル指定または対話で収集）
- [ ] スキルの目的と適用範囲が明確である
- [ ] 既存のConvention Skillを確認した

### コマンド実行後

- [ ] Convention Skillファイルが生成されている
- [ ] フロントマターが正しく記述されている
- [ ] 役割が明確に記述されている
- [ ] 規約・ガイドライン内容が適切に記述されている
- [ ] 適用範囲と除外範囲が定義されている
- [ ] チェックリストや検証項目が記述されている
- [ ] プラグインアーキテクチャ規約が遵守されている
- [ ] markdownlint検証に合格している
- [ ] 他の要素（エージェント、スキル、コマンド）を参照していない
- [ ] 固有名詞が使用されていない
