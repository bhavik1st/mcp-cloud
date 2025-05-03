from setuptools import setup, find_packages

setup(
    name="mcp_multi_cloud",
    version="0.1.0",
    description="MCP Server to interact with multiple clouds based on Anthropic's Model Context Protocol",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bhavik Shah",
    author_email="bhavik1st@gmail.com",
    url="https://github.com/bhavik1st/mcp_multi_cloud",
    packages=find_packages(include=["mcp_multi_cloud", "mcp_multi_cloud.*"]),
    package_dir={"mcp_multi_cloud": "mcp_multi_cloud"},
    python_requires=">=3.11",
    install_requires=[
        "httpx>=0.28.1",
        "mcp==1.6.0",
        "mcp[cli]>=1.6.0",
        "apache-libcloud>=3.8.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    entry_points={
        "console_scripts": [
            "mcp_multi_cloud=mcp_multi_cloud.main:main",
        ],
    },
) 