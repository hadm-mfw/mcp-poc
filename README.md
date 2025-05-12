# MCP POC (Model Context Protocol Proof of Concept)

This project demonstrates the use of Model Context Protocol (MCP) to interact with MoneyForward Cloud Expense API.

## Prerequisites

- Python 3.12 or higher
- MoneyForward Cloud Expense account with API access
- OAuth2.0 credentials (client ID and client secret)
- Docker and Docker Compose (for containerized deployment)

## Installation

1. Clone this repository
2. Download packages:
  ```bash
  pip install --no-cache-dir uv
  uv venv
  uv pip install -e .
  ```

3. Create `.env` file with required environment variables:
  ```bash
  CLIENT_ID=your_client_id
  CLIENT_SECRET=your_client_secret 
  IDP_URL=your_idp_url
  REDIRECT_URL=your_redirect_url
  ```

4. Start SSE Server:
  ```bash
  uv --directory /path/to/sse run main.py
  ```

5. Configure your MCP client to use the proxy server with:
  ```json
  {
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/proxy",
      "run",
      "main.py"
    ],
    "env": {
      "AUTH_CREDENTIALS": "/path/to/credentials.json",
      "MCP_SSE_SERVER": "http://localhost:8000"
    }
  }
  ```
  Note: Replace `/path/to/credentials.json` with the actual path to your credentials file.

## Running with Docker Compose

1. Build the proxy image:
  ```bash
  docker build -t mcp-proxy:latest -f docker/proxy/Dockerfile .
  ```

2. Create `.env` file with required environment variables:
  ```bash
  CLIENT_ID=your_client_id
  CLIENT_SECRET=your_client_secret 
  IDP_URL=your_idp_url
  REDIRECT_URL=your_redirect_url
  ```

3. Start the SSE server:
  ```bash
  docker compose up -d
  ```

4. Configure your MCP client to use the proxy server with:
  ```json
  {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "-e",
      "MCP_SSE_SERVER",
      "-e", 
      "AUTH_CREDENTIALS",
      "--volume",
      "/path/to/credentials.json:/app/credentials.json",
      "--network",
      "mcp-network",
      "mcp-proxy:latest",
      "uv",
      "--directory",
      "proxy",
      "run",
      "main.py"
    ],
    "env": {
      "MCP_SSE_SERVER": "http://sse-server:8000",
      "AUTH_CREDENTIALS": "/app/credentials.json"
    }
  }
  ```
  Note: Replace `/path/to/credentials.json` with the actual path to your credentials file.


## Available Tools

The project provides the following tools:

1. `fetch_office_list` - Fetches the list of offices/companies from MoneyForward Cloud Expense
2. `refresh_token` - Refreshes the OAuth access token using the refresh token

## Project Structure

- `core/` - Core functionality including tool definitions and handlers
- `stdio/` - STDIO server implementation
- `sse/` - Server-Sent Events implementation
- `proxy/` - Proxy server for remote mode
- `test/` - Test scripts for local and remote modes
- `docker/` - Docker configuration files

## License

[License information]
