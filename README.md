# Умный гардероб — система учёта одежды и подбора образов

Веб-приложение на Django для учёта личного гардероба нескольких пользователей,
классификации вещей по категориям, сезонам и стилям, а также формирования готовых образов.

## Ключевые особенности

- Многопользовательская система: каждый пользователь владеет своим гардеробом и образами
- Вещи принадлежат пользователям через `ForeignKey` (нормализованная БД)
- Автоматический подбор образов по сезону и поводу с учётом стиля
- Django Template Language: шаблоны, наследование, include, фильтры
- Собственные статические файлы: CSS, JavaScript, изображения

## Стек технологий

- Python 3.11+
- Django 5.2
- Django ORM + SQLite
- Django Template Language (DTL)
- HTML5 / CSS3 / JavaScript
- Bootstrap 5.3 (через CDN)
- Git

## Структура моделей

- `WardrobeUser` — пользователь системы
- `Category` — категория одежды (верх, низ, обувь, аксессуар)
- `ClothingItem` — вещь (связана с `WardrobeUser` через FK и с `Category` через FK)
- `Outfit` — образ (связан с `WardrobeUser` через FK, с `ClothingItem` через M2M)

## Работа с базой данных (Django ORM)

Проект полностью переведён на Django ORM. Взаимодействие с БД осуществляется через модели:
- `WardrobeUser` ↔ `ClothingItem`: связь **один-ко-многим** (`ForeignKey`, `on_delete=CASCADE`, `related_name="clothing_items"`).
- `Category` ↔ `ClothingItem`: связь **один-ко-многим** (`ForeignKey`, `on_delete=SET_NULL`).
- `Outfit` ↔ `ClothingItem`: связь **многие-ко-многим** (`ManyToManyField`, `related_name="in_outfits"`).

### Команды для управления БД:
```bash
# Создание файлов миграций после изменения моделей
python manage.py makemigrations

# Применение миграций к базе данных
python manage.py migrate

# Запуск интерактивной оболочки для ORM-запросов
python manage.py shell