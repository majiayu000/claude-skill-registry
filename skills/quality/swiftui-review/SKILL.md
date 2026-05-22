---
name: swiftui-review
description: "SwiftUIのベストプラクティスに基づくコードレビュー。パフォーマンス、アクセシビリティ、アーキテクチャをチェック。Use when: SwiftUI、View、レビュー、リファクタリング を依頼された時。"
---

# SwiftUI コードレビュー

## パフォーマンス
- [ ] 不要な@Stateの使用がないか
- [ ] @ObservedObjectの過剰な再描画がないか
- [ ] List/ForEachにidが適切に設定されているか
- [ ] 重い計算がbody内で行われていないか

## アクセシビリティ
- [ ] 画像に.accessibilityLabel()があるか
- [ ] タップ可能な要素に.accessibilityHint()があるか
- [ ] Dynamic Typeに対応しているか

## アーキテクチャ
- [ ] Viewが肥大化していないか（200行以上は分割検討）
- [ ] ビジネスロジックがViewModelに分離されているか
- [ ] PreviewProviderが適切に実装されているか