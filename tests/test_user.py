from models.clothing import ClothingItem
from models.outfit import Outfit
from models.user import User


def _make_user_with_items():
    user = User(1, "Тест")
    top_cat = next(c for c in user.categories if c.name == "верх")
    bottom_cat = next(c for c in user.categories if c.name == "низ")

    tshirt = ClothingItem(1, "Футболка", top_cat,
                          "белый", "лето", 800.0, 3, "повседневный")
    jeans = ClothingItem(2, "Джинсы", bottom_cat,
                         "синий", "демисезон", 3500.0, 2, "повседневный")
    user.add_clothing(tshirt)
    user.add_clothing(jeans)
    return user


def test_user_creation():
    user = User(1, "Иван")
    assert user.id == 1
    assert user.name == "Иван"
    assert user.wardrobe == []
    assert user.outfits == []
    assert len(user.categories) == 4


def test_add_clothing():
    user = User(1, "Тест")
    cat = user.categories[0]
    item = ClothingItem(1, "Футболка", cat, "белый", "лето", 800.0)
    user.add_clothing(item)
    assert len(user.wardrobe) == 1


def test_get_wardrobe_cost():
    user = _make_user_with_items()
    # 800*3 + 3500*2 = 2400 + 7000 = 9400
    assert user.get_wardrobe_cost() == 9400.0


def test_get_next_item_id():
    user = User(1, "Тест")
    assert user.get_next_item_id() == 1
    cat = user.categories[0]
    user.add_clothing(ClothingItem(1, "A", cat, "x", "лето", 100.0))
    assert user.get_next_item_id() == 2


def test_get_next_outfit_id():
    user = User(1, "Тест")
    assert user.get_next_outfit_id() == 1
    user.add_outfit(Outfit(1, "Тест"))
    assert user.get_next_outfit_id() == 2


def test_find_similar():
    user = _make_user_with_items()
    top_cat = next(c for c in user.categories if c.name == "верх")
    duplicate = ClothingItem(99, "футболка", top_cat,
                             "БЕЛЫЙ", "лето", 1000.0, 1, "повседневный")
    found = user.find_similar(duplicate)
    assert found is not None
    assert found.name == "Футболка"


def test_find_similar_not_found():
    user = _make_user_with_items()
    top_cat = next(c for c in user.categories if c.name == "верх")
    different = ClothingItem(99, "Рубашка", top_cat, "красный", "лето", 2000.0,
                             1, "деловой")
    assert user.find_similar(different) is None


def test_remove_clothing_one_decreases_quantity():
    user = _make_user_with_items()
    # Футболка имеет quantity=3
    removed_completely = user.remove_clothing_one(1)
    assert removed_completely is False
    assert user.wardrobe[0].quantity == 2
    assert len(user.wardrobe) == 2


def test_remove_clothing_one_deletes_when_one():
    user = User(1, "Тест")
    cat = user.categories[0]
    item = ClothingItem(1, "Футболка", cat, "белый", "лето", 800.0, 1)
    user.add_clothing(item)

    removed_completely = user.remove_clothing_one(1)
    assert removed_completely is True
    assert len(user.wardrobe) == 0


def test_remove_clothing_one_nonexistent():
    user = User(1, "Тест")
    result = user.remove_clothing_one(999)
    assert result is False


def test_add_category():
    user = User(1, "Тест")
    initial_count = len(user.categories)
    new_cat = user.add_category("головной убор")
    assert new_cat is not None
    assert new_cat.name == "головной убор"
    assert len(user.categories) == initial_count + 1


def test_add_category_duplicate():
    user = User(1, "Тест")
    result = user.add_category("верх")
    assert result is None


def test_remove_category_empty():
    user = User(1, "Тест")
    acc_cat = next(c for c in user.categories if c.name == "аксессуар")
    result = user.remove_category(acc_cat.id)
    assert result is True


def test_remove_category_with_items():
    user = _make_user_with_items()
    top_cat = next(c for c in user.categories if c.name == "верх")
    result = user.remove_category(top_cat.id)
    assert result is False


def test_suggest_outfit():
    user = User(1, "Тест")
    top_cat = next(c for c in user.categories if c.name == "верх")
    bottom_cat = next(c for c in user.categories if c.name == "низ")

    top = ClothingItem(1, "T", top_cat,
                       "x", "лето", 100.0, 1, "повседневный")
    bottom = ClothingItem(2, "B", bottom_cat, "x", "лето",
                          100.0, 1, "повседневный")
    user.add_clothing(top)
    user.add_clothing(bottom)

    outfit = user.suggest_outfit("лето", "повседневный")
    assert outfit is not None
    assert outfit.is_complete()


def test_suggest_outfit_no_match():
    user = User(1, "Тест")
    top_cat = next(c for c in user.categories if c.name == "верх")
    sport_top = ClothingItem(1, "T", top_cat,
                             "x", "лето", 100.0, 1, "спортивный")
    user.add_clothing(sport_top)

    outfit = user.suggest_outfit("зима", "деловой")
    assert outfit is None


def test_suggest_outfit_by_occasion():
    user = User(1, "Тест")
    top_cat = next(c for c in user.categories if c.name == "верх")
    bottom_cat = next(c for c in user.categories if c.name == "низ")

    casual_top = ClothingItem(1, "T", top_cat, "x", "лето",
                              100.0, 1, "повседневный")
    formal_top = ClothingItem(2, "F", top_cat, "x", "лето",
                              100.0, 1, "деловой")
    bottom = ClothingItem(3, "B", bottom_cat, "x", "лето",
                          100.0, 1, "повседневный")
    user.add_clothing(casual_top)
    user.add_clothing(formal_top)
    user.add_clothing(bottom)

    outfit = user.suggest_outfit("лето", "деловой")
    assert outfit is not None
    names = {i.name for i in outfit.items}
    assert "F" in names
    assert "T" not in names


def test_user_to_dict():
    user = User(1, "Иван")
    d = user.to_dict()
    assert d == {"id": 1, "name": "Иван"}


def test_user_from_data():
    data = {"id": 1, "name": "Иван"}
    user = User.from_data(data)
    assert user.id == 1
    assert user.name == "Иван"


def test_user_str():
    user = _make_user_with_items()
    text = str(user)
    assert "Тест" in text
    assert "Вещей: 2" in text
