import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

/**
 * Time Tool
 * Returns current time information
 */
export function registerTimeTool(server: McpServer) {
  server.registerTool(
    'get-time',
    {
      title: 'Get Current Time',
      description: 'Returns the current timestamp and timezone information',
      inputSchema: {
        format: z
          .enum(['iso', 'unix', 'locale'])
          .optional()
          .describe('Time format (default: iso)'),
      },
      outputSchema: {
        timestamp: z.string(),
        timezone: z.string(),
        format: z.string(),
      },
    },
    async ({ format = 'iso' }) => {
      const now = new Date();
      let timestamp: string;

      switch (format) {
        case 'unix':
          timestamp = Math.floor(now.getTime() / 1000).toString();
          break;
        case 'locale':
          timestamp = now.toLocaleString();
          break;
        case 'iso':
        default:
          timestamp = now.toISOString();
          break;
      }

      const output = {
        timestamp,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        format,
      };

      return {
        content: [{ type: 'text', text: JSON.stringify(output, null, 2) }],
        structuredContent: output,
      };
    }
  );
}
