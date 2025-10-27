"""
Setup script for Yapp Python SDK

For modern Python packaging, use pyproject.toml instead.
This setup.py is maintained for backwards compatibility.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="yapp",  # Changed from "yapp-sdk" to just "yapp" for pip install yapp
    version="0.2.0",
    author="Yapp",
    author_email="support@yapp.ai",
    description="Python SDK for Yapp Voice AI API - Speech-to-Text and Text-to-Speech",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yapp-sdk",
    project_urls={
        "Documentation": "https://github.com/yourusername/yapp-sdk#readme",
        "Bug Tracker": "https://github.com/yourusername/yapp-sdk/issues",
        "Source Code": "https://github.com/yourusername/yapp-sdk",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "typing-extensions>=4.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "mypy>=1.0",
            "ruff>=0.1.0",
        ],
    },
    keywords=[
        "voice",
        "ai",
        "speech-to-text",
        "text-to-speech",
        "tts",
        "stt",
        "audio",
        "speech-recognition",
        "voice-cloning",
    ],
    include_package_data=True,
    zip_safe=False,
)

