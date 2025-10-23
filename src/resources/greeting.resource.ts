import { McpServer, ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';

/**
 * Greeting Resource
 * Dynamic greeting generator using URI templates
 */
export function registerGreetingResource(server: McpServer) {
  server.registerResource(
    'greeting',
    new ResourceTemplate('greeting://{name}', { list: undefined }),
    {
      title: 'Greeting Resource',
      description: 'Generate personalized greetings',
    },
    async (uri, { name }) => ({
      contents: [
        {
          uri: uri.href,
          text: `Hello, ${name}! Welcome to ChillMCP.`,
        },
      ],
    })
  );
}
