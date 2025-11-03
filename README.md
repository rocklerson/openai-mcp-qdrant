# OpenAI MCP Qdrant

Qdrant MCP server with OpenAI Compatible API embedding support.

## 概要

このプロジェクトは、OpenAI Compatible API を使用した Qdrant MCP サーバーの実装です。[mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant) の実装を参考に、OpenAI の text-embedding-3-small モデルを使用してテキストをベクトル化し、Qdrant に保存・検索する機能を提供します。

## 主な機能

- **OpenAI Compatible API 統合**: text-embedding-3-small モデルによる高品質な埋め込み生成
- **カスタム Base URL サポート**: 任意の OpenAI 互換 API（Azure OpenAI、vLLM など）で使用可能
- **Qdrant 統合**: 自動コレクション作成、ベクトル保存、意味検索
- **MCP ツール**: 
  - `qdrant-store`: 情報とメタデータを保存
  - `qdrant-find`: 意味検索による関連情報の取得
- **環境変数設定**: 柔軟な設定管理
- **TypeScript 実装**: 型安全で保守しやすいコード

## インストール

### npm から

```bash
npm install -g @rocklerson/openai-mcp-qdrant
```

### ソースから

```bash
git clone https://github.com/rocklerson/openai-mcp-qdrant.git
cd openai-mcp-qdrant
npm install
npm run build
```

## 環境変数

### 必須
- `OPENAI_API_KEY`: OpenAI API キー

### オプション
- `OPENAI_BASE_URL`: OpenAI Compatible API のベース URL
- `OPENAI_EMBEDDING_MODEL`: 埋め込みモデル（デフォルト: text-embedding-3-small）
- `QDRANT_URL`: Qdrant サーバー URL（デフォルト: http://localhost:6333）
- `QDRANT_API_KEY`: Qdrant API キー
- `QDRANT_COLLECTION_NAME`: コレクション名（デフォルト: mcp_memories）
- `QDRANT_SEARCH_LIMIT`: 検索結果の最大数（デフォルト: 5）

## 使用方法

### Claude Desktop での設定

`claude_desktop_config.json` に以下を追加：

```json
{
  "mcpServers": {
    "qdrant": {
      "command": "npx",
      "args": ["-y", "@rocklerson/openai-mcp-qdrant"],
      "env": {
        "OPENAI_API_KEY": "your-api-key",
        "QDRANT_URL": "http://localhost:6333",
        "QDRANT_COLLECTION_NAME": "claude_memories"
      }
    }
  }
}
```

### ローカルでの開発

```bash
# 環境変数を設定
export OPENAI_API_KEY="your-api-key"
export QDRANT_URL="http://localhost:6333"

# ビルド
npm run build

# 実行
node dist/index.js
```

### MCP Inspector での開発

```bash
# 環境変数を設定
export OPENAI_API_KEY="your-api-key"
export QDRANT_URL="http://localhost:6333"

# ビルドと実行
npm run build
npm run inspector
```

## プロジェクト構成

```
src/
├── index.ts                      # メインエントリーポイント
├── config.ts                     # 環境変数設定管理
├── types.ts                      # 型定義
├── embeddings/
│   └── openai-provider.ts        # OpenAI Compatible API 実装
└── qdrant/
    └── connector.ts              # Qdrant 接続とデータ操作
```

## 利用可能なツール

### qdrant-store

情報を Qdrant に保存します。

**パラメータ:**
- `information` (string, 必須): 保存するテキスト情報
- `metadata` (object, オプション): 追加のメタデータ（JSON形式）

**例:**
```json
{
  "information": "Python は動的型付けのプログラミング言語です",
  "metadata": {
    "category": "programming",
    "language": "python"
  }
}
```

### qdrant-find

Qdrant から関連情報を検索します。

**パラメータ:**
- `query` (string, 必須): 検索クエリ

**例:**
```json
{
  "query": "プログラミング言語について教えて"
}
```

## Qdrant のセットアップ

### ローカル Qdrant の起動（Docker）

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Qdrant Cloud の使用

1. https://cloud.qdrant.io でアカウントを作成
2. クラスターを作成
3. API キーと URL を取得
4. 環境変数を設定：
   ```bash
   export QDRANT_URL="https://your-cluster.qdrant.io:6333"
   export QDRANT_API_KEY="your-api-key"
   ```

## 技術的な特徴

- **KISS 原則**: シンプルで理解しやすいコード構造
- **DRY 原則**: 重複を避けた実装
- **YAGNI 原則**: 必要な機能のみを実装
- **SOLID 原則**: 拡張可能で保守しやすい設計
- **型安全**: TypeScript による完全な型チェック
- **非同期処理**: async/await による高性能な I/O 操作
- **エラーハンドリング**: 適切なログとエラー処理

## 開発

```bash
# 依存関係のインストール
npm install

# ビルド
npm run build

# ウォッチモード
npm run watch
```

## ライセンス

MIT

## 参考

このプロジェクトは [qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant) の実装を参考にしています。

