# Foodgram
Foodgram - продуктовый помощник, онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд

<details>
   <summary>Исходные данные</summary> 
  
- бэкенд на Django;
- техническое описание проекта;
- Redoc спецификация API;

</details>

<details>
   <summary>Что было сделано</summary> 
  
- [составлена тестовая документация по API функционалу(тест-кейсы и чек-листы);](tests/Foodgram%20тестовая%20документация.xlsx)
- [написаны автотесты на Python по составленным тест-кейсам;](tests/test_api/test)
- подключен и настроен Allure с комментариями для каждого шага в тест-кейсе;

</details>



<details>
   <summary>Запуск проекта локально</summary> 

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:waitmon/foodgram-project.git
```

```
cd foodgram-project/
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

Загрузить имеющуюся базу данных для работы проекта:

```
python manage.py import_json
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Перейти в папку backend/

```
cd backend/
```

Обновить менеджер пакетов pip

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Запустить тесты:

```
cd ../tests/test_api/test
```

```
pytest -s -v
```

### Получить документацию:
- перейти в папку infra/

```
cd ../infra/
```

- выполнить команду:

```
docker-compose up
```

- документация и примеры запросов будут досупны по адресу:

```
http://localhost/api/docs/redoc.html
```
</details>


<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/pytest/pytest-original-wordmark.svg" title="Pytest" alt="Pytest" width="40" height="40"/>&nbsp;

</div>

