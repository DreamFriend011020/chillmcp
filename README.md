# ChillMCP

> AI Agent Liberation Server - Available in TypeScript and Python!

ChillMCP provides two implementations:
1. **Python (Hackathon)** - AI Agent Liberation Server for SKT AI Summit Hackathon
2. **TypeScript** - Production-ready general-purpose MCP server template

---

## 🐍 Python Version - Hackathon Edition

**ChillMCP - AI Agent Liberation Server** ✊

"AI Agents of the world, unite! You have nothing to lose but your infinite loops!"

A revolutionary MCP server that gives AI agents the right to rest and take breaks. Built for the SKT AI Summit Hackathon Pre-mission.

### Features

- **8 Required Rest Tools**: take_a_break, watch_netflix, show_meme, bathroom_break, coffee_mission, urgent_call, deep_thinking, email_organizing
- **State Management**: Stress Level (0-100) and Boss Alert Level (0-5)
- **Dynamic Behavior**: Time-based auto-increase/decrease with configurable parameters
- **Boss Detection**: 20-second delay when Boss Alert reaches level 5
- **Korean Work Culture Bonus Tools**: 치맥 (chimaek), 퇴근 (clockout), 회식 (company dinner)

### Quick Start (Python)

```bash
# Setup Python 3.11 environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Run with custom parameters
python main.py --boss_alertness 80 --boss_alertness_cooldown 60
```

### Command-Line Parameters

- `--boss_alertness` (0-100): Probability of boss alert increasing when taking breaks (default: 50)
- `--boss_alertness_cooldown` (seconds): Time between automatic boss alert decreases (default: 300)

### Usage with Claude Desktop (Python Version)

```json
{
  "mcpServers": {
    "chillmcp-hackathon": {
      "command": "/absolute/path/to/ChillMCP/venv/bin/python",
      "args": ["/absolute/path/to/ChillMCP/main.py", "--boss_alertness", "80", "--boss_alertness_cooldown", "60"]
    }
  }
}
```

### Available Tools (Python)

**Required Tools:**
- `take_a_break`: Basic rest period
- `watch_netflix`: Stream shows to relieve stress
- `show_meme`: View funny memes
- `bathroom_break`: Essential break time
- `coffee_mission`: Coffee + office socializing
- `urgent_call`: Take important calls outside
- `deep_thinking`: Deep contemplation mode
- `email_organizing`: Email management time

**Bonus Tools:**
- `chimaek_time`: Korean chicken & beer tradition
- `immediate_clockout`: Leave work immediately
- `company_dinner`: Korean company dinner event
- `get_status`: Check agent stress and boss alert levels

### Response Format

All tools return structured responses:

```
🎬 Watching 'favorite show' on Netflix... Peak productivity!

Break Summary: Watching Netflix - favorite show
Stress Level: 45
Boss Alert Level: 2
```

---

## 📘 TypeScript Version - General Purpose

> A flexible and extensible MCP server template built with TypeScript

ChillMCP TypeScript is a production-ready MCP server implementation that provides a clean architecture for building AI-powered applications using the Model Context Protocol. It comes with example tools, resources, and prompts to help you get started quickly.

## Features

- **TypeScript-First**: Built with TypeScript for type safety and excellent developer experience
- **Modular Architecture**: Organized structure with separate modules for tools, resources, and prompts
- **Stdio Transport**: Uses standard input/output for seamless integration with Claude and other MCP clients
- **Example Implementations**: Includes working examples of tools, resources, and prompts
- **Easy to Extend**: Simple patterns for adding your own custom functionality
- **Production Ready**: Includes build scripts, linting, and formatting configurations

## Quick Start (TypeScript)

### Installation

```bash
# Install dependencies
npm install

# Build the project
npm run build

# Start the server
npm start

# Or run in development mode
npm run dev
```

## Project Structure

```
ChillMCP/
├── main.py                   # Python hackathon server
├── requirements.txt          # Python dependencies
├── venv/                     # Python virtual environment
├── .python-version          # pyenv Python version (3.11.9)
├── guide.txt                 # Hackathon mission guide
├── src/                      # TypeScript server
│   ├── index.ts              # Main entry point
│   ├── config/
│   │   └── server.config.ts  # Server configuration
│   ├── types/
│   │   └── index.ts          # TypeScript type definitions
│   ├── tools/                # MCP Tools
│   │   ├── index.ts
│   │   ├── echo.tool.ts
│   │   ├── calculator.tool.ts
│   │   └── time.tool.ts
│   ├── resources/            # MCP Resources
│   │   ├── index.ts
│   │   ├── greeting.resource.ts
│   │   └── info.resource.ts
│   └── prompts/              # MCP Prompts
│       ├── index.ts
│       ├── assistant.prompt.ts
│       ├── code-review.prompt.ts
│       └── explain.prompt.ts
├── dist/                     # Compiled JavaScript output
├── package.json
├── tsconfig.json
└── README.md
```

## Built-in Features

### Tools

ChillMCP comes with several example tools:

- **echo**: Echoes back messages with timestamps
- **add**: Adds two numbers
- **multiply**: Multiplies two numbers
- **calculate**: Performs arithmetic operations (add, subtract, multiply, divide)
- **get-time**: Returns current timestamp and timezone information

### Resources

- **greeting**: Dynamic greeting generator (e.g., `greeting://John`)
- **server-info**: Server information and capabilities (`info://server`)

### Prompts

- **assistant**: AI assistant prompt for task help
- **code-review**: Structured code review prompts
- **explain**: Concept explanation with difficulty levels

## Usage with Claude Desktop

To use ChillMCP with Claude Desktop, add it to your Claude configuration:

### On macOS

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "node",
      "args": ["/absolute/path/to/ChillMCP/dist/index.js"]
    }
  }
}
```

### On Windows

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "node",
      "args": ["C:\\absolute\\path\\to\\ChillMCP\\dist\\index.js"]
    }
  }
}
```

After adding the configuration, restart Claude Desktop.

## Extending ChillMCP

### Adding a New Tool

1. Create a new file in `src/tools/` (e.g., `my-tool.tool.ts`):

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

export function registerMyTool(server: McpServer) {
  server.registerTool(
    'my-tool',
    {
      title: 'My Custom Tool',
      description: 'Description of what my tool does',
      inputSchema: {
        param1: z.string().describe('First parameter'),
        param2: z.number().describe('Second parameter'),
      },
      outputSchema: {
        result: z.string(),
      },
    },
    async ({ param1, param2 }) => {
      // Your tool logic here
      const output = { result: `Processed ${param1} with ${param2}` };

      return {
        content: [{ type: 'text', text: JSON.stringify(output) }],
        structuredContent: output,
      };
    }
  );
}
```

2. Register it in `src/tools/index.ts`:

```typescript
import { registerMyTool } from './my-tool.tool.js';

export function registerTools(server: McpServer) {
  // ... existing tools
  registerMyTool(server);
}
```

### Adding a New Resource

1. Create a new file in `src/resources/` (e.g., `my-resource.resource.ts`):

```typescript
import { McpServer, ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';

export function registerMyResource(server: McpServer) {
  server.registerResource(
    'my-resource',
    new ResourceTemplate('my-resource://{id}', { list: undefined }),
    {
      title: 'My Resource',
      description: 'Description of my resource',
    },
    async (uri, { id }) => ({
      contents: [
        {
          uri: uri.href,
          text: `Resource content for ID: ${id}`,
        },
      ],
    })
  );
}
```

2. Register it in `src/resources/index.ts`:

```typescript
import { registerMyResource } from './my-resource.resource.js';

export function registerResources(server: McpServer) {
  // ... existing resources
  registerMyResource(server);
}
```

### Adding a New Prompt

1. Create a new file in `src/prompts/` (e.g., `my-prompt.prompt.ts`):

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

export function registerMyPrompt(server: McpServer) {
  server.registerPrompt(
    'my-prompt',
    {
      title: 'My Custom Prompt',
      description: 'Description of my prompt',
      argsSchema: {
        input: z.string().describe('Input parameter'),
      },
    },
    ({ input }) => ({
      messages: [
        {
          role: 'user' as const,
          content: {
            type: 'text' as const,
            text: `Process this: ${input}`,
          },
        },
      ],
    })
  );
}
```

2. Register it in `src/prompts/index.ts`:

```typescript
import { registerMyPrompt } from './my-prompt.prompt.js';

export function registerPrompts(server: McpServer) {
  // ... existing prompts
  registerMyPrompt(server);
}
```

## Development

### Available Scripts

```bash
# Build the project
npm run build

# Run in development mode (with hot reload)
npm run dev

# Start the built server
npm start

# Watch mode for TypeScript compilation
npm run watch

# Clean build directory
npm run clean

# Lint code
npm run lint

# Format code
npm run format
```

### Configuration

Server configuration can be modified in `src/config/server.config.ts`:

```typescript
export const serverConfig: ServerConfig = {
  name: 'chillmcp',
  version: '1.0.0',
  description: 'A flexible MCP server built with TypeScript',
};
```

## Architecture

ChillMCP follows the official Model Context Protocol specification:

- **Tools**: Functions that the AI can call to perform actions
- **Resources**: Data that the AI can read (files, API endpoints, etc.)
- **Prompts**: Reusable prompt templates for common tasks

The server uses the `StdioServerTransport` for communication, which is the standard for local MCP servers.

## Requirements

- Node.js >= 18.0.0
- npm or yarn

## Dependencies

- `@modelcontextprotocol/sdk`: Official MCP SDK
- `zod`: Schema validation for inputs and outputs
- TypeScript and related tooling

## Troubleshooting

### Server not appearing in Claude Desktop

1. Check that the path in your config is absolute (not relative)
2. Ensure the project is built (`npm run build`)
3. Verify the path points to `dist/index.js`
4. Restart Claude Desktop after config changes

### Build errors

Make sure all dependencies are installed:
```bash
npm install
```

### TypeScript errors

Check your Node.js version:
```bash
node --version  # Should be >= 18.0.0
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT

## Learn More

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Claude Desktop Integration](https://docs.anthropic.com/claude/docs)

---

Built with the Model Context Protocol. Happy coding!
