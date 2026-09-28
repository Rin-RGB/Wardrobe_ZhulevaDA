from typing import List, Optional
from .category import Category
from .clothing import ClothingItem
from .outfit import Outfit


class User:
    def __init__(
        self,
        user_id: int = 1,
        name: str = "Пользователь",
    ) -> None:
        self.id = user_id
        self.name = name
        self.wardrobe: List[ClothingItem] = []
        self.outfits: List[Outfit] = []
        self.categories: List[Category] = Category.get_default_categories()

    def add_clothing(self, item: ClothingItem) -> None:
        self.wardrobe.append(item)

    def find_similar(self, item: ClothingItem) -> Optional[ClothingItem]:
        for existing in self.wardrobe:
            if existing.is_similar_to(item):
                return existing
        return None

    def remove_clothing_one(self, item_id: int) -> bool:
        for i, item in enumerate(self.wardrobe):
            if item.id == item_id:
                if item.quantity > 1:
                    item.quantity -= 1
                    return False
                self.wardrobe.pop(i)
                return True
        return False

    def find_clothing_by_id(self, item_id: int) -> Optional[ClothingItem]:
        return next((i for i in self.wardrobe if i.id == item_id), None)

    def add_outfit(self, outfit: Outfit) -> None:
        self.outfits.append(outfit)

    def remove_outfit(self, outfit_id: int) -> Optional[Outfit]:
        for i, outfit in enumerate(self.outfits):
            if outfit.id == outfit_id:
                return self.outfits.pop(i)
        return None

    def get_wardrobe_cost(self) -> float:
        return sum(item.total_cost for item in self.wardrobe)

    def get_next_item_id(self) -> int:
        if not self.wardrobe:
            return 1
        return max(item.id for item in self.wardrobe) + 1

    def get_next_outfit_id(self) -> int:
        if not self.outfits:
            return 1
        return max(o.id for o in self.outfits) + 1

    def suggest_outfit(
        self, season: str, occasion: str = "повседневный"
    ) -> Optional[Outfit]:
        suitable = [
            item for item in self.wardrobe
            if item.is_suitable_for_season(season)
            and item.is_suitable_for_occasion(occasion)
        ]
        if not suitable:
            return None

        outfit = Outfit(
            outfit_id=self.get_next_outfit_id(),
            name=f"Авто-образ ({season}, {occasion})",
            occasion=occasion,
            season=season,
        )

        added_categories = set()
        for item in suitable:
            if item.category.name not in added_categories:
                outfit.add_item(item)
                added_categories.add(item.category.name)
            if outfit.is_complete():
                break

        return outfit

    def add_category(self, name: str) -> Optional[Category]:
        name_lower = name.lower()
        if any(c.name == name_lower for c in self.categories):
            return None
        new_id = self.get_next_category_id()
        category = Category(new_id, name_lower)
        self.categories.append(category)
        return category

    def remove_category(self, category_id: int) -> bool:
        for i, cat in enumerate(self.categories):
            if cat.id == category_id:
                if any(
                    item.category.id == category_id
                    for item in self.wardrobe
                ):
                    return False
                self.categories.pop(i)
                return True
        return False

    def find_category_by_id(self, category_id: int) -> Optional[Category]:
        return next(
            (c for c in self.categories if c.id == category_id), None
        )

    def find_category_by_name(self, name: str) -> Optional[Category]:
        return next(
            (c for c in self.categories if c.name == name.lower()), None
        )

    def get_next_category_id(self) -> int:
        if not self.categories:
            return 1
        return max(c.id for c in self.categories) + 1

    def __str__(self) -> str:
        return (
            f"{self.name} | Вещей: {len(self.wardrobe)} | "
            f"Образов: {len(self.outfits)} | "
            f"Стоимость: {self.get_wardrobe_cost():.2f} руб."
        )

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_data(cls, data: dict) -> "User":
        return cls(
            user_id=data.get("id", 1),
            name=data.get("name", "Пользователь"),
        )
