"""Promptfoo 결과(results/check.json)를 사람이 정한 판정(../cases.json의 human)과 맞춰 봅니다. API 호출 없음.

  npx promptfoo eval      (먼저 실행. 결과가 results/check.json 에 저장됩니다)
  python3 compare.py
  python3 compare.py --pr  PR 검사 결과(results/pr.json)의 사례별 판정과 이유만 보여 줍니다. CI가 실패했을 때 씁니다(설명만 하므로 종료 코드 0)
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from cases_lib import load_cases  # noqa: E402

V = {True: "통과", False: "실패"}


def reason_of(r: dict) -> str:
    g = r.get("gradingResult") or {}
    parts = g.get("componentResults") or [g]
    return parts[0].get("reason") or r.get("error") or ""


def pr() -> int:
    out = HERE / "results" / "pr.json"
    if not out.exists():
        print("결과가 없습니다. 먼저 npx promptfoo eval -c ci/promptfooconfig.yaml 을 실행하세요.")
        return 1
    rows = json.loads(out.read_text(encoding="utf-8"))["results"]["results"]
    bad = 0
    for r in rows:
        bad += not r["success"]
        print(f"{r['testCase']['vars']['case_id']:<5} {V[bool(r['success'])]}  {reason_of(r)}")
    print(f"후보 응답 {len(rows)}건 중 실패 {bad}건" + (" · 이 PR의 답은 고객에게 보낼 수 없습니다" if bad else ""))
    return 0   # 설명만 합니다. 통과 · 실패는 앞 단계(promptfoo eval)의 종료 코드가 정합니다


def main() -> int:
    if "--pr" in sys.argv:
        return pr()
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
        reason = reason_of(r)
        print(f"{c['id']:<5} {V[human]:<4} {V[bool(r['success'])]:<9} {'O' if ok else 'X'}     {reason}")
    print(f"사람 판정과 일치 {agree}/{len(got)}")
    return 0 if agree == len(got) else 1


if __name__ == "__main__":
    raise SystemExit(main())
