# -*- coding: utf-8 -*-
"""
验证码抽象基类
"""

import base64
import os
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from .randoms import Randoms
from ..constants import *


class Captcha(Randoms, ABC):
    """验证码抽象基类"""
    
    def __init__(self):
        self._font = None
        self._len = 5  # 验证码字符长度
        self._width = 130  # 验证码宽度
        self._height = 48  # 验证码高度
        self._char_type = TYPE_DEFAULT  # 验证码字符类型
        self._chars = None  # 当前验证码文本
        self._font_size = 32  # 字体大小
    
    def _alphas(self):
        """
        生成随机验证码字符
        
        Returns:
            list: 验证码字符列表
        """
        chars = []
        for i in range(self._len):
            if self._char_type == TYPE_ONLY_NUMBER:
                # 纯数字
                chars.append(self.alpha(self.NUM_MAX_INDEX))
            elif self._char_type == TYPE_ONLY_CHAR:
                # 纯字母
                chars.append(self.alpha(self.CHAR_MIN_INDEX, self.CHAR_MAX_INDEX))
            elif self._char_type == TYPE_ONLY_UPPER:
                # 纯大写字母
                chars.append(self.alpha(self.UPPER_MIN_INDEX, self.UPPER_MAX_INDEX))
            elif self._char_type == TYPE_ONLY_LOWER:
                # 纯小写字母
                chars.append(self.alpha(self.LOWER_MIN_INDEX, self.LOWER_MAX_INDEX))
            elif self._char_type == TYPE_NUM_AND_UPPER:
                # 数字和大写字母
                chars.append(self.alpha(self.UPPER_MAX_INDEX))
            else:
                # 默认：数字和字母混合
                chars.append(self.alpha())
        
        self._chars = ''.join(chars)
        return chars
    
    def _color(self, fc=None, bc=None):
        """
        生成随机颜色
        
        Args:
            fc: 前景色最小值 (0-255)
            bc: 背景色最大值 (0-255)
            
        Returns:
            tuple: RGB颜色元组
        """
        if fc is not None and bc is not None:
            if fc > 255:
                fc = 255
            if bc > 255:
                bc = 255
            r = fc + self.num(bc - fc)
            g = fc + self.num(bc - fc)
            b = fc + self.num(bc - fc)
            return (r, g, b)
        else:
            # 返回预定义的常用颜色
            return COLORS[self.num(len(COLORS))]
    
    def check_alpha(self):
        """检查验证码是否已生成，如果没有则生成"""
        if self._chars is None:
            self._alphas()
    
    def text(self):
        """
        获取验证码文本
        
        Returns:
            str: 验证码文本
        """
        self.check_alpha()
        return self._chars
    
    def text_char(self):
        """
        获取验证码字符列表
        
        Returns:
            list: 验证码字符列表
        """
        self.check_alpha()
        return list(self._chars)
    
    @abstractmethod
    def out(self, stream: BytesIO) -> bool:
        """
        输出验证码到流
        
        Args:
            stream: 输出流
            
        Returns:
            bool: 是否成功
        """
        pass
    
    @abstractmethod
    def to_base64(self, prefix: str = "") -> str:
        """
        输出base64编码
        
        Args:
            prefix: base64前缀
            
        Returns:
            str: base64编码字符串
        """
        pass
    
    def _to_base64_impl(self, prefix: str = "") -> str:
        """
        base64编码实现

        Args:
            prefix: base64前缀

        Returns:
            str: base64编码字符串
        """
        stream = BytesIO()
        self.out(stream)
        b64_data = base64.b64encode(stream.getvalue()).decode('utf-8')
        return prefix + b64_data

    def draw_line(self, num: int, draw: ImageDraw.Draw, color: Optional[Tuple[int, int, int]] = None):
        """
        绘制干扰线

        Args:
            num: 线条数量
            draw: ImageDraw对象
            color: 线条颜色，None则随机
        """
        for i in range(num):
            line_color = color if color else self._color()
            x1 = self.num(-10, self._width - 10)
            y1 = self.num(5, self._height - 5)
            x2 = self.num(10, self._width + 10)
            y2 = self.num(2, self._height - 2)
            draw.line([(x1, y1), (x2, y2)], fill=line_color, width=1)

    def draw_oval(self, num: int, draw: ImageDraw.Draw, color: Optional[Tuple[int, int, int]] = None):
        """
        绘制干扰圆

        Args:
            num: 圆圈数量
            draw: ImageDraw对象
            color: 圆圈颜色，None则随机
        """
        for i in range(num):
            oval_color = color if color else self._color()
            w = 5 + self.num(10)
            x = self.num(self._width - 25)
            y = self.num(self._height - 15)
            draw.ellipse([x, y, x + w, y + w], outline=oval_color)

    def draw_bezier_curve(self, num: int, draw: ImageDraw.Draw, color: Optional[Tuple[int, int, int]] = None):
        """
        绘制贝塞尔曲线

        Args:
            num: 曲线数量
            draw: ImageDraw对象
            color: 曲线颜色，None则随机
        """
        for i in range(num):
            curve_color = color if color else self._color()

            # 起点和终点
            x1 = 5
            y1 = self.num(5, self._height // 2)
            x2 = self._width - 5
            y2 = self.num(self._height // 2, self._height - 5)

            # 控制点
            ctrlx = self.num(self._width // 4, self._width * 3 // 4)
            ctrly = self.num(5, self._height - 5)

            # 随机交换起点和终点的y坐标
            if self.num(2) == 0:
                y1, y2 = y2, y1

            # 随机选择二阶或三阶贝塞尔曲线
            if self.num(2) == 0:
                # 二阶贝塞尔曲线
                points = self._quadratic_bezier_points((x1, y1), (ctrlx, ctrly), (x2, y2), 50)
            else:
                # 三阶贝塞尔曲线
                ctrlx1 = self.num(self._width // 4, self._width * 3 // 4)
                ctrly1 = self.num(5, self._height - 5)
                points = self._cubic_bezier_points((x1, y1), (ctrlx, ctrly), (ctrlx1, ctrly1), (x2, y2), 50)

            draw.line(points, fill=curve_color, width=2)

    def _quadratic_bezier_points(self, p0, p1, p2, num_points):
        """
        计算二阶贝塞尔曲线上的点

        Args:
            p0: 起点 (x, y)
            p1: 控制点 (x, y)
            p2: 终点 (x, y)
            num_points: 点的数量

        Returns:
            list: 点的列表
        """
        points = []
        for i in range(num_points + 1):
            t = i / num_points
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            points.append((x, y))
        return points

    def _cubic_bezier_points(self, p0, p1, p2, p3, num_points):
        """
        计算三阶贝塞尔曲线上的点

        Args:
            p0: 起点 (x, y)
            p1: 控制点1 (x, y)
            p2: 控制点2 (x, y)
            p3: 终点 (x, y)
            num_points: 点的数量

        Returns:
            list: 点的列表
        """
        points = []
        for i in range(num_points + 1):
            t = i / num_points
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
            points.append((x, y))
        return points

    def get_font(self):
        """
        获取字体

        Returns:
            ImageFont: 字体对象
        """
        if self._font is None:
            self.set_font(FONT_1)
        return self._font

    def set_font(self, font, size: int = 32):
        """
        设置字体

        Args:
            font: 字体索引(0-9)或字体文件路径
            size: 字体大小
        """
        self._font_size = size

        if isinstance(font, int):
            # 使用内置字体
            font_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'fonts',
                FONT_NAMES[font]
            )
            try:
                self._font = ImageFont.truetype(font_path, size)
            except:
                # 如果加载失败，使用默认字体
                self._font = ImageFont.load_default()
        else:
            # 使用自定义字体文件
            try:
                self._font = ImageFont.truetype(font, size)
            except:
                self._font = ImageFont.load_default()

    # Getter和Setter方法
    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, value):
        self._len = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def char_type(self):
        return self._char_type

    @char_type.setter
    def char_type(self, value):
        self._char_type = value

