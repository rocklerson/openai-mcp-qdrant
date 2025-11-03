/**
 * Qdrant データベース接続とデータ操作
 */

import { QdrantClient } from '@qdrant/js-client-rest';
import { v4 as uuidv4 } from 'uuid';
import { Entry } from '../types.js';
import { OpenAIEmbeddingProvider } from '../embeddings/openai-provider.js';

export class QdrantConnector {
  private client: QdrantClient;
  private collectionName: string;
  private embeddingProvider: OpenAIEmbeddingProvider;

  constructor(
    url: string,
    apiKey: string | undefined,
    collectionName: string,
    embeddingProvider: OpenAIEmbeddingProvider
  ) {
    this.collectionName = collectionName;
    this.embeddingProvider = embeddingProvider;

    this.client = new QdrantClient({
      url,
      apiKey,
    });

    console.log(`Qdrant コネクターを初期化: url=${url}, collection=${collectionName}`);
  }

  /**
   * コレクションが存在することを確認し、存在しない場合は作成
   */
  async ensureCollection(): Promise<void> {
    try {
      // コレクションの存在を確認
      const collections = await this.client.getCollections();
      const collectionExists = collections.collections.some(
        c => c.name === this.collectionName
      );

      if (collectionExists) {
        console.log(`コレクション '${this.collectionName}' は既に存在します`);
        return;
      }

      // コレクションを作成
      const vectorSize = this.embeddingProvider.getVectorSize();
      const vectorName = this.embeddingProvider.getVectorName();

      console.log(
        `コレクション '${this.collectionName}' を作成中: ` +
        `vector_name=${vectorName}, vector_size=${vectorSize}`
      );

      await this.client.createCollection(this.collectionName, {
        vectors: {
          size: vectorSize,
          distance: 'Cosine',
        },
      });

      console.log(`コレクション '${this.collectionName}' を作成しました`);
    } catch (error) {
      console.error('コレクションの確認/作成中にエラーが発生:', error);
      throw error;
    }
  }

  /**
   * エントリーを Qdrant に保存
   */
  async store(entry: Entry): Promise<string> {
    // コレクションの存在を確認
    await this.ensureCollection();

    // テキストをベクトル化
    const vector = await this.embeddingProvider.embedQuery(entry.content);

    // ユニークな ID を生成
    const pointId = uuidv4();

    // ペイロードを準備
    const payload: Record<string, unknown> = {
      content: entry.content,
    };
    if (entry.metadata) {
      payload.metadata = entry.metadata;
    }

    // Qdrant に保存
    await this.client.upsert(this.collectionName, {
      wait: true,
      points: [
        {
          id: pointId,
          vector,
          payload,
        },
      ],
    });

    console.log(`エントリーを保存しました: id=${pointId}`);
    return pointId;
  }

  /**
   * クエリに基づいて類似エントリーを検索
   */
  async search(
    query: string,
    limit: number = 5,
    scoreThreshold: number = 0.0
  ): Promise<Entry[]> {
    // コレクションの存在を確認
    await this.ensureCollection();

    // クエリをベクトル化
    const queryVector = await this.embeddingProvider.embedQuery(query);

    // Qdrant で検索
    const results = await this.client.search(this.collectionName, {
      vector: queryVector,
      limit,
      score_threshold: scoreThreshold,
    });

    // 結果を Entry オブジェクトに変換
    const entries: Entry[] = results.map(result => ({
      content: (result.payload?.content as string) || '',
      metadata: result.payload?.metadata as Record<string, unknown> | undefined,
    }));

    console.log(`検索結果: ${entries.length}件のエントリーを取得`);
    return entries;
  }
}

