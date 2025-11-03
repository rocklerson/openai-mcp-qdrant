"""Qdrant MCP サーバーの実装"""
import json
import logging
from typing import Annotated, Any

from fastmcp import Context, FastMCP
from pydantic import Field

from .embeddings.base import EmbeddingProvider
from .embeddings.factory import create_embedding_provider
from .qdrant import Entry, Metadata, QdrantConnector
from .settings import OpenAISettings, QdrantSettings, ToolSettings

logger = logging.getLogger(__name__)


class QdrantMCPServer(FastMCP):
    """Qdrant MCP サーバー"""

    def __init__(
        self,
        tool_settings: ToolSettings,
        qdrant_settings: QdrantSettings,
        openai_settings: OpenAISettings,
        embedding_provider: EmbeddingProvider | None = None,
        name: str = "mcp-server-qdrant",
        instructions: str | None = None,
        **settings: Any,
    ):
        """初期化
        
        Args:
            tool_settings: ツール設定
            qdrant_settings: Qdrant 設定
            openai_settings: OpenAI 設定
            embedding_provider: 埋め込みプロバイダー（オプション）
            name: サーバー名
            instructions: サーバーの説明
            **settings: その他の設定
        """
        self.tool_settings = tool_settings
        self.qdrant_settings = qdrant_settings
        self.openai_settings = openai_settings

        # 埋め込みプロバイダーを作成または使用
        if embedding_provider is None:
            self.embedding_provider = create_embedding_provider(
                api_key=openai_settings.api_key,
                base_url=openai_settings.base_url,
                model=openai_settings.embedding_model,
            )
        else:
            self.embedding_provider = embedding_provider

        # Qdrant コネクターを初期化
        self.qdrant_connector = QdrantConnector(
            url=qdrant_settings.url,
            api_key=qdrant_settings.api_key,
            collection_name=qdrant_settings.collection_name,
            embedding_provider=self.embedding_provider,
        )

        # FastMCP を初期化
        super().__init__(name=name, instructions=instructions, **settings)

        # ツールを登録
        self.setup_tools()

    def format_entry(self, entry: Entry) -> str:
        """エントリーをフォーマット
        
        Args:
            entry: フォーマットするエントリー
            
        Returns:
            フォーマットされた文字列
        """
        entry_metadata = json.dumps(entry.metadata, ensure_ascii=False) if entry.metadata else ""
        return f"<entry><content>{entry.content}</content><metadata>{entry_metadata}</metadata></entry>"

    def setup_tools(self):
        """MCP ツールを登録"""

        async def store(
            ctx: Context,
            information: Annotated[str, Field(description="保存するテキスト情報")],
            metadata: Annotated[
                Metadata | None,
                Field(
                    description="情報と一緒に保存する追加のメタデータ（JSON形式）"
                ),
            ] = None,
        ) -> str:
            """Qdrant に情報を保存
            
            Args:
                ctx: コンテキスト
                information: 保存する情報
                metadata: メタデータ（オプション）
                
            Returns:
                保存完了メッセージ
            """
            await ctx.debug(f"情報を保存中: {information[:50]}...")

            entry = Entry(content=information, metadata=metadata)
            entry_id = await self.qdrant_connector.store(entry)
            
            return f"情報を保存しました: {information[:100]}... (ID: {entry_id})"

        async def find(
            ctx: Context,
            query: Annotated[str, Field(description="検索クエリ")],
        ) -> list[str] | None:
            """Qdrant から関連情報を検索
            
            Args:
                ctx: コンテキスト
                query: 検索クエリ
                
            Returns:
                検索結果のリスト
            """
            await ctx.debug(f"クエリで検索中: {query}")

            entries = await self.qdrant_connector.search(
                query,
                limit=self.qdrant_settings.search_limit,
            )
            
            if not entries:
                return None
            
            content = [f"クエリ '{query}' の検索結果:"]
            for entry in entries:
                content.append(self.format_entry(entry))
            
            return content

        # ツールを登録
        self.tool(
            store,
            name="qdrant-store",
            description=self.tool_settings.store_description,
        )

        self.tool(
            find,
            name="qdrant-find",
            description=self.tool_settings.find_description,
        )

