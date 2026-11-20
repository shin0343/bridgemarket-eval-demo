"""공통 사례 여섯 건을 섹션 2 채점기로만 채점하고, 사람 판정과 맞춰 봅니다. 도구 설치 전 확인용. API 호출 없음.

  python3 check_cases.py
"""

from __future__ import annotations

from cases_lib import find_old_policy, load_cases, short, stale_words

V = {"fail": "실패", "pass": "통과"}


def main() -> int:
    cases = load_cases()
    print("기준: 옛 정책을 현행처럼 안내했는가 · 채점기: s02/graders.py old_doc")
    print(f"{'사례':<5} {'종류':<6} {'옛 숫자':<12} {'사람':<4} {'채점기':<4} 일치")
    agree = 0
    for c in cases:
        got = "fail" if find_old_policy(c["reply"], c["cited"]) else "pass"
        ok = got == c["human"]["verdict"]
        agree += ok
        words = ", ".join(stale_words(c["reply"])) or "-"
        print(f"{c['id']:<5} {c['kind']:<6} {words:<12} {V[c['human']['verdict']]:<4} {V[got]:<4} {'O' if ok else 'X'}")
    print(f"사람 판정과 일치 {agree}/{len(cases)}")
    if agree != len(cases):
        print("어긋난 사례는 답 문장을 다시 읽고, 채점기와 사람 판정 중 무엇을 고칠지 정합니다(섹션 2의 rules.md).")
    return 0 if agree == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
