/**
 * 設定管理
 */

import { Config } from './types.js';

/**
 * 環境変数から設定を読み込む
 */
export function loadConfig(): Config {
  const openaiApiKey = process.env.OPENAI_API_KEY;
  if (!openaiApiKey) {
    throw new Error('OPENAI_API_KEY 環境変数が設定されていません');
  }

  return {
    openai: {
      apiKey: openaiApiKey,
      baseURL: process.env.OPENAI_BASE_URL,
      embeddingModel: process.env.OPENAI_EMBEDDING_MODEL || 'text-embedding-3-small',
    },
    qdrant: {
      url: process.env.QDRANT_URL || 'http://localhost:6333',
      apiKey: process.env.QDRANT_API_KEY,
      collectionName: process.env.QDRANT_COLLECTION_NAME || 'mcp_memories',
      searchLimit: parseInt(process.env.QDRANT_SEARCH_LIMIT || '5', 10),
    },
  };
}

