import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

/**
 * Server Info Resource
 * Provides information about the MCP server
 */
export function registerInfoResource(server: McpServer) {
  server.registerResource(
    'server-info',
    'info://server',
    {
      title: 'Server Information',
      description: 'Information about this MCP server',
      mimeType: 'application/json',
    },
    async uri => {
      const info = {
        name: 'ChillMCP',
        version: '1.0.0',
        description: 'A flexible MCP server built with TypeScript',
        capabilities: {
          tools: true,
          resources: true,
          prompts: true,
        },
        runtime: {
          node: process.version,
          platform: process.platform,
          arch: process.arch,
        },
        timestamp: new Date().toISOString(),
      };

      return {
        contents: [
          {
            uri: uri.href,
            text: JSON.stringify(info, null, 2),
            mimeType: 'application/json',
          },
        ],
      };
    }
  );
}
