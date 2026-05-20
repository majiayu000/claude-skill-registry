---
name: ux-design
description: UX心理学に基づくUIデザインスキル。UIコンポーネント設計時、フォーム設計時、ユーザーフロー設計時、UXレビュー時に使用。認知心理学・行動経済学の原則を適用して使いやすいインターフェースを設計する。
---

# UX Design スキル

認知心理学・行動経済学に基づくUXデザイン原則を適用し、
ユーザーにとって使いやすく、心地よいインターフェースを設計する。

## このスキルを使う場面

- UIコンポーネントの設計・実装時
- フォーム・入力インターフェースの設計時
- オンボーディング・ユーザーフローの設計時
- 既存UIのUXレビュー・改善時
- ローディング・フィードバック設計時

## 主要原則（頻出）

### 1. Aesthetic-Usability Effect（美的ユーザビリティ効果）

美しいデザインは、より使いやすいと感じられる。

```tsx
// ✅ 統一されたデザインシステム
<Card className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
  <CardHeader className="space-y-1">
    <CardTitle className="text-xl font-semibold">タイトル</CardTitle>
    <CardDescription className="text-gray-500">説明文</CardDescription>
  </CardHeader>
</Card>

// ❌ バラバラなスタイル
<div style={{ border: "1px solid black", padding: 10 }}>
  <h1>タイトル</h1>
  <p>説明文</p>
</div>
```

### 2. Doherty Threshold（0.4秒の壁）

0.4秒以上の待ち時間はユーザーの興味を失わせる。

```tsx
// ✅ 即座のフィードバック + ストリーミング
const [isPending, startTransition] = useTransition();

<Button disabled={isPending}>
  {isPending ? <Spinner className="animate-spin" /> : "送信"}
</Button>

// ✅ Optimistic Update
const { mutate } = useMutation({
  onMutate: async (newData) => {
    // 即座にUIを更新
    queryClient.setQueryData(["items"], (old) => [...old, newData]);
  },
});
```

### 3. Familiarity Bias（親近性バイアス）

既知のUIパターンを使うことで認知負荷を下げる。

```tsx
// ✅ 標準的なチャットUI
<div className="flex flex-col h-screen">
  <header className="border-b p-4">タイトル</header>
  <main className="flex-1 overflow-y-auto p-4">
    {/* メッセージ一覧 */}
  </main>
  <footer className="border-t p-4">
    <input placeholder="メッセージを入力..." />
  </footer>
</div>
```

### 4. Labor Illusion（労力の錯覚）

処理中であることを示すと、ユーザーは結果をより価値あるものと感じる。

```tsx
// ✅ 処理中の可視化
{isLoading && (
  <div className="flex items-center gap-2 text-gray-500">
    <Spinner className="animate-spin" />
    <span>AIが回答を生成中...</span>
  </div>
)}
```

### 5. Progressive Disclosure（段階的開示）

情報を段階的に表示し、必要な時に必要な情報にアクセスできるようにする。

```tsx
// ✅ 詳細は折りたたみ
<Accordion>
  <AccordionItem>
    <AccordionTrigger>詳細オプション</AccordionTrigger>
    <AccordionContent>
      {/* 高度な設定 */}
    </AccordionContent>
  </AccordionItem>
</Accordion>

// ✅ ステップ形式のフォーム
<Stepper currentStep={step}>
  <Step title="基本情報" />
  <Step title="詳細設定" />
  <Step title="確認" />
</Stepper>
```

## 設計時の適用フロー

### 1. ユーザーの状態を把握

| 状態 | 適用すべき原則 |
|------|---------------|
| 初めて使う | Familiarity Bias, Progressive Disclosure |
| 待っている | Doherty Threshold, Labor Illusion |
| 選択に迷っている | Default Bias, Decoy Effect |
| 離脱しそう | Peak-End Rule, Goal Gradient Effect |

### 2. 認知負荷を最小化

- **視覚的階層**: 重要な情報を目立たせる
- **チャンキング**: 情報をグループ化する
- **一貫性**: 同じ操作は同じ見た目にする

### 3. フィードバックを設計

- **即時性**: 0.4秒以内に何らかの反応
- **進捗表示**: 長い処理はプログレス表示
- **完了確認**: 成功・失敗を明確に伝える

## 参照ドキュメント

詳細な原則と実装パターンは以下を参照:

- [PRINCIPLES.md](PRINCIPLES.md) - UX心理学原則一覧（43原則）
- [PATTERNS.md](PATTERNS.md) - 実装パターン集
- [CHECKLIST.md](CHECKLIST.md) - UXレビューチェックリスト

## クイックリファレンス

### フォーム設計

| 課題 | 原則 | 実装 |
|------|------|------|
| 入力が面倒 | Default Bias | 適切なデフォルト値を設定 |
| 項目が多い | Progressive Disclosure | ステップ分割・折りたたみ |
| エラーが分かりにくい | Cognitive Load | インラインバリデーション |
| 送信に不安 | Social Proof | 「〇〇人が利用」表示 |

### ボタン・CTA設計

| 課題 | 原則 | 実装 |
|------|------|------|
| クリックされない | Visual Hierarchy | 色・サイズで強調 |
| 迷う | Decoy Effect | 推奨プランを明示 |
| 押すのが不安 | Loss Aversion | 「無料」「いつでも解約可」 |

### ローディング設計

| 課題 | 原則 | 実装 |
|------|------|------|
| 待ち時間が長い | Doherty Threshold | ストリーミング・スケルトン |
| 進捗が分からない | Labor Illusion | 処理内容を表示 |
| 完了が分からない | Peak-End Rule | 成功アニメーション |

## アンチパターン

### ❌ ダークパターン

以下は避けるべき操作的なUXパターン:

- **Confirmshaming**: 拒否オプションを恥ずかしい文言にする
- **Hidden Costs**: 最後まで追加料金を隠す
- **Roach Motel**: 登録は簡単、解約は困難
- **Trick Questions**: 紛らわしいチェックボックス

### ❌ 過剰な適用

- Gamificationの乱用（ポイント・バッジの氾濫）
- Scarcity Effectの嘘（常に「残りわずか」）
- Nudgeの強制（選択肢がないように見せる）
