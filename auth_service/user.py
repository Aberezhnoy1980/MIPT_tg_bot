class User:
    def __init__(self, telegram_id, name=None, email=None):
        self.telegram_id = telegram_id
        self.name = name
        self.email = email

    def __eq__(self, other):
        if isinstance(other, User):
            return (
                self.telegram_id == other.telegram_id
                and self.name == other.name
                and self.email == other.email
            )

    def __str__(self):
        return f'name: {self.name}, id: {self.telegram_id}, email: {self.email}'

    def __hash__(self):
        return hash((self.telegram_id, self.name, self.email))


