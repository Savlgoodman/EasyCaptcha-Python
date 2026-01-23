print("init")
from easy_captcha import SpecCaptcha
from io import BytesIO
print("import success")

# 三个参数分别为宽、高、位数
captcha = SpecCaptcha(130, 48, 5)

# 获取验证码文本
code = captcha.text()
print(f"验证码: {code}")

# 输出到文件
with open('captcha.png', 'wb') as f:
    stream = BytesIO()
    captcha.out(stream)
    f.write(stream.getvalue())