from models.category import Category
from models.clothing import ClothingItem
from models.outfit import Outfit


def _make_item(item_id, name, cat_name,
               season="всесезон", style="повседневный"):
    cat = Category(item_id, cat_name)
    return ClothingItem(item_id, name, cat,
                        "чёрный", season, 1000.0, 1, style)


def test_outfit_creation():
    outfit = Outfit(1, "Деловой", "деловой", "демисезон")
    assert outfit.id == 1
    assert outfit.name == "Деловой"
    assert outfit.occasion == "деловой"
    assert outfit.items == []


def test_add_item():
    outfit = Outfit(1, "Тест")
    item = _make_item(1, "Футболка", "верх")
    outfit.add_item(item)
    assert len(outfit.items) == 1


def test_add_item_no_duplicates():
    outfit = Outfit(1, "Тест")
    item = _make_item(1, "Футболка", "верх")
    outfit.add_item(item)
    outfit.add_item(item)
    assert len(outfit.items) == 1


def test_remove_item():
    outfit = Outfit(1, "Тест")
    item = _make_item(1, "Футболка", "верх")
    outfit.add_item(item)
    result = outfit.remove_item(item)
    assert result is True
    assert len(outfit.items) == 0


def test_remove_nonexistent():
    outfit = Outfit(1, "Тест")
    item = _make_item(1, "Футболка", "верх")
    result = outfit.remove_item(item)
    assert result is False


def test_is_complete():
    outfit = Outfit(1, "Тест")
    top = _make_item(1, "Футболка", "верх")
    bottom = _make_item(2, "Джинсы", "низ")

    assert not outfit.is_complete()
    outfit.add_item(top)
    assert not outfit.is_complete()
    outfit.add_item(bottom)
    assert outfit.is_complete()


def test_has_category():
    outfit = Outfit(1, "Тест")
    top = _make_item(1, "Футболка", "верх")
    outfit.add_item(top)
    assert outfit.has_category("верх")
    assert not outfit.has_category("низ")


def test_total_cost():
    outfit = Outfit(1, "Тест")
    outfit.add_item(_make_item(1, "A", "верх"))
    outfit.add_item(_make_item(2, "B", "низ"))
    assert outfit.get_total_cost() == 2000.0


def test_str_complete():
    outfit = Outfit(1, "Прогулка", "повседневный", "лето")
    outfit.add_item(_make_item(1, "Футболка", "верх"))
    outfit.add_item(_make_item(2, "Джинсы", "низ"))
    text = str(outfit)
    assert "Прогулка" in text
    assert "полный" in text


def test_str_incomplete():
    outfit = Outfit(1, "Прогулка", "повседневный", "лето")
    text = str(outfit)
    assert "неполный" in text


def test_to_dict():
    outfit = Outfit(1, "Тест", "деловой", "зима")
    outfit.add_item(_make_item(10, "A", "верх"))
    d = outfit.to_dict()
    assert d["id"] == 1
    assert d["occasion"] == "деловой"
    assert d["item_ids"] == [10]


def test_from_data():
    top = _make_item(1, "Футболка", "верх")
    bottom = _make_item(2, "Джинсы", "низ")
    wardrobe = [top, bottom]

    data = {
        "id": 1,
        "name": "Летний",
        "occasion": "повседневный",
        "season": "лето",
        "item_ids": [1, 2],
    }
    outfit = Outfit.from_data(data, wardrobe)
    assert outfit.name == "Летний"
    assert len(outfit.items) == 2
    assert outfit.is_complete()


def test_from_data_missing_item():
    top = _make_item(1, "Футболка", "верх")
    wardrobe = [top]

    data = {
        "id": 1,
        "name": "Неполный",
        "occasion": "повседневный",
        "season": "лето",
        "item_ids": [1, 999],
    }
    outfit = Outfit.from_data(data, wardrobe)
    assert len(outfit.items) == 1
