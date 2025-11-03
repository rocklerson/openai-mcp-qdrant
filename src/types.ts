/**
 * 型定義
 */

// メタデータの型
export type Metadata = Record<string, unknown>;

// エントリーの型
export interface Entry {
  content: string;
  metadata?: Metadata;
}

// 設定の型
export interface Config {
  openai: {
    apiKey: string;
    baseURL?: string;
    embeddingModel: string;
  };
  qdrant: {
    url: string;
    apiKey?: string;
    collectionName: string;
    searchLimit: number;
  };
}

