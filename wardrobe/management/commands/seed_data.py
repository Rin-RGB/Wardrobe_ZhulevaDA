from django.core.management.base import BaseCommand
from accounts.models import WardrobeUser
from wardrobe.models import Category, ClothingItem
from outfits.models import Outfit


class Command(BaseCommand):
    help = 'Заполнить БД начальными данными'

    def handle(self, *args, **options):
        # Категории
        top, _ = Category.objects.get_or_create(name='верх')
        bottom, _ = Category.objects.get_or_create(name='низ')
        shoes, _ = Category.objects.get_or_create(name='обувь')
        Category.objects.get_or_create(name='аксессуар')

        # Пользователи
        anna, _ = WardrobeUser.objects.get_or_create(
            name='Анна', email='anna@example.com',
        )
        WardrobeUser.objects.get_or_create(
            name='Иван', email='ivan@example.com',
        )

        # Вещи Анны
        tshirt = ClothingItem.objects.create(
            user=anna, category=top, name='Футболка',
            color='белый', season='summer', style='casual',
            price=800, quantity=3,
        )
        jeans = ClothingItem.objects.create(
            user=anna, category=bottom, name='Джинсы',
            color='синий', season='demiseason', style='casual',
            price=3500, quantity=2,
        )
        ClothingItem.objects.create(
            user=anna, category=shoes, name='Зимние ботинки',
            color='чёрный', season='winter', style='casual',
            price=8500, quantity=1,
        )

        # Вещи Ивана
        ClothingItem.objects.create(
            user=anna, category=top, name='Рубашка',
            color='голубой', season='all_season', style='formal',
            price=4500, quantity=1,
        )
        ClothingItem.objects.create(
            user=anna, category=bottom, name='Брюки',
            color='чёрный', season='all_season', style='formal',
            price=6000, quantity=1,
        )

        # Образ Анны
        outfit = Outfit.objects.create(
            user=anna, name='Повседневный летний',
            occasion='casual', season='лето',
        )
        outfit.items.add(tshirt, jeans)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
