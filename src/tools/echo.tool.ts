import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

/**
 * Echo Tool
 * A simple example tool that echoes back the provided message
 */
export function registerEchoTool(server: McpServer) {
  server.registerTool(
    'echo',
    {
      title: 'Echo Tool',
      description: 'Echoes back the provided message',
      inputSchema: {
        message: z.string().describe('The message to echo back'),
      },
      outputSchema: {
        echo: z.string(),
        timestamp: z.string(),
      },
    },
    async ({ message }) => {
      const output = {
        echo: message,
        timestamp: new Date().toISOString(),
      };

      return {
        content: [{ type: 'text', text: JSON.stringify(output, null, 2) }],
        structuredContent: output,
      };
    }
  );
}
