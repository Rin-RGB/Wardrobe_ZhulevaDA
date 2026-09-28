from typing import Optional
from models import ClothingItem, Outfit, User
from storage import (
    list_users, load_user_data, save_user_data, user_exists,
)
from utils import (
    get_current_season, input_category, input_price,
    input_quantity, input_season, input_style, input_occasion,
)


def choose_user() -> Optional[User]:
    """Выбор существующего пользователя или создание нового."""
    while True:
        print("\n=== ВЫБОР ПОЛЬЗОВАТЕЛЯ ===")
        users = list_users()

        if users:
            print("Существующие пользователи:")
            for i, name in enumerate(users, 1):
                print(f"  {i}. {name}")
            print(f"  {len(users) + 1}. Создать нового пользователя")
        else:
            print("Пока нет зарегистрированных пользователей.")
            print("  1. Создать нового пользователя")

        print("  0. Выйти из программы")

        raw = input("\nВыберите пункт: ").strip()
        if not raw or raw == "0":
            return None

        if not raw.isdigit():
            print("Нужно ввести число.")
            continue

        choice = int(raw)

        if users and 1 <= choice <= len(users):
            name = users[choice - 1]
            user = User(user_id=1, name=name)
            load_user_data(user)
            print(f"\nЗдравствуйте, {user.name}!")
            return user

        if (not users and choice == 1) or (users and choice == len(users) + 1):
            name = input("Введите имя нового пользователя: ").strip()
            if not name:
                print("Имя не может быть пустым.")
                continue
            if user_exists(name):
                print(f"Пользователь '{name}' уже существует.")
                continue
            # Создаём пользователя без начальных вещей
            user = User(user_id=1, name=name)
            save_user_data(user)
            print(f"\nПользователь '{name}' создан. "
                  f"Гардероб пуст — можете добавить вещи.")
            return user

        print("Неверный ввод.")


def print_item_details(item: ClothingItem) -> None:
    current_season = get_current_season()
    season_ok = item.is_suitable_for_season(current_season)
    season_msg = (
        f"подходит для текущего сезона ({current_season})"
        if season_ok
        else f"предназначена для '{item.season}', а сейчас '{current_season}'"
    )

    print(f"\nВещь: {item.name}")
    print(f"Категория: {item.category}")
    print(f"Цвет: {item.color}")
    print(f"Стиль: {item.style}")
    print(f"Сезон: {item.season} — "
          f"{season_msg}")
    print(f"Цена: {item.price:.2f} руб."
          f" — категория: {item.get_price_category()}")
    print(f"Количество: {item.quantity}")
    print(f"Общая стоимость: {item.total_cost:.2f} руб.")


def add_item(user: User) -> None:
    name = input("Название вещи: ").strip() or "Без названия"
    category = input_category(user)
    color = input("Цвет вещи: ").strip().lower()
    season = input_season()
    style = input_style()
    price = input_price()
    quantity = input_quantity()

    new_item = ClothingItem(
        item_id=user.get_next_item_id(),
        name=name,
        category=category,
        color=color,
        season=season,
        price=price,
        quantity=quantity,
        style=style,
    )

    similar = user.find_similar(new_item)
    if similar is not None:
        similar.quantity += quantity
        similar.price = price
        print(f"\nПохожая вещь уже есть: '"
              f"{similar.name}'.")
        print(f"Количество увеличено на {quantity}."
              f" Теперь: {similar.quantity}.")
        print_item_details(similar)
        save_user_data(user)
        return

    user.add_clothing(new_item)
    print_item_details(new_item)
    print(f"\nВещь '{new_item.name}' добавлена в гардероб.")
    save_user_data(user)


def view_wardrobe(user: User) -> None:
    if not user.wardrobe:
        print("\nГардероб пуст.\n")
        return

    print(f"\nГАРДЕРОБ {user.name}")
    for i, item in enumerate(user.wardrobe, 1):
        print(f"{i}. {item}")

    total_items = sum(item.quantity for item in user.wardrobe)
    print(f"\nВсего позиций: {len(user.wardrobe)}")
    print(f"Всего вещей: {total_items}")
    print(f"Общая стоимость: "
          f"{user.get_wardrobe_cost():.2f} руб.")


def pick_item(user: User, prompt: str = "Выберите номер вещи")\
        -> Optional[ClothingItem]:
    if not user.wardrobe:
        print("\nГардероб пуст.\n")
        return None

    print("\nСПИСОК ВЕЩЕЙ")
    for i, item in enumerate(user.wardrobe, 1):
        print(f"{i}. {item}")

    raw = input(f"\n{prompt} (1-{len(user.wardrobe)}, 0 — отмена): ").strip()
    if not raw or raw == "0":
        print("Действие отменено.")
        return None
    if not raw.isdigit():
        print("Нужно ввести число.")
        return None

    idx = int(raw) - 1
    if idx < 0 or idx >= len(user.wardrobe):
        print("Нет вещи с таким номером.")
        return None
    return user.wardrobe[idx]


def delete_item(user: User) -> None:
    item = pick_item(user, "Какую вещь убрать?")
    if item is None:
        return

    if item.quantity > 1:
        confirm = input(
            f"Убрать 1 штуку '{item.name}'? "
            f"(Останется {item.quantity - 1}) (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Действие отменено.")
            return

        item.quantity -= 1
        print(f"Убрана 1 штука. Осталось: {item.quantity}.")
        save_user_data(user)
    else:
        confirm = input(
            f"Удалить '{item.name}' ({item.category}, "
            f"{item.color}) полностью? (y/n): "
        ).strip().lower()
        if confirm != "y":
            print("Удаление отменено.")
            return

        user.wardrobe.remove(item)
        print(f"Вещь '{item.name}' удалена.")
        save_user_data(user)


def edit_item(user: User) -> None:
    item = pick_item(user, "Какую вещь редактировать?")
    if item is None:
        return

    print(f"\nРедактируем: {item.name}")
    print("(Нажмите Enter, чтобы оставить текущее значение)\n")

    new_val = input(f"Название [{item.name}]: ").strip()
    if new_val:
        item.name = new_val

    new_val = input(f"Категория [{item.category}]: ").strip().lower()
    if new_val:
        item.category = input_category(user)

    new_val = input(f"Цвет [{item.color}]: ").strip().lower()
    if new_val:
        item.color = new_val

    new_val = input(f"Сезон [{item.season}]: ").strip().lower()
    if new_val:
        item.season = input_season()

    new_val = input(f"Стиль [{item.style}]: ").strip().lower()
    if new_val:
        item.style = input_style()

    new_val = input(f"Цена [{item.price:.2f}]: ").strip().replace(",", ".")
    if new_val:
        if new_val.replace(".", "", 1).isdigit():
            item.price = float(new_val)
        else:
            print("Некорректная цена, оставлено прежнее значение.")

    new_val = input(f"Количество [{item.quantity}]: ").strip()
    if new_val:
        if new_val.isdigit() and int(new_val) > 0:
            item.quantity = int(new_val)
        else:
            print("Некорректное количество, оставлено прежнее значение.")

    print_item_details(item)
    print(f"\nВещь '{item.name}' обновлена.")
    save_user_data(user)


def create_outfit(user: User) -> None:
    if len(user.wardrobe) < 2:
        print("\nНужно хотя бы 2 вещи для создания образа.\n")
        return

    name = input("Название образа: ").strip() or "Без названия"
    occasion = input_occasion()
    season = (input("Сезон образа (лето / зима / демисезон / всесезон): ")
              .strip().lower())
    if season not in ClothingItem.VALID_SEASONS:
        season = "всесезон"

    outfit = Outfit(
        outfit_id=user.get_next_outfit_id(),
        name=name,
        occasion=occasion,
        season=season,
    )

    print("\nВыберите вещи для образа (вводите номера, 0 — готово):")
    for i, item in enumerate(user.wardrobe, 1):
        print(f"{i}. {item}")

    while True:
        raw = input("Номер вещи: ").strip()
        if raw == "0" or not raw:
            break
        if not raw.isdigit():
            print("Нужно ввести число.")
            continue
        idx = int(raw) - 1
        if idx < 0 or idx >= len(user.wardrobe):
            print("Нет вещи с таким номером.")
            continue
        outfit.add_item(user.wardrobe[idx])
        print(f"  Добавлено: {user.wardrobe[idx].name}")

    user.add_outfit(outfit)
    save_user_data(user)
    print(f"\n{outfit}")
    print(f"Образ '{outfit.name}' создан.")


def view_outfits(user: User) -> None:
    if not user.outfits:
        print("\nУ вас пока нет образов.\n")
        return

    print(f"\nОБРАЗЫ {user.name}")
    for i, outfit in enumerate(user.outfits, 1):
        print(f"\n{i}. {outfit}")


def auto_suggest_outfit(user: User) -> None:
    season = get_current_season()
    print(f"\nТекущий сезон: {season}")
    occasion = input_occasion()

    print(f"Подбираю образ: сезон '{season}', повод '{occasion}'...")

    outfit = user.suggest_outfit(season, occasion)
    if outfit is None:
        print("Не удалось подобрать образ — нет подходящих вещей.")
        return

    user.add_outfit(outfit)
    save_user_data(user)
    print(f"\n{outfit}")
    if not outfit.is_complete():
        print("⚠ Образ неполный — "
              "не хватает верха или низа подходящего стиля.")
    print("Авто-образ сохранён. Вы можете дополнить его вручную.")


def manage_categories(user: User) -> None:
    """Меню управления категориями."""
    while True:
        print("\nУПРАВЛЕНИЕ КАТЕГОРИЯМИ")
        for i, cat in enumerate(user.categories, 1):
            items_count = sum(1 for item in user.wardrobe
                              if item.category.id == cat.id)
            print(f"  {i}. {cat} (вещей: {items_count})")
        print("  0. Назад")

        raw = (input("\nВыберите категорию для удаления (номер) или 0: ")
               .strip())
        if not raw or raw == "0":
            return
        if not raw.isdigit():
            print("Нужно ввести число.")
            continue

        idx = int(raw) - 1
        if idx < 0 or idx >= len(user.categories):
            print("Нет такой категории.")
            continue

        cat = user.categories[idx]
        if not user.remove_category(cat.id):
            print(f"Нельзя удалить '{cat}' — есть вещи этой категории.")
            continue
        print(f"Категория '{cat}' удалена.")
        save_user_data(user)


def wardrobe_menu(user: User) -> None:
    """Меню гардероба для конкретного пользователя."""
    while True:
        print(f"\nМЕНЮ ({user.name}):")
        print("1. Добавить вещь")
        print("2. Посмотреть гардероб")
        print("3. Убрать вещь (уменьшить количество / удалить)")
        print("4. Редактировать вещь")
        print("5. Создать образ")
        print("6. Посмотреть образы")
        print("7. Автоподбор образа")
        print("8. Управление категориями")
        print("9. Сменить пользователя")
        print("10. Выйти из программы")

        choice = input("Выберите пункт (1-10): ").strip()

        if choice == "1":
            add_item(user)
        elif choice == "2":
            view_wardrobe(user)
        elif choice == "3":
            delete_item(user)
        elif choice == "4":
            edit_item(user)
        elif choice == "5":
            create_outfit(user)
        elif choice == "6":
            view_outfits(user)
        elif choice == "7":
            auto_suggest_outfit(user)
        elif choice == "8":
            manage_categories(user)
        elif choice == "9":
            save_user_data(user)
            print(f"Данные пользователя '{user.name}' сохранены.")
            return  # вернуться к выбору пользователя
        elif choice == "10":
            save_user_data(user)
            print("Данные сохранены. До свидания!")
            exit(0)
        else:
            print("Неверный ввод.")


def main() -> None:
    """Главный цикл: выбор пользователя → работа с гардеробом."""
    while True:
        user = choose_user()
        if user is None:
            print("До свидания!")
            break
        wardrobe_menu(user)


if __name__ == "__main__":
    main()
