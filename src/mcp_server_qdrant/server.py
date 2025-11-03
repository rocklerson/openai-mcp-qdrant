"""MCP サーバーのエントリーポイント"""
import logging

from .mcp_server import QdrantMCPServer
from .settings import OpenAISettings, QdrantSettings, ToolSettings

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """メイン関数"""
    try:
        # 設定を読み込み
        tool_settings = ToolSettings()
        qdrant_settings = QdrantSettings()
        openai_settings = OpenAISettings()
        
        logger.info("MCP サーバーを起動中...")
        logger.info(f"Qdrant URL: {qdrant_settings.url}")
        logger.info(f"コレクション名: {qdrant_settings.collection_name}")
        logger.info(f"埋め込みモデル: {openai_settings.embedding_model}")
        if openai_settings.base_url:
            logger.info(f"OpenAI Base URL: {openai_settings.base_url}")
        
        # MCP サーバーを作成
        mcp = QdrantMCPServer(
            tool_settings=tool_settings,
            qdrant_settings=qdrant_settings,
            openai_settings=openai_settings,
        )
        
        logger.info("MCP サーバーが正常に起動しました")
        
        # サーバーを返す（FastMCP が自動的に実行）
        return mcp
        
    except Exception as e:
        logger.error(f"サーバーの起動中にエラーが発生: {e}")
        raise


# FastMCP のエントリーポイント
mcp = main()


if __name__ == "__main__":
    # 直接実行された場合
    import sys
    sys.exit(0)

