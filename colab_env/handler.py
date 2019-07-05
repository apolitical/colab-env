try:
    from google.colab import drive
except ImportError:
    raise ImportError("colab-env only works in a Google Colab notebook")

import os

from dotenv import load_dotenv


class ColabEnvHandler:

    """
    ColabEnvHandler

    This class is used to administer the use of environment variables
    in Google Colab using the user's Google Drive vars.env file

    When initialised, the google.colab.drive.mount authentication flow
    is used. We rely on this to protect the secrets held in vars.env so
    be sure not to expose them in any cell outputs.

    """

    envpath = "/content/gdrive/My Drive/vars.env"

    def __init__(self, force_remount=False):

        """ 
        __init__ for ColabEnvHandler 
        
        This may open the authentication flow for Google Drive.

        KEYWORDS:
            force_remount = False - passed to drive.mount
        
        """

        drive.mount("/content/gdrive", force_remount=force_remount)

        if os.path.isfile(self.envpath):
            self.envload()
        else:
            self.create_vars_dot_env()

    def envload(self):

        """
        envload

        This method simply calls dotenv.load_dotenv on the
        stand filepath to vars.env

        OUTPUTS:
            check - result of load_dotenv(self.envpath)

        """

        check = load_dotenv(self.envpath, override=True)

        return check

    def create_vars_dot_env(self):

        """
        create_vars_dot_env

        This method is invoked if the vars.env file is not found.

        It will create the file.
        
        """

        print("Creating vars.env in your Google Drive!")

        with open(self.envpath, "w") as envfile:
            envfile.write("COLAB_ENV = Active\n")

    @staticmethod
    def __kv_pair(line):

        """
        __kv_pair

        Breaks down a character string around the first '=' sign,
        returns a key, value tuple.
        
        If the breakdown fails, returns (None, None).

        INPUTS:
            line - character string

        OUTPUTS:
            key, value

        """

        splitline = line.split("=")

        if len(splitline) <= 1:
            return None, None

        key = splitline[0].strip()

        val = "=".join(splitline[1:]).strip()

        return key, val

    def add_env(self, envname, envval, overwrite=False):

        """
        add_env

        This method adds a new environment key:value pair to vars.env

        INPUTS:
            envname - name of the environment variable
                      (usual convention: capitalised string)
            envval  - corresponding value of the environment variable

        KEYWORDS:
            overwrite = False - default is to not overwrite 

        """

        with open(self.envpath, "r") as envfile:
            my_vars = {}
            for line in envfile.readlines():
                key, value = self.__kv_pair(line)
                if key is not None:
                    my_vars[key] = value

        current_value = my_vars.get(envname)

        if (current_value is None) or overwrite:
            my_vars[envname] = envval
        else:
            return  # if overwrite = False and current_value is not None

        new_lines = [f"{k} = {v}\n" for k, v in my_vars.items()]

        with open(self.envpath, "w") as envfile:
            envfile.writelines(new_lines)

        os.environ[envname] = envval

    def del_env(self, envname):

        """
        del_env

        This method deletes an environment variable from vars.env

        Does nothing if the environment variable doesn't exist.

        INPUTS:
            envname - name of variable to delete

        """

        with open(self.envpath, "r") as envfile:
            my_vars = {}
            for line in envfile.readlines():
                key, value = self.__kv_pair(line)
                if key is not None:
                    my_vars[key] = value

        current_value = my_vars.pop(envname)

        if current_value is None:
            return  # do nothing if not set

        new_lines = [f"{k} = {v}\n" for k, v in my_vars.items()]

        with open(self.envpath, "w") as envfile:
            envfile.writelines(new_lines)

        os.environ.unsetenv(envname)
