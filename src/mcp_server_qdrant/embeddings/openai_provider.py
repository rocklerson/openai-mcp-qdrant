"""OpenAI Compatible API を使用した埋め込みプロバイダー"""
import logging
from typing import Optional

from openai import AsyncOpenAI

from .base import EmbeddingProvider

logger = logging.getLogger(__name__)


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI Compatible API を使用した埋め込みプロバイダー"""

    # text-embedding-3-small のベクトルサイズ
    VECTOR_SIZE = 1536

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        model: str = "text-embedding-3-small",
    ):
        """初期化
        
        Args:
            api_key: OpenAI API キー
            base_url: OpenAI Compatible API のベース URL（オプション）
            model: 使用する埋め込みモデル名
        """
        self.model = model
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        logger.info(f"OpenAI埋め込みプロバイダーを初期化: model={model}, base_url={base_url}")

    async def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """ドキュメントのリストをベクトルに埋め込む
        
        Args:
            documents: 埋め込むドキュメントのリスト
            
        Returns:
            ベクトルのリスト
        """
        if not documents:
            return []

        logger.debug(f"{len(documents)}個のドキュメントを埋め込み中")
        
        try:
            response = await self.client.embeddings.create(
                input=documents,
                model=self.model,
            )
            
            # レスポンスからベクトルを抽出
            embeddings = [item.embedding for item in response.data]
            logger.debug(f"{len(embeddings)}個のベクトルを取得")
            
            return embeddings
        except Exception as e:
            logger.error(f"ドキュメントの埋め込み中にエラーが発生: {e}")
            raise

    async def embed_query(self, query: str) -> list[float]:
        """クエリをベクトルに埋め込む
        
        Args:
            query: 埋め込むクエリ
            
        Returns:
            ベクトル
        """
        logger.debug(f"クエリを埋め込み中: {query[:50]}...")
        
        try:
            response = await self.client.embeddings.create(
                input=[query],
                model=self.model,
            )
            
            embedding = response.data[0].embedding
            logger.debug(f"ベクトルを取得: サイズ={len(embedding)}")
            
            return embedding
        except Exception as e:
            logger.error(f"クエリの埋め込み中にエラーが発生: {e}")
            raise

    def get_vector_name(self) -> str:
        """Qdrantコレクションのベクトル名を取得
        
        Returns:
            ベクトル名
        """
        return self.model.replace("/", "_").replace("-", "_")

    def get_vector_size(self) -> int:
        """Qdrantコレクションのベクトルサイズを取得
        
        Returns:
            ベクトルサイズ
        """
        return self.VECTOR_SIZE

