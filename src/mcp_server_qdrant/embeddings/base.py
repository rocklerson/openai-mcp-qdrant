"""埋め込みプロバイダーの抽象基底クラス"""
from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """埋め込みプロバイダーの抽象基底クラス"""

    @abstractmethod
    async def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """ドキュメントのリストをベクトルに埋め込む
        
        Args:
            documents: 埋め込むドキュメントのリスト
            
        Returns:
            ベクトルのリスト
        """
        pass

    @abstractmethod
    async def embed_query(self, query: str) -> list[float]:
        """クエリをベクトルに埋め込む
        
        Args:
            query: 埋め込むクエリ
            
        Returns:
            ベクトル
        """
        pass

    @abstractmethod
    def get_vector_name(self) -> str:
        """Qdrantコレクションのベクトル名を取得
        
        Returns:
            ベクトル名
        """
        pass

    @abstractmethod
    def get_vector_size(self) -> int:
        """Qdrantコレクションのベクトルサイズを取得
        
        Returns:
            ベクトルサイズ
        """
        pass

