"""Qdrant データベース接続とデータ操作"""
import logging
import uuid
from typing import Any, Optional

from pydantic import BaseModel
from qdrant_client import AsyncQdrantClient, models

from ..embeddings.base import EmbeddingProvider

logger = logging.getLogger(__name__)

# メタデータの型定義
Metadata = dict[str, Any]


class Entry(BaseModel):
    """Qdrant に保存するエントリー"""
    
    content: str
    metadata: Optional[Metadata] = None


class QdrantConnector:
    """Qdrant データベースへの接続とデータ操作を管理"""

    def __init__(
        self,
        url: str,
        api_key: Optional[str],
        collection_name: str,
        embedding_provider: EmbeddingProvider,
    ):
        """初期化
        
        Args:
            url: Qdrant サーバーの URL
            api_key: Qdrant API キー
            collection_name: 使用するコレクション名
            embedding_provider: 埋め込みプロバイダー
        """
        self.url = url
        self.api_key = api_key
        self.collection_name = collection_name
        self.embedding_provider = embedding_provider
        
        # Qdrant クライアントを初期化
        self.client = AsyncQdrantClient(
            url=url,
            api_key=api_key,
        )
        
        logger.info(f"Qdrant コネクターを初期化: url={url}, collection={collection_name}")

    async def ensure_collection(self) -> None:
        """コレクションが存在することを確認し、存在しない場合は作成"""
        try:
            # コレクションの存在を確認
            collections = await self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection_name in collection_names:
                logger.debug(f"コレクション '{self.collection_name}' は既に存在します")
                return
            
            # コレクションを作成
            vector_size = self.embedding_provider.get_vector_size()
            vector_name = self.embedding_provider.get_vector_name()
            
            logger.info(
                f"コレクション '{self.collection_name}' を作成中: "
                f"vector_name={vector_name}, vector_size={vector_size}"
            )
            
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    vector_name: models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE,
                    )
                },
            )
            
            logger.info(f"コレクション '{self.collection_name}' を作成しました")
            
        except Exception as e:
            logger.error(f"コレクションの確認/作成中にエラーが発生: {e}")
            raise

    async def store(self, entry: Entry) -> str:
        """エントリーを Qdrant に保存
        
        Args:
            entry: 保存するエントリー
            
        Returns:
            保存されたエントリーの ID
        """
        # コレクションの存在を確認
        await self.ensure_collection()
        
        # テキストをベクトル化
        vector = await self.embedding_provider.embed_query(entry.content)
        
        # ユニークな ID を生成
        point_id = str(uuid.uuid4())
        
        # ペイロードを準備
        payload = {
            "content": entry.content,
        }
        if entry.metadata:
            payload["metadata"] = entry.metadata
        
        # Qdrant に保存
        vector_name = self.embedding_provider.get_vector_name()
        
        await self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector={vector_name: vector},
                    payload=payload,
                )
            ],
        )
        
        logger.info(f"エントリーを保存しました: id={point_id}")
        return point_id

    async def search(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.0,
    ) -> list[Entry]:
        """クエリに基づいて類似エントリーを検索
        
        Args:
            query: 検索クエリ
            limit: 返す結果の最大数
            score_threshold: スコアの閾値
            
        Returns:
            検索結果のエントリーリスト
        """
        # コレクションの存在を確認
        await self.ensure_collection()
        
        # クエリをベクトル化
        query_vector = await self.embedding_provider.embed_query(query)
        
        # Qdrant で検索
        vector_name = self.embedding_provider.get_vector_name()
        
        results = await self.client.search(
            collection_name=self.collection_name,
            query_vector=(vector_name, query_vector),
            limit=limit,
            score_threshold=score_threshold,
        )
        
        # 結果を Entry オブジェクトに変換
        entries = []
        for result in results:
            payload = result.payload
            entry = Entry(
                content=payload.get("content", ""),
                metadata=payload.get("metadata"),
            )
            entries.append(entry)
        
        logger.info(f"検索結果: {len(entries)}件のエントリーを取得")
        return entries

