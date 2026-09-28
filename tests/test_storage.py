import os
import shutil
import pytest
from models.clothing import ClothingItem
from models.outfit import Outfit
from models.user import User
from storage import (
    list_users, load_user_data, save_user_data,
    user_exists, USERS_DIR,
)


@pytest.fixture(autouse=True)
def clean_data_dir():
    if os.path.exists(USERS_DIR):
        shutil.rmtree(USERS_DIR)
    yield
    if os.path.exists(USERS_DIR):
        shutil.rmtree(USERS_DIR)


def test_list_users_empty():
    assert list_users() == []


def test_save_and_load_user():
    user = User(1, "Тест")
    top_cat = next(c for c in user.categories if c.name == "верх")
    item = ClothingItem(1, "Футболка",
                        top_cat, "белый", "лето", 800.0, 2, "повседневный")
    user.add_clothing(item)

    save_user_data(user)
    assert user_exists("Тест")
    assert "Тест" in list_users()

    loaded = User(1, "Тест")
    load_user_data(loaded)
    assert len(loaded.wardrobe) == 1
    assert loaded.wardrobe[0].name == "Футболка"
    assert loaded.wardrobe[0].quantity == 2


def test_save_and_load_outfit():
    user = User(1, "Тест")
    top_cat = next(c for c in user.categories if c.name == "верх")
    bottom_cat = next(c for c in user.categories if c.name == "низ")

    top = ClothingItem(1, "Футболка", top_cat, "белый", "лето",
                       800.0, 1, "повседневный")
    bottom = ClothingItem(2, "Джинсы", bottom_cat, "синий",
                          "лето", 3500.0, 1, "повседневный")
    user.add_clothing(top)
    user.add_clothing(bottom)

    outfit = Outfit(1, "Летний", "повседневный", "лето")
    outfit.add_item(top)
    outfit.add_item(bottom)
    user.add_outfit(outfit)

    save_user_data(user)

    loaded = User(1, "Тест")
    load_user_data(loaded)
    assert len(loaded.outfits) == 1
    assert loaded.outfits[0].name == "Летний"
    assert len(loaded.outfits[0].items) == 2


def test_load_nonexistent_user():
    user = User(1, "НетТакого")
    load_user_data(user)
    assert len(user.wardrobe) == 0


def test_user_exists():
    assert not user_exists("Никто")
    user = User(1, "КтоТо")
    save_user_data(user)
    assert user_exists("КтоТо")


def test_save_preserves_categories():
    user = User(1, "Тест")
    user.add_category("головной убор")
    save_user_data(user)

    loaded = User(1, "Тест")
    load_user_data(loaded)
    cat_names = [c.name for c in loaded.categories]
    assert "головной убор" in cat_names


def test_load_empty_file():
    os.makedirs(USERS_DIR, exist_ok=True)
    path = os.path.join(USERS_DIR, "Пустой.json")
    with open(path, "w", encoding="utf-8") as f:
        f.write("")

    user = User(1, "Пустой")
    load_user_data(user)
    assert len(user.wardrobe) == 0


def test_load_corrupted_file():
    os.makedirs(USERS_DIR, exist_ok=True)
    path = os.path.join(USERS_DIR, "Битый.json")
    with open(path, "w", encoding="utf-8") as f:
        f.write("{невалидный json")

    user = User(1, "Битый")
    load_user_data(user)
    assert len(user.wardrobe) == 0
