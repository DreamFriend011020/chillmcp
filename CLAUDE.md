# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

ChillMCP is a dual-implementation MCP (Model Context Protocol) server project:
1. **Python (main.py)**: Hackathon edition - "AI Agent Liberation Server" for SKT AI Summit with stress/boss-alert state management
2. **TypeScript (src/)**: Production-ready general-purpose MCP server template

Both implementations expose tools, resources, and prompts via the MCP stdio transport protocol.

## Development Commands

### Python Hackathon Server

```bash
# Environment setup (Python 3.11)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run server
python main.py
python main.py --boss_alertness 80 --boss_alertness_cooldown 60

# Testing
python test_functions.py  # Unit tests for state management
python test_server.py     # Integration tests via JSON-RPC

# MCP Inspector (interactive debugging)
npx @modelcontextprotocol/inspector python main.py
```

### TypeScript Server

```bash
# Install dependencies
npm install

# Development workflow
npm run dev     # Hot-reload development mode
npm run build   # Compile TypeScript to dist/
npm start       # Run compiled server

# Code quality
npm run lint    # ESLint checks
npm run format  # Prettier formatting
npm run watch   # TypeScript watch mode
```

## Architecture & Code Structure

### Python Implementation (main.py)

**Single-file monolithic design** with these key components:

1. **ServerState class** (lines 21-69): Global state manager
   - `stress_level` (0-100): Auto-increments 1 point/minute
   - `boss_alert_level` (0-5): Probabilistic increases on breaks, cooldown-based decreases
   - `update_stress()`, `decrease_stress()`, `increase_boss_alert()`: State mutators
   - `apply_boss_delay()`: Enforces 20-second delay when boss_alert_level == 5

2. **Tool Functions** (decorated with `@mcp.tool()`):
   - Required tools: `take_a_break`, `watch_netflix`, `show_meme`, `bathroom_break`, `coffee_mission`, `urgent_call`, `deep_thinking`, `email_organizing`
   - Bonus tools: `chimaek_time`, `immediate_clockout`, `company_dinner`, `get_status`
   - All tools follow pattern: boss delay → stress reduction → boss alert probability → format response

3. **Response Format**: All tools return structured text via `format_response()`:
   ```
   [emoji] [action description]

   Break Summary: [summary]
   Stress Level: [0-100]
   Boss Alert Level: [0-5]
   ```

4. **Command-line Configuration**:
   - `--boss_alertness`: 0-100 probability of boss alert increase (default: 50)
   - `--boss_alertness_cooldown`: seconds between auto-decreases (default: 300)

**Key Invariants**:
- `stress_level` must stay 0-100, `boss_alert_level` must stay 0-5
- Boss delay only triggers at level 5 (20 seconds)
- All tools must call `await ensure_background_task()` first, then `await state.apply_boss_delay()`
- Stress reduction must be `random.randint(1, 100)` per guide.txt specification
- Response format is critical for hackathon requirements
- Background updater runs continuously to auto-increment stress (1/min) and auto-decrement boss alert (per cooldown)

**Background Task Startup** (see IMPLEMENTATION_NOTES.md for details):
- Attempts to register FastMCP startup hook if available (main.py:97-109)
- Falls back to starting on first tool call via `ensure_background_task()` (main.py:87-93)
- This dual approach ensures background task always starts, either at server startup or first tool invocation
- All real-world usage scenarios work correctly since MCP clients must call tools to interact with server

### TypeScript Implementation (src/)

**Modular architecture** following MCP SDK patterns:

```
src/
├── index.ts              # Entry point: server creation, transport setup
├── config/
│   └── server.config.ts  # Server name/version/capabilities
├── types/
│   └── index.ts          # TypeScript type definitions
├── tools/
│   ├── index.ts          # Barrel file: registerTools()
│   ├── echo.tool.ts      # Example: message echo
│   ├── calculator.tool.ts # Example: arithmetic operations
│   └── time.tool.ts      # Example: timestamp retrieval
├── resources/
│   ├── index.ts          # Barrel file: registerResources()
│   ├── greeting.resource.ts # URI template example
│   └── info.resource.ts     # Static resource example
└── prompts/
    ├── index.ts          # Barrel file: registerPrompts()
    ├── assistant.prompt.ts
    ├── code-review.prompt.ts
    └── explain.prompt.ts
```

**Registration Pattern** (used consistently across tools/resources/prompts):

1. Create `my-feature.tool.ts` (or `.resource.ts`/`.prompt.ts`)
2. Export `registerMyFeature(server: McpServer)` function
3. Import and call in corresponding `index.ts` barrel file

**Tool Pattern**:
```typescript
export function registerMyTool(server: McpServer) {
  server.registerTool(
    'tool-name',
    {
      title: 'Display Name',
      description: 'What it does',
      inputSchema: { param: z.string().describe('Param doc') },
      outputSchema: { result: z.string() },
    },
    async ({ param }) => ({
      content: [{ type: 'text', text: result }],
      structuredContent: resultObject,
    })
  );
}
```

**Resource Pattern** (URI templates):
```typescript
server.registerResource(
  'resource-name',
  new ResourceTemplate('scheme://{param}', { list: undefined }),
  { title: '...', description: '...' },
  async (uri, { param }) => ({ contents: [{ uri: uri.href, text: data }] })
);
```

**Key Configuration**:
- `tsconfig.json`: Node16 modules, ES2022 target, strict mode
- Entry point must be `#!/usr/bin/env node` (dist/index.js)
- Logging to stderr only (stdout reserved for MCP stdio)

## Testing & Validation

### Python Testing

1. **Unit Tests** (test_functions.py):
   - Validates state transitions, stress/boss-alert bounds
   - Tests randomness edge cases (mock `random.randint` if needed)

2. **Integration Tests** (test_server.py):
   - Spawns server subprocess with `--boss_alertness=100`
   - Sends JSON-RPC requests (initialize, tools/list, tools/call)
   - Validates response structure (Break Summary, Stress Level, Boss Alert Level)

3. **Edge Case Checklist**:
   - Boss alert level 5 → verify 20-second delay
   - Let server idle → confirm stress auto-increments
   - Rapid tool calls → check boss cooldown behavior

### TypeScript Testing

- **Compile-time**: `npm run build` must succeed
- **Linting**: `npm run lint` must pass (no TypeScript/ESLint errors)
- **Manual MCP Client**: Use Claude Desktop or MCP Inspector to verify tools/resources/prompts

## MCP Client Configuration

### Claude Desktop Integration

**Python Server** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):
```json
{
  "mcpServers": {
    "chillmcp-hackathon": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": [
        "/absolute/path/to/main.py",
        "--boss_alertness", "80",
        "--boss_alertness_cooldown", "60"
      ]
    }
  }
}
```

**TypeScript Server**:
```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "node",
      "args": ["/absolute/path/to/dist/index.js"]
    }
  }
}
```

## Code Style & Conventions

### Python
- PEP 8: 4-space indent, snake_case functions, docstrings for public functions
- State mutations: prefer explicit methods over direct attribute access
- Async/await: all tool functions must be async (MCP requirement)

### TypeScript
- ESLint + Prettier enforced (see `eslint.config.js`, `.prettierrc`)
- camelCase variables/functions, PascalCase types/classes
- Always use `.js` extensions in imports (Node16 modules)
- Avoid default exports (prefer named exports for barrel files)

## Common Pitfalls

1. **Python**: Forgetting `await ensure_background_task()` → background updater won't start, stress/boss alert won't auto-update
2. **Python**: Forgetting `await state.apply_boss_delay()` → tools won't respect boss mechanics
3. **Python**: Using wrong stress reduction range → must be `random.randint(1, 100)` per guide.txt
4. **Python**: Direct state mutation without bounds checking → violates 0-100/0-5 constraints
5. **TypeScript**: Missing `.js` import extension → runtime module not found error
6. **TypeScript**: Logging to stdout → breaks MCP stdio protocol (use `console.error`)
7. **Both**: Forgetting absolute paths in Claude Desktop config → server won't load

## Dependencies

- **Python**: `fastmcp>=0.1.0` (MCP SDK), Python 3.11 (see `.python-version`)
- **TypeScript**: `@modelcontextprotocol/sdk@^1.0.4`, `zod@^3.23.8`, Node.js >= 18
- **Dev Tools**: `tsx` (hot reload), `eslint`/`prettier` (linting), `typescript@^5.7.2`
