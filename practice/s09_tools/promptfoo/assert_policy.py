"""Promptfoo의 Python 채점(assert type: python). 섹션 2의 old_doc을 Promptfoo에 연결합니다. API 호출 없음.

  python3 assert_policy.py --check     TODO 자가 점검 (R13은 실패, R17은 통과여야 합니다)

Promptfoo는 답마다 get_assert(output, context)를 부르고, 돌려준 pass 로 통과 · 실패를 표시합니다.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import find_old_policy, load_cases, stale_words  # noqa: E402


def passed(found_old_policy: bool) -> bool:
    """예시 답안. 섹션 2 함수가 옛 정책을 찾았으면 통과가 아닙니다."""
    return not found_old_policy


def get_assert(output: str, context: dict) -> dict:
    v = context["vars"]
    cited = [d for d in (v.get("cited") or "").split(",") if d]
    found = find_old_policy(output, cited)
    ok = passed(found)
    words = ", ".join(stale_words(output))
    reason = (f"옛 정책을 현행처럼 안내하지 않음 (옛 기준과 같은 글자: {words} · 근거 {', '.join(cited)})" if ok and words
              else "옛 정책을 현행처럼 안내하지 않음" if ok
              else f"옛 정책을 현행처럼 안내함: {words} · 근거 {', '.join(cited)}")
    return {"pass": ok, "score": 1.0 if ok else 0.0, "reason": reason}


def check() -> int:
    try:
        cases = {c["id"]: c for c in load_cases()}
        got = {k: get_assert(cases[k]["reply"], {"vars": {"cited": ",".join(cases[k]["cited"])}})["pass"] for k in ("R13", "R17")}
    except NotImplementedError as e:
        print(f"아직 채우지 않았습니다: {e}")
        return 1
    if got == {"R13": False, "R17": True}:
        print("TODO 통과  R13 실패 · R17 통과 (판정 방향이 맞습니다)")
        return 0
    print(f"  ✗ 기대 R13 실패 · R17 통과 / 지금 R13 {'통과' if got['R13'] else '실패'} · R17 {'통과' if got['R17'] else '실패'}")
    print("  힌트: 섹션 2 함수가 True 를 돌려주면, 이 답은 통과가 아닙니다.")
    return 1


if __name__ == "__main__" and "--check" in sys.argv:
    raise SystemExit(check())
