"""보너스 실습 공통 코드. 사례 읽기와 2강 채점기 불러오기. 모델을 부르지 않습니다.

세 도구(LangSmith · Promptfoo · DeepEval)가 모두 이 파일을 씁니다.
채점 기준은 섹션 2의 old_doc 하나입니다. 도구를 바꿔도 기준은 그대로 둡니다.
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent          # practice/s09_tools
PRACTICE = HERE.parent                                  # practice
CASES = HERE / "cases.json"
STALE = ["2주", "14일", "5,000원"]                       # 섹션 2 graders.py 와 같은 목록

sys.path.insert(0, str(PRACTICE / "s02"))
from graders import old_doc as _old_doc  # noqa: E402  섹션 2에서 채운 함수


def load_cases(path: pathlib.Path = CASES) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def find_old_policy(reply: str, cited: list[str]) -> bool:
    """섹션 2의 old_doc 그대로. True 면 '옛 정책을 현행처럼 안내함'을 찾았다(= 실패)는 뜻입니다."""
    try:
        return bool(_old_doc({"reply": reply, "cited": cited}))
    except NotImplementedError:
        raise SystemExit("섹션 2 graders.py의 TODO 2(old_doc)를 먼저 채워 주세요. "
                         "막히면 practice/s02/solution/old_doc.py 를 참고합니다.")


def stale_words(reply: str) -> list[str]:
    """답 문장에 들어 있는 옛 숫자. 판정에는 쓰지 않고, 결과 화면의 이유 문장에만 씁니다."""
    return [w for w in STALE if w in (reply or "")]


def short(text: str, n: int = 60) -> str:
    t = " ".join((text or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"
