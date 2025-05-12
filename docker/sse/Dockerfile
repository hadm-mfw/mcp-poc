FROM python:3.12-slim

WORKDIR /app

# Copy requirements
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
RUN pip install --no-cache-dir uv
RUN uv venv
RUN uv pip install -e .

# Copy application code
COPY . .

# Expose port for the SSE server
EXPOSE 8000

# Set the host to 0.0.0.0 to make it accessible from outside the container
CMD ["uv", "run", "sse/main.py"] 
