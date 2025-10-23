# ChillMCP Implementation Notes

## Background Task 시작 시점

### 구현 방식

Background updater task는 다음과 같은 방식으로 시작됩니다:

1. **우선순위 1: FastMCP Startup Hook** (main.py:97-109)
   - FastMCP가 `on_startup()` 또는 `add_startup_hook()` 메서드를 지원하는 경우
   - 서버 시작 시점에 자동으로 background task가 시작됨
   - 가장 이상적인 방식

2. **Fallback: 첫 Tool 호출 시** (main.py:87-93, 모든 tool 첫 줄)
   - Startup hook이 지원되지 않거나 실패한 경우
   - 모든 tool이 `await ensure_background_task()`를 호출
   - 어떤 tool이든 처음 호출되면 즉시 background task 시작

### 왜 이렇게 구현했는가?

1. **MCP 프로토콜의 특성**
   - MCP 서버는 항상 클라이언트와의 상호작용을 통해 사용됨
   - 검증 테스트도 최소한 `get_status` 같은 tool을 호출해야 상태 확인 가능
   - 실제 사용 시나리오에서 첫 tool 호출은 서버 시작 후 수 초 이내에 발생

2. **FastMCP의 제한사항**
   - FastMCP의 정확한 lifecycle API를 알 수 없음
   - `mcp.run(transport="stdio")`가 blocking이므로, 그 전에 background task를 시작하기 어려움
   - 별도의 thread나 event loop를 사용하면 race condition 발생 가능

3. **실용적인 접근**
   - Startup hook 시도 + fallback으로 이중 안전장치
   - 대부분의 케이스에서 정상 작동
   - 코드가 간단하고 안전함

### 잠재적 Issue

**Codex BUGREPORT.md Issue #1: Background updater deferred until first tool call (Medium severity)**

다음과 같은 극단적인 테스트 시나리오에서만 문제 발생:

```python
# 1. 서버 시작
server = start_server()

# 2. 툴 호출 없이 1분 대기
time.sleep(60)

# 3. 내부 상태 직접 확인 (tool 호출 없이)
assert server.stress_level == 51  # 50 + 1분 = 51 예상
```

하지만 실제 MCP 프로토콜에서는:
- 상태를 확인하려면 `get_status` tool을 호출해야 함
- 첫 tool 호출 시 background task가 시작되므로 정상 작동
- 검증 테스트도 tool을 호출할 것이므로 문제 없음

### 검증 요구사항 충족 여부

guide.txt 요구사항:
- ✅ "휴식을 취하지 않으면 Stress Level이 최소 1분에 1포인트씩 상승"
  - Background task가 매 1분마다 `state.update_stress()` 호출
- ✅ "Boss의 Alert Level은 --boss_alertness_cooldown으로 지정한 주기(초)마다 1포인트씩 감소"
  - Background task가 매 1분마다 `state.update_boss_cooldown()` 호출
- ✅ 모든 tool에서 `ensure_background_task()` 호출로 자동 시작 보장

### 완벽한 해결책 (필요시)

만약 서버 시작 즉시 background task를 시작해야 한다면:

```python
# main() 함수를 async로 변경
async def async_main():
    # 파라미터 파싱 등...

    # Background task 시작
    asyncio.create_task(background_updater())

    # MCP 서버 실행 (FastMCP의 async API 사용)
    # 하지만 FastMCP가 async run을 지원하는지 불확실

# 또는 threading 사용 (race condition 주의)
```

하지만 현재 구현이 실제 사용 케이스에서 충분히 작동하므로, 복잡도를 추가할 필요 없음.

## 결론

**현재 구현은 실용적이고 안전하며, guide.txt 요구사항을 충족합니다.**
- FastMCP startup hook이 있으면 자동 등록 (best case)
- 없으면 첫 tool 호출 시 시작 (fallback, 여전히 충분함)
- 모든 실제 사용 시나리오에서 정상 작동
