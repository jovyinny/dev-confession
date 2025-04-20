# Dev Confession

This is fun project, after lost some interest in coding, simply thought of random ideas on stuffs that i should get at least to understand. Just post some random dev confession and get some fun out of it. I am not a pro developer, but i am trying to learn and improve my skills.

Hoping to get some hands on experience on some of the following:

- Websockets

Maybe later rewrite the same using another langauge as i do explore some other languages like Go, and Elixir.

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

  After activating the virtual environment, you can install the requirements using pip.

    ```bash
    pip install -r requirements.txt
    ```

  This will install all the dependencies listed in the `requirements.txt` file.

- Run the project
  After installing the requirements, you can run the project using the command below.

    ```bash
    python app.py
    ```

## Features

- [x] Random confession
- [ ] Random confession with image
- [ ] Create confession room for specific Topic eg database
- [ ] Join confession room

__It's a work in progress, weekend project.[I use Copilot with README edits]__
