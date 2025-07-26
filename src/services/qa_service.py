from typing import List, Optional

from pymongo import MongoClient


class QA_Service:
    def __init__(self):
        self.client = QA_Repository()

    def get_random_question(self):
        """Возвращает вопрос"""
        qa = self.client.get_random_qa()
        return qa["question"]

    def get_answer_by_question(): ...

    def add_qa_pair(): ...


qa_schema = {
    "type": "object",
    "properties": {"_id": {}, "question": {"type": "string"}, "answer": {"type": "string"}},
    "required": ["question", "answer"],
    "additionalProperties": False,
}


# TODO: Вынести в отдельный класс
class QA_Repository:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")  # TODO: вынести в конфиг
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
        random_qa = self.collection.aggregate(pipeline)

        if random_qa is None:
            raise ValueError("Не удалось получить вопрос-ответ")

        return next(random_qa)

    def find_by_id(self, question_id: int) -> Optional[dict]:
        pass

    def save(self, question_data: dict) -> None:
        # ??? Нужна ли тут обработка или она нужна выше
        self.collection.insert_one(question_data)

    def update(self, question_id: int, updated_data: dict) -> bool:
        pass

    def delete(self, question_id: int) -> bool:
        pass

    def list_all_questions(self) -> List[dict]:
        pass
