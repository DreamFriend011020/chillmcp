import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { registerGreetingResource } from './greeting.resource.js';
import { registerInfoResource } from './info.resource.js';

/**
 * Register all resources with the MCP server
 *
 * Add your custom resources here by importing them and calling their register functions
 */
export function registerResources(server: McpServer) {
  registerGreetingResource(server);
  registerInfoResource(server);

  console.error('✅ Registered resources: greeting, server-info');
}
