import { ServerConfig } from '../types/index.js';

/**
 * Default server configuration
 * Customize these values for your specific MCP server implementation
 */
export const serverConfig: ServerConfig = {
  name: 'chillmcp',
  version: '1.0.0',
  description: 'A flexible MCP server built with TypeScript',
};

/**
 * Server capabilities configuration
 */
export const serverCapabilities = {
  tools: {},
  resources: {},
  prompts: {},
};
