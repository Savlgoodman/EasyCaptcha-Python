# 安装和发布指南

## 📦 本地安装测试

### 方法1：开发模式安装（推荐用于开发）

```bash
# 在项目根目录执行
pip install -e .
```

这会以可编辑模式安装包，修改代码后无需重新安装。

### 方法2：直接安装

```bash
pip install .
```

### 验证安装

```python
# 测试导入
python -c "from easy_captcha import SpecCaptcha; print('安装成功！')"

# 快速测试
python examples/basic_usage.py
```

---

## 🚀 发布到PyPI

### 前置准备

1. 安装构建工具：
```bash
pip install build twine
```

2. 注册PyPI账号：
   - 正式环境: https://pypi.org/account/register/
   - 测试环境: https://test.pypi.org/account/register/

3. 配置API Token（推荐）：
   - 在PyPI账户设置中生成API Token
   - 创建 `~/.pypirc` 文件：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # 你的API Token

[testpypi]
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZw...  # 测试环境的API Token
```

### 构建包

```bash
# 清理旧的构建文件
rm -rf dist/ build/ *.egg-info

# 构建源码包和wheel包
python -m build
```

这会在 `dist/` 目录生成：
- `easy-captcha-python-1.0.0.tar.gz` (源码包)
- `easy_captcha_python-1.0.0-py3-none-any.whl` (wheel包)

### 发布到TestPyPI（测试）

```bash
# 上传到测试环境
twine upload --repository testpypi dist/*

# 从测试环境安装验证
pip install --index-url https://test.pypi.org/simple/ easy-captcha-python
```

### 发布到正式PyPI

```bash
# 上传到正式PyPI
twine upload dist/*

# 安装验证
pip install easy-captcha-python
```

---

## 🔄 版本更新流程

1. 更新版本号：
   - 修改 `pyproject.toml` 中的 `version`
   - 修改 `setup.py` 中的 `version`
   - 修改 `easy_captcha/__init__.py` 中的 `__version__`

2. 更新CHANGELOG（如果有）

3. 提交代码：
```bash
git add .
git commit -m "Release v1.0.1"
git tag v1.0.1
git push origin main --tags
```

4. 重新构建和发布：
```bash
rm -rf dist/
python -m build
twine upload dist/*
```

---

## 📋 发布检查清单

发布前确认：

- [ ] 所有测试通过
- [ ] README.md 完整且准确
- [ ] 版本号已更新
- [ ] LICENSE 文件存在
- [ ] 依赖项正确配置
- [ ] 字体文件包含在包中（检查MANIFEST.in）
- [ ] 在本地测试安装成功
- [ ] 在TestPyPI测试成功

---

## 🛠️ 常见问题

### Q: 上传时提示文件已存在？
A: PyPI不允许覆盖已发布的版本，需要更新版本号。

### Q: 安装后找不到字体文件？
A: 确保 `MANIFEST.in` 包含字体文件，并且 `setup.py` 中配置了 `package_data`。

### Q: 如何撤回已发布的版本？
A: PyPI不支持删除已发布的版本，只能发布新版本修复问题。

### Q: 如何查看包的详细信息？
```bash
pip show easy-captcha-python
```

---

## 📚 参考资源

- [Python打包用户指南](https://packaging.python.org/)
- [PyPI官方文档](https://pypi.org/help/)
- [Twine文档](https://twine.readthedocs.io/)

