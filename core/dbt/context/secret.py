import os
from typing import Any, Dict, Optional

from dbt.contracts.connection import HasCredentials

from .base import (
    BaseContext, contextproperty, contextmember
)

from dbt.exceptions import raise_parsing_error


class SecretContext(BaseContext):
    # the only thing this does is reimplement env_var to return actual secret values

    @contextmember
    def env_var(self, var: str, default: Optional[str] = None) -> str:
        """The env_var() function. Return the environment variable named 'var'.
        If there is no such environment variable set, return the default.

        If the default is None, raise an exception for an undefined variable.
        """
        return_value = None
        if var in os.environ:
            return_value = os.environ[var]
        elif default is not None:
            return_value = default

        if return_value is not None:
            self.env_vars[var] = return_value
            return return_value
        else:
            msg = f"Env var required but not provided: '{var}'"
            raise_parsing_error(msg)


def generate_secret_context(cli_vars: Dict[str, Any]) -> Dict[str, Any]:
    ctx = SecretContext(cli_vars)
    # This is not a Mashumaro to_dict call
    return ctx.to_dict()
