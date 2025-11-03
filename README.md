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
- **FastMCP フレームワーク**: 高性能な非同期処理

## インストール

```bash
pip install -e .
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

### 基本的な使用方法

```bash
# 環境変数を設定
export OPENAI_API_KEY="your-api-key"
export QDRANT_URL="http://localhost:6333"

# 開発モードで起動（MCP インスペクター付き）
fastmcp dev src/mcp_server_qdrant/server.py

# stdio モードで起動（ローカル MCP クライアント用）
fastmcp run src/mcp_server_qdrant/server.py

# SSE モードで起動（リモート MCP クライアント用）
fastmcp run src/mcp_server_qdrant/server.py --transport sse
```

### Claude Desktop での設定

`claude_desktop_config.json` に以下を追加：

```json
{
  "mcpServers": {
    "qdrant": {
      "command": "fastmcp",
      "args": ["run", "/path/to/workspace/src/mcp_server_qdrant/server.py"],
      "env": {
        "OPENAI_API_KEY": "your-api-key",
        "QDRANT_URL": "http://localhost:6333",
        "QDRANT_COLLECTION_NAME": "claude_memories"
      }
    }
  }
}
```

詳細な使用例は `USAGE_EXAMPLES.py` を参照してください。

## プロジェクト構成

```
src/mcp_server_qdrant/
├── __init__.py
├── server.py              # メインエントリーポイント
├── mcp_server.py          # MCP サーバー実装
├── settings.py            # 環境変数設定管理
├── embeddings/
│   ├── __init__.py
│   ├── base.py            # 埋め込みプロバイダー抽象基底クラス
│   ├── openai_provider.py # OpenAI Compatible API 実装
│   └── factory.py         # ファクトリー関数
└── qdrant/
    ├── __init__.py
    └── connector.py       # Qdrant 接続とデータ操作
```

## 技術的な特徴

- **KISS 原則**: シンプルで理解しやすいコード構造
- **DRY 原則**: 重複を避けた実装
- **YAGNI 原則**: 必要な機能のみを実装
- **SOLID 原則**: 拡張可能で保守しやすい設計
- **非同期処理**: 高性能な I/O 操作
- **型ヒント**: 完全な型アノテーション
- **エラーハンドリング**: 適切なログとエラー処理

## 参考

このプロジェクトは [qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant) の実装を参考にしています。

