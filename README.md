# PERT-MCP
An LLM-based application to design and maintain PERT charts using LLM interfaces to support effective project management

## Getting Started

1. Copy `sample.env` to a `.env` environment variables file:
    ```bash
    cp sample.env .env
    ```
    Add your own environment variables.

2. Copy pre-commit hooks to .git folder:
    ```bash
    cp hooks/pre-commit .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    ```

3. To allow the application to perform read/write operations to local disk (via mounts shown in `compose.yaml`), you should update the `UID` and `GID` variables in the .env file to be those of your local machine's development user.
    ```bash
    # Linux
    uid=$(id -u); gid=$(id -g); sed -i -e "s/UID=.*/UID=${uid}/g" -e "s/GID=.*/GID=${gid}/g" .env

    # MacOS
    uid=$(id -u); gid=$(id -g); sed -i '' -e "s/UID=.*/UID=${uid}/g" -e "s/GID=.*/GID=${gid}/g" .env
    ```

4. Run the app:
    ```bash
    docker compose up --build
    ```

### Pre-commit hooks
This hook runs code checks. To skip it, use the `--no-verify` flag when committing.