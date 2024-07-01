# 1. num_sequence.py
Программа, которая выводит n первых элементов последовательности 122333444455555… (число повторяется столько раз, чему оно равно)


# 2. grocery_store
Тестовое задание для Доктор24 и Сарафан.

Django backend проект магазина продуктов со следующим функционалом:

- реализована возможность создания, редактирования, удаления категорий и подкатегорий товаров в админке

- реализован эндпоинт для просмотра всех категорий с подкатегориями с пагинацией

- реализована возможность добавления, изменения, удаления продуктов в админке
- реализован эндпоинт вывода продуктов с пагинацией
- реализован эндпоинт добавления, изменения (изменение количества), удаления продукта в корзине.
- реализован эндпоинт вывода  состава корзины с подсчетом количества товаров и суммы стоимости товаров в корзине.
- реализована возможность полной очистки корзины
- операции по эндпоинтам категорий и продуктов может осуществлять любой пользователь
- операции по эндпоинтам корзины может осуществлять только авторизированный пользователь и только со своей корзиной
- реализована авторизация по токену


## Технологии:
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/DJANGO-4.2.13-blue?logo=django&logoColor=white)
![djangorestframework](https://img.shields.io/badge/DJANGORESTFRAMEWORK-3.15.1-blue?logo=django&logoColor=white)
[![Django-Imagekit](https://img.shields.io/badge/DjangoImagekit-blue)](https://django-imagekit.readthedocs.io/)

## Запуск проекта

Клонируйте репозиторий и перейдите в него:
```
git clone https://github.com/ZebraHr/grocery_store
cd grocery_store
```
Создайте и активируйте виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```
```
python -m pip install --upgrade pip
```
Установите зависимости:
```
pip install -r requirements.txt
```
Создайте файл .env и поместите туда следующие переменные:
```
SECRET_KEY='your_sercret_key'
ALLOWED_HOSTS=127.0.0.1, localhost
DEBUG=True (при необходимости)
```
Для генерации своего SECRET_KEY можете исполнить следующий код:
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Проведите миграции:
```
cd grocery_store
python manage.py migrate
```
Запустите проект:
```
python manage.py runserver
```
Для управления через систему администратора создайте superuser:
```
python manage.py createsuperuser
```
### Примеры запросов
Пример GET-запроса для получения списка всех категорий
```
GET .../api/categories/
http://127.0.0.1:8000/api/v1/titles/?category=movie
```
Ответ
```
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "name": "string",
      "slug": "string",
      "image": "http://example.com",
      "subcategories": [
        {
          "id": 0,
          "name": "string",
          "slug": "string",
          "image": "http://example.com"
        }
      ]
    }
  ]
}
```
Пример POST-запроса добавление продукта в корзину
```
POST .../api/cart/add_product/
```
```
{
    "product_id": "0",
    "amount": "1"
}
```
Ответ
```
{
  "id": 0,
  "user": 0,
  "cart_products": [
    {
      "id": 0,
      "product": {
        "name": "string"
      },
      "amount": 1,
      "total_price": "string"
    }
  ],
  "total_amount": "string",
  "total_price": "string"
}
```

##### Весь доступный функционал API:

http://127.0.0.1:8000/redoc/

http://127.0.0.1:8000/swagger/


### Автор

[Анна Победоносцева](https://github.com/ZebraHr)