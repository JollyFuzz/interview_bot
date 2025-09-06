import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.TG_TOKEN = os.getenv("TG_TOKEN")

        self.MONGO_HOST = os.getenv("MONGO_HOST")
        self.MONGO_PORT = os.getenv("MONGO_PORT")


cfg = Config()
