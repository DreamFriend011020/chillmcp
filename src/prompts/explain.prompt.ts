import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

/**
 * Explain Prompt
 * Creates a prompt to explain a concept or code
 */
export function registerExplainPrompt(server: McpServer) {
  server.registerPrompt(
    'explain',
    {
      title: 'Explain Concept',
      description: 'Generate a prompt to explain a concept, code, or topic',
      argsSchema: {
        topic: z.string().describe('What to explain'),
        level: z
          .enum(['beginner', 'intermediate', 'advanced'])
          .optional()
          .describe('Explanation level'),
      },
    },
    ({ topic, level = 'intermediate' }) => {
      let promptText = `Please explain ${topic}`;

      if (level === 'beginner') {
        promptText += ' in simple terms for beginners';
      } else if (level === 'advanced') {
        promptText += ' with technical depth for advanced users';
      }

      promptText += '. Please include practical examples to illustrate the concepts.';

      return {
        messages: [
          {
            role: 'user' as const,
            content: {
              type: 'text' as const,
              text: promptText,
            },
          },
        ],
      };
    }
  );
}
