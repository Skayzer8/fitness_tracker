##Модуль фитнес-трекера
----------

###ТЗ

Задача — разработать программный модуль фитнес-трекера, который обрабатывает данные для трех видов тренировок: для бега, спортивной ходьбы и плавания.
Этот модуль принимает от блока датчиков информацию о прошедшей тренировке, определяет вид тренировки, рассчитывает результаты тренировки,выводит информационное сообщение о результатах тренировки.

----------

###Информационное сообщение должно включать такую информацию:

 - тип тренировки (бег, ходьба или плавание);
 - длительность тренировки
 - дистанция, которую преодолел пользователь, в километрах;
 - среднюю скорость на дистанции, в км/ч;
 - расход энергии, в килокалориях.

----------

###Структура программы

Каждый вид спортивной активности в модуле должен быть описан соответствующим классом:

 - Бег → class Running;
 - Спортивная ходьба → class SportsWalking;
 - Плавание → class Swimming.

Конструктор каждого из классов должен получать информацию с датчиков:

 - action, тип int — количество совершённых действий (число шагов при ходьбе и беге либо гребков — при плавании);
 - duration, тип float — длительность тренировки;
 - weight, тип float — вес спортсмена.
