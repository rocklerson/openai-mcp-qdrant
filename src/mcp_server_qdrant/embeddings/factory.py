"""埋め込みプロバイダーのファクトリー関数"""
import logging

from .base import EmbeddingProvider
from .openai_provider import OpenAIEmbeddingProvider

logger = logging.getLogger(__name__)


def create_embedding_provider(
    api_key: str,
    base_url: str | None = None,
    model: str = "text-embedding-3-small",
) -> EmbeddingProvider:
    """埋め込みプロバイダーを作成
    
    Args:
        api_key: OpenAI API キー
        base_url: OpenAI Compatible API のベース URL
        model: 使用する埋め込みモデル名
        
    Returns:
        埋め込みプロバイダーのインスタンス
    """
    logger.info(f"埋め込みプロバイダーを作成: model={model}")
    
    return OpenAIEmbeddingProvider(
        api_key=api_key,
        base_url=base_url,
        model=model,
    )

