# -*- coding: utf-8 -*-
"""
SpecCaptcha 测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from io import BytesIO
from easy_captcha import SpecCaptcha, TYPE_ONLY_NUMBER


def test_basic_creation():
    """测试基本创建"""
    captcha = SpecCaptcha()
    assert captcha is not None
    print("✓ 基本创建测试通过")


def test_text_generation():
    """测试验证码文本生成"""
    captcha = SpecCaptcha(length=5)
    text = captcha.text()
    assert text is not None
    assert len(text) == 5
    print(f"✓ 文本生成测试通过: {text}")


def test_custom_size():
    """测试自定义尺寸"""
    captcha = SpecCaptcha(width=200, height=60, length=6)
    assert captcha.width == 200
    assert captcha.height == 60
    assert captcha.len == 6
    print("✓ 自定义尺寸测试通过")


def test_only_number():
    """测试纯数字验证码"""
    captcha = SpecCaptcha()
    captcha.char_type = TYPE_ONLY_NUMBER
    text = captcha.text()
    assert text.isdigit()
    print(f"✓ 纯数字验证码测试通过: {text}")


def test_image_output():
    """测试图像输出"""
    captcha = SpecCaptcha()
    stream = BytesIO()
    result = captcha.out(stream)
    assert result is True
    assert stream.getvalue() is not None
    assert len(stream.getvalue()) > 0
    print(f"✓ 图像输出测试通过，大小: {len(stream.getvalue())} 字节")


def test_base64_output():
    """测试Base64输出"""
    captcha = SpecCaptcha()
    base64_str = captcha.to_base64()
    assert base64_str is not None
    assert base64_str.startswith("data:image/png;base64,")
    print(f"✓ Base64输出测试通过，长度: {len(base64_str)}")


def test_multiple_generation():
    """测试多次生成"""
    texts = set()
    for i in range(10):
        captcha = SpecCaptcha()
        text = captcha.text()
        texts.add(text)
    
    # 10次生成应该有不同的验证码
    assert len(texts) > 1
    print(f"✓ 多次生成测试通过，生成了 {len(texts)} 个不同的验证码")


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("运行 SpecCaptcha 测试")
    print("=" * 50 + "\n")
    
    test_basic_creation()
    test_text_generation()
    test_custom_size()
    test_only_number()
    test_image_output()
    test_base64_output()
    test_multiple_generation()
    
    print("\n" + "=" * 50)
    print("所有测试通过！✓")
    print("=" * 50 + "\n")

