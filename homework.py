from dataclasses import dataclass

from exceptions import WorkoutTypeError


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return (self.MESSAGE.format(training_type=self.training_type,
                                    duration=self.duration,
                                    distance=self.distance,
                                    speed=self.speed,
                                    calories=self.calories)
                )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUNNING_CALORIE_COEFF_1: int = 18
    RUNNING_CALORIE_COEFF_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.RUNNING_CALORIE_COEFF_1 * self.get_mean_speed()
                - self.RUNNING_CALORIE_COEFF_2) * self.weight / self.M_IN_KM
                * (self.duration * 60))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: int

    SPORT_WALKING_CALORIE_COEFF_1: float = 0.035
    SPORT_WALKING_CALORIE_COEFF_2: float = 0.029

    def get_spent_calories(self) -> float:
        return ((self.SPORT_WALKING_CALORIE_COEFF_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.SPORT_WALKING_CALORIE_COEFF_2 * self.weight)
                * (self.duration * 60))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int

    LEN_STEP = 1.38
    SWIMMING_CALORIE_COEFF_1: float = 1.1
    SWIMMING_CALORIE_COEFF_2: int = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.SWIMMING_CALORIE_COEFF_1)
                * self.SWIMMING_CALORIE_COEFF_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    
    if workout_type not in list(training_dict):
        raise WorkoutTypeError('Неизвестный тип тренеровки.')
    
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
