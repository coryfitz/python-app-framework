from setuptools import setup, find_packages

setup(
    name="moderne",
    version="0.0.1",
    author="Cory Fitz",
    author_email="coryalanfitz@gmail.com",
    description="Moderne Web Framework",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/coryfitz/moderne",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'moderne.templates': ['*.html', '*.py', '*.png'],
    },
    entry_points={
        'console_scripts': [
            'moderne = moderne.cli:main',
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