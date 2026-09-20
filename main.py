import datetime

wardrobe = []


def get_current_season():
    month = datetime.datetime.now().month
    if month in (12, 1, 2): return "зима"
    if month in (3, 4, 5): return "весна"
    if month in (6, 7, 8): return "лето"
    return "осень"


def init_wardrobe():
    wardrobe.extend([
        {
            'name': 'Джинсы',
            'category': 'низ',
            'color': 'синий',
            'season': 'демисезон',
            'price': 3500.0,
            'quantity': 2,
            'total': 7000.0
        },
        {
            'name': 'Футболка',
            'category': 'верх',
            'color': 'белый',
            'season': 'лето',
            'price': 800.0,
            'quantity': 3,
            'total': 2400.0
        },
        {
            'name': 'Зимние ботинки',
            'category': 'обувь',
            'color': 'черный',
            'season': 'зима',
            'price': 8500.0,
            'quantity': 1,
            'total': 8500.0
        }
    ])


def validate_item(item):
    current_season = get_current_season()

    if item['category'] in ("верх", "низ", "обувь", "аксессуар"):
        category_ok = True
        category_msg = f"Категория '{item['category']}' корректна."
    else:
        category_ok = False
        category_msg = f"Категория '{item['category']}' неизвестна. Будет отнесена к 'прочее'."

    season = item['season']
    if season == "всесезон":
        season_ok = True
        season_msg = "Вещь всесезонная — подойдёт в любое время года."
    elif season == current_season:
        season_ok = True
        season_msg = f"Вещь подходит для текущего сезона ({current_season})."
    elif season == "демисезон" and current_season in ("весна", "осень"):
        season_ok = True
        season_msg = f"Вещь подходит для текущего сезона ({current_season})."
    else:
        season_ok = False
        season_msg = f"Вещь предназначена для сезона '{season}', а сейчас '{current_season}'."

    price = item['price']
    if price <= 0:
        price_msg = "Цена не указана или указана некорректно."
        price_category = "неизвестно"
    elif price < 1000:
        price_msg = "Бюджетная вещь."
        price_category = "эконом"
    elif price < 5000:
        price_msg = "Вещь средней ценовой категории."
        price_category = "средний"
    else:
        price_msg = "Дорогая вещь."
        price_category = "премиум"

    return {
        'category_ok': category_ok,
        'category_msg': category_msg,
        'season_ok': season_ok,
        'season_msg': season_msg,
        'price_msg': price_msg,
        'price_category': price_category,
    }


def input_category(current=None):
    valid_categories = ("верх", "низ", "обувь", "аксессуар")
    prompt_suffix = f" [{current}]" if current else ""

    while True:
        category = input(f"Категория (верх / низ / обувь / аксессуар){prompt_suffix}: ").strip().lower()

        if not category and current:
            return current

        if category in valid_categories:
            return category

        print(f"\nЭто не стандартная категория ('{category}').")
        print("Вещь будет отнесена к категории 'прочее'.")
        confirm = input("Уточнить категорию? (Enter — принять 'прочее', или введите новую категорию): ").strip().lower()

        if not confirm:
            return "прочее"

        if confirm in valid_categories:
            return confirm

        print(f"Категория '{confirm}' тоже не стандартная. Попробуйте ещё раз.\n")


def input_season(current=None):
    valid_seasons = ['лето', 'зима', 'демисезон', 'всесезон']
    prompt_suffix = f" [{current}]" if current else ""

    while True:
        season = input(f"Сезон (лето / зима / демисезон / всесезон){prompt_suffix}: ").strip().lower()

        if not season and current:
            return current

        if season in valid_seasons:
            return season

        if season in ('осень', 'весна'):
            print(f"\nВы указали '{season}', который относится к демисезону.")
            confirm = input("Указать 'демисезон'? (Enter — да, или введите другой сезон): ").strip().lower()

            if not confirm:
                return "демисезон"

            if confirm in valid_seasons:
                return confirm

            print(f"Сезон '{confirm}' не распознан. Попробуйте ещё раз.\n")
            continue

        print(f"\nСезон '{season}' не распознан.")
        print("Вещь будет определена как всесезонная.")
        confirm = input("Вы согласны? (Enter — да, или введите правильный сезон): ").strip().lower()

        if not confirm:
            return "всесезон"

        if confirm in valid_seasons:
            return confirm

        print(f"Сезон '{confirm}' не распознан. Попробуйте ещё раз.\n")


def add_item():
    item_name = input("Название вещи (например, 'Джинсы'): ").strip() or "Без названия"
    category = input_category()
    color = input("Цвет вещи: ").strip().lower()
    season = input_season()

    price_str = input("Цена вещи (в рублях): ").strip().replace(',', '.')
    quantity_str = input("Количество таких вещей: ").strip()

    price = float(price_str) if price_str.replace(".", "", 1).isdigit() else 0.0
    quantity = int(quantity_str) if quantity_str.isdigit() else 1

    item = {
        'name': item_name,
        'category': category,
        'color': color,
        'season': season,
        'price': price,
        'quantity': quantity,
    }
    item['total'] = item['price'] * item['quantity']
    wardrobe.append(item)

    v = validate_item(item)

    print(f"\nВещь: {item['name']}")
    print(f"Категория: {item['category']} — {v['category_msg']}")
    print(f"Цвет: {item['color']}")
    print(f"Сезон: {item['season']} — {v['season_msg']}")
    print(f"Цена: {item['price']:.2f} руб. — {v['price_msg']} (категория: {v['price_category']})")
    print(f"Количество: {item['quantity']}")
    print(f"Общая стоимость: {item['total']:.2f} руб.")

    print("\nРЕКОМЕНДАЦИЯ")
    if v['category_ok'] and v['season_ok'] and item['quantity'] > 0 and item['price'] > 0:
        print(f"Вещь '{item['name']}' успешно добавлена в гардероб.")
    elif not v['category_ok']:
        print(f"Вещь '{item['name']}' добавлена, но её категория требует уточнения.")
    elif not v['season_ok']:
        print(f"Вещь '{item['name']}' добавлена, но сейчас не сезон для неё.")
    else:
        print(f"Вещь '{item['name']}' добавлена с предупреждениями.")


def view_wardrobe():
    if not wardrobe:
        print("\nВаш гардероб пока пуст.\n")
        return

    print("\nВАШ ГАРДЕРОБ")
    total_cost = 0
    for i, item in enumerate(wardrobe, 1):
        print(f"{i}. {item['name']} | Категория: {item['category']} | Цвет: {item['color']} | Сезон: {item['season']}")
        print(f"   Цена: {item['price']:.2f} руб. | Кол-во: {item['quantity']} | Сумма: {item['total']:.2f} руб.")
        total_cost += item['total']
    print(f"\nВсего вещей: {len(wardrobe)}")
    print(f"Общая стоимость гардероба: {total_cost:.2f} руб.")


def pick_item(prompt="Выберите номер вещи"):
    if not wardrobe:
        print("\nГардероб пуст — нечего выбирать.\n")
        return None

    print("\nСПИСОК ВЕЩЕЙ")
    for i, item in enumerate(wardrobe, 1):
        print(f"{i}. {item['name']} | {item['category']} | {item['color']} | {item['season']} | "
              f"{item['price']:.2f} руб. x {item['quantity']}")

    raw = input(f"\n{prompt} (1-{len(wardrobe)}, 0 — отмена): ").strip()
    if not raw or raw == '0':
        print("Действие отменено.")
        return None

    if not raw.isdigit():
        print("Нужно ввести число.")
        return None

    idx = int(raw) - 1
    if idx < 0 or idx >= len(wardrobe):
        print("Нет вещи с таким номером.")
        return None

    return idx


def delete_item():
    idx = pick_item("Какую вещь удалить?")
    if idx is None:
        return

    item = wardrobe[idx]
    confirm = input(f"Удалить '{item['name']}' ({item['category']}, {item['color']})? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Удаление отменено.")
        return

    removed = wardrobe.pop(idx)
    print(f"Вещь '{removed['name']}' удалена из гардероба.")


def edit_item():
    idx = pick_item("Какую вещь редактировать?")
    if idx is None:
        return

    item = wardrobe[idx]
    print(f"\nРедактируем: {item['name']}")
    print("(Нажмите Enter, чтобы оставить текущее значение)\n")

    new_val = input(f"Название [{item['name']}]: ").strip()
    if new_val:
        item['name'] = new_val

    item['category'] = input_category(item['category'])

    new_val = input(f"Цвет [{item['color']}]: ").strip().lower()
    if new_val:
        item['color'] = new_val

    item['season'] = input_season(item['season'])

    new_val = input(f"Цена [{item['price']:.2f}]: ").strip().replace(',', '.')
    if new_val:
        if new_val.replace(".", "", 1).isdigit():
            item['price'] = float(new_val)
        else:
            print("Некорректная цена, оставлено прежнее значение.")

    new_val = input(f"Количество [{item['quantity']}]: ").strip()
    if new_val:
        if new_val.isdigit():
            item['quantity'] = int(new_val)
        else:
            print("Некорректное количество, оставлено прежнее значение.")

    item['total'] = item['price'] * item['quantity']

    v = validate_item(item)

    print(f"\nОбновлённая вещь:")
    print(f"Вещь: {item['name']}")
    print(f"Категория: {item['category']} — {v['category_msg']}")
    print(f"Цвет: {item['color']}")
    print(f"Сезон: {item['season']} — {v['season_msg']}")
    print(f"Цена: {item['price']:.2f} руб. — {v['price_msg']} (категория: {v['price_category']})")
    print(f"Количество: {item['quantity']}")
    print(f"Общая стоимость: {item['total']:.2f} руб.")

    print("\nРЕКОМЕНДАЦИЯ")
    if v['category_ok'] and v['season_ok'] and item['quantity'] > 0 and item['price'] > 0:
        print(f"Вещь '{item['name']}' обновлена без замечаний.")
    elif not v['category_ok']:
        print(f"Вещь '{item['name']}' обновлена, но её категория требует уточнения.")
    elif not v['season_ok']:
        print(f"Вещь '{item['name']}' обновлена, но сейчас не сезон для неё.")
    else:
        print(f"Вещь '{item['name']}' обновлена с предупреждениями.")


init_wardrobe()

while True:
    print("\nМЕНЮ:")
    print("1. Добавить вещь")
    print("2. Посмотреть гардероб")
    print("3. Удалить вещь")
    print("4. Редактировать вещь")
    print("5. Выйти")

    choice = input("Выберите пункт меню (1-5): ").strip()

    if choice == '1':
        add_item()
    elif choice == '2':
        view_wardrobe()
    elif choice == '3':
        delete_item()
    elif choice == '4':
        edit_item()
    elif choice == '5':
        print("Спасибо за использование системы!")
        break
    else:
        print("Неверный ввод, попробуйте снова.")