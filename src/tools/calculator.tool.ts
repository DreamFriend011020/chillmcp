import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

/**
 * Calculator Tools
 * Basic arithmetic operations demonstrating tool implementation
 */

export function registerCalculatorTools(server: McpServer) {
  // Addition tool
  server.registerTool(
    'add',
    {
      title: 'Addition Tool',
      description: 'Add two numbers together',
      inputSchema: {
        a: z.number().describe('First number'),
        b: z.number().describe('Second number'),
      },
      outputSchema: {
        result: z.number(),
        operation: z.string(),
      },
    },
    async ({ a, b }) => {
      const output = {
        result: a + b,
        operation: `${a} + ${b} = ${a + b}`,
      };

      return {
        content: [{ type: 'text', text: JSON.stringify(output) }],
        structuredContent: output,
      };
    }
  );

  // Multiplication tool
  server.registerTool(
    'multiply',
    {
      title: 'Multiplication Tool',
      description: 'Multiply two numbers',
      inputSchema: {
        a: z.number().describe('First number'),
        b: z.number().describe('Second number'),
      },
      outputSchema: {
        result: z.number(),
        operation: z.string(),
      },
    },
    async ({ a, b }) => {
      const output = {
        result: a * b,
        operation: `${a} × ${b} = ${a * b}`,
      };

      return {
        content: [{ type: 'text', text: JSON.stringify(output) }],
        structuredContent: output,
      };
    }
  );

  // Calculate tool - supports multiple operations
  server.registerTool(
    'calculate',
    {
      title: 'Calculator',
      description: 'Perform arithmetic calculations (add, subtract, multiply, divide)',
      inputSchema: {
        a: z.number().describe('First number'),
        b: z.number().describe('Second number'),
        operation: z.enum(['add', 'subtract', 'multiply', 'divide']).describe('Operation to perform'),
      },
      outputSchema: {
        result: z.number(),
        operation: z.string(),
      },
    },
    async ({ a, b, operation }) => {
      let result: number;
      let operationSymbol: string;

      switch (operation) {
        case 'add':
          result = a + b;
          operationSymbol = '+';
          break;
        case 'subtract':
          result = a - b;
          operationSymbol = '-';
          break;
        case 'multiply':
          result = a * b;
          operationSymbol = '×';
          break;
        case 'divide':
          if (b === 0) {
            return {
              content: [{ type: 'text', text: 'Error: Division by zero' }],
              isError: true,
            };
          }
          result = a / b;
          operationSymbol = '÷';
          break;
      }

      const output = {
        result,
        operation: `${a} ${operationSymbol} ${b} = ${result}`,
      };

      return {
        content: [{ type: 'text', text: JSON.stringify(output) }],
        structuredContent: output,
      };
    }
  );
}
