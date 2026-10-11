from django.test import TestCase
from accounts.models import WardrobeUser
from wardrobe.models import Category, ClothingItem
from .models import Outfit


class OutfitModelTest(TestCase):
    def setUp(self):
        self.user = WardrobeUser.objects.create(
            name='Тест', email='test@test.ru',
        )
        self.top = Category.objects.create(name='верх')
        self.bottom = Category.objects.create(name='низ')
        self.tshirt = ClothingItem.objects.create(
            user=self.user, category=self.top,
            name='Футболка', color='белый',
            season='summer', price=1000,
        )
        self.jeans = ClothingItem.objects.create(
            user=self.user, category=self.bottom,
            name='Джинсы', color='синий',
            season='demiseason', price=3000,
        )

    def test_create_outfit(self):
        outfit = Outfit.objects.create(
            user=self.user, name='Летний',
            occasion='casual', season='лето',
        )
        outfit.items.add(self.tshirt, self.jeans)
        self.assertEqual(outfit.name, 'Летний')
        self.assertEqual(outfit.items.count(), 2)
        self.assertEqual(outfit.total_cost, 4000)

    def test_complete_outfit(self):
        outfit = Outfit.objects.create(
            user=self.user, name='Полный',
            occasion='casual', season='лето',
        )
        outfit.items.add(self.tshirt, self.jeans)
        self.assertTrue(outfit.is_complete)

    def test_incomplete_outfit(self):
        outfit = Outfit.objects.create(
            user=self.user, name='Неполный',
            occasion='casual', season='лето',
        )
        outfit.items.add(self.tshirt)
        self.assertFalse(outfit.is_complete)