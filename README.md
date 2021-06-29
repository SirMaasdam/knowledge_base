# Проект "База знаний"

## Используемый стек технологий:

- Django 3.2
- Redis (управление информацией о просмотрах статей)
- Celery (создание асинхронной отправка писем на почту через smtp google)
- JQuery (создание и редактирование контента статей)
- PostgreSQL

## Приватные данные
Отправка почты происходит при помощи **smtp.gmail.com**
Приветные данные подгружаются из переменной окружения при помощи библиотеки **python-dotenv**.
Необходимо создать файл **.env** и прописать в нем эти переменные окружения.

## Необходимые действия

Поиск статей на сайте происходит при помощи поиска по триграмному подобию (trigram similarity) PostgreSQL. Необходимо для базы данных проекта прописать:

```
CREATE EXTENSION pg_trgm;
```

Отправка почты происходит при помощи **smtp.gmail.com**, необходимо прописать данные в переменную окружения

