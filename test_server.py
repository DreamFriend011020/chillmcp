#!/usr/bin/env python3
"""
Simple test script for ChillMCP server
Tests the tools and verifies response format
"""

import subprocess
import json
import time

def test_mcp_server():
    """Test ChillMCP server with JSON-RPC calls"""

    print("🧪 Testing ChillMCP Server\n")
    print("=" * 60)

    # Start the server
    server = subprocess.Popen(
        ["python", "main.py", "--boss_alertness", "100", "--boss_alertness_cooldown", "5"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Wait for server to start
    time.sleep(2)

    try:
        print("\n1️⃣ Test: Initialize")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        server.stdin.write(json.dumps(init_request) + "\n")
        server.stdin.flush()

        # Read response
        response = server.stdout.readline()
        if response:
            print(f"✅ Initialize response received")
            print(f"   {response[:100]}...")

        time.sleep(1)

        print("\n2️⃣ Test: List Tools")
        list_tools = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }

        server.stdin.write(json.dumps(list_tools) + "\n")
        server.stdin.flush()

        response = server.stdout.readline()
        if response:
            resp_data = json.loads(response)
            if "result" in resp_data and "tools" in resp_data["result"]:
                tools = resp_data["result"]["tools"]
                print(f"✅ Found {len(tools)} tools:")
                for tool in tools[:5]:  # Show first 5
                    print(f"   - {tool.get('name', 'unknown')}: {tool.get('description', '')[:50]}...")
            else:
                print(f"   Response: {response[:200]}")

        time.sleep(1)

        print("\n3️⃣ Test: Call 'take_a_break' tool")
        call_tool = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "take_a_break",
                "arguments": {
                    "duration": 5
                }
            }
        }

        server.stdin.write(json.dumps(call_tool) + "\n")
        server.stdin.flush()

        response = server.stdout.readline()
        if response:
            resp_data = json.loads(response)
            if "result" in resp_data:
                result = resp_data["result"]
                if "content" in result and len(result["content"]) > 0:
                    text = result["content"][0].get("text", "")
                    print(f"✅ Tool executed successfully:")
                    print(f"\n{text}\n")

                    # Validate response format
                    if "Break Summary:" in text and "Stress Level:" in text and "Boss Alert Level:" in text:
                        print("✅ Response format is correct!")
                    else:
                        print("⚠️  Response format might be incorrect")
                else:
                    print(f"   Result: {result}")
            else:
                print(f"   Response: {response[:300]}")

        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")

    except Exception as e:
        print(f"\n❌ Error during test: {e}")

    finally:
        # Clean up
        server.terminate()
        try:
            server.wait(timeout=3)
        except:
            server.kill()

if __name__ == "__main__":
    test_mcp_server()
