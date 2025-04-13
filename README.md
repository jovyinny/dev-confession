# Dev Confession

This is fun project, after lost some interest in coding, simply thought of random ideas on stuffs that i should get at least to understand.

## Set Up

- Create Virtual Env
  Why virtual environment? simply isolate project dependencies. You can read more about this after
  Depending on your OS you can get the way around how to create and activate virual Env. All the commands related to virtual env here will be Unix specific.

    ```bash
    python3.11 -m venv .venv
    ```

  I had to specify the version of python as i have more than 3 version of python and would like to user 3.11 [previously used to go with 3.10]

  - Activate the virtual environment

    ```bash
    source .venv/bin/Activate
    ```

    After activating, i always want to confirm the path of python used. I do simply run the command below after activating the environment.

    ```bash
    which python
    ```

- Install requirements.
