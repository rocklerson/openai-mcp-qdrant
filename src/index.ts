#!/usr/bin/env node

/**
 * OpenAI MCP Qdrant サーバーのエントリーポイント
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { loadConfig } from './config.js';
import { OpenAIEmbeddingProvider } from './embeddings/openai-provider.js';
import { QdrantConnector } from './qdrant/connector.js';
import { Entry, Metadata } from './types.js';

/**
 * エントリーをフォーマット
 */
function formatEntry(entry: Entry): string {
  const entryMetadata = entry.metadata ? JSON.stringify(entry.metadata) : '';
  return `<entry><content>${entry.content}</content><metadata>${entryMetadata}</metadata></entry>`;
}

/**
 * MCP サーバーを起動
 */
async function main() {
  try {
    // 設定を読み込み
    const config = loadConfig();

    console.error('MCP サーバーを起動中...');
    console.error(`Qdrant URL: ${config.qdrant.url}`);
    console.error(`コレクション名: ${config.qdrant.collectionName}`);
    console.error(`埋め込みモデル: ${config.openai.embeddingModel}`);
    if (config.openai.baseURL) {
      console.error(`OpenAI Base URL: ${config.openai.baseURL}`);
    }

    // 埋め込みプロバイダーを初期化
    const embeddingProvider = new OpenAIEmbeddingProvider(
      config.openai.apiKey,
      config.openai.baseURL,
      config.openai.embeddingModel
    );

    // Qdrant コネクターを初期化
    const qdrantConnector = new QdrantConnector(
      config.qdrant.url,
      config.qdrant.apiKey,
      config.qdrant.collectionName,
      embeddingProvider
    );

    // MCP サーバーを作成
    const server = new Server(
      {
        name: 'openai-mcp-qdrant',
        version: '0.1.3',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    // ツールのリストを返すハンドラー
    server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'qdrant-store',
          description:
            'Qdrant に情報を保存します。テキストとオプションのメタデータを受け取り、ベクトル化して保存します。',
          inputSchema: {
            type: 'object',
            properties: {
              information: {
                type: 'string',
                description: '保存するテキスト情報',
              },
              metadata: {
                type: 'object',
                description: '情報と一緒に保存する追加のメタデータ（JSON形式）',
              },
            },
            required: ['information'],
          },
        },
        {
          name: 'qdrant-find',
          description:
            'Qdrant から関連情報を検索します。クエリに基づいて意味的に類似した情報を取得します。',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: '検索クエリ',
              },
            },
            required: ['query'],
          },
        },
      ],
    }));

    // ツールの実行ハンドラー
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        if (name === 'qdrant-store') {
          const { information, metadata } = args as {
            information: string;
            metadata?: Metadata;
          };

          console.error(`情報を保存中: ${information.substring(0, 50)}...`);

          const entry: Entry = {
            content: information,
            metadata,
          };

          const entryId = await qdrantConnector.store(entry);

          return {
            content: [
              {
                type: 'text',
                text: `情報を保存しました: ${information.substring(0, 100)}... (ID: ${entryId})`,
              },
            ],
          };
        } else if (name === 'qdrant-find') {
          const { query } = args as { query: string };

          console.error(`クエリで検索中: ${query}`);

          const entries = await qdrantConnector.search(
            query,
            config.qdrant.searchLimit
          );

          if (!entries || entries.length === 0) {
            return {
              content: [
                {
                  type: 'text',
                  text: `クエリ '${query}' に一致する結果が見つかりませんでした。`,
                },
              ],
            };
          }

          const results = [`クエリ '${query}' の検索結果:`];
          for (const entry of entries) {
            results.push(formatEntry(entry));
          }

          return {
            content: [
              {
                type: 'text',
                text: results.join('\n'),
              },
            ],
          };
        } else {
          throw new Error(`未知のツール: ${name}`);
        }
      } catch (error) {
        console.error(`ツール '${name}' の実行中にエラーが発生:`, error);
        return {
          content: [
            {
              type: 'text',
              text: `エラー: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    });

    // トランスポートを作成して接続
    const transport = new StdioServerTransport();
    await server.connect(transport);

    console.error('MCP サーバーが正常に起動しました');
  } catch (error) {
    console.error('サーバーの起動中にエラーが発生:', error);
    process.exit(1);
  }
}

// サーバーを起動
main();

