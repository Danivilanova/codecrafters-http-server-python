# Build Your Own HTTP Server Challenge

[![progress-banner](https://backend.codecrafters.io/progress/http-server/316cd5f8-08b1-4958-9f6e-d3035930780d)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This repository is a Python-based solution to the ["Build Your Own HTTP Server" Challenge](https://app.codecrafters.io/courses/http-server/overview) on CodeCrafters. The goal is to build a multi-client HTTP/1.1 server using Python.

## Getting Started

### Prerequisites

- Python 3.11

### How to Run the Server

1. **Clone this repository**: `git clone https://github.com/Danivilanova/codecrafters-http-server-python.git`
2. **Navigate to the repository**: `cd codecrafters-http-server-python`
3. **Run the server**: `./your_server.sh`

## Features

- HTTP/1.1 Compliant Server
- Multi-threaded client handling
- Basic Routing
- File operations (Read & Write)
- Custom Echo & User-Agent endpoints

## Code Structure

- `main.py` serves as the entry point and contains the server loop and socket setup.
- The function `handle_client` is responsible for processing incoming client requests and sending appropriate responses.
- Utility functions like `read_file`, `write_file`, and `send_response` assist in reading/writing files and sending HTTP responses, respectively.
