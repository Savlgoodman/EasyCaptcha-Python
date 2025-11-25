# -*- coding: utf-8 -*-
"""
基本使用示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from io import BytesIO
from easy_captcha import SpecCaptcha, TYPE_ONLY_NUMBER, FONT_1


def example_1_basic():
    """示例1: 基本使用"""
    print("=" * 50)
    print("示例1: 基本使用")
    print("=" * 50)
    
    # 创建验证码对象
    captcha = SpecCaptcha()
    
    # 获取验证码文本
    code = captcha.text()
    print(f"验证码文本: {code}")
    
    # 输出到文件
    with open('captcha_basic.png', 'wb') as f:
        stream = BytesIO()
        captcha.out(stream)
        f.write(stream.getvalue())
    
    print("验证码已保存到: captcha_basic.png")
    print()


def example_2_custom_size():
    """示例2: 自定义宽高和位数"""
    print("=" * 50)
    print("示例2: 自定义宽高和位数")
    print("=" * 50)
    
    # 创建自定义尺寸的验证码
    captcha = SpecCaptcha(width=200, height=60, length=6)
    
    code = captcha.text()
    print(f"验证码文本: {code}")
    
    with open('captcha_custom_size.png', 'wb') as f:
        stream = BytesIO()
        captcha.out(stream)
        f.write(stream.getvalue())
    
    print("验证码已保存到: captcha_custom_size.png")
    print()


def example_3_only_number():
    """示例3: 纯数字验证码"""
    print("=" * 50)
    print("示例3: 纯数字验证码")
    print("=" * 50)
    
    captcha = SpecCaptcha(width=130, height=48, length=4)
    captcha.char_type = TYPE_ONLY_NUMBER
    
    code = captcha.text()
    print(f"验证码文本: {code}")
    
    with open('captcha_only_number.png', 'wb') as f:
        stream = BytesIO()
        captcha.out(stream)
        f.write(stream.getvalue())
    
    print("验证码已保存到: captcha_only_number.png")
    print()


def example_4_base64():
    """示例4: 输出Base64编码"""
    print("=" * 50)
    print("示例4: 输出Base64编码")
    print("=" * 50)
    
    captcha = SpecCaptcha()
    
    code = captcha.text()
    print(f"验证码文本: {code}")
    
    # 获取base64编码
    base64_str = captcha.to_base64()
    print(f"Base64编码 (前100字符): {base64_str[:100]}...")
    
    # 也可以不要前缀
    base64_no_prefix = captcha.to_base64(prefix="")
    print(f"无前缀Base64 (前100字符): {base64_no_prefix[:100]}...")
    print()


def example_5_custom_font():
    """示例5: 使用不同的内置字体"""
    print("=" * 50)
    print("示例5: 使用不同的内置字体")
    print("=" * 50)
    
    for i in range(3):
        captcha = SpecCaptcha()
        captcha.set_font(i, size=36)  # 使用字体索引0, 1, 2
        
        code = captcha.text()
        print(f"字体{i} - 验证码文本: {code}")
        
        with open(f'captcha_font_{i}.png', 'wb') as f:
            stream = BytesIO()
            captcha.out(stream)
            f.write(stream.getvalue())
        
        print(f"验证码已保存到: captcha_font_{i}.png")
    
    print()


def example_6_multiple():
    """示例6: 批量生成验证码"""
    print("=" * 50)
    print("示例6: 批量生成5个验证码")
    print("=" * 50)
    
    for i in range(5):
        captcha = SpecCaptcha()
        code = captcha.text()
        
        with open(f'captcha_batch_{i}.png', 'wb') as f:
            stream = BytesIO()
            captcha.out(stream)
            f.write(stream.getvalue())
        
        print(f"验证码 {i+1}: {code} -> captcha_batch_{i}.png")
    
    print()


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("EasyCaptcha Python 使用示例")
    print("=" * 50 + "\n")
    
    example_1_basic()
    example_2_custom_size()
    example_3_only_number()
    example_4_base64()
    example_5_custom_font()
    example_6_multiple()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)

