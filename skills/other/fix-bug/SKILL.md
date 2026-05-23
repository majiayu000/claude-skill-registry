---
name: fix-bug
description: バグ修正統合スキル（原因調査→修正→テスト→レビュー→QA→PR作成の全工程自動化）
---

# Fix Bug Skill - バグ修正統合スキル

## 役割

バグ修正の全工程を統合的に実行するスキルです。原因調査、修正実装、テスト追加、レビュー、品質保証、PR作成まで、完全なバグ修正フローを自動化します。

## 実行フロー

### Phase 1: 事前確認とブランチ作成

#### 1-1. パラメータ確認
- bug_description: バグの説明確認
- issue_number: Issue番号確認
- target: 修正対象確認（backend/frontend/both）
- suspected_files: 問題が疑われるファイル確認（オプション）

#### 1-2. ブランチ管理
```bash
# 現在のブランチを確認
git branch --show-current

# mainブランチの場合は新しいブランチを作成
# ブランチ名: fix/[bug-description-summary]-[issue_number]
# 例: fix/login-session-error-456

# mainブランチでないことを確認
```

### Phase 2: バグ原因調査

#### 2-1. エラーログ確認
```bash
# Backendログ確認（該当する場合）
grep -r "[bug related keywords]" backend/logs/
grep -r "ERROR" backend/logs/ | tail -50

# Frontendコンソールエラー確認（該当する場合）
# ブラウザDevToolsでエラー確認
```

#### 2-2. 関連コード検索
```bash
# suspected_filesが指定されている場合は優先的に確認
# 指定がない場合は、バグ説明から関連キーワードを抽出して検索

# Backendコード検索
grep -r "[keyword]" backend/src/main/java/

# Frontendコード検索
grep -r "[keyword]" frontend/
```

#### 2-3. 既存テスト確認
```bash
# 関連するテストケースを検索
# Backendテスト
find backend/src/test/java/ -name "*Test.java" | xargs grep -l "[keyword]"

# Frontendテスト
find frontend/ -name "*.test.ts*" | xargs grep -l "[keyword]"
```

#### 2-4. 原因分析レポート作成
```markdown
## バグ原因調査レポート

### バグ概要
- [bug_description]

### 再現手順（推測）
1. [手順1]
2. [手順2]
3. [手順3]

### 原因箇所
- **ファイル**: [ファイルパス]:[行番号]
- **問題**: [具体的な問題内容]
- **根本原因**: [なぜこのバグが発生したか]

### 影響範囲
- [影響を受ける機能や画面]

### 修正方針
- [どのように修正するか]

### テスト方針
- [どのようにテストするか]
```

### Phase 3: バグ修正実装

#### 3-1. Backend修正（target が "backend" または "both" の場合）

**最小限の変更で修正**:
1. 原因箇所を特定
2. 必要最小限のコード変更
3. 既存の動作を壊さないように注意
4. エラーハンドリング追加（必要に応じて）

**修正例（NullPointerException）**:
```java
// Before: バグあり
public User getUser(UUID userId) {
    User user = userMapper.selectById(userId);
    return user; // userがnullの場合、後続処理でNPE発生
}

// After: 修正後
public User getUser(UUID userId) {
    User user = userMapper.selectById(userId);
    if (user == null) {
        throw new UserNotFoundException("User not found: " + userId);
    }
    return user;
}
```

**修正後のチェック**:
- [ ] コンパイルエラーなし
- [ ] Lintエラーなし
- [ ] 既存テストが通る
- [ ] 修正箇所のテストを追加

#### 3-2. Frontend修正（target が "frontend" または "both" の場合）

**最小限の変更で修正**:
1. 原因箇所を特定
2. 必要最小限のコード変更
3. 既存の動作を壊さないように注意
4. エラーハンドリング追加（必要に応じて）

**修正例（useEffectのメモリリーク）**:
```typescript
// Before: バグあり
useEffect(() => {
  fetchData().then(data => setData(data));
}, []);
// コンポーネントアンマウント後にsetDataが呼ばれる可能性

// After: 修正後
useEffect(() => {
  let cancelled = false;

  fetchData().then(data => {
    if (!cancelled) {
      setData(data);
    }
  });

  return () => {
    cancelled = true;
  };
}, []);
```

**修正後のチェック**:
- [ ] TypeScriptエラーなし
- [ ] Lintエラーなし
- [ ] 既存テストが通る
- [ ] 修正箇所のテストを追加

### Phase 4: テスト追加（test-backend/test-frontend）

#### 4-1. Backend テスト追加（Backend修正時）

```
/test-backend target_class="[修正したクラスの完全修飾名]" test_type="unit" coverage_target=90
```

**バグ再現テストの追加**:
```java
@Test
void バグ再現_ユーザーIDがnullの場合は例外を投げる() {
    // given
    UUID userId = null;

    // when & then
    assertThatThrownBy(() -> userService.getUser(userId))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessageContaining("User ID must not be null");
}

@Test
void バグ再現_存在しないユーザーIDの場合は例外を投げる() {
    // given
    UUID userId = UUID.randomUUID();
    when(userMapper.selectById(userId)).thenReturn(null);

    // when & then
    assertThatThrownBy(() -> userService.getUser(userId))
        .isInstanceOf(UserNotFoundException.class)
        .hasMessageContaining("User not found");
}
```

#### 4-2. Frontend テスト追加（Frontend修正時）

```
/test-frontend target_file="[修正したファイルのパス]" test_type="component" coverage_target=90
```

**バグ再現テストの追加**:
```typescript
it('バグ再現: コンポーネントアンマウント後にAPIレスポンスが返ってきてもエラーにならない', async () => {
  const { unmount } = render(<UserProfile userId="123" />);

  // コンポーネントを即座にアンマウント
  unmount();

  // APIレスポンスを待つ
  await waitFor(() => {
    // エラーが発生しないことを確認
    expect(console.error).not.toHaveBeenCalled();
  });
});
```

### Phase 5: サーバー起動による動作確認

#### 5-1. Backend修正の場合
```bash
cd backend
./gradlew bootRun
```

**確認事項**:
- [ ] サーバーが正常に起動すること
- [ ] 修正した機能が正常に動作すること
- [ ] エラーログが出力されていないこと
- [ ] バグが再現しないことを確認

#### 5-2. Frontend修正の場合
```bash
cd frontend
pnpm dev
```

**確認事項**:
- [ ] サーバーが正常に起動すること
- [ ] 修正した画面/コンポーネントが正常に動作すること
- [ ] コンソールエラーが出力されていないこと
- [ ] バグが再現しないことを確認

### Phase 6: アーキテクチャレビュー（review-architecture）

```
/review-architecture target="[target]"
```

**実行内容**:
- コーディング規約準拠確認
- 修正内容の妥当性確認
- 副作用がないか確認

**判定**:
- ✅ 合格 → Phase 7へ
- ❌ 不合格 → Phase 3へ戻って修正

### Phase 7: 品質保証（qa-check）

```
/qa-check target="[target]"
```

**実行内容**:
- Lintチェック
- 既存テスト + 新規テストの実行
- ビルド検証
- カバレッジ確認

**判定**:
- ✅ 合格 → Phase 8へ
- ❌ 不合格 → Phase 3へ戻って修正

### Phase 8: PR作成（create-pr）

```
/create-pr issue_number=[issue_number]
```

**PR説明文に含める内容**:
- バグの概要
- 原因
- 修正内容
- テスト追加内容
- 確認事項

### Phase 9: 完了報告

```markdown
## Fix Bug 完了報告

### バグ概要
- [bug_description]

### Issue番号
- #[issue_number]

### PR URL
- [PR URL]

### 原因
- **ファイル**: [ファイルパス]:[行番号]
- **問題**: [具体的な問題内容]
- **根本原因**: [なぜこのバグが発生したか]

### 修正内容
- [具体的な修正内容]

### 影響範囲
- [影響を受ける機能や画面]

### テスト追加
- バグ再現テスト: [テストケース数] ケース
- 境界値テスト: [テストケース数] ケース
- 既存テスト: すべて成功

### 品質保証結果
- ✅ アーキテクチャレビュー: 合格
- ✅ QAチェック: 合格
- ✅ テストカバレッジ: [数値]%
- ✅ Lint/ビルド: 成功
- ✅ サーバー起動・動作確認: 完了
- ✅ バグ再現しないことを確認: 完了

### 次のステップ
Pull Requestのレビューを依頼してください。
```

## エラーハンドリング

### 原因特定できない場合
1. より広範囲にコード検索
2. 関連するログをすべて確認
3. 類似のバグ報告を検索
4. ユーザーに追加情報を依頼

### 修正が複雑になる場合
1. 修正方針を再検討
2. より小さな単位に分割
3. リファクタリングが必要か判断
4. ユーザーに相談

### テストが通らない場合
1. 修正内容を見直し
2. テストの期待値を確認
3. 副作用がないか確認
4. 修正を調整

## 重要な注意事項

### 最小限の変更
- バグ修正は必要最小限の変更に留める
- 関係ない箇所はリファクタリングしない
- 既存の動作を壊さない

### テストの追加必須
- バグ再現テストを必ず追加
- 同様のバグが再発しないようにする
- 境界値・異常系のテストも追加

### ドキュメント更新
- 新規エラーコードを追加した場合は error-codes.md に追記
- DB変更した場合は database-design.md を更新

## 使用するスキル一覧

1. **test-backend**: バックエンドテスト追加（Backend修正時）
2. **test-frontend**: フロントエンドテスト追加（Frontend修正時）
3. **review-architecture**: アーキテクチャレビュー
4. **qa-check**: 品質保証
5. **create-pr**: PR作成

## 参照ドキュメント

### 必須参照
- `documents/development/development-policy.md`: 開発ガイドライン
- `documents/development/coding-rules/`: コーディング規約
- `documents/development/error-codes.md`: エラーコード一覧

### バグ調査に役立つドキュメント
- `documents/architecture/database-design.md`: データベース設計
- `documents/architecture/system-architecture.md`: システムアーキテクチャ
- `documents/features/[機能名]/specification.md`: 機能仕様書
