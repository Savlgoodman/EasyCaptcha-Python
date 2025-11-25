from setuptools import setup, find_packages

setup(
    name="easy-captcha",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Pillow>=9.0.0",
    ],
    package_data={
        'easy_captcha': ['fonts/*.ttf'],
    },
    python_requires='>=3.7',
)

