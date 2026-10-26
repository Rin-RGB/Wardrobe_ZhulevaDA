from django.db import models

from accounts.models import WardrobeUser


class Category(models.Model):
    """Категория одежды (верх, низ, обувь и т. п.)."""

    name = models.CharField("Название", max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name.capitalize()


class ClothingItem(models.Model):
    """Единица одежды. Принадлежит пользователю через ForeignKey."""

    SEASON_CHOICES = [
        ("summer", "Лето"),
        ("winter", "Зима"),
        ("demiseason", "Демисезон"),
        ("all_season", "Всесезон"),
    ]
    STYLE_CHOICES = [
        ("casual", "Повседневный"),
        ("formal", "Деловой"),
        ("sport", "Спортивный"),
        ("street", "Уличный"),
        ("classic", "Классический"),
        ("romantic", "Романтический"),
    ]

    user = models.ForeignKey(
        WardrobeUser,
        on_delete=models.CASCADE,
        related_name="clothing_items",
        verbose_name="Владелец",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="items",
        verbose_name="Категория",
    )
    name = models.CharField("Название", max_length=100)
    color = models.CharField("Цвет", max_length=50)
    season = models.CharField(
        "Сезон",
        max_length=20,
        choices=SEASON_CHOICES,
        default="all_season",
    )
    style = models.CharField(
        "Стиль",
        max_length=20,
        choices=STYLE_CHOICES,
        default="casual",
    )
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"
        ordering = ["user", "category", "name"]

    def __str__(self):
        return f"{self.name} ({self.user.name})"

    @property
    def total_cost(self):
        """Общая стоимость позиции (цена × количество)."""
        return float(self.price) * self.quantity

    @property
    def season_display_ru(self):
        return dict(self.SEASON_CHOICES).get(self.season, self.season)

    @property
    def style_display_ru(self):
        return dict(self.STYLE_CHOICES).get(self.style, self.style)

    def get_price_category(self):
        if self.price <= 0:
            return "неизвестно"
        if self.price < 1000:
            return "эконом"
        if self.price < 5000:
            return "средний"
        return "премиум"
