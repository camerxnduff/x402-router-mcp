# x402 Router MCP server (stdio). Read-only: holds no keys, never pays.
# mcp-name: io.github.camerxnduff/x402-router
FROM python:3.12-slim

LABEL io.modelcontextprotocol.server.name="io.github.camerxnduff/x402-router" \
      org.opencontainers.image.source="https://github.com/camerxnduff/x402-router-mcp" \
      org.opencontainers.image.description="MCP server: search and route to 20k+ live x402 pay-per-call endpoints (Base, Solana, USDC)" \
      org.opencontainers.image.licenses="MIT"

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY mcp-server/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY mcp-server/server.py ./server.py

# Run as an unprivileged user
RUN useradd --create-home --uid 10001 mcp
USER mcp

# Default: stdio transport (what MCP clients and Glama expect).
# Streamable HTTP: docker run -p 8000:8000 -e HOST=0.0.0.0 IMAGE python server.py --http 8000
ENTRYPOINT ["python", "server.py"]
