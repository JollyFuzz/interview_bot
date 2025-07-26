from services.qa_service import QA_Service


def get_question():
    qa_service = QA_Service()
    question = qa_service.get_random_question()
    return question
