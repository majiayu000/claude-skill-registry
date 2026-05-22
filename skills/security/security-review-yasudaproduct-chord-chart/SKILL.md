---
name: security-review
description: セキュリティレビューを実施。脆弱性チェック、セキュリティベストプラクティス確認、OWASP Top 10対策の際に使用。
---

# セキュリティレビュースキル

ChordBook プロジェクトのセキュリティレビューガイドラインです。

## OWASP Top 10 チェックリスト

### 1. インジェクション攻撃
- [ ] **SQLインジェクション**: パラメータ化クエリを使用しているか
- [ ] **コマンドインジェクション**: ユーザー入力をシェルコマンドに渡していないか
- [ ] **XSS (クロスサイトスクリプティング)**: ユーザー入力を適切にエスケープしているか

#### チェックポイント (バックエンド)
```csharp
// NG: 文字列連結
var query = $"SELECT * FROM Songs WHERE Title = '{title}'";

// OK: パラメータ化クエリ (EF Core)
var songs = await _context.Songs
    .Where(s => s.Title == title)
    .ToListAsync();
```

#### チェックポイント (フロントエンド)
```tsx
// NG: dangerouslySetInnerHTML の不適切な使用
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// OK: React のデフォルトエスケープを使用
<div>{userInput}</div>
```

### 2. 認証・認可
- [ ] JWTトークンが適切に検証されているか
- [ ] 認可チェックが全てのエンドポイントで行われているか
- [ ] パスワードポリシーが適切か
- [ ] セッション管理が安全か

#### チェックポイント
```csharp
// 認可チェックの例
[Authorize]
[HttpGet("{id}")]
public async Task<ActionResult<SongDto>> GetById(Guid id)
{
    var song = await _repository.GetByIdAsync(id, cancellationToken);

    // 所有者チェック
    if (song.UserId != User.GetUserId())
        return Forbid();

    return Ok(song);
}
```

### 3. 機密データの露出
- [ ] 機密情報がログに出力されていないか
- [ ] APIレスポンスに不要な情報が含まれていないか
- [ ] 環境変数で機密情報を管理しているか
- [ ] `.env` ファイルが `.gitignore` に含まれているか

#### チェック対象
```
.env
.env.local
*.pem
*.key
credentials.json
secrets.json
```

### 4. CSRF (クロスサイトリクエストフォージェリ)
- [ ] CSRFトークンが実装されているか
- [ ] SameSite Cookie属性が設定されているか

### 5. セキュリティヘッダー
- [ ] Content-Security-Policy
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] Strict-Transport-Security (HSTS)

### 6. 入力検証
- [ ] サーバーサイドで入力検証を行っているか
- [ ] ファイルアップロードの検証（サイズ、拡張子、MIMEタイプ）
- [ ] 数値の範囲チェック

```csharp
// FluentValidation の例
public class CreateSongValidator : AbstractValidator<CreateSongCommand>
{
    public CreateSongValidator()
    {
        RuleFor(x => x.Title)
            .NotEmpty()
            .MaximumLength(200);

        RuleFor(x => x.Bpm)
            .InclusiveBetween(20, 300)
            .When(x => x.Bpm.HasValue);
    }
}
```

### 7. エラーハンドリング
- [ ] 詳細なエラー情報が本番環境で露出していないか
- [ ] スタックトレースがユーザーに表示されていないか

```csharp
// 本番環境では詳細を隠す
if (env.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/error");
}
```

### 8. 依存関係のセキュリティ
- [ ] 既知の脆弱性がある依存パッケージがないか

```bash
# npm/pnpm
pnpm audit

# .NET
dotnet list package --vulnerable
```

## Supabase 固有のセキュリティ

### Row Level Security (RLS)
- [ ] RLSポリシーが有効化されているか
- [ ] 適切なポリシーが設定されているか

```sql
-- 例: ユーザーは自分の楽曲のみアクセス可能
CREATE POLICY "Users can view own songs"
ON songs FOR SELECT
USING (auth.uid() = user_id);
```

### API キー管理
- [ ] `anon` キーがフロントエンドで使用されているか
- [ ] `service_role` キーがサーバーサイドのみで使用されているか

## セキュリティスキャンコマンド

```bash
# npm 脆弱性チェック
cd apps/frontend
pnpm audit

# .NET 脆弱性チェック
cd apps/backend
dotnet list package --vulnerable

# 機密情報のスキャン
git secrets --scan
```

## レポートフォーマット

```markdown
## セキュリティレビュー結果

### 対象
- PR番号: #XXX
- レビュー日: YYYY-MM-DD

### 発見事項

#### 🔴 重大 (Critical)
- なし

#### 🟠 高 (High)
- なし

#### 🟡 中 (Medium)
-

#### 🟢 低 (Low)
-

### 推奨事項
1.
2.

### 結論
[ ] 承認 / [ ] 要修正
```
