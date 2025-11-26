# -*- coding: utf-8 -*-
"""
中文GIF动画验证码
"""

from io import BytesIO
from PIL import Image, ImageDraw

from ..base.chinese_captcha_abstract import ChineseCaptchaAbstract


class ChineseGifCaptcha(ChineseCaptchaAbstract):
    """中文GIF动画验证码"""
    
    def __init__(self, width: int = 130, height: int = 48, length: int = 4):
        """
        初始化中文GIF验证码
        
        Args:
            width: 验证码宽度
            height: 验证码高度
            length: 验证码字符数
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
        chars = self.text_char()
        
        try:
            # 为每个字符生成随机颜色
            font_colors = [self._color() for _ in range(self._len)]
            
            # 生成贝塞尔曲线参数
            x1 = 5
            y1 = self.num(5, self._height // 2)
            x2 = self._width - 5
            y2 = self.num(self._height // 2, self._height - 5)
            ctrlx = self.num(self._width // 4, self._width * 3 // 4)
            ctrly = self.num(5, self._height - 5)
            
            if self.num(2) == 0:
                y1, y2 = y2, y1
            
            ctrlx1 = self.num(self._width // 4, self._width * 3 // 4)
            ctrly1 = self.num(5, self._height - 5)
            
            bezier_params = [(x1, y1), (ctrlx, ctrly), (ctrlx1, ctrly1), (x2, y2)]
            
            # 生成每一帧
            frames = []
            for i in range(self._len):
                frame = self._graphics_image(font_colors, chars, i, bezier_params)
                frames.append(frame)
            
            # 保存为GIF
            frames[0].save(
                stream,
                format='GIF',
                save_all=True,
                append_images=frames[1:],
                duration=100,  # 每帧100ms
                loop=0  # 无限循环
            )
            stream.seek(0)
            return True
            
        except Exception as e:
            print(f"生成中文GIF验证码失败: {e}")
            return False
    
    def to_base64(self, prefix: str = "data:image/gif;base64,") -> str:
        """
        输出base64编码
        
        Args:
            prefix: base64前缀
            
        Returns:
            str: base64编码字符串
        """
        return self._to_base64_impl(prefix)
    
    def _graphics_image(self, font_colors, chars, flag, bezier_params):
        """
        生成单帧图像
        
        Args:
            font_colors: 字体颜色列表
            chars: 字符列表
            flag: 当前帧索引
            bezier_params: 贝塞尔曲线参数
            
        Returns:
            Image: PIL图像对象
        """
        # 创建图像
        image = Image.new('RGB', (self._width, self._height), 'white')
        draw = ImageDraw.Draw(image)
        
        # 绘制干扰圆
        self.draw_oval(2, draw)
        
        # 绘制贝塞尔曲线
        curve_points = self._cubic_bezier_points(
            bezier_params[0], bezier_params[1], 
            bezier_params[2], bezier_params[3], 50
        )
        draw.line(curve_points, fill=font_colors[0], width=2)
        
        # 绘制验证码文字
        font = self.get_font()
        char_width = self._width // len(chars)
        
        for i, char in enumerate(chars):
            # 计算透明度（渐变效果）
            alpha = self._get_alpha(flag, i)
            
            # 根据透明度调整颜色亮度
            color = self._adjust_color_alpha(font_colors[i], alpha)
            
            # 计算字符位置
            bbox = draw.textbbox((0, 0), char, font=font)
            char_w = bbox[2] - bbox[0]
            char_h = bbox[3] - bbox[1]
            
            char_spacing = (char_width - char_w) // 2
            x = i * char_width + char_spacing - 3
            y = (self._height - char_h) // 2 - 3
            
            # 绘制字符
            draw.text((x, y), char, fill=color, font=font)
        
        return image
    
    def _get_alpha(self, i, j):
        """
        获取透明度，从0到1，自动计算步长
        
        Args:
            i: 当前帧索引
            j: 字符索引
            
        Returns:
            float: 透明度值 (0-1)
        """
        num = i + j
        r = 1.0 / (self._len - 1) if self._len > 1 else 1.0
        s = self._len * r
        return (num * r - s) if num >= self._len else num * r
    
    def _adjust_color_alpha(self, color, alpha):
        """
        根据透明度调整颜色
        
        Args:
            color: RGB颜色元组
            alpha: 透明度 (0-1)
            
        Returns:
            tuple: 调整后的RGB颜色
        """
        # 简单的透明度模拟：与白色混合
        r = int(color[0] * alpha + 255 * (1 - alpha))
        g = int(color[1] * alpha + 255 * (1 - alpha))
        b = int(color[2] * alpha + 255 * (1 - alpha))
        return (r, g, b)

