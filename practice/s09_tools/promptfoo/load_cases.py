"""Promptfoo가 부르는 테스트 생성 함수. 공통 사례(../cases.json)를 Promptfoo 테스트 형식으로 바꿉니다.

promptfooconfig.yaml 의  tests: file://load_cases.py:generate_tests  가 이 함수를 부릅니다.
사람이 정한 판정(human)은 넘기지 않습니다. 채점기는 답 문장과 근거 문서만 봅니다.
"""

from __future__ import annotations

import json
import os
import pathlib

HERE = pathlib.Path(__file__).resolve().parent


def to_tests(cases: list[dict]) -> list[dict]:
    return [{
        "description": f"{c['id']} · {c.get('kind', '후보 응답')}",
        "vars": {"case_id": c["id"], "question": c["question"], "reply": c["reply"],
                 "cited": ",".join(c.get("cited", []))},   # 목록을 그대로 넣으면 Promptfoo가 경우의 수로 펼칩니다
    } for c in cases]


def generate_tests(config=None):
    path = HERE.parent / "cases.json"
    if config and config.get("path"):
        path = HERE / config["path"]
    return to_tests(json.loads(path.read_text(encoding="utf-8"))["cases"])
