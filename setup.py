from setuptools import setup, find_packages
import tomllib 
with open('config.toml', 'rb') as f:
    config = tomllib.load(f)
FRAMEWORK_NAME = config['framework_name']
GITHUB_URL = config['github_url']


setup(
    name=FRAMEWORK_NAME.lower(),
    version="0.0.2",
    author="Cory Fitz",
    author_email="coryalanfitz@gmail.com",
    description=f"{FRAMEWORK_NAME} Web Framework",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    packages=find_packages(include=["moderne", "moderne.*"]),
    include_package_data=True,
    package_data={
        'framework.templates': ['*.html', '*.py', '*.png'],
        FRAMEWORK_NAME.lower(): ['config.toml']
    },
    entry_points={
        'console_scripts': [
            f'{FRAMEWORK_NAME.lower()} = framework.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "psx_syntax>=0.0.2",
        "starlette>=0.41.0",
        "uvicorn>=0.32.0",
    ],
)