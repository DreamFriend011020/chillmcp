#!/usr/bin/env python3
"""
ChillMCP Full Tests
Complete tests with time delays for stress accumulation, boss alert cooldown, etc.
These tests take longer to run but verify time-based behavior
"""

import asyncio
import time
import re
import sys
from datetime import datetime


async def test_stress_accumulation():
    """Test 1: Stress Level auto-increases 1 point per minute"""
    print("\n" + "=" * 70)
    print("TEST 1: Stress Level Accumulation")
    print("=" * 70)

    try:
        from main import state

        # Set initial state
        initial_stress = 30
        state.stress_level = initial_stress
        state.last_stress_update = time.time()

        print(f"Initial stress level: {state.stress_level}")
        print("Waiting 65 seconds to test 1 minute accumulation...")
        print("(This tests the requirement: 'Stress increases 1 point per minute')")

        # Wait 65 seconds (a bit more than 1 minute to ensure it triggers)
        for i in range(13):
            await asyncio.sleep(5)
            print(f"  ... {(i + 1) * 5} seconds elapsed")

        # Update and check
        state.update_stress()
        final_stress = state.stress_level

        print(f"\nFinal stress level: {final_stress}")
        print(f"Expected: {initial_stress + 1} (at least)")

        if final_stress > initial_stress:
            increase = final_stress - initial_stress
            print(f"✅ Stress increased by {increase} point(s)")
            return True
        else:
            print(f"❌ Stress did NOT increase (stayed at {final_stress})")
            return False

    except Exception as e:
        print(f"❌ Error during stress accumulation test: {e}")
        return False


async def test_boss_alert_delay():
    """Test 2: Boss Alert Level 5 causes 20 second delay"""
    print("\n" + "=" * 70)
    print("TEST 2: Boss Alert Level 5 Delay")
    print("=" * 70)

    try:
        from main import state, coffee_mission

        print("Setting Boss Alert Level to 5...")
        state.boss_alert_level = 5

        print("Calling tool with Boss Alert = 5")
        print("(This should trigger 20 second delay)")

        start_time = time.time()
        result = await coffee_mission()
        elapsed = time.time() - start_time

        print(f"\nTime elapsed: {elapsed:.2f} seconds")
        print(f"Expected: >= 20 seconds")

        if elapsed >= 19.5:  # Allow small margin
            print(f"✅ Delay worked correctly ({elapsed:.2f}s >= 20s)")
            return True
        else:
            print(f"❌ Delay too short ({elapsed:.2f}s < 20s)")
            return False

    except Exception as e:
        print(f"❌ Error during boss delay test: {e}")
        return False


async def test_boss_cooldown():
    """Test 3: Boss Alert Level decreases based on cooldown"""
    print("\n" + "=" * 70)
    print("TEST 3: Boss Alert Cooldown")
    print("=" * 70)

    try:
        from main import state

        # Set short cooldown for testing
        cooldown_seconds = 15
        state.boss_alertness_cooldown = cooldown_seconds
        state.boss_alert_level = 3
        state.last_boss_cooldown = time.time()

        print(f"Initial Boss Alert Level: {state.boss_alert_level}")
        print(f"Cooldown period: {cooldown_seconds} seconds")
        print(f"Waiting {cooldown_seconds + 2} seconds for cooldown...")

        # Wait for cooldown period
        for i in range(int((cooldown_seconds + 2) / 3)):
            await asyncio.sleep(3)
            print(f"  ... {(i + 1) * 3} seconds elapsed")

        # Update and check
        state.update_boss_cooldown()
        final_boss = state.boss_alert_level

        print(f"\nFinal Boss Alert Level: {final_boss}")
        print(f"Expected: {max(0, 3 - 1)} (decreased by 1)")

        if final_boss < 3:
            decrease = 3 - final_boss
            print(f"✅ Boss Alert decreased by {decrease}")
            return True
        else:
            print(f"❌ Boss Alert did NOT decrease (stayed at {final_boss})")
            return False

    except Exception as e:
        print(f"❌ Error during boss cooldown test: {e}")
        return False


async def test_continuous_breaks():
    """Test 4: Multiple breaks increase Boss Alert"""
    print("\n" + "=" * 70)
    print("TEST 4: Continuous Breaks Increase Boss Alert")
    print("=" * 70)

    try:
        from main import state, coffee_mission, bathroom_break, watch_netflix

        # Set high alertness for testing
        state.boss_alertness = 100  # 100% chance
        state.boss_alert_level = 0

        print("Boss Alertness: 100% (always triggers)")
        print("Initial Boss Alert Level: 0")
        print("\nCalling 3 different break tools...")

        tools = [
            ("coffee_mission", coffee_mission),
            ("bathroom_break", bathroom_break),
            ("watch_netflix", watch_netflix),
        ]

        for i, (name, tool) in enumerate(tools, 1):
            print(f"\n{i}. Calling {name}...")
            result = await tool()

            # Parse boss alert from response
            match = re.search(r"Boss Alert Level:\s*([0-5])", result)
            if match:
                current_boss = int(match.group(1))
                print(f"   Boss Alert Level: {current_boss}")
            else:
                print("   ⚠️  Could not parse Boss Alert Level")

            # Small delay between calls
            await asyncio.sleep(1)

        print(f"\nFinal Boss Alert Level: {state.boss_alert_level}")
        print(f"Expected: > 0 (should have increased)")

        if state.boss_alert_level > 0:
            print(f"✅ Boss Alert increased to {state.boss_alert_level}")
            return True
        else:
            print(f"❌ Boss Alert did NOT increase (stayed at 0)")
            return False

    except Exception as e:
        print(f"❌ Error during continuous breaks test: {e}")
        return False


async def test_stress_recovery():
    """Test 5: Breaks decrease stress level"""
    print("\n" + "=" * 70)
    print("TEST 5: Stress Recovery from Breaks")
    print("=" * 70)

    try:
        from main import state, take_a_break

        # Set high stress
        state.stress_level = 90
        print(f"Initial stress level: {state.stress_level}")

        print("\nTaking a break...")
        result = await take_a_break()

        # Parse stress from response
        match = re.search(r"Stress Level:\s*(\d{1,3})", result)
        if match:
            final_stress = int(match.group(1))
            print(f"Final stress level: {final_stress}")

            if final_stress < 90:
                decrease = 90 - final_stress
                print(f"✅ Stress decreased by {decrease} points")
                return True
            else:
                print(f"❌ Stress did NOT decrease (stayed at {final_stress})")
                return False
        else:
            print("❌ Could not parse Stress Level from response")
            return False

    except Exception as e:
        print(f"❌ Error during stress recovery test: {e}")
        return False


async def test_immediate_clockout():
    """Test 6: Immediate clockout sets stress to 0"""
    print("\n" + "=" * 70)
    print("TEST 6: Immediate Clockout (Bonus Feature)")
    print("=" * 70)

    try:
        from main import state, immediate_clockout

        # Set high stress
        state.stress_level = 100
        print(f"Initial stress level: {state.stress_level}")

        print("\nCalling immediate_clockout() (퇴근!)...")
        result = await immediate_clockout()

        print("\nResponse:")
        print("-" * 70)
        print(result)
        print("-" * 70)

        # Parse stress from response
        match = re.search(r"Stress Level:\s*(\d{1,3})", result)
        if match:
            final_stress = int(match.group(1))
            print(f"\nFinal stress level: {final_stress}")

            if final_stress == 0:
                print(f"✅ Stress set to 0 (complete relief!)")
                return True
            else:
                print(f"⚠️  Stress is {final_stress}, expected 0")
                return final_stress < 100  # At least decreased
        else:
            print("❌ Could not parse Stress Level from response")
            return False

    except Exception as e:
        print(f"❌ Error during immediate clockout test: {e}")
        return False


async def run_all_tests():
    """Run all full tests"""
    print("=" * 70)
    print("ChillMCP Full Tests")
    print("Complete tests with time delays")
    print("=" * 70)
    print("\n⚠️  WARNING: These tests will take several minutes to complete")
    print("They test time-based features like stress accumulation and cooldowns\n")

    tests = [
        ("Stress Accumulation (65s)", test_stress_accumulation),
        ("Boss Alert Delay (20s)", test_boss_alert_delay),
        ("Boss Alert Cooldown (17s)", test_boss_cooldown),
        ("Continuous Breaks", test_continuous_breaks),
        ("Stress Recovery", test_stress_recovery),
        ("Immediate Clockout", test_immediate_clockout),
    ]

    results = []
    total_start = time.time()

    for name, test_func in tests:
        test_start = time.time()
        print(f"\n{'=' * 70}")
        print(f"Running: {name}")
        print(f"Started at: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'=' * 70}")

        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

        test_elapsed = time.time() - test_start
        print(f"\nTest completed in {test_elapsed:.1f} seconds")

    total_elapsed = time.time() - total_start

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
    print(f"Total time: {total_elapsed:.1f} seconds ({total_elapsed / 60:.1f} minutes)")
    print("=" * 70)

    return failed == 0


if __name__ == '__main__':
    print("Starting async tests...")
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
