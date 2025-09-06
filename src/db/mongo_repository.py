from typing import List, Optional

from pymongo import MongoClient

from config import cfg
from db.shemas import qa_schema


class QA_Repository:
    """
    Класс для работы с базой
    """

    def __init__(self):
        self.client = MongoClient(f"mongodb://{cfg.MONGO_HOST}:{cfg.MONGO_PORT}/")
        self.db = self.client["answer_question"]
        self.collection_name = "python"

        # TODO: узнать как это можно сделать иначе
        if self.collection_name not in self.db.list_collection_names():
            self.db.create_collection(self.collection_name, validator={"$jsonSchema": qa_schema})

        self.collection = self.db[self.collection_name]
        # TODO: переделать через синглтон(если нужно)

    def get_collection_size(self):
        """Возвращает длину коллекции"""
        return self.collection.count_documents({})

    def get_random_qa(self):
        pipeline = [{"$sample": {"size": 1}}]
        random_qa = list(self.collection.aggregate(pipeline))

        if not random_qa:
            raise ValueError("Не удалось получить вопрос-ответ")

        return random_qa[0]