from setuptools import setup, find_packages

setup(
    name="geoip",
    version="0.1.0",
    author="Pavel Safonov",
    author_email="safonovpavel97@gmail.com",
    description="A library to get geoip info for ip address",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/psafonov7/geoip",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your dependencies here
        # 'requests>=2.25.0',
    ],
)
