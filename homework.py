""" Программа представляет собой программный модуль фитнес-трекера,
    который обрабатывает данные для трех видов тренировок:
    для бега, спортивной ходьбы и плавания."""
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    INF_MESSAGE = ('Тип тренировки: {training_type}; '
                   'Длительность: {duration:.3f} ч.; '
                   'Дистанция: {distance:.3f} км; '
                   'Ср. скорость: {speed:.3f} км/ч; '
                   'Потрачено ккал: {calories:.3f}.')

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывести информационное сообщение о результатах тренировки."""
        return self.INF_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки.
    Атрибуты:
        action, int — количество совершённых действий (число шагов, гребков);
        duration, float — длительность тренировки в часах;
        weight, float — вес спортсмена.
        LEN_STEP — расстояние, за один шаг или гребок в м.
        M_IN_KM — константа для перевода значений из метров в километры."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    DURATION_MIN: float = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Метод определения количества затраченных калорий'
            '(get_spent_calories) не определен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    COEF_CALORIE_1: float = 18
    COEF_CALORIE_2: float = 20
    """Тренировка: бег.
    Все свойства и методы класса без изменений наследуются от базового класса.
    За исключением метода расчёта калорий, который переопределен ниже."""

    def get_spent_calories(self) -> float:
        return ((self.COEF_CALORIE_1 * self.get_mean_speed()
                - self.COEF_CALORIE_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.DURATION_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба
    В конструкторе этого класса принимается дополнительный параметр:
        height — рост спортсмена."""

    COEF_CALORIE_1: float = 0.035
    COEF_CALORIE_2: float = 0.029
    COEF_CALORIE_3: float = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество калорий."""
        return ((self.COEF_CALORIE_1 * self.weight + (self.get_mean_speed()
                ** self.COEF_CALORIE_3 // self.height)
                * self.COEF_CALORIE_2 * self.weight) * self.duration
                * self.DURATION_MIN)


class Swimming(Training):
    """Тренировка: плавание.
    Кроме свойств базового класса, принимаются еще два параметра:
    length_pool — длина бассейна в метрах;
    count_pool — сколько раз пользователь переплыл бассейн.
    Переопределяются методы расчета калорий и скорости."""

    COEF_CALORIE_1: float = 1.1
    COEF_CALORIE_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в воде."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество калорий."""
        return((self.get_mean_speed() + self.COEF_CALORIE_1)
               * self.COEF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_data = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type in class_data:
        return class_data[workout_type](*data)
    else:
        raise TypeError('Вид активности не определен (Код ошибки: 1.02)')


def main(training: Training) -> None:
    """Главная функция."""
    message_train = training.show_training_info()
    print(message_train.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except (TypeError):
            print(
                'Упс! Что-то пошло не так!'
                'Обратитесь в службу поддержки (Код ошибки: 1.01)')
