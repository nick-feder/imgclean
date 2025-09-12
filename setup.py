from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="imgclean",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A super easy tool to clean image datasets by removing duplicates, blurry images, and corrupted files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/imgclean",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Image Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=9.0.0",
        "numpy>=1.19.0",
        "opencv-python>=4.5.0",
        "imagehash>=4.2.0",
        "tqdm>=4.60.0",
    ],
    entry_points={
        "console_scripts": [
            "imgclean=imgclean.cli:main",
        ],
    },
)
