"""
文本相似度计算模块
算法difflib.SequenceMatcher
结果范围 [0, 1]
"""

from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]


def read_text(path: PathLike) -> str:
    """按 UTF-8 编码读取"""
    return Path(path).read_text(encoding="utf-8")


def write_similarity(path: PathLike, score: float) -> None:
    """将重复率写入答案文件"""
    if not 0.0 <= score <= 1.0:
        raise ValueError("相似度必须在 [0, 1] 范围内")

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"{score:.4f}\n", encoding="utf-8")


def normalize_text(text: str) -> str:
    """归一化文本"""
    return "".join(ch.lower() for ch in text if ch.isalnum())


def calc_similarity(original: str, copied: str) -> float:
    """计算重复率"""
    left = normalize_text(original)
    right = normalize_text(copied)

    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0

    return SequenceMatcher(None, left, right).ratio()