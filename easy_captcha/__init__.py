# -*- coding: utf-8 -*-
"""
EasyCaptcha - Python图形验证码生成库
支持GIF、中文、算术等类型
"""

__version__ = "1.0.0"

from .captcha.spec_captcha import SpecCaptcha
from .constants import (
    TYPE_DEFAULT,
    TYPE_ONLY_NUMBER,
    TYPE_ONLY_CHAR,
    TYPE_ONLY_UPPER,
    TYPE_ONLY_LOWER,
    TYPE_NUM_AND_UPPER,
    FONT_1, FONT_2, FONT_3, FONT_4, FONT_5,
    FONT_6, FONT_7, FONT_8, FONT_9, FONT_10
)

__all__ = [
    'SpecCaptcha',
    'TYPE_DEFAULT',
    'TYPE_ONLY_NUMBER',
    'TYPE_ONLY_CHAR',
    'TYPE_ONLY_UPPER',
    'TYPE_ONLY_LOWER',
    'TYPE_NUM_AND_UPPER',
    'FONT_1', 'FONT_2', 'FONT_3', 'FONT_4', 'FONT_5',
    'FONT_6', 'FONT_7', 'FONT_8', 'FONT_9', 'FONT_10'
]

