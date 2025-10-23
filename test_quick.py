#!/usr/bin/env python3
"""
ChillMCP Quick Tests
Fast tests that can be executed immediately without time delays
Tests response parsing, tool availability, and basic functionality
"""

import re
import sys


def test_response_parsing():
    """Test 1: Response parsing with regex (guide.txt requirement)"""
    print("\n" + "=" * 70)
    print("TEST 1: Response Parsing")
    print("=" * 70)

    # Sample response from a tool
    sample_response = """🎬 Watching 'favorite show' on Netflix... Peak productivity!

Break Summary: Watching Netflix - favorite show
Stress Level: 45
Boss Alert Level: 2"""

    # Regex patterns from guide.txt
    break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
    stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
    boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"

    # Test Break Summary extraction
    break_match = re.search(break_summary_pattern, sample_response, re.MULTILINE)
    if break_match:
        print(f"✅ Break Summary found: {break_match.group(1)}")
    else:
        print("❌ Break Summary NOT found")
        return False

    # Test Stress Level extraction
    stress_match = re.search(stress_level_pattern, sample_response)
    if stress_match:
        stress_val = int(stress_match.group(1))
        if 0 <= stress_val <= 100:
            print(f"✅ Stress Level found and valid: {stress_val}")
        else:
            print(f"❌ Stress Level out of range: {stress_val}")
            return False
    else:
        print("❌ Stress Level NOT found")
        return False

    # Test Boss Alert Level extraction
    boss_match = re.search(boss_alert_pattern, sample_response)
    if boss_match:
        boss_val = int(boss_match.group(1))
        if 0 <= boss_val <= 5:
            print(f"✅ Boss Alert Level found and valid: {boss_val}")
        else:
            print(f"❌ Boss Alert Level out of range: {boss_val}")
            return False
    else:
        print("❌ Boss Alert Level NOT found")
        return False

    print("✅ All parsing tests passed!")
    return True


def test_tool_definitions():
    """Test 2: Verify all required tools are defined"""
    print("\n" + "=" * 70)
    print("TEST 2: Tool Definitions")
    print("=" * 70)

    try:
        from main import (
            take_a_break,
            watch_netflix,
            show_meme,
            bathroom_break,
            coffee_mission,
            urgent_call,
            deep_thinking,
            email_organizing,
            # Bonus tools
            chimaek_time,
            immediate_clockout,
            company_dinner,
            get_status
        )

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

        bonus_tools = [
            "chimaek_time",
            "immediate_clockout",
            "company_dinner"
        ]

        print("\nRequired Tools (8):")
        for tool in required_tools:
            print(f"  ✅ {tool}")

        print("\nBonus Tools (3):")
        for tool in bonus_tools:
            print(f"  ✅ {tool}")

        print("\nUtility Tools:")
        print(f"  ✅ get_status")

        print(f"\n✅ All {len(required_tools) + len(bonus_tools) + 1} tools are defined!")
        return True

    except ImportError as e:
        print(f"❌ Failed to import tools: {e}")
        return False


def test_state_class():
    """Test 3: Verify ServerState class structure"""
    print("\n" + "=" * 70)
    print("TEST 3: ServerState Class")
    print("=" * 70)

    try:
        from main import ServerState

        state = ServerState()

        # Check required attributes
        required_attrs = [
            'stress_level',
            'boss_alert_level',
            'last_stress_update',
            'last_boss_cooldown',
            'boss_alertness',
            'boss_alertness_cooldown'
        ]

        print("\nChecking attributes:")
        for attr in required_attrs:
            if hasattr(state, attr):
                value = getattr(state, attr)
                print(f"  ✅ {attr}: {value}")
            else:
                print(f"  ❌ {attr}: MISSING")
                return False

        # Check required methods
        required_methods = [
            'update_stress',
            'decrease_stress',
            'increase_boss_alert',
            'update_boss_cooldown',
            'apply_boss_delay'
        ]

        print("\nChecking methods:")
        for method in required_methods:
            if hasattr(state, method):
                print(f"  ✅ {method}()")
            else:
                print(f"  ❌ {method}(): MISSING")
                return False

        # Check initial values
        print("\nChecking initial state:")
        if 0 <= state.stress_level <= 100:
            print(f"  ✅ Initial stress_level: {state.stress_level} (valid range)")
        else:
            print(f"  ❌ Initial stress_level: {state.stress_level} (out of range)")
            return False

        if 0 <= state.boss_alert_level <= 5:
            print(f"  ✅ Initial boss_alert_level: {state.boss_alert_level} (valid range)")
        else:
            print(f"  ❌ Initial boss_alert_level: {state.boss_alert_level} (out of range)")
            return False

        print("\n✅ ServerState class structure is correct!")
        return True

    except ImportError as e:
        print(f"❌ Failed to import ServerState: {e}")
        return False


def test_format_response():
    """Test 4: Verify response formatting function"""
    print("\n" + "=" * 70)
    print("TEST 4: Response Formatting")
    print("=" * 70)

    try:
        from main import format_response, state

        # Set known state
        state.stress_level = 42
        state.boss_alert_level = 3

        response = format_response("Test summary", "🧪")

        print("\nGenerated response:")
        print("-" * 70)
        print(response)
        print("-" * 70)

        # Verify format
        if "Break Summary:" in response:
            print("✅ Contains 'Break Summary:'")
        else:
            print("❌ Missing 'Break Summary:'")
            return False

        if "Stress Level:" in response:
            print("✅ Contains 'Stress Level:'")
        else:
            print("❌ Missing 'Stress Level:'")
            return False

        if "Boss Alert Level:" in response:
            print("✅ Contains 'Boss Alert Level:'")
        else:
            print("❌ Missing 'Boss Alert Level:'")
            return False

        # Verify values are parseable
        stress_match = re.search(r"Stress Level:\s*(\d{1,3})", response)
        boss_match = re.search(r"Boss Alert Level:\s*([0-5])", response)

        if stress_match and boss_match:
            print(f"✅ Values are parseable: Stress={stress_match.group(1)}, Boss Alert={boss_match.group(1)}")
        else:
            print("❌ Values are not parseable")
            return False

        print("\n✅ Response formatting is correct!")
        return True

    except Exception as e:
        print(f"❌ Error testing format_response: {e}")
        return False


def test_command_line_args():
    """Test 5: Verify command-line argument parsing"""
    print("\n" + "=" * 70)
    print("TEST 5: Command-Line Arguments")
    print("=" * 70)

    try:
        import argparse
        from main import main

        print("\nChecking argparse setup in main()...")

        # Check if main.py has argparse code
        with open('main.py', 'r') as f:
            content = f.read()

        if '--boss_alertness' in content:
            print("✅ --boss_alertness argument is defined")
        else:
            print("❌ --boss_alertness argument NOT found")
            return False

        if '--boss_alertness_cooldown' in content:
            print("✅ --boss_alertness_cooldown argument is defined")
        else:
            print("❌ --boss_alertness_cooldown argument NOT found")
            return False

        # Check default values
        if 'default=50' in content or 'default: 50' in content:
            print("✅ Default boss_alertness found")

        if 'default=300' in content or 'default: 300' in content:
            print("✅ Default boss_alertness_cooldown found")

        print("\n✅ Command-line arguments are properly defined!")
        return True

    except Exception as e:
        print(f"❌ Error checking command-line args: {e}")
        return False


def test_mcp_server():
    """Test 6: Verify MCP server setup"""
    print("\n" + "=" * 70)
    print("TEST 6: MCP Server Setup")
    print("=" * 70)

    try:
        from main import mcp

        print(f"✅ MCP server instance created: {type(mcp)}")

        # Check if it's a FastMCP instance
        if hasattr(mcp, 'tool'):
            print("✅ MCP has 'tool' decorator")
        else:
            print("⚠️  MCP doesn't have 'tool' decorator (might be okay)")

        print("\n✅ MCP server is set up!")
        return True

    except ImportError as e:
        print(f"❌ Failed to import MCP server: {e}")
        return False


def run_all_tests():
    """Run all quick tests"""
    print("=" * 70)
    print("ChillMCP Quick Tests")
    print("Fast tests without time delays")
    print("=" * 70)

    tests = [
        ("Response Parsing", test_response_parsing),
        ("Tool Definitions", test_tool_definitions),
        ("ServerState Class", test_state_class),
        ("Response Formatting", test_format_response),
        ("Command-Line Arguments", test_command_line_args),
        ("MCP Server Setup", test_mcp_server),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = 0
    failed = 0

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if result:
            passed += 1
        else:
            failed += 1

    print("-" * 70)
    print(f"Total: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 70)

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
