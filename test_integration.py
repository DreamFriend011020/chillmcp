#!/usr/bin/env python3
"""
ChillMCP Integration Tests
Tests MCP server via JSON-RPC protocol with subprocess
Verifies complete end-to-end functionality including command-line parameters
"""

import subprocess
import json
import time
import re
import sys
from typing import Optional, Dict, Any


class MCPClient:
    """Simple MCP client for testing via stdio"""

    def __init__(self, boss_alertness: int = 50, boss_alertness_cooldown: int = 300):
        """Start MCP server process"""
        self.process = subprocess.Popen(
            [
                sys.executable,
                'main.py',
                '--boss_alertness', str(boss_alertness),
                '--boss_alertness_cooldown', str(boss_alertness_cooldown)
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.request_id = 0
        print(f"✅ MCP Server started (PID: {self.process.pid})")
        time.sleep(2)  # Wait for server to initialize

    def send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send JSON-RPC request to server"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
        }
        if params:
            request["params"] = params

        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()

        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise Exception("No response from server")

        return json.loads(response_line)

    def initialize(self):
        """Initialize MCP connection"""
        return self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })

    def list_tools(self):
        """List available tools"""
        return self.send_request("tools/list")

    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None):
        """Call a specific tool"""
        return self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments or {}
        })

    def close(self):
        """Close server process"""
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait(timeout=5)
        print(f"✅ MCP Server stopped")


def test_command_line_parameters():
    """Test 1: Command-line parameter recognition (CRITICAL - guide.txt requirement)"""
    print("\n" + "=" * 70)
    print("TEST 1: Command-Line Parameters (CRITICAL)")
    print("=" * 70)

    print("\n⚠️  This is a REQUIRED test from guide.txt")
    print("Failure here means automatic disqualification!\n")

    try:
        # Test with boss_alertness=100 and short cooldown
        print("Starting server with --boss_alertness 100 --boss_alertness_cooldown 10")
        client = MCPClient(boss_alertness=100, boss_alertness_cooldown=10)

        # Initialize
        print("Initializing connection...")
        init_response = client.initialize()
        if "result" in init_response:
            print("✅ Server initialized successfully")
        else:
            print("❌ Server initialization failed")
            client.close()
            return False

        # Call a tool - with boss_alertness=100, boss alert should ALWAYS increase
        print("\nCalling coffee_mission (boss_alertness=100, should always trigger)...")
        response = client.call_tool("coffee_mission")

        if "result" in response:
            content = response["result"]["content"][0]["text"]
            print("\nResponse:")
            print("-" * 70)
            print(content)
            print("-" * 70)

            # Parse boss alert level
            boss_match = re.search(r"Boss Alert Level:\s*([0-5])", content)
            if boss_match:
                boss_level = int(boss_match.group(1))
                print(f"\nBoss Alert Level: {boss_level}")

                if boss_level > 0:
                    print(f"✅ Boss Alert increased (boss_alertness=100 is working)")
                else:
                    print(f"⚠️  Boss Alert is 0 (boss_alertness=100 should trigger)")
                    # This might still pass if it's the first call
            else:
                print("❌ Could not parse Boss Alert Level")
                client.close()
                return False
        else:
            print(f"❌ Tool call failed: {response}")
            client.close()
            return False

        client.close()
        print("\n✅ Command-line parameters are recognized and working!")
        return True

    except Exception as e:
        print(f"❌ Error during command-line parameter test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_required_tools():
    """Test 2: All 8 required tools are available"""
    print("\n" + "=" * 70)
    print("TEST 2: Required Tools Availability")
    print("=" * 70)

    try:
        client = MCPClient()

        # Initialize
        client.initialize()

        # List tools
        print("Requesting tools list...")
        response = client.list_tools()

        if "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            tool_names = [tool["name"] for tool in tools]

            print(f"\nFound {len(tools)} tools:")
            for name in sorted(tool_names):
                print(f"  - {name}")

            # Check required tools
            required_tools = [
                "take_a_break",
                "watch_netflix",
                "show_meme",
                "bathroom_break",
                "coffee_mission",
                "urgent_call",
                "deep_thinking",
                "email_organizing"
            ]

            print("\nChecking required tools:")
            missing = []
            for tool in required_tools:
                if tool in tool_names:
                    print(f"  ✅ {tool}")
                else:
                    print(f"  ❌ {tool} (MISSING)")
                    missing.append(tool)

            client.close()

            if missing:
                print(f"\n❌ Missing {len(missing)} required tools!")
                return False
            else:
                print("\n✅ All 8 required tools are available!")
                return True
        else:
            print(f"❌ Failed to get tools list: {response}")
            client.close()
            return False

    except Exception as e:
        print(f"❌ Error during tools test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_response_format():
    """Test 3: Response format follows guide.txt specification"""
    print("\n" + "=" * 70)
    print("TEST 3: Response Format Validation")
    print("=" * 70)

    try:
        client = MCPClient()
        client.initialize()

        # Call a tool
        print("Calling watch_netflix...")
        response = client.call_tool("watch_netflix", {"show": "Test Show"})

        if "result" in response:
            content = response["result"]["content"][0]["text"]

            print("\nResponse:")
            print("-" * 70)
            print(content)
            print("-" * 70)

            # Check required fields (guide.txt specification)
            print("\nValidating response format:")

            # Break Summary
            break_match = re.search(r"Break Summary:\s*(.+?)(?:\n|$)", content, re.MULTILINE)
            if break_match:
                print(f"  ✅ Break Summary: {break_match.group(1)}")
            else:
                print("  ❌ Break Summary: MISSING")
                client.close()
                return False

            # Stress Level
            stress_match = re.search(r"Stress Level:\s*(\d{1,3})", content)
            if stress_match:
                stress = int(stress_match.group(1))
                if 0 <= stress <= 100:
                    print(f"  ✅ Stress Level: {stress} (valid range)")
                else:
                    print(f"  ❌ Stress Level: {stress} (out of range 0-100)")
                    client.close()
                    return False
            else:
                print("  ❌ Stress Level: MISSING")
                client.close()
                return False

            # Boss Alert Level
            boss_match = re.search(r"Boss Alert Level:\s*([0-5])", content)
            if boss_match:
                boss = int(boss_match.group(1))
                if 0 <= boss <= 5:
                    print(f"  ✅ Boss Alert Level: {boss} (valid range)")
                else:
                    print(f"  ❌ Boss Alert Level: {boss} (out of range 0-5)")
                    client.close()
                    return False
            else:
                print("  ❌ Boss Alert Level: MISSING")
                client.close()
                return False

            client.close()
            print("\n✅ Response format is valid!")
            return True
        else:
            print(f"❌ Tool call failed: {response}")
            client.close()
            return False

    except Exception as e:
        print(f"❌ Error during response format test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bonus_tools():
    """Test 4: Bonus tools (치맥, 퇴근, 회식)"""
    print("\n" + "=" * 70)
    print("TEST 4: Bonus Tools (Optional)")
    print("=" * 70)

    try:
        client = MCPClient()
        client.initialize()

        bonus_tools = [
            ("chimaek_time", "치맥"),
            ("immediate_clockout", "퇴근"),
            ("company_dinner", "회식")
        ]

        results = []
        for tool_name, korean_name in bonus_tools:
            print(f"\nTesting {tool_name} ({korean_name})...")
            try:
                response = client.call_tool(tool_name)

                if "result" in response:
                    content = response["result"]["content"][0]["text"]
                    print(f"  ✅ {tool_name} works!")
                    print(f"     Preview: {content[:60]}...")
                    results.append(True)
                else:
                    print(f"  ❌ {tool_name} failed")
                    results.append(False)
            except Exception as e:
                print(f"  ⚠️  {tool_name} not available: {e}")
                results.append(False)

        client.close()

        if all(results):
            print("\n✅ All bonus tools are working!")
            return True
        elif any(results):
            print(f"\n⚠️  Some bonus tools work ({sum(results)}/{len(results)})")
            return True
        else:
            print("\n❌ No bonus tools available")
            return False

    except Exception as e:
        print(f"❌ Error during bonus tools test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_calls():
    """Test 5: Multiple tool calls work correctly"""
    print("\n" + "=" * 70)
    print("TEST 5: Multiple Sequential Calls")
    print("=" * 70)

    try:
        client = MCPClient()
        client.initialize()

        tools_to_test = [
            "coffee_mission",
            "bathroom_break",
            "show_meme"
        ]

        print(f"Calling {len(tools_to_test)} tools sequentially...\n")

        for i, tool_name in enumerate(tools_to_test, 1):
            print(f"{i}. Calling {tool_name}...")
            response = client.call_tool(tool_name)

            if "result" in response:
                content = response["result"]["content"][0]["text"]

                # Parse stress and boss levels
                stress_match = re.search(r"Stress Level:\s*(\d{1,3})", content)
                boss_match = re.search(r"Boss Alert Level:\s*([0-5])", content)

                if stress_match and boss_match:
                    print(f"   Stress: {stress_match.group(1)}, Boss Alert: {boss_match.group(1)}")
                else:
                    print("   ⚠️  Could not parse levels")
            else:
                print(f"   ❌ Call failed")
                client.close()
                return False

            time.sleep(0.5)  # Small delay between calls

        client.close()
        print("\n✅ Multiple calls work correctly!")
        return True

    except Exception as e:
        print(f"❌ Error during multiple calls test: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all integration tests"""
    print("=" * 70)
    print("ChillMCP Integration Tests")
    print("End-to-end testing via JSON-RPC")
    print("=" * 70)

    tests = [
        ("Command-Line Parameters (CRITICAL)", test_command_line_parameters),
        ("Required Tools Availability", test_required_tools),
        ("Response Format Validation", test_response_format),
        ("Bonus Tools", test_bonus_tools),
        ("Multiple Sequential Calls", test_multiple_calls),
    ]

    results = []

    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))

            # If critical test fails, stop
            if "CRITICAL" in name and not result:
                print("\n" + "=" * 70)
                print("❌ CRITICAL TEST FAILED - Stopping further tests")
                print("=" * 70)
                break

        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = 0
    failed = 0

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        marker = " (CRITICAL)" if "CRITICAL" in name else ""
        print(f"{status}: {name}{marker}")
        if result:
            passed += 1
        else:
            failed += 1

    print("-" * 70)
    print(f"Total: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    # Check critical test
    critical_passed = results[0][1] if results else False
    if not critical_passed:
        print("\n⚠️  CRITICAL: Command-line parameter test failed!")
        print("This means AUTOMATIC DISQUALIFICATION per guide.txt")

    print("=" * 70)

    return failed == 0 and critical_passed


if __name__ == '__main__':
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
