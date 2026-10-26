from django.db import models

from accounts.models import WardrobeUser
from wardrobe.models import ClothingItem


class Outfit(models.Model):
    """Образ — комплект вещей пользователя."""

    OCCASION_CHOICES = [
        ("casual", "Повседневный"),
        ("business", "Деловой"),
        ("evening", "Вечерний"),
        ("sport", "Спортивный"),
        ("festive", "Праздничный"),
    ]

    user = models.ForeignKey(
        WardrobeUser,
        on_delete=models.CASCADE,
        related_name="outfits",
        verbose_name="Владелец",
    )
    name = models.CharField("Название", max_length=100)
    occasion = models.CharField(
        "Повод",
        max_length=20,
        choices=OCCASION_CHOICES,
        default="casual",
    )
    season = models.CharField("Сезон", max_length=50, default="всесезон")
    items = models.ManyToManyField(
        ClothingItem,
        related_name="in_outfits",
        verbose_name="Вещи",
        blank=True,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Образ"
        verbose_name_plural = "Образы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.user.name})"

    @property
    def total_cost(self):
        return sum(item.price for item in self.items.all())

    @property
    def is_complete(self):
        """Образ полный, если есть верх и низ."""
        categories = {
            item.category.name if item.category else None for item in self.items.all()
        }
        return "верх" in categories and "низ" in categories
