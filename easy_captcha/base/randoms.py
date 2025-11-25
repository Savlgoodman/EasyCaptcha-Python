# -*- coding: utf-8 -*-
"""
随机数工具类
"""

import secrets


class Randoms:
    """随机数生成工具类"""
    
    # 验证码字符集，去除了0、O、I、L等容易混淆的字母
    ALPHA = [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]
    
    # 数字的最大索引（不包括）
    NUM_MAX_INDEX = 8
    # 字符的最小索引（包括）
    CHAR_MIN_INDEX = NUM_MAX_INDEX
    # 字符的最大索引（不包括）
    CHAR_MAX_INDEX = len(ALPHA)
    # 大写字符最小索引
    UPPER_MIN_INDEX = CHAR_MIN_INDEX
    # 大写字符最大索引
    UPPER_MAX_INDEX = UPPER_MIN_INDEX + 23
    # 小写字母最小索引
    LOWER_MIN_INDEX = UPPER_MAX_INDEX
    # 小写字母最大索引
    LOWER_MAX_INDEX = CHAR_MAX_INDEX
    
    @staticmethod
    def num(min_val=None, max_val=None):
        """
        生成随机数
        
        Args:
            min_val: 最小值（包括），如果为None则从0开始
            max_val: 最大值（不包括），如果为None则min_val作为最大值
            
        Returns:
            int: 随机数
        """
        if min_val is None and max_val is None:
            raise ValueError("至少需要提供一个参数")
        
        if max_val is None:
            # 只提供一个参数，生成0到min_val之间的随机数
            return secrets.randbelow(min_val)
        else:
            # 提供两个参数，生成min_val到max_val之间的随机数
            return min_val + secrets.randbelow(max_val - min_val)
    
    @classmethod
    def alpha(cls, min_index=None, max_index=None):
        """
        返回ALPHA中的随机字符
        
        Args:
            min_index: 最小索引（包括）
            max_index: 最大索引（不包括）
            
        Returns:
            str: 随机字符
        """
        if min_index is None and max_index is None:
            # 返回所有字符中的随机一个
            return cls.ALPHA[cls.num(len(cls.ALPHA))]
        elif max_index is None:
            # 返回0到min_index之间的随机字符
            return cls.ALPHA[cls.num(min_index)]
        else:
            # 返回min_index到max_index之间的随机字符
            return cls.ALPHA[cls.num(min_index, max_index)]

