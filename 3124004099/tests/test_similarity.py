"""
测试文本相似度计算模块。
假设被测模块文件名为 similarity.py，与本测试文件在同一目录。
运行：pytest test_similarity.py -v
"""

import pytest

from similarity import (
    read_text,
    write_similarity,
    normalize_text,
    calc_similarity,
)


# ---------- normalize_text ----------

def test_normalize_text_lowercase_and_remove_punctuation():
    assert normalize_text("Hello, World!") == "helloworld"


def test_normalize_text_removes_whitespace_and_special_chars():
    assert normalize_text("  A B\tC\nD  ") == "abcd"


def test_normalize_text_keeps_alnum_only():
    assert normalize_text("abc123!@#") == "abc123"


def test_normalize_text_chinese():
    assert normalize_text("你好，世界！") == "你好世界"


def test_normalize_text_empty():
    assert normalize_text("") == ""


# ---------- calc_similarity ----------

def test_calc_similarity_identical_after_normalization():
    assert calc_similarity("Hello, World!", "hello world") == pytest.approx(1.0)


def test_calc_similarity_completely_different():
    assert calc_similarity("abc", "xyz") == pytest.approx(0.0)


def test_calc_similarity_partial():
    # "abcd" vs "abef" -> 匹配 "ab"，比例 2*2/(4+4)=0.5
    assert calc_similarity("abcd", "abef") == pytest.approx(0.5)


def test_calc_similarity_both_empty():
    assert calc_similarity("", "") == pytest.approx(1.0)


def test_calc_similarity_one_empty():
    assert calc_similarity("abc", "") == pytest.approx(0.0)
    assert calc_similarity("", "abc") == pytest.approx(0.0)


def test_calc_similarity_only_punctuation_normalizes_to_empty():
    # 两边归一化后都为空，按代码逻辑返回 1.0
    assert calc_similarity("!!!", "???") == pytest.approx(1.0)


def test_calc_similarity_chinese_partial():
    assert calc_similarity("你好世界", "你好朋友") == pytest.approx(0.5)


# ---------- write_similarity ----------

def test_write_similarity_creates_file(tmp_path):
    output = tmp_path / "score.txt"
    write_similarity(output, 0.5)
    assert output.read_text(encoding="utf-8") == "0.5000\n"


def test_write_similarity_creates_parent_dirs(tmp_path):
    output = tmp_path / "sub" / "dir" / "score.txt"
    write_similarity(output, 0.1234)
    assert output.read_text(encoding="utf-8") == "0.1234\n"


def test_write_similarity_rounds_to_4_decimals(tmp_path):
    output = tmp_path / "score.txt"

    write_similarity(output, 0.12344)
    assert output.read_text(encoding="utf-8") == "0.1234\n"

    write_similarity(output, 0.12346)
    assert output.read_text(encoding="utf-8") == "0.1235\n"


def test_write_similarity_allows_bounds(tmp_path):
    zero = tmp_path / "zero.txt"
    one = tmp_path / "one.txt"

    write_similarity(zero, 0.0)
    write_similarity(one, 1.0)

    assert zero.read_text(encoding="utf-8") == "0.0000\n"
    assert one.read_text(encoding="utf-8") == "1.0000\n"


def test_write_similarity_rejects_out_of_range(tmp_path):
    with pytest.raises(ValueError):
        write_similarity(tmp_path / "score.txt", -0.1)

    with pytest.raises(ValueError):
        write_similarity(tmp_path / "score.txt", 1.1)


# ---------- read_text ----------

def test_read_text_utf8(tmp_path):
    file = tmp_path / "text.txt"
    content = "你好，世界！\nHello"
    file.write_text(content, encoding="utf-8")

    assert read_text(file) == content


def test_read_text_accepts_str_path(tmp_path):
    file = tmp_path / "text.txt"
    file.write_text("abc", encoding="utf-8")

    assert read_text(str(file)) == "abc"


def test_read_text_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_text(tmp_path / "missing.txt")