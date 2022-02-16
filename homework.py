from dataclasses import dataclass
from typing import Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Создать сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000.
    MIN_IN_HOUR = 60.

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Калории можно посчитать '
                                  'только для Running, SportsWalking '
                                  'или Swimming')

    def show_training_info(self) -> InfoMessage:
        """Получить объект класса ссобщения."""
        kwargs = {'training_type': self.__class__.__name__,
                  'duration': self.duration,
                  'distance': self.get_distance(),
                  'speed': self.get_mean_speed(),
                  'calories': self.get_spent_calories()}
        return InfoMessage(**kwargs)


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18.
    COEFF_CALORIE_2 = 20.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM
                * self.duration
                * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_3 = 0.035
    COEFF_CALORIE_4 = 0.029

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        total_speed = (self.get_mean_speed() ** 2 // self.height)
        total_speed_at_weight = (total_speed
                                 * self.COEFF_CALORIE_4
                                 * self.weight)
        spend_calories_sportwalking = ((self.COEFF_CALORIE_3
                                       * self.weight
                                       + total_speed_at_weight)
                                       * self.duration
                                       * self.MIN_IN_HOUR)
        return spend_calories_sportwalking


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_CALORIE_5: float = 1.1
    COEFF_CALORIE_6: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.COEFF_CALORIE_5)
                * self.COEFF_CALORIE_6
                * self.weight)


DECODING_OF_ABBREVIATIONS: Dict[str, Training] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in DECODING_OF_ABBREVIATIONS.keys():
        return DECODING_OF_ABBREVIATIONS[workout_type](*data)
    else:
        return None


def main(training: Training) -> None:
    """Главная функция."""
    if training is None:
        print('Неизвестный вид тренировки')
    else:
        print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
