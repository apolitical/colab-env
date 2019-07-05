# __init__.py

__version__ = "0.1.1"

from colab_env.handler import ColabEnvHandler

envvar_handler = ColabEnvHandler()


def RELOAD():
    """
    RELOAD - reload the environment variable handler, envvar_handler
    """
    global envvar_handler
    envvar_handler = ColabEnvHandler()
