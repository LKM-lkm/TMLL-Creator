from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ttml-generator",
    version="1.0.0",
    author="TTML Generator Team",
    author_email="your-email@example.com",
    description="专业的TTML歌词生成器，支持多角色标记、时间戳标注和格式转换",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/ttml-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
        "audio": [
            "librosa>=0.9.0",
            "soundfile>=0.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ttml-generator=ttml_generator.main:main",
            "ttml-gui=run_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ttml_generator": [
            "templates/*.j2",
            "templates/*.xml",
        ],
    },
    keywords="ttml lyrics music audio subtitle karaoke",
    project_urls={
        "Bug Reports": "https://github.com/your-username/ttml-generator/issues",
        "Source": "https://github.com/your-username/ttml-generator",
        "Documentation": "https://github.com/your-username/ttml-generator#readme",
    },
)