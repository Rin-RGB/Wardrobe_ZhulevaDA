import json
import os
from typing import List
from models.user import User
from models.clothing import ClothingItem
from models.outfit import Outfit

DATA_DIR = "data"
USERS_DIR = os.path.join(DATA_DIR, "users")


def ensure_dirs() -> None:
    os.makedirs(USERS_DIR, exist_ok=True)


def _user_file(name: str) -> str:
    safe_name = "".join(
        c if c.isalnum() or c in " _-" else "_" for c in name
    )
    return os.path.join(USERS_DIR, f"{safe_name}.json")


def list_users() -> List[str]:
    ensure_dirs()
    names = []
    for filename in sorted(os.listdir(USERS_DIR)):
        if filename.endswith(".json"):
            names.append(filename[:-5])
    return names


def load_user_data(user: User) -> None:
    ensure_dirs()
    path = _user_file(user.name)
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return
            data = json.loads(content)
    except (json.JSONDecodeError, IOError):
        return

    user.wardrobe.clear()
    user.outfits.clear()

    if "categories" in data and data["categories"]:
        from models.category import Category
        user.categories = [
            Category.from_data(c) for c in data["categories"]
        ]
    else:
        from models.category import Category
        user.categories = Category.get_default_categories()

    for item_data in data.get("wardrobe", []):
        item = ClothingItem.from_data(item_data, user.categories)
        user.add_clothing(item)

    for outfit_data in data.get("outfits", []):
        outfit = Outfit.from_data(outfit_data, user.wardrobe)
        user.add_outfit(outfit)


def save_user_data(user: User) -> None:
    ensure_dirs()
    data = {
        "user": user.to_dict(),
        "categories": [c.to_dict() for c in user.categories],
        "wardrobe": [item.to_dict() for item in user.wardrobe],
        "outfits": [outfit.to_dict() for outfit in user.outfits],
    }
    with open(_user_file(user.name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def user_exists(name: str) -> bool:
    return os.path.exists(_user_file(name))
