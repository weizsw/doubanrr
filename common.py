import json
import os


def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"The environment variable {var_name} is not set.")
    try:
        # Try to parse the value as JSON
        value = json.loads(value)
    except json.JSONDecodeError:
        # If it's not a valid JSON string, just return the original string
        pass

    return value


def is_wanna_watch(title):
    return title.startswith("想看")
