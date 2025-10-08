import json
import os
from typing import Any, Callable

from loguru import logger


def get_env_variable(
    var_name: str, cast_as: Callable = str, default=None, as_list: bool = False
) -> Any:
    """
    Retrieve an environment variable and cast it to a specified type.
    If the variable contains a comma, or as_list is True, it will be returned as a list of the specified type.
    """

    try:
        value = os.environ[var_name]
    except KeyError:
        if default is not None:
            logger.info(
                f"Environment variable '{var_name}' not found. Using default value."
            )
            return default
        raise EnvironmentError(
            f"Environment variable '{var_name}' not found and no default value provided."
        )
    try:
        if value.startswith("{"):
            logger.info("Parsing JSON string from environment variable.")
            return json.loads(value)
        if "," in value or as_list:
            logger.info("Parsing list from environment variable.")
            return [cast_as(item.strip()) for item in value.split(",")]
        if cast_as is bool:
            return value.lower() in ("true", "1", "t", "y", "yes")
        return cast_as(value)
    except ValueError as e:
        logger.error(f"Error casting environment variable '{var_name}': {e}")
        raise ValueError(
            f"Could not cast environment variable '{var_name}' to {cast_as}: {e}"
        )
