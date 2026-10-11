from django.db import models


class WardrobeUser(models.Model):
    """Пользователь системы — владелец гардероба и образов."""
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email', unique=True)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_wardrobe_cost(self):
        """Общая стоимость гардероба пользователя."""
        return sum(item.total_cost for item in self.clothing_items.all())

    def get_items_count(self):
        """Общее количество вещей (с учётом quantity)."""
        return sum(item.quantity for item in self.clothing_items.all())
