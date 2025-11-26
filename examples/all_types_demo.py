# -*- coding: utf-8 -*-
"""
所有验证码类型演示
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from io import BytesIO
from easy_captcha import (
    SpecCaptcha, GifCaptcha, ChineseCaptcha, 
    ChineseGifCaptcha, ArithmeticCaptcha,
    TYPE_ONLY_NUMBER, TYPE_ONLY_CHAR, FONT_1, FONT_2
)

# 创建输出目录
OUTPUT_DIR = './out'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def demo_spec_captcha():
    """演示PNG验证码"""
    print("\n" + "=" * 60)
    print("1. PNG验证码 (SpecCaptcha)")
    print("=" * 60)
    
    # 基本PNG验证码
    captcha = SpecCaptcha(width=130, height=48, length=5)
    code = captcha.text()
    
    with open(f'{OUTPUT_DIR}/spec_captcha.png', 'wb') as f:
        stream = BytesIO()
        captcha.out(stream)
        f.write(stream.getvalue())
    
    print(f"✓ 验证码文本: {code}")
    print(f"✓ 已保存到: {OUTPUT_DIR}/spec_captcha.png")
    
    # 纯数字PNG验证码
    captcha2 = SpecCaptcha(width=130, height=48, length=4)
    captcha2.char_type = TYPE_ONLY_NUMBER
    code2 = captcha2.text()
    
    with open(f'{OUTPUT_DIR}/spec_captcha_number.png', 'wb') as f:
        stream = BytesIO()
        captcha2.out(stream)
        f.write(stream.getvalue())
    
    print(f"✓ 纯数字验证码: {code2}")
    print(f"✓ 已保存到: {OUTPUT_DIR}/spec_captcha_number.png")


def demo_gif_captcha():
    """演示GIF动画验证码"""
    print("\n" + "=" * 60)
    print("2. GIF动画验证码 (GifCaptcha)")
    print("=" * 60)
    
    captcha = GifCaptcha(width=130, height=48, length=5)
    code = captcha.text()
    
    with open(f'{OUTPUT_DIR}/gif_captcha.gif', 'wb') as f:
        stream = BytesIO()
        captcha.out(stream)
        f.write(stream.getvalue())
    
    print(f"✓ 验证码文本: {code}")
    print(f"✓ 已保存到: {OUTPUT_DIR}/gif_captcha.gif")
    
    # 纯字母GIF验证码
    captcha2 = GifCaptcha(width=150, height=50, length=6)
    captcha2.char_type = TYPE_ONLY_CHAR
    code2 = captcha2.text()
    
    with open(f'{OUTPUT_DIR}/gif_captcha_char.gif', 'wb') as f:
        stream = BytesIO()
        captcha2.out(stream)
        f.write(stream.getvalue())
    
    print(f"✓ 纯字母验证码: {code2}")
    print(f"✓ 已保存到: {OUTPUT_DIR}/gif_captcha_char.gif")


def demo_arithmetic_captcha():
    """演示算术验证码"""
    print("\n" + "=" * 60)
    print("3. 算术验证码 (ArithmeticCaptcha)")
    print("=" * 60)
    
    # 2位数运算
    captcha = ArithmeticCaptcha(width=130, height=48, length=2)
    formula = captcha.get_arithmetic_string()
    result = captcha.text()
    
    with open(f'{OUTPUT_DIR}/arithmetic_captcha_2.png', 'wb') as f:
        stream = BytesIO()
        captcha.out(stream)
        f.write(stream.getvalue())
    
    print(f"✓ 算术公式: {formula}")
    print(f"✓ 计算结果: {result}")
    print(f"✓ 已保存到: {OUTPUT_DIR}/arithmetic_captcha_2.png")
    
    # 3位数运算
    captcha2 = ArithmeticCaptcha(width=150, height=48, length=3)
    formula2 = captcha2.get_arithmetic_string()
    result2 = captcha2.text()
    
    with open(f'{OUTPUT_DIR}/arithmetic_captcha_3.png', 'wb') as f:
        stream = BytesIO()
        captcha2.out(stream)
        f.write(stream.getvalue())
    
    print(f"✓ 算术公式: {formula2}")
    print(f"✓ 计算结果: {result2}")
    print(f"✓ 已保存到: {OUTPUT_DIR}/arithmetic_captcha_3.png")


def demo_chinese_captcha():
    """演示中文验证码"""
    print("\n" + "=" * 60)
    print("4. 中文验证码 (ChineseCaptcha)")
    print("=" * 60)
    
    captcha = ChineseCaptcha(width=130, height=48, length=4)
    code = captcha.text()
    
    with open(f'{OUTPUT_DIR}/chinese_captcha.png', 'wb') as f:
        stream = BytesIO()
        captcha.out(stream)
        f.write(stream.getvalue())
    
    print(f"✓ 验证码文本: {code}")
    print(f"✓ 已保存到: {OUTPUT_DIR}/chinese_captcha.png")


def demo_chinese_gif_captcha():
    """演示中文GIF验证码"""
    print("\n" + "=" * 60)
    print("5. 中文GIF动画验证码 (ChineseGifCaptcha)")
    print("=" * 60)
    
    captcha = ChineseGifCaptcha(width=130, height=48, length=4)
    code = captcha.text()
    
    with open(f'{OUTPUT_DIR}/chinese_gif_captcha.gif', 'wb') as f:
        stream = BytesIO()
        captcha.out(stream)
        f.write(stream.getvalue())
    
    print(f"✓ 验证码文本: {code}")
    print(f"✓ 已保存到: {OUTPUT_DIR}/chinese_gif_captcha.gif")


def demo_base64_output():
    """演示Base64输出"""
    print("\n" + "=" * 60)
    print("6. Base64编码输出")
    print("=" * 60)
    
    captcha = SpecCaptcha()
    code = captcha.text()
    base64_str = captcha.to_base64()
    
    print(f"✓ 验证码文本: {code}")
    print(f"✓ Base64编码 (前80字符): {base64_str[:80]}...")
    print(f"✓ 完整长度: {len(base64_str)} 字符")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("EasyCaptcha-Python 完整功能演示")
    print("=" * 60)
    
    demo_spec_captcha()
    demo_gif_captcha()
    demo_arithmetic_captcha()
    demo_chinese_captcha()
    demo_chinese_gif_captcha()
    demo_base64_output()
    
    print("\n" + "=" * 60)
    print(f"✓ 所有演示完成！验证码已保存到 {OUTPUT_DIR}/ 目录")
    print("=" * 60 + "\n")

