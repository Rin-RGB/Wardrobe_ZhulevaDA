from django.test import TestCase
from .models import WardrobeUser


class WardrobeUserModelTest(TestCase):
    def test_create_user(self):
        user = WardrobeUser.objects.create(
            name='Тест', email='test@test.ru',
        )
        self.assertEqual(user.name, 'Тест')
        self.assertEqual(user.email, 'test@test.ru')

    def test_user_str(self):
        user = WardrobeUser.objects.create(
            name='Тест', email='test@test.ru',
        )
        self.assertEqual(str(user), 'Тест')

    def test_empty_wardrobe_cost(self):
        user = WardrobeUser.objects.create(
            name='Тест', email='test@test.ru',
        )
        self.assertEqual(user.get_wardrobe_cost(), 0)
        self.assertEqual(user.get_items_count(), 0)
