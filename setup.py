from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="amazon-product-video-fetcher",
    version="0.0.4",  # bump version
    author="Liran Bratt",
    author_email="brattlirannin@gmail.com",
    description="A small tool to extract and download m3u8 videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LiranBratt2121/amazon-product-video-fetcher",
    packages=find_packages(),  # finds 'amazon_product_video_fetcher' and 'core' inside it
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
