class WorkoutTypeError(Exception):
    """Тип тренеровки не поддерживается."""

    def __init__(self, *args):
        self.message = args[0] if args else None
    def __str__(self):
        if self.message:
            return f"Ошибка: {self.message}"
        else:
            return f"Ошибка: Тип тренеровки не поддерживается."
