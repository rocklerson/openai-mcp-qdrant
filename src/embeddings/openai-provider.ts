/**
 * OpenAI Compatible API を使用した埋め込みプロバイダー
 */

import OpenAI from 'openai';

export class OpenAIEmbeddingProvider {
  private client: OpenAI;
  private model: string;
  
  // text-embedding-3-small のベクトルサイズ
  private static readonly VECTOR_SIZE = 1536;

  constructor(apiKey: string, baseURL?: string, model: string = 'text-embedding-3-small') {
    this.model = model;
    this.client = new OpenAI({
      apiKey,
      baseURL,
    });
    
    console.log(`OpenAI埋め込みプロバイダーを初期化: model=${model}, baseURL=${baseURL || 'default'}`);
  }

  /**
   * ドキュメントのリストをベクトルに埋め込む
   */
  async embedDocuments(documents: string[]): Promise<number[][]> {
    if (documents.length === 0) {
      return [];
    }

    console.log(`${documents.length}個のドキュメントを埋め込み中`);

    try {
      const response = await this.client.embeddings.create({
        input: documents,
        model: this.model,
      });

      const embeddings = response.data.map(item => item.embedding);
      console.log(`${embeddings.length}個のベクトルを取得`);

      return embeddings;
    } catch (error) {
      console.error('ドキュメントの埋め込み中にエラーが発生:', error);
      throw error;
    }
  }

  /**
   * クエリをベクトルに埋め込む
   */
  async embedQuery(query: string): Promise<number[]> {
    console.log(`クエリを埋め込み中: ${query.substring(0, 50)}...`);

    try {
      const response = await this.client.embeddings.create({
        input: [query],
        model: this.model,
      });

      const embedding = response.data[0].embedding;
      console.log(`ベクトルを取得: サイズ=${embedding.length}`);

      return embedding;
    } catch (error) {
      console.error('クエリの埋め込み中にエラーが発生:', error);
      throw error;
    }
  }

  /**
   * Qdrantコレクションのベクトル名を取得
   */
  getVectorName(): string {
    return this.model.replace(/\//g, '_').replace(/-/g, '_');
  }

  /**
   * Qdrantコレクションのベクトルサイズを取得
   */
  getVectorSize(): number {
    return OpenAIEmbeddingProvider.VECTOR_SIZE;
  }
}

