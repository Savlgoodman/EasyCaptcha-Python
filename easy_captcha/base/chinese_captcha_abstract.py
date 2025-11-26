# -*- coding: utf-8 -*-
"""
中文验证码抽象类
"""

from .captcha import Captcha


class ChineseCaptchaAbstract(Captcha):
    """中文验证码抽象基类"""
    
    # 常用汉字字符集
    CHINESE_CHARS = (
        "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严"
    )
    
    def __init__(self):
        super().__init__()
        self._len = 4  # 中文验证码默认4个字
        # 中文验证码使用系统字体
        self.set_font_for_chinese()
    
    def set_font_for_chinese(self):
        """设置中文字体"""
        import platform
        
        # 根据操作系统选择合适的中文字体
        system = platform.system()
        
        try:
            if system == 'Windows':
                # Windows系统使用微软雅黑或宋体
                try:
                    from PIL import ImageFont
                    self._font = ImageFont.truetype("msyh.ttc", 28)  # 微软雅黑
                except:
                    try:
                        self._font = ImageFont.truetype("simsun.ttc", 28)  # 宋体
                    except:
                        self._font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 28)  # 黑体
            elif system == 'Darwin':  # macOS
                from PIL import ImageFont
                self._font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
            else:  # Linux
                from PIL import ImageFont
                # 尝试常见的Linux中文字体
                try:
                    self._font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 28)
                except:
                    try:
                        self._font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 28)
                    except:
                        self._font = ImageFont.load_default()
        except:
            from PIL import ImageFont
            self._font = ImageFont.load_default()
    
    def _alphas(self):
        """
        生成随机中文验证码
        
        Returns:
            list: 验证码字符列表
        """
        chars = []
        for i in range(self._len):
            chars.append(self._alpha_han())
        
        self._chars = ''.join(chars)
        return chars
    
    @classmethod
    def _alpha_han(cls):
        """
        返回随机汉字
        
        Returns:
            str: 随机汉字
        """
        return cls.CHINESE_CHARS[cls.num(len(cls.CHINESE_CHARS))]

