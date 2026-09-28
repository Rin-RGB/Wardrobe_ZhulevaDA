import datetime
from models.category import Category
from models.clothing import ClothingItem
from models.user import User


def get_current_season() -> str:
    month = datetime.datetime.now().month
    if month in (12, 1, 2):
        return "зима"
    if month in (3, 4, 5):
        return "весна"
    if month in (6, 7, 8):
        return "лето"
    return "осень"


def input_category(user: User) -> Category:
    """Интерактивный выбор категории."""
    while True:
        print("\nДоступные категории:")
        for i, cat in enumerate(user.categories, 1):
            print(f"  {i}. {cat}")
        print(f"  {len(user.categories) + 1}. + Создать новую")

        raw = input("Выберите номер: ").strip()
        if not raw.isdigit():
            print("Нужно ввести число.")
            continue

        choice = int(raw)

        if 1 <= choice <= len(user.categories):
            return user.categories[choice - 1]

        if choice == len(user.categories) + 1:
            name = input("Название новой категории: ").strip()
            if not name:
                print("Название не может быть пустым.")
                continue
            new_cat = user.add_category(name)
            if new_cat is None:
                print(f"Категория '{name}' уже существует.")
                continue
            print(f"Категория '{new_cat}' создана.")
            return new_cat

        print("Неверный ввод.")


def input_season() -> str:
    valid_seasons = ["лето", "зима", "демисезон", "всесезон"]

    while True:
        season = input(
            "Сезон (лето / зима / демисезон / всесезон): "
        ).strip().lower()

        if season in valid_seasons:
            return season

        if season in ("осень", "весна"):
            print(f"\nВы указали '{season}', относится к демисезону.")
            confirm = input(
                "Указать 'демисезон'? (Enter — да, "
                "или введите другой): "
            ).strip().lower()

            if not confirm:
                return "демисезон"
            if confirm in valid_seasons:
                return confirm
            print(f"Сезон '{confirm}' не распознан.\n")
            continue

        print(f"\nСезон '{season}' не распознан.")
        print("Будет определена как всесезонная.")
        confirm = input(
            "Согласны? (Enter — да, или введите правильный): "
        ).strip().lower()

        if not confirm:
            return "всесезон"
        if confirm in valid_seasons:
            return confirm
        print(f"Сезон '{confirm}' не распознан.\n")


def input_style() -> str:
    valid_styles = list(ClothingItem.VALID_STYLES)
    prompt = " / ".join(valid_styles)

    while True:
        raw = input(f"Стиль ({prompt}): ").strip().lower()
        if raw in valid_styles:
            return raw

        print(f"\nСтиль '{raw}' не распознан.")
        print("Будет установлен 'повседневный'.")
        confirm = input(
            "Согласны? (Enter — да, или введите правильный): "
        ).strip().lower()

        if not confirm:
            return "повседневный"
        if confirm in valid_styles:
            return confirm
        print(f"Стиль '{confirm}' не распознан.\n")


def input_price() -> float:
    raw = input("Цена вещи (в рублях): ").strip().replace(",", ".")
    if raw.replace(".", "", 1).isdigit():
        return float(raw)
    print("Некорректная цена, установлено 0.")
    return 0.0


def input_quantity() -> int:
    raw = input("Количество таких вещей: ").strip()
    if raw.isdigit() and int(raw) > 0:
        return int(raw)
    return 1


def input_occasion() -> str:
    valid = list((
        "повседневный", "деловой", "вечерний",
        "спортивный", "праздничный",
    ))
    prompt = " / ".join(valid)
    while True:
        raw = input(f"Повод ({prompt}): ").strip().lower()
        if raw in valid:
            return raw
        print(f"Повод '{raw}' не распознан. Попробуйте ещё раз.\n")
