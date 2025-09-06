from typing import List, Optional

from pymongo import MongoClient

from db.mongo_repository import QA_Repository


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
