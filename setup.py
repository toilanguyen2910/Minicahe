from setuptools import setup, find_packages

setup(
    name="minicahe",
    version="0.1.0",
    description="Minicahe - Mini Token Optimizer: talk smart, use fewer tokens",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0",
        "tiktoken>=0.5.0",
    ],
    entry_points={
        "console_scripts": [
            "minicahe=minicahe.cli:main",
        ],
    },
    python_requires=">=3.9",
)
