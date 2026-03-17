---
name: flutter-ui-design
description: FlutterアプリのモダンUIデザインガイドライン。Material Design 3をベースに、洗練されたビジュアルを実現。
---

# Flutter UI Design Guidelines

## Purpose

このスキルは、FlutterアプリのUIを「ありきたりなデフォルト」から脱却させ、プロフェッショナルで印象的なデザインを実現するためのガイドラインを提供します。

## Typography（タイポグラフィ）

### 避けるべきパターン
- デフォルトの`Roboto`のみの使用
- 単調なフォントウェイト（Regular/Boldのみ）
- 均一なテキストサイズ

### 推奨アプローチ

```dart
// Google Fontsでモダンなフォントを使用
import 'package:google_fonts/google_fonts.dart';

// タイトル用: 個性的なディスプレイフォント
GoogleFonts.poppins(fontWeight: FontWeight.w700)
GoogleFonts.inter(fontWeight: FontWeight.w800)
GoogleFonts.plusJakartaSans()

// 本文用: 読みやすいサンセリフ
GoogleFonts.inter()
GoogleFonts.dmSans()

// コントラストを意識したサイズ階層
headlineLarge: 32sp, weight: 800
headlineMedium: 24sp, weight: 700
titleLarge: 20sp, weight: 600
bodyLarge: 16sp, weight: 400
labelSmall: 12sp, weight: 500
```

### フォントウェイトの活用
- 極端なコントラスト: `w300` と `w800` を組み合わせる
- 見出しは太く（w600-w800）、本文は通常（w400）

## Color & Theme（カラー・テーマ）

### 避けるべきパターン
- Material Design のデフォルト青/紫
- 控えめで均等なカラーパレット
- 灰色ばかりの無難なUI

### 推奨アプローチ

```dart
// ダークテーマ: 深みのある背景 + 鮮やかなアクセント
ColorScheme.dark(
  surface: Color(0xFF0F0F14),        // 深いダークグレー
  surfaceContainerHighest: Color(0xFF1A1A23),
  primary: Color(0xFF6366F1),         // 鮮やかなインディゴ
  secondary: Color(0xFF22D3EE),       // シアンアクセント
  tertiary: Color(0xFFF472B6),        // ピンクアクセント
)

// ライトテーマ: クリーンな白 + ビビッドなアクセント
ColorScheme.light(
  surface: Color(0xFFFAFAFC),
  surfaceContainerHighest: Color(0xFFF1F5F9),
  primary: Color(0xFF4F46E5),         // インディゴ
  secondary: Color(0xFF0EA5E9),       // スカイブルー
  tertiary: Color(0xFFEC4899),        // ピンク
)
```

### カラー活用のポイント
- **Dominant Color**: 1つのプライマリカラーを大胆に使用
- **Sharp Accents**: セカンダリカラーはアクセントとして控えめに
- **Semantic Colors**: 成功=緑、エラー=赤、警告=黄は直感的に

## Elevation & Depth（立体感）

### 避けるべきパターン
- フラットすぎるデザイン
- 均一なelevation
- 影の乱用

### 推奨アプローチ

```dart
// カードに微妙な立体感
Card(
  elevation: 0,
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(16),
  ),
  color: theme.colorScheme.surfaceContainerHighest,
  child: ...
)

// ソフトシャドウ（コントラスト控えめ）
BoxDecoration(
  borderRadius: BorderRadius.circular(16),
  boxShadow: [
    BoxShadow(
      color: Colors.black.withOpacity(0.04),
      blurRadius: 10,
      offset: Offset(0, 4),
    ),
  ],
)

// グラスモーフィズム効果
ClipRRect(
  borderRadius: BorderRadius.circular(16),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
    child: Container(
      color: Colors.white.withOpacity(0.1),
      child: ...
    ),
  ),
)
```

## Motion & Animation（アニメーション）

### 避けるべきパターン
- アニメーションなしの硬いUI
- 過剰で散漫なアニメーション
- 一貫性のないタイミング

### 推奨アプローチ

```dart
// ページ遷移: スムーズなフェード+スライド
PageRouteBuilder(
  transitionDuration: Duration(milliseconds: 300),
  pageBuilder: (_, __, ___) => DestinationPage(),
  transitionsBuilder: (_, animation, __, child) {
    return FadeTransition(
      opacity: animation,
      child: SlideTransition(
        position: Tween<Offset>(
          begin: Offset(0, 0.05),
          end: Offset.zero,
        ).animate(CurvedAnimation(
          parent: animation,
          curve: Curves.easeOutCubic,
        )),
        child: child,
      ),
    );
  },
)

// リスト項目: Staggered Animation
AnimatedList + interval-based delays

// タップフィードバック: 微細なスケール
Transform.scale(
  scale: isPressed ? 0.98 : 1.0,
  child: AnimatedContainer(
    duration: Duration(milliseconds: 100),
    ...
  ),
)
```

### タイミングの指針
- **短い操作（タップ）**: 100-150ms
- **画面遷移**: 250-350ms
- **複雑なアニメーション**: 400-600ms
- **Curve**: `easeOutCubic`、`easeInOutCubic` を基本に

## Layout & Spacing（レイアウト・余白）

### 避けるべきパターン
- 詰まりすぎたUI
- 不規則なパディング
- 要素間の余白不足

### 推奨アプローチ

```dart
// 8px基準のスペーシングシステム
const spacing = (
  xs: 4.0,
  sm: 8.0,
  md: 16.0,
  lg: 24.0,
  xl: 32.0,
  xxl: 48.0,
);

// コンテンツエリアの余白
Padding(
  padding: EdgeInsets.symmetric(horizontal: 20, vertical: 16),
  child: ...
)

// カード内の余白は外より大きく
Card(
  child: Padding(
    padding: EdgeInsets.all(20),
    child: ...
  ),
)

// 要素間のギャップ
SizedBox(height: 16) // 関連要素間
SizedBox(height: 32) // セクション間
```

## Components（コンポーネント）

### ボタン

```dart
// プライマリボタン: 角丸 + 十分なパディング
FilledButton(
  style: FilledButton.styleFrom(
    padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
  ),
  child: Text('Action'),
)

// アウトラインボタン
OutlinedButton(
  style: OutlinedButton.styleFrom(
    side: BorderSide(color: theme.colorScheme.outline, width: 1.5),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
  ),
)
```

### 入力フィールド

```dart
TextField(
  decoration: InputDecoration(
    filled: true,
    fillColor: theme.colorScheme.surfaceContainerHighest,
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide.none,
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide(
        color: theme.colorScheme.primary,
        width: 2,
      ),
    ),
    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 16),
  ),
)
```

### FAB

```dart
FloatingActionButton(
  elevation: 2,
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(16),
  ),
  child: Icon(Icons.add),
)
```

## Background（背景）

### 推奨テクニック

```dart
// グラデーション背景
Container(
  decoration: BoxDecoration(
    gradient: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [
        theme.colorScheme.surface,
        theme.colorScheme.surface.withOpacity(0.95),
      ],
    ),
  ),
)

// サブトルなパターン（ドット、グリッド）
CustomPaint(
  painter: DotPatternPainter(
    color: theme.colorScheme.outline.withOpacity(0.05),
    spacing: 20,
  ),
)
```

## Checklist

UIを実装する際のチェックリスト:

- [ ] デフォルトフォント以外を使用しているか
- [ ] カラーパレットにアクセントカラーがあるか
- [ ] 適切な余白・パディングが設定されているか
- [ ] インタラクションにフィードバック（アニメーション）があるか
- [ ] コンポーネントの角丸が統一されているか（12-16px推奨）
- [ ] テキストの階層（サイズ・ウェイト）が明確か
