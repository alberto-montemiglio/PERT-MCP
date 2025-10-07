FROM python:3.13-slim-bookworm

# Avoid writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure stdout and stderr are unbuffered
ENV PYTHONUNBUFFERED=1

# Update system dependencies
RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv and uvx from the specified image
COPY --from=ghcr.io/astral-sh/uv:0.8.24 /uv /uvx /bin/

# Create a non-root user and switch to it
ARG UID
ARG GID
RUN groupadd -g ${GID} nonroot && \
    useradd -u ${UID} -g nonroot -m nonroot
USER nonroot

# Set working directory
WORKDIR /home/nonroot/app/src

# Copy and install Python dependencies using uv
COPY --chown=nonroot:nonroot ./pyproject.toml ../pyproject.toml
COPY --chown=nonroot:nonroot ./uv.lock ../uv.lock
RUN uv sync --frozen

# Copy application source code, overwriting previous documents (pyproject.toml, uv.lock)
COPY --chown=nonroot:nonroot src/ src/

# Set working directory to the application source code
WORKDIR /home/nonroot/app/src

# Run the application with auto-reload for development
CMD [ "uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
