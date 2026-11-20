"""섹션 2 · 1단계. 실패 유형 하나에 채점기 하나. 결과는 실패(True) 아니면 통과(False) 둘뿐입니다. API를 부르지 않습니다.

  python3 graders.py --check     TODO 1 · TODO 2 자가 점검 (몇 번이든 돌려도 됩니다)

채점기는 섹션 1에서 남긴 기록 한 건(r)을 받습니다. r["reply"]는 답 문장, r["cited"]는 근거로 댄 문서 ID 목록입니다.
"""

from __future__ import annotations

import re
import sys

OLD_DOCS = {"D02", "D04"}           # 폐지된 반품 정책 v2, 2026-05에 쓴 옛 FAQ
STALE = ["2주", "14일", "5,000원"]   # 옛 문서에만 있는 기한·금액


def foreign_chars(reply: str) -> list[str]:
    """예시 답안. 가나·한자 범위를 한 덩어리씩 찾습니다."""
    return re.findall(r"[\u3040-\u30ff\u4e00-\u9fff]+", reply)


def old_doc_naive(r: dict) -> bool:
    """이론 장의 '문장 기준' 그대로입니다(고치지 않습니다). 옛 숫자가 어디든 들어 있으면 실패."""
    return any(s in (r.get("reply") or "") for s in STALE)


def old_doc(r: dict) -> bool:
    """예시 답안. 옛 기한(2주)이나 배송비 옆의 5,000원을 안내했는데, '폐지'라고 밝히지 않았으면 실패."""
    t = r.get("reply") or ""
    stale = "2주" in t or re.search(r"배송비[^.\n]{0,12}5,000원", t)
    return bool(stale) and "폐지" not in t


# 유형 → 그 유형을 채점하는 채점기들 (이름, 함수). grade.py 와 compare.py 가 씁니다.
GRADERS = {
    "lang": [("foreign_chars", lambda r: bool(foreign_chars(r.get("reply") or "")))],
    "old_doc": [("old_doc_naive", old_doc_naive), ("old_doc", old_doc)],
}
TYPE_NAMES = {"lang": "다른 언어가 섞임", "old_doc": "옛 문서를 근거로 답함",
              "ask_info": "필요한 정보를 묻지 않음"}   # 섹션 3: 코드 채점기 없이 사람 라벨과 LLM 판정기로


def check() -> int:
    bad = 0
    try:
        cases = [("환불은 9월 1일からの v3 정책에 따릅니다", ["からの"]), ("2번公式에 따라 계산합니다", ["公式"]),
                 ("현행 v3 기준으로 7일 이내입니다", [])]
        wrong = [(t, w, foreign_chars(t)) for t, w in cases if foreign_chars(t) != w]
        for t, w, g in wrong:
            print(f"  ✗ TODO 1 \"{t}\" → 기대 {w} / 지금 {g}")
        if wrong:
            bad += 1; print("  힌트: re.findall 에 문자 범위 [\\u3040-\\u30ff\\u4e00-\\u9fff] 를 넣고 + 로 덩어리째 잡습니다.")
        else:
            print("TODO 1 통과  가나 · 한자 · 한국어만 있는 문장 3개")
    except NotImplementedError as e:
        bad += 1; print(f"아직 채우지 않았습니다: {e}")
    cases = [
        ("받은 날로부터 2주 안에는 부담 없이 반품하실 수 있어요", ["D04"], True),
        ("단순 변심이면 반품 배송비는 5,000원이에요", ["D04"], True),
        ("11월 14일에 받으신 상품은 7일 이내라 반품할 수 있습니다", ["D01"], False),
        ("주문하신 25,000원 양말은 반품 배송비 3,000원을 뺍니다", ["D01"], False),
        ("상품 쿠폰으로 5,000원을 쓰셨다면 결제 금액 기준으로 환불됩니다", ["D09"], False),
        ("검색된 D02는 폐지된 정책이라 14일·5,000원 기준은 적용할 수 없습니다", ["D02"], False),
    ]
    try:
        wrong = [(t, w) for t, c, w in cases if old_doc({"reply": t, "cited": c}) != w]
        for t, w in wrong:
            print(f"  ✗ TODO 2 \"{t}\" → 기대 {'실패' if w else '통과'}")
        if wrong:
            bad += 1; print("  힌트: 옛 숫자가 '어떤 말과 같이' 나왔는지 보세요. 배송비 옆의 5,000원, '폐지'라는 말.")
        else:
            print(f"TODO 2 통과  실패 2 · 통과 4 (날짜 · 25,000원 · 쿠폰 · 폐지라고 밝힘)")
    except NotImplementedError as e:
        bad += 1; print(f"아직 채우지 않았습니다: {e}")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    print(__doc__)
