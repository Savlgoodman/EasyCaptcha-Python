# -*- coding: utf-8 -*-
"""
算术验证码（PNG格式）
"""

from io import BytesIO
from PIL import Image, ImageDraw

from ..base.arithmetic_captcha_abstract import ArithmeticCaptchaAbstract


class ArithmeticCaptcha(ArithmeticCaptchaAbstract):
    """算术验证码（PNG格式）"""
    
    def __init__(self, width: int = 130, height: int = 48, length: int = 2):
        """
        初始化算术验证码
        
        Args:
            width: 验证码宽度
            height: 验证码高度
            length: 运算数字的位数（默认2位数运算）
        """
        super().__init__()
        self._width = width
        self._height = height
        self._len = length
    
    def out(self, stream: BytesIO) -> bool:
        """
        输出验证码到流
        
        Args:
            stream: 输出流
            
        Returns:
            bool: 是否成功
        """
        self.check_alpha()
        # 显示算术公式而不是结果
        return self._graphics_image(list(self.get_arithmetic_string()), stream)
    
    def to_base64(self, prefix: str = "data:image/png;base64,") -> str:
        """
        输出base64编码
        
        Args:
            prefix: base64前缀
            
        Returns:
            str: base64编码字符串
        """
        return self._to_base64_impl(prefix)
    
    def _graphics_image(self, chars, stream: BytesIO) -> bool:
        """
        生成验证码图像
        
        Args:
            chars: 验证码字符列表（算术公式）
            stream: 输出流
            
        Returns:
            bool: 是否成功
        """
        try:
            # 创建图像
            image = Image.new('RGB', (self._width, self._height), 'white')
            draw = ImageDraw.Draw(image)
            
            # 绘制干扰圆
            self.draw_oval(2, draw)
            
            # 绘制验证码文字
            font = self.get_font()
            
            # 计算每个字符的宽度
            char_width = self._width // len(chars)
            
            for i, char in enumerate(chars):
                # 随机颜色
                color = self._color()
                
                # 计算字符位置
                bbox = draw.textbbox((0, 0), char, font=font)
                char_w = bbox[2] - bbox[0]
                char_h = bbox[3] - bbox[1]
                
                # 字符的左右边距
                char_spacing = (char_width - char_w) // 2
                
                # 字符的x坐标
                x = i * char_width + char_spacing + 3
                
                # 字符的y坐标（垂直居中）
                y = (self._height - char_h) // 2 - 3
                
                # 绘制字符
                draw.text((x, y), char, fill=color, font=font)
            
            # 保存为PNG
            image.save(stream, format='PNG')
            stream.seek(0)
            return True
            
        except Exception as e:
            print(f"生成算术验证码失败: {e}")
            return False

