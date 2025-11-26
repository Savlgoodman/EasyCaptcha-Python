# -*- coding: utf-8 -*-
"""
算术验证码抽象类
"""

from .captcha import Captcha


class ArithmeticCaptchaAbstract(Captcha):
    """算术验证码抽象基类"""
    
    def __init__(self):
        super().__init__()
        self._len = 2  # 算术验证码默认2位数运算
        self._arithmetic_string = None  # 算术公式字符串
    
    def _alphas(self):
        """
        生成随机算术验证码
        
        Returns:
            list: 验证码字符列表（这里是计算结果）
        """
        formula_parts = []
        
        # 生成算术表达式
        for i in range(self._len):
            # 生成0-9的随机数字
            num = self.num(10)
            formula_parts.append(str(num))
            
            # 如果不是最后一个数字，添加运算符
            if i < self._len - 1:
                operator_type = self.num(1, 4)  # 1: +, 2: -, 3: x
                if operator_type == 1:
                    formula_parts.append('+')
                elif operator_type == 2:
                    formula_parts.append('-')
                else:  # operator_type == 3
                    formula_parts.append('x')
        
        # 构建公式字符串
        formula = ''.join(formula_parts)
        
        # 计算结果
        try:
            # 将 'x' 替换为 '*' 进行计算
            result = eval(formula.replace('x', '*'))
            # 确保结果为整数
            result = int(result)
            self._chars = str(result)
        except:
            # 如果计算失败，默认为0
            self._chars = '0'
        
        # 保存公式字符串（显示用）
        self._arithmetic_string = formula + '=?'
        
        return list(self._chars)
    
    def get_arithmetic_string(self):
        """
        获取算术公式字符串
        
        Returns:
            str: 算术公式，如 "3+2=?"
        """
        self.check_alpha()
        return self._arithmetic_string
    
    def set_arithmetic_string(self, arithmetic_string):
        """
        设置算术公式字符串
        
        Args:
            arithmetic_string: 算术公式字符串
        """
        self._arithmetic_string = arithmetic_string

