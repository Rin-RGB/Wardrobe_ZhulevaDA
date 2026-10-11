# Умный гардероб — система учёта одежды и подбора образов

Веб-приложение на Django для учёта личного гардероба нескольких пользователей,
классификации вещей по категориям, сезонам и стилям, а также формирования готовых образов.

## Ключевая особенность архитектуры

Вещи принадлежат пользователям через `ForeignKey` (а не наоборот):
`ClothingItem.user → WardrobeUser`. Это обеспечивает нормализацию БД
и позволяет одному пользователю иметь много вещей, а вещи — принадлежать только одному владельцу.

## Стек технологий

- Python 3.11+
- Django 5.2
- SQLite (через Django ORM)
- HTML / CSS / Bootstrap 5.3

## Структура моделей

- `WardrobeUser` — пользователь системы
- `Category` — категория одежды (верх, низ, обувь, аксессуар)
- `ClothingItem` — вещь (связана с `WardrobeUser` через FK и с `Category` через FK)
- `Outfit` — образ (связан с `WardrobeUser` через FK, с `ClothingItem` через M2M)

## Установка и запуск

```bash
python -m venv venv
source venv/bin/activate   # Windows:  .\.venv\bin\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data  # заполнение тестовыми данными
python manage.py runserver