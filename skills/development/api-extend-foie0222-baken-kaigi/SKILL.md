---
name: api-extend
description: API拡張ワークフロー（ports → provider → handler → Mock → テスト → フロント型 → UI）を自動化
version: 1.0.0
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
skill_type: workflow
auto_invoke: false
---

# API拡張ワークフロー

## 概要

新しいAPIフィールドやエンドポイントを追加する際の定型フローを自動化します。DDD（ドメイン駆動設計）とクリーンアーキテクチャの原則に従い、以下の8ステップを実行します:

1. **ports定義** - ドメイン層のインターフェース定義
2. **provider実装** - JRA-VAN APIプロバイダー実装
3. **Mock実装** - モックプロバイダー実装
4. **handler実装** - APIハンドラー（Lambda関数）
5. **テスト作成/更新** - TDDに基づくテストコード
6. **フロント型定義** - TypeScript型とマッピング関数
7. **APIクライアント** - フロントエンドAPIクライアント更新
8. **UI実装** - React コンポーネント更新

## 入力形式

スキル呼び出し時に以下の情報を提供してください:

```
/api-extend

追加内容:
- データクラス名: <DataClass名>（例: TrainingData）
- フィールド:
  - <field_name>: <type> - <説明>
  - <field_name>: <type> - <説明>
- エンドポイント（新規の場合）: GET /path/{param}
- 既存エンドポイントへの追加（の場合）: <エンドポイント名>
```

## 実行プロセス

### ステップ1: ports定義（ドメイン層）

**ファイル**: `main/backend/src/domain/ports/race_data_provider.py`

**パターン**:
```python
@dataclass(frozen=True)
class <DataClass>:
    """<説明>."""

    field_name: type
    field_name: type | None = None  # オプショナルフィールド

class RaceDataProvider(ABC):
    @abstractmethod
    def get_<method_name>(self, <params>) -> <ReturnType>:
        """<説明>."""
        pass
```

**重要な規則**:
- すべてのデータクラスは `@dataclass(frozen=True)` でイミュータブル
- abstractmethodには必ず `pass` を記述
- 型ヒントは必須（`str | None` 形式）

### ステップ2: JRA-VAN Provider実装

**ファイル**: `main/backend/src/infrastructure/providers/jravan_race_data_provider.py`

**パターン**:
```python
def get_<method_name>(self, <params>) -> <ReturnType>:
    """<説明>."""
    try:
        response = self._session.get(
            f"{self._base_url}/<endpoint>",
            params={"param": value} if needs_params else {},
            timeout=self._timeout,
        )
        if response.status_code == 404:
            return None  # または []
        response.raise_for_status()

        # リストの場合
        data = response.json()
        return [self._to_<data_class>(d) for d in data]

        # 単一オブジェクトの場合
        return self._to_<data_class>(response.json())
    except requests.RequestException as e:
        logger.warning(f"Could not get <resource>: {e}")
        return None  # または []

def _to_<data_class>(self, data: dict) -> <DataClass>:
    """API レスポンスを <DataClass> に変換する."""
    return <DataClass>(
        field_name=data["field_name"],
        optional_field=data.get("optional_field"),
    )
```

**重要な規則**:
- 404エラーは `None` または空リスト `[]` を返す
- その他のエラーは警告ログを出力してデフォルト値を返す
- 必ず `_to_<data_class>` 変換メソッドを実装
- `data.get("key")` でオプショナルフィールドを取得

### ステップ3: Mock Provider実装

**ファイル**: `main/backend/src/infrastructure/providers/mock_race_data_provider.py`

**パターン**:
```python
def get_<method_name>(self, <params>) -> <ReturnType>:
    """<説明>."""
    import random

    random.seed(_stable_hash(str(<unique_key>)) % (2**32))

    # データを生成
    results = []
    for i in range(<count>):
        data = <DataClass>(
            field_name=random.choice(self.SAMPLE_DATA),
            numeric_field=random.randint(min, max),
            optional_field=random.choice([...]) if needed else None,
        )
        results.append(data)

    return results
```

**重要な規則**:
- 必ず `_stable_hash()` でシード固定（再現可能なデータ生成）
- クラス定数として `SAMPLE_DATA` を定義
- ランダム生成でもリアルなデータ分布を意識

### ステップ4: API Handler実装

**ファイル**: `main/backend/src/api/handlers/races.py`

**レスポンス構築パターン**:
```python
def get_<endpoint>(event: dict, context: Any) -> dict:
    """<説明>.

    GET /<path>?param=value

    Query/Path Parameters:
        param: 説明

    Returns:
        レスポンス説明
    """
    # パラメータ取得
    param = get_query_parameter(event, "param")
    # または
    param = get_path_parameter(event, "param")

    if not param:
        return bad_request_response("param is required")

    # ユースケース実行
    provider = Dependencies.get_race_data_provider()
    result = provider.get_<method>(param)

    if result is None:
        return not_found_response("<Resource>")

    # レスポンス構築
    response_data = [
        {
            "field_name": item.field_name,
            "optional_field": item.optional_field,
        }
        for item in result
    ]

    return success_response({"data": response_data})
```

**重要な規則**:
- snake_case → camelCase 変換は不要（バックエンドはsnake_case統一）
- 必ず入力バリデーション
- エラーレスポンスは `bad_request_response()`, `not_found_response()` を使用

### ステップ5: テスト作成/更新

**ファイル**: `main/backend/tests/` 配下の適切な場所

**テストパターン**:
```python
def test_get_<method_name>():
    """<説明>."""
    # Arrange
    provider = MockRaceDataProvider()

    # Act
    result = provider.get_<method_name>(<params>)

    # Assert
    assert result is not None
    assert len(result) > 0
    assert result[0].field_name == expected_value
```

**重要な規則**:
- AAA パターン（Arrange, Act, Assert）
- Mockプロバイダーを使用してテスト
- 境界値・エラーケースもテスト

### ステップ6: フロントエンド型定義

**ファイル**: `main/frontend/src/types/index.ts`

**パターン**:
```typescript
// API形式（バックエンドレスポンス）
export interface Api<DataClass> {
  field_name: string;
  optional_field?: number;
}

// フロントエンド表示用
export interface <DataClass> {
  fieldName: string;
  optionalField?: number;
}

// 変換関数
export function mapApi<DataClass>To<DataClass>(api: Api<DataClass>): <DataClass> {
  return {
    fieldName: api.field_name,
    optionalField: api.optional_field,
  };
}
```

**重要な規則**:
- API型は `Api<Name>` プレフィックス（snake_case）
- フロントエンド型は camelCase
- 必ずマッピング関数を提供

### ステップ7: APIクライアント更新

**ファイル**: `main/frontend/src/api/client.ts`

**パターン**:
```typescript
async get<Resource>(<params>): Promise<ApiResponse<<DataClass>>> {
  const response = await this.request<Api<DataClass>Response>(
    `/endpoint/${encodeURIComponent(param)}`
  );

  if (!response.success || !response.data) {
    return { success: false, error: response.error };
  }

  return {
    success: true,
    data: mapApi<DataClass>To<DataClass>(response.data),
  };
}
```

**重要な規則**:
- URLパラメータは `encodeURIComponent()` でエンコード
- レスポンス型チェックを必ず実施
- エラーハンドリングを統一

### ステップ8: UI実装ガイダンス

**対象ファイル**: `main/frontend/src/pages/*Page.tsx`, `main/frontend/src/components/*`

**提供内容**:
- どのコンポーネントを更新すべきか
- 新しいフィールドの表示例（Tailwind CSS）
- 状態管理パターン（useState, useEffect）

## 出力形式

以下の形式で進捗を報告:

```
✅ ステップ1: ports定義完了
  - <DataClass>を追加
  - get_<method>メソッドを追加

✅ ステップ2: JRA-VAN Provider実装完了
  - get_<method>を実装
  - _to_<data_class>変換メソッドを実装

✅ ステップ3: Mock Provider実装完了
  - サンプルデータ生成ロジックを実装

✅ ステップ4: API Handler実装完了
  - GET /<endpoint> エンドポイントを実装

✅ ステップ5: テスト作成完了
  - test_get_<method> を追加

✅ ステップ6: フロントエンド型定義完了
  - Api<DataClass>, <DataClass> 型を追加
  - マッピング関数を追加

✅ ステップ7: APIクライアント更新完了
  - get<Resource>メソッドを追加

⏳ ステップ8: UI実装ガイダンス
  - 更新対象: <component_path>
  - 表示例コードを提供

次のアクション:
- [ ] テスト実行（pytest）
- [ ] フロントエンドビルド確認（npm run build）
- [ ] デプロイ前チェック（./scripts/pre-deploy-check.sh）
```

## エラーハンドリング

### 頻出エラーと対処法

1. **ImportError: frozen dataclassのimport漏れ**
   - 対処: `from dataclasses import dataclass` を確認

2. **型エラー: Optional型の扱い**
   - 対処: `str | None` 形式を使用（`Optional[str]` は使わない）

3. **Mock更新漏れ**
   - 対処: 必ず Mock Provider も同時に更新

4. **フロントエンド型不整合**
   - 対処: `npm run typecheck` で確認

## 使用例

### 例1: 馬の血統情報を追加

```
/api-extend

追加内容:
- データクラス名: PedigreeData
- フィールド:
  - horse_id: str - 馬ID
  - horse_name: str | None - 馬名
  - sire_name: str | None - 父馬名
  - dam_name: str | None - 母馬名
  - broodmare_sire: str | None - 母父馬名
- エンドポイント: GET /horses/{horse_id}/pedigree
```

### 例2: 既存APIに馬体重フィールドを追加

```
/api-extend

追加内容:
- データクラス名: WeightData
- フィールド:
  - weight: int - 馬体重(kg)
  - weight_diff: int - 前走比増減
- 既存エンドポイントへの追加: GET /races/{race_id} のrunnersに追加
```

## 参照コード

実装時は以下のファイルを参照:

- **ports定義**: `main/backend/src/domain/ports/race_data_provider.py`
- **JRA-VAN Provider**: `main/backend/src/infrastructure/providers/jravan_race_data_provider.py`
- **Mock Provider**: `main/backend/src/infrastructure/providers/mock_race_data_provider.py`
- **API Handler**: `main/backend/src/api/handlers/races.py`
- **フロント型**: `main/frontend/src/types/index.ts`
- **APIクライアント**: `main/frontend/src/api/client.ts`

## 注意事項

- **TDD原則**: テストを先に書いてから実装（Red → Green → Refactor）
- **イミュータブル**: すべてのデータクラスは `frozen=True`
- **DDD原則**: ドメインロジックはポート・アダプターパターンを遵守
- **型安全性**: フロントエンドは必ず `npm run typecheck` で確認
- **git worktree**: 作業は必ず feature ブランチで（main直接push禁止）
