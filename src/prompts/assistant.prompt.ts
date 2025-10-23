import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

/**
 * Assistant Prompt
 * Creates a prompt for an AI assistant to help with a task
 */
export function registerAssistantPrompt(server: McpServer) {
  server.registerPrompt(
    'assistant',
    {
      title: 'AI Assistant',
      description: 'Create a prompt for an AI assistant to help with a specific task',
      argsSchema: {
        task: z.string().describe('The task you need help with'),
        context: z.string().optional().describe('Additional context or information'),
      },
    },
    ({ task, context }) => {
      const messages = [
        {
          role: 'user' as const,
          content: {
            type: 'text' as const,
            text: context
              ? `I need help with the following task: ${task}\n\nAdditional context: ${context}`
              : `I need help with the following task: ${task}`,
          },
        },
      ];

      return { messages };
    }
  );
}
