import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { registerEchoTool } from './echo.tool.js';
import { registerCalculatorTools } from './calculator.tool.js';
import { registerTimeTool } from './time.tool.js';

/**
 * Register all tools with the MCP server
 *
 * Add your custom tools here by importing them and calling their register functions
 */
export function registerTools(server: McpServer) {
  registerEchoTool(server);
  registerCalculatorTools(server);
  registerTimeTool(server);

  console.error('✅ Registered tools: echo, add, multiply, calculate, get-time');
}
