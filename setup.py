from setuptools import setup, find_packages

setup(
    name="pieces_copilot_sdk",
    version="0.2.0",
    author="Mason Williams",
    author_email="mason@pieces.app",
    description="A Pieces OS SDK wrapper that allows anyone to easily create a Pieces Copilot experience with minimal code.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/mason-at-pieces/pieces-copilot-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
