from django.db import models
from django.utils.text import slugify
from accounts.models import WardrobeUser
from wardrobe.models import ClothingItem


class OccasionChoices(models.TextChoices):
    CASUAL = 'casual', 'Повседневный'
    BUSINESS = 'business', 'Деловой'
    EVENING = 'evening', 'Вечерний'
    SPORT = 'sport', 'Спортивный'
    FESTIVE = 'festive', 'Праздничный'


class Outfit(models.Model):
    """Образ — комплект вещей пользователя."""
    user = models.ForeignKey(
        WardrobeUser,
        on_delete=models.CASCADE,
        related_name="outfits",
        verbose_name="Владелец",
    )
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("URL-адрес", max_length=100, unique=True, blank=True)
    occasion = models.CharField(
        "Повод",
        max_length=20,
        choices=OccasionChoices.choices,
        default=OccasionChoices.CASUAL,
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

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.startswith('-'):
            base_slug = slugify(self.name, allow_unicode=True)
            if not base_slug:
                base_slug = f"outfit-{self.pk or 'new'}"

            slug = base_slug
            counter = 1
            while Outfit.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('outfits:outfit_detail', kwargs={'slug': self.slug})

    @property
    def total_cost(self):
        return sum(item.price for item in self.items.all())

    @property
    def is_complete(self):
        """Образ полный, если есть верх и низ."""
        categories = {
            item.category.name.lower() if item.category else None for item in self.items.all()
        }
        return "верх" in categories and "низ" in categories