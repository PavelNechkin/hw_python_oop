from dataclasses import dataclass
from typing import List
Astrakhanets = List[float]


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Создать сообщение."""
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Калории можно посчитать '
                                    'только для Running, SportsWalking '
                                    'или Swimming')

    def show_training_info(self) -> InfoMessage:
        """Получить объект класса ссобщения."""
        args = (self.__class__.__name__,
                self.duration,
                self.get_distance(),
                self.get_mean_speed(),
                self.get_spent_calories())
        training_info = InfoMessage(*args)
        return training_info


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18.
    COEFF_CALORIE_2 = 20.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spend_calories_running = ((self.COEFF_CALORIE_1
                                  * self.get_mean_speed()
                                  - self.COEFF_CALORIE_2)
                                  * self.weight / self.M_IN_KM
                                  * self.duration
                                  * self.MIN_IN_HOUR)
        return spend_calories_running


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


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_CALORIE_5 = 1.1
    COEFF_CALORIE_6 = 2.
    LEN_STEP = 1.38

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool
                      * self.count_pool
                      / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spend_calories_swimming = ((self.get_mean_speed()
                                   + self.COEFF_CALORIE_5)
                                   * self.COEFF_CALORIE_6
                                   * self.weight)
        return spend_calories_swimming

dict = {'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}

def read_package(workout_type: str, data: Astrakhanets) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in dict:
        return dict[workout_type](*data)
    else:
        print('Попробуй другой тип тренировки')

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
