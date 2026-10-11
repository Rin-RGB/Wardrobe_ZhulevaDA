from django.test import TestCase
from accounts.models import WardrobeUser
from .models import Category, ClothingItem


class CategoryModelTest(TestCase):
    def test_create_category(self):
        cat = Category.objects.create(name='верх')
        self.assertEqual(cat.name, 'верх')
        self.assertEqual(str(cat), 'Верх')


class ClothingItemModelTest(TestCase):
    def setUp(self):
        self.user = WardrobeUser.objects.create(
            name='Тест', email='test@test.ru',
        )
        self.category = Category.objects.create(name='верх')

    def test_create_item(self):
        item = ClothingItem.objects.create(
            user=self.user,
            category=self.category,
            name='Футболка',
            color='белый',
            season='summer',
            price=1000,
            quantity=2,
        )
        self.assertEqual(item.name, 'Футболка')
        self.assertEqual(item.total_cost, 2000)

    def test_price_category(self):
        cheap = ClothingItem.objects.create(
            user=self.user, category=self.category,
            name='A', color='x', season='summer', price=500,
        )
        mid = ClothingItem.objects.create(
            user=self.user, category=self.category,
            name='B', color='x', season='summer', price=3000,
        )
        expensive = ClothingItem.objects.create(
            user=self.user, category=self.category,
            name='C', color='x', season='summer', price=8000,
        )
        self.assertEqual(cheap.get_price_category(), 'эконом')
        self.assertEqual(mid.get_price_category(), 'средний')
        self.assertEqual(expensive.get_price_category(), 'премиум')