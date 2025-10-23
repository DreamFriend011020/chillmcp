import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { registerAssistantPrompt } from './assistant.prompt.js';
import { registerCodeReviewPrompt } from './code-review.prompt.js';
import { registerExplainPrompt } from './explain.prompt.js';

/**
 * Register all prompts with the MCP server
 *
 * Add your custom prompts here by importing them and calling their register functions
 */
export function registerPrompts(server: McpServer) {
  registerAssistantPrompt(server);
  registerCodeReviewPrompt(server);
  registerExplainPrompt(server);

  console.error('✅ Registered prompts: assistant, code-review, explain');
}
