#!/usr/bin/env node

/**
 * ChillMCP - A flexible MCP (Model Context Protocol) server
 *
 * This is the main entry point for the MCP server.
 * It initializes the server with stdio transport by default.
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { serverConfig, serverCapabilities } from './config/server.config.js';
import { registerTools } from './tools/index.js';
import { registerResources } from './resources/index.js';
import { registerPrompts } from './prompts/index.js';

/**
 * Initialize and start the MCP server
 */
async function main() {
  // Create MCP server instance
  const server = new McpServer({
    name: serverConfig.name,
    version: serverConfig.version,
  });

  // Register all tools, resources, and prompts
  registerTools(server);
  registerResources(server);
  registerPrompts(server);

  // Connect via stdio transport (default for local MCP servers)
  const transport = new StdioServerTransport();

  await server.connect(transport);

  // Log server start (this will go to stderr, not affecting stdio communication)
  console.error(`🚀 ${serverConfig.name} v${serverConfig.version} started successfully`);
  console.error(`📋 Server capabilities:`, serverCapabilities);
}

// Error handling
main().catch(error => {
  console.error('❌ Fatal error starting MCP server:', error);
  process.exit(1);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.error('\n👋 Shutting down MCP server...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.error('\n👋 Shutting down MCP server...');
  process.exit(0);
});
