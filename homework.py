class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ) -> None:
        self.training_type = training_type
        self.duration = '%.3f' % duration
        self.distance = '%.3f' % distance
        self.speed = '%.3f' % speed
        self.calories = '%.3f' % calories

    def get_message(self):
        message1 = f'Тип тренировки: {self.training_type}; '
        message2 = f'Длительность: {self.duration} ч.; '
        message3 = f'Дистанция: {self.distance} км; '
        message4 = f'Ср. скорость: {self.speed} км/ч; '
        message5 = f'Потрачено ккал: {self.calories}.'
        message = message1+message2+message3+message4+message5
        return message

class Training:

    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    M_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        pass

    def show_training_info(self) -> InfoMessage:
        training_info = InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())
        return training_info
      


class Running(Training):

    """Тренировка: бег."""
    coeff_calorie_1: float = 18
    coeff_calorie_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spend_calories_running = (self.coeff_calorie_1 * self.get_mean_speed() - self.coeff_calorie_2) * self.weight / self.M_IN_KM * self.duration * self.M_IN_H
        return spend_calories_running


class SportsWalking(Training):

    """Тренировка: спортивная ходьба."""
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: рост спортсмена
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spend_calories_sportwalking = (self.coeff_calorie_3 * self.weight + (self.get_mean_speed() ** 2 // self.height) * self.coeff_calorie_4 * self.weight) * self.duration * self.M_IN_H
        return spend_calories_sportwalking

class Swimming(Training):

    """Тренировка: плавание."""
    coeff_calorie_5: float = 1.1
    coeff_calorie_6: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новые функционии: длина бассена(м), количество переплываний
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.length_pool*self.count_pool/self.M_IN_KM/self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spend_calories_swimming = (self.get_mean_speed()+self.coeff_calorie_5)*self.coeff_calorie_6*self.weight
        return spend_calories_swimming


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict = {'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking}
    for key in dict:
        if key == workout_type:
            return dict[key](*data)



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

