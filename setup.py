"""
Setup script for Hathora Python SDK

For modern Python packaging, use pyproject.toml instead.
This setup.py is maintained for backwards compatibility.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="hathora",  # Package name on PyPI - install with: pip install hathora
    version="0.3.0",
    author="Hathora",
    author_email="support@hathora.com",
    description="Python SDK for Hathora Voice AI API - Speech-to-Text and Text-to-Speech",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hathora/yapp-sdk",
    project_urls={
        "Documentation": "https://github.com/hathora/yapp-sdk#readme",
        "Bug Tracker": "https://github.com/hathora/yapp-sdk/issues",
        "Source Code": "https://github.com/hathora/yapp-sdk",
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

