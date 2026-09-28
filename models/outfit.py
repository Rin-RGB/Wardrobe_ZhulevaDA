from typing import List
from .clothing import ClothingItem


class Outfit:
    """Образ — комплект одежды из нескольких вещей."""

    VALID_OCCASIONS = (
        "повседневный", "деловой", "вечерний",
        "спортивный", "праздничный",
    )

    def __init__(
        self,
        outfit_id: int,
        name: str,
        occasion: str = "повседневный",
        season: str = "всесезон",
    ) -> None:
        self.id = outfit_id
        self.name = name
        self.occasion = occasion
        self.season = season
        self.items: List[ClothingItem] = []

    def add_item(self, item: ClothingItem) -> None:
        if item not in self.items:
            self.items.append(item)

    def remove_item(self, item: ClothingItem) -> bool:
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def has_category(self, category_name: str) -> bool:
        return any(
            item.category.name == category_name for item in self.items
        )

    def is_complete(self) -> bool:
        return self.has_category("верх") and self.has_category("низ")

    def get_total_cost(self) -> float:
        return sum(item.price for item in self.items)

    def __str__(self) -> str:
        status = "полный" if self.is_complete() else "неполный"
        items_str = (
            ", ".join(item.name for item in self.items)
            if self.items else "пусто"
        )
        return (
            f"{self.name} ({self.occasion}, {self.season}) [{status}]\n"
            f"   Вещи: {items_str} | "
            f"Стоимость: {self.get_total_cost():.2f} руб."
        )

    def __repr__(self) -> str:
        return f"Outfit({self.id}, '{self.name}')"

    @classmethod
    def from_data(
        cls, data: dict, wardrobe: List[ClothingItem]
    ) -> "Outfit":
        outfit = cls(
            outfit_id=data["id"],
            name=data["name"],
            occasion=data.get("occasion", "повседневный"),
            season=data.get("season", "всесезон"),
        )
        for item_id in data.get("item_ids", []):
            item = next((i for i in wardrobe if i.id == item_id), None)
            if item:
                outfit.add_item(item)
        return outfit

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "occasion": self.occasion,
            "season": self.season,
            "item_ids": [item.id for item in self.items],
        }
