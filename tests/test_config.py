import os, sys
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)


def test_env():
    # Find .env file
    env_conf = os.path.join(base_dir, ".env")
    load_dotenv(env_conf)

    # General Config
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    STATIC_FOLDER = os.getenv("STATIC_FOLDER")
    ADDR_TO_LOC_URL = os.getenv("ADDR_TO_LOC_URL")
    assert all(
        [
            FLASK_DEBUG == "1",
            STATIC_FOLDER == "static",
            ADDR_TO_LOC_URL == "https://apis.map.qq.com/ws/geocoder/v1/?",
        ]
    )
