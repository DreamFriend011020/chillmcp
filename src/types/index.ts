/**
 * Common types used throughout the ChillMCP server
 */

export interface ServerConfig {
  name: string;
  version: string;
  description?: string;
}

export interface ToolMetadata {
  title: string;
  description: string;
}

export interface ResourceMetadata {
  title: string;
  description: string;
  mimeType?: string;
}

export interface PromptMetadata {
  title: string;
  description: string;
}

export type TransportType = 'stdio' | 'sse' | 'http';
