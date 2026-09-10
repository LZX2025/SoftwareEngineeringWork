"""
论文查重命令行入口
用法：python main.py <原文绝对路径> <抄袭版绝对路径> <输出答案绝对路径>
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from similarity import calc_similarity, read_text, write_similarity


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="论文查重程序"
    )
    parser.add_argument("original_path", help="论文原文文件绝对路径")
    parser.add_argument("copied_path", help="抄袭版论文文件绝对路径")
    parser.add_argument("output_path", help="输出答案文件绝对路径")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """程序主函数。"""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        original = read_text(args.original_path)
        copied = read_text(args.copied_path)
        score = calc_similarity(original, copied)
        write_similarity(args.output_path, score)
    except (OSError, ValueError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    print(f"重复率: {score:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())