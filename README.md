# Парсер сайта - https://studarium.ru/

Данный Python скрипт позволяет получить все задания по темам с сайта https://studarium.ru/ в excel файл.

## Как пользоваться скриптом:

1) Клонируем репозиторий
```chatinput
git clone git@github.com:Krokky4/studarium_parser.git
```
2) Создаём venv и устанавливаем зависимости из requirements.txt
```chatinput
python -m venv venv
pip install -r requirements.txt
```
3) Запускаем скрипт
```chatinput
python parser.py
```

В рабочей директории появляется tasks.xlsx - это файл со всеми задачами с сайта.
Скрипт работает для задач по информатике, вы можете поменять желаемую тему при помощи ссылке в коде.

https://studarium.ru/working/11/{theme_counter}/page-{page_counter} - 11 в данной ссылке - это "информатика"
на сайте, подставив значение нужной темы, вы сможете спарсить её задания.