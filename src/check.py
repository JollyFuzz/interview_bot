class Auth:
    def __init__(self, allowed_users=None):
        """
        :param allowed_users: Словарь с разрешёнными пользователями
            Например: {'user_ids': [123, 456], 'usernames': ['alice', 'bob']}
        """
        self.allowed_users = allowed_users or ["jolly_fuzz"]
        self.qa_pairs = []  # Здесь будут храниться вопросы и ответы после загрузки

    def is_user_authorized(self, username=None):
        """
        Проверяет, является ли пользователь авторизованным
        """
        if username and username.lower() in self.allowed_users:
            return True
        return False