from models.category import Category
from models.clothing import ClothingItem


def _make_item(item_id=1, name="Футболка", cat_name="верх",
               color="белый", season="лето", price=800.0,
               quantity=1, style="повседневный"):
    cat = Category(1, cat_name)
    return ClothingItem(item_id, name, cat,
                        color, season, price, quantity, style)


def test_clothing_creation():
    item = _make_item()
    assert item.id == 1
    assert item.name == "Футболка"
    assert item.category.name == "верх"
    assert item.color == "белый"
    assert item.season == "лето"
    assert item.price == 800.0
    assert item.quantity == 1
    assert item.style == "повседневный"


def test_total_cost():
    item = _make_item(price=800.0, quantity=3)
    assert item.total_cost == 2400.0


def test_is_suitable_for_season_exact():
    item = _make_item(season="лето")
    assert item.is_suitable_for_season("лето")
    assert not item.is_suitable_for_season("зима")


def test_is_suitable_for_season_all():
    item = _make_item(season="всесезон")
    assert item.is_suitable_for_season("лето")
    assert item.is_suitable_for_season("зима")
    assert item.is_suitable_for_season("весна")
    assert item.is_suitable_for_season("осень")


def test_is_suitable_for_season_demi():
    item = _make_item(season="демисезон")
    assert item.is_suitable_for_season("весна")
    assert item.is_suitable_for_season("осень")
    assert not item.is_suitable_for_season("лето")
    assert not item.is_suitable_for_season("зима")


def test_price_category():
    assert _make_item(price=0).get_price_category() == "неизвестно"
    assert _make_item(price=500).get_price_category() == "эконом"
    assert _make_item(price=3000).get_price_category() == "средний"
    assert _make_item(price=8000).get_price_category() == "премиум"


def test_is_similar_to_same():
    a = _make_item(item_id=1, name="Футболка",
                   color="белый", season="лето", style="повседневный")
    b = _make_item(item_id=2, name="футболка",
                   color="БЕЛЫЙ", season="лето", style="повседневный")
    assert a.is_similar_to(b)


def test_is_similar_to_different_color():
    a = _make_item(color="белый")
    b = _make_item(color="чёрный")
    assert not a.is_similar_to(b)


def test_is_similar_to_different_style():
    a = _make_item(style="повседневный")
    b = _make_item(style="деловой")
    assert not a.is_similar_to(b)


def test_is_suitable_for_occasion():
    casual = _make_item(style="повседневный")
    formal = _make_item(style="деловой")
    sport = _make_item(style="спортивный")

    assert casual.is_suitable_for_occasion("повседневный")
    assert not casual.is_suitable_for_occasion("деловой")
    assert formal.is_suitable_for_occasion("деловой")
    assert formal.is_suitable_for_occasion("вечерний")
    assert sport.is_suitable_for_occasion("спортивный")
    assert not sport.is_suitable_for_occasion("праздничный")


def test_str_representation():
    item = _make_item(name="Джинсы", cat_name="низ", color="синий")
    text = str(item)
    assert "Джинсы" in text
    assert "Низ" in text
    assert "синий" in text


def test_to_dict():
    item = _make_item(item_id=5, name="Куртка", cat_name="верх",
                      color="чёрный", season="зима", price=10000.0,
                      quantity=1, style="повседневный")
    d = item.to_dict()
    assert d["id"] == 5
    assert d["name"] == "Куртка"
    assert d["category"] == "верх"
    assert d["style"] == "повседневный"


def test_from_data():
    cat = Category(1, "верх")
    data = {
        "id": 1,
        "name": "Футболка",
        "category": "верх",
        "color": "белый",
        "season": "лето",
        "price": 800.0,
        "quantity": 2,
        "style": "повседневный",
    }
    item = ClothingItem.from_data(data, [cat])
    assert item.name == "Футболка"
    assert item.category.name == "верх"
    assert item.quantity == 2


def test_from_data_missing_category():
    data = {
        "id": 1,
        "name": "Шляпа",
        "category": "несуществующая",
        "color": "чёрный",
        "season": "лето",
        "price": 500.0,
    }
    item = ClothingItem.from_data(data, [])
    assert item.category.name == "прочее"
    assert item.style == "повседневный"
