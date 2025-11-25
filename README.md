# EasyCaptcha-Python

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)

Python图形验证码生成库，支持GIF、中文、算术等类型。

这是 [EasyCaptcha](https://github.com/whvcse/EasyCaptcha) Java版本的Python实现。

## ✨ 特性

- 🎨 多种验证码类型：PNG、GIF、中文、算术
- 🔤 多种字符类型：数字、字母、混合
- 🎭 10种内置漂亮字体
- 🌈 贝塞尔曲线干扰线
- 🎯 简单易用的API
- 📦 零依赖（仅需Pillow）

## 📦 安装

```bash
pip install easy-captcha
```

或从源码安装：

```bash
git clone https://github.com/yourusername/easy-captcha-python.git
cd easy-captcha-python
pip install -e .
```

## 🚀 快速开始

### 基本使用

```python
from easy_captcha import SpecCaptcha
from io import BytesIO

# 创建验证码
captcha = SpecCaptcha()

# 获取验证码文本
code = captcha.text()
print(f"验证码: {code}")

# 输出到文件
with open('captcha.png', 'wb') as f:
    stream = BytesIO()
    captcha.out(stream)
    f.write(stream.getvalue())
```

### 自定义尺寸和位数

```python
from easy_captcha import SpecCaptcha

# 宽度200，高度60，验证码长度6位
captcha = SpecCaptcha(width=200, height=60, length=6)
code = captcha.text()
```

### 设置验证码类型

```python
from easy_captcha import SpecCaptcha, TYPE_ONLY_NUMBER, TYPE_ONLY_CHAR

# 纯数字验证码
captcha = SpecCaptcha()
captcha.char_type = TYPE_ONLY_NUMBER

# 纯字母验证码
captcha = SpecCaptcha()
captcha.char_type = TYPE_ONLY_CHAR
```

### 输出Base64编码

```python
from easy_captcha import SpecCaptcha

captcha = SpecCaptcha()
base64_str = captcha.to_base64()
# 返回: data:image/png;base64,iVBORw0KGgoAAAANS...

# 不需要前缀
base64_str = captcha.to_base64(prefix="")
```

### 使用不同字体

```python
from easy_captcha import SpecCaptcha, FONT_1, FONT_2

captcha = SpecCaptcha()
captcha.set_font(FONT_1, size=36)  # 使用内置字体1，大小36
```

## 📚 验证码类型

| 类型 | 说明 | 状态 |
|-----|------|------|
| `SpecCaptcha` | PNG格式验证码 | ✅ 已实现 |
| `GifCaptcha` | GIF动画验证码 | 🚧 开发中 |
| `ChineseCaptcha` | 中文验证码 | 🚧 开发中 |
| `ChineseGifCaptcha` | 中文GIF验证码 | 🚧 开发中 |
| `ArithmeticCaptcha` | 算术验证码 | 🚧 开发中 |

## 🎨 字符类型

| 常量 | 说明 |
|-----|------|
| `TYPE_DEFAULT` | 数字和字母混合 |
| `TYPE_ONLY_NUMBER` | 纯数字 |
| `TYPE_ONLY_CHAR` | 纯字母 |
| `TYPE_ONLY_UPPER` | 纯大写字母 |
| `TYPE_ONLY_LOWER` | 纯小写字母 |
| `TYPE_NUM_AND_UPPER` | 数字和大写字母 |

## 🌐 Web框架集成

### Flask示例

```python
from flask import Flask, session, make_response
from easy_captcha import SpecCaptcha
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/captcha')
def captcha():
    cap = SpecCaptcha()
    session['captcha'] = cap.text().lower()
    
    stream = BytesIO()
    cap.out(stream)
    
    response = make_response(stream.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/verify/<code>')
def verify(code):
    if code.lower() == session.get('captcha'):
        return '验证成功'
    return '验证失败'
```

### FastAPI示例

```python
from fastapi import FastAPI, Response
from easy_captcha import SpecCaptcha
from io import BytesIO

app = FastAPI()

@app.get("/captcha")
async def captcha():
    cap = SpecCaptcha()
    code = cap.text()
    
    stream = BytesIO()
    cap.out(stream)
    
    return Response(content=stream.getvalue(), media_type="image/png")
```

## 🧪 运行测试

```bash
# 运行测试
python tests/test_spec_captcha.py

# 运行示例
python examples/basic_usage.py
```

## 📄 许可证

Apache License 2.0

## 🙏 致谢

本项目是 [EasyCaptcha](https://github.com/whvcse/EasyCaptcha) 的Python实现版本。

## 🤝 贡献

欢迎提交Issue和Pull Request！

