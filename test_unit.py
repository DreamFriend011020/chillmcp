#!/usr/bin/env python3
"""
ChillMCP Unit Tests
Tests for ServerState class and individual functions
"""

import unittest
import time
from unittest.mock import patch, MagicMock
from main import ServerState


class TestServerState(unittest.TestCase):
    """Unit tests for ServerState class"""

    def setUp(self):
        """Set up fresh ServerState for each test"""
        self.state = ServerState()
        self.state.stress_level = 50
        self.state.boss_alert_level = 0
        self.state.boss_alertness = 50
        self.state.boss_alertness_cooldown = 300

    def test_initial_state(self):
        """Test initial state values"""
        state = ServerState()
        self.assertEqual(state.stress_level, 50)
        self.assertEqual(state.boss_alert_level, 0)
        self.assertEqual(state.boss_alertness, 50)
        self.assertEqual(state.boss_alertness_cooldown, 300)

    def test_stress_level_boundaries(self):
        """Test stress level stays within 0-100"""
        # Test upper boundary
        self.state.stress_level = 95
        self.state.last_stress_update = time.time() - 600  # 10 minutes ago
        self.state.update_stress()
        self.assertLessEqual(self.state.stress_level, 100)
        self.assertEqual(self.state.stress_level, 100)

        # Test lower boundary
        self.state.stress_level = 5
        self.state.decrease_stress(10)
        self.assertGreaterEqual(self.state.stress_level, 0)
        self.assertEqual(self.state.stress_level, 0)

    def test_boss_alert_boundaries(self):
        """Test boss alert level stays within 0-5"""
        # Test upper boundary
        self.state.boss_alert_level = 4
        with patch('random.randint', return_value=100):  # Always triggers
            self.state.boss_alertness = 100
            self.state.increase_boss_alert()
            self.assertLessEqual(self.state.boss_alert_level, 5)
            self.assertEqual(self.state.boss_alert_level, 5)

            # Try to go over 5
            self.state.increase_boss_alert()
            self.assertEqual(self.state.boss_alert_level, 5)

        # Test lower boundary
        self.state.boss_alert_level = 1
        self.state.last_boss_cooldown = time.time() - 600
        self.state.boss_alertness_cooldown = 300
        self.state.update_boss_cooldown()
        self.assertGreaterEqual(self.state.boss_alert_level, 0)

    def test_stress_increase_rate(self):
        """Test stress increases 1 point per minute"""
        self.state.stress_level = 50
        self.state.last_stress_update = time.time() - 120  # 2 minutes ago

        self.state.update_stress()

        # Should increase by 2 points (2 minutes)
        self.assertEqual(self.state.stress_level, 52)

    def test_stress_decrease_random(self):
        """Test stress decreases by random amount 1-100"""
        self.state.stress_level = 80

        with patch('random.randint', return_value=30):
            self.state.decrease_stress()
            self.assertEqual(self.state.stress_level, 50)

    def test_stress_decrease_specific(self):
        """Test stress decreases by specific amount"""
        self.state.stress_level = 80
        self.state.decrease_stress(25)
        self.assertEqual(self.state.stress_level, 55)

    def test_boss_alert_increase_probability(self):
        """Test boss alert increases based on probability"""
        # 100% probability - should always increase
        self.state.boss_alertness = 100
        self.state.boss_alert_level = 0

        with patch('random.randint', return_value=50):  # Any value <= 100
            result = self.state.increase_boss_alert()
            self.assertTrue(result)
            self.assertEqual(self.state.boss_alert_level, 1)

        # 0% probability - should never increase
        self.state.boss_alertness = 0
        self.state.boss_alert_level = 0

        with patch('random.randint', return_value=50):  # Any value > 0
            result = self.state.increase_boss_alert()
            self.assertFalse(result)
            self.assertEqual(self.state.boss_alert_level, 0)

    def test_boss_cooldown_decrease(self):
        """Test boss alert decreases after cooldown period"""
        self.state.boss_alert_level = 3
        self.state.boss_alertness_cooldown = 10  # 10 seconds
        self.state.last_boss_cooldown = time.time() - 25  # 25 seconds ago

        self.state.update_boss_cooldown()

        # Should decrease by 2 (25 seconds / 10 seconds cooldown)
        self.assertEqual(self.state.boss_alert_level, 1)

    def test_boss_cooldown_multiple_periods(self):
        """Test boss alert handles multiple cooldown periods"""
        self.state.boss_alert_level = 5
        self.state.boss_alertness_cooldown = 10
        self.state.last_boss_cooldown = time.time() - 60  # 60 seconds ago

        self.state.update_boss_cooldown()

        # Should decrease by 6, but capped at 0
        self.assertEqual(self.state.boss_alert_level, 0)

    def test_stress_no_change_if_time_not_elapsed(self):
        """Test stress doesn't change if less than 1 minute passed"""
        self.state.stress_level = 50
        self.state.last_stress_update = time.time() - 30  # 30 seconds ago

        self.state.update_stress()

        # Should remain the same
        self.assertEqual(self.state.stress_level, 50)

    def test_boss_no_change_if_cooldown_not_elapsed(self):
        """Test boss alert doesn't change if cooldown not elapsed"""
        self.state.boss_alert_level = 3
        self.state.boss_alertness_cooldown = 300
        self.state.last_boss_cooldown = time.time() - 100  # 100 seconds ago

        self.state.update_boss_cooldown()

        # Should remain the same (100 < 300)
        self.assertEqual(self.state.boss_alert_level, 3)


class TestAsyncBossDelay(unittest.TestCase):
    """Test boss delay functionality"""

    def setUp(self):
        """Set up state for delay tests"""
        from main import state
        self.state = state

    @patch('asyncio.sleep')
    async def test_boss_delay_at_level_5(self, mock_sleep):
        """Test 20 second delay when boss alert is 5"""
        self.state.boss_alert_level = 5

        await self.state.apply_boss_delay()

        mock_sleep.assert_called_once_with(20)

    @patch('asyncio.sleep')
    async def test_no_delay_below_level_5(self, mock_sleep):
        """Test no delay when boss alert is below 5"""
        for level in range(5):
            mock_sleep.reset_mock()
            self.state.boss_alert_level = level

            await self.state.apply_boss_delay()

            mock_sleep.assert_not_called()


def run_tests():
    """Run all unit tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestServerState))
    suite.addTests(loader.loadTestsFromTestCase(TestAsyncBossDelay))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 70)
    print("ChillMCP Unit Tests")
    print("Testing ServerState class and core functionality")
    print("=" * 70)
    print()

    success = run_tests()

    print()
    print("=" * 70)
    if success:
        print("✅ All unit tests passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 70)

    exit(0 if success else 1)
