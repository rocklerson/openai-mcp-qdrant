"""
OpenAI MCP Qdrant サーバーの使用例

このファイルは、MCP サーバーの使用方法を示す例です。
実際に実行するには、環境変数を設定する必要があります。

## 環境変数の設定

必須の環境変数：
- OPENAI_API_KEY: OpenAI API キー
- QDRANT_URL: Qdrant サーバーの URL（デフォルト: http://localhost:6333）

オプションの環境変数：
- OPENAI_BASE_URL: OpenAI Compatible API のベース URL
- OPENAI_EMBEDDING_MODEL: 埋め込みモデル名（デフォルト: text-embedding-3-small）
- QDRANT_API_KEY: Qdrant API キー
- QDRANT_COLLECTION_NAME: コレクション名（デフォルト: mcp_memories）
- QDRANT_SEARCH_LIMIT: 検索結果の最大数（デフォルト: 5）

## 使用方法

### 1. 環境変数を設定

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # オプション
export QDRANT_URL="http://localhost:6333"
export QDRANT_COLLECTION_NAME="my_collection"
```

### 2. MCP サーバーを起動

#### stdio モード（ローカル MCP クライアント用）
```bash
fastmcp run src/mcp_server_qdrant/server.py
```

#### SSE モード（リモート MCP クライアント用）
```bash
fastmcp run src/mcp_server_qdrant/server.py --transport sse
```

#### 開発モード（MCP インスペクター付き）
```bash
fastmcp dev src/mcp_server_qdrant/server.py
```

### 3. Claude Desktop での設定

claude_desktop_config.json に以下を追加：

```json
{
  "mcpServers": {
    "qdrant": {
      "command": "fastmcp",
      "args": ["run", "/path/to/workspace/src/mcp_server_qdrant/server.py"],
      "env": {
        "OPENAI_API_KEY": "your-api-key",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "QDRANT_URL": "http://localhost:6333",
        "QDRANT_COLLECTION_NAME": "claude_memories"
      }
    }
  }
}
```

### 4. 利用可能なツール

#### qdrant-store
情報を Qdrant に保存します。

パラメータ：
- information (string): 保存するテキスト情報
- metadata (object, optional): 追加のメタデータ（JSON形式）

例：
```
情報を保存: "Python は動的型付けのプログラミング言語です"
メタデータ: {"category": "programming", "language": "python"}
```

#### qdrant-find
Qdrant から関連情報を検索します。

パラメータ：
- query (string): 検索クエリ

例：
```
クエリ: "プログラミング言語について教えて"
```

## OpenAI Compatible API の使用

このサーバーは OpenAI Compatible API をサポートしているため、
以下のようなサービスでも使用できます：

- OpenAI API
- Azure OpenAI
- その他の OpenAI 互換 API（例: vLLM, FastChat など）

OPENAI_BASE_URL を設定することで、任意の互換 API を使用できます。

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

## トラブルシューティング

### エラー: "OPENAI_API_KEY is required"
環境変数 OPENAI_API_KEY が設定されていません。
.env ファイルを作成するか、環境変数を設定してください。

### エラー: "Failed to connect to Qdrant"
Qdrant サーバーが起動していないか、URL が正しくありません。
QDRANT_URL を確認してください。

### エラー: "Collection not found"
コレクションは自動的に作成されます。
初回実行時にこのエラーが出る場合は、再度実行してください。
"""

# このファイルは実行可能ではありません。
# 上記のコメントを参照して、MCP サーバーを起動してください。

if __name__ == "__main__":
    print(__doc__)

