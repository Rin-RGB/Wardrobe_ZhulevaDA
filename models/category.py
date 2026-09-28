from typing import List


class Category:
    """Категория одежды — полноценная сущность."""

    def __init__(self, category_id: int, name: str) -> None:
        self.id = category_id
        self.name = name.lower()

    def rename(self, new_name: str) -> None:
        self.name = new_name.lower()

    def __str__(self) -> str:
        return self.name.capitalize()

    def __repr__(self) -> str:
        return f"Category({self.id}, '{self.name}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Category):
            return self.name == other.name
        return False

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        return cls(category_id=data["id"], name=data["name"])

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @staticmethod
    def get_default_categories() -> List["Category"]:
        """Стандартные категории для нового пользователя."""
        return [
            Category(1, "верх"),
            Category(2, "низ"),
            Category(3, "обувь"),
            Category(4, "аксессуар"),
        ]
