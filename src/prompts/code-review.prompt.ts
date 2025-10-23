import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

/**
 * Code Review Prompt
 * Creates a prompt for code review and analysis
 */
export function registerCodeReviewPrompt(server: McpServer) {
  server.registerPrompt(
    'code-review',
    {
      title: 'Code Review',
      description: 'Generate a structured code review prompt',
      argsSchema: {
        code: z.string().describe('The code to review'),
        language: z.string().optional().describe('Programming language'),
        focus: z
          .string()
          .optional()
          .describe('Specific areas to focus on (e.g., performance, security)'),
      },
    },
    ({ code, language, focus }) => {
      let reviewText = `Please review the following code`;

      if (language) {
        reviewText += ` (${language})`;
      }

      reviewText += ':\n\n```\n' + code + '\n```\n\n';
      reviewText += 'Please analyze:\n';
      reviewText += '- Code quality and best practices\n';
      reviewText += '- Potential bugs or issues\n';
      reviewText += '- Performance considerations\n';
      reviewText += '- Security concerns\n';
      reviewText += '- Suggestions for improvement\n';

      if (focus) {
        reviewText += `\nPlease pay special attention to: ${focus}`;
      }

      return {
        messages: [
          {
            role: 'user' as const,
            content: {
              type: 'text' as const,
              text: reviewText,
            },
          },
        ],
      };
    }
  );
}
