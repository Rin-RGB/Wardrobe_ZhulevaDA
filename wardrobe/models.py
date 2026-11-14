from django.db import models
from django.utils.text import slugify
from accounts.models import WardrobeUser


class SeasonChoices(models.TextChoices):
    SUMMER = 'summer', 'Лето'
    WINTER = 'winter', 'Зима'
    DEMISEASON = 'demiseason', 'Демисезон'
    ALL_SEASON = 'all_season', 'Всесезон'


class StyleChoices(models.TextChoices):
    CASUAL = 'casual', 'Повседневный'
    FORMAL = 'formal', 'Деловой'
    SPORT = 'sport', 'Спортивный'
    STREET = 'street', 'Уличный'
    CLASSIC = 'classic', 'Классический'
    ROMANTIC = 'romantic', 'Романтический'


class ClothingItemQuerySet(models.QuerySet):
    """Кастомный QuerySet для фильтрации вещей (Критерий 9)"""

    def for_season(self, season):
        return self.filter(season=season)

    def by_style(self, style):
        return self.filter(style=style)

    def in_stock(self):
        return self.filter(quantity__gt=0)


class ClothingItemManager(models.Manager):
    """Кастомный менеджер, подключающий QuerySet"""

    def get_queryset(self):
        return ClothingItemQuerySet(self.model, using=self._db)

    def for_season(self, season):
        return self.get_queryset().for_season(season)

    def by_style(self, style):
        return self.get_queryset().by_style(style)


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
    slug = models.SlugField("URL-адрес", max_length=100, unique=True, blank=True)  # Критерий 15
    color = models.CharField("Цвет", max_length=50)
    season = models.CharField(
        "Сезон",
        max_length=20,
        choices=SeasonChoices.choices,
        default=SeasonChoices.ALL_SEASON,
    )
    style = models.CharField(
        "Стиль",
        max_length=20,
        choices=StyleChoices.choices,
        default=StyleChoices.CASUAL,
    )
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    objects = ClothingItemManager()  # Подключение кастомного менеджера

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"
        ordering = ["user", "category", "name"]

    def __str__(self):
        return f"{self.name} ({self.user.name})"

    def save(self, *args, **kwargs):
        """Автогенерация уникального slug с поддержкой кириллицы."""
        if not self.slug or self.slug.startswith('-'):
            # Генерируем базовый slug
            base_slug = slugify(self.name, allow_unicode=True)
            if not base_slug:
                base_slug = f"item-{self.pk or 'new'}"

            slug = base_slug
            counter = 1
            # Проверяем уникальность, исключая текущий объект
            while ClothingItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Возвращает URL для детальной страницы вещи (Критерий 15)"""
        from django.urls import reverse
        return reverse('wardrobe:item_detail', kwargs={'slug': self.slug})

    @property
    def total_cost(self):
        """Общая стоимость позиции (цена × количество)."""
        return float(self.price) * self.quantity

    @property
    def season_display_ru(self):
        return SeasonChoices(self.season).label

    @property
    def style_display_ru(self):
        return StyleChoices(self.style).label

    def get_price_category(self):
        if self.price <= 0:
            return "неизвестно"
        if self.price < 1000:
            return "эконом"
        if self.price < 5000:
            return "средний"
        return "премиум"
