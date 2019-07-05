colab-env
=========

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Outline
-------

This Python package handles environment variables in [Google Colab](https://research.google.com/colaboratory/faq.html). Environment variables are an important infrastructure component e.g. containing secrets such as API keys that ought not to be included directly in the codebase. At the time of writing, however, Google Colab does not have built-in support for environment variables.

Our solution is to use the [python-dotenv](https://pypi.org/project/python-dotenv/) package in concert with Colab's built in authorisation tool for Google Drive. The package will attempt to

1. mount Google Drive locally
2. load environment variables from a file called `vars.env`

Usage
-----

To load environment variables using `colab-env` you should include the following code at the top of your Colab notebook:

```
!pip install colab-env -qU
import colab_env
```

This will usually open the `google.colab.drive.mount` authentication flow. We use this authentication step to protect any secrets in `vars.env`.

**Remember not to expose these secrets in the outputs of any cells!**

When the authentication challenge is passed, the environment variables will either be loaded into the Google Colab environment, or `vars.env` will be created in your Google Drive.

To modify environment variables using `colab-env` you should do the following:

```
!pip install colab-env -qU
from colab_env import envvar_handler
```

... and then use `envvar_handler`'s `add_env` and `del_env` methods to add/modify and delete environment variables respectively from `vars.env`.

Contributors
------------

Paddy Alton (paddy.alton@apolitical.co)

(with thanks to the [Apolitical](https://apolitical.co) engineering team for assistance and review)
