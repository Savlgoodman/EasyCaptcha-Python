# EasyCaptcha-Python

[中文文档](README_zh.md) | English

![Captcha](https://s2.ax1x.com/2019/08/23/msMe6U.png)

---

## 1. Introduction

**EasyCaptcha-Python** is a Python captcha generation library that supports multiple types of captchas including GIF animations, Chinese characters, and arithmetic operations.

**Features:**

-   🎨 5 captcha types (PNG, GIF, Chinese, Chinese GIF, Arithmetic)
-   🔤 6 character types (mixed, numbers only, letters only, etc.)
-   🎭 10 built-in fonts
-   🌈 Random colors and interference
-   📦 Zero extra dependencies (only Pillow required)
-   🔒 Cryptographically secure random generation
-   🚀 Easy integration with Flask, Django, FastAPI

---

## 2. Captcha Types

### PNG Captcha

![PNG Captcha](https://s2.ax1x.com/2019/08/23/msKz6S.png)

### GIF Captcha

![GIF Captcha](https://s2.ax1x.com/2019/08/23/msKxl8.png)

### Arithmetic Captcha

![Arithmetic Captcha](https://s2.ax1x.com/2019/08/23/msMPTs.png)

### Chinese Captcha

![Chinese Captcha](https://s2.ax1x.com/2019/08/23/msMmXF.png)

### Built-in Fonts

| Font    | Preview                                        |
| :------ | :--------------------------------------------- |
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

---

## 3. Installation

### 3.1. Install via pip

```bash
pip install easy-captcha-python
```

### 3.2. Install from source

```bash
git clone https://github.com/yourusername/easy-captcha-python.git
cd easy-captcha-python
pip install -e .
```

---

## 4. Quick Start

### 4.1. Basic Usage

```python
from easy_captcha import SpecCaptcha
from io import BytesIO

# Create a captcha instance (width=130, height=48, length=5)
captcha = SpecCaptcha(130, 48, 5)

# Get captcha text
code = captcha.text()
print(f"Captcha code: {code}")

# Output to file
with open('captcha.png', 'wb') as f:
    stream = BytesIO()
    captcha.out(stream)
    f.write(stream.getvalue())

# Or get base64 encoded string
base64_str = captcha.to_base64()
print(f"Base64: {base64_str}")
```

### 4.2. Flask Integration

```python
from flask import Flask, make_response
from easy_captcha import SpecCaptcha
from io import BytesIO

app = Flask(__name__)

@app.route('/captcha')
def captcha():
    cap = SpecCaptcha(130, 48, 5)
    code = cap.text()

    # Store code in session
    # session['captcha'] = code.lower()

    stream = BytesIO()
    cap.out(stream)

    resp = make_response(stream.getvalue())
    resp.headers['Content-Type'] = 'image/png'
    return resp

if __name__ == '__main__':
    app.run(debug=True)
```

### 4.3. Django Integration

```python
from django.http import HttpResponse
from easy_captcha import SpecCaptcha
from io import BytesIO

def captcha(request):
    cap = SpecCaptcha(130, 48, 5)
    code = cap.text()

    # Store code in session
    # request.session['captcha'] = code.lower()

    stream = BytesIO()
    cap.out(stream)

    return HttpResponse(stream.getvalue(), content_type='image/png')
```

### 4.4. FastAPI Integration

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

### 4.5. Frontend-Backend Separation

For frontend-backend separation projects, it's recommended to use base64 encoding:

```python
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)
# Using dict for demo, Redis recommended for production
captcha_store = {}

@app.route('/captcha')
def get_captcha():
    from easy_captcha import SpecCaptcha

    cap = SpecCaptcha(130, 48, 5)
    code = cap.text().lower()
    key = str(uuid.uuid4())

    # Store captcha (use Redis with expiration in production)
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
        # Verification successful, remove it
        captcha_store.pop(ver_key, None)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid captcha'})
```

Frontend example:

```html
<img id="verImg" width="130px" height="48px" />

<script>
    var verKey;
    // Get captcha
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

## 5. Advanced Usage

### 5.1. Captcha Types

```python
from easy_captcha import (
    SpecCaptcha, GifCaptcha, ChineseCaptcha,
    ChineseGifCaptcha, ArithmeticCaptcha
)

# PNG captcha
captcha = SpecCaptcha(130, 48, 5)
code = captcha.text()

# GIF captcha
captcha = GifCaptcha(130, 48, 5)

# Chinese captcha
captcha = ChineseCaptcha(130, 48, 4)

# Chinese GIF captcha
captcha = ChineseGifCaptcha(130, 48, 4)

# Arithmetic captcha
captcha = ArithmeticCaptcha(130, 48, 2)
captcha.len = 3  # Number of operands (default is 2)
formula = captcha.get_arithmetic_string()  # Get formula: "3+2=?"
result = captcha.text()  # Get result: "5"

# Output captcha
from io import BytesIO
stream = BytesIO()
captcha.out(stream)
```

> **Note:**
> For arithmetic captcha, `len` represents the number of operands, while for other captchas it represents the number of characters.
> The `text()` method returns the calculation result, not the formula. You should store the result in the session, not the formula.

### 5.2. Character Types

| Type               | Description                   |
| :----------------- | :---------------------------- |
| TYPE_DEFAULT       | Mixed numbers and letters     |
| TYPE_ONLY_NUMBER   | Numbers only                  |
| TYPE_ONLY_CHAR     | Letters only                  |
| TYPE_ONLY_UPPER    | Uppercase letters only        |
| TYPE_ONLY_LOWER    | Lowercase letters only        |
| TYPE_NUM_AND_UPPER | Numbers and uppercase letters |

Usage:

```python
from easy_captcha import SpecCaptcha, TYPE_ONLY_NUMBER

captcha = SpecCaptcha(130, 48, 5)
captcha.char_type = TYPE_ONLY_NUMBER
```

> Only effective for `SpecCaptcha` and `GifCaptcha`.

### 5.3. Font Settings

Usage:

```python
from easy_captcha import SpecCaptcha, FONT_1, FONT_2

captcha = SpecCaptcha(130, 48, 5)

# Set built-in font
captcha.set_font(FONT_1, size=32)

# Or use system fonts (requires PIL.ImageFont support)
from PIL import ImageFont
captcha._font = ImageFont.truetype("arial.ttf", 32)
```

### 5.4. Base64 Output

```python
from easy_captcha import SpecCaptcha

captcha = SpecCaptcha(130, 48, 5)
base64_str = captcha.to_base64()

# Without base64 header (data:image/png;base64,)
base64_str = captcha.to_base64("")  # Pass empty string
```

### 5.5. File Output

```python
from easy_captcha import SpecCaptcha
from io import BytesIO

captcha = SpecCaptcha(130, 48, 5)

# Output to file
with open('captcha.png', 'wb') as f:
    stream = BytesIO()
    captcha.out(stream)
    f.write(stream.getvalue())
```

---

## 6. Examples

Check the `examples/` directory for more examples:

-   `basic_usage.py` - Basic usage examples
-   `all_types_demo.py` - All captcha types demonstration

Run examples:

```bash
# Run basic example
python examples/basic_usage.py

# Run full demonstration
python examples/all_types_demo.py
```

All generated captcha images will be saved to the `./out/` directory.

---

## 7. Testing

```bash
# Run SpecCaptcha tests
python tests/test_spec_captcha.py

# Run all captcha type tests
python tests/test_all_captcha.py

# Run package verification
python verify_package.py
```

---

## 8. API Reference

### Captcha Classes

All captcha classes share the following common methods:

#### `__init__(width, height, length)`

Create a captcha instance.

-   `width`: Image width (default: 130)
-   `height`: Image height (default: 48)
-   `length`: Number of characters (default: 5)

#### `text()`

Get the captcha text (for arithmetic captcha, returns the calculation result).

#### `text_char()`

Get the captcha text as a character array.

#### `out(stream)`

Output the captcha image to a stream.

-   `stream`: BytesIO or file stream

#### `to_base64(prefix)`

Get the base64 encoded string.

-   `prefix`: Base64 prefix (default: "data:image/png;base64," or "data:image/gif;base64,")

#### `set_font(font_index, size)`

Set the font.

-   `font_index`: Font index (FONT_1 to FONT_10)
-   `size`: Font size (default: 32)

### ArithmeticCaptcha Specific Methods

#### `get_arithmetic_string()`

Get the arithmetic formula string (e.g., "3+2=?").

---

## 9. License

Apache License 2.0

---

## 10. Acknowledgments

This project is a Python implementation of [EasyCaptcha](https://github.com/whvcse/EasyCaptcha).

---

## 11. Contributing

Issues and Pull Requests are welcome!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/easy-captcha-python.git
cd easy-captcha-python

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/

# Run verification
python verify_package.py
```

---

## 12. FAQ

**Q: How to verify the captcha on the backend?**

A: Store the captcha text in the session and compare it with user input (case-insensitive):

```python
# Generate captcha
code = captcha.text().lower()
session['captcha'] = code

# Verify
user_input = request.form.get('captcha', '').lower()
if user_input == session.get('captcha'):
    # Verification successful
    session.pop('captcha')  # Remove after verification
```

**Q: How to refresh the captcha?**

A: Simply request the captcha endpoint again to get a new captcha.

**Q: Can I customize the interference lines and circles?**

A: Yes, you can override the `draw_line()` and `draw_oval()` methods in the captcha class.

**Q: Does it support custom character sets?**

A: Yes, you can modify the `ALPHA` array in the `Randoms` class or override the `_alphas()` method.

---

## 13. Changelog

### v1.0.0 (2024-01-01)

-   ✨ Initial release
-   ✅ Support for 5 captcha types
-   ✅ Support for 6 character types
-   ✅ 10 built-in fonts
-   ✅ Base64 encoding support
-   ✅ Web framework integration examples

---

## 14. Support

If you find this project helpful, please give it a ⭐️!

For issues and questions, please open an issue on GitHub.
