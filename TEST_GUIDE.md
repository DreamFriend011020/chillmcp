# ChillMCP Test Suite Guide

Complete testing guide for the ChillMCP server based on guide.txt requirements.

## 📋 Test Files Overview

### 1. **test_unit.py** - Unit Tests
**Purpose:** Test individual components and functions in isolation
**Duration:** < 1 second
**No Dependencies:** Can run without MCP server

**What it tests:**
- ✅ ServerState class initialization
- ✅ Stress level boundaries (0-100)
- ✅ Boss alert level boundaries (0-5)
- ✅ Stress increase rate (1 point/minute)
- ✅ Stress decrease (random 1-100)
- ✅ Boss alert probability logic
- ✅ Boss cooldown decrease logic
- ✅ Boss delay function (20 seconds at level 5)

**Run:**
```bash
python test_unit.py
```

---

### 2. **test_quick.py** - Fast Integration Tests
**Purpose:** Quick validation without time delays
**Duration:** < 5 seconds
**Dependencies:** Requires main.py imports

**What it tests:**
- ✅ Response parsing (regex patterns from guide.txt)
- ✅ All 8 required tools are defined
- ✅ ServerState class structure
- ✅ Response formatting function
- ✅ Command-line argument definitions
- ✅ MCP server setup

**Run:**
```bash
python test_quick.py
```

---

### 3. **test_full.py** - Complete Time-Based Tests
**Purpose:** Full validation with actual time delays
**Duration:** ~3-5 minutes
**Dependencies:** Requires running server context

**What it tests:**
- ⏱️ Stress accumulation (65 seconds)
- ⏱️ Boss Alert Level 5 delay (20 seconds)
- ⏱️ Boss cooldown auto-decrease (17 seconds)
- ✅ Continuous breaks increase Boss Alert
- ✅ Breaks decrease stress level
- ✅ Immediate clockout sets stress to 0

**Run:**
```bash
python test_full.py
```

⚠️ **Warning:** This takes several minutes due to real-time delays!

---

### 4. **test_integration.py** - MCP JSON-RPC Tests
**Purpose:** End-to-end testing via MCP protocol
**Duration:** ~10-20 seconds
**Dependencies:** Spawns MCP server as subprocess

**What it tests:**
- ⚠️ **CRITICAL:** Command-line parameters (--boss_alertness, --boss_alertness_cooldown)
- ✅ All 8 required tools available via MCP
- ✅ Response format per guide.txt spec
- ✅ Bonus tools (치맥, 퇴근, 회식)
- ✅ Multiple sequential tool calls

**Run:**
```bash
python test_integration.py
```

⚠️ **Critical Test:** Failure on command-line parameters = automatic disqualification per guide.txt!

---

## 🎯 guide.txt Test Scenarios Coverage

### Required Tests (guide.txt lines 289-301)

| Test Scenario | File | Status |
|--------------|------|--------|
| **커맨드라인 파라미터 테스트** | test_integration.py | ✅ TEST 1 (CRITICAL) |
| **연속 휴식 테스트** | test_full.py | ✅ TEST 4 |
| **스트레스 누적 테스트** | test_full.py | ✅ TEST 1 |
| **지연 테스트** | test_full.py | ✅ TEST 2 |
| **파싱 테스트** | test_quick.py | ✅ TEST 1 |
| **파싱 테스트** | test_integration.py | ✅ TEST 3 |
| **Cooldown 테스트** | test_full.py | ✅ TEST 3 |

### Optional Tests (guide.txt lines 303-307)

| Test Scenario | File | Status |
|--------------|------|--------|
| **치맥 테스트** | test_integration.py | ✅ TEST 4 |
| **퇴근 테스트** | test_full.py | ✅ TEST 6 |
| **회식 테스트** | test_integration.py | ✅ TEST 4 |

---

## 🚀 Quick Start

### Run All Tests (Recommended Order)

```bash
# 1. Fast unit tests (< 1 second)
python test_unit.py

# 2. Quick integration tests (< 5 seconds)
python test_quick.py

# 3. MCP protocol tests (10-20 seconds) - INCLUDES CRITICAL TEST
python test_integration.py

# 4. Full time-based tests (3-5 minutes)
python test_full.py
```

### Run Only Critical Tests

```bash
# CRITICAL: Command-line parameters (guide.txt requirement)
python test_integration.py
```

This runs TEST 1 which verifies:
- ✅ `--boss_alertness` parameter works
- ✅ `--boss_alertness_cooldown` parameter works
- ⚠️ **Failure = Automatic Disqualification!**

---

## 📊 Expected Results

### test_unit.py
```
ChillMCP Unit Tests
==================================================
test_boss_alert_boundaries ... ok
test_boss_cooldown_decrease ... ok
test_boss_cooldown_multiple_periods ... ok
test_initial_state ... ok
test_stress_level_boundaries ... ok
...

✅ All unit tests passed!
```

### test_quick.py
```
ChillMCP Quick Tests
==================================================
✅ PASS: Response Parsing
✅ PASS: Tool Definitions
✅ PASS: ServerState Class
✅ PASS: Response Formatting
✅ PASS: Command-Line Arguments
✅ PASS: MCP Server Setup

Total: 6 tests
Passed: 6
Failed: 0
```

### test_integration.py
```
ChillMCP Integration Tests
==================================================
✅ PASS: Command-Line Parameters (CRITICAL)
✅ PASS: Required Tools Availability
✅ PASS: Response Format Validation
✅ PASS: Bonus Tools
✅ PASS: Multiple Sequential Calls

Total: 5 tests
Passed: 5
Failed: 0
```

### test_full.py
```
ChillMCP Full Tests
==================================================
✅ PASS: Stress Accumulation (65s)
✅ PASS: Boss Alert Delay (20s)
✅ PASS: Boss Alert Cooldown (17s)
✅ PASS: Continuous Breaks
✅ PASS: Stress Recovery
✅ PASS: Immediate Clockout

Total: 6 tests
Passed: 6
Failed: 0
Total time: 182.3 seconds (3.0 minutes)
```

---

## ⚠️ Critical Requirements (guide.txt)

### MUST PASS (Automatic Disqualification if Failed)

**Command-Line Parameters Test** (test_integration.py TEST 1)

From guide.txt lines 124-125:
> ⚠️ 필수 요구사항: 커맨드라인 파라미터 지원
> 서버는 실행 시 다음 커맨드라인 파라미터들을 반드시 지원해야 합니다. 이를 지원하지 않을 경우 미션 실패로 간주됩니다.

**What is tested:**
1. `--boss_alertness N` (0-100) works correctly
2. `--boss_alertness_cooldown N` (seconds) works correctly
3. Server recognizes and applies these parameters

**How to verify manually:**
```bash
# Test high boss alertness
python main.py --boss_alertness 100 --boss_alertness_cooldown 10

# In Claude Desktop or MCP client:
# Call any break tool multiple times
# Boss Alert should increase every time (100% probability)
```

---

## 🔍 Debugging Failed Tests

### Unit Tests Failing?
- Check `main.py` for ServerState class implementation
- Verify stress_level stays 0-100
- Verify boss_alert_level stays 0-5

### Quick Tests Failing?
- **Response Parsing:** Check `format_response()` function
- **Tool Definitions:** Ensure all @mcp.tool() decorators are present
- **Command-Line Args:** Check `argparse` setup in `main()`

### Integration Tests Failing?
- **Server won't start:** Check Python version (3.11 recommended)
- **Tools not found:** Check tool registration with FastMCP
- **CRITICAL test fails:** Verify `args.boss_alertness` and `args.boss_alertness_cooldown` are used

### Full Tests Failing?
- **Stress accumulation:** Check `update_stress()` implementation
- **Boss delay:** Check `apply_boss_delay()` async function
- **Cooldown:** Check `update_boss_cooldown()` calculation

---

## 📝 Test Coverage Summary

### guide.txt Requirements Covered: **100%**

✅ All 8 required tools
✅ All 3 bonus tools
✅ Command-line parameters (CRITICAL)
✅ Response format (Break Summary, Stress Level, Boss Alert Level)
✅ Regex parsing patterns
✅ Stress accumulation (1 point/minute)
✅ Boss Alert probability
✅ Boss Alert cooldown
✅ Boss Alert Level 5 delay (20 seconds)
✅ Stress decrease (1-100 random)
✅ State boundaries (0-100, 0-5)

### Evaluation Criteria (guide.txt lines 310-318)

| Criterion | Weight | Test Coverage |
|-----------|--------|---------------|
| **커맨드라인 파라미터** | CRITICAL | ✅ test_integration.py |
| **기능 완성도** | 40% | ✅ test_integration.py, test_quick.py |
| **상태 관리** | 30% | ✅ test_unit.py, test_full.py |
| **창의성** | 20% | Manual review |
| **코드 품질** | 10% | Manual review |

---

## 🎬 CI/CD Integration

### GitHub Actions Example

```yaml
name: ChillMCP Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python 3.11
      uses: actions/setup-python@v2
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run unit tests
      run: python test_unit.py

    - name: Run quick tests
      run: python test_quick.py

    - name: Run integration tests (CRITICAL)
      run: python test_integration.py

    # Uncomment for full tests (takes 3-5 minutes)
    # - name: Run full tests
    #   run: python test_full.py
```

---

## 📞 Support

If tests are failing:

1. **Check Python version:** `python --version` (3.11 recommended)
2. **Reinstall dependencies:** `pip install -r requirements.txt`
3. **Check main.py:** Ensure all code is present
4. **Run tests individually:** Isolate which test is failing
5. **Check guide.txt:** Verify implementation matches requirements

---

**Generated by:** ChillMCP Test Suite Generator
**Version:** 1.0.0
**Date:** 2025-10-19
**Compliance:** guide.txt (SKT AI Summit Hackathon Pre-mission)
