"""設定管理"""
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class QdrantSettings(BaseSettings):
    """Qdrant 接続設定"""
    
    model_config = SettingsConfigDict(
        env_prefix="QDRANT_",
        case_sensitive=False,
    )
    
    url: str = Field(
        default="http://localhost:6333",
        description="Qdrant サーバーの URL",
    )
    api_key: Optional[str] = Field(
        default=None,
        description="Qdrant API キー",
    )
    collection_name: str = Field(
        default="mcp_memories",
        description="使用するコレクション名",
    )
    search_limit: int = Field(
        default=5,
        description="検索結果の最大数",
    )


class OpenAISettings(BaseSettings):
    """OpenAI API 設定"""
    
    model_config = SettingsConfigDict(
        env_prefix="OPENAI_",
        case_sensitive=False,
    )
    
    api_key: str = Field(
        ...,
        description="OpenAI API キー",
    )
    base_url: Optional[str] = Field(
        default=None,
        description="OpenAI Compatible API のベース URL",
    )
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="使用する埋め込みモデル",
    )


class ToolSettings(BaseSettings):
    """MCP ツール設定"""
    
    model_config = SettingsConfigDict(
        env_prefix="TOOL_",
        case_sensitive=False,
    )
    
    store_description: str = Field(
        default="Qdrant に情報を保存します。テキストとオプションのメタデータを受け取り、ベクトル化して保存します。",
        description="store ツールの説明",
    )
    find_description: str = Field(
        default="Qdrant から関連情報を検索します。クエリに基づいて意味的に類似した情報を取得します。",
        description="find ツールの説明",
    )

