from models.category import Category


def test_category_creation():
    cat = Category(1, "верх")
    assert cat.id == 1
    assert cat.name == "верх"


def test_category_str():
    cat = Category(1, "верх")
    assert str(cat) == "Верх"


def test_category_repr():
    cat = Category(1, "верх")
    assert repr(cat) == "Category(1, 'верх')"


def test_category_eq():
    a = Category(1, "верх")
    b = Category(2, "верх")
    c = Category(3, "низ")
    assert a == b
    assert a != c
    assert a != "верх"


def test_category_rename():
    cat = Category(1, "верх")
    cat.rename("Верхняя одежда")
    assert cat.name == "верхняя одежда"


def test_category_to_dict():
    cat = Category(1, "верх")
    d = cat.to_dict()
    assert d == {"id": 1, "name": "верх"}


def test_category_from_data():
    data = {"id": 2, "name": "низ"}
    cat = Category.from_data(data)
    assert cat.id == 2
    assert cat.name == "низ"


def test_default_categories():
    defaults = Category.get_default_categories()
    assert len(defaults) == 4
    names = [c.name for c in defaults]
    assert "верх" in names
    assert "низ" in names
    assert "обувь" in names
    assert "аксессуар" in names
