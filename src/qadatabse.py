import re
from pathlib import Path

def parse_qa(text):
    # Регулярное выражение для поиска пар вопрос-ответ
    pattern = r'&startQ(.*?)&endQ\s*&startA(.*?)&startA'

    # Извлечение всех пар вопрос-ответ
    qa_pairs = re.findall(pattern, text, re.DOTALL)[0]

    return qa_pairs[0], qa_pairs[1]

class QADatabase:
    root = Path(__file__).parent.parent / "data"

    def get_random_answer(self):
        qa_file = self.root / "1.txt"
        content = qa_file.read_text()
        question, answer = parse_qa(content)
        return question, answer
    