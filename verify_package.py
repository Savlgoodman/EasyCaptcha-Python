#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证 easy-captcha-python 包的完整性和功能
"""

import os
import sys
from io import BytesIO

def test_imports():
    """测试所有导入"""
    print("=" * 60)
    print("1. 测试导入...")
    print("=" * 60)
    
    try:
        from easy_captcha import (
            SpecCaptcha, GifCaptcha, ChineseCaptcha,
            ChineseGifCaptcha, ArithmeticCaptcha,
            TYPE_DEFAULT, TYPE_ONLY_NUMBER, TYPE_ONLY_CHAR,
            TYPE_ONLY_UPPER, TYPE_ONLY_LOWER, TYPE_NUM_AND_UPPER,
            FONT_1, FONT_2, FONT_3, FONT_4, FONT_5,
            FONT_6, FONT_7, FONT_8, FONT_9, FONT_10,
            __version__
        )
        print("✓ 所有类和常量导入成功")
        print(f"✓ 版本: {__version__}")
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_spec_captcha():
    """测试PNG验证码"""
    print("\n" + "=" * 60)
    print("2. 测试 SpecCaptcha (PNG验证码)...")
    print("=" * 60)
    
    try:
        from easy_captcha import SpecCaptcha, TYPE_ONLY_NUMBER
        
        cap = SpecCaptcha(130, 48, 5)
        code = cap.text()
        
        stream = BytesIO()
        cap.out(stream)
        
        print(f"✓ 生成成功，验证码: {code}")
        print(f"✓ 图片大小: {len(stream.getvalue())} bytes")
        
        # 测试Base64
        base64_str = cap.to_base64()
        print(f"✓ Base64编码成功，长度: {len(base64_str)}")
        
        # 测试字符类型
        cap.char_type = TYPE_ONLY_NUMBER
        num_code = cap.text()
        print(f"✓ 纯数字验证码: {num_code}")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gif_captcha():
    """测试GIF验证码"""
    print("\n" + "=" * 60)
    print("3. 测试 GifCaptcha (GIF动画验证码)...")
    print("=" * 60)
    
    try:
        from easy_captcha import GifCaptcha
        
        cap = GifCaptcha(130, 48, 5)
        code = cap.text()
        
        stream = BytesIO()
        cap.out(stream)
        
        print(f"✓ 生成成功，验证码: {code}")
        print(f"✓ GIF大小: {len(stream.getvalue())} bytes")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_arithmetic_captcha():
    """测试算术验证码"""
    print("\n" + "=" * 60)
    print("4. 测试 ArithmeticCaptcha (算术验证码)...")
    print("=" * 60)
    
    try:
        from easy_captcha import ArithmeticCaptcha
        
        cap = ArithmeticCaptcha(130, 48, 2)
        formula = cap.get_arithmetic_string()
        result = cap.text()
        
        stream = BytesIO()
        cap.out(stream)
        
        print(f"✓ 生成成功，公式: {formula}")
        print(f"✓ 结果: {result}")
        print(f"✓ 图片大小: {len(stream.getvalue())} bytes")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chinese_captcha():
    """测试中文验证码"""
    print("\n" + "=" * 60)
    print("5. 测试 ChineseCaptcha (中文验证码)...")
    print("=" * 60)
    
    try:
        from easy_captcha import ChineseCaptcha
        
        cap = ChineseCaptcha(130, 48, 4)
        code = cap.text()
        
        stream = BytesIO()
        cap.out(stream)
        
        print(f"✓ 生成成功，验证码: {code}")
        print(f"✓ 图片大小: {len(stream.getvalue())} bytes")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chinese_gif_captcha():
    """测试中文GIF验证码"""
    print("\n" + "=" * 60)
    print("6. 测试 ChineseGifCaptcha (中文GIF验证码)...")
    print("=" * 60)
    
    try:
        from easy_captcha import ChineseGifCaptcha
        
        cap = ChineseGifCaptcha(130, 48, 4)
        code = cap.text()
        
        stream = BytesIO()
        cap.out(stream)
        
        print(f"✓ 生成成功，验证码: {code}")
        print(f"✓ GIF大小: {len(stream.getvalue())} bytes")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("easy-captcha-python 包验证")
    print("=" * 60)
    
    results = []
    
    results.append(("导入测试", test_imports()))
    results.append(("SpecCaptcha", test_spec_captcha()))
    results.append(("GifCaptcha", test_gif_captcha()))
    results.append(("ArithmeticCaptcha", test_arithmetic_captcha()))
    results.append(("ChineseCaptcha", test_chinese_captcha()))
    results.append(("ChineseGifCaptcha", test_chinese_gif_captcha()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:20s} {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"总计: {passed}/{total} 测试通过")
    print("=" * 60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

