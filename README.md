# Web application for managing the database of bonus cards

###### Веб-приложение для управления базой данных бонусных карт

Описание
========

Необходимо создать веб-приложение для управления базой данных бонусных карт

##### Функционал приложения:

> 1. Список карт с полями: серия, номер, дата выпуска, дата окончания
     активности, статус
> 2. Поиск по этим же полям
> 3. Просмотр профиля карты с историей покупок по ней
> 4. Активация/деактивация карты
> 5. Удаление карты

##### Список полей:

> - серия карты
> - номер карты
> - дата выпуска карты
> - дата окончания активности карты
> - дата использования
> - сумма
> - статус карты (не активирована/активирована/просрочена)

##### Требования

Реализовать генератор карт, с указанием серии и количества генерируемых карт, а
также "срок окончания активности" со значениями "1 год", "6 месяцев" "1 месяц".
После истечения срока активности карты, у карты проставляется статус"
просрочена".

Примечание: поля с датами должны содержать также и время.


Основные технологии
-------------------

```
* Python 3.11.1
* Django 4.1.4
* Postgresql 14.5
* Elasticsearch
```

```
* Docker
* Docker Compose
```

Установка и запуск
------------------

* Переходим в директорию проекта

```cd card_db```

* Создаем виртуальное окружение

```python3 -m venv venv```

* Активируем виртуальное окружение

```source venv/bin/activate```

* Создаем файл .env такой же, как .env.sample (меняем настройки при
  необходимости)

```touch .env```

* Устанавливаем зависимости

```pip install -r requirements.txt```


Запуск с помощью docker-compose
-------------------------------

###### Делаем файл docker_commands.sh исполняемым

```chmod +x docker_commands.sh```

##### Запуск

```docker-compose up -d --build```
