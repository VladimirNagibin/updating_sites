### О проекте: 

**Проект.**



**Используемые технологии:**

- FastApi
- pydantic
- pydantic-settings
- SQLAlchemy
- PyMySQL
- pandas
- sshtunnel

### Запуск проекта локально:

Склонируйте проект:

```
git clone https://github.com/VladimirNagibin/updating_sites.git
```

Перейдите в директорию updating_sites:

```
cd updating_sites
```

Создайте файл .env. Тестовые данные можно взять из .env.example. 

```
cp .env.example .env
```

Запустите сервисы:

```
sudo docker compose up
```

Сайт будет доступен по адресу http://127.0.0.1:8000/api/openapi

____

**Владимир Нагибин** 

Github: [@VladimirNagibin](https://github.com/VladimirNagibin/)
