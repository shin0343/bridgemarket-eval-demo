"""Promptfoo 결과(results/check.json)를 사람이 정한 판정(../cases.json의 human)과 맞춰 봅니다. API 호출 없음.

  npx promptfoo eval      (먼저 실행. 결과가 results/check.json 에 저장됩니다)
  python3 compare.py
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from common import load_cases  # noqa: E402

V = {True: "통과", False: "실패"}


def main() -> int:
    out = HERE / "results" / "check.json"
    if not out.exists():
        print("결과가 없습니다. 먼저 npx promptfoo eval 을 실행하세요.")
        return 1
    rows = json.loads(out.read_text(encoding="utf-8"))["results"]["results"]
    got = {r["testCase"]["vars"]["case_id"]: r for r in rows}
    agree = 0
    print(f"{'사례':<5} {'사람':<4} {'Promptfoo':<9} 일치  이유")
    for c in load_cases():
        r = got.get(c["id"])
        if r is None:
            print(f"{c['id']:<5} 결과에 없음"); continue
        human = c["human"]["verdict"] == "pass"
        ok = bool(r["success"]) == human
        agree += ok
        g = r.get("gradingResult") or {}
        parts = g.get("componentResults") or [g]
        reason = parts[0].get("reason") or r.get("error") or ""
        print(f"{c['id']:<5} {V[human]:<4} {V[bool(r['success'])]:<9} {'O' if ok else 'X'}     {reason}")
    print(f"사람 판정과 일치 {agree}/{len(got)}")
    return 0 if agree == len(got) else 1


if __name__ == "__main__":
    raise SystemExit(main())
