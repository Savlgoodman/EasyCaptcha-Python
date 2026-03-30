# EasyCaptcha-Python

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)
[![EN](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![中文](https://img.shields.io/badge/Language-中文-green.svg)](README_zh.md)

Python graphic captcha generation library supporting GIF, Chinese characters, arithmetic, and other types. Suitable for Python Web, desktop applications, and more.

This is a Python implementation of the [EasyCaptcha](https://github.com/whvcse/EasyCaptcha) Java version.

---

## 1. Introduction

Python graphic captcha supporting GIF, Chinese characters, arithmetic, and other types. Compatible with Flask, Django, FastAPI, and other web frameworks.

---

## 2. Demo

**PNG Type:**

![Captcha](https://s2.ax1x.com/2019/08/23/msFrE8.png)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/msF0DP.png)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/msFwut.png)

**GIF Type:**

![Captcha](https://s2.ax1x.com/2019/08/23/msFzVK.gif)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/msFvb6.gif)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/msFXK1.gif)

**Arithmetic Type:**

![Captcha](https://s2.ax1x.com/2019/08/23/mskKPg.png)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/msknIS.png)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/mskma8.png)

**Chinese Type:**

![Captcha](https://s2.ax1x.com/2019/08/23/mskcdK.png)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/msk6Z6.png)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/msksqx.png)

**Built-in Fonts:**

![Captcha](https://s2.ax1x.com/2019/08/23/msAVSJ.png)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/msAAW4.png)
&emsp;&emsp;
![Captcha](https://s2.ax1x.com/2019/08/23/msAkYF.png)

---

## 3. Installation

### 3.1. Install via pip

```bash
pip install easy-captcha-python
```

### 3.2. Install from source

```bash
git clone https://github.com/Savlgoodman/EasyCaptcha-Python
cd easy-captcha-python
pip install -e .
```

---

## 4. Usage

### 4.1. Quick Start

```python
from easy_captcha import SpecCaptcha
from io import BytesIO

# Three parameters: width, height, character count
captcha = SpecCaptcha(130, 48, 5)

# Get captcha text
code = captcha.text()
print(f"Captcha: {code}")

# Write to file
with open('captcha.png', 'wb') as f:
    stream = BytesIO()
    captcha.out(stream)
    f.write(stream.getvalue())
```

### 4.2. Use with Flask

```python
from flask import Flask, session, make_response
from easy_captcha import SpecCaptcha
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/captcha')
def captcha():
    # Create captcha
    cap = SpecCaptcha(130, 48, 5)
    # Store captcha text in session
    session['captcha'] = cap.text().lower()

    # Output image
    stream = BytesIO()
    cap.out(stream)

    response = make_response(stream.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/verify/<code>')
def verify(code):
    # Get captcha from session
    if code.lower() == session.get('captcha'):
        return 'Verification successful'
    return 'Verification failed'
```

Frontend HTML:

```html
<img src="/captcha" width="130px" height="48px" />
```

### 4.3. Use with Django

```python
from django.http import HttpResponse
from easy_captcha import SpecCaptcha
from io import BytesIO

def captcha(request):
    cap = SpecCaptcha(130, 48, 5)
    # Store captcha text in session
    request.session['captcha'] = cap.text().lower()

    # Output image
    stream = BytesIO()
    cap.out(stream)

    return HttpResponse(stream.getvalue(), content_type='image/png')
```

### 4.4. Use with FastAPI

```python
from fastapi import FastAPI, Response
from easy_captcha import SpecCaptcha
from io import BytesIO

app = FastAPI()

@app.get("/captcha")
async def captcha():
    cap = SpecCaptcha(130, 48, 5)
    code = cap.text()

    stream = BytesIO()
    cap.out(stream)

    return Response(content=stream.getvalue(), media_type="image/png")
```

### 4.5. Frontend-Backend Separated Projects

For frontend-backend separated projects, it is recommended to return base64 encoded images:

```python
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)
# Using dictionary as simulation, Redis is recommended for production
captcha_store = {}

@app.route('/captcha')
def get_captcha():
    from easy_captcha import SpecCaptcha

    cap = SpecCaptcha(130, 48, 5)
    code = cap.text().lower()
    key = str(uuid.uuid4())

    # Store captcha (recommend storing in Redis with expiration in production)
    captcha_store[key] = code

    # Return key and base64 image
    return jsonify({
        'key': key,
        'image': cap.to_base64()
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    ver_key = data.get('verKey')
    ver_code = data.get('verCode', '').lower()

    # Verify captcha
    if ver_code == captcha_store.get(ver_key):
        # Remove after successful verification
        captcha_store.pop(ver_key, None)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Captcha error'})
```

Frontend example:

```html
<img id="verImg" width="130px" height="48px" />

<script>
    var verKey;
    // Fetch captcha
    fetch("/captcha")
        .then((res) => res.json())
        .then((data) => {
            verKey = data.key;
            document.getElementById("verImg").src = data.image;
        });

    // Login
    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            verKey: verKey,
            verCode: "8u6h",
            username: "admin",
            password: "admin",
        }),
    })
        .then((res) => res.json())
        .then((data) => console.log(data));
</script>
```

---

## 5. More Settings

### 5.1. Captcha Types

```python
from easy_captcha import (
    SpecCaptcha, GifCaptcha, ChineseCaptcha,
    ChineseGifCaptcha, ArithmeticCaptcha
)

# PNG type
captcha = SpecCaptcha(130, 48, 5)
code = captcha.text()  # Get captcha text
chars = captcha.text_char()  # Get captcha character array

# GIF type
captcha = GifCaptcha(130, 48, 5)

# Chinese type
captcha = ChineseCaptcha(130, 48, 4)

# Chinese GIF type
captcha = ChineseGifCaptcha(130, 48, 4)

# Arithmetic type
captcha = ArithmeticCaptcha(130, 48, 2)
captcha.len = 3  # Number of digits for arithmetic, default is two
formula = captcha.get_arithmetic_string()  # Get arithmetic formula: 3+2=?
result = captcha.text()  # Get result: 5

# Output captcha
from io import BytesIO
stream = BytesIO()
captcha.out(stream)
```

> Note:<br/>
> &emsp;For arithmetic captcha, `len` represents the number of digits in the operation, while for other captchas `len` represents the number of characters. The `text()` method for arithmetic captcha returns the result of the formula.
> For arithmetic captcha, you should store the result in session, not the formula itself.

### 5.2. Character Types

| Type              | Description           |
| :----------------- | :-------------------- |
| TYPE_DEFAULT       | Numbers and letters   |
| TYPE_ONLY_NUMBER   | Numbers only          |
| TYPE_ONLY_CHAR     | Letters only          |
| TYPE_ONLY_UPPER    | Uppercase only        |
| TYPE_ONLY_LOWER    | Lowercase only        |
| TYPE_NUM_AND_UPPER | Numbers and uppercase |

Usage:

```python
from easy_captcha import SpecCaptcha, TYPE_ONLY_NUMBER

captcha = SpecCaptcha(130, 48, 5)
captcha.char_type = TYPE_ONLY_NUMBER
```

> Only effective for `SpecCaptcha` and `GifCaptcha`.

### 5.3. Font Settings

Built-in fonts:

| Font   | Preview                                      |
| :------ | :------------------------------------------- |
| FONT_1  | ![](https://s2.ax1x.com/2019/08/23/msMe6U.png) |
| FONT_2  | ![](https://s2.ax1x.com/2019/08/23/msMAf0.png) |
| FONT_3  | ![](https://s2.ax1x.com/2019/08/23/msMCwj.png) |
| FONT_4  | ![](https://s2.ax1x.com/2019/08/23/msM9mQ.png) |
| FONT_5  | ![](https://s2.ax1x.com/2019/08/23/msKz6S.png) |
| FONT_6  | ![](https://s2.ax1x.com/2019/08/23/msKxl8.png) |
| FONT_7  | ![](https://s2.ax1x.com/2019/08/23/msMPTs.png) |
| FONT_8  | ![](https://s2.ax1x.com/2019/08/23/msMmXF.png) |
| FONT_9  | ![](https://s2.ax1x.com/2019/08/23/msMVpV.png) |
| FONT_10 | ![](https://s2.ax1x.com/2019/08/23/msMZlT.png) |

Usage:

```python
from easy_captcha import SpecCaptcha, FONT_1, FONT_2

captcha = SpecCaptcha(130, 48, 5)

# Set built-in font
captcha.set_font(FONT_1, size=32)

# You can also use system fonts (requires PIL.ImageFont support)
from PIL import ImageFont
captcha._font = ImageFont.truetype("arial.ttf", 32)
```

### 5.4. Output base64

```python
from easy_captcha import SpecCaptcha

captcha = SpecCaptcha(130, 48, 5)
base64_str = captcha.to_base64()

# If you don't want the base64 header "data:image/png;base64,"
base64_str = captcha.to_base64("")  # Just pass an empty parameter
```

### 5.5. Output to File

```python
from easy_captcha import SpecCaptcha
from io import BytesIO

captcha = SpecCaptcha(130, 48, 5)

# Write to file
with open('captcha.png', 'wb') as f:
    stream = BytesIO()
    captcha.out(stream)
    f.write(stream.getvalue())
```

---

## 6. Complete Examples

Check the `examples/` directory for more examples:

-   `basic_usage.py` - Basic usage example
-   `all_types_demo.py` - All captcha types demo

Run examples:

```bash
# Run basic example
python examples/basic_usage.py

# Run full demo
python examples/all_types_demo.py
```

All generated captcha images will be saved to the `./out/` directory.

---

## 7. License

Apache License 2.0

---

## 8. Acknowledgments

This project is a Python implementation of [EasyCaptcha](https://github.com/whvcse/EasyCaptcha).

---

## 9. Contributing

Issues and Pull Requests are welcome!

## 10. References

For more detailed documentation, please refer to the [Usage Guide](https://github.com/Savlgoodman/EasyCaptcha-Python/blob/master/docs/EASYCAPTCHA-PYTHON-USAGE.md).
