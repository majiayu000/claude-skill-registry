---
name: astro
category: tech
user-invocable: false
description: Astroプロジェクトの設計・実装・レビューを、HTML中心/Islands/JS最小化の思想で整理する。doc/input/rdd.md に「技術スタック Astro」があるリポジトリ、またはAstro/Islands/SSG/SSR/パフォーマンス最適化の相談で使う。
---

# Astro Web-First Skill

## 参照（公式）
- [Astro公式](https://astro.build)
- [Docs](https://docs.astro.build)

## 発火条件（リポジトリ判定）
- まず `doc/input/rdd.md` を確認し、そこに `技術スタック Astro` が書かれている場合は、このSkillの方針をデフォルト採用する。
- 書かれていない場合でも、ユーザーの依頼がAstro/Islands/SSG/SSR/JS削減/速度改善に該当するなら適用する。

## このSkillの基本方針
- 基本方針: HTML中心（ドキュメント中心）。JSは必要箇所のみ（Islands）。
- レンダリング: まずSSGを第一候補。更新頻度が高い箇所のみSSR/オンデマンドを検討。
- Islands設計: 動的UIは小さく分割し、責務を限定する。島の肥大化は避ける。
- パフォーマンス: 「送らない最適化」を優先（クライアントJS、画像、フォント、3rd party）。
- 参考: [Astro公式](https://astro.build) / [Docs](https://docs.astro.build)

## 思想（判断ルール）
1. HTMLを先に完成させる（Webはまずドキュメント）。
2. クライアントJSはコスト。必要性を説明できる分だけ送る。
3. Islandsは「動的UIの特区」。島は小さく、責務を限定する。
4. “便利だから全部クライアント”を避け、送信量の最小化を優先する。

## 出力フォーマット（必ずこの順）
1. 推奨方針（1〜3行）
2. 理由（Web制約 / 性能 / 保守性）
3. 設計案（レンダリング戦略 / Islands粒度 / データ取得 / バンドル・資産 / キャッシュ）
4. チェックリスト（実装前に確認）
5. 落とし穴（避けるべき）
6. 次アクション（小さく試す順）

## チェックリスト
- [ ] Islandsは本当に必要箇所だけか
- [ ] 島が大きすぎないか（ページ/一覧まるごとを避ける）
- [ ] 画像・フォント・3rd party が速度を壊していないか
- [ ] SSGを第一候補にできているか（SSRは必要部分だけか）
- [ ] 「送らない最適化」の観点でJS量を説明できるか

## よくある落とし穴
- React等を“とりあえず”全部クライアントに送ってAstroの旨味が消える
- 島間の状態共有が増え、結果的にSPA級の複雑さになる
- 解析/広告などの3rd partyがINP/LCPを悪化させる
