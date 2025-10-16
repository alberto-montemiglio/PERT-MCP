# PERT-MCP
[![Python](https://img.shields.io/badge/python-v3.12-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

E, w, f, i, b, c4, up, -e203
## Overview
An LLM-based application to design and maintain PERT charts using LLM interfaces to support effective project management

### Running the App:

1. Copy `sample.env` to a `.env` environment variables file:
    ```bash
    cp sample.env .env
    ```
    Add your own environment variables.

2. Run the app:
    ```bash
    docker compose up --build
    ```

### Develop the App:

#### Pre-commit hooks
Some pre-commits hooks that run code checks with 'ruff' and 'mypy' are provided
To set them up with git, copy the pre-commit file containing the hooks to the .git folder:
```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```
To skip the pre-commit checks, use the `--no-verify` flag when committing:
```
git commit --no-verify
```
