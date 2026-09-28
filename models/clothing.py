from typing import List
from .category import Category


class ClothingItem:
    """Единица одежды в гардеробе пользователя."""

    VALID_SEASONS = ("лето", "зима", "демисезон", "всесезон")
    VALID_STYLES = (
        "повседневный", "деловой", "спортивный",
        "уличный", "классический", "романтический",
    )

    def __init__(
        self,
        item_id: int,
        name: str,
        category: Category,
        color: str,
        season: str,
        price: float,
        quantity: int = 1,
        style: str = "повседневный",
    ) -> None:
        self.id = item_id
        self.name = name
        self.category = category
        self.color = color
        self.season = season
        self.price = price
        self.quantity = quantity
        self.style = style

    @property
    def total_cost(self) -> float:
        return self.price * self.quantity

    def is_suitable_for_season(self, current_season: str) -> bool:
        if self.season == "всесезон":
            return True
        if self.season == current_season:
            return True
        if self.season == "демисезон" and current_season in ("весна", "осень"):
            return True
        return False

    def is_suitable_for_occasion(self, occasion: str) -> bool:
        mapping = {
            "повседневный": ("повседневный", "уличный"),
            "деловой": ("деловой", "классический"),
            "вечерний": ("деловой", "романтический", "классический"),
            "спортивный": ("спортивный",),
            "праздничный": ("романтический", "классический", "деловой"),
        }
        allowed = mapping.get(occasion, ())
        return self.style in allowed

    def get_price_category(self) -> str:
        if self.price <= 0:
            return "неизвестно"
        if self.price < 1000:
            return "эконом"
        if self.price < 5000:
            return "средний"
        return "премиум"

    def is_similar_to(self, other: "ClothingItem") -> bool:
        return (
            self.name.lower() == other.name.lower()
            and self.category == other.category
            and self.color.lower() == other.color.lower()
            and self.season == other.season
            and self.style == other.style
        )

    def __str__(self) -> str:
        return (
            f"{self.name} | {self.category} | {self.color} | "
            f"{self.season} | стиль: {self.style} | "
            f"{self.price:.2f} руб. x {self.quantity}"
        )

    def __repr__(self) -> str:
        return f"ClothingItem({self.id}, '{self.name}')"

    @classmethod
    def from_data(
        cls, data: dict, categories: List[Category]
    ) -> "ClothingItem":
        category = next(
            (
                c for c in categories
                if c.name == data.get("category", "прочее")
            ),
            Category(-1, "прочее"),
        )
        return cls(
            item_id=data["id"],
            name=data["name"],
            category=category,
            color=data["color"],
            season=data["season"],
            price=data["price"],
            quantity=data.get("quantity", 1),
            style=data.get("style", "повседневный"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.name,
            "color": self.color,
            "season": self.season,
            "price": self.price,
            "quantity": self.quantity,
            "style": self.style,
        }
