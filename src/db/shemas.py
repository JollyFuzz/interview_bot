# Схема базы вопросов-ответов
qa_schema = {
    "type": "object",
    "properties": {"_id": {}, "question": {"type": "string"}, "answer": {"type": "string"}},
    "required": ["question", "answer"],
    "additionalProperties": False,
}
