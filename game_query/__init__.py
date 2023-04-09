import os

try:
    from json_environ import Environ

    env_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "env.json"
    )
    env = Environ(path=env_path)
except (FileNotFoundError, ModuleNotFoundError):
    try:
        from dotenv import load_dotenv

        load_dotenv(".env")
        env = os.getenv
    except ModuleNotFoundError:
        env = os.getenv
