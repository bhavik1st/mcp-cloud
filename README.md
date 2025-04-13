# mcp-cloud
[![PyPI version](https://badge.fury.io/py/mcp-cloud.svg)](https://badge.fury.io/py/mcp-cloud)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Model Context Protocol Server for Public Cloud environments like AWS, Azure, and more.
mcp-cloud is a Python MCP server:
- Connects to public cloud to access resources like S3 Buckets, Azure Blobs
- Provides tools performing certain operations like CRUD on resources.

## Overview

mcp-cloud is a Python server implementation of the Model Context Protocol (MCP) designed specifically for public cloud environments. It enables AI models to seamlessly connect with various cloud resources and services.

# mcp-cloud
Model Context Protocol Server for Public Cloud
mcp-cloud is designed to run a MCP Server for Public Cloud like AWS, Azure etc.

# Mode Context Protocol

MCP Protocol for GenAI agents has been created by Anthropic.
MCP is an open protocol that standardizes how applications provide context to LLMs. 
Think of MCP like a USB-C port for AI applications. MCP provides a standardized way to connect AI models to different data sources and tools.
Refer Anthopic's [MCP Protocol Introduction](https://modelcontextprotocol.io/introduction).
Refer to the [MCP Quickstart Guide for Users](https://modelcontextprotocol.io/quickstart/user) to learn how to use MCP

# Concepts
MCP servers can provide three main types of capabilities:
Resources: File-like data that can be read by clients (like API responses or file contents)
Tools: Functions that can be called by the LLM (with user approval)
Prompts: Pre-written templates that help users accomplish specific tasks

Initial version of MCP Server will focus on resources available of Public Clouds e.g S3 Buckets, Azure for now.


# Features
0.1 
[x] Cloud Storage
[ ] Cloud Compute
    .. Coming Soon ..

# Steps to Install 
TODO: Update

# Steps to Use
TODO:   



